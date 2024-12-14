from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'unique_revision_id'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'products',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('stock_quantity', sa.Integer(), nullable=False),
        sa.Column('image_url', sa.String(), nullable=True),
    )

def downgrade():
    op.drop_table('products')
