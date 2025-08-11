#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont

from .codec_ascii import encode_to_ascii

from pathlib import Path

svg_template = \
    '<svg baseProfile="tiny" version="1.2" ' \
    'height="{height}px" width="{width}px" ' \
    'style="background-color:{bg}" ' \
    'xmlns="http://www.w3.org/2000/svg">' \
    '<path d="M{left_offset},{up_offset} {path_cmds}" stroke="{fg}" stroke-width="{stroke_width}"/></svg>'

font_path = Path(__file__).parent / 'fonts' / 'GOST_A.TTF'


class DataMatrix:
    """
    Create a datamatrix code for message 'msg'.

    Set rect=True for a rectangular datamatrix (if possible). Default is
    False, resulting in a square datamatrix.

    Set codecs to a list of codecs if you don't want DataMatrix to
    select freely from all codecs for minimum code size.
    """

    def __init__(
            self, msg: str, rect=False,
            pixel_size: int = 1,
            left_offset: int = 0,
            down_offset: int = 0
    ):
        self.message = msg
        self.rectangular = rect
        self.__pixel_size = pixel_size
        self.__left_offset = left_offset
        self.__down_offset = down_offset

    def __repr__(self):
        """Return a text representation of this object."""
        return f"DataMatrix('{self.message}')"

    def _repr_svg_(self):
        return self.svg(bg='#000', fg='#FFF')

    def __draw_datamatrix(self, draw: ImageDraw, start_x: int, start_y: int, mat: list):
        x, y = start_x, start_y

        for line in mat:
            for col in line:
                if col:
                    draw.rectangle(
                        (x, y, x + self.__pixel_size, y + self.__pixel_size),
                        fill='#000'
                    )

                x += self.__pixel_size
            y += self.__pixel_size
            x = start_x

    def big_datamatrix(self, filename: str):
        mat = self.matrix
        height = len(mat)
        width = len(mat[0])
        big_datamatrix_text_offset = 20
        big_datamatrix_offset_from_outline = 20
        big_datamatrix_text_data = ["КИ:", "КлФ:", "Пр.Пл.:", "Год:", "Месяц:"]
        big_datamatrix_text_answers_data = [
            self.message[:4],
            self.message[4:7],
            self.message[7:10],
            "20" + self.message[10:12],
            self.message[12:14],
        ]

        font_max = ImageFont.truetype(
            font_path.as_posix(),
            size=(height * self.__pixel_size + big_datamatrix_text_offset * 4 - 125) // 5
        )
        font_min = ImageFont.truetype(
            font_path.as_posix(),
            size=(height * self.__pixel_size + big_datamatrix_text_offset * 4 - 225) // 5
        )

        img = Image.new(
            'RGB',
            (
                (width * self.__pixel_size) * 2,
                (height * self.__pixel_size) * 2,
            ),
            (255, 255, 255)
        )
        draw = ImageDraw.Draw(img)
        self.__draw_datamatrix(draw, big_datamatrix_offset_from_outline, big_datamatrix_offset_from_outline, mat)

        text_y = 20
        for text in big_datamatrix_text_data:
            draw.text(
                (width * self.__pixel_size + 50, text_y),
                text,
                font=font_max,
                fill='#000',
                stroke_width=1
            )
            text_y += big_datamatrix_text_offset + font_max.size

        text_y = 20
        for text in big_datamatrix_text_answers_data:
            draw.text(
                (width * self.__pixel_size + 340, text_y),
                text,
                font=font_max,
                fill='#000',
                stroke_width=1
            )
            text_y += big_datamatrix_text_offset + font_max.size

        draw.rectangle(
            (big_datamatrix_offset_from_outline, height * self.__pixel_size + big_datamatrix_offset_from_outline * 2,
             (width * self.__pixel_size) * 2 - big_datamatrix_offset_from_outline,
             (height * self.__pixel_size) * 2 - big_datamatrix_offset_from_outline),
            fill='#fff',
            outline='#000',
            width=5
        )

        serial_numbers = self.message.split('/')[1:]
        first_column_serial_numbers = serial_numbers[:5]
        second_column_serial_numbers = serial_numbers[5:]

        text_y = height * self.__pixel_size + big_datamatrix_offset_from_outline * 2 + 20
        for index, serial_number in enumerate(first_column_serial_numbers):
            draw.text(
                (big_datamatrix_offset_from_outline + 10, text_y),
                f"{index + 1}.",
                font=font_min,
                fill='#000',
                stroke_width=1
            )
            draw.text(
                (big_datamatrix_offset_from_outline + 110, text_y),
                f"{self.message[4:7]}-{serial_number}",
                font=font_min,
                fill='#000'
            )
            text_y += big_datamatrix_text_offset + font_min.size

        text_y = height * self.__pixel_size + big_datamatrix_offset_from_outline * 2 + 20
        text_x = width * self.__pixel_size + big_datamatrix_offset_from_outline * 2
        for index, serial_number in enumerate(second_column_serial_numbers):
            draw.text(
                (text_x, text_y),
                f"{index + 6}.",
                font=font_min,
                fill='#000',
                stroke_width=1
            )
            draw.text(
                (text_x + 100, text_y),
                f"{self.message[4:7]}-{serial_number}",
                font=font_min,
                fill='#000'
            )
            text_y += big_datamatrix_text_offset + font_min.size

        img.save(filename)
        return filename

    def box_datamatrix(self, filename: str) -> str:
        mat = self.matrix
        height = len(mat)
        width = len(mat[0])

        img = Image.new(
            'RGB',
            (
                width * self.__pixel_size + 50,
                height * self.__pixel_size + 50,
            ),
            (255, 255, 255)
        )
        draw = ImageDraw.Draw(img)

        self.__draw_datamatrix(draw, 25, 25, mat)
        img.save(filename)

        return filename

    def drone_datamatrix(self, filename: str, code: str):
        mat = self.matrix
        height = len(mat)
        width = len(mat[0])
        fnt_max = ImageFont.truetype(
            font_path.as_posix(),
            size=245
        )

        fnt_min = ImageFont.truetype(
            font_path.as_posix(),
            size=187
        )

        img = Image.new(
            'RGB',
            (
                width * self.__pixel_size + 220,
                height * self.__pixel_size + 200
            ),
            (255, 255, 255)
        )
        draw = ImageDraw.Draw(img)
        self.__draw_datamatrix(draw, 200, 20, mat)

        draw.text(
            (200, height * self.__pixel_size + 50),
            code[10:],
            font=fnt_min,
            fill='#000',
            stroke_width=2
        )

        text_image_1 = Image.new(
            "RGBA",
            (980, 300),
            (255, 255, 255, 0)
        )
        draw_text_image_1 = ImageDraw.Draw(text_image_1)
        draw_text_image_1.text((0, 0), code[:10], font=fnt_max, fill='#000', stroke_width=1)

        text_image_1_rotated = text_image_1.rotate(90, expand=1)

        img.paste(
            text_image_1_rotated,
            (10, 0),
            text_image_1_rotated
        )

        img.save(filename)

    def _svg_path_iterator(self):
        mat = self.matrix
        w = len(mat[0])

        for line in mat:
            i = 0
            while i < w:
                color = line[i]
                i0 = i
                while i < w and line[i] == color:
                    i = i + 1

                length = i - i0
                if color == 1:
                    yield 'h'
                    yield str(length * self.__pixel_size)
                else:
                    yield 'm'
                    yield f'{length * self.__pixel_size},0'
            yield 'm'
            yield f'{-w * self.__pixel_size},{self.__pixel_size}'

    def svg(self, fg='#000', bg='#FFF'):
        """
        SVG of datamatrix.

        Use fg and bg arguments to specify foreground and background color,
        respectively. Colors are given as hex triplets such as fg=#F00
        (red).
        """
        cmds = ''.join(self._svg_path_iterator())
        mat = self.matrix
        height = len(mat)
        width = len(mat[0])
        return svg_template.format(
            fg=fg, bg=bg,
            path_cmds=cmds,
            height=height * self.__pixel_size + (
                self.__down_offset if self.__down_offset != self.__pixel_size // 2 else 0),
            width=width * self.__pixel_size + self.__left_offset,
            stroke_width=self.__pixel_size,
            left_offset=self.__left_offset,
            up_offset=self.__pixel_size // 2,
        )

    @property
    def matrix(self):
        """
        Return datamatrix as list of rows. Each row is a list of 1's and 0's.
        """

        def bit(_x, _y):
            m[_y] = m.get(_y, {})
            m[_y][_x] = 1

        m = {}
        enc = encode_to_ascii(self.message)
        enc = {i: c for i, c in enumerate(enc)}
        el = len(enc)

        nc = 1
        nr = 1  # symbol size, regions, region size
        j = - 1
        b = 1  # compute symbol size

        rs = [0] * 70  # reed solomon code
        rc = [0] * 70
        lg = [0] * 256  # log / exp table for multiplication
        ex = [0] * 255

        if self.rectangular and el < 50:  # rectangular code
            # symbol width, check words
            k = [16, 7, 28, 11, 24, 14, 32, 18, 32, 24, 44, 28]

            while True:
                j += 1
                w = k[j]  # width
                h = 6 + (j & 12)  # height
                bc = w * h // 8  # bytes count in symbol

                j += 1
                if bc - k[j] >= el:  # could we fill the rect?
                    break

            # column regions
            if w > 25:
                nc = 2

        else:  # square code
            w = h = 6
            i = 2  # size increment
            # rs check words
            k = [5, 7, 10, 12, 14, 18, 20, 24, 28, 36, 42, 48, 56, 68,
                 84, 112, 144, 192, 224, 272, 336, 408, 496, 620]

            while True:
                j += 1
                if j == len(k):
                    raise ValueError('Message is too long')

                if w > 11 * i:
                    i = 4 + i & 12  # advance increment

                h += i
                w = h
                bc = (w * h) >> 3

                if bc - k[j] >= el:
                    break

            if w > 27:
                nr = nc = 2 * (w // 54 | 0) + 2  # regions
            if bc > 255:
                b = 2 * (bc >> 9) + 2  # blocks

        s = k[j]  # rs check words
        fw = w // nc  # region size
        fh = h // nr

        # first padding
        if el < bc - s:
            enc[el] = 129
            el += 1

        # more padding
        while el < bc - s:
            enc[el] = (((149 * (el + 1)) % 253) + 130) % 254
            el += 1

        # Reed Solomon error detection and correction
        s //= b

        # log / exp table of Galois field
        j = 1
        for i in range(255):
            ex[i] = j
            lg[j] = i
            j += j

            if j > 255:
                j ^= 301  # 301 == a^8 + a^5 + a^3 + a^2 + 1

        # RS generator polynomial
        rs[s] = 0
        for i in range(1, s + 1):
            rs[s - i] = 1
            for j in range(s - i, s):
                rs[j] = rs[j + 1] ^ ex[(lg[rs[j]] + i) % 255]

        # RS correction data for each block
        for c in range(b):
            for i in range(s + 1):
                rc[i] = 0
            for i in range(c, el, b):
                x = rc[0] ^ enc[i]
                for j in range(s):
                    if x:
                        rc[j] = rc[j + 1] ^ ex[(lg[rs[j]] + lg[x]) % 255]
                    else:
                        rc[j] = rc[j + 1]

            # interleaved correction data
            for i in range(s):
                enc[el + c + i * b] = rc[i]

        # layout perimeter finder pattern
        # horizontal
        for i in range(0, h + 2 * nr, fh + 2):
            for j in range(0, w + 2 * nc):
                bit(j, i + fh + 1)
                if (j & 1) == 0:
                    bit(j, i)

        # vertical
        for i in range(0, w + 2 * nc, fw + 2):
            for j in range(h):
                bit(i, j + (j // fh | 0) * 2 + 1)
                if (j & 1) == 1:
                    bit(i + fw + 1, j + (j // fh | 0) * 2)

        s = 2  # step
        c = 0  # column
        r = 4  # row
        b = [  # nominal byte layout
            0, 0,
            -1, 0,
            -2, 0,
            0, -1,
            -1, -1,
            -2, -1,
            -1, -2,
            -2, -2]

        # diagonal steps
        i = 0
        while True:
            if i >= bc:
                break

            if r == h - 3 and c == - 1:
                k = [  # corner A layout
                    w, 6 - h,
                    w, 5 - h,
                    w, 4 - h,
                    w, 3 - h,
                       w - 1, 3 - h,
                    3, 2,
                    2, 2,
                    1, 2]
            elif r == h + 1 and c == 1 and (w & 7) == 0 and (h & 7) == 6:
                k = [  # corner D layout
                    w - 2, -h,
                    w - 3, -h,
                    w - 4, -h,
                    w - 2, -1 - h,
                    w - 3, -1 - h,
                    w - 4, -1 - h,
                    w - 2, -2,
                    -1, -2]
            else:
                if r == 0 and c == w - 2 and (w & 3):
                    r -= s
                    c += s
                    continue  # corner B: omit upper left
                if r < 0 or c >= w or r >= h or c < 0:  # outside
                    s = -s  # turn around
                    r += 2 + s // 2
                    c += 2 - s // 2

                    while r < 0 or c >= w or r >= h or c < 0:
                        r -= s
                        c += s

                if r == h - 2 and c == 0 and (w & 3):
                    k = [  # corner B layout
                        w - 1, 3 - h,
                        w - 1, 2 - h,
                        w - 2, 2 - h,
                        w - 3, 2 - h,
                        w - 4, 2 - h,
                        0, 1,
                        0, 0,
                        0, -1]
                elif r == h - 2 and c == 0 and (w & 7) == 4:
                    k = [  # corner C layout
                        w - 1, 5 - h,
                        w - 1, 4 - h,
                        w - 1, 3 - h,
                        w - 1, 2 - h,
                        w - 2, 2 - h,
                        0, 1,
                        0, 0,
                        0, -1]
                elif r == 1 and c == w - 1 and (w & 7) == 0 and (h & 7) == 6:
                    r -= s
                    c += s
                    continue  # omit corner D
                else:
                    k = b  # nominal L - shape layout

            # layout each bit
            el = enc[i]
            i += 1
            j = 0
            while True:
                if el <= 0:
                    break

                if el & 1:
                    x = c + k[j]
                    y = r + k[j + 1]

                    # wrap around
                    if x < 0:
                        x += w
                        y += 4 - ((w + 4) & 7)
                    if y < 0:
                        y += h
                        x += 4 - ((h + 4) & 7)

                    # region gap
                    bit(x + 2 * (x // fw | 0) + 1, y + 2 * (y // fh | 0) + 1)

                j += 2
                el >>= 1

            r -= s
            c += s

        # unfilled corner
        i = w
        while True:
            if not i & 3:
                break

            bit(i, i)
            i -= 1

        matrix = []
        rows = h + 2 * nr
        cols = w + 2 * nc
        for j in range(rows):
            matrix.append([])
            for i in range(cols):
                matrix[j].append(m[j].get(i, 0))

        return matrix
