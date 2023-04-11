"""Added new fields

Revision ID: aa31799c7630
Revises: 41262bc15d7f
Create Date: 2023-04-11 22:53:45.772872

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa31799c7630'
down_revision = '41262bc15d7f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('prompts', sa.Column('call_id', sa.String(), nullable=True))
    op.add_column('prompts', sa.Column('generated', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('prompts', 'generated')
    op.drop_column('prompts', 'call_id')
    # ### end Alembic commands ###