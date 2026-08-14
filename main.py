from fastapi import FastAPI, Path , HTTPException
import json

app = FastAPI()

def data_load():
    with open("patients.json","r") as f:
        data = json.load(f)

    return data

@app.get("/")
def hello():
    return {"message":"Patient Management API system"}

@app.get("/about")
def about():
    return {"message":"a fully functional API to manage your patients"}

@app.get("/view")
def view():
    data = data_load()

    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(...,description = "ID of the patient in db",example = "P001")):
    # load all the patients
    data = data_load()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code= 404 , detail = "Patient not found")
