from errors import send_error_message

class FinCode: 

    async def calculate(self, berthday: str) -> str:
        self.__day, self.__month, self.__year = map(int, berthday.split('.'))
        try:
            day = self.__calc_day(self.__day)
            month = self.__calc_month(self.__month) 
            year = self.__calc_year(self.__year) 
            code = self.__calc_code(day, month, year) 
            return f"{day}{month}{year}{code}"
        except Exception as ex:
            print(f'Ошибка {ex}')
            await send_error_message('Ошибка подсчета денежного кода')
            return ('Ошибка подсчета денежного кода')

    def __calc(self, data) -> int:
        data_sum = sum(map(int, str(data))) 
        if data_sum > 9:
            data_sum =  self.__calc(data_sum)
        return data_sum

    # TODO: use just self.__calc() ?
    def __calc_day(self, day) -> int:
        return self.__calc(day) 

    def __calc_month(self, month) -> int:
        return self.__calc(month) 

    # TODO: combine with __calc_code ?
    def __calc_year(self, year) -> int:
        year_sum = sum(map(int, str(sum(map(int, str(year))))))
        if year_sum > 9:
            year_sum = self.__calc_month(year_sum)
        return year_sum

    def __calc_code(self, day, month, year) -> int:
        code_sum = sum(map(int, str(day + month + year)))
        if code_sum > 9:
            return self.__calc(code_sum)
        return code_sum
