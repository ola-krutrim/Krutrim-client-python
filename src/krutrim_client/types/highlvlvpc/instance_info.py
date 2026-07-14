
from typing import Any, List, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from ..._models import BaseModel


__all__ = ["InstanceInfo"]


class InstanceInfo(BaseModel):
    """Instance fields from search_instances / retrieve_instance."""

    krn: Optional[str] = None
    """Instance KRN."""

    vm_name: Optional[str] = None
    """Name of the instance."""

    instance_name: Optional[str] = FieldInfo(alias="instanceName", default=None)
    """Legacy alias for vm_name."""

    status: Optional[str] = None
    """Current status of the instance."""

    region: Optional[str] = None
    """Region where the instance is located."""

    flavor_name: Optional[str] = None
    """Instance flavor / type (e.g. CPU-2x-8GB)."""

    instance_type: Optional[str] = FieldInfo(alias="instanceType", default=None)

    ip_fixed: Optional[str] = None
    """Primary private IP address."""

    ip_list: Optional[str] = None
    """JSON string of fixed/floating IP entries from search_instances."""

    ip_addresses: Optional[str] = None
    """JSON string of IP entries from retrieve_instance."""

    ip_address: Optional[str] = FieldInfo(alias="ipAddress", default=None)
    floating_ip_address: Optional[str] = FieldInfo(alias="floatingIpAddress", default=None)

    project_krn: Optional[str] = None
    """VPC KRN the instance belongs to."""

    vpc_id: Optional[str] = FieldInfo(alias="vpcId", default=None)
    network_id: Optional[str] = FieldInfo(alias="networkId", default=None)
    subnet_id: Optional[str] = FieldInfo(alias="subnetId", default=None)

    sshkey_name: Optional[str] = None
    security_groups: Optional[List[Any]] = None
    network_ports: Optional[List[Any]] = None
    volumes: Optional[List[Any]] = None
    tags: Optional[List[Any]] = None

    account_id: Optional[str] = None
    user_name: Optional[str] = None
    project_name: Optional[str] = None
    locked: Optional[bool] = None
    asg_check: Optional[bool] = None
    delete_protection_status: Optional[bool] = None
    manage_del_protection: Optional[bool] = None
    subnet_visibility: Optional[bool] = None
    flavor_cost: Optional[float] = None
    flavor_type: Optional[str] = None
    image_krn: Optional[str] = None
    instance_id: Optional[str] = FieldInfo(alias="instanceId", default=None)
    created_at: Optional[datetime] = None
    batch_id: Optional[str] = None
    task_id: Optional[str] = None
    failed_step: Optional[str] = None
    failure_reason: Optional[str] = None
    ssh_id: Optional[str] = None
    ssh_status: Optional[str] = None
    vm_volume_disk_size: Optional[str] = None
