'''
 @GladisValenzuela
 DataScientest MLOps Training Project
 Creation date: January 2023
'''

import os
import util
import torch
import bcrypt
import mysql.connector

from saver.model_saver import ModelSaver
from termcolor import colored
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends, HTTPBasic, HTTPBasicCredentials, status, UploadFile, File


app = FastAPI(
    title="Pulmonary Embolism - DataScientest MLOps Training Project")


required_envs = ['DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']

for env in required_envs:
    if env not in os.environ:
        raise ValueError(f"{env} env var is not set.")


# database connection
cnx = mysql.connector.connect(
    host=os.environ("DB_HOST"),
    user=os.environ("DB_USER"),
    password=os.environ['DB_PASSWORD'],
    database=os.environ("DB_NAME")
)

cursor = cnx.cursor()


class User(BaseModel):
    id: int
    email: str
    password: str
    role: str
    nom: str
    prenom: str


def hash_password(password: str):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()


def check_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def create_user(user: User):
    hashed_password = hash_password(user.password)
    query = "INSERT INTO users (email, hashed_password, role, nom, prenom) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (user.email, hashed_password,
                   user.role, user.nom, user.prenom))
    cnx.commit()


def authenticate_user(email: str, password: str):
    query = f"SELECT hashed_password, role FROM users WHERE email = '{email}'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    hashed_password, role = result
    if check_password(password, hashed_password):
        return role
    return False


def get_current_user(credentials: HTTPBasicCredentials = Depends(HTTPBasic())):
    email = credentials.username
    role = authenticate_user(email, credentials.password, credentials.id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return role


def add_prediction_to_db(input_data: str, prediction_result: float, user_id: int):
    query = f"INSERT INTO prediction (input_data, prediction_result, user_id) VALUES ('{input_data}', '{prediction_result}', '{user_id}')"
    cursor.execute(query)
    cnx.commit()


@app.get("/")
async def get_index():
    return {"message": "Welcome to {} !".format(app.title)}


@app.get("/user")
async def current_user(username: str = Depends(get_current_user)):
    return "Hello {}".format(username)


@app.post("/predict/pulmonary-embolism")
async def predict_pulmonary_embolism(input_study: UploadFile = File(...), ckpt_path="data/penet_best.pth.tar", gpu_ids=0, device='cpu'):

    extension = input_study.filename.split(".")[-1]
    if not extension == 'dcm':
        return "Image must be DICOM format!"

    # create npy from dicom
    print(colored("Reading input dicom...", 'cyan'))
    study = util.dicom_2_npy(input_study)

    # normalize and convert to tensor
    print(colored("Formatting input for model...", 'cyan'))
    study_windows = util.format_img(study)

    print(colored("Loading saved model...", 'cyan'))
    model = ModelSaver.load_model(ckpt_path, gpu_ids)

    print(colored("Sending model to CPU device...", 'cyan'))
    model = model.to(device)

    print(colored("Evaluating study..."), 'cyan')
    model.eval()
    predicted_probabilities = []
    with torch.no_grad():
        for window in study_windows:
            cls_logits = model.forward(
                window.to(device, dtype=torch.float))
            cls_probs = torch.sigmoid(cls_logits).to('cpu').numpy()
            predicted_probabilities.append(cls_probs[0][0])

    print(colored(
        f"Probablity of having Pulmonary Embolism: {max(predicted_probabilities)}"), 'green')

    add_prediction_to_db(input_study, max(predicted_probabilities), User.id)

    return max(predicted_probabilities)
