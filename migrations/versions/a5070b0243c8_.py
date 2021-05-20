"""empty message

Revision ID: a5070b0243c8
Revises: 39db843b5364
Create Date: 2021-05-18 10:35:29.860466

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5070b0243c8'
down_revision = '39db843b5364'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post_comments', sa.Column('course_code', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post_comments', 'course_code')
    # ### end Alembic commands ###