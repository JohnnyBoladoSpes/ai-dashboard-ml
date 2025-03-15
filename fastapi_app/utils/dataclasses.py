from dataclasses import fields
from typing import Type, TypeVar, Union

T = TypeVar("T")


def build_dataclass_from_model_instance(
    klass: Type[T], instance: Union[dict, object], **kwargs
) -> T:
    """
    Converts a dictionary (MongoDB document) or a Django model instance into a dataclass.
    Allows adding extra fields via kwargs.
    """
    # Get the dataclass fields
    dataclass_field_names = {f.name for f in fields(klass)}

    # Exclude manually provided attributes
    dataclass_field_names -= kwargs.keys()

    # Extract data (compatible with dict or Django models)
    _kwargs = {
        field: (
            getattr(instance, field, None)
            if hasattr(instance, field)
            else instance.get(field, None)
        )
        for field in dataclass_field_names
    }

    # Convert MongoDB `_id` to string if present
    if "_id" in instance:
        _kwargs["_id"] = str(instance["_id"])

    # Merge with provided kwargs
    _kwargs.update(kwargs)

    return klass(**_kwargs)
