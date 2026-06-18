from datetime import datetime

def validate_date(date_str):

    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m-%d-%Y"
    ]

    for fmt in formats:
        try:
            datetime.strptime(str(date_str), fmt)
            return True
        except:
            pass

    return False