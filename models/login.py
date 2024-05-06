from pydantic import BaseModel, constr

class Login(BaseModel):
        role: str
        userid: constr(max_length=8, pattern="^[A-Z0-9]*$")
        pwd: constr(min_length=8,max_length=8)