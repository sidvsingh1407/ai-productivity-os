from pydantic import BaseModel, ConfigDict
from users.schemas import UserResponse
from organizations.schemas import OrgResponse

class AuthResponse(BaseModel):
    user: UserResponse
    org: OrgResponse
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(from_attributes=True)
