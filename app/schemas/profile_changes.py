from pydantic import BaseModel
from typing import Optional

class ProfileChanges(BaseModel):
    user_id : int
    field_name: str
    old_value: Optional[str]
    new_value: Optional[str]
    changed_by: int