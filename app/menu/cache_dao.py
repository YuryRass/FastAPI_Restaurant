from app.dao.cache_base import RedisBaseDAO
from app.menu.model import Menu


class RedisMenuDAO(RedisBaseDAO):
    model = Menu
