from pydantic import ConfigDict, BaseModel, Field
from pydantic.alias_generators import to_camel




class TokenSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    token_type: str
    access_token: str
    refresh_token: str


class LoginResponseSchema(BaseModel):
    token: TokenSchema


class LoginRequestSchema(BaseModel):
    email: str = Field(default="user@example.com")
    password: str = Field(default="string")


class RefreshRequestSchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    refresh_token: str

class RefreshResponseSchema(BaseModel):
    token: TokenSchema