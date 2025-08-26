from pydantic import BaseModel, HttpUrl, Field

from config import settings


class CreateFileRequestSchema(BaseModel):
    filename: str = Field(default="image.jpg")
    directory: str = Field(default="testdata")
    upload_file: str = Field(default = settings.test_data.image_jpg_file)


class FileSchema(BaseModel):
    id: str
    filename: str
    directory: str
    url: HttpUrl


class CreateFileResponseSchema(BaseModel):
    file: FileSchema


class GetFileResponseSchema(BaseModel):
    file: FileSchema


