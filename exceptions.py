from fastapi import HTTPException
from fastapi import status


class APIException:
    headers = {
        "WWW-Authenticate": 'Bearer'
    }

    @classmethod
    async def create_exception(
            cls,
            detail,
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers=True
    ):
        if headers:
            headers = cls.headers

        return HTTPException(status_code, detail, headers)
