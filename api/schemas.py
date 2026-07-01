from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict


# =====================================================
# Channel Schemas
# =====================================================

class ChannelBase(BaseModel):
    channel_name: str


class Channel(ChannelBase):
    channel_key: int

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# Date Dimension Schemas
# =====================================================

class DateBase(BaseModel):

    full_date: date

    year: int

    month: int

    day: int

    weekday: str


class DateDimension(DateBase):

    date_key: int

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# Image Detection Schemas
# =====================================================

class ImageDetectionBase(BaseModel):

    detected_class: Optional[str] = None

    confidence_score: Optional[Decimal] = None

    image_category: Optional[str] = None


class ImageDetection(ImageDetectionBase):

    message_id: int

    channel_key: int

    date_key: int

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# Message Schemas
# =====================================================

class MessageBase(BaseModel):

    message_text: Optional[str] = None

    views: Optional[int] = None

    forwards: Optional[int] = None


class Message(MessageBase):

    message_id: int

    channel_key: int

    date_key: int

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# Detailed Message Response
# =====================================================

class MessageDetail(Message):

    channel: Optional[Channel] = None

    date: Optional[DateDimension] = None

    image_detection: Optional[ImageDetection] = None

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# Analytics Response
# =====================================================

class AnalyticsSummary(BaseModel):

    total_messages: int

    total_channels: int

    total_images: int

    average_views: float

    average_confidence: float


# =====================================================
# Channel Statistics
# =====================================================

class ChannelStatistics(BaseModel):

    channel_name: str

    total_messages: int

    total_images: int

    average_views: float

    promotional_images: int


# =====================================================
# Image Category Statistics
# =====================================================

class ImageCategoryStatistics(BaseModel):

    image_category: str

    total: int