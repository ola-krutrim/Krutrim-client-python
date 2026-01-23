from __future__ import annotations

from typing import Any
from typing_extensions import TypedDict, Annotated
from ..._utils import PropertyInfo

__all__ = ["PolicyParam"]


class PolicyParam(TypedDict, total=False):
    """
    Flexible ASG policy definition.
    Backend supports multiple policy shapes.
    """

    # Metric-based scaling
    predefined_metric_specification: Annotated[
        dict[str, Any],
        PropertyInfo(alias="PredefinedMetricSpecification"),
    ]

    up_scale_target_value: Annotated[
        int,
        PropertyInfo(alias="UpScaleTargetValue"),
    ]

    down_scale_target_value: Annotated[
        int,
        PropertyInfo(alias="DownScaleTargetValue"),
    ]

    scale_out_cooldown: Annotated[
        int,
        PropertyInfo(alias="ScaleOutCooldown"),
    ]

    scale_in_cooldown: Annotated[
        int,
        PropertyInfo(alias="ScaleInCooldown"),
    ]

    # Scheduled / custom policies
    predefined_metric_type: Annotated[
        str,
        PropertyInfo(alias="PredefinedMetricType"),
    ]

    up_scale_time: Annotated[
        str,
        PropertyInfo(alias="UpScaleTime"),
    ]

    down_scale_time: Annotated[
        str,
        PropertyInfo(alias="DownScaleTime"),
    ]
