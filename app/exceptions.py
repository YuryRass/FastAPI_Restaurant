"""Различные HTTP-ошибки"""
from fastapi import HTTPException, status


class RestaurantException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class MenuNotFoundException(RestaurantException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "menu not found"