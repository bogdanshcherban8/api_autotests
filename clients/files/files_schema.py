from pydantic import BaseModel, HttpUrl, Field


class CreateFileRequestSchema(BaseModel):
    filename: str = Field(default="image.jpg")
    directory: str = Field(default="testdata")
    upload_file: str = Field(default = "./testdata/image.jpg")


class FileSchema(BaseModel):
    id: str
    filename: str
    directory: str
    url: HttpUrl


class CreateFileResponseSchema(BaseModel):
    file: FileSchema


class GetFileResponseSchema(BaseModel):
    file: FileSchema


