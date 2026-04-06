"""rbac per role permissions

Revision ID: 0002_rbac_per_role_permissions
Revises: 0001_initial
Create Date: 2026-04-06
"""

from alembic import op
import sqlalchemy as sa


revision = "0002_rbac_per_role_permissions"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint("permissions_module_key", "permissions", type_="unique")

    conn = op.get_bind()
    roles = {r.name: r.id for r in conn.execute(sa.text("SELECT id, name FROM roles"))}
    conn.execute(
        sa.text(
            "DELETE FROM permissions WHERE module IN "
            "('products','suppliers','buyers','cost_heads','calculations','reports')"
        )
    )

    conn.execute(sa.text("DELETE FROM role_permissions"))

    admin_perm_ids = []
    for module in ["products", "suppliers", "buyers", "cost_heads", "calculations"]:
        pid = conn.execute(
            sa.text(
                """
                INSERT INTO permissions (module, can_view, can_create, can_edit, can_delete)
                VALUES (:module, true, true, true, true)
                RETURNING id
                """
            ),
            {"module": module},
        ).scalar_one()
        admin_perm_ids.append(pid)
    admin_reports_id = conn.execute(
        sa.text(
            """
            INSERT INTO permissions (module, can_view, can_create, can_edit, can_delete)
            VALUES ('reports', true, false, false, false)
            RETURNING id
            """
        )
    ).scalar_one()
    admin_perm_ids.append(admin_reports_id)

    staff_perm_ids = []
    for module in ["products", "suppliers", "buyers", "calculations"]:
        pid = conn.execute(
            sa.text(
                """
                INSERT INTO permissions (module, can_view, can_create, can_edit, can_delete)
                VALUES (:module, true, true, true, false)
                RETURNING id
                """
            ),
            {"module": module},
        ).scalar_one()
        staff_perm_ids.append(pid)
    staff_cost_heads_id = conn.execute(
        sa.text(
            """
            INSERT INTO permissions (module, can_view, can_create, can_edit, can_delete)
            VALUES ('cost_heads', true, false, false, false)
            RETURNING id
            """
        )
    ).scalar_one()
    staff_reports_id = conn.execute(
        sa.text(
            """
            INSERT INTO permissions (module, can_view, can_create, can_edit, can_delete)
            VALUES ('reports', true, false, false, false)
            RETURNING id
            """
        )
    ).scalar_one()
    staff_perm_ids.extend([staff_cost_heads_id, staff_reports_id])

    for pid in admin_perm_ids:
        conn.execute(
            sa.text(
                "INSERT INTO role_permissions(role_id, permission_id) VALUES (:role_id, :permission_id)"
            ),
            {"role_id": roles["Admin"], "permission_id": pid},
        )
    for pid in staff_perm_ids:
        conn.execute(
            sa.text(
                "INSERT INTO role_permissions(role_id, permission_id) VALUES (:role_id, :permission_id)"
            ),
            {"role_id": roles["Staff"], "permission_id": pid},
        )

def downgrade() -> None:
    raise RuntimeError("Downgrade not supported for RBAC migration")
