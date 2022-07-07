from fastapi import HTTPException
from fastapi import status


class AuthorizedException:
    headers = {
        "WWW-Authenticate": 'Bearer'
    }

    async def create_exception(
            self,
            detail,
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers=True
    ):
        if headers:
            headers = self.headers

        return HTTPException(status_code, detail, headers)
