from datetime import datetime

def parse_iso_datetime(dt_str):
    if dt_str.endswith('Z'):
        dt_str = dt_str[:-1]
    dt = datetime.fromisoformat(dt_str)
    return dt.replace(tzinfo=None) 