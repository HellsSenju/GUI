from datamatrix import DataMatrix

# 11221726292507/000001/000002/000003/000004/000005/000006/000007/000008/000009/000010


code = "1122"
art = "172"
place = "629"
year = "25"
month = "07"
serial_pattern = "%06d"

all_code = code + art + place + year + month + "/" + "/".join([serial_pattern % i for i in range(1, 11)])

myDataMatrix = DataMatrix(
    all_code,
    pixel_size=20
)
myDataMatrix.big_datamatrix('big_test.png')
