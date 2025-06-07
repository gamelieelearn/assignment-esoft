import os

import pytest

from src.infrastructure.inference.transformer_runner import SimpleTransformerRunner


class TestSimpleTransformerRunner:
    @pytest.fixture(scope='class')
    def example_image_bytes(self):
        image_path = os.path.join(os.path.dirname(__file__), '../../artifacts/example_image.jpg')
        image_path = os.path.abspath(image_path)
        if not os.path.exists(image_path):
            pytest.skip('Example image not found for transformer runner test.')
        with open(image_path, 'rb') as f:
            return f.read()

    def test_predict_cats_vs_dogs(self, example_image_bytes):
        runner = SimpleTransformerRunner('akahana/vit-base-cats-vs-dogs')
        # Run prediction on a batch of two identical images
        result = runner.predict([example_image_bytes, example_image_bytes])
        assert isinstance(result, list)
        assert len(result) == 2
        # The model should predict either 'cat' or 'dog' for each image
        for label in result:
            assert label in {'cat', 'dog'}
