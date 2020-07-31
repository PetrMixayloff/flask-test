"""init_migration

Revision ID: c5019223fb42
Revises: 
Create Date: 2020-07-31 13:19:26.196577

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c5019223fb42'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('task', sa.String(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('result', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_date_created'), 'task', ['date_created'], unique=False)
    op.create_index(op.f('ix_task_id'), 'task', ['id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_task_id'), table_name='task')
    op.drop_index(op.f('ix_task_date_created'), table_name='task')
    op.drop_table('task')
    # ### end Alembic commands ###
