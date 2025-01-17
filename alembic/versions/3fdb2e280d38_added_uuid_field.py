"""Added UUID field

Revision ID: 3fdb2e280d38
Revises: aa31799c7630
Create Date: 2023-04-11 23:07:41.560271

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3fdb2e280d38'
down_revision = 'aa31799c7630'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('prompts', sa.Column('uuid', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('prompts', 'uuid')
    # ### end Alembic commands ###
