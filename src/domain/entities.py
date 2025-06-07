from pydantic import BaseModel


class InputModel(BaseModel):
    bucket: str
    key: str


class InferOut(BaseModel):
    class_name: str


class OutputModel(BaseModel):
    input: InputModel
    result: InferOut


class InferIn(BaseModel):
    image: bytes
