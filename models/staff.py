from pydantic import BaseModel, constr

class Staff(BaseModel):
        role: str
        name: constr(max_length=8, pattern="^[A-za-z]*$")