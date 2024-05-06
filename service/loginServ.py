


async def loginService(header,body)-> str:
        # Business Logics here
        userId = body.userid
        password = body.pwd
        role = body.role

        return userId