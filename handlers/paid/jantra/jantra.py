from PIL import Image, ImageDraw, ImageFont
from functools import cache
import os
import io

class Jantra:
    __single_digit: int = 1
    __font_size: int = 20
    __cell_size_px: int = 50
    __font_color: str = 'black'
    __background_color: str = 'white'
    __line_width: int = 2

    @classmethod
    @cache
    def create(cls, date: str) -> tuple[bytes, int]:
        cls.__day, cls.__month, cls.__year = map(int, date.split('.'))
        cls.__jantra_digits: list[list[int]] = cls.__calculate_jantra()
        jantra_image_bytes: bytes = cls.__draw()
        lucky_number: int = cls.__calculate_lucky_number()

        return jantra_image_bytes, lucky_number 

    @classmethod
    def __calculate_jantra(cls) -> list[list[int]]:
        A: int = cls.__month
        B: int = cls.__day
        C: int = int(str(cls.__year)[-2:])  
        D: int = cls.__calculate_D()

        result = [
            [A, B, C, D],
            [C - 2, D + 2, A - 2, B + 2],
            [D + 1, C + 1, B - 1, A - 1],
            [B + 1, A - 3, D + 3, C - 1]
        ]

        return result 

    @classmethod
    def __calculate_D(cls) -> int:
        d: int = sum([int(digit) for digit in str(cls.__day + cls.__month + cls.__year)])
        d: int = cls.__convertToSingleDigit(d)
        return d

    @staticmethod
    def __convertToSingleDigit(num: int) -> int:
        while num > 9:  
            if num == 22 or num == 11:
                break
            num = sum([int(digit) for digit in str(num)])
        return num 

    @classmethod
    def __draw(cls) -> bytes:

        root_folder = "staticfiles"
        fonts_folder = "fonts"
        font_filename = "BarlowCondensed-SemiBoldItalic.ttf"
        font_path = os.path.join(root_folder, fonts_folder, font_filename)

        # Базовый шрифт
        font = ImageFont.truetype(font_path, cls.__font_size)

        width = len(cls.__jantra_digits[0]) * cls.__cell_size_px
        height = len(cls.__jantra_digits) * cls.__cell_size_px

        image = Image.new('RGB', (width, height), cls.__background_color)
        draw = ImageDraw.Draw(image)

        for row in range(len(cls.__jantra_digits)):
            for col in range(len(cls.__jantra_digits[row])):
                x = col * cls.__cell_size_px
                y = row * cls.__cell_size_px

                # Расчет координат центра ячейки
                center_x = x + cls.__cell_size_px // 2
                center_y = y + cls.__cell_size_px // 2.5

                # Определение размеров текста
                text_width, text_height = draw.textsize(str(cls.__jantra_digits[row][col]))

                # Определение координат верхнего левого угла текста для выравнивания по центру ячейки
                text_x = center_x - text_width // 2
                text_y = center_y - text_height // 2

                # Рисование прямоугольника
                draw.rectangle((x, y, x + cls.__cell_size_px, y + cls.__cell_size_px), outline='black', width=cls.__line_width)

                # Рисование текста
                draw.text((text_x, text_y), str(cls.__jantra_digits[row][col]), font=font, fill=cls.__font_color)

        byte_stream = io.BytesIO()
        image.save(byte_stream, format='PNG')
        byte_stream.seek(0)

        return byte_stream.read()

    @classmethod
    def __calculate_lucky_number(cls) -> int:
        row_sums = [sum(row) for row in cls.__jantra_digits]
        lucky_number = sum(int(digit) for digit in str(row_sums[0]))
        if len(str(lucky_number)) == cls.__single_digit: 
            return int(lucky_number)
        else:
            return sum(int(digit) for digit in str(lucky_number))    
