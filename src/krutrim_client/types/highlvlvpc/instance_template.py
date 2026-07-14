
from __future__ import annotations

from typing import List, Optional, Any

from ..._models import BaseModel

__all__ = [
    "InstanceTemplateConfig",
    "InstanceTemplate",
    "InstanceTemplateList",
    "BatchVmCreateResponse",
]


class InstanceTemplateConfig(BaseModel):
    image_krn: Optional[str] = None
    image_name: Optional[str] = None
    instanceType: Optional[str] = None
    isGpu: Optional[bool] = None
    network_id: Optional[str] = None
    network_name: Optional[str] = None
    region: Optional[str] = None
    security_groups: Optional[List[str]] = None
    security_group_names: Optional[List[Any]] = None
    sshkey_name: Optional[str] = None
    subnet_id: Optional[str] = None
    subnet_name: Optional[str] = None
    user_data: Optional[str] = None
    volume_name: Optional[str] = None
    volume_size: Optional[int] = None
    volumetype: Optional[str] = None
    vpc_id: Optional[str] = None
    vpc_name: Optional[str] = None


class InstanceTemplate(BaseModel):
    account_id: Optional[str] = None
    config: Optional[InstanceTemplateConfig] = None
    created_at: Optional[str] = None
    customer_id: Optional[str] = None
    name: Optional[str] = None
    template_krn: Optional[str] = None
    updated_at: Optional[str] = None


class InstanceTemplateList(BaseModel):
    templates: Optional[List[InstanceTemplate]] = None
    data: Optional[List[InstanceTemplate]] = None
    total_count: Optional[int] = None
    page: Optional[int] = None
    limit: Optional[int] = None


class BatchVmCreateResponse(BaseModel):
    batch_source: Optional[str] = None
    job_id: Optional[str] = None
    message: Optional[str] = None
    total_count: Optional[int] = None
