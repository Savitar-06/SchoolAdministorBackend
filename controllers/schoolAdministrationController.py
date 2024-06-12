import fastapi
from models.login import Login
from service.loginServ import loginService
from utils import validateRoleBasedAuth,responseStructure,security,oauth,hashing
from models.staff import Staff
from config.dbConfig import collection
from config.dbConfig import login
from schemas.staffSchema import getStaffSchemaList
from bson import ObjectId

from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="logincheck")
from fastapi.security import OAuth2PasswordRequestForm

router = fastapi.APIRouter(prefix="/api")


@router.get("/check")
async def checkfun():
        return "Working..."


@router.post("/test")
async def loginn(req : fastapi.Request, loginReq : Login):
       validationCheck: bool = await validateRoleBasedAuth.validate_role_based_auth(req.headers)
       if not validationCheck:
        message = "Login failed"
        return  responseStructure.responseStruct(Status=400, Error=True, Output=None, Message=message, devMessage="")
       else:
         Response = await loginService(req.headers,loginReq)
         return  responseStructure.responseStruct(Status=200, Error=False, Output=Response, Message="test successful", devMessage="")
       
@router.post("/getstaff")
async def getStaff():
     stafflist = getStaffSchemaList(collection.find())
     return stafflist

@router.post("/savestaff")
def saveStaff(staff: Staff):
    result = collection.insert_one(staff.dict())
    if result.inserted_id:
        inserted_id = str(result.inserted_id)
        return responseStructure.responseStruct(Status=201, Error=False, Output=inserted_id, Message="save successful", devMessage="successfully inserted into staff collection")
    else:
        data = responseStructure.responseStruct(Status=500, Error=True, Output=None, Message="Failed to save", devMessage="Failed to save staff")
        raise fastapi.HTTPException(status_code=500, detail=data)

@router.put("/updatestaff")
async def updatestaff(_id:str, name:str, role:str):
    result = collection.find_one_and_update({"_id":ObjectId(_id)},{"$set": {"name": name, "role": role}})
    if result:
        inserted_id = str(result)
        return responseStructure.responseStruct(Status=201, Error=False, Output=inserted_id, Message="save successful", devMessage="successfully inserted into staff collection")
    else:
        data = responseStructure.responseStruct(Status=500, Error=True, Output=None, Message="Failed to save", devMessage="Failed to save staff")
        raise fastapi.HTTPException(status_code=500, detail=data)
    
@router.delete("/deletestaff")
async def deltaff(_id:str):
    result = collection.find_one_and_delete({"_id":ObjectId(_id)})
    if result:
        inserted_id = str(result)
        return responseStructure.responseStruct(Status=201, Error=False, Output=inserted_id, Message="save successful", devMessage="successfully inserted into staff collection")
    else:
        data = responseStructure.responseStruct(Status=500, Error=True, Output=None, Message="Failed to save", devMessage="Failed to save staff")
        raise fastapi.HTTPException(status_code=500, detail=data)
    
    
@router.post("/login")
def getStaffbyname(logins:Login):
    loginss = list(login.find({"userid": {"$regex": logins.userid},"pwd": {"$regex": logins.pwd},"role": {"$regex": logins.role}}))#{"$regex": name, "$options": "i"}
    if loginss:
            access_token = security.create_access_token(data={"sub": logins.userid})
            for doc in loginss:
                doc['_id'] = str(doc['_id'])
            return access_token
    else:
        # Document not found
        raise fastapi.HTTPException(status_code=404, detail="Staff document not found")
    
@router.post("/logincheck")
def getStaffbyname(token: str):
    data = oauth.get_current_user(token)
    return data
    # loginss = list(login.find({"userid": {"$regex": logins.userid},"pwd": {"$regex": logins.pwd},"role": {"$regex": logins.role}}))#{"$regex": name, "$options": "i"}
    # if loginss:
    #         access_token = security.create_access_token(data={"sub": logins.userid})
    #         for doc in loginss:
    #             doc['_id'] = str(doc['_id'])
    #         return access_token
    # else:
    #     # Document not found
    #     raise fastapi.HTTPException(status_code=404, detail="Staff document not found")