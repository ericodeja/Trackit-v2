from sqlalchemy.orm import Session
from app.db.base import engine
from app.models.profile_changes import ProfileChange

def add_change(data):
    with Session(engine) as session:
        new_change = ProfileChange(
            user_id = data.user_id,
            field_name = data.field_name,
            old_value = data.old_value,
            new_value = data.new_value,
            changed_by = data.changed_by
        )

        session.add(new_change)
        session.commit()