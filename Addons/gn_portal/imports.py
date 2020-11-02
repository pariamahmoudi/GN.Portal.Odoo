from odoo import models, fields, api
from math import ceil
from typing import TYPE_CHECKING, Any, List, Dict
import logging
#from .models.parnian_translation_branch import ParnianTranslationBranch
if TYPE_CHECKING:
    from odoo.addons.base.models.res_partner import Partner
    from odoo.addons.product.models.product import ProductProduct
    from odoo.addons.product.models.product_template import ProductTemplate
    from odoo.addons.sale.models.sale import SaleOrder, SaleOrderLine
    from odoo.addons.account.models.account_move import AccountMove, AccountMoveLine
else:
    Partner = models.Model
    ProductTemplate = models.Model
    ProductProduct = models.Model
    SaleOrder = models.Model
    SaleOrderLine = models.Model
    AccountMove = models.Model
    AccountMoveLine = models.Model
#dervied from http://farsitools.sf.net
#Copyright (C) 2003-2011  Parspooyesh Fanavar (http://parspooyesh.com/)
#see LICENSE.txt
g_days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
j_days_in_month = [31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29]

class Utils():
    @staticmethod
    def numbertotext(t):
        return "hi"
class GregorianToJalali:

    def __init__(self,gyear,gmonth,gday):
        """
            Convert gregorian date to jalali date
            gmonth: number of month in range 1-12
        """
        self.gyear=gyear
        self.gmonth=gmonth
        self.gday=gday
        self.__gregorianToJalali()

    def getJalaliList(self):
        return (self.jyear,self.jmonth,self.jday)

    def __gregorianToJalali(self):
        """
            g_y: gregorian year
            g_m: gregorian month
            g_d: gregorian day
        """
        global g_days_in_month,j_days_in_month

        gy = self.gyear-1600
        gm = self.gmonth-1
        gd = self.gday-1

        g_day_no = 365*gy+(gy+3)//4-(gy+99)//100+(gy+399)//400

        for i in range(gm):
            g_day_no += g_days_in_month[i]
        if gm>1 and ((gy%4==0 and gy%100!=0) or (gy%400==0)):
            # leap and after Feb
            g_day_no+=1
        g_day_no += gd

        j_day_no = g_day_no-79

        j_np = j_day_no // 12053
        j_day_no %= 12053
        jy = 979+33*j_np+4*int(j_day_no//1461)

        j_day_no %= 1461

        if j_day_no >= 366:
            jy += (j_day_no-1)// 365
            j_day_no = (j_day_no-1)%365

        for i in range(11):
            if not j_day_no >= j_days_in_month[i]:
                i-=1
                break
            j_day_no -= j_days_in_month[i]

        jm = i+2
        jd = j_day_no+1


        self.jyear=jy
        self.jmonth=jm
        self.jday=jd



class JalaliToGregorian:
    def __init__(self,jyear,jmonth,jday):
        """
            Convert db time stamp (in gregorian date) to jalali date
        """
        self.jyear=jyear
        self.jmonth=jmonth
        self.jday=jday
        self.__jalaliToGregorian()

    def getGregorianList(self):
        return (self.gyear,self.gmonth,self.gday)


    def __jalaliToGregorian(self):
        global g_days_in_month,j_days_in_month
        jy = self.jyear-979
        jm = self.jmonth-1
        jd = self.jday-1


        j_day_no = 365*jy +int(jy//33)*8 + (jy%33+3)//4
        for i in range(jm):
            j_day_no += j_days_in_month[i]

        j_day_no += jd

        g_day_no = j_day_no+79

        gy = 1600 + 400*int(g_day_no// 146097) # 146097 = 365*400 + 400/4 - 400/100 + 400/400
        g_day_no = g_day_no % 146097

        leap = 1
        if g_day_no >= 36525: # 36525 = 365*100 + 100/4
            g_day_no-=1
            gy += 100*int(g_day_no// 36524) # 36524 = 365*100 + 100/4 - 100/100
            g_day_no = g_day_no % 36524

            if g_day_no >= 365:
                g_day_no+=1
            else:
                leap = 0


        gy += 4*int(g_day_no//1461) # 1461 = 365*4 + 4/4
        g_day_no %= 1461

        if g_day_no >= 366:
            leap = 0
            g_day_no-=1
            gy += g_day_no//365
            g_day_no = g_day_no % 365

        i=0
        while g_day_no >= g_days_in_month[i] + (i == 1 and leap):
            g_day_no -= g_days_in_month[i] + (i == 1 and leap)
            i+=1
        self.gmonth = i+1
        self.gday = g_day_no+1
        self.gyear = gy
unit = {
"0" : "" ,
"1" : "یک" ,  
"2" : "دو" , 
"3" : "سه" ,
"4" : "چهار" ,
"5" : "پنج" , 
"6" : "شش" , 
"7" : "هفت" , 
"8" : "هشت" , 
"9" : "نه"}

tens = {
"0" : "" ,
"10" : "ده" , 
"11" : "یازده" , 
"12" : "دوازده" , 
"13" : "سیزده" , 
"14" : "چهارده" , 
"15" : "پانزده" , 
"16" : "شانزده" , 
"17" : "هفده" , 
"18" : "هجده" , 
"19" : "نوزده" , 
"2" : "بیست" , 
"3" : "سی" , 
"4" : "چهل" , 
"5" : "پنجاه" , 
"6" : "شصت" , 
"7" : "هفتاد" , 
"8" : "هشتاد" , 
"9" : "نود"}

hundreds = {
"0" : "" ,
"1" : "یکصد" ,  
"2" : "دویست" , 
"3" : "سیصد" ,
"4" : "چهارصد" ,
"5" : "پانصد" , 
"6" : "ششصد" , 
"7" : "هفتصد" , 
"8" : "هشتصد" , 
"9" : "نهصد"
}
prefix =[
    "ریال" ,
    "هزار و" ,
    "میلیون و" ,
    "میلیارد و" ,
]

def toalpha(a):   
    result = []
    if len(a) == 1:
            result.append(unit.get(a))
    if len(a) == 2:
            if a[0] == "1":
                    result.append(tens.get(a[0::]))
            else:
                    result.append(tens.get(a[0]))
                    result.append(unit.get(a[1]))
    if len(a) == 3:
            result.append(hundreds.get(a[0]))
            if a[1] == "1":
                    result.append(tens.get(a[1::]))
            else:
                    result.append(tens.get(a[1]))
                    result.append(unit.get(a[2]))
    for a in range(len(result)-1):
            if result[a] == "":
                    result.pop(a)
    return " و ".join(result)
              
def count(b):
    res = []
    for i in range(ceil(len(b) / 3)):
            if len(b)% 3 > 0:
                    res.append(toalpha(b[0:len(b)% 3:]))
                    b = b[len(b)% 3:]
            else :
                    res.append(toalpha(b[0:3:]))
                    b = b[3:]
    return res
def main(ta):
    total = str(int(ta))
    result = count(total)
    resultreversed = result[::-1]
    final = []
    p = ""
    for i in range(len(resultreversed)):
            final.append(resultreversed[i] + " " + prefix[i])
    for i in reversed(final):
            p += i
    return p

