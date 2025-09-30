from app.models.profile_changes import ProfileChange
from app.db.db_connection import db_connection

def add_change(data):
        new_change = ProfileChange(
            user_id = data.user_id,
            field_name = data.field_name,
            old_value = data.old_value,
            new_value = data.new_value,
            changed_by = data.changed_by
        )

        db_connection.add(new_change)