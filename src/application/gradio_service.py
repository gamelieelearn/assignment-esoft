import base64
import io
import uuid
from typing import Dict, List

import gradio as gr

from src.domain.entities import OutputModel
from src.domain.ports import MessageBus, S3Compatible


class GradioService:
    def __init__(self, bus_in: MessageBus, s3: S3Compatible, bus_out: MessageBus, bucket_name: str):
        self.s3 = s3
        self.bus_in = bus_in
        self.bus_out = bus_out
        self.bucket = bucket_name
        self.results: List[Dict] = []  # Store dicts: {key, prediction, image_bytes}

    def upload_image(self, image):
        buf = io.BytesIO()
        image.save(buf, format='JPEG')
        image_bytes = buf.getvalue()
        key = f'gradio_uploads/{uuid.uuid4().hex}.jpg'
        self.s3.store(key, image_bytes, self.bucket)
        self.bus_in.send({'bucket': self.bucket, 'key': key})
        return f'Image uploaded. Key: {key}'

    def poll_results(self) -> None:
        raw_messages = self.bus_out.receive(max_messages=10, wait_time_seconds=2, delete_after_polling=False)
        messages = [OutputModel.model_validate_json(msg) for msg in raw_messages]
        for msg in messages:
            try:
                image_bytes = self.s3.retrieve(key=msg.input.key, bucket=msg.input.bucket)
            except Exception:
                image_bytes = None
            pred = msg.result.class_name
            row = {'image': image_bytes, 'key': msg.input.key, 'prediction': pred}
            self.results.append(row)
        self.results = self.results[-10:]

    def get_gradio_interface(self):
        with gr.Blocks() as demo:
            with gr.Row():
                with gr.Column():
                    image_input = gr.Image(type='pil', label='Upload Image')
                    upload_btn = gr.Button('Upload')
                    upload_output = gr.Textbox(label='Upload Status')
                with gr.Column():
                    refresh_btn = gr.Button('Refresh')
                    table_html = gr.HTML(label='Results Table')
            upload_btn.click(self.upload_image, inputs=image_input, outputs=upload_output)

            def update_table():
                self.poll_results()
                # Build HTML table
                html = '<table border="1" style="width:100%; text-align:center;">'
                html += '<tr><th>Image</th><th>Prediction</th></tr>'
                for row in self.results:
                    if (img := row['image']) is not None:
                        img_b64 = base64.b64encode(img).decode('utf-8')
                        img_tag = (
                            f'<img src="data:image/jpeg;base64,{img_b64}" style="max-height:100px; max-width:100px;" />'
                        )
                    else:
                        img_tag = ''
                    pred = row['prediction']
                    html += f'<tr><td>{img_tag}</td><td>{pred}</td></tr>'
                html += '</table>'
                return html

            refresh_btn.click(update_table, outputs=table_html)
            demo.load(update_table, outputs=table_html)
        return demo

    def run_forever(self):
        self.get_gradio_interface().launch()
