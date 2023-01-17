from pydantic import BaseModel, Field, EmailStr

class UserSchema(BaseModel):
    full_name: str = Field(default=None)
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)
    
    class Config:
        the_schema = {
            'user_demo': {
                'full_name': 'Danya',
                'email': 'vakdan555@gmail.com',
                'password': '12345'
            }
        }
        
        
class UserLoginSchema(BaseModel):
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)
    
    class Config:
        the_schema = {
            'user_demo': {
                'email': 'valdan555@gmail.com',
                'password': '12345'
            }
        }
        
class Plate(BaseModel):
    plate: str = Field(default=None)
    
    class Config:
        the_schema = {
            'plate_demo': {
                'plate': 'A123AA'
            }
        }