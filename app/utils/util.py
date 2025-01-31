from datetime import datetime, timedelta
# Function to check if a year is a leap year
def is_leap_year(year):
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    return False


def renewal():
    current_date = datetime.now()
    year = current_date.year
    month = current_date.month
    day = current_date.day
    if is_leap_year(year):
        current_date += timedelta(days=366)
    else:
        current_date += timedelta(days=365)

    return current_date