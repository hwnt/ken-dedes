"""empty message

Revision ID: 572651f8878b
Revises: 
Create Date: 2020-05-07 21:26:39.255675

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '572651f8878b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'providers', ['user_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'providers', type_='unique')
    # ### end Alembic commands ###