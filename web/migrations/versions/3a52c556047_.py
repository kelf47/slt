"""empty message

Revision ID: 3a52c556047
Revises: None
Create Date: 2017-07-10 15:23:01.019176

"""

# revision identifiers, used by Alembic.
revision = '3a52c556047'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), server_default='', nullable=False),
    sa.Column('label', sa.Unicode(length=255), server_default='', nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('tipus_document',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tipus', sa.String(length=50), server_default='', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('tipus')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.Unicode(length=255), server_default='', nullable=False),
    sa.Column('password', sa.String(length=255), server_default='', nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default='0', nullable=False),
    sa.Column('nom', sa.Unicode(length=50), server_default='', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('documents',
    sa.Column('mimetype', sa.Unicode(length=255), nullable=False),
    sa.Column('filename', sa.Unicode(length=255), nullable=False),
    sa.Column('blob', sa.LargeBinary(), nullable=False),
    sa.Column('size', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('creat', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('nom', sa.Unicode(length=255), nullable=False),
    sa.Column('compartit', sa.Boolean(), server_default='0', nullable=False),
    sa.Column('tipus_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['tipus_id'], ['tipus_document.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nom')
    )
    op.create_table('users_roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users_documents',
    sa.Column('document_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['document_id'], ['documents.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_documents')
    op.drop_table('users_roles')
    op.drop_table('documents')
    op.drop_table('users')
    op.drop_table('tipus_document')
    op.drop_table('roles')
    ### end Alembic commands ###
