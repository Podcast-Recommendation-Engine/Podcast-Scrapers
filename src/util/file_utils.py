import re
from email.utils import parsedate_to_datetime

def sanitize_title(title, date_str=None):
    sanitized_title = re.sub(r'[\\/*?:"<>|]', '', title)
    sanitized_title = sanitized_title.replace(' ', '_').lower()

    if date_str:
        try:
            date = parsedate_to_datetime(date_str)
            sanitized_title = f'{date.strftime("%Y-%m-%d")}_{sanitized_title}'
        except (ValueError, TypeError):
            pass

    return sanitized_title
