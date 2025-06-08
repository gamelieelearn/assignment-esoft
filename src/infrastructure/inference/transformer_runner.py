import io
import os

import requests
import torch
from PIL import Image
from transformers import AutoModelForImageClassification, AutoProcessor


class SimpleTransformerRunner:
    """Run model from huggingface"""

    def __init__(self, model_name: str):
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model = AutoModelForImageClassification.from_pretrained(model_name)

    def predict(self, batch: list[bytes]) -> list[str]:
        """
        input_data: list of image bytes
        Returns: list of predicted labels
        """
        if len(batch) == 0:
            return []
        images = [Image.open(io.BytesIO(img_bytes)).convert('RGB') for img_bytes in batch]
        inputs = self.processor(images=images, return_tensors='pt')
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            predicted_class_idxs = logits.argmax(-1).tolist()
            labels = [self.model.config.id2label[idx] for idx in predicted_class_idxs]
            print(f'Predicted classes: {labels}')
            return labels


if __name__ == '__main__':
    image_path = 'test/artifacts/example_image.jpg'

    if not os.path.exists(image_path):
        url = 'https://images.pexels.com/photos/45201/kitty-cat-kitten-pet-45201.jpeg'
        img_data = requests.get(url).content
        with open(image_path, 'wb') as handler:
            handler.write(img_data)
        print(f'Downloaded example image to {image_path}')

    simple_transformer_runner = SimpleTransformerRunner(
        model_name='akahana/vit-base-cats-vs-dogs',
    )

    # Example usage for batch
    with open(image_path, 'rb') as f:
        img_bytes = f.read()
    result = simple_transformer_runner.predict([img_bytes, img_bytes])
    print(f'Result: {result}')
