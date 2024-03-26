from pydantic import BaseModel, Field
from datetime import datetime,date
from typing import List, Optional

class RegisterSuperAdmin(BaseModel):
    username: str
    password: str
    email: str
    role: str
    
class PostAdmin(BaseModel):
    username: str
    email: str
    password: str

class GetAdmin(BaseModel):
    id: int
    username: str
    email: str
    class ConfigDict:
        from_attributes = True


class PostCategory(BaseModel):
    category: str

class GetCategory(BaseModel):
    id: int
    category: str 
    class ConfigDict:
        from_attributes = True

class GetEvent(BaseModel):
    event: str
    date: date
    users: GetAdmin | None
    categories: List[GetCategory] | None
    class ConfigDict:
        from_attributes = True

class PostEvents(BaseModel):
    event: str
    date: date
    user_id: int
    categories: GetCategory
    class ConfigDict:
        from_attributes = True


class PostUser(PostAdmin):
    events: PostEvents

    class ConfigDict:
        from_attributes = True

class GetAllAdmins(GetAdmin):
    events: List[PostAdmin] | None

    class ConfigDict:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    username: str


class UserAuth(BaseModel):
    id: int
    username: str
    email: str
    role: str

class UsersPics(BaseModel):
    image_name: str
    events: GetEvent | None
    class ConfigDict:
        from_attributes = True

class DownloadPics(BaseModel):
    images: List[str]


class OthesUserInfo(BaseModel):
    device_name: str
    device_ip: str
    event_id: str