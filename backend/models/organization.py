import uuid
import enum
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, ForeignKey, func, Uuid, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class OrgRole(str, enum.Enum):
    admin = "admin"
    member = "member"

class Organization(Base):
    __tablename__ = "organizations"

id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    # Relationships
    members: Mapped[list["OrgMember"]] = relationship("OrgMember", back_populates="organization", cascade="all, delete-orphan")
    invitations: Mapped[list["Invitation"]] = relationship("Invitation", back_populates="organization", cascade="all, delete-orphan")
    audits: Mapped[list["Audit"]] = relationship("Audit", back_populates="organization")
    workflows: Mapped[list["Workflow"]] = relationship("Workflow", back_populates="organization")
    subscription: Mapped[Optional["Subscription"]] = relationship("Subscription", back_populates="organization", uselist=False)

class OrgMember(Base):
    __tablename__ = "org_members"

user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    org_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), primary_key=True)
    role: Mapped[OrgRole] = mapped_column(SQLAlchemyEnum(OrgRole), default=OrgRole.member, nullable=False)
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="org_members")
    organization: Mapped["Organization"] = relationship("Organization", back_populates="members")

class Invitation(Base):
    __tablename__ = "invitations"

id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    token: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    accepted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="invitations")
