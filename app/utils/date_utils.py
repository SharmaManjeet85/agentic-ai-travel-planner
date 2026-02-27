from datetime import datetime

def normalize_date(date_str: str) -> str:
    """
    Convert DD/MM/YYYY or YYYY-MM-DD → YYYY-MM-DD
    """
    try:
        # Already ISO
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        pass

    try:
        # DD/MM/YYYY
        return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}")