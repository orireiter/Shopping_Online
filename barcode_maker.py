from barcode import EAN13, Code128
from barcode.writer import ImageWriter
import os.path

def make(itemname, barcode_num):
    itemname = str(itemname)
    # itemname1 = itemname.replace('"',"")
    # print(itemname)
    pather = r'.\static\barcoding\\' + itemname + '.jpeg'
    num = str(barcode_num)
    
    if os.path.isfile(pather):
        pass
    elif len(num) < 2:
        pass
    elif num == "#N/A":
        num = "NO Barcode"
        with open(pather, 'wb') as f:
            Code128(num, writer=ImageWriter()).write(f)
    else:
        with open(pather, 'wb') as f:
            Code128(num, writer=ImageWriter()).write(f)
