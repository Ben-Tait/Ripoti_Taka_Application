"""empty message

Revision ID: d45941174035
Revises: 
Create Date: 2024-05-21 10:03:53.475424

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd45941174035'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('categoryId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('categoryId')
    )
    op.create_table('reward',
    sa.Column('rewardId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('pointsRequired', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('rewardId')
    )
    op.create_table('role',
    sa.Column('roleId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('default', sa.Boolean(), nullable=True),
    sa.Column('permissions', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('roleId')
    )
    with op.batch_alter_table('role', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_role_default'), ['default'], unique=False)

    op.create_table('status',
    sa.Column('statusId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('statusId')
    )
    op.create_table('user',
    sa.Column('userId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('firstName', sa.String(length=30), nullable=True),
    sa.Column('middleName', sa.String(length=30), nullable=True),
    sa.Column('lastName', sa.String(length=30), nullable=True),
    sa.Column('userName', sa.String(length=50), nullable=False),
    sa.Column('emailAddress', sa.String(length=100), nullable=False),
    sa.Column('passwordHash', sa.String(length=100), nullable=False),
    sa.Column('phoneNumber', sa.String(length=20), nullable=True),
    sa.Column('gender', sa.String(length=8), nullable=False),
    sa.Column('locationAddress', sa.String(length=255), nullable=True),
    sa.Column('about_me', sa.String(length=140), nullable=True),
    sa.Column('avatar_hash', sa.String(length=32), nullable=True),
    sa.Column('pointsAcquired', sa.Integer(), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.Column('dateCreated', sa.DateTime(), nullable=True),
    sa.Column('lastUpdated', sa.DateTime(), nullable=True),
    sa.Column('imageUrl', sa.String(length=200), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('roleId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['roleId'], ['role.roleId'], ),
    sa.PrimaryKeyConstraint('userId'),
    sa.UniqueConstraint('userName')
    )
    op.create_table('report',
    sa.Column('reportId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('location', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('moderated', sa.Boolean(), nullable=True),
    sa.Column('isResolved', sa.Boolean(), nullable=True),
    sa.Column('dateCreated', sa.DateTime(), nullable=True),
    sa.Column('lastUpdated', sa.DateTime(), nullable=True),
    sa.Column('categoryId', sa.Integer(), nullable=True),
    sa.Column('userId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['categoryId'], ['category.categoryId'], ),
    sa.ForeignKeyConstraint(['userId'], ['user.userId'], ),
    sa.PrimaryKeyConstraint('reportId')
    )
    with op.batch_alter_table('report', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_report_location'), ['location'], unique=False)

    op.create_table('user_reward',
    sa.Column('userRewardId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('userId', sa.Integer(), nullable=True),
    sa.Column('rewardId', sa.Integer(), nullable=True),
    sa.Column('dateAssigned', sa.DateTime(), nullable=True),
    sa.Column('isAssigned', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['rewardId'], ['reward.rewardId'], ),
    sa.ForeignKeyConstraint(['userId'], ['user.userId'], ),
    sa.PrimaryKeyConstraint('userRewardId')
    )
    op.create_table('comment',
    sa.Column('commentId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('dateCreated', sa.DateTime(), nullable=True),
    sa.Column('lastUpdated', sa.DateTime(), nullable=True),
    sa.Column('reportId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['reportId'], ['report.reportId'], ),
    sa.PrimaryKeyConstraint('commentId')
    )
    op.create_table('report_status',
    sa.Column('reportStatusId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('reportId', sa.Integer(), nullable=True),
    sa.Column('statusId', sa.Integer(), nullable=True),
    sa.Column('dateCreated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['reportId'], ['report.reportId'], ),
    sa.ForeignKeyConstraint(['statusId'], ['status.statusId'], ),
    sa.PrimaryKeyConstraint('reportStatusId')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('report_status')
    op.drop_table('comment')
    op.drop_table('user_reward')
    with op.batch_alter_table('report', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_report_location'))

    op.drop_table('report')
    op.drop_table('user')
    op.drop_table('status')
    with op.batch_alter_table('role', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_role_default'))

    op.drop_table('role')
    op.drop_table('reward')
    op.drop_table('category')
    # ### end Alembic commands ###
