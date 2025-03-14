from copy import deepcopy
from typing import Optional, Type, Any, Tuple

from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo


def partial_model(model: Type[BaseModel]):
    def make_field_optional(
        field: FieldInfo, default: Any = None
    ) -> Tuple[Any, FieldInfo]:
        new = deepcopy(field)
        new.default = default
        new.annotation = Optional[field.annotation]  # type: ignore
        return new.annotation, new

    return create_model(
        f"Partial{model.__name__}",
        __base__=model,
        __module__=model.__module__,
        **{
            field_name: make_field_optional(field_info)
            for field_name, field_info in model.model_fields.items()
        },
    )


class MountainPeak(BaseModel):
    id: int
    name: str
    lat: float
    lng: float
    altitude: int


class MountainPeakCreateOrUpdate(BaseModel):
    name: str
    lat: float
    lng: float
    altitude: int


MountainPeakOptional = partial_model(MountainPeakCreateOrUpdate)
