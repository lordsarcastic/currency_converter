"""Added conversion history

Revision ID: 98f5726393b4
Revises: 199b1fe61d72
Create Date: 2022-07-20 18:50:17.658744

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '98f5726393b4'
down_revision = '199b1fe61d72'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('conversionhistory',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('from_currency', sa.String(length=3), nullable=False),
    sa.Column('to_currency', sa.String(length=3), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('rate', sa.Float(), nullable=False),
    sa.Column('result', sa.Float(), nullable=False),
    sa.Column('timestamp', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_conversionhistory_from_currency'), 'conversionhistory', ['from_currency'], unique=False)
    op.create_index(op.f('ix_conversionhistory_to_currency'), 'conversionhistory', ['to_currency'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_conversionhistory_to_currency'), table_name='conversionhistory')
    op.drop_index(op.f('ix_conversionhistory_from_currency'), table_name='conversionhistory')
    op.drop_table('conversionhistory')
    # ### end Alembic commands ###
