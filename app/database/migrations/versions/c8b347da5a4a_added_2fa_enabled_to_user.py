"""Added 2FA Enabled to User

Revision ID: c8b347da5a4a
Revises: 53edb733cb79
Create Date: 2024-10-30 14:39:00.557906

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8b347da5a4a'
down_revision = '53edb733cb79'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_2fa_auth_enabled', sa.Boolean(), server_default='f', nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('is_2fa_auth_enabled')

    # ### end Alembic commands ###
