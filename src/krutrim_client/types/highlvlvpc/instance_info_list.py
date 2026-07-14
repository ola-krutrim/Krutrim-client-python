
from typing import List, Optional

from ..._models import BaseModel
from .instance_info import InstanceInfo

__all__ = ["InstanceInfoList"]


class InstanceInfoList(BaseModel):
    instances: Optional[List[InstanceInfo]] = None

    total_count: Optional[int] = None
    """The total number of instances matching the filter."""

    page: Optional[int] = None
    """The current page number."""

    page_size: Optional[int] = None
    """The number of items per page."""

    total_pages: Optional[int] = None
    """The total number of pages."""
