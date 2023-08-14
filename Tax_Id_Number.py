import time
from unicodedata import decimal
import re
import jdatetime
import datetime
from datetime import date
import random
from nltk import flatten
import datetime
import time


def date_to_hex(Year,Month,Day):
    gregorian_date = jdatetime.date(Year, Month, Day).togregorian()
    to_str = str(gregorian_date).split('-')

    date_time = datetime.datetime(int(to_str[0]), int(to_str[1]), int(to_str[2]))
    y = time.mktime(date_time.timetuple()) * 1000

    d0 = date(1970, 1, 1)
    d1 = date(int(to_str[0]), int(to_str[1]), int(to_str[2]))
    delta = d1 - d0
    days = delta.days
    to_hex = ('0' + hex(days).removeprefix('0x'))
    return to_hex ,int(y)
verhoeff_table_d = (
    (0,1,2,3,4,5,6,7,8,9),
    (1,2,3,4,0,6,7,8,9,5),
    (2,3,4,0,1,7,8,9,5,6),
    (3,4,0,1,2,8,9,5,6,7),
    (4,0,1,2,3,9,5,6,7,8),
    (5,9,8,7,6,0,4,3,2,1),
    (6,5,9,8,7,1,0,4,3,2),
    (7,6,5,9,8,2,1,0,4,3),
    (8,7,6,5,9,3,2,1,0,4),
    (9,8,7,6,5,4,3,2,1,0))
verhoeff_table_p = (
    (0,1,2,3,4,5,6,7,8,9),
    (1,5,7,6,2,8,3,0,9,4),
    (5,8,0,3,7,9,6,1,4,2),
    (8,9,1,6,0,4,3,5,2,7),
    (9,4,5,3,1,2,6,8,7,0),
    (4,2,8,6,5,7,3,9,0,1),
    (2,7,9,3,8,0,6,4,1,5),
    (7,0,4,6,9,1,3,2,5,8))
verhoeff_table_inv = (0,4,3,2,1,5,6,7,8,9)
def calcsum(number):
    #or a given number returns a Verhoeff checksum digit
    c = 0
    for i, item in enumerate(reversed(str(number))):
        c = verhoeff_table_d[c][verhoeff_table_p[(i+1)%8][int(item)]]
    return verhoeff_table_inv[c]



def convert_to_utf_8(shenase_yekta):
    utf_8_dict ={"A":65,"B":66,"C":67,"D":68,"E":69,"F":70,"G":71,"H":72,"I":73,"J":74,"K":75,"L":76,"M":77,"N":78,"O":79,"P":80,"Q":81,"R":82,"S":83,"T":84,"U":85,"V":86,"W":87,"X":88,"Y":89,"Z":90}
    mamno_character =["I","J","L","Q","V"]
    utf8_number=[]
    for i in shenase_yekta:
        if i >= '0' and i <= '9':
            utf8_number.append(int(i))
        for y in utf_8_dict.keys():
            if i not in mamno_character and y == i :
                utf8_number.append(utf_8_dict[y])

    return ''.join(map(str, utf8_number))



def verhoff_inputer(shenaseh_yekta,hex_date,serial_hex): # Convert to Verhoeff
    date_hex= int(hex_date[0],16)
    date_hex_with_0 = str(date_hex).rjust(6, '0')


    serial_dec =str(int(serial_hex, 16))
    serial = serial_dec.rjust(12, '0')

    return str(shenaseh_yekta) + date_hex_with_0 + serial



def Tax_Number(shenaseh_yekta):
    range = str(random.randint(0,999999999999))
    serial_hex = hex(int(range)).removeprefix('0x')
    serial= serial_hex.rjust(10, '0')
    shenaseh_yekta_uft8=convert_to_utf_8(shenaseh_yekta)
    hex_date=date_to_hex(1402,3,1) # jalali date



    verhoff_number = verhoff_inputer(shenaseh_yekta_uft8, hex_date, serial)
    verhoff= calcsum(verhoff_number)
    milisecond_timestamp = hex_date[1]
    tax_number ={"shenaseh_yekta":str(shenaseh_yekta),"hex_date":str(hex_date[0]),"serial":str(serial),"verhoff":str(verhoff)}
    return  tax_number,milisecond_timestamp

