import random
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

def id_generator():
    now = str(datetime.now())
    rand_num = random.sample(range(100000, 999999), 1)
    user_id = f"{now.split()[0]}-{rand_num[0]}"  # format -> user_ld = 2025-01-22-123456
    return user_id