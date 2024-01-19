"""v3

Revision ID: 468f59e39625
Revises: 00ca7fd09ea0
Create Date: 2024-01-19 13:24:35.168292

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '468f59e39625'
down_revision: Union[str, None] = '00ca7fd09ea0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('menu_submenu_id_fkey', 'menu', type_='foreignkey')
    op.create_foreign_key(None, 'menu', 'submenu', ['submenu_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('submenu_menu_id_fkey', 'submenu', type_='foreignkey')
    op.drop_constraint('submenu_dish_id_fkey', 'submenu', type_='foreignkey')
    op.create_foreign_key(None, 'submenu', 'dish', ['dish_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'submenu', 'menu', ['menu_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'submenu', type_='foreignkey')
    op.drop_constraint(None, 'submenu', type_='foreignkey')
    op.create_foreign_key('submenu_dish_id_fkey', 'submenu', 'dish', ['dish_id'], ['id'])
    op.create_foreign_key('submenu_menu_id_fkey', 'submenu', 'menu', ['menu_id'], ['id'])
    op.drop_constraint(None, 'menu', type_='foreignkey')
    op.create_foreign_key('menu_submenu_id_fkey', 'menu', 'submenu', ['submenu_id'], ['id'])
    # ### end Alembic commands ###
