import uuid
import enum
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, func, Uuid, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class OrgRole(enum.Enum):
    admin = "admin"
    member = "member"

class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    members = relationship("OrgMember", back_populates="organization")
    invitations = relationship("Invitation", back_populates="organization")
    audits = relationship("Audit", back_populates="organization")
    workflows = relationship("Workflow", back_populates="organization")
    subscriptions = relationship("Subscription", back_populates="organization")
    integration_results = relationship("IntegrationResult", back_populates="organization")

class OrgMember(Base):
    __tablename__ = "org_members"

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id"), primary_key=True)
    org_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("organizations.id"), primary_key=True)
    role: Mapped[OrgRole] = mapped_column(Enum(OrgRole), nullable=False)
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="org_memberships")
    organization = relationship("Organization", back_populates="members")

class Invitation(Base):
    __tablename__ = "invitations"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    org_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("organizations.id"), nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    token: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    accepted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    organization = relationship("Organization", back_populates="invitations")
