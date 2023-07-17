from errors import send_error_message

async def calculate_code(berthday: str) -> str:
    day, month, year = map(int, berthday.split('.'))
    try:
        day_sum = sum(map(int, str(day)))
        month_sum = sum(map(int, str(month)))
        year_sum = sum(map(int, str(sum(map(int, str(year))))))
        code = sum(map(int, str(day_sum + month_sum + year_sum)))
        return f"{day_sum}{month_sum}{year_sum}{code}"
    except Exception as ex:
        print(f'Ошибка {ex}')
        await send_error_message("Ошибка подсчета денежного кода")
        return ("Ошибка подсчета денежного кода")
