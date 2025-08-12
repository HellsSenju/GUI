from datamatrix import DataMatrix


def save_svg(svg_code: str):
    with open("test.svg", "w") as f:
        f.write(svg_code)


code = "1122"
art = "172"
place = "629"
year = "25"
month = "07"
serial_pattern = "%06d"

missed = [
    878,
    303,
    994,
    495,
    399,
    464,
    704,
    287,
    478,
    473,
    991,
    431,
    461,
    967,
    397,
    284,
    976,
    943,
    327,
    396,
    285,
    395,
    274,
    725,
]

for i in missed:
    serial = serial_pattern % i

    all_datamatrix_code = code + art + place + year + month + serial
    dm = DataMatrix(
        msg=all_datamatrix_code,
        pixel_size=50,
        left_offset=200,
        down_offset=140,
    )
    dm.drone_datamatrix(f"missed/{all_datamatrix_code}.png", all_datamatrix_code)
    print(all_datamatrix_code, f"complete {i + 1}/1000")
