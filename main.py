from fastapi import FastAPI, Path , HTTPException, Query
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel , Field , computed_field
from typing import Annotated ,Literal

app = FastAPI()

class Patient(BaseModel):

    id : Annotated[str,Field(...,dscription = "Id of the Patient",example = "P001")]
    name: Annotated[str,Field(...,description="Name of the Patient")]
    city : Annotated[str,Field(...,description = "Name of the city")]
    age : Annotated[int,Field(...,gt=0,lt=120,description="age of the patient")]
    gender : Annotated[Literal["Male","Female","Other"],Field(...,description ="Gender of the Patient")]
    height : Annotated[float,Field(..., gt=0, description = "Height of the patient in mtrs")]
    weight : Annotated[float,Field(..., gt=0, description = "Weight of the patient in kgs")]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "underwieght"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "obese"

def data_load():
    with open("patients.json","r") as f:
        data = json.load(f)

    return data

def save_data(data):
    with open("patients.json","w") as f:
        json.dump(data,f)

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
        raise HTTPException(status_code=400,detail =f"invalid feild select from {valid_feilds}" )

    if order not in ["asc","desc"]:
        raise HTTPException(status_code=400,detail = "Invalid order select between asc and desc ")

    data = data_load()

    sort_order = True if order == "desc" else False

    sorted_data = sorted(data.values(),key = lambda x: x.get(sort_by,0),reverse = sort_order)

    return sorted_data


@app.post("/create")
def create_patient(patient : Patient): # pateint is varibale whic stores the new patient data and Patient is its data type which is a Pydantic class

    # load_existing data
    data = data_load()

    # check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400,detail = "Patient already in existense")

    # add new patient into the db
    # we have to convert the data into python dict for that we use model_dump(),it converts the data into dict
    data[patient.id] = patient.model_dump()

    # save the data into json file

    save_data(data) # calling the save data func

    return JSONResponse(content = "Patient added succesfull",status_code=201)
