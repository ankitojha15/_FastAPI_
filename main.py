from fastapi import FastAPI, Path , HTTPException, Query
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

# NOTE : three dots(...,description =  ........) makes the parameter mandaotry else optional

@app.get("/sort")
def sort_patients(sort_by:str = Query(...,description = "sort on the basis of height,weight or bmi"), 
                order : str = Query("asc",description = "sort in asc or desc order")):

    valid_feilds = ["height","weight","bmi"]

    if sort_by not in valid_feilds:
        raise HTTPException(status_code=400,detail ="invalid feild select from {valid_feilds}" )

    if order not in ["asc","desc"]:
        raise HTTPException(status_code=400,detail = "Invalid order select between asc and desc ")

    data = data_load()

    sort_order = True if order == "desc" else False

    sorted_data = sorted(data.values(),key = lambda x: x.get(sort_by,0),reverse = sort_order)

    return sorted_data