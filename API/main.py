'''
 @GladisValenzuela
 DataScientest MLOps Training Project
 Creation date: January 2023
'''

import os
import util
import time
import torch
import bcrypt
import uvicorn
import mysql.connector

from saver.model_saver import ModelSaver
from termcolor import colored
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Tuple


app = FastAPI(
    title="Pulmonary Embolism - DataScientest MLOps Training Project")


# required_envs = ['DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']


# for env in required_envs:
#     if env not in os.environ:
#         raise ValueError(f"{env} env var is not set.")


# database connection
cnx = mysql.connector.connect(
    host=DB_HOST,#"host.docker.internal",  # os.environ("DB_HOST"),
    user=DB_USER, #"root",  # os.environ("DB_USER"),
    password=MYSQL_ROOT_PASSWORD, #"8vdkqk13",  # os.environ['DB_PASSWORD'],
    database=MYSQL_DATABASE #"pe_api",   # os.environ("DB_NAME"),
)

cursor = cnx.cursor()


class User(BaseModel):
    id: int
    username: str
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
    query = "INSERT INTO user (username, hashed_password, role, nom, prenom) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (user.username, hashed_password,
                   user.role, user.nom, user.prenom))
    cnx.commit()


def authenticate_user(username: str, password: str):
    query = f"SELECT id, hashed_password, role FROM user WHERE username = '{username}'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        return False
    id, hashed_password, role = result
    if check_password(password, hashed_password):
        return role
    return False


def get_current_user(credentials: HTTPBasicCredentials = Depends(HTTPBasic())):
    user = credentials.username
    auth = authenticate_user(user, credentials.password)
    if not auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    query = f"SELECT id FROM user WHERE username = '{user}'"
    cursor.execute(query)
    user_id = cursor.fetchone()[0]
    return (user, user_id)


def add_prediction_to_db(input_data: str, prediction_result: float, user_id: User):
    query = f"INSERT INTO prediction (input_data, prediction_result, user_id) VALUES ('{input_data}', '{prediction_result}', '{user_id}')"
    cursor.execute(query)
    cnx.commit()


@app.get("/")
async def get_index():
    return {"Welcome to {} !".format(app.title)}


@app.get("/user")
# (username: str = Depends(get_current_user)):
async def current_user(current_user: Tuple[str, int] = Depends(get_current_user)):
    return "Hello {}".format(current_user[0])


@app.post("/predict/pulmonary-embolism")
async def predict_pulmonary_embolism(input_study: UploadFile = File(...), ckpt_path="data/penet_best.pth.tar", gpu_ids=0, device='cpu', user_id=Depends(get_current_user)):
    start = time.time()

    extension = input_study.filename.split(".")[-1]
    if not extension == 'zip':
        return "Images must be DICOM in a zip format!"

    # create npy from dicom
    print(colored("Reading input dicom...", 'cyan'))
    study = await util.dicom_2_npy(input_study)

    # normalize and convert to tensor
    print(colored("Formatting input for model...", 'cyan'))
    study_windows = util.format_img(study)

    print(colored("Loading saved model...", 'cyan'))
    model, _ = ModelSaver.load_model(ckpt_path, gpu_ids)

    print(colored("Sending model to CPU device...", 'cyan'))
    model = model.to(device)

    print(colored("Evaluating study...", 'cyan'))
    model.eval()
    predicted_probabilities = []
    with torch.no_grad():
        cls_logits = model.forward(
            study_windows[0].to(device, dtype=torch.float))
        cls_probs = torch.sigmoid(cls_logits).to('cpu').numpy()
        predicted_probabilities.append(cls_probs[0][0])

        add_prediction_to_db(input_study.filename, round(
            float(max(predicted_probabilities)), 4), user_id[1])  # 1 car renvoie le tuple (username, user_id)

        print(colored(
            f"Probablity of having Pulmonary Embolism: {round(float(max(predicted_probabilities)), 4)}", 'green'))

        end = time.time()

        print(colored(
            f"Temps d'exécution: {round((end - start), 4)} secondes, soit {round((end - start) / 60, 4)} minutes.", 'green'))

        return float(round(max(predicted_probabilities), 4))


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
