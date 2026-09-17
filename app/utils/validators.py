from datetime import datetime


def validate_date_range(
    start_date: datetime,
    end_date: datetime
):
    if end_date <= start_date:
        raise ValueError(
            "End date must be after start date"
        )

    return True


def validate_registration_period(
    registration_start: datetime,
    registration_end: datetime,
    event_start: datetime
):
    if registration_end < registration_start:
        raise ValueError(
            "Registration end must be after registration start"
        )

    if registration_end > event_start:
        raise ValueError(
            "Registration end cannot be after event start"
        )

    return True


def validate_capacity(capacity: int):
    if capacity <= 0:
        raise ValueError(
            "Capacity must be greater than 0"
        )

    return True


def validate_rating(rating: int):
    if rating < 1 or rating > 5:
        raise ValueError(
            "Rating must be between 1 and 5"
        )

    return True


def validate_price(price: float):
    if price < 0:
        raise ValueError(
            "Price cannot be negative"
        )

    return True


def validate_quantity(quantity: int):
    if quantity <= 0:
        raise ValueError(
            "Quantity must be greater than 0"
        )

    return True


def validate_ticket_stock(
    quantity: int,
    available_quantity: int
):
    if available_quantity < 0:
        raise ValueError(
            "Available quantity cannot be negative"
        )

    if available_quantity > quantity:
        raise ValueError(
            "Available quantity cannot exceed total quantity"
        )

    return True