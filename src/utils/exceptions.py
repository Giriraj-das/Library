from fastapi import HTTPException, status


class CustomException:
    @staticmethod
    def http_400(detail: str = '400. Bad request') -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

    @staticmethod
    def http_404(detail: str = '404. Not_found') -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )
