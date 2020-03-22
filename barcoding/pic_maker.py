from barcode import EAN13
from barcode.writer import ImageWriter


with open(r'.\files\somefile.jpeg', 'wb') as f:
    EAN13('100029991111', writer=ImageWriter()).write(f)