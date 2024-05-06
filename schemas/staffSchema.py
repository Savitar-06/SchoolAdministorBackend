def getStaffSchema(data)->dict:
    return {
        "_id": str(data["_id"]),
        "name": str(data["name"]),
        "role": str(data["role"])
    }

def getStaffSchemaList(datas)->list:
    return [getStaffSchema(data) for data in datas]