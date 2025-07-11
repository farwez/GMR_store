from datetime import datetime

def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%b %d, %Y")
    except:
        return date_str

def validate_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
