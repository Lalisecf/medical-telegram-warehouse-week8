from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import BigInteger
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Numeric
from sqlalchemy import ForeignKey
from sqlalchemy import Date

from sqlalchemy.orm import relationship

from api.database import Base


# ======================================================
# Dimension: Channels
# ======================================================

class Channel(Base):
    __tablename__ = "dim_channels"
    __table_args__ = {"schema": "marts"}

    channel_key = Column(
        Integer,
        primary_key=True
    )

    channel_name = Column(
        String,
        nullable=False,
        unique=True
    )

    messages = relationship(
        "Message",
        back_populates="channel"
    )


# ======================================================
# Dimension: Dates
# ======================================================

class DateDimension(Base):
    __tablename__ = "dim_dates"
    __table_args__ = {"schema": "marts"}

    date_key = Column(
        Integer,
        primary_key=True
    )

    full_date = Column(
        Date,
        nullable=False
    )

    year = Column(Integer)

    month = Column(Integer)

    day = Column(Integer)

    weekday = Column(String)

    messages = relationship(
        "Message",
        back_populates="date"
    )


# ======================================================
# Fact Messages
# ======================================================

class Message(Base):
    __tablename__ = "fct_messages"
    __table_args__ = {"schema": "marts"}

    message_id = Column(
        BigInteger,
        primary_key=True
    )

    channel_key = Column(
        Integer,
        ForeignKey("marts.dim_channels.channel_key")
    )

    date_key = Column(
        Integer,
        ForeignKey("marts.dim_dates.date_key")
    )

    message_text = Column(Text)

    views = Column(Integer)

    forwards = Column(Integer)

    channel = relationship(
        "Channel",
        back_populates="messages"
    )

    date = relationship(
        "DateDimension",
        back_populates="messages"
    )

    image_detection = relationship(
        "ImageDetection",
        uselist=False,
        back_populates="message"
    )


# ======================================================
# Fact Image Detections
# ======================================================

class ImageDetection(Base):
    __tablename__ = "fct_image_detections"
    __table_args__ = {"schema": "marts"}

    message_id = Column(
        BigInteger,
        ForeignKey("marts.fct_messages.message_id"),
        primary_key=True
    )

    channel_key = Column(Integer)

    date_key = Column(Integer)

    detected_class = Column(Text)

    confidence_score = Column(
        Numeric(5, 3)
    )

    image_category = Column(
        String
    )

    message = relationship(
        "Message",
        back_populates="image_detection"
    )