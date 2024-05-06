def responseStruct (Status:int,Error:bool,Output:any,Message:any,devMessage:any):
    return {
        "status": Status,
        "error": Error,
        "output": Output,
        "message": Message,
        "devMessage": devMessage
    }
    