import uuid
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.compiler import compiles
from pgvector.sqlalchemy import Vector
from database import Base

# SQLAlchemy compiler override to fallback gracefully in SQLite
@compiles(Vector, "sqlite")
def compile_vector_sqlite(element, compiler, **kw):
    # In SQLite, we can just treat the vector as JSON or TEXT
    return "JSON"

@compiles(UUID, 'sqlite')
def compile_uuid_sqlite(type_, compiler, **kw):
    return "VARCHAR"

class RegulationChunk(Base):
    __tablename__ = "regulation_chunks"

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source = sa.Column(sa.String, nullable=False, index=True)
    article_number = sa.Column(sa.String, nullable=True)
    section_title = sa.Column(sa.String, nullable=True)
    content = sa.Column(sa.Text, nullable=False)
    embedding = sa.Column(Vector(768))
    created_at = sa.Column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now()
    )
