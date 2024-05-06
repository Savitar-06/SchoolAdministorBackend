from fastapi import FastAPI,Request
from controllers import schoolAdministrationController
from utils import responseStructure
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

app.include_router(schoolAdministrationController.router)

origins=['https://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials= True,
    allow_methods=["*"],
    allow_headers=["*"]
)



@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_details = []
    for error in exc.errors():
        if (error["input"]==None):
             print(error,error["input"],"HHHH")
             error_detail = {
                "type": error["type"],
                "loc": error["loc"],
                "msg": error["msg"],
                "input": error["type"],
            }
        else :     
            error_detail = {
                    "type": error["type"],
                    "loc": error["loc"],
                    "msg": error["msg"],
                    "input": error["type"],
                    "ctx": error["ctx"]
                }    

        error_details.append(error_detail)

    response_body = responseStructure.responseStruct(Status=400, Error=True, Output=error_details, Message="In-Correct Input Please Check Again", devMessage="Schema Validation Missing")
    return JSONResponse(content=response_body, status_code=400)