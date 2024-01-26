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


class SubMenuNotFoundException(RestaurantException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "submenu not found"


class DishNotFoundException(RestaurantException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "dish not found"

class SimilarMenuTitlesException(RestaurantException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "menu titles must be unique"


class SimilarSubmenuTitlesException(RestaurantException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "submenu titles must be unique"