from fastapi import FastAPI, Body, Depends, HTTPException, status
from model import UserSchema, UserLoginSchema, Plate
from auth.jwt_handler import sign_jwt, decode_jwt
from auth.jwt_bearer import jwtBearer
from random import choice
import database
import uuid
import re

# Структура данных:
# {
#    uid: 'uuid',
#    plate: 'A123AA',
# }

users = []

#regular expression for russian auto plates


alphabet = ['А', 'В', 'Е', 'К', 'М', 'Н', 'О', 'Р', 'С', 'Т', 'У', 'Х']
digits = ["0","1","2","3","4","5","6","7","8","9"]

def generator():
    return choice(alphabet) + choice(digits) + choice(digits) + choice(digits) + choice(alphabet) + choice(alphabet)


app = FastAPI()

@app.get("/")
def home():
    return {"Hello": "World!"}

@app.get("/users", dependencies=[Depends(jwtBearer())], tags = ["users"])
def read_users():
    print(users)
    return users

@app.get("/plates", dependencies=[Depends(jwtBearer())], tags = ["plates"])
def read_plates():
    all_plate = []
    plate_data = database.get_all_records()
    for plate in plate_data:
        all_plate.append({"uid": plate["uid"], "plate": plate['plate']})
    return all_plate

@app.get("/plate/get/{uid}", dependencies=[Depends(jwtBearer())], tags = ["plates"])
def get_plate(uid: str):
    is_return = False
    plate_data = database.get_all_records()
    for plate in plate_data:
        if plate['uid'] == uid:
            return {"plate": plate['plate']}
            is_return = True
    if not is_return:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plate not found"
        )

@app.get("/plate/generate/", dependencies=[Depends(jwtBearer())], tags = ["plates"])
def generate_plate():
    amount = 1
    plate_data = database.get_all_records()
    plates = []
    all_plate = []
    insert_list = []
    for plate in plate_data:
        all_plate.append(plate['plate'])
    i = 0
    while i < amount:
        new_plate = generator()
        if new_plate not in all_plate:
            all_plate.append(new_plate)
            plates.append(new_plate)
            insert_list.append({"uid": str(uuid.uuid4()),"plate": new_plate})
            i += 1
    database.insert_many_records(insert_list)
    return {"plates": plates}

@app.get("/plate/generate/{amount}", dependencies=[Depends(jwtBearer())], tags = ["plates"]) #dependencies=[Depends(jwtBearer())],
def generate_plate(amount: int):
    if amount < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Amount must be greater than 0"
        )
    else:
        plate_data = database.get_all_records()
        plates = []
        all_plate = []
        insert_list = []
        for plate in plate_data:
            all_plate.append(plate['plate'])
        i = 0
        while i < amount:
            new_plate = generator()
            if new_plate not in all_plate:
                all_plate.append(new_plate)
                plates.append(new_plate)
                insert_list.append({"uid": str(uuid.uuid4()),"plate": new_plate})
                i += 1
        database.insert_many_records(insert_list)
        return {"plates": plates}
    
@app.post("/plate/add", dependencies=[Depends(jwtBearer())], tags = ["plates"])
def add_plate(plate: Plate = Body(default=None)):
    if re.match("[АВЕКМНОРСТУХ]{1}[0-9]{3}[АВЕКМНОРСТУХ]{2}", plate.plate):
        all_plate = []
        plate_data = database.get_all_records()
        for one_plate in plate_data:
            all_plate.append(one_plate['plate'])
        if plate.plate not in all_plate:
            database.insert_record({"uid": str(uuid.uuid4()),"plate": plate.plate})
            return {"Added": plate.plate}
        else:
            return {"This plate already exists"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid plate"
        )
        
@app.post("/user/signup", tags = ["users"])
def user_signup(user: UserSchema = Body(default=None)):
    users.append(user)
    return sign_jwt(user.email)

def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        else:
            return False
        
@app.post("/user/login", tags = ["users"])
def user_login(data: UserLoginSchema = Body(default=None)):
    if check_user(data):
        return sign_jwt(data.email)
    else:
        return {"error": "Invalid credentials"}