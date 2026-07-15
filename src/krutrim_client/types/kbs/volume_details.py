
from typing import Any, Dict, List, Optional
from datetime import datetime
from typing_extensions import TypeAlias

from pydantic import Field as FieldInfo

from .qos import Qos
from .source import Source
from ..._models import BaseModel

__all__ = ["VolumeDetail", "Attachment", "VolumeList", "VolumeActionResponse"]


class Attachment(BaseModel):
    device: Optional[str] = None
    instance_id: Optional[str] = None
    instance_name: Optional[str] = None
    volume_id: Optional[str] = None
    remote_attachment_id: Optional[str] = None


class VolumeDetail(BaseModel):
    id: Optional[str] = None
    """Unique identifier / KRN of the volume."""

    Name: Optional[str] = None
    """Volume name (API returns capital N)."""

    name: Optional[str] = None
    """Volume name (alternate)."""

    attachments: Optional[List[Attachment]] = None
    availability_zone: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    krn: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    multiattach: Optional[bool] = None
    multi_attached_enabled: Optional[bool] = None
    qos: Optional[Qos] = None
    size: Optional[int] = None
    source: Optional[Source] = None
    source_type: Optional[str] = None
    source_id: Optional[str] = None
    status: Optional[str] = None
    state: Optional[str] = None
    bootable: Optional[bool] = None
    volume_type: Optional[str] = None
    volumetype: Optional[str] = None
    description: Optional[str] = None
    remote_volume_id: Optional[str] = None
    account_id: Optional[str] = None
    project_id: Optional[str] = None
    k_customer_id: Optional[str] = None
    last_action: Optional[str] = None
    last_action_status: Optional[str] = None
    last_action_log: Optional[str] = None
    encrypted: Optional[bool] = None
    tags: Optional[Any] = None
    snapshot_policy: Optional[Any] = None
    backup_policy: Optional[Any] = None
    kms_key_id: Optional[str] = None
    tenant_id: Optional[str] = None


VolumeList: TypeAlias = List[VolumeDetail]


class VolumeActionResponse(BaseModel):
    message: Optional[str] = None
