"""initial schema and seed

Revision ID: 0001_initial
Revises:
Create Date: 2026-04-06
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "companies",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=50), nullable=False, unique=True),
    )
    op.create_table(
        "permissions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("module", sa.String(length=100), nullable=False, unique=True),
        sa.Column("can_view", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("can_create", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("can_edit", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("can_delete", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("company_id", sa.Integer(), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role_id", sa.Integer(), sa.ForeignKey("roles.id"), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_table(
        "role_permissions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("role_id", sa.Integer(), sa.ForeignKey("roles.id"), nullable=False),
        sa.Column(
            "permission_id", sa.Integer(), sa.ForeignKey("permissions.id"), nullable=False
        ),
    )
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("company_id", sa.Integer(), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=True),
        sa.Column("grade", sa.String(length=100), nullable=True),
        sa.Column("unit", sa.String(length=50), nullable=False),
    )
    op.create_table(
        "product_prices",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("product_id", sa.Integer(), sa.ForeignKey("products.id"), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
    )
    op.create_table(
        "suppliers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("company_id", sa.Integer(), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("phone", sa.String(length=50), nullable=True),
        sa.Column("district", sa.String(length=100), nullable=True),
        sa.Column("address", sa.String(length=500), nullable=True),
    )
    op.create_table(
        "buyers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("company_id", sa.Integer(), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("company_name", sa.String(length=255), nullable=True),
        sa.Column("country", sa.String(length=100), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=50), nullable=True),
    )
    op.create_table(
        "cost_heads",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("company_id", sa.Integer(), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("type", sa.String(length=10), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_table(
        "calculations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("company_id", sa.Integer(), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("product_id", sa.Integer(), sa.ForeignKey("products.id"), nullable=False),
        sa.Column("total_fob", sa.Float(), nullable=False, server_default="0"),
        sa.Column("total_cfr", sa.Float(), nullable=False, server_default="0"),
        sa.Column("total_cpt", sa.Float(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "cost_entries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "calculation_id", sa.Integer(), sa.ForeignKey("calculations.id"), nullable=False
        ),
        sa.Column("cost_head_id", sa.Integer(), sa.ForeignKey("cost_heads.id"), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
    )

    op.execute("INSERT INTO roles (name) VALUES ('Admin'), ('Staff')")
    op.execute(
        """
        INSERT INTO permissions (module, can_view, can_create, can_edit, can_delete) VALUES
        ('products', true, true, true, true),
        ('suppliers', true, true, true, true),
        ('buyers', true, true, true, true),
        ('cost_heads', true, true, true, true),
        ('calculations', true, true, true, true),
        ('reports', true, false, false, false)
        """
    )
    op.execute(
        """
        INSERT INTO role_permissions(role_id, permission_id)
        SELECT r.id, p.id FROM roles r CROSS JOIN permissions p WHERE r.name = 'Admin'
        """
    )
    op.execute(
        """
        INSERT INTO role_permissions(role_id, permission_id)
        SELECT r.id, p.id FROM roles r JOIN permissions p ON p.module IN ('products','suppliers','buyers','cost_heads','calculations','reports')
        WHERE r.name = 'Staff'
        """
    )


def downgrade() -> None:
    op.drop_table("cost_entries")
    op.drop_table("calculations")
    op.drop_table("cost_heads")
    op.drop_table("buyers")
    op.drop_table("suppliers")
    op.drop_table("product_prices")
    op.drop_table("products")
    op.drop_table("role_permissions")
    op.drop_table("users")
    op.drop_table("permissions")
    op.drop_table("roles")
    op.drop_table("companies")
