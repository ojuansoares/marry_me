from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Boolean, DECIMAL, DateTime
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

# Create ENUM types
usertype = ENUM('fiance', 'guest', name='usertype', create_type=False)
weddingstatus = ENUM('active', 'postponed', 'cancelled', name='weddingstatus', create_type=False)
phototype = ENUM('couple', 'guests', name='phototype', create_type=False)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    u_name = Column(String(100), nullable=False)
    u_email = Column(String(100), unique=True, nullable=False)
    u_password_hash = Column(Text, nullable=False)
    u_phone = Column(String(20))
    u_type = Column(usertype, nullable=False)
    u_created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    weddings_groom = relationship("Wedding", foreign_keys="[Wedding.w_groom_id]", back_populates="groom")
    weddings_bride = relationship("Wedding", foreign_keys="[Wedding.w_bride_id]", back_populates="bride")
    images = relationship("Image", back_populates="user")

class Wedding(Base):
    __tablename__ = "weddings"

    id = Column(Integer, primary_key=True, index=True)
    w_groom_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    w_bride_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    w_date = Column(Date, nullable=False)
    w_location = Column(String(255), nullable=False)
    w_description = Column(Text)
    w_status = Column(weddingstatus, default='active')
    w_created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    groom = relationship("User", foreign_keys=[w_groom_id], back_populates="weddings_groom")
    bride = relationship("User", foreign_keys=[w_bride_id], back_populates="weddings_bride")
    guests = relationship("Guest", back_populates="wedding")
    guest_groups = relationship("GuestGroup", back_populates="wedding")
    reminders = relationship("Reminder", back_populates="wedding")
    images = relationship("Image", back_populates="wedding")
    budgets = relationship("Budget", back_populates="wedding")

class GuestGroup(Base):
    __tablename__ = "guest_groups"

    id = Column(Integer, primary_key=True, index=True)
    gg_wedding_id = Column(Integer, ForeignKey("weddings.id", ondelete="CASCADE"))
    gg_name = Column(String(100), nullable=False)
    gg_responsible_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    gg_confirmed = Column(Boolean, default=False)
    gg_created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    wedding = relationship("Wedding", back_populates="guest_groups")
    guests = relationship("Guest", back_populates="guest_group")
    responsible = relationship("User")

class Guest(Base):
    __tablename__ = "guests"

    id = Column(Integer, primary_key=True, index=True)
    g_wedding_id = Column(Integer, ForeignKey("weddings.id", ondelete="CASCADE"))
    g_user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    g_group_id = Column(Integer, ForeignKey("guest_groups.id", ondelete="CASCADE"), nullable=True)
    g_name = Column(String(100), nullable=False)
    g_phone = Column(String(20))
    g_email = Column(String(100))
    g_qr_code = Column(String(255), unique=True)
    g_confirmed = Column(Boolean, default=False)
    g_created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    wedding = relationship("Wedding", back_populates="guests")
    user = relationship("User")
    guest_group = relationship("GuestGroup", back_populates="guests")

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    r_wedding_id = Column(Integer, ForeignKey("weddings.id", ondelete="CASCADE"))
    r_description = Column(Text, nullable=False)
    r_datetime = Column(DateTime, nullable=False)
    r_created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    wedding = relationship("Wedding", back_populates="reminders")

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    i_wedding_id = Column(Integer, ForeignKey("weddings.id", ondelete="CASCADE"))
    i_user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    i_url = Column(Text, nullable=False)
    i_type = Column(phototype, nullable=False)
    i_created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    wedding = relationship("Wedding", back_populates="images")
    user = relationship("User", back_populates="images")

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    b_wedding_id = Column(Integer, ForeignKey("weddings.id", ondelete="CASCADE"))
    b_description = Column(String(255), nullable=False)
    b_value = Column(DECIMAL(10, 2), nullable=False)
    b_paid = Column(Boolean, default=False)
    b_created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    wedding = relationship("Wedding", back_populates="budgets") 