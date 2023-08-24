import calendar
import datetime
import random

def get_calendar_dates():
    current_date = datetime.date.today()
    days_in_month = calendar.monthrange(current_date.year, current_date.month)[1]
    num_dates = random.randint(12, 16)
    random_dates = random.sample(range(1, days_in_month + 1), num_dates)
    sorted_dates = sorted(random_dates)
    dates_string = ', '.join(str(date) for date in sorted_dates)
    return dates_string
