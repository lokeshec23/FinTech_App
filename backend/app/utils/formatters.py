"""
Indian currency and number formatting utilities
"""


def format_indian_currency(amount: float) -> str:
    """
    Format amount in Indian currency format with lakhs and crores
    Example: 1234567.89 -> ₹12,34,567.89
    """
    if amount < 0:
        sign = "-"
        amount = abs(amount)
    else:
        sign = ""
    
    # Split into integer and decimal parts
    amount_str = f"{amount:.2f}"
    integer_part, decimal_part = amount_str.split('.')
    
    # Indian number system formatting
    if len(integer_part) <= 3:
        formatted = integer_part
    else:
        # Last 3 digits
        last_three = integer_part[-3:]
        remaining = integer_part[:-3]
        
        # Add commas every 2 digits from right to left
        formatted_remaining = ""
        while remaining:
            if len(remaining) <= 2:
                formatted_remaining = remaining + formatted_remaining
                remaining = ""
            else:
                formatted_remaining = "," + remaining[-2:] + formatted_remaining
                remaining = remaining[:-2]
        
        formatted = formatted_remaining + "," + last_three
    
    return f"{sign}₹{formatted}.{decimal_part}"


def format_number_indian(number: int) -> str:
    """
    Format numbers in Indian style (lakhs, crores)
    Example: 123456 -> 1,23,456
    """
    number_str = str(abs(number))
    sign = "-" if number < 0 else ""
    
    if len(number_str) <= 3:
        return sign + number_str
    
    last_three = number_str[-3:]
    remaining = number_str[:-3]
    
    formatted_remaining = ""
    while remaining:
        if len(remaining) <= 2:
            formatted_remaining = remaining + formatted_remaining
            remaining = ""
        else:
            formatted_remaining = "," + remaining[-2:] + formatted_remaining
            remaining = remaining[:-2]
    
    return sign + formatted_remaining + "," + last_three
