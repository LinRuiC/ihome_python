"""empty message

Revision ID: d81bed2e456b
Revises: ad334a2bc88d
Create Date: 2019-03-09 17:14:04.932931

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd81bed2e456b'
down_revision = 'ad334a2bc88d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ih_house_image',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('house_id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=256), nullable=False),
    sa.ForeignKeyConstraint(['house_id'], ['ih_house_info.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ih_house_image')
    # ### end Alembic commands ###