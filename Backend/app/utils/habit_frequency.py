from datetime import datetime, timezone

frequency_type = ('daily', 'weekly', 'monthly', 'yearly')


def can_complete_task(last_completed: datetime | None, frequency: str):

    now = datetime.now(timezone.utc)

    if last_completed is None:
        return True

    elif frequency == frequency_type[0]:
        return now.date() > last_completed.date()

    elif frequency == frequency_type[1]:
        return (now.year, now.isocalendar()[1]) > (last_completed.year, last_completed.isocalendar()[1])

    elif frequency == frequency_type[2]:
        return (now.year, now.month) > (last_completed.year, last_completed.month)

    elif frequency == frequency_type[3]:
        return now.year > last_completed.year

    else:
        raise ValueError('Invalid Input')
