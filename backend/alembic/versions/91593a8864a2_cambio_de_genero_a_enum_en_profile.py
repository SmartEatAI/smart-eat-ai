"""cambio de genero a enum en profile

Revision ID: 91593a8864a2
Revises: 1e6279aa4b4a
Create Date: 2026-02-21 16:20:54.968880

"""
from alembic import op
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '91593a8864a2'
down_revision = '1e6279aa4b4a'
branch_labels = None
depends_on = None

def upgrade():
    # 1. Crear el tipo ENUM en la base de datos (Postgres lo necesita como objeto independiente)
    gender_enum = postgresql.ENUM('male', 'female', name='gender_enum')
    gender_enum.create(op.get_bind(), checkfirst=True)

    # 2. Cambiar el tipo de la columna usando una ejecución SQL directa con USING
    # Esto es lo que op.alter_column NO puede hacer por sí solo
    op.execute(
        'ALTER TABLE profiles ALTER COLUMN gender TYPE gender_enum '
        'USING gender::gender_enum'
    )

    # 3. Opcional: Si después de la conversión quieres asegurar que sea nullable o no
    op.alter_column('profiles', 'gender',
               existing_type=postgresql.ENUM('male', 'female', name='gender_enum'),
               nullable=True) # O False, según tu modelo

def downgrade():
    # Para volver atrás, primero convertimos a VARCHAR y luego borramos el tipo
    op.execute('ALTER TABLE profiles ALTER COLUMN gender TYPE VARCHAR USING gender::text')
    postgresql.ENUM(name='gender_enum').drop(op.get_bind(), checkfirst=True)