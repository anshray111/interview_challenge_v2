"""Create business and symptom tables

Revision ID: 18614180db7a
Revises: 
Create Date: 2025-04-08 19:41:21.819714

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18614180db7a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('business',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('created_by', sa.String(length=100), nullable=True),
    sa.Column('updated_by', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('symptom',
    sa.Column('code', sa.String(length=20), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('created_by', sa.String(length=100), nullable=True),
    sa.Column('updated_by', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('code')
    )
    op.create_table('business_symptom',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('business_id', sa.Integer(), nullable=False),
    sa.Column('symptom_code', sa.String(length=20), nullable=False),
    sa.Column('diagnostic', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('created_by', sa.String(length=100), nullable=True),
    sa.Column('updated_by', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['business_id'], ['business.id'], ),
    sa.ForeignKeyConstraint(['symptom_code'], ['symptom.code'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('business_symptom')
    op.drop_table('symptom')
    op.drop_table('business')
    # ### end Alembic commands ###