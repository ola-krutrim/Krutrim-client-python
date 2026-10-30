from __future__ import annotations

from typing import List, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = [
    "SshkeyListResponse",
    "SshkeyListMeta",
    "SshkeyListItem",
    "SshkeyVmAttached",
]


class SshkeyVmAttached(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None


class SshkeyListMeta(BaseModel):
    limit: Optional[int] = None
    page: Optional[int] = None
    region: Optional[str] = None
    sort_by: Optional[str] = FieldInfo(alias="sortBy", default=None)
    sort_order: Optional[str] = FieldInfo(alias="sortOrder", default=None)
    total: Optional[int] = None
    total_pages: Optional[int] = FieldInfo(alias="totalPages", default=None)


class SshkeyListItem(BaseModel):
    id: Optional[str] = FieldInfo(alias="_id", default=None)
    account_id: Optional[str] = FieldInfo(alias="accountId", default=None)
    uuid: Optional[str] = None
    key_name: Optional[str] = FieldInfo(alias="keyName", default=None)
    public_key: Optional[str] = FieldInfo(alias="publicKey", default=None)
    user_id: Optional[str] = FieldInfo(alias="userId", default=None)
    created_by: Optional[str] = FieldInfo(alias="createdBy", default=None)
    created_at: Optional[datetime] = FieldInfo(alias="createdAt", default=None)
    updated_at: Optional[datetime] = FieldInfo(alias="updatedAt", default=None)
    vm_attached: Optional[List[SshkeyVmAttached]] = FieldInfo(alias="vmAttached", default=None)
    region: Optional[str] = None
    status: Optional[str] = None
    expires_at: Optional[datetime] = FieldInfo(alias="expiresAt", default=None)


class SshkeyListResponse(BaseModel):
    """Response for GET /v2/sshkeys/{customer_id}.

    Matches the console curl shape: ``{"meta": {...}, "sshKeys": [...]}``.
    When the API returns 204 No Content (no keys), the SDK returns this with
    ``ssh_keys=[]``.
    """

    meta: Optional[SshkeyListMeta] = None
    ssh_keys: List[SshkeyListItem] = FieldInfo(alias="sshKeys", default_factory=list)
