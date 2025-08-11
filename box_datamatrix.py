from datamatrix import DataMatrix

place = "629"
year = "25"
month = "07"
serial_pattern = "%06d"

dm = DataMatrix(
    msg= place + year + month + "000089",
    pixel_size=50,
)
dm.box_datamatrix(f'box_test.png')

# for i in range(101, 1001):
#     serial = serial_pattern % i
#
#     all_datamatrix_code = place + year + month + serial
#     dm = DataMatrix(
#         msg=all_datamatrix_code,
#         pixel_size=50,
#     )
#     dm.box_datamatrix(f'box_datamatrix/{all_datamatrix_code}.png')
#     print(all_datamatrix_code, f"complete {i + 1}/1000")
