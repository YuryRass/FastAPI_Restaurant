"""Различные HTTP-ошибки"""

from fastapi import HTTPException, status


class RestaurantException(HTTPException):
    """Базовое исключение для ресторана."""
    status_code = 500
    detail = ''

    def __init__(self) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail)


class MenuNotFoundException(RestaurantException):
    """Исключение: меню не найдено."""
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'menu not found'


class SubMenuNotFoundException(RestaurantException):
    """Исключение: подменю не найдено."""
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'submenu not found'


class DishNotFoundException(RestaurantException):
    """Исключение: блюдо не найдено."""
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'dish not found'


class SimilarMenuTitlesException(RestaurantException):
    """Исключение: названия меню должны быть уникальными."""
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'menu titles must be unique'


class SimilarSubmenuTitlesException(RestaurantException):
    """Исключение: названия подменю должны быть уникальными."""
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'submenu titles must be unique'


class SimilarDishTitlesException(RestaurantException):
    """Исключение: названия блюд должны быть уникальными."""
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'dish titles must be unique'
