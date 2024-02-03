from app.dao.cache_base import RedisBaseDAO
from app.submenu.model import Submenu


class RedisSubmenuDAO(RedisBaseDAO):
    model = Submenu
