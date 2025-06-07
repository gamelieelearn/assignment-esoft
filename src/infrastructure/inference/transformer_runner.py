import os

import requests
import torch
from PIL import Image
from transformers import AutoModelForImageClassification, AutoProcessor

from src.domain.ports import ModelRunner


class SimpleTransformerRunner(ModelRunner):
    """Run model from huggingface"""

    def __init__(self, model_name: str):
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model = AutoModelForImageClassification.from_pretrained(model_name)

    def predict(self, input_data):
        image_path = input_data
        image = Image.open(image_path).convert('RGB')
        inputs = self.processor(images=image, return_tensors='pt')
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            print(f'{logits=}')
            predicted_class_idx = logits.argmax(-1).item()
            label = self.model.config.id2label[predicted_class_idx]
            print(f'Predicted class: {label}')
            return label


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

    result = simple_transformer_runner.predict(image_path)
    print(f'Result: {result}')
