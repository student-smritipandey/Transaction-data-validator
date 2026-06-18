def validate_payment(mode):

    allowed_modes = [
        "UPI",
        "CARD",
        "CASH",
        "PAYPAL",
        "NETBANKING"
    ]

    return str(mode).strip().upper() in allowed_modes