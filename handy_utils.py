#!/usr/bin/env python3
"""
Collection of Handy Utilities & Dialogs used by RHP-POS.

A smattering of functions & objects used to make
everything run smoothly & correctly.

"""
#-*- coding: utf-8 -*-
#import wxversion
#wxversion.select('2.8')

import wx
import os
import re
import json
import pout
import sys
import string
#import sqlite3
#import pymysql as MySQLdb
import datetime
#import psycopg2
import wx.grid as gridlib
import wx.lib.masked as masked
import printer as PRx
from decimal import Decimal, ROUND_HALF_UP, ROUND_UP, ROUND_05UP
import wx,os,sys,time
import wx.lib.inspection
import numpy
import itertools as it
from contextlib import ContextDecorator
from ObjectListView import ObjectListView, ColumnDefn, OLVEvent
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin
import wx.lib.agw.ultimatelistctrl as ULC
from operator import itemgetter
from button_stuff import ButtonOps
from var_operations import VarOps
#from wx.lib.masked import TimeCtrl
from db_related import TableAware, LookupDB, SQConnect, QueryOps


global debug
debug = False


# class RetailOps(object):
#     """Collection of Retail Operations."""

#     def __init__(self, debug=False):
#         """Almalgamation of all the retail number calculations.

#         Decimal Unit refers to '1.00', '10.00', '0.00', etc.
#         """
        

#     def DoMargin(self, avgcost, calcMargin, unitd):
#         """Calculate Margin (AvgCost * (Decimal(Margin) / 100)."""
#         profit_margin = Decimal(calcMargin) / 100
        
#         newRetail = (Decimal(avgcost) / (profit_margin) * Decimal(unitd))
#         return newRetail


#     def GetMargin(self,avgcost, retail, unitd):
#         """Get Margin from an already calculated Retail.

#         Requires AvgCost, Retail, Decimal Unit i.e. '1.00'. 
#         """    
#         raw = (Decimal(retail) / Decimal(unitd))
#         new = ((Decimal(raw) - Decimal(avgcost)) / Decimal(raw)) * 100
#         return new

#     def MarginUpdate(self, avg_cost, retail, unit):
#         """Re-adjust Margin in margin Column according to avg_cost."""
#         actual_retail = Decimal(retail)/Decimal(unit)
#         gross_profit = Decimal(actual_retail) - Decimal(avg_cost)
#         deci_margin = Decimal(gross_profit) / Decimal(actual_retail)
#         perc_margin = Decimal(deci_margin) * Decimal(100)
#         percentage_margin = RO.DoRound(perc_margin, '1.000')
#         return percentage_margin


#     def RoundNickel(self, x):
#         """Round to the nearest Nickel."""    
#         a = .05
#         b = round(Decimal(x) / Decimal(a))
#         c = Decimal(b) * Decimal(a)
#         return c


#     #def Dollard(self, money):
        
#     def DoRound(self, oldmoney, unitd='1.00', typd='plain'):
#         """Round Sums using different definable schemes."""
#         noPenny, rndScheme = False, '3'
#         if typd == 'tax':
#             (noPenny, rndScheme) = LookupDB('tax_tables').Specific('TAX','tax_name','no_pennies_rounding, RNDscheme')
        
#         roundtype = {'1':'ROUND_DOWN','2':'ROUND_HALF_UP','3':'ROUND_UP'}
#         if rndScheme == 0:
#             rndScheme = 3
#         rnd = str(rndScheme)
        
#         newMoney = Decimal(Decimal(oldmoney).quantize(Decimal(unitd), rounding=roundtype[rnd]))
            
#         return newMoney

#     def DoDiscount(self, retail, discount):
#         """Return New Retail after Applying Discount."""
        
#         newRetail = Decimal(retail) - (Decimal(retail) * (Decimal(discount) / 100))
#         return newRetail

#     def CheckDiscount(self, itemNumber=None, custNum=None, on_discount=None):
#         query = 'SELECT do_not_discount FROM item_detailed2 WHERE upc=(?)'
#         data = (itemNumber,)
#         nodiscount = SQConnect(query, data).ONE()
#         discount = 0
#         dnd = False
        
        
#         if nodiscount is None or nodiscount[0] is True or nodiscount[0] == 1:
            
#             dnd = True

#         if len(custNum) > 0:
#             query = '''SELECT fixed_discount, discount_amt
#                     FROM customer_sales_options
#                     WHERE cust_num=(?)'''
#             data = (custNum,)
#             returnd = SQConnect(query, data ).ONE()
            
#             (fixed_discount, discount_amt) = returnd
#             if returnd is not None:
#                 if returnd[0] is True or returnd[0] == 1:
#                     discount = returnd[1]
                
        
#         discountSingle = wx.FindWindowByName('pos_discounttype_combobox').GetValue()
#         if discountSingle == 'Discount All':
#             discountAll = wx.FindWindowByName('pos_discountpercent_txtctrl').GetCtrl()
#             if discountAll and discountAll > 0:
                
#                 discount = discountAll
    
#         if on_discount > 0:
#             discount = on_discount
        
#         if dnd is True:
#             discount = 0
        
#         return discount


    
#     # def GetDiscountdPrice(self, discount, totalprice):
#     #     if re.match('[0-9]', str(discount), re.I):
#     #         discprice = self.DoDiscount(startret, discount)
#     #     return discprice

#     def LevelDiscount(self, upc, qty, discount, totalprice):
#         qtyd = int(qty)
#         retails = self.RetailSifting(upc)
#         startret = Decimal(retails['standard_price']['price'])*Decimal(qtyd)
#         #pout.v(f'Discount @ LevelDiscount : {discount}')
#         discprice = startret
#         if re.match('[0-9]', str(discount), re.I):
#             discprice = self.DoDiscount(startret, discount)
            
#         levelprice = startret
#         lvl = ''
        
#         if qtyd > 1:
#             for level in retails:
#                 if 'standard' in level:
#                     continue
#                 #pout.v(f'Level : {level}')
#                 #pout.v(f'Retails[{level}] : {retails[level]}')
#                 if retails[level]['price'] > 0:
#                     lastnum = int(retails[level]['unit'])
                    
#                     if qtyd >= lastnum:
#                         levelprice = retails[level]['price']
#                         lvl = level

                    
        
#         RetPrice = (levelprice, self.levelLabel(lvl))                

#         if Decimal(discprice) < Decimal(levelprice):
#             RetPrice = (self.DoRound(discprice), f"{discount}%")

#         if totalprice > Decimal(RetPrice[0]):
#             totalprice = RetPrice[0]
#             disccol = RetPrice[1]

#         return RetPrice 
        

#     def levelLabel(self, label):
#         c = label
#         if 'level' in label:
#             a = re.search('level_(.)_price', label, re.IGNORECASE)
#             b = a.group(1)
            
#             c = b.upper()
#             #print(f'levelLabel :{label}\na : {a}\nb : {b}\nc : {c}')
        
#         return c

#     def Dollars(self, amount):
#         if amount >= 0:
#             return '{:,.2f}'.format(amount)
#         else:
#             return '{:,.2f}'.format(-amount)


#     def StartingMargin(self, name):
#         grid = wx.FindWindowByName('inv_details_cost_grid')
#         current_margin = GridOps(grid.GetName()).GetCell('Margin %',0)
#         if float(current_margin) > 10:
#             StartingMargin_L = current_margin
#             wx.FindWindowByName('details_startingMargin_numctrl').GetCtrl(current_margin)
#         else:
#             StartingMargin_L = '50'
        
#         return StartingMargin_L

#     def RetailSifting(self, upc):
#         sift_list = [(0, 'item_retails', 'standard_unit', 'standard_price'),
#                     (1,'item_retails', 'level_a_unit', 'level_a_price'), 
#                     (2, 'item_retails', 'level_b_unit', 'level_b_price'),
#                     (3, 'item_retails', 'level_c_unit', 'level_c_price'),
#                     (4, 'item_retails', 'level_d_unit', 'level_d_price'),
#                     (5, 'item_retails', 'level_e_unit', 'level_e_price'),
#                     (6, 'item_retails', 'level_f_unit', 'level_f_price'),
#                     (7, 'item_retails', 'level_g_unit', 'level_g_price'),
#                     (8, 'item_retails', 'level_h_unit', 'level_h_price'),
#                     (9, 'item_retails', 'level_i_unit', 'level_i_price'),
#                     (10, 'item_retails', 'compare_unit', 'compare_price'),
#                     (11, 'item_retails', 'on_sale_unit', 'on_sale_price')]
                        
#         sift_dict = {}
#         retail = '1'
#         for row, table, unit_field, price_field in sift_list:
#             query = '''SELECT {}, {}
#                     FROM {}
#                     WHERE upc=(?)'''.format(unit_field, price_field, table)
                        
#             data = (str(upc).upper().strip(),)
#             returnd = SQConnect(query,data).ONE()
            
#             if not returnd:
#                 return None
                
#             unitd, retaild = returnd
#             #print 'unitd : ',unitd
#             #print 'retaild : ',retaild
#             sift_dict[price_field] = {'unit':str(unitd), 'price': retaild}
                           
#         return sift_dict    

#     def GetRetail(upcd, cust_num, retailsd_JSON=None, on_discount=None, debug=False):
#         if retailsd_JSON is None:
#             discountd = None
#             new_retail = '0'
        
#         else:   
#             retailsd = retailsd_JSON
            
#             retail_regular = retailsd['standard_price']['price']
#             if on_discount[1] > 0:
#                 discount = CheckDiscount(upcd, cust_num, on_discount[1])
#             else:
#                 discount = CheckDiscount(upcd, cust_num, on_discount[0])
            
#             if discount > 0:
#                 discountd = str(discount)
#                 new_retail = DiscountIt(retail_regular, discountd)
#             else:
#                 discountd = None
#                 new_retail = retail_regular
                                
        
#         return discountd,new_retail
    
    
#     def GetTaxRate(price):
#         fields = '''min_sale, max_sale, from_amt0, 
#                     tax_rate0, from_amt1, tax_rate1, from_amt2, tax_rate2''' 
        
#         returnd = LookupDB('tax_tables').Specific('TAX','tax_name',fields)
#         (min_sale, max_sale, from_amt0, tax_rate0, from_amt1,
#         tax_rate1, from_amt2, tax_rate2) = returnd 
#         if returnd is None:
#             return
        
#         if Decimal(price) > Decimal(min_sale):
#             if Decimal(price) > Decimal(from_amt0):
#                 taxd = Decimal(tax_rate0)    
                

#             if Decimal(from_amt1) > 0:
#                 if Decimal(price) > Decimal(from_amt1):
#                     taxd = Decimal(tax_rate1)
                    

#             if Decimal(from_amt2) > 0:
#                 if Decimal(price) > Decimal(from_amt2):
#                     taxd = Decimal(tax_rate2)
                    
            
        
            
#         if taxd >= 1:
#             taxd = Decimal(taxd) / 100
                    
        
#         return taxd
    

#     def GetTaxable(upc, taxable, discount_col=''):
        
#         Taxed = True
#         query = 'SELECT tax1,tax2,tax3,tax4,tax_never FROM item_detailed2 WHERE upc=(?)'
#         data = (upc,)
#         returnd = SQConnect(query, data).ONE()
        
        
#         tax1, tax2, tax3, tax4, tax_never = 0,0,0,0,0
        
#         if returnd is not None:
#             (tax1,tax2,tax3,tax4,tax_never) = returnd
            
        
#         tax_list = [(0, tax1),('A',tax2),('B',tax3),('C',tax4)]
        
#         tx_dict = {}
#         for key, value in tax_list:
#             tx_dict[key] = value
        
#         if discount_col == '' or discount_col is None:
#             discount_col = 0
        
#         if tx_dict[discount_col] == 1 or tx_dict is True:
#             Taxed = False
        
#         if taxable is False:
#             Taxed = False
            
#         if tax_never == 1:
#             Taxed = False
        
#         if Taxed is False:
#             pr_tax = 'nTx'
#         else:   
#             pr_tax = 'Tx'
        
#         return Taxed,pr_tax

#     def CheckTaxHoliday(upc):
#         """Check Tax Holiday Worksheet."""
#         query = 'SELECT begin_date, end_date, upc, active FROM tax_holiday'
#         data = ''
#         returnd = SQConnect(query, data).ALL()
#         for begins, ends, upcs, active in returnd:
#             if active == 1:
#                 delta = begins
        
        
    
                

class DictMaker(dict):
    def __init__(self):
        self._dict = {}

    def add(self, key, val):
        self._dict[key] = val

    def get(self):
        return self._dict

# class ItemOps(object):
#     def __init__(self, upc, custNum, debug=False):
        
#         self.upc = upc
#         self.custNum(custNum)

#     def Lookup(self):
#         pass

#     def CheckDiscount(self):
#         pass

#     def CheckSale(self):
#         pass

#     def CheckQty(self, qty):
#         pass

#     def CheckTaxExempt(self):
#         pass

#     def CheckTaxHoliday(self):
#         pass


# class ButtonOps(object):
#     def __init__(self, debug=False):
#         pass    

#     def ButtonWidth_onRow(self, button_cnt, bar_width, num_of_levels=2, minWidth=50, button_gap=3):
#         if button_cnt % 2 != 0:
#             button_cnt += 1
#         lvl_cnt = button_cnt/num_of_levels
#         add_width = (((lvl_cnt*minWidth)+(lvl_cnt*button_gap))-bar_width)/lvl_cnt
#         button_width = minWidth+abs(add_width)
        
#         return int(button_width)

#     def ButtonSized(self, button_list):

#         tup_item_cnt = len(button_list[0])
#         list_cnt = len(button_list)
#         last_size = 0
#         multiplier = 0
        
#         for major in range(list_cnt):
#             for minor in range(tup_item_cnt):
#                 valued = button_list[major][minor]
#                 styled = str(type(valued))
#                 if re.search('(str|unicode)', styled):
#                     types = '(button|text|radiobox|radiobtn|ctrl)'
#                     if not re.search(types, valued):
#                         if len(valued) > last_size:
#                             last_size = len(valued)
#                         if valued.count('\n') > multiplier:
#                             multiplier = valued.count('\n') + 1

#         wsize = last_size * 9
#         hsize = 25 * multiplier

#         return wsize, hsize

#     def ButtonToggle(self, buttonName, state=True):
#         btn = wx.FindWindowByName(buttonName)
#         downColor = (121, 145, 183)
#         upColor = (wx.NullColour) #212, 226, 247
#         if state is not True:
#             btn.SetBackgroundColour(downColor)
#             return True
#         else:
#             btn.SetBackgroundColour(upColor)
#             return False

#     def ButtonCenterText(self, label):
#         labels = label.split('\n')
#         labelNum = len(labels)
        
#         if labelNum > 1:
#             lab1_W = len(labels[0])
#             lab2_W = len(labels[1])
            
            
#             if lab1_W >= 6 and lab1_W < 10:
#                 if lab2_W > 5:
#                     spaces = 2
#                 else:
#                     spaces = 3
                    
#             if lab1_W <=5:
#                 if lab2_W > 5:
#                     spaces = 0
#                 else:    
#                     spaces = 2
            
#             if lab1_W >= 10: 
#                 if lab2_W > 10:
#                     spaces = 0
#                 else:
#                     spaces = 6
                    
#             spaced=''
#             for spc in range(spaces):
#                 spaced += ' '   
                
#             labeld = '{}\n{}{}'.format(labels[0], spaced, labels[1])
#         else:
#             labeld = label     
                    
        
#         return labeld

#     def ListAdjustEven(self, listd):
#         list_cnt = len(listd)
#         entr_cnt = len(listd[0])
        
#         if list_cnt % 2 != 0:
#             value = ('',)
#             for i in range(entr_cnt-1):
#                 value += ('',)
#             #value = ('','','')
#             listd.append(value)
        
#         return listd
                    
#     def ButtonOff(self, names, state=True):
#         typ = str(type(names))
#         print(('typd : ',typ))
#         if re.search('(unicode|str)', typ, re.I):
#             item = wx.FindWindowByName(names)
#             if state is True:
#                 item.Disable()
#             else:
#                 item.Enable()
                
#         if 'list' in typ:
#             for name in names:
#                 print(('button name : ',name))
#                 item = wx.FindWindowByName(name)
#                 if state is True:
#                     item.Disable()
#                 else:
#                     item.Enable()

#     def Icons(self, typd, size=24):
#         """Available Icon Sizes are as follows:
#         128x128, 16x16, 24x24, 36x36, 48x48
#         """
#         sized = f'{size}x{size}'
#         icondir = './icons'
#         logodir = '../logos'
#         a_dict = {'save': f'{icondir}/{sized}/{sized}_Save.png', 
#                  'add': f'{icondir}/{sized}/{sized}_Add.png',
#                  'exit': f'{icondir}/{sized}/{sized}_Exit.png',
#                  'find': f'{icondir}/{sized}/{sized}_Binocular2_Black.png',
#                  'undo': f'{icondir}/{sized}/{sized}_Undo.png',
#                  'delete': f'{icondir}/{sized}/{sized}_Minus.png',
#                  'print': f'{icondir}/{sized}/{sized}_Printer.png',
#                  'empty': f'{icondir}/empty-300x300.png',
#                  'refresh': f'{icondir}/{sized}/{sized}_Refresh.png',
#                  'receiving': f'{icondir}/{sized}/{sized}_Receiving.png',
#                  'pdf': f'{icondir}/{sized}/{sized}_PDF.png',
#                  'logo': f'{logodir}',
#                  'addrmaint': f'{icondir}/{sized}/{sized}_AddrMap_Color.png'}
                 
#         loc = a_dict[typd.lower()]
#         return loc


#     def TextIcons(self, typd, size=24):
#         """Available Icon Sizes are as follows:
#         128x128, 16x16, 24x24, 36x36, 48x48
#         """
#         sized = f'{size}x{size}'
#         fontdir = './fonts'
#         iconfont = 'ttf-font-awesome'
#         exitIcon = '\f52b'
#         #t.SetFont(wx.Font(sized, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Ubuntu")
#         t.SetFont(wx.Font(sized, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'fa-solid-900'))

#         aList = [('save', f'{icondir}/{sized}/{sized}_Save.png'), 
#                  ('add', f'{icondir}/{sized}/{sized}_Add.png'),
#                  ('exit', f'{icondir}/{sized}/{sized}_Exit.png'),
#                  ('find', f'{icondir}/{sized}/{sized}_Binocular2_Black.png'),
#                  ('undo', f'{icondir}/{sized}/{sized}_Undo.png'),
#                  ('delete', f'{icondir}/{sized}/{sized}_Minus.png'),
#                  ('print', f'{icondir}/{sized}/{sized}_Printer.png'),
#                  ('empty', f'{icondir}/empty-300x300.png'),
#                  ('storeAwning',f'{icondir}/Store_awning_sm.png'),
#                  ('refresh', f'{icondir}/{sized}/{sized}_Refresh.png'),
#                  ('receiving', f'{icondir}/{sized}/{sized}_Receiving.png'),
#                  ('pdf', f'{icondir}/{sized}/{sized}_PDF.png'),
#                  ('logo',f'{logodir}')]
                 
#         for icon, loc in aList:
#             if typd.lower() == icon:
#                 return loc


# class CtrlOps(object):
#     def __init__(self, name, debug=False):
#         self.name = name
        

#     def ClearCtrl(self, fillwith=None):
#         name = self.name
#         if re.search('(unicode|str)', str(type(self.name)), re.I):
#             ctrl = []
#             ctrl.append(self.name)
#             name = ctrl
#         for ctrl in name:    
#             item = wx.FindWindowByName(ctrl)
            
#             typd = str(type(item))
            
            
#             if re.search('textctrl', typd, re.I):
#                 item.SetValue('')
#             if re.search('radiobox', typd, re.I):
#                 item.SetSelection(0)
#             if re.search('radiobutton', typd, re.I):
#                 item.SetValue(0)
#             if re.search('combobox', typd, re.I):
#                 #item.Clear()
#                 #blank_list = ['']
#                 #item.SetItems(blank_list)
#                 item.SetSelection(0)
#             if re.search('listbox', typd, re.I):
#                 item.Clear()
#             if re.search('listctrl', typd, re.I):
#                 item.DeleteAllItems()
#             if re.search('(checkbox|numctrl)', typd, re.I):
#                 item.SetValue(0)
#             if re.search('datepickerctrl', typd, re.I):
#                 item.SetValue(wx.DateTime())
#             if re.search('timectrl', typd, re.I):
#                 item.SetValue('12:00am')
#             if re.search('grid', typd, re.I):
#                 item.ClearGrid()
#                 cols = item.GetNumberCols()
#                 rows = item.GetNumberRows()
#                 for xx in range(rows):
#                     for yy in range(cols):
#                         item.SetReadOnly(xx,yy,False)
#                         if fillwith is not None:
#                             item.SetCellValue(xx,yy,str(fillwith))

#     def GetCtrl(self):
#         name = self.name
#         item = wx.FindWindowByName(name)
#         typd = str(type(item))
        
#         value = None
#         if re.search('filepickerctrl', typd, re.I):
#             return item.GetPath()
        
#         if re.search('combobox', typd, re.I):
#             return item.GetValue()
        
#         if re.search('(txtctrl|textctrl)', typd, re.I):
#             if re.search('masked', typd, re.I):
#                 return item.GetPlainValue()
#             else:
#                 return item.GetValue()
            
#         if re.search('statictext', typd, re.I):
#             return item.GetLabel()
        
#         if re.search('checkbox', typd, re.I):
#             value = item.GetValue()
#             if value is True:
#                 return 1
#             else:
#                 return 0
        
#         if re.search('timectrl', typd, re.I):
#             value = item.GetValue()
#             if value == '':
#                 return 0

#         if re.search('numctrl', typd, re.I):
#             value = item.GetValue()
#             if value == '' or value is None:
#                 return 0

#         if re.search('radiobox', typd, re.I):
#             return item.GetSelection()

#         if re.search('radiobutton', typd, re.I):
#             value = item.GetValue()
#             if value is True:
#                 return 1
#             if value is False:
#                 return 0

#         if re.search('listctrl', typd, re.I):
#             rows = item.GetItemCount()
#             cols = item.GetColumnCount()
#             listctrl_dict = {}
            
#             for row in range(rows):
#                 tup = ()
#                 for col in range(cols):
#                     typed = item.GetItem(row, col).GetText().upper()
#                     tup = tup + (typed,)
#                 listctrl_dict[row] = tup
                
#             return json.dumps(listctrl_dict)
        
#         if re.search('datepickerctrl', typd, re.I):
#             a = item.GetValue().FormatISODate()
#             print(f'Date Get : {a}')
#             return item.GetValue().FormatISODate()
        
#         if re.search('datectrl', typd, re.I):
#             return item.GetValue().FormatISODate()
            
#         if re.search('listbox', typd, re.I):
#             strings = item.GetStrings()
            
#             if len(strings) > 0:
#                 return json.dumps(strings)
            
            
        
#         if re.search('grid', typd, re.I):
#             grid_dict = {}
#             for xx in range(item.GetNumberRows()):
#                 LabelKey = item.GetRowLabelValue(xx).replace(" ", "_").lower()
#                 valued = []
#                 for yy in range(item.GetNumberCols()):
#                     #header = item.GetColLabelValue(yy)
#                     value = item.GetCellValue(xx, yy)
#                     valued.append(value)

#                 grid_dict[LabelKey] = (valued)
#             value = json.dumps(grid_dict)
        
        
#         valtype = str(type(value))
#         if re.search('(str|unicode)', valtype, re.I):
#             return value.strip()

#         return value

#     def SetCtrl(self, value):
#         name = self.name
        
#         item = wx.FindWindowByName(self.name)
#         typd = str(type(item))
#         valtype = str(type(value))
#         if 'tuple' in valtype:
#             value = VarOps().DeTupler(value)
#         #print "{} : {}\n{} : {}".format(name,typd,value,valtype)
#         self.ClearCtrl()
        
#         if 'str' in valtype:
#             value = value.strip()
#         if 'glpost' in name:
            
#             if not value:
#                 value = '145-010'
#             if not re.search('[0-9]+', value):
#                 value = '000000'

        
#         if re.search('statictext', typd, re.I):
#             try:
#                 item.SetLabel(str(value))
#             except:
#                 print(f"Value : {str(value)}")
#         elif re.search('combobox', typd, re.I):
#             if 'list' in valtype:
#                 try:
                    
#                     item.SetItems(value)
                    
#                 except:
#                     print(f"value : {value}")

#             if re.search('(str|unicode)', valtype, re.I):
#                 if not value:
#                     value = ''
#                 if value == 0:
#                     value = '0'
#                 try:
#                     item.SetValue(str(value))
#                 except:
#                     print(f'value : {value}')

#         elif re.search('textctrl', typd, re.I):
#             if not value:
#                 value = ''
#             try:
#                 item.SetValue(str(value))
#             except:
#                 print(f'value : {value}')

#         elif re.search('timectrl', typd, re.I):
            
#             if value is None or value == 0 or value == '0':
#                 value = '00:00:00'
            
#             if not re.search('[ap]m', str(value), re.I):
#                 d = datetime.datetime.strptime(str(value), "%H:%M:%S")
#                 value = d.strftime("%I:%M %p")

#             if not value or value == '':
                
#                 value = '12:00:00 AM'
#             try:
#                 item.SetValue(value)
#             except:
#                 print(f'value : {value}')

            

#         elif re.search('datepickerctrl', typd, re.I):
#             year, month, day = 0,0,0
            
#             if value == '' or not re.search('[0-9]', str(value)):
                
#                 value = wx.DateTime()
#             else:
#                 raw = str(value)
                
#                 if re.search('-', raw):
#                     year, month, day = raw.split('-')
#                 if re.search('/', raw):
#                     year, month, day = raw.split('/')
#                 dt = wx.DateTime()
#                 dtd = '{}/{}/{}'.format(day,month,year)
#                 dt.ParseFormat(dtd, '%d/%m/%Y')
                
                
#                 #Debugger("Y-{0} / M-{1} / D-{2}".format(year, month, day))
#                 #datd = wx.DateTimeFromDMY(int(day), int(month), int(year))
#                 value = dt

            
#             try:
#                 item.SetValue(value)
#             except:
#                 print(f'value : {value}')

#         elif re.search('checkbox', typd, re.I):
            
#             if value is None or value == '':
#                 value = 0
            
#             if value is True:
#                 value = 1
            
#             elif value is False:
#                 value = 0    
            
#             try:
#                 item.SetValue(value)
#             except:
#                 print(f'value : {value}')
#         elif re.search('filepickerctrl',typd, re.I):
#             if not value:
#                 value = ''
#             try:
#                 item.SetPath(value)    
#             except:
#                 print(f'value : {value}')
                
#         elif re.search('numctrl', typd, re.I):
#             if not value:
#                 value = 0
#             try:
#                 item.SetValue(float(value))
#             except:
#                 print(f'value : {value}')

#         elif re.search('listbox', typd, re.I):
#             if value:
#                 valued = value
#             else:
#                 valued = ''
#             if not valued:
#                 pass
#             else:
#                 try:
#                     item.InsertItems(valued, 0)
#                 except:
#                     print(f'Value : {valued}')

#         elif re.search('listctrl', typd, re.I):
#             if not value or value is None:
#                 pass
#             else:
#                 value = value

#             rows = len(value)
#             hasRows = item.GetItemCount()
#             cols = item.GetColumnCount()

#             dd = """** ListCtrl Counts\n  Current Item : {0}\n  New Item : {1}
#             Column : {2}\n  Value : {3}""".format(hasRows, rows, cols, value)
            
#             item.DeleteAllItems()

#             for row in range(hasRows, rows):
                
#                 for col in range(cols):
                    
#                     if col == 0:
#                         new_row = str(row)
                        
                        
#                         item.InsertItem(row, value[new_row][col])

#                     try:
                        
#                         if value[new_row]:
#                             pass    
#                     except:
                        
#                         break
#                     else:
                        
#                         item.SetItem(row, col, value[new_row][col])

#         elif re.search('radiobox', typd, re.I):
#             if not value:
#                 value = 0
#             try:
#                 item.SetSelection(int(value))
#             except:
#                 print(f'value : {value}')

#         elif re.search('radiobutton', typd, re.I):
#             if not value:
#                 value = False
#             try:
#                 item.SetValue(value)
#             except:
#                 print(f'value : {value}')

#         elif re.search('grid', typd, re.I):
#             grid = wx.FindWindowByName(name)
#             if value:
#                 grid_dict = value

#                 for xx in range(grid.GetNumberRows()):
#                     LabelKey = grid.GetRowLabelValue(xx).replace(" ", "_").lower()
#                     for yy in range(grid.GetNumberCols()):
#                         new_value = grid_dict[LabelKey][yy]
#                         grid.SetCellValue(xx, yy, new_value)

#     def EnableCtrl(self, enable=True):
#         name = self.name
        
#         nametypd = str(type(name))
#         if 'list' in nametypd:
#             for item in name:
#                 ctrl = wx.FindWindowByName(item)
#                 ctrltypd = str(type(ctrl))
                
#                 if re.search('(textctrl|numctrl)', ctrltypd, re.I):
#                     if enable is False:
#                         ctrl.SetEditable(editable=False)
#                         ctrl.Disable()
                        
#                     else:
#                         ctrl.SetEditable(editable=True)
#                         ctrl.Enable()
                    
#                 else:
#                     if enable is False:
#                         ctrl.Disable()
                        
#                     else:
#                         ctrl.Enable()

#         elif 'str' in nametypd:
#             ctrl = wx.FindWindowByName(name)
#             ctrltypd = str(type(ctrl))
            
#             if re.search('(textctrl|numctrl)', ctrltypd, re.I):
#                 if enable is False:
#                     ctrl.SetEditable(editable=False)
#                     ctrl.Disable()
                    
#                 else:
#                     ctrl.SetEditable(editable=True)
#                     ctrl.Enable()
#             else:
#                 if enable is False:
#                     ctrl.Disable()
                    
#                 else:
#                     ctrl.Enable()

#     def ReturndSet(self, returnd, retnum=0):
#         name = self.name
#         if returnd is not None:
#                 if 'tuple' in str(type(returnd)):
#                     ret = str(returnd[retnum])
#                 else:
#                     ret = str(returnd)

#                 setctrl = self.SetCtrl(ret)



class AccountOps(object):
    def __init__(self, debug=False):
        pass

    def AcctNumCheck(self, tableName, fieldName, prop_num, debug=False):
        cnt_returnd = QueryOps().QueryCheck(tableName, fieldName, prop_num)
        return cnt_returnd
            
    def AcctNumAuto(self, tableName, fieldName, fill0s=9, prefix='', debug=False):
        print(f'Account Num Auto --__')
        query = 'SELECT {0} FROM {1}'.format(fieldName, tableName)
        data = ''
        returnd = SQConnect(query, data).ALL()
        print(f'Query : {query} ; Returnd : {returnd}')
        acct_num_exist = True
        cnt = 0
        if returnd:
            cnt = len(returnd)
        
        print(f"AcctNumAuto Cnt : {cnt}")
        while acct_num_exist is True:
            account_num = '{}{}'.format(prefix, str(cnt).zfill(fill0s))
            pout.v(f'Account Num : {account_num}')
            returnd = LookupDB(tableName).Count(fieldName)
            if not account_num in returnd:
                pout.v(f'Account Num Exist : {acct_num_exist}')
                if returnd[0] == 0:
                    acct_num_exist = False
                    break
            cnt += 1

        return account_num

    def TransNumAuto(self, fill0s=7, addOne=False, debug=False):
        if addOne is False:
            query = 'SELECT trans_num FROM transaction_control WHERE abuser="rhp";'
            data = ''
            returnd = SQConnect(query, data).ONE()
        
            if returnd[0]:
                transNum = str(returnd[0]).zfill(fill0s)
                return transNum
        
        if addOne is True:
            query = 'UPDATE transaction_control SET trans_num=trans_num+1 WHERE abuser="rhp";'
            data = ''
            returnd = SQConnect(query, data).ONE()

class Debugger(object):
    def __init__(self, debug=False, h1=False):
        self.debug = debug
        

    def Show(self, alert, h1=False):
        if h1 is False:
            self.Normal(alert)
        else:
            self.BeVerbose(alert)


    def Normal(self,alert):
        if self.debug is True:
            print(alert)

    def BeVerbose(self, alert):
        if self.debug is True:
            boxcenter = "\t\t\t\t\t\t"
            head = str(alert)
            headlen = len(alert) + 2
            boxtop = "#" * headlen
            print(("""\n\n{2} {0}\n{2}# {1} #\n{2} {0}\n\n""".format(boxtop, head, boxcenter)))


# def ChangeType(instr, typd):
#     rd = str(type(instr))
#     final = instr
#     if not re.search(rd, typd, re.I):
#         if re.match(typd, 'decimal', re.I):
#             final = Decimal(instr)
#         if re.match(typd, 'string', re.I):
#             final = str(instr)
#         if re.match(typd, 'float', re.I):
#             final = float(instr)
#         if re.match(typd, 'integer', re.I):
#             final = int(instr)
        
#     return final
    

# def checkNone(rtd):
#     if rtd == 'None':
#         rtd = None
    
#     return(rtd)
    
class RecordOps(object):
    def __init__(self, tableName, debug=False):
        self.tableName = tableName
        

    def UpdateRecordDate(self, fieldName, ctrlFieldName, ctrlValue,
                        namedCtrl=None):
        dated = datetime.date.today()
        query = 'UPDATE {0} SET {1}=(?) WHERE {2}=(?)'.format(self.tableName,
                                                            fieldName,
                                                            ctrlFieldName)
        data = (dated, ctrlValue)
        SQConnect(query, data).ONE()
        if namedCtrl is not None:
            wx.FindWindowByName(namedCtrl).SetCtrl(dated)

    def DeleteEntryRecord(self, controlField, controlNumber):
        controlNumber = controlNumber.strip()
        ty = str(type(self.tableName))
        if 'list' in ty:
            for table in self.tableName:
                query = "DELETE FROM {0} WHERE {1}=(?)".format(table, controlField)
                data = (controlNumber,)
                returnd = SQConnect(query, data).ONE()

        if 'str' in ty:
                query = "DELETE FROM {0} WHERE {1}=(?)".format(self.tableName, controlField)
                data = (controlNumber,)
                returnd = SQConnect(query, data).ONE()

            
        
class LoadSaveList(object):
    def __init__(self):
        self.listd = []
    
    def Add(self, item):
        self.listd.append(item)
    
    def Show(self):
        pout.v(self.listd)

    def Get(self):
        return self.listd



# class VarOps(object):
#     def __init__(self, debug=False):
#         pass    

#     def DeTupler(self, value):
#         typd = str(type(value))
#         if value:
#             while re.search('(tuple|list)', str(type(value)), re.I):
#                 value = value[0]

#         return value

#     def is_json(self, myjson):
#         try:
#             json_object = json.loads(myjson)
#         except (TypeError, ValueError) as e:
#             #print(f'JSON Error : {e}')
#             return False
#         return True

#     def CheckJson(self, vari):
#         b = self.CheckNone(vari)
#         if b is None:
#             return None
#         #print(f'Before CHECKJSON : {vari[0]}')
#         a = self.is_json(vari[0])
#         #print(f'AFTER CHeckJSON : {a}')
#         if a is True:
#             a = json.loads(vari[0])
#         else:
#             a = vari
#         return a
    
#     def DoJson(self, vari):
#         a = vari
#         ta = self.GetTyped(a)
#         if re.search('(list|tuple|dict)', ta, re.I):
#             a = json.dumps(vari)
#         return a

#     def GetTyped(self, item, debug=False):
#         return str(type(item))
        
#     def StrList(self, listd):
#         a = listd
        
#         if listd is not None:
#             a = []
#             for i in listd: 
#                 a.append(str(i))
        
#         return a

#     def CheckNone(self, val, debug=False):
#         a = str(type(val))
#         b = VarOps().DeTupler(val)
#         if b is None:
#             return None
       
#         obret = val
#         a = str(type(val))
#         if 'tuple' in a:
#             if len(val) == 0:
#                 obret = None
#             else:
#                 obret = val[0]
    
#         if 'None' in a:
#             obret = None

#         return obret


#     def ChangeType(self, instr, typd):
#         rd = str(type(instr))
#         final = instr
#         if not re.search(rd, typd, re.I):
#             if re.match(typd, 'decimal', re.I):
#                 final = Decimal(instr)
#             if re.match(typd, 'string', re.I):
#                 final = str(instr)
#             if re.match(typd, 'float', re.I):
#                 final = float(instr)
#             if re.match(typd, 'integer', re.I):
#                 final = int(instr)
            
#         return final


    #def GetJson(self,jsond):




#class ListCtrl_Ops(object):
#    def __init__(self, lcname, debug=False):
#        
#        pass


class ListBox_Ops(object):
    def __init__(self, listboxname, debug=False):
        self.listbox = wx.FindWindowByName(listboxname)
        
    

    def ListBoxClearSpaces(self):
        
        spaces_exist = self.listbox.FindString('')
        cnt = 0
        
        listed = []
        for idx in range(self.listbox.GetCount()):
            if re.search('[A-Z0-9]+', self.listbox.GetString(idx)):
                listed.append(self.listbox.GetString(idx))
        self.listbox.Clear()
        newList = self.UniqueList(seq=listed)
        pout.v(f'newList : {newList}')
        try:
            self.listbox.InsertItems(newList, 0)
        except:
            print('No List Found')

        
    def UniqueList(self, seq, idfun=None):
    # order preserving
        if idfun is None:
            def idfun(x):
                return x
        seen = {}
        result = []
        for item in seq:
            marker = idfun(item)
            # in old Python versions:
            # if seen.has_key(marker)
            # but in new ones:
            if marker in seen:
                continue
            seen[marker] = 1
            result.append(item)
        return result


    # def MaskData(self, query, data, debug=False):
    #     if data is not None or data != '' or len(data) != 0:
    #         new_data = []
    #         fromquery = []
    #         if re.search('SELECT', query, re.I):
                
                
    #             if re.search('LIKE', query, re.I):
                    
                    
    #                 if re.search('(or|and)', query, re.I):
                        
                        
    #                     fromquery = re.split('(or|and)', query, flags=re.IGNORECASE)
    #                 else:
    #                     fromquery.append(query)
                        
    #                 idx = 0
    #                 for item in fromquery:
    #                     dat = ''
                        
    #                     if re.search('(\?|%s)', item):
                            
    #                         if re.search('LIKE',item, re.I):
    #                             if len(data) != 0:
                                    
    #                                 dat = '%{}%'.format(data[idx])
                                
    #                         else:
    #                             dat = '{}'.format(data[idx])
                            
    #                         new_data.append(dat)
        
    #                         idx += 1
    #             else:
    #                 new_data = data
    #         else:
    #             new_data = data
            
            
            
    #         typd = str(type(new_data))
            
    #         if 'list' in typd:
            
    #             new_data = tuple(new_data)
                
    #         else:
    #             pass    
            
    #         if len(data) == 0:
    #             new_data = ''
                
            
    #         return new_data

# def CreditCheck(custNum=None, credit=False):
#     print(('CheckCredit : {} \ {}'.format(custNum, credit)))
#     if custNum is not None:
#         query = 'SELECT freeze_charges FROM customer_accts_receivable WHERE cust_num=(?)'
#         data = [custNum,]
#         returnd = SQConnect(query,data).ONE()
    
#         print(('check Credit returnd : ',returnd))
    
#         if returnd[0] is 1:
#             credit = True
    
#     return credit
    
    
# def CheckEntryExist(controlfield, ItemNumberd, table_list, debug=False):
#     for table in table_list:
#         
#         queryWhere = "{0}".format(controlfield)
#         queryData = (ItemNumberd,)
#         countreturn = QueryOps().QueryCheck(table, queryWhere, queryData)
#         
#         added = False
#         if countreturn == 0:
#             added = True
#             
#             query = "INSERT INTO {0} ({1}) VALUES (?)".format(table,
#                                                               controlfield)
#             
#             data = (ItemNumberd,)
#             SQConnect(query, data).ONE()
#         else:
#             

#     return added


# def DeleteEntryRecord(controlField, controlNumber, table_list):
#     controlNumber = controlNumber.strip()
#     for table in table_list:
#         query = "DELETE FROM {0} WHERE {1}=(?)".format(table, controlField)
#         
#         data = (controlNumber,)
#         returnd = SQConnect(query, data).ONE()

#     



    


# def DisplayItemsinGrid(headers, itemList, gridname):
#     
#     if itemList:
#         grid = wx.FindWindowByName(gridname)
#         grid.ClearGrid()
#         yy = 0
#         for xx in range(len(itemList)):
#             
#             for yy in range(grid.GetNumberCols()):
#                 
#                 grid_header = grid.GetColLabelValue(yy)
#                 
#                 if re.search(headers[yy], grid_header, re.I):
#                     if 'price' in grid_header:
#                         grid.SetCellValue(xx, yy,
#                                           itemList['standard_price'][1])
#                     else:
#                         grid.SetCellValue(xx, yy, itemList[xx][yy])
#                     
#                          item Value : {1}""".format(headers[yy],
#                                                     itemList[xx][yy]))


class TextOps(object):
    def __init__(self):
        pass    

    def Joind(*args):
        full=''
        for item in args:
            if item is None:
                item = ''
            full += item
        
        return full
                
        
    def AllinaRow(self, num=None, cardinal=None, name=None, str_type=None, unit=None):
        rowd = ''
        print(f'unit : {unit}')
        setup = [num, cardinal, name, str_type]
        for item in setup:
            if item is not None and len(item) > 0:
                print(f'Item : \'{item}\'')
                rowd += '{} '.format(item.strip())

        if unit is not None and len(unit) > 0:
            rowd += 'UNIT {} '.format(unit)

        return rowd




# def CheckDiscount(itemNumber=None, custNum=None, on_discount=None, debug=False):
#     query = 'SELECT do_not_discount FROM item_detailed2 WHERE upc=(?)'
#     data = (itemNumber,)
#     nodiscount = SQConnect(query, data).ONE()
#     discount = 0
#     dnd = False
#     
#     
#     if nodiscount is None or nodiscount[0] is True or nodiscount[0] == 1:
#         
#         dnd = True

#     if len(custNum) > 0:
#         query = '''SELECT fixed_discount, discount_amt
#                    FROM customer_sales_options
#                    WHERE cust_num=(?)'''
#         data = (custNum,)
#         returnd = SQConnect(query, data ).ONE()
#         
#         (fixed_discount, discount_amt) = returnd
#         if returnd is not None:
#             if returnd[0] is True or returnd[0] == 1:
#                 discount = returnd[1]
            
    
#     discountSingle = wx.FindWindowByName('pos_discounttype_combobox').GetValue()
#     if discountSingle == 'Discount All':
#         discountAll = wx.FindWindowByName('pos_discountpercent_txtctrl').GetCtrl()
#         if discountAll and discountAll > 0:
#             
#             discount = discountAll
   
#     if on_discount > 0:
#         discount = on_discount
    
#     if dnd is True:
#         discount = 0
    
#     return discount
                  

# def FindEmptyRow(name):
#     grid = wx.FindWindowByName(name)
#     rows = grid.GetNumberRows()
    
#     for xx in range(rows):
#         cell = grid.GetCellValue(xx, 0)
#         if cell == '' or cell is None:
#             return xx    
        

# def OnNumbersOnly(event):
#         """
#         check for numeric entry accepted result is in self.value
#         """
#         
#         valued = event.GetEventObject()
#         raw_value = valued.GetValue().strip()
#         if raw_value == '' or raw_value == None:
#             raw_value = '0'
#         named = valued.GetName()
#         edit_txtctrl = wx.FindWindowByName(named)
#         # numeric check
#         if all(x in '0123456789.+-/' for x in raw_value):
#             # convert to float and limit to 2 decimals
#             value = int(raw_value)
#             edit_txtctrl.ChangeValue(str(value))
#         else:
#             edit_txtctrl.ChangeValue("")
#             edit_txtctrl.SetToolTip(wx.ToolTip("NUMBERS ONLY!!!"))



# def DB_with_Splash(query, data, typed):
#     """ Database Lookup With Splash """
#     if typed.lower() == 'all':
#         returnd = SQConnect(query, data).ALL()
#     if typed.lower() == 'one':
#         returnd = SQConnect(query, data).ONE()
#     splash = wx.FindWindowByName('splash_loading')
#     wx.CallAfter(splash.Destroy())

#     return returnd


class MiscOps(object):
    def __init__(self, debug=False):
        pass    

    def timeStages(self, label, nowd):
        pass

    def StrNone(self, vari):
        if vari is None:
            a = ''
        else:
            a = vari
        
        return a
        
    

    def AddAll(self, tuple_of_names, setName):
        
        fullSet = ''
        if 'tuple' in str(type(tuple_of_names)):
            for name in tuple_of_names:
                ctrl = wx.FindWindowByName(name).GetCtrl()
                
                if ctrl:
                    fullSet += ctrl + ' '
                    
            
            wx.FindWindowByName(setName).SetCtrl(fullSet)

    def NumbersOnly(self, value):
        raw_value = value.strip()
        if raw_value == '' or raw_value == None:
            raw_value = '0'
        #    named = valued.GetName()
        #    edit_txtctrl = wx.FindWindowByName(named)
            # numeric check
        if all(x in '0123456789.+-/' for x in raw_value):
        # convert to float and limit to 2 decimals
            value=int(raw_value)
            return value
        return None    

    def Scrub(self, value, debug=False):
        """
            Scrub non-alphanumeric
        """
        strip_regex = '[\[\]\(\)\/\:\;\!\@\#\$\%\^\&\*\=\+-]'
        if re.search(strip_regex, value):
            
            sys.exit(0)

        return value


    def FindSQLFile(self, tableName, debug=False):
        sql_file = './db/SUPPORT.sql'
        prefix = './db/'
        query = "SELECT sql_file FROM tableSupport WHERE table_names=(?)"
        data = (tableName,)
        returnd = SQConnect(query, data, sql_file).ONE()
        
        filed = prefix + returnd[0]
        if os.path.isfile(filed):
            return filed
        else:
            
            print(('--- table Name : {0} ---'.format(tableName)))

    def ShowAddress(self, returnd):
        (addr0,addr2,addr3,city,state,zipcode) = returnd
        addrShow = ''
        for addrItem in [addr0, addr2, addr3]:
            if addrItem:
                addrShow += '{0} \n'.format(addrItem)
            
        if city and state and zipcode:
            addrShow +='{0}, {1}  {2}\n'.format(city, state, zipcode)
            
        return addrShow

    def ToggleState(self, name, statuses, debug=False):
        current = wx.FindWindowByName(name).GetCtrl()
        if len(current) == 0:
            current = statuses[0]
        idx = statuses.index(current)
        cnt = len(statuses)
        
        next = idx + 1
        if next > cnt-1:
            next = 0
        
        wx.FindWindowByName(name).GetCtrl( statuses[next])
        return statuses[next]

    def WHSup(self, app=None, widget=None, font=None, cell=None):
        '''Check Screen Size return width & height.
        
        Stake out small & mid-size screen accomodated app sizes.'''
        s_w, s_h = wx.GetDisplaySize()
        percSize = .50
        # s_w = 1028
        # s_h = 768
        if cell is not None:
            new_w = int(cell*percSize)
            new_h = None
            if s_w > 1028:
                new_w = cell
                new_h = None

        if font is not None:
            new_w = font-2
            new_h = None
            if s_w > 1028:
                new_w = font
                new_h = None

        if app is not None:
            new_w = 875 
            new_h = 653
            if s_w > 1028:
                new_w = 1225
            if s_h > 768:
                new_h = 850

        if widget is not None:
            w_w, w_h = widget
            new_w = int(w_w*percSize)
            if w_h == -1:
                new_h = -1
            else:
                new_h = int(w_h*percSize)

            if s_w > 1028:
                new_w = w_w
            if s_h > 768:
                new_h = w_h
            
        return (new_w, new_h)
        


# class QueryOps(object):
#     def __init__(self, debug=False):
#         pass    

#     def GetQuery(self, fields, tableName, whereField, whereValue):
#         query = '''SELECT {}
#                    FROM {}
#                    WHERE {}=(?)'''.format(fields, tableName, whereField)
#         data = [whereValue]
#         returnd = SQConnect(query, data).ONE()
#         return returnd

#     def QueryCheck(self, fromTable, queryWhere=None, queryData=None, debug=False):
#         if queryWhere == '' or queryWhere is None:
            
#             query = 'SELECT count(*) FROM {0}'.format(fromTable)
#             data = ''
            
#         elif not re.search('(=|LIKE)', queryWhere) and queryWhere.count('?') == 0:
#             query = '''SELECT count(*)
#                        FROM {0}
#                        WHERE {1}=(?)'''.format(fromTable, queryWhere)
#             data = queryData
#         else:
            
#             query = '''SELECT count(*)
#                     FROM {0}
#                     WHERE {1}'''.format(fromTable, queryWhere)
#             data = queryData
        
#         VarOps().GetTyped(fromTable)
#         returnd = SQConnect(query, data).ONE()
        
#         if re.search('(list|tuple)', str(type(returnd)), re.I):
#             returnd = VarOps().DeTupler(returnd)    
        
#         return returnd

#     def ANDSearch(self, whatField, items):

#         cnt = items.count(' ')
#         text = ''

#         if cnt > 0:
#             sp1 = items.split()
#             if 'list' in str(type(whatField)):
#                 xx = 0
#                 longList = len(whatField) - 1
#                 for field in whatField:
#                     if xx > 0:
#                         text += ' OR '

#                     for i in range(len(sp1)):
#                         text += "{0} LIKE '%{1}%'".format(field, sp1[i])
#                         if i < len(sp1) - 1:
#                             text += ' AND '
#                     xx += 1
#             else:
#                 for i in range(len(sp1)):
#                     text += "{0} LIKE '%{1}%'".format(whatField, sp1[i])
#                     if i < len(sp1) - 1:
#                         text += ' AND '

#         else:
#             if 'list' in str(type(whatField)):
#                 xx = 0
#                 for field in whatField:
#                     if xx > 0:
#                         text += ' OR '

#                     text += "{0} LIKE '%{1}%'".format(field, items)
#                     xx += 1
#             else:
#                 text = "{0} LIKE '%{1}%'".format(whatField, items)
#         print(("And Search Text : ",text))
#         return text

#     def CheckEntryExist(self, controlfield, ItemNumberd, table_list, debug=False):
#         for table in table_list:
#             queryWhere = "{0}".format(controlfield)
#             queryData = (ItemNumberd,)
#             countreturn = QueryOps().QueryCheck(table, queryWhere, queryData)
            
#             added = False
#             if countreturn == 0:
#                 added = True
                
#                 query = "INSERT INTO {0} ({1}) VALUES (?)".format(table,
#                                                                 controlfield)
                
#                 data = (ItemNumberd,)
#                 SQConnect(query, data).ONE()
#             else:
#                 pass      

#         return added



#     def Commaize(self, list_of_tuples, typd='names'):
#         idx = 0
#         fieldSet = ''
#         dataSet = []
        
#         print(('CommaIze : {} : {}'.format(list_of_tuples, typd)))
#         for name,table,field in list_of_tuples:
#             if typd == 'names':
#                 value = wx.FindWindowByName(name).GetCtrl()
#             if typd == 'vari':  
#                 value = name
#             if value is None or value == '':
#                 value = None #continue
#             if idx > 0:
#                 fieldSet += ', '
                
#             fieldSet += '{}=(?)'.format(field)
#             dataSet.append(value)
                
#             idx += 1
#             table = table
                
#         # pout.v('Field Set : ',fieldSet)
#         # pout.v('data Set : ',dataSet)
#         # pout.v('table : ',table)
#         return fieldSet, dataSet, table

#     def CreditCheck(self, custNum=None, credit=False):
#         print(('CheckCredit : {} \ {}'.format(custNum, credit)))
#         if custNum is not None:
#             query = 'SELECT freeze_charges FROM customer_accts_receivable WHERE cust_num=(?)'
#             data = [custNum,]
#             returnd = SQConnect(query,data).ONE()
        
#             #print(('check Credit returnd : ',returnd))
        
#             if returnd[0] == 1:
#                 credit = True
        
#         return credit

#     def CustPenaltyCheck(self, custNum):
#         query = 'SELECT last_avail_credit FROM customer_penalty_info WHERE cust_num=(?)'
#         data = [custNum,]
#         returnd = SQConnect(query, data).ONE()
#         limit = 0
#         if returnd is not None and returnd > 0:
#             limit = returnd[0]
            
        
#         return limit
            
#     def CheckCredit(self, custNum):
#         query = 'SELECT credit_limit FROM customer_accts_receivable WHERE cust_num=(?)'
#         data = [custNum,]
#         returnd = SQConnect(query,data).ONE()
#         climit = 0
#         if returnd[0] is not None and returnd[0] > 0:
#             climit = returnd[0]
        
#         penalty_limit = CustPenaltyCheck(custNum)
        
#         if penalty_limit is not None and penalty_limit > 0:
#             climit = penalty_limit
        
#         return climit    


#     def DisplayLookupItemsinGrid(self, queryWhere, queryData, queryTable, debug=False):
#             fields = 'upc,description,retails,quantity_on_hand'
            
#             if not 'item_detailed' in queryTable:
                
#                 returnd = []
#                 query = '''SELECT upc
#                         FROM {0}
#                         WHERE {1}'''.format(queryTable, queryWhere)

#                 data = queryData
#                 returnd1 = SQConnect(query, data).ALL()
                
#                 for upcd in returnd1:
#                     query = '''SELECT {0}
#                             FROM {1}
#                             WHERE upc=(?)'''.format(fields, 'item_detailed')
#                     data = (upcd,)
#                     returnd2 = SQConnect(query, data).ALL()

#                     returnd.append(returnd2)
                    
#             else:
#                 query = '''SELECT {0}
#                         FROM {1}
#                         WHERE {2}'''.format(fields, queryTable, queryWhere)
#                 data = queryData
#                 returnd = SQConnect(query, data).ALL()

#             if len(returnd) > 0:
#                 grid = wx.FindWindowByName('itemLookup_display_grid')
#                 ClearCtrl(grid.GetName())
#                 AlterGrid(grid.GetName(), returnd)

                
#                 xx = 0
                
#                 for upc, description, retails, qoh in returnd:
#                     for yy in range(grid.GetNumberCols()):
#                         header = grid.GetColLabelValue(yy)
                        
#                         if 'Item Number' in header:
#                             grid.SetCellValue(xx, yy, str(upc))
#                         if 'Item Description' in header:
#                             grid.SetCellValue(xx, yy, str(description))
#                         if 'Price' in header:
#                             try:
#                                 retail_now = retails
#                                 retailPrice = retail_now['standard_price']['price']
                             
#                                 moneyd = RoundIt(retailPrice, '1.00')
                                
#                                 grid.SetCellValue(xx, yy, str(moneyd))
#                             except:
#                                 grid.SetCellValue(xx, yy, '')
#                         if 'OnHand' in header:
#                             grid.SetCellValue(xx, yy, str(qoh))

#                     xx += 1

#                 GridOps(grid.GetName()).GridAlternateColor(len(returnd))
#                 grid.Refresh()


#     def GetItemLine(self, gridname,row):
#         getList = ['Item Number','Description','Price','Quantity','Total','Disc','Tx']
#         got = []
#         for item in getList:
#             x = GridOps(gridname).GetCell(item, row)
#             got.append(x)
        
#         return got

# def RetailSifting(upc):
#     sift_list = [(0, 'item_retails', 'standard_unit', 'standard_price'),
#                  (1,'item_retails', 'level_a_unit', 'level_a_price'), 
#                  (2, 'item_retails', 'level_b_unit', 'level_b_price'),
#                  (3, 'item_retails', 'level_c_unit', 'level_c_price'),
#                  (4, 'item_retails', 'level_d_unit', 'level_d_price'),
#                  (5, 'item_retails', 'level_e_unit', 'level_e_price'),
#                  (6, 'item_retails', 'level_f_unit', 'level_f_price'),
#                  (7, 'item_retails', 'level_g_unit', 'level_g_price'),
#                  (8, 'item_retails', 'level_h_unit', 'level_h_price'),
#                  (9, 'item_retails', 'level_i_unit', 'level_i_price'),
#                  (10, 'item_retails', 'compare_unit', 'compare_price'),
#                  (11, 'item_retails', 'on_sale_unit', 'on_sale_price')]
                     
#     sift_dict = {}
#     retail = '1'
#     for row, table, unit_field, price_field in sift_list:
#         query = '''SELECT {}, {}
#                    FROM {}
#                    WHERE upc=(?)'''.format(unit_field, price_field, table)
                       
#         data = (str(upc).upper().strip(),)
#         returnd = SQConnect(query,data).ONE()
#         print(('Retail Sifter returnd : ',returnd))
#         if not returnd:
#             return None
            
#         unitd, retaild = returnd
#         #print 'unitd : ',unitd
#         #print 'retaild : ',retaild

#         sift_dict[price_field] = [str(unitd), str(retaild)]

#     print(('Sift Dict : ',sift_dict))            
#     return sift_dict             
        

def numToWords(num,join=True):
    '''words = {} convert an integer number into words'''
    
    units = ['','one','two','three','four','five','six','seven','eight','nine']
    teens = ['','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen']
    tens = ['','ten','twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety']
    thousands = ['','thousand','million','billion','trillion','quadrillion',
                 'quintillion','sextillion','septillion','octillion', 'nonillion',
                 'decillion','undecillion','duodecillion', 
                 'tredecillion','quattuordecillion','sexdecillion', 
                 'septendecillion','octodecillion','novemdecillion',
                 'vigintillion']
    words = []
    if num==0: words.append('zero')
    else:
        numStr = '%d'%num
        numStrLen = len(numStr)
        groups = (numStrLen+2)/3
        numStr = numStr.zfill(groups*3)
        for i in range(0,groups*3,3):
            h,t,u = int(numStr[i]),int(numStr[i+1]),int(numStr[i+2])
            g = groups-(i/3+1)
            if h>=1:
                words.append(units[h])
                words.append('hundred')
            if t>1:
                words.append(tens[t])
                if u>=1: words.append(units[u])
            elif t==1:
                if u>=1: words.append(teens[u])
                else: words.append(tens[t])
            else:
                if u>=1: words.append(units[u])
            if (g>=1) and ((h+t+u)>0): words.append(thousands[g]+',')
    if join: return ' '.join(words)
    return words        


def ReturnItems(return_dict):
    cnt = len(return_dict)
    for key, tup in list(return_dict.items()):
        print(('return Items : {} -- {}'.format(key, tup)))
        (transNum, itemNum, price, qty) = tup
        #for transNum, itemNum, price, qty in tup:
            
        query = '''UPDATE transactions
                   SET quantity=quantity-(?)
                   WHERE transaction_id=(?) and upc=(?) 
                   LIMIT 1'''
        data = [Decimal(qty), transNum, itemNum,]
        returnd = SQConnect(query, data).ONE()
        
        
def ReadyClose(CloseDict): #ATs,payment=None,transType=None,stationNum=None,drawer=None,addrNum=None,custNum=None,ponumber=None,transNum=None,returns=None, debug=False):
    if CloseDict['transNum'] is None:
        transNum = TransNumAuto()
    
    if CloseDict['stationNum'] is None:
        stationNum = GetStation()
    
    if CloseDict['drawer'] is None:
        drawer = '1'

    stationNum = CloseDict['stationNum']            
    drawer = CloseDict['drawer']

    QueryOps().CheckEntryExist('transaction_id',transNum, ['transactions','transaction_payments'])
    dated = datetime.datetime.now().strftime('%Y-%m-%d') 
    timed = datetime.datetime.now().strftime('%H:%M:%S')
    
    ATs = CloseDict['ATs']
    for key, value in list(ATs.items()):
        upc = ATs[key][0]
        #print 'KEY : {} ==== VALUE : {}'.format(key,value)
        cost = LookupDB('item_detailed').Specific(upc,'upc','avg_cost')
        cost = VarOps().DeTupler(cost)
        ATs[key].insert(2,cost)
    
        fields = 'tax1,tax2,tax3,tax4,tax_never'
        returnd = LookupDB('item_detailed2').Specific(upc,'upc',fields)
        if returnd is None:
            returnd = (0, 0, 0, 0, 0)
        print(('UPC : {} : {}'.format(upc, returnd)))
        
        for i in returnd:
            ATs[key].append(i)
        
        ATs[key].insert(0,addrNum)
        ATs[key].insert(0,custNum)
        
        ATs[key].insert(0,timed)
        ATs[key].insert(0,dated)
        
        ATs[key].insert(0,transNum)
    
    subtotald =wx.FindWindowByName('pos_subtotal_txtctrl').GetCtrl()
    totald = wx.FindWindowByName('pos_total_txtctrl').GetCtrl()
    taxd = wx.FindWindowByName('pos_tax_txtctrl').GetCtrl()
    paid = wx.FindWindowByName('finishIt_paid_txtctrl').GetCtrl()
    chg = wx.FindWindowByName('finishIt_change_txtctrl').GetCtrl()
        
    try:
        receipt = PRx.TransactionReceiptPrinted(transNum, 
                                                CloseDict['transType'], 
                                                CloseDict['stationNum'],
                                                CloseDict['drawer'],
                                                dated, 
                                                timed)
        usb = True
    except:
        usb = False        
    
    if usb is not False and payment is not None:
        receipt.Header(custNum=CloseDict['custNum'],addrNum=CloseDict['addrNum'])
        transCnt = len(ATs)
        if transCnt > 0:
            totalqty = 0
            
            print(('ATS : ',ATs))
            for idx in range(transCnt):
                qty = ATs[idx][9]
                desc = ATs[idx][6]
                totalprice = ATs[idx][10]
                eachprice = ATs[idx][8]
                upc = ATs[idx][5]
                receipt.TransactionLine(idx,upc,qty,desc,totalprice)
                totalqty += Decimal(qty)
                
            receipt.SubTotal(totalqty,subtotald,taxd,totald)
            print(('Paid : {}\nPayment : {}'.format(paid, payment)))
            receipt.Change(paid,payment,chg)
            receipt.FinishPrint()
    
    
        
    VarOps().GetTyped(ATs)
        
    for key, value in list(ATs.items()):
        (transNum, date, time, custNum, addrNum, upc, description, cost, 
         retail, qty, totalprice, discount, taxable, tax1, tax2, tax3, tax4, 
         tax_never) = value
        tax_list = [tax1, tax2, tax3, tax4, tax_never]
        taxExempt = 0
        for i in tax_list:
            if i == 1:
                taxExempt = 1
                break
                
                
        
        
        
        #ponumber = wx.FindWindowByName('pos_PoTab_ponumber_txtctrl').GetCtrl()
        saveList = [(date, 'transactions', 'date'), 
                   (time,'transactions','time'),
                   (CloseDict['custNum'], 'transactions','cust_num'),
                   (CloseDict['addrNum'],'transactions','address_acct_num'),
                   (upc,'transactions','upc'),
                   (description,'transactions','description'),
                   (cost,'transactions','avg_cost'),
                   (RoundIt(retail, '1.00'),'transactions','unit_price'),
                   (qty,'transactions','quantity'),
                   (RoundIt(totalprice,'1.00'),'transactions','total_price'),
                   (discount,'transactions','discount'),
                   (CloseDict['transType'],'transactions','type_of_transaction'),
                   (tax1,'transactions','tax1'),
                   (tax2,'transactions','tax2'),
                   (tax3,'transactions','tax3'),
                   (tax4,'transactions','tax4'),
                   (tax_never,'transactions','tax_never'),
                   (taxExempt, 'transactions','tax_exempt'),
                   (CloseDict['poNum'],'transactions','po_number')]
                   
        fieldSet, dataSet, table = QueryOps().Commaize(saveList, 'vari')
        
        
        query = '''UPDATE {} 
                   SET {}
                   WHERE transaction_id=(?)'''.format(table, fieldSet)  

        data = dataSet + [transNum,]                             
                                      
        returnd = SQConnect(query, data).ONE()
        
        
    
    query = 'UPDATE transactions SET type_of_transaction=(?) WHERE transaction_id=(?)'
    data = (transType, transNum,)
    SQConnect(query, data).ONE()
    #
    query = '''UPDATE transaction_notes 
               SET transaction_id=(?)
               WHERE transaction_id="CURRENT"'''
    data = (transNum,)
    SQConnect(query, data).ONE()
    
    TransNumAuto(addOne=True)
    
    if transType != 'Hold':
        paid = wx.FindWindowByName('finishIt_paid_txtctrl').GetCtrl()
        if paid == '' or paid is None:
            paid = 0
        
        query = '''UPDATE transaction_payments SET paid=(?),
                                                   total_price=(?),
                                                   date=(?),
                                                   time=(?),
                                                   cust_num=(?),
                                                   address_acct_num=(?),
                                                   pay_method=(?),
                                                   type_of_transaction=(?),
                                                   tax=(?),
                                                   cash_payment=(?),
                                                   check_payment=(?),
                                                   check_num=(?),
                                                   dl_number=(?),
                                                   phone_num=(?),
                                                   dob=(?),
                                                   card1_payment=(?),
                                                   auth1_num=(?),
                                                   card1_type=(?),
                                                   card1_numbers=(?),
                                                   card2_payment=(?),
                                                   auth2_num=(?),
                                                   card2_type=(?),
                                                   card2_numbers=(?),
                                                   card3_payment=(?),
                                                   auth3_num=(?),
                                                   card3_type=(?),
                                                   card3_numbers=(?),
                                                   card4_payment=(?),
                                                   auth4_num=(?),
                                                   card4_type=(?),
                                                   card4_numbers=(?),
                                                   card5_payment=(?),
                                                   auth5_num=(?),
                                                   card5_type=(?),
                                                   card5_numbers=(?),
                                                   debit_payment=(?),
                                                   auth6_num=(?),
                                                   debit_type=(?),
                                                   debit_numbers=(?),
                                                   charge=(?),
                                                   change_back=(?)
                   WHERE transaction_id=(?)
               '''
        
#        query = '''INSERT INTO transaction_payments (transaction_id, total_price, date, time, cust_num, address_acct_num, 
#                                                     pay_method, type_of_transaction, tax, cash_payment, check_payment, check_num, 
#                                                     dl_number, phone_num, dob,
#                                                     card1_payment, auth1_num, card1_type, card1_numbers,
#                                                     card2_payment, auth2_num, card2_type, card2_numbers, 
#                                                     card3_payment, auth3_num, card3_type, card3_numbers, 
#                                                     card4_payment, auth4_num, card4_type, card4_numbers,
#                                                     card5_payment, auth5_num, card5_type, card5_numbers,
#                                                     debit_payment, auth6_num, debit_type, debit_numbers, charge, change_back)
#                   VALUES (?,?,?,?,?,?,
 #                          ?,?,?,?,?,
 #                          ?,?,?,?,?,
 #                          ?,?,?,?,?,
 #                          ?,?,?,?,?,
 #                          ?,?,?,?,?,
 #                          ?,?,?,?,?,?,?,?,?,?);'''       
    
        pay_method = SplitTender(payment)
    
        
    
        print(('date : ',date))
        print(('time : ',time))    
        toData = (totalprice, date, time, custNum, addrNum, pay_method, transType, taxd)
    
        restoData = PayDatas(payment)
    
        whereFrom = (transNum,)
        data = (paid,) + toData + restoData + whereFrom
       
        SQConnect(query, data).ONE()
    
        UnHoldSale(transNum)
    
    if returns is not None and len(returns) > 0:
        ReturnItems(returns)
    
        #            data = (transNum, date, time, custNum, addrNum,)            
    

    return 'finished'

def PayDatas(credInfo, debug=False):
    payDict = {'cash' : {'paid':0},
               'check' : {'paid':0,'checkNum':'','dlNum':'','phoneNum':'','dob':''},
               'credit1' : {'paid':0,'authNum':'','cardType':'','cardNum':''},
               'credit2' : {'paid':0,'authNum':'','cardType':'','cardNum':''},
               'credit3' : {'paid':0,'authNum':'','cardType':'','cardNum':''},
               'credit4' : {'paid':0,'authNum':'','cardType':'','cardNum':''},
               'credit5' : {'paid':0,'authNum':'','cardType':'','cardNum':''},      
               'debit' : {'paid':0,'authNum':'','cardType':'','cardNum':''},
               'charged' : {'paid':0},
               'change_back' : {'change':0}
               }
        
    print(f'Cred Info : {credInfo}')
    for key, value in list(credInfo.items()):
        typd = str(type(value))
        print(('key : {} => {}'.format(key, typd)))
        if 'tuple' in typd:
            payDict[key] = value
        elif 'str' in typd:
            payDict[key] = (value,)
        else:
            print("I Don't Know where to put you")

        
     
    return payDict
    
    
    
    
def SplitTender(credInfo, debug=False):
    
    mto = 0
    paymeth = ''
    
    if credInfo is not None:
        for key, value in list(credInfo.items()):
            value = str(value)
            if value != 0:
                mto += 1
                paymeth = key
                
    
        if mto > 2:
            paymeth = 'Split'
    
    return paymeth.upper()
        

def UnHoldSale(transNum):
    query = '''UPDATE transactions 
               SET type_of_transaction = "Sale" 
               WHERE transaction_id = ? 
                AND type_of_transaction = "Hold"'''
    
    data = (transNum,)
    returnd = SQConnect(query,data).ALL()
    
    
    
        
# def ListAdjustEven(listd):
#     list_cnt = len(listd)
#     entr_cnt = len(listd[0])
    
#     if list_cnt % 2 != 0:
#         value = ('',)
#         for i in range(entr_cnt-1):
#             value += ('',)
#         #value = ('','','')
#         listd.append(value)
    
#     return listd
                 
# def ButtonOff(names, state=True):
#     typ = str(type(names))
#     print(('typd : ',typ))
#     if re.search('(unicode|str)', typ, re.I):
#         item = wx.FindWindowByName(names)
#         if state is True:
#             item.Disable()
#         else:
#             item.Enable()
            
#     if 'list' in typ:
#         for name in names:
#             print(('button name : ',name))
#             item = wx.FindWindowByName(name)
#             if state is True:
#                 item.Disable()
#             else:
#                 item.Enable()


 

def UnDated(dated):
    typd = str(type(dated))
    dater = dated
    if 'datetime' in typd:
        dater = dated.strftime('%Y-%m-%d')
    
    
    return dater
     
# def LCGetSelected(evt):
#     debug=False
#     obj = evt.GetEventObject()
#     named = obj.GetName()
#     item_id = obj.GetFirstSelected()
#     
#     objText = obj.GetItemText(item_id)
#     return item_id, objText
            
def ScaleImage(filepath):
    img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
    # scale the image, preserving the aspect ratio
    W = img.GetWidth()
    H = img.GetHeight()
    photoMaxSize = 300
    if W > H:
        NewW = photoMaxSize
        NewH = photoMaxSize * H / W
    else:
        NewH = photoMaxSize
        NewW = photoMaxSize * W / H
    
    img = img.Scale(NewW,NewH)
    
    return img         


class Transactional(object):
    def __init__(self, dictionary, debug=False):
        """
    This Object keeps track of all the items & their properties.
    Comparing the latest to all previous items, inorder to join with previous items
    to make the inventory & transaction entries easier to manipulate later.

    Transaction Data Variable layout:
        self.transData = {"Sale":
                            {transaction_number:
                                {"UPC":
                                    {
                                    "Desc":"example Description",
                                    "Qty":"1",
                                    "Cost":"0.00",
                                    "setRTL":"0.00",
                                    "pricetree":{"1":"0.00"},
                                    "Discount":"0%", 
                                    "Taxable":True
                                    }
                                }
                            }
                        "Return":
                            {transaction_number:
                                {"UPC":
                                    {
                                    "Desc":"example Description",
                                    "Qty":"1",
                                    "Cost":"0.00",
                                    "RTL":"0.00",
                                    "pricetree":{'1':'0.00'}, 
                                    "Discount":"0%", 
                                    "Taxable":True
                                    }
                                }
                            }
                        }
    """    
        self.dict = dictionary
        self.grid = wx.FindWindowByName('pos_transactions_grid')
        

    def LoadDict(self):
        rows = self.grid.GetNumberRows()
        for idx in range(rows):
            chkItem = self.grid.GetCellValue(idx,0)
            if len(chkItem) > 0:
                self.dict[idx] = GetItemLine(self.grid.GetName(), idx)
        
        return d    
        
    def RefreshDict(self):
        idx = 0
        maxd = len(self.dict)
        for item in range(maxd):
            if idx in self.dict: 
                self.dict[idx] = self.dict[item]
            else:
                self.dict[idx] = self.dict[item + 1]   
                self.dict.pop(item + 1)
            
            idx += 1
        
        return self.dict
        

    def RefreshTransactions(self):
        self.grid.ClearGrid()
        
        for xx in range(grid.GetNumberRows()):
            for yy in range(grid.GetNumberCols()):
                self.grid.SetReadOnly(xx,yy,False)
        
        for key in self.dict:
            
            (upc,desc,price,qty,total,disc,tx) = self.dict[key]
                
            setList = [('Item Number',upc),('Description',desc),('Price',price),
                    ('Quantity',qty),('Total',total),('Disc',disc),
                    ('Tx',tx)]
            
            self.grid.SetReadOnly(key,0,True)
            GridOps(gridname).FillGrid(setList, row=key)

   
   

    def GetTaxRate(price):
        fields = '''min_sale, max_sale, from_amt0, 
                    tax_rate0, from_amt1, tax_rate1, 
                    from_amt2, tax_rate2''' 
        
        returnd = LookupDB('tax_tables').Specific('TAX','tax_name',fields)
        (min_sale, max_sale, from_amt0, tax_rate0, from_amt1,
        tax_rate1, from_amt2, tax_rate2) = returnd 
        if returnd is None:
            return
        
        if Decimal(price) > Decimal(min_sale):
            if Decimal(price) > Decimal(from_amt0):
                taxd = Decimal(tax_rate0)    
                

            if Decimal(from_amt1) > 0:
                if Decimal(price) > Decimal(from_amt1):
                    taxd = Decimal(tax_rate1)
                    

            if Decimal(from_amt2) > 0:
                if Decimal(price) > Decimal(from_amt2):
                    taxd = Decimal(tax_rate2)
                    
            
        
            
        if taxd >= 1:
            taxd = Decimal(taxd) / 100
                    
        
        return taxd
    
    def GetTaxable(upc, taxable, discount_col=''):
        
        Taxed = True
        query = 'SELECT tax1,tax2,tax3,tax4,tax_never FROM item_detailed2 WHERE upc=(?)'
        data = (upc,)
        returnd = SQConnect(query, data).ONE()
        
        
        tax1, tax2, tax3, tax4, tax_never = 0,0,0,0,0
        
        if returnd is not None:
            (tax1,tax2,tax3,tax4,tax_never) = returnd
            
        
        tax_list = [(0, tax1),('A',tax2),('B',tax3),('C',tax4)]
        
        tx_dict = {}
        for key, value in tax_list:
            tx_dict[key] = value
        
        if discount_col == '' or discount_col is None:
            discount_col = 0
        
        if tx_dict[discount_col] == 1 or tx_dict is True:
            Taxed = False
        
        if taxable is False:
            Taxed = False
            
            
        if tax_never == 1:
            Taxed = False
            
            
        
        if Taxed is False:
            pr_tax = 'nTx'
        else:   
            pr_tax = 'Tx'
        
        return Taxed,pr_tax


    def CheckTaxHoliday(upc):
        """Check Tax Holiday Worksheet."""
        query = 'SELECT begin_date, end_date, upc, active FROM tax_holiday'
        data = ''
        returnd = SQConnect(query, data).ALL()
        for begins, ends, upcs, active in returnd:
            if active == 1:
                delta = begins
        
        
        
        
        
    def GetRetail(upcd, cust_num, retailsd_JSON=None, on_discount=None, debug=False):
        if retailsd_JSON is None:
            discountd = None
            new_retail = '0'
        
        else:   
            retailsd = retailsd_JSON
            
            retail_regular = retailsd['standard_price']['price']
            if on_discount[1] > 0:
                discount = CheckDiscount(upcd, cust_num, on_discount[1])
            else:
                discount = CheckDiscount(upcd, cust_num, on_discount[0])
            
            if discount > 0:
                discountd = str(discount)
                new_retail = DiscountIt(retail_regular, discountd)
            else:
                discountd = None
                new_retail = retail_regular
                                
        
        return discountd,new_retail
        
    
    
# def DecimalOnly(gridname, colname, row, col, value=None):
#     grid = wx.FindWindowByName(gridname)
#     if value is None:
#         value = GetCell(grid.GetName(),colname,row)
    
#     if re.search(r'[0-9]', value, re.I):
#         new_value = RoundIt(value, '1.00')
#         setList = [(colname,new_value)]
#         FillGrid(grid.GetName(),setList, row=row)
#         return 'OK',new_value
       
#     else:
#         setList = [(colname,'')]
#         FillGrid(grid.GetName(),setList,row=row)
#         wx.CallAfter(grid.SetGridCursor, row, col)    
    
# class LookupDB(object):
#     def __init__(self, table, debug=False):
#         self.table = table
        
    
#     def General(self, selectFields, limit=None):
#         """
#         Lookup in the database for a non-specific search.

#         Arguments:
#           selectFields -- Which fields that you will be searching for. (Mandatory)
#           limit        -- Limit the search to a specific number of records. (Optional)
#         """

#         limitd = self.Limit(limit)
#         query = '''SELECT {}
#                    FROM {}
#                    {}'''.format(selectFields, self.table, limitd)
        
#         data = ''
#         returnd = SQConnect(query, data).ALL()

#         return returnd
        
#     def Specific(self, whereValue, whereField, selectFields, limit=None):
#         limitd = self.Limit(limit)
#         query = '''SELECT {}
#                    FROM {}
#                    WHERE {}=(?)
#                    {}'''.format(selectFields, self.table, whereField, limitd)
        
#         data = [whereValue,]
#         returnd = SQConnect(query, data).ALL()
        
#         if returnd is None:
#             returnd = (None,)
#         if len(returnd) == 0 :
#             returnd = (None,)

#         return returnd[0]                

#     def Count(self, whereValue=None, whereField=None, limit=None):
#         limitd = self.Limit(limit)
#         where_Stmt = 'WHERE {}=(?)'.format(whereField)
#         if whereField is None:
#             where_Stmt = ''
#         query = '''SELECT count(*)
#                    FROM {}
#                    {}
#                    {}'''.format(self.table, where_Stmt, limitd)
#         data = [whereValue,]
#         if not whereValue:
#             data = []
#         pout.v(f'Where : {query}\n Data : {data}')
#         returnd = SQConnect(query, data).ONE()
#         # if len(returnd) == 0:
#         #     returnd = (None,)

#         pout.v(f'Count : {returnd}')
#         return returnd[0]


#     def Limit(self, limit):
        
#         if limit is not None:
#             limitd = 'LIMIT {}'.format(limit)
#         else:
#             limitd = ''
#         return limitd            

#     def UpdateSingle(self, setField, setValue, whereField, whereValue):
#         if setValue is None:
#             setValue = "NULL"            
#         else:
#             setValue = f"'{setValue}'"

#         query = '''UPDATE {}
#                    SET {}={}
#                    WHERE {}=(?)'''.format(self.table, setField, setValue, whereField)
#         data = [whereValue,]
#         returnd = SQConnect(query, data).ALL()
#         # print(f"Update Single Returnd : {returnd}")
#         # print('Type of Returnd : {}'.format(str(type(returnd))))
#         a = str(type(returnd))
#         obret = VarOps().CheckNone(returnd)
        
#         return obret    

#     def UpdateGroup(self, setWhatNto, whereField, whereValue):
#         query = '''UPDATE {}
#                    SET {}
#                    WHERE {}=(?)'''.format(self.table, setWhatNto, WhereField)
#         data = WhereValue
#         returnd = SQConnect(query, data).ALL()
        
#         return returnd[0]

#     def DescribeTable(self):
#         try:
#             query = 'DESCRIBE {};'.format(self.table)
#             data = []
#             returnd = SQConnect(query, data).ALL()
#             pout.v(f'DescribeTable : {query}')
#             info = {}
#             tb = len(returnd)
#             for cnt in range(0, tb):
#                 for val in returnd:
#                     info[cnt] = {'field': val[0],
#                             'type': val[1],
#                             'null': val[2],
#                             'key': val[3],
#                             'default': val[4],
#                             'extra': val[5]}
#                 returnd = info
#             pout.v(returnd)
#             time.sleep(3)
#         except:
#             returnd = None
        
#         return returnd

#     def is_table(self):
#         query = '''SELECT * FROM information_schema.COLUMNS 
#                    WHERE TABLE_SCHEMA = 'rhp' 
#                    AND TABLE_NAME = "{}"
#                 '''.format(self.table)
#         data = []
#         returnd = SQConnect(query, data).ALL()
#         return returnd
    
#     def is_field(self, fieldname):
#         query = '''   
#         SELECT * 
#         FROM information_schema.COLUMNS 
#         WHERE 
#             TABLE_SCHEMA = 'rhp' 
#         AND TABLE_NAME = '{}' 
#         AND COLUMN_NAME = '{}'; '''.format(self.table, fieldname)
#         data = []
#         returnd = SQConnect(query, data).ONE()
#         return returnd
        
# def LookupDB(itemNumber,getType,fromtable,fields_to_return, limit=None):
#     ''' itemNumber = could be item upc or customer acct_num whatever is the Primary Key
#         getType = is the field name of the Primary Key
#         fromtable = from Table Who knows, hopefully you do
#         field_to_return = a string such as this 'description,retails' or whatever you want'''
#     limitd = ''
#     if limit is not None:
#         limitd = 'LIMIT {}'.format(limit)
#     
#     if getType is None or getType == '':
#         query = 'SELECT {0} FROM {1} {}'.format(fields_to_return, fromtable, limitd)
#         data = ''
#     else:
#         query = 'SELECT {0} FROM {1} WHERE {2}=(?) {}'.format(fields_to_return,
#                                                            fromtable,getType,limitd)
#         data = (itemNumber,)
#     
#     returnd = SQConnect(query, data).ONE()
#     
#     return returnd

# def ToggleState(name, statuses, debug=False):
#     current = wx.FindWindowByName(name).GetCtrl()
#     if len(current) == 0:
#         current = statuses[0]
#     idx = statuses.index(current)
#     cnt = len(statuses)
    
#     next = idx + 1
#     if next > cnt-1:
#         next = 0
    
#     wx.FindWindowByName(name).GetCtrl( statuses[next])
#     return statuses[next]
    
# def ButtonToggle(buttonName, state=True):
#     btn = wx.FindWindowByName(buttonName)
#     downColor = (121, 145, 183)
#     upColor = (wx.NullColour) #212, 226, 247
#     if state is not True:
#         btn.SetBackgroundColour(downColor)
#         return True
#     else:
#         btn.SetBackgroundColour(upColor)
#         return False
                       

def AddIt(dictionary):
    add = 0
    for key,value in list(dictionary.items()):
        add += Decimal(value)
    
    return add                            


class GridOps(object):
    def __init__(self, gridname, debug=False):
        self.gridname = gridname
        self.grid = wx.FindWindowByName(gridname)
        
    def GRIDtoJSON(self):
        xcnt = self.grid.GetNumberRows()
        ycnt = self.grid.GetNumberCols()
        dictd = {}
        for x in range(xcnt):
            rowLabel = self.grid.GetRowLabelValue(x)
            dictd[rowLabel] = {}
            for y in range(ycnt):
                colLabel = self.grid.GetColLabelValue(y)
                celldata = self.grid.GetCellValue(x, y)
                dictd [rowLabel][colLabel]=celldata
            
            
        return json.dumps(dictd)
    
    def JSONtoGRID(self, JSONFile):
        dictd = json.loads(JSONFile)
        x = 0
        y = 0
        for x in range(xcnt):
            rowLabel = self.grid.GetRowLabelValue()
            for y in range(ycnt):
                colLabel = self.grid.GetColLabelValue()
                celldata = dictd[rowLabel][colLabel]
                pout.v(f'Row : {rowLabel} ; Col : {colLabel} ; Data : {celldata}')
                self.grid.SetCellValue(x,y,celldata)    
            
            


    def CurGridLine(self, blank=False):
        row = 0
        maxRows = self.grid.GetNumberRows()
        for x in range(maxRows):
            value = self.grid.GetCellValue(x,0)
            if value == '' or value is None:
                row = x - 1
                if blank is True:
                    row = x
                
                if row < 0:
                    row = 0    
                
                return row     

    def GetGridCursor(self):
        row = self.grid.GetGridCursorRow()
        col = self.grid.GetGridCursorCol()
        
        return row, col   
        
    def GridFocusNGo(self, row=None, col=0):
        cur_row = self.CurGridLine()
        if row == None and cur_row != 0:
            row = self.CurGridLine()+1
        else:
            row = cur_row
            
        self.grid.SetFocus()
        wx.CallAfter(self.grid.SetGridCursor, row, col) 

    def FillGrid(self, setlist, row=None,col=None, debug=False):
        
        if row is not None:
            for yy in range(self.grid.GetNumberCols()):
                header = self.grid.GetColLabelValue(yy)
                
                for title, value in setlist:
                    if title in header:
                        self.grid.SetCellValue(int(row), yy, str(value))

        if col is not None:
            for xx in range(grid.GetNumberRows()):
                header = self.grid.GetRowLabelValue(xx)
                
                
                for title, value in setlist:
                    if title in header:
                        self.grid.SetCellValue(xx, int(col),str(value))                    
                    
    def GridAlternateColor(self, result=None):
        bgcolor = Themes(self.gridname).GetColor('bg')
        whitetext = Themes(self.gridname).GetColor('text')
        cell_color = Themes(self.gridname).GetColor('cell')
        
        if result is None:
            result = self.grid.GetNumberRows()
            
        colorlength = result
        
        if not str(result).isdigit():
            colorlength = self.grid.GetNumberRows()
        for xx in range(colorlength):
            for yy in range(self.grid.GetNumberCols()):
                try:
                    self.grid.SetCellBackgroundColour(xx, yy, bgcolor)
                except:
                    print(f'bgcolor : {bgcolor}')
        
        for xx in range(colorlength):
            if xx % 2:
                for yy in range(self.grid.GetNumberCols()):
                    try:
                        self.grid.SetCellBackgroundColour(xx, yy, cell_color)
                    except:
                        print(f'bgcolor : {bgcolor}')
    
    def GridHomeColor(self, row):
        bgcolor = (0, 0, 255)
        whitetext = (255, 255, 255)
        home_color = (209, 201, 94)
        
        for yy in range(self.grid.GetNumberCols()):
            self.grid.SetCellBackgroundColour(row, yy, home_color) 

    def GridListReadOnly(self, header_list, rowcol='row'):
        if 'row' in rowcol:
            for xx in range(self.grid.GetNumberRows()):
                for item in header_list:
                    rowName = self.grid.GetRowLabelValue(xx)
                    if rowName == item:
                        self.grid.SetReadOnly(xx,0,True)
                
        if 'col' in rowcol:
            for yy in range(self.grid.GetNumberCols()):
                for item in header_list:
                    colName = self.grid.GetColLabelValue(yy)
                    if rowName == item:
                        self.grid.SetReadOnly(0,yy,True)

    def DecimalOnly(self, colname, row, col, value=None):
        if value is None:
            value = GridOps(self.grid.GetName).GetCell(colname,row)
        
        if re.search(r'[0-9]', value, re.I):
            new_value = RoundIt(value, '1.00')
            setList = [(colname,new_value)]
            self.FillGrid(setList, row=row)
            return 'OK',new_value
        
        else:
            setList = [(colname,'')]
            self.FillGrid(setList,row=row)
            wx.CallAfter(self.grid.SetGridCursor, row, col)    

    def FindEmptyRow(self):
        rows = self.grid.GetNumberRows()
        
        for xx in range(rows):
            cell = self.grid.GetCellValue(xx, 0)
            if cell == '' or cell is None:
                return xx    
        
    def DisplayItemsinGrid(self, headers, itemList):
        if itemList:
            self.grid.ClearGrid()
            yy = 0
            for xx in range(len(itemList)):
                
                for yy in range(self.grid.GetNumberCols()):
                    
                    grid_header = self.grid.GetColLabelValue(yy)
                    
                    if re.search(headers[yy], grid_header, re.I):
                        if 'price' in grid_header:
                            self.grid.SetCellValue(xx, yy,
                                            itemList['standard_price']['price'])
                        else:
                            self.grid.SetCellValue(xx, yy, itemList[xx][yy])
                        
                            

    def AlterGrid(self, returnd):
        if returnd is None:
            current = self.grid.GetNumberRows()
            self.grid.DeleteRows(0, current, True)
        else:
            current, new = (self.grid.GetNumberRows(), len(returnd))

            if new > current:
                self.grid.AppendRows(new - current)

            if new < current:
                self.grid.DeleteRows(0, current - new, True)

        wx.FindWindowByName(grid.GetName()).ClearCtrl()
        self.GridAlternateColor()

    def GridCellLabelSet(self, col_list, tname='POS'):
        bgcolor = Themes(tname).GetColor('bg')
        textcolor = Themes(tname).GetColor('whitetext')
        sized = self.GridCol_Sized(col_list)
        self.GridAlternateColor('')
        
        

        for xx, yy, label in col_list:
            
            self.grid.SetColSize(yy, sized[yy])
            self.grid.SetCellValue(xx, yy, label)
            self.grid.SetCellBackgroundColour(xx, yy, bgcolor)
            self.grid.SetCellTextColour(xx, yy, textcolor)
            self.grid.SetCellFont(xx, yy, wx.Font(wx.FontInfo(12).Bold()))
            self.grid.SetReadOnly(xx, yy, True)
            self.grid.SetRowSize(xx, 50)

        self.grid.SetColSize(1, 150)
        self.grid.SetReadOnly(0, 1, False)

    def GridCol_Sized(self, col_list, debug=False):
        last_size = {}
        size = {}
        sized = {}
        ListSize = len(col_list)
        last_yy = 0
        for xx, yy, label in col_list:
            last_size[yy] = 0
            size[yy] = 0

        for xx, yy, label in col_list:
            if not last_size[yy]:
                last_size[yy] = 0
            size[yy] = len(label)
            if size[yy] > last_size[yy]:
                last_size[yy] = size[yy]

        for key, value in list(last_size.items()):
            sized[key] = value * 12
            

        return sized

    def GetCell(self, title, rowcol):
        colsnum = self.grid.GetNumberCols()
        checkColName = self.grid.GetColLabelValue(0)
        if re.match('[A-Z]', checkColName) and len(checkColName) == 1:
            rowsnum = self.grid.GetNumberRows()
            for row in range(rowsnum):
                if title in self.grid.GetRowLabelValue(row):
                    now_retail = self.grid.GetCellValue(row, rowcol)
        else:
            for col in range(colsnum):
                if title in self.grid.GetColLabelValue(col):
                    now_retail = self.grid.GetCellValue(rowcol, col)

        return now_retail.strip()


    def GetColNumber(self, title):
        rowcol = self.grid.GetNumberCols()
        for col in range(rowcol):
            if title in self.grid.GetColLabelValue(col):
                colnum = col
                break

        return colnum




def GetStation():
    with open('config.rhp', 'r') as f:
        for l in f:
            if re.match('station', l, re.I):
                b = re.search('station=([0-9])', l, re.I)
                station_num = b.group(1)
                if not re.match('[0-9]', station_num):
                    station_num = 0
    
    return station_num



# def GetTyped(item, debug=False):

#     typed = str(type(item))
#     
    
#     return typed


def EmptyRetails(upc):
    do_list = ['standard_price', 'price_level_(a)', 'price_level_(b)',
               'price_level_(c)', 'price_level_(d)', 'price_level_(e)',
               'price_level_(f)', 'price_level_(g)', 'price_level_(h)',
               'price_level_(i)', 'on_sale_price','compare_price']
               
    retails = {}
    for key in do_list:
        retails[key] = ('1','0.00','Margin','0.0000')
    
    retaild_JSON = json.dumps(retails)    
    # query = 'UPDATE item_detailed SET retails = (?) WHERE upc=(?)'
    # data = (retaild_JSON, upc)
    # SQConnect(query, data).ONE()
    LookupDB('item_detailed').UpdateSingle('retails', retaild_JSON, 'upc', upc)
    
def TransactionCheck(transId):
    query="""SELECT date, time, type_of_transaction,
                    total_price  
                 FROM transactions 
                 WHERE transaction_id=(?)"""
            
    data = (transId)
    returnd = SQConnect(query,data).ALL()
    
 

def GroupUpdate(groupList, whereOwner, whereUser):
    ''' Group List should include tuples of (1,2,3)
        1. field to be updated
        2. name of ctrl to be saved
        3. table name
    '''
    
    pass    
    
class Themes(object):
    def __init__(self, tname='POS', debug=False):
        self.tname = self.GetThemeName(tname)
        pout.v(self.tname)

    def GetColor(self, color_for):
        note_color = '#f8fda9'
        info_color = '#e8f4f0'
        returnd = None
        returnd = LookupDB('themes').Specific(self.tname, 'theme_name', color_for)
        print(f'GetColor {self.tname} : Returnd : {returnd}')
        return returnd
        # (bg, text, cell) = returnd
        
        # bg = re.sub('[b\']','',bg)
        # text = re.sub('[b\']','',text)
        # cell = re.sub('[b\']','',cell)
        
        
        # if returnd is None:
        #     bg = '#fffff'
        #     text = '#00000'
        #     cell = '#d9f1e8'
        
        # listd = [('info', info_color),('note',note_color),('cell',cell),('text',text),('bg',bg)]
        # for label, color in listd:
        #     if label in color_for:
        #         return color
       
    def GetThemeName(self,ctrlname):
        tname='POS'
        
        if re.match('cus[tomers_]+', ctrlname, re.I):
            tname = 'CUSTOMERS'
        
        if re.match('In[ventory_]+', ctrlname, re.I):
            tname = 'INVENTORY'
        
        if re.match('Ven[dors_]+', ctrlname, re.I):
            tname = 'VENDORS'
    
        return tname            
                    
    
    
    
def LCAlternateColor(lc_name,result_length,module_name='POS'):
    cell = Themes(lc_name).GetColor('cell')
    lc = wx.FindWindowByName(lc_name)
    idx = 0
    for idx in range(result_length):
        if idx % 2:
            pass
#            lc.SetItemBackgroundColour(idx,cell)
        

def LCFill(lc_name, setList,idx):
    lc = wx.FindWindowByName(lc_name)
    
    for xx, vari in setList:
        if xx == 0:
            lc.InsertItem(idx, str(vari))
        if xx > 0:
            lc.SetItem(idx, xx, str(vari))
                
 
# def GridListReadOnly(gridname, header_list, rowcol='row'):
#     grid = wx.FindWindowByName(gridname)
#     if 'row' in rowcol:
#         for xx in range(grid.GetNumberRows()):
#             for item in header_list:
#                 rowName = grid.GetRowLabelValue(xx)
#                 if rowName == item:
#                     grid.SetReadOnly(xx,0,True)
            
#     if 'col' in rowcol:
#         for yy in range(grid.GetNumberCols()):
#             for item in header_list:
#                 colName = grid.GetColLabelValue(yy)
#                 if rowName == item:
#                     grid.SetReadOnly(0,yy,True)
                                

# def Commaize(list_of_tuples, typd='names'):
#     idx = 0
#     fieldSet = ''
#     dataSet = []
    
#     print(('CommaIze : {} : {}'.format(list_of_tuples, typd)))
#     for name,table,field in list_of_tuples:
#         if typd == 'names':
#             value = wx.FindWindowByName(name).GetCtrl()
#         if typd == 'vari':  
#             value = name
#         if value is None or value == '':
#             continue
#         if idx > 0:
#             fieldSet += ', '
            
#         fieldSet += '{}=(?)'.format(field)
#         dataSet.append(value)
            
#         idx += 1
#         table = table
            
#     print(('Field Set : ',fieldSet))
#     print(('data Set : ',dataSet))
#     print(('table : ',table))
#     return fieldSet, dataSet, table
    
    
class ListCtrl_Ops(object):
    def __init__(self, lcname, debug=False):
        self.lcname = lcname
        self.lc = wx.FindWindowByName(self.lcname)
        

    def LCSetHeaders(self, setList):
        
        for idx, label, width, opts in setList:
            if 'right' in opts.lower():
                self.lc.InsertColumn(idx, label, format=wx.LIST_FORMAT_RIGHT, width=width)    
            else:
                self.lc.InsertColumn(idx, label, width=width)

    def LCAlternateColor(self, result_length,module_name='POS'):
        cell = Themes(self.lcname).GetColor('cell')
        idx = 0
        for idx in range(result_length):
            if idx % 2:
                self.lc.SetItemBackgroundColour(idx,cell)
            

    def LCFill(self, setList,idx):
        for xx, vari in setList:
            
            if xx == 0:
                self.lc.InsertItem(idx, str(vari))
            if xx > 0:
                self.lc.SetItem(idx, xx, str(vari))

    # def LCGet(self, idx=None):
    #     for 

class EventOps(object):
    def __init__(self):
        '''Collection of Events.'''
        

    def OnNumbersOnly(self, event):
            """
            check for numeric entry accepted result is in self.value
            """
            
            valued = event.GetEventObject()
            raw_value = valued.GetValue().strip()
            if raw_value == '' or raw_value == None:
                raw_value = '0'
            named = valued.GetName()
            edit_txtctrl = wx.FindWindowByName(named)
            # numeric check
            if re.match('[Xx]', raw_value):
                raw_value = "10"
                #edit_txtctrl.ChangeValue(str(raw_value))


            if all(x in '0123456789.+-/' for x in raw_value):
                # convert to float and limit to 2 decimals
                value = Decimal(raw_value)
                if 'discount' in named:
                    if value > 100:
                        value = 10

                edit_txtctrl.ChangeValue(str(value))
            #else:
            #    edit_txtctrl.ChangeValue("")
            #    edit_txtctrl.SetToolTip(wx.ToolTip("NUMBERS ONLY!!!"))


    def LCGetSelected(self, event):
        debug=False
        obj = event.GetEventObject()
        named = obj.GetName()
        item_id = obj.GetFirstSelected()
        
        objText = obj.GetItemText(item_id)
        return item_id, objText

    def ListBoxOnAddButton(self, event):
        
        obj = event.GetEventObject()
        print(f'OBJ : {obj}')
        
        addbutton_name = obj.GetName()
        print(f'addbutton name : {obj.GetName()}')
        listbox_name = re.sub('_addbutton', '', addbutton_name)
        tc_name = re.sub('_addbutton', '_txtctrl', addbutton_name)
        lc_txtctrl = wx.FindWindowByName(tc_name)
        if not lc_txtctrl.GetValue():
            return
        print(f'List Box Name : {listbox_name}')
        listbox = wx.FindWindowByName(listbox_name)
        num_altlookups = listbox.GetCount()
        

        tobe_searched = lc_txtctrl.GetValue()
        has_found = listbox.FindString(tobe_searched)
        addbutton = wx.FindWindowByName(addbutton_name)
        if has_found != -1:
            
            foundIndex = has_found
            listbox.EnsureVisible(foundIndex)
            addbutton.SetBackgroundColour('Red')
            lc_txtctrl.Clear()
            lc_txtctrl.SetFocus()
        else:
            
            addbutton.SetBackgroundColour('Green')
            listbox.Append(lc_txtctrl.GetValue().upper())
            lc_txtctrl.Clear()
            lc_txtctrl.SetFocus()

        allstrings = listbox.GetStrings()
        


    def ListBoxSelectItem(self, event):
        obj = event.GetEventObject()
        obj_name = obj.GetName()
        tc_name = re.sub('_listbox', '_listbox_txtctrl', obj_name)
        addbutton_name = re.sub('_listbox', '_listbox_addbutton', obj_name)
        rembutton_name = re.sub('_listbox', '_listbox_rembutton', obj_name)
        listbox_name = obj_name
        
        lc_txtctrl = wx.FindWindowByName(tc_name)
        addbutton = wx.FindWindowByName(addbutton_name)
        rembutton = wx.FindWindowByName(rembutton_name)
        listbox = wx.FindWindowByName(listbox_name)
        selection = listbox.GetStringSelection()
        wx.FindWindowByName(tc_name).SetCtrl(selection)


    def ListBoxOnRemoveButton(self, event):
        obj = event.GetEventObject()
        rembutton_name = obj.GetName()
        tc_name = re.sub('_rembutton', '_txtctrl', rembutton_name)
        addbutton_name = re.sub('_rembutton', '_addbutton', rembutton_name)
        listbox_name = re.sub('_rembutton', '', rembutton_name)
        
        
        lc_txtctrl = wx.FindWindowByName(tc_name)
        addbutton = wx.FindWindowByName(addbutton_name)
        rembutton = wx.FindWindowByName(rembutton_name)
        listbox = wx.FindWindowByName(listbox_name)

        tobe_removed = lc_txtctrl.GetValue()
        currentItem = listbox.FindString(tobe_removed)
        
        if currentItem != -1:
            listbox.EnsureVisible(currentItem)
            listbox.Delete(currentItem)
            

        lc_txtctrl.Clear()
        lc_txtctrl.SetFocus()

        
    def Capitals(self, event):
        """ Capitalize First Letters """
        valued = event.GetEventObject()
        raw_value = valued.GetValue()
        named = valued.GetName()
        edit_ctrl = wx.FindWindowByName(named)
        new_value = raw_value.title()
        exempt_list = [' llc', ' ltd', ' corp ', 'sr ',
                    ' S.R. ', ' rv ', 'pk', 'x']
        for exempt in exempt_list:
            if re.search(exempt, new_value, re.I):
                new_exempt = exempt.upper()
                new_value = re.sub(exempt, new_exempt, new_value, flags=re.I)
                
        if 'combobox' in named:
            edit_ctrl.SetValue(new_value)
        if 'txtctrl' in named:
            edit_ctrl.ChangeValue(new_value)


    def CheckMeasurements(self, event):
        valued = event.GetEventObject()
        raw_value = valued.GetValue()
        named = valued.GetName()
        edit_ctrl = wx.FindWindowByName(named)

        repl_list = [('"', 'in'), ("'", 'ft')]
        for start, finish in repl_list:
            if re.search(start, raw_value, re.I):
                raw_value = re.sub(start, finish, raw_value)
                

        new_value = raw_value
        if 'combobox' in named:
            edit_ctrl.SetValue(new_value)
        if 'txtctrl' in named:
            edit_ctrl.ChangeValue(new_value)

    




class PrintOps(object):
    '''Print Operations.'''

    def __init__(self, debug=False):
        '''Initialize Variables.'''
        


    def printLast(debug=False):
        ''' Print Last Sale via Last Transaction Number'''
        
        # query = 'SELECT trans_num FROM transaction_control'
        # data = ''
        # returnd = SQConnect(query, data).ONE()
        returnd = LookupDB('transaction_control').General('trans_num')
        print(('print last : {}'.format(returnd[0])))
        pretransNum = int(returnd[0]) - 1
        transNum = str(pretransNum).zfill(7)
                
        print(('TransNum : {} {}'.format(transNum, transNum)))
        # query = 'SELECT cust_num, address_acct_num, type_of_transaction, date, time FROM transactions WHERE transaction_id = (?) LIMIT 1'
        # data = (transNum,)
        # returnd = SQConnect(query, data).ONE()
        
        returnd = LookupDB('transactions').Specific(transNum, 'transaction_id', 'cust_num, address_acct_num, type_of_transaction, date, time', limit=1)

        stationNum = 1
        drawer = 1
        # print(('_-_-_ Returnd : ',returnd))
        (custNum, addrNum, transType, dated, timed) = returnd
        # print(('Dated : ',dated))
        # print(('Timed : ',timed))
        
        # query = 'SELECT upc, quantity, description, unit_price, total_price, discount FROM transactions WHERE transaction_id = ?'
        # data = (transNum,)
        # tickie = SQConnect(query, data).ALL()
        tickie = LookupDB('transactions').Specific(transNum, 'transaction_id','upc, quantity, description, unit_price, total_price, discount')
        print(('tickie : ',tickie))
        
        # query = 'SELECT paid, total_price, cust_num, address_acct_num, pay_method, tax FROM transaction_payments WHERE transaction_id = ?'  
        # data = (transNum,)
        # tickiePaid = SQConnect(query, data).ONE()
        tickiePaid = LookupDB('transaction_payments')(transNum, 'transaction_id', 'paid, total_price, cust_num, address_acct_num, pay_method, tax')
        print(('tickiePaid : ',tickiePaid))
        
        (paid, totald, custNum, addrNum, pay_method, taxd) = tickiePaid  
        
        chg = paid - totald
        if chg == 0:
            chg = ''
        
        # query = 'SELECT paid, card5_payment, cash_payment, card2_payment, card3_payment, card1_payment, card4_payment, debit_payment, check_payment, charge FROM transaction_payments WHERE transaction_id = ?;'
        # data = (transNum,)
        # returnd = SQConnect(query,data).ONE()
        fields = 'paid, card5_payment, cash_payment, card2_payment, card3_payment, card1_payment, card4_payment, debit_payment, check_payment, charge'
        returnd = LookupDB('transaction_payments').Specific(transNum, 'transaction_id',fields)
        (paidd, crd5, cash, crd2, crd3, crd1, crd4, deb, chk, chrg) = returnd
        
        payment_type = {'paid': paidd, 'credit5': crd5, 'cash': cash, 'credit2': crd2, 'credit3': crd3, 'charge': 0.0, 'credit1': crd1, 'credit4': crd4, 'debit': deb, 'check': chk}
        
        #addr = CheckPrinterDefs()
        #print 'addr : ',addr
                
        try:
            print(('transNum : ',transNum))
            print(('transType :',transType))
            print(('stationNum : ',stationNum))
            print(('drawer : ',drawer))
            print(('dated : ',dated))
            print(('timed : ',timed))
            receipt = PRx.TransactionReceiptPrinted(transNum, transType, stationNum, drawer, dated, timed, reprint=True)
            usb = True
        except:
            
            usb = False        
        
        if usb is not False:
            receipt.Header(custNum=custNum,addrNum=addrNum)
            transCnt = len(tickie)
            if transCnt > 0:
                totalqty = 0
                subtotald = 0
                
                
                for idx in range(transCnt):
                    qty = tickie[idx][1]
                    desc = tickie[idx][2]
                    totalprice = tickie[idx][4]
                    eachprice = tickie[idx][3]
                    upc = tickie[idx][0]
                    receipt.TransactionLine(idx, upc, qty, desc, totalprice)
                    totalqty += Decimal(qty)
                    subtotald += totalprice
                    
                receipt.SubTotal(totalqty, subtotald, taxd, totald)
                receipt.Change(paid, payment_type, chg)
                receipt.FinishPrint()
    


# def CustPenaltyCheck(custNum):
#     query = 'SELECT last_avail_credit FROM customer_penalty_info WHERE cust_num=(?)'
#     data = [custNum,]
#     returnd = SQConnect(query, data).ONE()
#     limit = 0
#     if returnd is not None and returnd > 0:
#         limit = returnd[0]
        
#     
#     return limit
        
# def CheckCredit(custNum):
#     query = 'SELECT credit_limit FROM customer_accts_receivable WHERE cust_num=(?)'
#     data = [custNum,]
#     returnd = SQConnect(query,data).ONE()
#     climit = 0
#     if returnd[0] is not None and returnd[0] > 0:
#         climit = returnd[0]
    
#     penalty_limit = CustPenaltyCheck(custNum)
    
#     if penalty_limit is not None and penalty_limit > 0:
#         climit = penalty_limit
    
#     return climit    
            
################### OBJECTS ########################
class transAction(object):
    """
    This Object keeps track of all the items & their properties.
    Comparing the latest to all previous items, inorder to join with previous items
    to make the inventory & transaction entries easier to manipulate later.

    Transaction Data Variable layout:
        self.transData = {"Sale":
                            {transaction_number:
                                {"UPC":
                                    {"Desc":"example Description","Qty":"1","Cost":"0.00","setRTL":"0.00","RTL_dict":{"1":"0.00"},"Discount":"0%", "Taxable":True}
                                }
                            }
                        "Return":
                            {transaction_number:
                                {"UPC":
                                    {""Desc":"example Description","Qty":"1","Cost":"0.00","RTL":"0.00","Discount":"0%", "Taxable":True}
                            }
                        }
    """    
    def __init__(self, transGridname, debug=False):
        self.transGrid = wx.FindWindowByName(transGridname)
        self.transData = {}
        

    def Add(self,newitem):
        pass

    def Compare(self):
        pass

    def Joinr(self):
        pass

    def Pull(self): 
        pass

    def Push(self):
        pass

    


# class TableAware(object):
#     def __init__(self, table_name, sql_file=None, dbtype='mysql'):
#         self.table_name = table_name
#         self.sql_file = sql_file
#         self.dbtype = dbtype.lower()
#         self.table_list = None
    
#     def CheckTable(self):
#         print(f'** Table Check : {self.table_name} : ')
#         if self.dbtype == 'mysql':
#             returnd = LookupDB(self.table_name).is_table()
#             #print(f'(( ** returnd : {returnd}')
#             addTable = False
#             if returnd is None:
#                 print('\r Adding...')
#                 addTable = True
#         return addTable 

#     def CheckFieldName(self, fieldname):
#         print(f'\t Field Name Check : {fieldname}')
#         self.CheckTable()
#         if self.dbtype == 'mysql':
#             returnd = LookupDB(self.table_name).is_field(fieldname)
#             addcolumn = False
#             if returnd is None:
#                 addcolumn = True
            
#             return addcolumn
    
#     def CompareField(self, fieldname, defn):
#         self.table_list = LookupDB(self.table_name).DescribeTable()
#         pout.v(self.table_name, self.table_list)
#         if self.table_list is not None:
#             tb = len(self.table_list)
#             for cnt in range(0, tb):
#                 if self.table_list[cnt]['field'] == fieldname:
#                     print(f"{self.table_list[cnt]['field']} == {fieldname}")
#                     if self.table_list[cnt]['type'] != defn:
#                         print('Drop Field : {}'.format(fieldname))
#                         # self.DropField(fieldname)
#             time.sleep(3)        

#     def CreateTable(self, fieldname, defn):
#         query = 'CREATE TABLE {} ({} {})'.format(self.table_name, fieldname, defn) 
#         print(f' ** Create Table : query : {query}')
#         data = []
#         returnd = SQConnect(query, data).ONE()

    
#     def CheckDBType(self):
#         pass

#     def SortDefn(self, defn):
#         primary_key = defn['primary_key']
#         defaults = defn['defaults']
#         del defn['primary_key']
#         del defn['defaults']
#         coldefn = ''
#         for key, value in defn.items():
#             if value is not None:
#                 if key in ['date', 'bool', 'text', 'time']:
#                     coldefn = '{}'.format(key)
#                 elif key in ['decimal']:
#                     coldefn = '{}'.format(key)
#                 else:
#                     coldefn = '{}({})'.format(key, value)
#         typed = coldefn        
#         if primary_key is not False:
#             coldefn += ' PRIMARY KEY'
#         if defaults is not None:
#             coldefn += ' DEFAULT {}'.format(defaults)
        
#         return coldefn, typed

#     def AddField(self, fieldname, char=None, varchar=None, integer=None, text=None, date=None, bool=None, time=None, decimal=None, primary_key=False, defaults=None):
#         addTable = self.CheckTable()
#         defn = {'char':char, 'varchar':varchar, 'int':integer, 'text':text, 'date':date, 'bool':bool, 'time':time, 'decimal':decimal, 'primary_key':primary_key, 'defaults':defaults}
#         col_defn, justtypd = self.SortDefn(defn)
#         print(f'Column Definitions : {col_defn}, {justtypd}')
#         self.CompareField(fieldname, justtypd)
#         if addTable is True:
#             self.CreateTable(fieldname, col_defn)
#         chkfield = self.CheckFieldName(fieldname)
#         if chkfield is True:
#             query = 'ALTER TABLE {} ADD COLUMN {} {}'.format(self.table_name, fieldname, col_defn)
#             print(f'++ ALTER TABLE : ADD COLUMN : {query}')
#             data = []
#             returnd = SQConnect(query, data).ONE()

#     def DropField(self, fieldname):
#         addTable = self.CheckTable()
#         if addTable is True:
#             print('Table does not Exist')
#         else:
#             query = 'ALTER TABLE {} DROP {}'.format(self.table_name, fieldname)
#             print(f'-- ALTER TABLE : DROP COLUMN : {query}')
#             data = []
#             returnd = SQConnect(query, data).ONE()

#     def CheckEntries(self):
#         query = 'SELECT COUNT(*) FROM {}'.format(self.table_name)
#         data = ''
#         returnd = SQConnect(query, data).ONE()
#         return returnd

#     def CreateTestItem(self, fieldnames, values, extra=None):
#         returnd = self.CheckEntries()
#         if returnd[0] == 0 or extra is not None:
#             fn = fieldnames.split(",")
#             val = values.split(",")
#             pout.v(f'FieldNames : {fn} ; Values : {val}')
#             chkexist = LookupDB(self.table_name).Count(val[0].strip("'"), fn[0].strip("'"))
#             if chkexist == 0:
#                 print(f'Creating Test Item for {self.table_name}')
#                 query = f"INSERT INTO {self.table_name} ({fieldnames}) VALUES ({values});"
#                 print(f'$$ -- Create Test Item : query : {query}')
#                 data = ''
#                 SQConnect(query,data).ONE()    
        



# class TableAware(object):
#     def __init__(self, sql_file, table_info, debug=False):
#         self.sql_file = sql_file
#         self.table_name = table_info['table_name']
#         self.column_info = column_info
#         self.primary_key = primary_key
#         self.default = default

#     def Run(self):
#         self.Check()

#     def Check(self):
#         tableCheck = self.TableCheck()
#         if tableCheck == 1:
#             fieldCheck = self.FieldCheck()
#         else:
#             pout.v('Table Not Found')
        
            

#     def TableCheck(self):
#         pout.b(f'Table Check : {self.table_name}')
#         query = '''SELECT * FROM information_schema.COLUMNS 
#                    WHERE TABLE_SCHEMA = 'rhp' 
#                    AND TABLE_NAME = "{}"
#                 '''.format(self.table_name)
#         data = []
#         returnd = SQConnect(query, data).ALL()
#         if returnd is None:
#             self.Create()
            
#             return 0
        
#         return 1

#     def FieldCheck(self):
#         query = 'DESCRIBE {};'.format(self.table_name)
#         data = []
#         returnd = SQConnect(query, data).ALL()
#         #pout.v(f'tableName : {self.table_name} ; returnd : {returnd}')
        
#         cur_cols = {}
#         for item in returnd:
#             named, data, na, pk, na2, ex = item
#             cur_cols[named] = {'data':data, 'Empty':na, 'Primary':pk, 'Default':na2, 'Extra':ex}
        
#         pout.v(cur_cols)
        
#         for fieldname, typdata in self.column_info:
#             print(f'Field : {fieldname}')
#             if not fieldname in cur_cols:
#                 print('\tNot Found. Adding...')
#                 try:
#                     self.DropColumn(fieldname)
#                 except:
#                     print('Tried Drop first, JUST in Case')
                
#                 self.AddColumn(fieldname, typdata)
                
#             else:
#                 print('\tFound. Checking Types...')
#                 jda = typdata
#                 newprimkey = False
#                 oldprimkey = False
#                 newdef = False
#                 olddef = False
                
#                 if self.primary_key is True:
#                     newprimkey = True
                
#                 if self.default is not None:
#                     newdef = True
                
                
#                 if cur_cols[fieldname]['Default'] is not None:
#                     olddef = True

#                 if cur_cols[fieldname]['Primary'] == 'PRI':
#                     oldprimkey = True

#                 oldata = cur_cols[fieldname]['data'].rstrip()

#                 if jda.strip() == oldata.strip() and newprimkey == oldprimkey and newdef == olddef:
#                     print('\t\tTypes Match. \n\t\t\t{} == {}'.format(jda, oldata))
#                     print('\t\t\tPrimary Key : {} ++ {}'.format(newprimkey, oldprimkey))
#                     print('\t\t\tDefault : {} ++ {}'.format(newdef, olddef))
#                 else:
#                     if jda.strip() != oldata.strip():
#                         print(f"\t\tTypes MisMatch. \n\t\t\t{jda} != {oldata}")
#                     if newprimkey != oldprimkey:
#                         print('\t\t\tPrimary Key : {} != {}'.format(newprimkey, oldprimkey))
#                     if newdef != olddef:
#                         print('\t\t\tDefault : {} != {}'.format(newdef, olddef))
#                     self.DropColumn(fieldname)
#                     self.AddColumn(fieldname, typdata)
                    
            
            
#         pout.b()
#     def AddColumn(self, fieldname, typdata):
#         print('\t\t\t!ADD {} ({})'.format(fieldname, typdata))
#         pks = re.search('primary.key',typdata,re.I)
#         ndata = typdata
#         primdata = None
#         print(pks)
#         if pks:
#             try:
#                 query = 'ALTER TABLE {} DROP PRIMARY KEY'.format(self.table_name)
#                 returnd = SQConnect(query,[]).ONE()
#             except:
#                 pout.v('NO Primary Key')
#             ndata = typdata.replace(pks[0], '').strip()
#             primdata = 'ALTER TABLE {} ADD PRIMARY KEY({});'.format(self.table_name, fieldname)
#             ndata += ' NOT NULL'

#             pout.v(f'primdata : {primdata}')
        
#         pout.v(f'NDATA : {ndata}')
#         query = 'ALTER TABLE {} ADD COLUMN {} {};'.format(self.table_name, fieldname, ndata)
#         data = []
#         pout.v(f'Add fieldName : {query}')
#         returnd = SQConnect(query, data).ONE()
#         if primdata is not None:
#             pout.v(f'PRIMData : {primdata}')
#             returnd = SQConnect(primdata, data).ONE()

#     def DropColumn(self, fieldname):
#         print('\t\t\t!DROP {}'.format(fieldname))
#         query = 'ALTER TABLE {} DROP {};'.format(self.table_name, fieldname)
#         data = []
#         returnd = SQConnect(query, data).ONE()

#     def Create(self):
#         con = None
#         exists = None
#         con = MySQLdb.connect(host="localhost",
#                               user="rhp",
#                               passwd="password",
#                               db="rhp") #sql_file
        
#         with con:
#             cur = con.cursor()
    
#             cur.execute("SELECT * FROM information_schema.tables WHERE table_schema = 'rhp' AND table_name = '{0}' LIMIT 1;".format(self.table_name))
#             exists = cur.fetchone()
#             print("Fetch Catch : ")
#             if not exists:
#                 print("Does Not Exist; Creating...")
#                 cols = ''
#                 for fst in self.column_info:
#                     cols += '{} {}, '.format(fst[0], fst[1])
#                 cols = cols.strip(' ').strip(',')
#                 pout.v(cols)
#                 cur.execute("CREATE TABLE {0} ({1});".format(self.table_name, cols))
#             else:
#                 print("Table '{}' Exists".format(self.table_name))
    
    
#     def CheckEntries(self):
#         query = 'SELECT COUNT(*) FROM {}'.format(self.table_name)
#         data = ''
#         returnd = SQConnect(query, data).ONE()
#         return returnd

#     def CreateTestItem(self, fieldnames, values):
#         print(f'Creating Test Item for {self.table_name}')
#         query = f"INSERT INTO {self.table_name} ({fieldnames}) VALUES ({values});"
#         data = ''
#         SQConnect(query,data).ONE()


class RetailPrice(object):
    def __init__(self, upc, custNum, qty, debug=False):
        
        self.upc = upc
        self.custNum = custNum
        self.qty = qty
        self.priced_dict = {'Price':0,'Options':[0,0,0],'nTx': False, 'Note':''}
        # Price : $0.00
        # Options : [3/0.00, 10%, 0]
        # nTx : True/False
        
        
    def CheckTaxExempt(self):
        pass
        
    def CheckRetail(self):
        pass
    
    def CheckTaxHoliday(self):
        pass
    
    def CheckCustDiscount(self):
        pass
    
    def WriteLine(self):
        pass
        
    def Get(self):
        pass
      
      
        
    
class InvMan(object):
    def __init__(self, lookup=None, debug=False):
        self.lookup = lookup
        self.item_model = {}
        # 'upc':0, 'desc':0, 'retails':0
        

    def Run(self):
        count_returnd = LookupDB('item_detailed').Count(self.lookup, 'upc')
        #pout.v('Count_Returnd : {}'.format(count_returnd))
        item_cnt = VarOps().DeTupler(count_returnd)
                  
        if item_cnt == 1:
            fields = 'upc'
            returnd = LookupDB('item_detailed').Specific(self.lookup, 'upc',fields)
            #pout.v(f'1 Item Found : {returnd}')
            self.Set(returnd[0])
        elif item_cnt == 0 and len(self.lookup) < 3:
            return None        
        elif item_cnt == 0 and len(self.lookup) >= 3:              
            queryWhere = QueryOps().ANDSearch(['upc','description','part_num',
                                               'oempart_num','altlookup'],
                                               self.lookup)

            queryData = []
                    
            query = '''SELECT count(upc),upc FROM item_detailed WHERE {0};'''.format(queryWhere)
            count_returnd = SQConnect(query,queryData).ONE()
            
            upcd = count_returnd[1]
            #pout.v(f"Count Returnd : {count_returnd}")
            
            item_cnt = VarOps().DeTupler(count_returnd[0])
            #pout.v(f'item_cnt : {item_cnt}')
            if item_cnt == 0:
                return None

            elif item_cnt == 1:
                self.Set(upcd)

            elif item_cnt > 1:
                defFrame = wx.DEFAULT_FRAME_STYLE
                style = defFrame & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
                ItemLookupD = ItemLookupDialog(None,
                                               title="Item Lookup",
                                               itemNumber=self.lookup,
                                               size=(1000,800),
                                               style=style)

                ItemLookupD.ShowModal()
                print("-!-" * 40)
                try:
                    self.itempick = ItemLookupD.itemPicked
                    ItemLookupD.Destroy()

                except:
                    self.itempick = ''
                    ItemLookupD.Destroy()
                    return None
                
                self.Set(self.itempick)
        
        return self.item_model        
                
    def Set(self,upc):
        self.item_model['upc'] = upc
        self.item_model['retails'] = self.GetPriceTree(upc)
        desc, cost = self.GetID(upc)
        self.item_model['desc'] =  desc
        self.item_model['cost'] = cost
        self.item_model['do_not_discount'] = self.GetDND(upc)
        self.item_model['taxable'] = self.GetTaxes(upc)

    def GetPriceTree(self, upc):
        price = RetailOps().RetailSifting(upc)
        pout.v('InvMan -> GetPriceTree : {}'.format(price))
        return price
    
    def GetID(self, upc):
        desc, cost = LookupDB('item_detailed').Specific(upc, 'upc','description, avg_cost')
        return desc, cost

    def GetDND(self, upc):
        dnd = LookupDB('item_detailed2').Specific(upc, 'upc', 'do_not_discount')
        pout.v(f'InvMan -> DND : {dnd}')

        return dnd
    def GetTaxes(self, upc):
        taxes = tax1, tax2, tax3, tax4, taxnever = LookupDB('item_detailed2').Specific(upc, 'upc', 'tax1, tax2, tax3, tax4, tax_never')
        taxable = True
        for tx in taxes:
            if tx == 1:
                taxable = False
            
        return taxable



class CustomerManagement(object):
    def __init__(self, custNum, debug=False):
        self.custNum = custNum
        

    def LookupDB(self,getType,fromtable,fields_to_return):
        ''' itemNumber = could be item upc or customer acct_num whatever is the Primary Key
            getType = is the field name of the Primary Key
            fromtable = from Table Who knows, hopefully you do
            field_to_return = a string such as this 'description,retails' or whatever you want'''
    
        if getType is None or getType == '':
            query = 'SELECT {0} FROM {1}'.format(fields_to_return, fromtable)
            data = ''
        else:
            query = 'SELECT {0} FROM {1} WHERE {2}=(?)'.format(fields_to_return,
                                                               fromtable,getType)
            data = (self.custNum,)
        
        returnd = SQConnect(query, data).ONE()
    
        return returnd        


    def SearchCount(self):
        queryWhere = 'cust_num LIKE (?) OR last_name LIKE (?) OR first_name LIKE (?)'
        queryData = (self.custNum,self.custNum,self.custNum,)
        #qD = HU.MaskData(queryWhere, queryData)
        count_returnd = QueryOps().QueryCheck('customer_basic_info',queryWhere,queryData)
        
        
        return count_returnd               
            

        
    
        

class CurrentNotes(object):
    def __init__(self,trans_id='CURRENT', debug=False):
        """ Set, Get, & Clear Notes for Current Transaction """
        self.station_num = GetStation()
        self.trans_id = trans_id
        

    def TempSet(self,linePos, notes):
        query = '''INSERT INTO transaction_notes (station_num, transaction_id, 
                                                  line_position, note) 
               VALUES (?,?,?,?)'''
        
        data = (self.station_num, self.trans_id, linePos, notes) 
        returnd = SQConnect(query, data).ONE()
        
    def PermSet(self,trans_id):
        new_id = trans_id
        query = '''UPDATE TABLE transaction_notes SET transaction_id=(?) WHERE transaction_id=(?)'''
        data = (new_id, self.trans_id)        
        returnd = SQConnect(query, data).ONE()
        

    def Clear(self):
        RecordOps(['transaction_notes']).DeleteEntryRecord('transaction_id','CURRENT')
        
                  
class SetAcctInfo(object):
    def __init__(self, acctInfoName, debug=False):
        """ Acct Info refers to the name of the AcctInfo Static Text """
        
        
        self.acctNum = None
        self.addrAcctNum = None
        self.fullName = None
        self.address1 = None
        self.address2 = None
        self.csz = None
        self.discount = None
        self.availCredit = None
        self.acctInfoName = acctInfoName

    def custAcctNum(self, acctNum=None):
        
        self.acctNum = acctNum
        self.UpdateSetAcctInfo()
        
    def addressAcctNum(self, addrAcctNum):
        
        
        self.addrAcctNum(self, addrAcctNum)
        self.UpdateSetAcctInfo()
            
    def name(self, firstName, lastName=None):
        
        
        self.fullName = firstName
        if lastName is not None:
            self.fullName = '{} {}'.format(firstName, lastName)
        
        self.UpdateSetAcctInfo()
        
    def address(self, addr0, addr1=None, addr2=None, unit=None, debug=False):
        
        if unit == '':
            unit = None
        
        
        self.address1 = addr0
        if addr1 is not None:
            if re.search('unit',addr1, re.I):
                self.address1 = '{}  {}'.format(addr0, addr1)
                
            self.address2 = addr1
        if addr2 is not None:
            if re.search('unit',addr2, re.I):
                self.address2 = '{}  {}'.format(addr1, addr2)
        
        if unit is not None:
            self.address1 = '{} UNIT {}'.format(addr0,unit)
            if re.search('unit', unit, re.I):
                self.address1 = '{} {}'.format(addr0, unit)
               
        self.UpdateSetAcctInfo()

        
    def cistzi(self, cityd, stated=None, zipd=None):
        
        
        self.csz = '{}, {}  {}'.format(cityd, stated, zipd)
        if stated is None:
            self.csz = cityd
            
        self.UpdateSetAcctInfo()

    def discountd(self, fixdiscount='0', discount=None):
        
        
        if fixdiscount == '0':
            discount = None
        
        discount = str(discount)
        if discount is not None:
            if not '%' in discount:
                discount = '{}%'.format(discount)
        
        self.discount = discount
        
        self.UpdateSetAcctInfo()
        

    def availCredit(self, availCredit=None):
        
        
        self.availCredit = availCredit    
        self.UpdateSetAcctInfo()
        
    def UpdateSetAcctInfo(self):
        
        
        grid = wx.FindWindowByName(self.acctInfoName)
        
        typefind = str(type(grid))
        if re.search('grid',typefind, re.I):
            
            listing = [('Account Number',self.acctNum),
                       ('Address Account',self.addrAcctNum),
                       ('Name',self.fullName),
                       ('Address 1',self.address1),
                       ('Address 2', self.address2),
                       ('City, State, Zip',self.csz),
                       ('A/R/Avail Credit',self.availCredit),
                       ('Discount %',self.discount)]
                   
            rows = grid.GetNumberRows()
            cols = grid.GetNumberCols()
            
            for header, value in listing:
                for row in range(rows):
                    label = grid.GetRowLabelValue(row)
                    if label == header:
                        if value is not None:
                            grid.SetCellValue(row, cols-1, str(value))        
        
        else:
            acctInfo = '{ad}\n{cs}'.format(ad=self.address0,
                                           cs=self.csz)

            wx.FindWindowByName(self.acctInfoName).GetCtrl( acctInfo)


        
class Splash(object): #wx.SplashScreen
    def __init__(self, parent=None, id=-1, debug=False):
        
        basePath = os.path.dirname(os.path.realpath(__file__)) + '/'
        image = basePath + "loading.gif"
        aBitmap = wx.Image(name=image).ConvertToBitmap()
        splashStyle = wx.SPLASH_CENTRE_ON_PARENT
        splashDuration = 0  # milliseconds
        wx.SplashScreen.__init__(self, aBitmap, splashStyle,
                                 splashDuration, parent)
        #self.SetName('splash_loading')

        gif = wx.animate.GIFAnimationCtrl(self, -1, image,)

        self.Show()
        self.gif = gif

    def Run(self):
        self.gif.Play()

    def Stop(self):
        self.gif.Hide()
        self.gif.Destroy()


#----- TaxIt
class TaxIt(object):
    def __init__(self, itemNumber, qty, debug=False):
        self.itemNumber = itemNumber.upper().strip()
        self.qty = qty
        

    def Check(self):
        tax_qualify_list = [('tax1, tax2, tax3, tax4, tax_never',
                             'item_detailed2', 'tax_returnd'),
                            ('category', 'item_options', 'bulk_returnd')]
        for field, table, varib in tax_qualify_list:
            query = 'SELECT {0} FROM {1} WHERE upc=(?)'.format(field, table)
            data = (self.itemNumber,)
            setattr(self, varib, SQConnect(query, data).ALL())

        
        try:
            (tax1, tax2, tax3, tax4, tax_never) = self.tax_returnd[0]
        except:
            tax1, tax2, tax3, tax4, tax_never = '', '', '', '', ''

        categoryd = self.bulk_returnd[0]

        if tax_never is True:
            self.taxExempt = 'yes'
        else:
            self.taxExempt = 'no'

        return self.taxExempt


#----- Pricing
class Pricing(object):
    def __init__(self, name, scheme_List, reduceBy, avgCost, margin, currPrice):
        self.name = name
        self.schemeList = scheme_List
        self.reduceBy = reduceBy
        self.avgCost = avgCost
        self.margin = margin
        self.currPrice = currPrice

    def Scheme(self):
        getAvgCost = Decimal(self.avgCost)
        startingMargin = Decimal(self.margin)
        #if startingMargin < 11:
        #    startingMargin = Decimal('40')

        if getAvgCost > 0:
            level = 0
            reducingby = self.reduceBy
            Scheme_List = self.schemeList
            NextMargin = startingMargin
            priceScheme_dict = {}
            
            VarOps().GetTyped(reducingby)
            if '-' in reducingby:
                reduced_list = reducingby.split('-')
            else:
                reduced_list = []
                reduced_list.append(reducingby)
                print(reduced_list)
            VarOps().GetTyped(reduced_list)
            for idx, unit in enumerate(Scheme_List):
                if NextMargin < 1:
                    NextMargin = Decimal('1')
                calcMargin = 100 - NextMargin

                Pricd = RetailOps().DoMargin(getAvgCost, calcMargin, unit)
                NextPrice = str(RetailOps().DoRound(Pricd, '.01'))
                Margind = str(RetailOps().DoRound(NextMargin, '.001'))
                LabelKey = unit

                priceScheme_dict[LabelKey] = (NextPrice, Margind)
                
                NextMargin -= Decimal(VarOps().DeTupler(reduced_list[level]))
                if level < len(reduced_list) - 1:
                    level += 1

        return priceScheme_dict


#----- Transactions
class Transaction2(object):
    def __init__(self, transNum=None, debug=False):
        """
    This Object keeps track of all the items & their properties.
    Comparing the latest to all previous items, inorder to join with previous items
    to make the inventory & transaction entries easier to manipulate later.

    Transaction Data Variable layout:
        self.transData = {"Sale":
                            {transaction_number:
                                {"UPC":
                                    {"Desc":"example Description","Qty":"1","Cost":"0.00","setRTL":"0.00","RTL_dict":{"1":"0.00"},"Discount":"0%", "Taxable":True}
                                }
                            }
                        "Return":
                            {transaction_number:
                                {"UPC":
                                    {""Desc":"example Description","Qty":"1","Cost":"0.00","RTL":"0.00","Discount":"0%", "Taxable":True}
                            }
                        }
    """    
        self.balance = Decimal(0)
        self.Total = Decimal(0)
        self.subTotal = Decimal(0)
        self.tax_balance = Decimal(0)
        if transNum is None:
            self.transNum = self.TransNumAuto()
            
                
    def TransNumAuto(self, fill0s=7, debug=False):
        query = 'SELECT trans_num FROM transaction_control WHERE abuser="rhp";'
        data = ''
        returnd = SQConnect(query, data).ONE()
        
        if returnd[0]:
            transNum = str(returnd[0]).zfill(fill0s)
        
        query = 'INSERT INTO transactions (transaction_id, type_of_transaction) VALUES (?, ?)'
        data = [self.transNum, 'VOID']
        returnd = SQConnect(query,data).ALL()
        # print(('INSERT into returnd : {}'.format(returnd)))
            
        query = 'UPDATE transaction_control SET trans_num=trans_num+1 WHERE abuser="rhp";'
        data = ''
        returnd = SQConnect(query, data).ONE()
        
        return transNum

    #def Add(self, upc, qty, price):
        
    
            
        
            
class Transaction(object):
    def __init__(self,transNum=None, debug=False):
        """
    This Object keeps track of all the items & their properties.
    Comparing the latest to all previous items, inorder to join with previous items
    to make the inventory & transaction entries easier to manipulate later.

    Transaction Data Dictionary layout:
        self.transData = {"Sale":
                            {"transaction_number":
                                {"UPC":
                                    {"Desc":"example Description","Qty":"1","Cost":"0.00","setRTL":"0.00","RTL_dict":{"1":"0.00"},"Discount":"0%", "Taxable":True}
                                }
                            }
                        "Return":
                            {"transaction_number":
                                {"UPC":
                                    {""Desc":"example Description","Qty":"1","Cost":"0.00","RTL":"0.00","Discount":"0%", "Taxable":True}
                            }
                        }
    """    
        self.balance = Decimal(0)
        self.Total = Decimal(0)
        self.tax_balance = Decimal(0)
     
        fields = 'RNDscheme,no_pennies_rounding'
        (self.noPennies, self.RNDtype) = LookupDB('tax_tables').Specific('TAX','tax_name',fields)   
    
    def Clear(self):
        print("Transactions Clear")
        self.Total = Decimal(0)
        self.tax_balance = Decimal(0)
        self.balance = Decimal(0)
        
    def AddAll(self, d):
        print("Transactions Add ALL ")
        maxd = len(d)
        for key in range(maxd):
            current_price = self.Add(d[key][4],d[key][6],'no')
            self.Be_Current(current_price)
        if maxd == 0:
            current_price = 0
            self.Be_Current(0)
        
    def Add(self, add_price, taxed, override):
        self.add_price = add_price
        self.balance += Decimal(self.add_price)
        if taxed is True or taxed == 'Tx':
            self.tax_balance += Decimal(self.add_price) * Decimal(GetTaxRate(self.add_price))

        return self.balance

    def Subtract(self, subtract_price, taxed, override):
        self.subtract_price = subtract_price
        self.balance -= Decimal(self.subtract_price)
        if override == 'no':
            if self.balance <= 0:
                self.balance = Decimal('0.00')

        if taxed is True or taxed == 1 or taxed == 'Tx':
            subprice = Decimal(self.subtract_price)
            taxrate = Decimal(GetTaxRate(self.subtract_price))
            self.tax_balance -= Decimal(subprice) * Decimal(taxrate)
        return self.balance

    def Taxes(self):
        #tax_figured = Decimal(self.balance) * Decimal(self.TaxRate)
        self.tax_time = RoundIt(self.tax_balance, '1.00')
        return self.tax_time

    def Totaled(self):
        Total = Decimal(self.balance) + Decimal(self.tax_time)
        self.Totald = RoundIt(Total, '1.00')
        
        return self.Totald

    def Be_Current(self, current_price):
        self.current_price = current_price
        
        current_tax = self.Taxes()
        current_total = self.Totaled()
        
        values_set_list = [('pos_subtotal_txtctrl', self.current_price),
                           ('pos_tax_txtctrl', current_tax),
                           ('pos_total_txtctrl', current_total)]
        
        for name, value in values_set_list:
            item = wx.FindWindowByName(name)
            item.SetValue(str(value))

                
            
    


class CustomerChecks(object):
    def __init__(self, custNum=None, debug=False):
        
        self.custNum = None
        if len(custNum) > 0:
            self.custNum = custNum
            
        
    def TaxStatus(self):
        status = True
        if self.custNum is not None:
            fields = 'tax_exempt'
            returnd = LookupDB('customer_sales_options').Specific(self.custNum,'cust_num',fields)
            if returnd[0] == '1':
                status = False
        
        return status
            
    
    def DiscountStatus(self):
        status = False
        discount = 0
        if self.custNum is not None:
            fields = 'fixed_discount, discount_amt'
            returnd = LookupDB('customer_sales_options').Specific(self.custNum, 'cust_num', fields)
            if returnd[0] == '1':
                status = True
                discount = returnd[1]
    
            
        
        return status, discount

    
# class SQConnect(object):
#     def __init__(self, query, data=None, sql_file=None, debug=False):
        
#         self.query = None
#         self.data = None
#         self.use_db = "MySQL" #SQLite
#         self.debug = debug
#         checkTypes = []
#         if self.use_db == "MySQL":
#             #self.sql_file = "host='localhost', user='rhp', passwd='password', db='rhp'"
#             if query is not None:
#                 query = query.replace("?","%s")
            
#             checkTypes = [('query', self.query),
#                           ('data', self.data)]    
        
#         if self.use_db == 'SQLite':
#             self.sql_file = sql_file
#             checkTypes = [('sql_file', self.sql_file),
#                           ('query', self.query),
#                           ('data', self.data)]

        
#             if self.sql_file == None:
#                 chk_list = [('select','FROM'), 
#                             ('update','^UPDATE'), 
#                             ('insert','^INSERT INTO'),
#                             ('delete','FROM')]
#                 for check, pattern in chk_list:
#                     if re.match(check, query, re.I):
#                         patt = '{} ([A-Z_-]+)'.format(pattern)
#                         a = re.search(patt,query,re.I)
#                         tableName = a.group(1)
#                         self.sql_file = FindSQLFile(tableName)
                    
        
#         self.query = query
#         self.data = self.MaskData(query,data)
        
        
#         #for text, vari in checkTypes:
#             #print(f'QueryText {self.query} : Vari {self.data}')
#         returnd = None
#         #self.data = MaskData(self.query, self.data)

#     def ALL(self):
#         con = None
#         if self.use_db == "MySQL":
#             con = MySQLdb.connect(host='localhost', user='rhp', passwd='password', db='rhp')
#         if self.use_db == "SQLite":
#             con = sqlite3.connect(self.sql_file)
        
#         with con.cursor() as cur:
#             #cur = con #.cursor()
#             if len(self.data) > 0:
#                 cur.execute(self.query, self.data)
#             else:
#                 cur.execute(self.query)
                
#             returnd = cur.fetchall()
#             if re.search('(UPDATE|INSERT)', self.query, re.I):
#                 con.commit()

#         return VarOps().CheckJson(returnd)

#     def ONE(self):
#         con = None
#         if self.use_db == "MySQL":
#             con = MySQLdb.connect(host='localhost', user='rhp', passwd='password', db='rhp')
#         if self.use_db == "SQLite":
#             con = sqlite3.connect(self.sql_file)
        
#         with con.cursor() as cur:
#             #cur = con #. cursor()
#             if len(self.data) > 0:
#                 cur.execute(self.query, self.data)
             
#             else:
#                 cur.execute(self.query)
                
        
#             returnd = cur.fetchone()
#             if re.search('(UPDATE|INSERT)', self.query, re.I):
#                 con.commit()
        
#         return VarOps().CheckJson(returnd)

#     def CHECK(self):
#         if re.search('update', self.query, re.I):
#             tab = re.search('update.(.*).set', self. query, re.I)
#         elif re.search('select', self.query, re.I):
#             tab = re.search('where.(.*).set', self.query, re.I)

#         tabld = tab.group(1).strip()
        
#         sql_file = FindSQLFile(tabld)
#         newq = 'SELECT COUNT(*) FROM {0} WHERE upc=(?)'.format(tabld)
#         newdata = self.data[len(self.data) - 1]
        
#         newdatas = (newdata,)
#         returnd = SQConnect(sql_file, newq, newdatas).ONE()
        
#         if returnd[0] >= 1:
#             print(f'Returnd : {returnd[0]}')
           
#         return returnd[0]

#     def UniqueList(self, seq, idfun=None):
#     # order preserving
#         if idfun is None:
#             def idfun(x):
#                 return x
#         seen = {}
#         result = []
#         for item in seq:
#             marker = idfun(item)
#             # in old Python versions:
#             # if seen.has_key(marker)
#             # but in new ones:
#             if marker in seen:
#                 continue
#             seen[marker] = 1
#             result.append(item)
#         return result


#     def MaskData(self, query, data, debug=False):
#         if data is not None or data != '' or len(data) != 0:
#             new_data = []
#             fromquery = []
#             if re.search('SELECT', query, re.I):
#                 if re.search('LIKE', query, re.I):
#                     if re.search('(or|and)', query, re.I):
#                         fromquery = re.split('(or|and)', query, flags=re.IGNORECASE)
#                     else:
#                         fromquery.append(query)
                        
#                     idx = 0
#                     for item in fromquery:
#                         print(f'Item L : {len(fromquery)}')
#                         dat = ''
#                         if re.search('(\?|%s)', item):
#                             if re.search('LIKE',item, re.I):
#                                 if len(data) != 0:
#                                     dat = '%{}%'.format(data[idx])
#                             else:
#                                 print(f'IDX : {idx} ; Data : {data}')
#                                 print(f'FROMQuery : {fromquery}\nItem : {item}')
#                                 dat = '{}'.format(data[idx])
#                             new_data.append(dat)
#                             idx += 1
#                 else:
#                     new_data = data
#             else:
#                 new_data = data

#             typd = str(type(new_data))
#             if 'list' in typd:
                
#                 new_data = tuple(new_data)
                
#         else:
#             pass    
        
#         if len(data) == 0:
#             new_data = ''
        
#         return new_data



# class DBConnect(object):
#     def __init__(self, query, data, debug=False):
        
#         self.query = str(query)
#         self.data = data
#         self.debug = debug
        
        

#     def ALL(self):
#         con = psycopg2.connect("dbname='rhp' user='exc'")
#         cur = con.cursor()
#         try:
#             cur.execute(self.query, self.data)
#         except psycopg2.Error as e:
#             print(f'Error : {e}')    

#         returnd = cur.fetchall()
#         con.commit()
#         con.close()

#         return returnd

#     def ONE(self):
       
#         con = psycopg2.connect("dbname='rhp' user='exc'")
#         cur = con.cursor()
#         try:
#             cur.execute(self.query, self.data)
#         except psycopg2.Error as e:
#             print(f'Error : {e}')    

#         if re.search('(UPDATE|INSERT.INTO|DELETE.FROM)', self.query, re.I):
#             returnd = None
#             con.commit()

#         else:
#             returnd = cur.fetchone()

#         con.close()
        
#         return returnd

#     def CHECK(self):
        
#         if re.search('update', self.query, re.I):
#             tab = re.search('update.(.*).set', self.query, re.I)
#         elif re.search('select', self.query, re.I):
#             tab = re.search('where.(.*).set', self.query, re.I)

#         tabld = tab.group(1).strip()
        
#         newq = 'SELECT COUNT(*) FROM {0} WHERE upc=(?)'.format(tabld)
#         newdata = self.data[len(self.data) - 1]
        
#         newdatas = (newdata,)
#         returnd = DBConnect(newq, newdatas).ONE()

#         return returnd[0]
#         con.commit()
#         cur.close()




# def ANDSearch(whatField, items):

#     cnt = items.count(' ')
#     text = ''

#     if cnt > 0:
#         sp1 = items.split()
#         if 'list' in str(type(whatField)):
#             xx = 0
#             longList = len(whatField) - 1
#             for field in whatField:
#                 if xx > 0:
#                     text += ' OR '

#                 for i in range(len(sp1)):
#                     text += "{0} LIKE '%{1}%'".format(field, sp1[i])
#                     if i < len(sp1) - 1:
#                         text += ' AND '
#                 xx += 1
#         else:
#             for i in range(len(sp1)):
#                 text += "{0} LIKE '%{1}%'".format(whatField, sp1[i])
#                 if i < len(sp1) - 1:
#                     text += ' AND '

#     else:
#         if 'list' in str(type(whatField)):
#             xx = 0
#             for field in whatField:
#                 if xx > 0:
#                     text += ' OR '

#                 text += "{0} LIKE '%{1}%'".format(field, items)
#                 xx += 1
#         else:
#             text = "{0} LIKE '%{1}%'".format(whatField, items)
#     print(("And Search Text : ",text))
#     return text


#-------------------------------------
class GridComboBox(object):
    def __init__(self, event, gridname, comboboxname, debug=False):
        
        
        self.event = event
        self.gridname = gridname
        self.comboBoxname = comboboxname
        
        
        self.grid = wx.FindWindowByName(self.gridname)

    def Make(self):
        comboBox = self.event.GetControl()
        comboBox.SetName(self.comboBoxname)
        comboBox.Bind(wx.EVT_COMBOBOX, self.Selection)
        comboBox.Bind(wx.EVT_TEXT, self.Text)

        for (item, data) in self.grid.list:
            comboBox.Append(item, data)

    def Selection(self, event):
        comboBox = wx.FindWindowByName(self.comboBoxname)
        self.grid.index = comboBox.GetSelection()
        
        

    def Text(self, event):
        comboBox = wx.FindWindowByName(self.comboBoxname)
        self.grid.index = comboBox.GetSelection()
        
        

        event.Skip()

    def Hidden(self, event):
        comboBox = wx.FindWindowByName(self.comboBoxname)
        item = comboBox.GetValue()
        self.grid.index = comboBox.GetCount()
        comboBox.Append(item, self.grid.data)
        self.grid.counter += 1

#--------------------------------------------------------------------------
# class RH_Transaction_Dictionary(dict):
#     def __init__(self,transId=None):
#         self = dict()
#         if transId is None:
#             self.transId = AccountOps().TransNumAuto(fill0s=8)
    
#     def AddSale(self, typd="SALE", key, value):
#         ]
#--------------------------------------------------------------------------
        
class RH_Icon(wx.Button):
    def __init__(self, *args, **kwargs):
        typd = kwargs.pop('icon')
        save = ButtonOps().Icons(typd.lower())
        wx.Button.__init__(self, *args, **kwargs)
        self.SetBitmap(wx.Bitmap(save))

class RH_Button(wx.Button):
    def __init__(self, *args, **kwargs):
        wx.Button.__init__(self, *args, **kwargs) 
        self.listd = None
        self.tableName = None
        self.fieldName = None
        self.DefaultTable = None
        self.DefaultField = None
        self.cnt = 0
        #pout.v(f'Listd : {self.listd} ; CNT : {self.cnt}')
        self.Bind(wx.EVT_BUTTON, self.NextLabel)
        
    def DefaultChoices(self):
        returnd = LookupDB(self.DefaultTable).General(self.DefaultField)
        try:
            self.listd = returnd[0]
        except:
            pout.v(returnd)

    def NextLabel(self, evt):
        obj = evt.GetEventObject()
        if self.listd is not None:
            maxd = len(self.listd)
            self.SetLabel(self.listd[self.cnt])
            self.cnt += 1
            if self.cnt >= maxd:
                self.cnt = 0
        
    def OnSave(self, whereField, whereValue):
        a = self.GetLabel()
        try:
            returnd = LookupDB(self.tableName).UpdateSingle(self.fieldName, a, whereField, whereValue)
        except:
            pout.v(f'Table : {self.tableName} ; Field : {self.fieldName} ; WhereField : {whereField} ; whereValue: {whereValue}')
    
    def OnLoad(self, whereField, whereValue):
        returnd = LookupDB(self.tableName).Specific(whereValue, whereField, self.fieldName)
        a = VarOps().GetTyped(returnd)
        if 'tuple' in a:
            returnd = returnd[0]
        if returnd is None:
            returnd = ''
        try:
            self.SetLabel(returnd)
        except TypeError as e:
            pout.v(e)

    def GetCtrl(self):
        return self.GetLabel()

    def SetCtrl(self, value):
        self.SetLabel(value)

    def Clear(self):
        a = ''
        self.SetLabel('')


#--------------------------------------------------------------------------

# class RH_Button(wx.Button):
#     def __init__(self, *args, **kwargs): #name, label, size, hdlr):
#         wx.Button.__init__(self, *args, **kwargs)
#         self.hdlr = kwargs.pop('hdlr')
#         self.Binder()

#     def Binder(self, hdlr):
#         self.Bind(wx.EVT_BUTTON, self.hdlr)

#     def OnSave(self, tableName, fieldName, whereField, whereKey):
#         a = self.GetLabel()
#         try:
#             returnd = LookupDB(tableName).UpdateSingle(fieldName, a, whereField, whereKey)
#         except:
#             pout.v(f'Table : {tableName} ; Field : {fieldName} ; WhereField : {whereField} ; whereValue: {whereKey}')


#
    

#---------------------------------------------------------------------------------------
class RH_LoadSaveSelection(object):
    def __init__(self, *args, **kwargs):
        self.tableName = None
        self.fieldName = None

    def OnLoad(self, whereField, whereValue):
        returnd = LookupDB(self.tableName).Specific(whereValue, whereField, self.fieldName)
        a = VarOps().GetTyped(returnd)
        if 'tuple' in a:
            returnd = returnd[0]
        if returnd is None:
            returnd = 0
        try:
            self.SetSelection(returnd)
        except TypeError as e:
            pout.v(e)

    def OnSave(self, whereField, whereValue):
        a = self.GetSelection()
        try:
            returnd = LookupDB(self.tableName).UpdateSingle(self.fieldName, a, whereField, whereValue)
        except:
            pout.v(f'Table : {self.tableName} ; Field : {self.fieldName} ; WhereField : {whereField} ; whereValue: {whereValue}')

    def GetCtrl(self):
        return self.GetSelection()

    def SetCtrl(self, value):
        self.SetSelection(value)

    def Clear(self):
        self.SetSelection(0)
#---------------------------------------------------------------------------------------
class RH_LoadSaveNum(object):
    def __init__(self, *args, **kwargs):
        self.tableName = None
        self.fieldName = None

    def OnLoad(self, whereField, whereValue):
        returnd = LookupDB(self.tableName).Specific(whereValue, whereField, self.fieldName)
        a = VarOps().GetTyped(returnd)
        #pout.v(a)
        if 'tuple' in a:
            returnd = returnd[0]
            #pout.v('Tuple Unwound')
        
        a = VarOps().GetTyped(returnd)
        if 'decimal' in a:
            #pout.v('Convert Decimal -> float')
            returnd = float(returnd)
        
        if returnd is None:
            returnd = 0
        
        a = VarOps().GetTyped(returnd)
        #pout.v(a)
        self.SetValue(returnd)

    def OnSave(self, whereField, whereValue):
        a = self.GetValue()
        
        if a is True:
            a = 1
        if a is False:
            a = 0
        try:
            returnd = LookupDB(self.tableName).UpdateSingle(self.fieldName, a, whereField, whereValue)
        except:
            pout.v(f'Table : {self.tableName} ; Field : {self.fieldName} ; WhereField : {whereField} ; whereValue: {whereValue}')

    def GetCtrl(self):
        return self.GetValue()

    def SetCtrl(self, value):
        self.SetValue(int(Decimal(value)))

    def Clear(self):
        self.SetValue(0)
#--------------------------------------------------------------------------------------
class RH_LoadSaveDate(object):
    def __init__(self, *args, **kwargs):
        self.tableName = None
        self.fieldName = None

    def OnLoad(self, whereField, whereValue):
        returnd = LookupDB(self.tableName).Specific(whereValue, whereField, self.fieldName)
        a = VarOps().GetTyped(returnd)
        if 'tuple' in a:
            returnd = returnd[0]
        
        if returnd is None:
            returnd = datetime.datetime.strptime('01/01/1969', '%m/%d/%Y')
        self.SetValue(returnd)

    def OnSave(self, whereField, whereValue):
        a = self.GetValue()
        pout.v(f'Date Picker Ctrl : {a}')
        b = a.FormatISODate()
        pout.v(f'Date Picker Crtl ISO Date : {b}')
        try:
            returnd = LookupDB(self.tableName).UpdateSingle(self.fieldName, b, whereField, whereValue)
        except:
            pout.v(f'Table : {self.tableName} ; Field : {self.fieldName} ; WhereField : {whereField} ; whereValue: {whereValue}')

    def GetCtrl(self):
        a = self.GetValue()
        b = a.FormatISODate()
        return b

    def SetCtrl(self, value):
        
        self.SetValue(value)

    def Clear(self):
        deflt = wx.DateTime(4,3,1968)
        self.SetValue(deflt)

#--------------------------------------------------------------------------------------
class RH_LoadSaveTime(object):
    def __init__(self, *args, **kwargs):
        self.tableName = None
        self.fieldName = None

    def OnLoad(self, whereField, whereValue):
        returnd = LookupDB(self.tableName).Specific(whereValue, whereField, self.fieldName)
        a = VarOps().GetTyped(returnd)
        pout.v(f'OnLoad Time Returnd : {returnd}')
        if returnd is None:
            returnd = datetime.datetime.strptime('01/01/1969', '%m/%d/%Y')

        date_obj = datetime.datetime.strptime(returnd, '%d-%m-%Y %H:%M:%S')
        self.SetValue(returnd)

    def OnSave(self, whereField, whereValue):
        a = self.GetValue()
        date_str = a.strftime('%d-%m-%Y %H:%M:%S')
        try:
            returnd = LookupDB(self.tableName).UpdateSingle(self.fieldName, b, whereField, whereValue)
        except:
            pout.v(f'Table : {self.tableName} ; Field : {self.fieldName} ; WhereField : {whereField} ; whereValue: {whereValue}')


    def GetCtrl(self):
        a = self.GetValue()
        b = a.FormatIsoTime()
        return b

    def SetCtrl(self, value):
        self.SetValue(value)

    def Clear(self):
        self.SetValue()
#--------------------------------------------------------------------------------------
class RH_LoadSavePath(object):
    def __init__(self, *args, **kwargs):
        self.tableName = None
        self.fieldName = None
    
    def OnLoad(self, whereField, whereValue):
        val = LookupDB(self.tableName).Specific(whereValue, whereField, self.fieldName)
        self.SetCtrl(val)
        
    def OnSave(self, whereField, whereValue):
        setTo = self.GetPath()
        pout.b(f'WhereField : {whereField} --> WhereValue : {whereValue}')
        pout.v(f'tableName : {self.tableName} ; fieldName : {self.fieldName}')
        try:
            item = LookupDB(self.tableName).UpdateSingle(self.fieldName, setTo, whereField, whereValue)
        except:
            pout.v(f'Table : {self.tableName} ; Field : {self.fieldName} ; WhereField : {whereField} ; whereValue: {whereValue}')

    def GetCtrl(self):
        return self.GetPath()
    
    def SetCtrl(self, value):
        typd = str(type(value))
        if value is None:
            value = ''
        if 'tuple' in typd:
            value = value[0]
        self.SetPath(str(value))

    def Clear(self):
        self.Clear()


#--------------------------------------------------------------------------------------
class RH_LoadSaveString(object):
    def __init__(self, *args, **kwargs):
        self.tableName = None
        self.fieldName = None
                     
    def OnLoad(self, whereField, whereValue):
        val = LookupDB(self.tableName).Specific(whereValue, whereField, self.fieldName)
        self.SetCtrl(val)
        
    def OnSave(self, whereField, whereValue):
        setTo = self.GetValue()
        pout.b(f'WhereField : {whereField} --> WhereValue : {whereValue}')
        pout.v(f'tableName : {self.tableName} ; fieldName : {self.fieldName}')
        try:
            item = LookupDB(self.tableName).UpdateSingle(self.fieldName, setTo, whereField, whereValue)
        except:
            pout.v(f'Table : {self.tableName} ; Field : {self.fieldName} ; WhereField : {whereField} ; whereValue: {whereValue}')

    def GetCtrl(self):
        return self.GetValue()
    
    def SetCtrl(self, value):
        if value is None:
            value = ''
        self.SetValue(str(value))

    def Clear(self):
        self.Clear()

#--------------------------------------------------------------------------------------
class RH_LoadSaveCombo(object):
    def __init__(self, *args, **kwargs):
        self.tableName = None
        self.fieldName = None

    def LoadDefaults(self, tableName, fieldName, whereField, whereValue):
        returnd = LookupDB(tableName).Specific(whereValue, whereField, fieldName)
        jsond = VarOps().CheckJson(returnd)        
        d = VarOps().GetTyped(jsond)
        print(f'jsond : {d}')
        if re.search('(list|tuple)', d, re.I):
            c = True
        a = VarOps().StrList(jsond)
        if jsond is not None and c is True:
            self.AppendItems(a)
            
    def OnLoad(self, whereField, whereValue):
        returnd = LookupDB(self.tableName).Specific(whereValue, whereField, self.fieldName)
        jsond = VarOps().CheckJson(returnd)
        d = VarOps().GetTyped(jsond)
        print(f'jsond : {d}')
        if re.search('(list|tuple)', d, re.I):
            c = True
        a = VarOps().StrList(jsond)
        if jsond is not None and c is True:
            self.AppendItems(a)
        
    def OnSave(self, whereField, whereValue):
        a = self.GetSelection()        
        b = VarOps().DoJson(a)
        try:
            returnd = LookupDB(self.tableName).UpdateSingle(self.fieldName, b, whereField, whereValue)        
        except:
            pout.v(f'Table : {self.tableName} ; Field : {self.fieldName} ; WhereField : {whereField} ; whereValue: {whereValue}')

    def GetCtrl(self):
        return self.GetSelection()

    def SetCtrl(self, value):
        self.SetSelection(value)

    def Clear(self):
        self.Clear()

#--------------------------------------------------------------------------------------
class RH_LoadSaveListBox(object):
    def __init__(self, *args, **kwargs):
        self.tableName = None
        self.fieldName = None
        
    def OnLoad(self, whereField, whereValue):
        returnd = LookupDB(self.tableName).Specific(whereValue, whereField, self.fieldName)
        jsond = VarOps().CheckJson(returnd)
        pout.v(f'RH_LoadSaveListBox : {jsond}')
        if jsond is not None:
            self.AppendItems(jsond)
        
    def OnSave(self, whereField, whereValue):
        a = self.GetSelection()        
        b = VarOps().DoJson(a)
        try:
            returnd = LookupDB(self.tableName).UpdateSingle(self.fieldName, b, whereField, whereValue)
        except:
            pout.v(f'Table : {self.tableName} ; Field : {self.fieldName} ; WhereField : {whereField} ; whereValue: {whereValue}')

    def GetCtrl(self):
            return self.GetSelection()

    def SetCtrl(self, value):
        self.SetSelection(value)

    def Clear(self):
        self.Clear()

#--------------------------------------------------------------------------
class RH_LoadSaveListCtrl(object):
    def __init__(self, *args, **kwargs):
        self.tableName = None
        self.fieldName = None
        
    def OnLoad(self, whereField, whereValue):
        returnd = LookupDB(self.tableName).Specific(whereValue, whereField, self.fieldName)
        jsond = VarOps().CheckJson(returnd)
        self.AppendItems(jsond)
        
    def OnSave(self, whereField, whereValue):
        a = self.GetValue()        
        b = VarOps().DoJson(a)
        try:
            returnd = LookupDB(self.tableName).UpdateSingle(self.fieldName, b, whereField, whereValue)
        except:
            pout.v(f'Table : {self.tableName} ; Field : {self.fieldName} ; WhereField : {whereField} ; whereValue: {whereValue}')

    def Clear(self):
        self.DeleteAllItems()

#------------------------------------------------------------------------
class RH_LoadSaveOLV(object):
    def __init__(self, *args, **kwargs):
        self.tableName = None
        self.fieldName = None
    
    def OnLoad(self, whereField, whereValue):
        returnd = LookupDB(self.tableName).Specific(whereValue, whereField, self.fieldName)
        try:
            jsond = json.loads(returnd)
            self.SetObjects(jsond)
        except:
            print('returnd Not JSON\'d')
            pout.v(jsond)
    
    def OnSave(self, whereField, whereValue):
        b = self.GetObjects()
        jsond = json.dumps(b)
        pout.v(f'GetSelectedObjects : {b}')
        try:
            returnd = LookupDB(self.tableName).UpdateSingle(self.fieldname, jsond, whereField, whereValue)
        except:
            pout.v(f'Table : {self.tableName} ; Field : {self.fieldName} ; WhereField : {whereField} ; whereValue: {whereValue}')

    def GetEntry(self):
        return self.GetSelectedObject()

    def GetAll(self):
        return self.GetObjects()
    
    def AddEntry(self, listdicts):
        old = self.GetObjects()
        new = old + listdicts
        self.SetObjects(new)
    
    def Clear(self):
        self.DeleteAllItems()


    


class RH_lineColor(wx.Colour):
    def __init__(self,*args, **kwargs):
        kwargs['red'] = 157
        kwargs['green'] = 224
        kwargs['blue'] = 173
        kwargs['alpha'] = 255
        wx.Colour.__init__(self, *args, **kwargs)
        self.Get()
#--------------------------------------------------------------------------        
class RH_FilePickerCtrl(wx.FilePickerCtrl, RH_LoadSavePath):
    def __init__(self, *args, **kwargs):
        wx.FilePickerCtrl.__init__(self, *args, **kwargs)

#-------------------------------------------------------------------------    
class RH_OLV(ObjectListView, RH_LoadSaveOLV):
    def __init__(self, *args, **kwargs):
        ObjectListView.__init__(self, *args, **kwargs)
        self.SetEmptyListMsg('No One Home')
       # self.evenRowsBackColor(RH_lineColor)

#--------------------------------------------------------------------------
class RH_DatePickerCtrl(wx.adv.DatePickerCtrl, RH_LoadSaveDate):
    def __init__(self, *args, **kwargs):
        wx.adv.DatePickerCtrl.__init__(self, *args, **kwargs)
    

#--------------------------------------------------------------------------------------
class RH_DateCtrl(wx.adv.DatePickerCtrl, RH_LoadSaveDate):
    def __init__(self, *args, **kwargs):
        wx.adv.DatePickerCtrl.__init__(self, *args, **kwargs)
        

#--------------------------------------------------------------------------
class RH_TimeCtrl(masked.TimeCtrl, RH_LoadSaveTime):
    def __init__(self, *args, **kwargs):
        masked.TimeCtrl.__init__(self, *args, **kwargs)


#--------------------------------------------------------------------------
class RH_CheckBox(wx.CheckBox, RH_LoadSaveNum):
    def __init__(self, *args, **kwargs):
        wx.CheckBox.__init__(self, *args, **kwargs)
    
#--------------------------------------------------------------------------
class RH_RadioButton(wx.RadioButton, RH_LoadSaveNum):
    def __init__(self, *args, **kwargs):
        wx.RadioButton.__init__(self, *args, **kwargs)


#--------------------------------------------------------------------------
class RH_RadioBox(wx.RadioBox, RH_LoadSaveSelection):
    def __init__(self, *args, **kwargs):
        wx.RadioBox.__init__(self, *args, **kwargs)
   
        
#--------------------------------------------------------------------------
class RH_ComboBox(wx.ComboBox, RH_LoadSaveCombo):
    def __init__(self, *args, **kwargs):
        wx.ComboBox.__init__(self, *args, **kwargs)


#--------------------------------------------------------------------------
class RH_ListCtrl(wx.ListCtrl, RH_LoadSaveListCtrl):
    def __init__(self, *args, **kwargs):
        wx.ListCtrl.__init__(self, *args, **kwargs)


#--------------------------------------------------------------------------
class RH_ListBox(wx.ListBox, RH_LoadSaveListBox):
    def __init__(self, *args, **kwargs):
         wx.ListBox.__init__(self, *args, **kwargs)


#--------------------------------------------------------------------------
class RH_TextCtrl(wx.TextCtrl, RH_LoadSaveString):
    def __init__(self, *args, **kwargs):
        wx.TextCtrl.__init__(self, *args, **kwargs)


#--------------------------------------------------------------------------
class RH_MComboBox(masked.combobox.ComboBox, RH_LoadSaveCombo):
    def __init__(self, *args, **kwargs):
        masked.combobox.ComboBox.__init__(self, *args, **kwargs)


#--------------------------------------------------------------------------
class RH_MTextCtrl(masked.textctrl.TextCtrl, RH_LoadSaveString):
    def __init__(self, *args, **kwargs):
        masked.textctrl.TextCtrl.__init__(self, *args, **kwargs)
        

#--------------------------------------------------------------------------        
class RH_NumCtrl(wx.lib.masked.NumCtrl, RH_LoadSaveNum):
    def __init__(self, *args, **kwargs):
        wx.lib.masked.NumCtrl.__init__(self, *args, **kwargs)


#---------------------------------------------------------------------------
class LCDisplay(wx.ListCtrl):
    def __init__(self, name, size, setList, debug=False, style=wx.LC_REPORT|wx.BORDER_SUNKEN):
        wx.ListCtrl.__init__(self, name)
        self.name = name
        self.size = size
        self.setList = setList
    
    def SetHeaders(self):
        for idx, label, width, opts in self.setList:
            if 'right' in opts.lower():
                self.InsertColumn(idx, label, format=wx.LIST_FORMAT_RIGHT, width=width)    
            else:
                self.InsertColumn(idx, label, width=width)


#-------------------------------------------------------------------------------            
# class GridCellNumCtrl(gridlib.GridCellEditor):
#     def __init__(self, fractionWidth=2, debug=False):
#         gridlib.GridCellEditor.__init__(self)
        
#         self.fractionWidth = fractionWidth

#     def Create(self, parent, id, evtHandler):

#         self._tc = masked.NumCtrl(parent, id=-1,
#                                   integerWidth=6,
#                                   fractionWidth=self.fractionWidth,
#                                   allowNone=False,
#                                   allowNegative=True,
#                                   useParensForNegatives=False,
#                                   groupDigits=False,
#                                   groupChar=',',
#                                   decimalChar='.',
#                                   min=None,
#                                   max=None,
#                                   limited=False,
#                                   limitOnFieldChange=False,
#                                   selectOnEntry=False,
#                                   foregroundColour="Black",
#                                   signedForegroundColour="Red",
#                                   emptyBackgroundColour="White",
#                                   validBackgroundColour="White",
#                                   invalidBackgroundColour="Yellow",
#                                   autoSize=True
#                                   )

#         self._tc.SetInsertionPoint(0)
#         self.SetControl(self._tc)

#         if evtHandler:
#             self._tc.PushEventHandler(evtHandler)

#     def SetSize(self, rect):

#         self._tc.SetSize(rect.x, rect.y, rect.width + 2, rect.height + 2,
#                                wx.SIZE_ALLOW_MINUS_ONE)

#     def Show(self, show, attr):
#         super(GridCellNumCtrl, self).Show(show, attr)

#     # def PaintBackground(self, rect, attr):
#     #     pass

#     def BeginEdit(self, row, col, grid):
#         self.startValue = grid.GetTable().GetValue(row, col)
#         if self.startValue == '':
#             self.startValue = 0

#         self.oldVal = self.startValue
#         typd = str(type(self._tc))
        
        

#         self._tc.SetValue(self.startValue)
#         self._tc.SetInsertionPointEnd()
#         self._tc.SetFocus()

#         # For this example, select the text
#         #self._tc.SetSelection(0)

#     def EndEdit(self, row, col, grid,eld):
#         val = self._tc.GetValue()
#         print(f'row : {row}\ncol : {col}\ngrid : {grid}\neld : {eld}')
        
#         if self.fractionWidth == 0:
#             qDecValue = '1'
#         if self.fractionWidth > 0:
#             starter = '1.'
#             bb = ''.zfill(self.fractionWidth)
#             qDecValue = starter + bb
        
#         if val != self.oldVal:
#             val = Decimal(self._tc.GetValue()).quantize(Decimal(qDecValue),
#                                                         rounding=ROUND_HALF_UP)
#             grid.GetTable().SetValue(row, col, str(val))
#             return val
#         else:
#             return None

#     def ApplyEdit(self, row, col, grid):
#         """
#         This function should save the value of the control into the
#         grid or grid table. It is called only after EndEdit() returns
#         a non-None value.
#         *Must Override*
#         """
#         val = self._tc.GetValue()
#         grid.GetTable().SetValue(row, col, val)

#  # update the table

#         self.startValue = ''
#         self._tc.SetValue('')

#     def Reset(self):
#         self._tc.SetValue(self.startValue)
#         self._tc.SetInsertionPointEnd()

#     def IsAcceptedKey(self, evt):
#         """
#         Return True to allow the given key to start editing: the base class
#         version only checks that the event has no modifiers.  F2 is special
#         and will always start the editor.
#         """

#         ## We can ask the base class to do it
#         #return super(MyCellEditor, self).IsAcceptedKey(evt)

#         # or do it ourselves
#         return (not (evt.ControlDown() or evt.AltDown()) and
#                 evt.GetKeyCode() != wx.WXK_SHIFT)

#     def StartingKey(self, evt):
#         """
#         If the editor is enabled by pressing keys on the grid, this will be
#         called to let the editor do something about that first key if desired.
#         """
#         key = evt.GetKeyCode()
#         ch = None
        
#         if key in [wx.WXK_NUMPAD0, wx.WXK_NUMPAD1, wx.WXK_NUMPAD2,
#                    wx.WXK_NUMPAD3, wx.WXK_NUMPAD4, wx.WXK_NUMPAD5,
#                    wx.WXK_NUMPAD6, wx.WXK_NUMPAD7, wx.WXK_NUMPAD8,
#                    wx.WXK_NUMPAD9]:

#             ch = ch = chr(ord('0') + key - wx.WXK_NUMPAD0)

#         elif key >= 48 and key <= 71 and chr(key) in string.printable:
#             ch = chr(key)

#         if ch is not None:
#             # For this example, replace the text.  Normally we would append it.
#             #self._tc.AppendText(ch)
#             self._tc.SetValue(ch)
#             self._tc.SetInsertionPointEnd()
#         else:
#             evt.Skip()

#     # def StartingClick(self):
#     #     """
#     #     If the editor is enabled by clicking on the cell, this method will be
#     #     called to allow the editor to simulate the click on the control if
#     #     needed.
#     #     """
#     #     pass

#     def Destroy(self):
#         """final cleanup"""
#         super(GridCellNumCtrl, self).Destroy()

#     # def Clone(self):
#     #     """
#     #     Create a new object which is the copy of this one
#     #     *Must Override*
#     #     """
#     #     pass

#-------------------------------------------------------------------------------
class MaskedCtrlEditor(wx.grid.GridCellEditor):
    def __init__(self, mask='###-###', debug=False):
        super(MaskedCtrlEditor, self).__init__()
        self.mask = mask
        

    def Create(self, parent, id, evtHandler):
        # Only gets called once  
        self.nc = masked.TextCtrl(parent, id, 
                          mask=self.mask)

        self.SetControl(self.nc)

        if evtHandler:
            self.nc.PushEventHandler(evtHandler)

    def BeginEdit(self, row, col, grid):
        self.startValue = grid.GetTable().GetValue(row, col)
        if self.startValue == "":
            self.startValue = "   -   "
        self.nc.SetValue(self.startValue)
        self.nc.SetFocus()

    def EndEdit(self, row, col, grid):
        changed = False
        val = self.nc.GetValue()
        if val != self.startValue:
            changed = True
            grid.GetTable().SetValue(row, col, val)
        self.startValue = "   -   "
        return changed

    def Show(self, show, attr):
       # if show:
               #self.nc.SetParameters(validBackgroundColour=attr.GetBackgroundColour())
        pass
        
    def Reset(self):
        self.nc.SetValue(self.startValue)

    def Clone(self):
        return MaskedCtrlEditor()

    def SetSize(self, rect):
        self.nc.SetDimensions(rect.x, rect.y, rect.width+2, rect.height+2,
                              wx.SIZE_ALLOW_MINUS_ONE)


#-------------------------------------------------------------------------------
class GridCellComboBox(gridlib.GridCellEditor):
    def __init__(self, *args, **kwargs):
        listd = kwargs.pop('listd')
        gridlib.GridCellEditor.__init__(self, *args, **kwargs)
        self.listd = listd
        

    def Create(self, parent, id, evtHandler):
        self._combobox = wx.ComboBox(parent, id=-1, choices=[])
        self._combobox.SetItems(self.listd)
        #self._combobox.SetInsertionPoint(0)
        self._combobox.SetSelection(0)
        self.SetControl(self._combobox)

        if evtHandler:
            self._combobox.PushEventHandler(evtHandler)

    def SetSize(self, rect):
        self._combobox.SetDimensions(rect.x, rect.y, rect.width + 2,
                                     rect.height + 2,
                               wx.SIZE_ALLOW_MINUS_ONE)

    def Show(self, show, attr):
        super(GridCellComboBox, self).Show(show, attr)

    def PaintBackground(self, rect, attr):
        pass

    def BeginEdit(self, row, col, grid):
        self.startValue = grid.GetTable().GetValue(row, col)
        self.oldVal = self.startValue
        self._combobox.SetValue(self.startValue)
        #self._combobox.SetInsertionPointEnd()
        self._combobox.SetFocus()

        self._combobox.SetSelection(0)
        #, self._combobox.GetLastPosition())

    def EndEdit(self, row, col, grid):
        val = self._combobox.GetValue()
        
        if val != self.oldVal:
            val = self._combobox.GetValue()
            grid.GetTable().SetValue(row, col, str(val))
            return val
        else:
            return None

    def ApplyEdit(self, row, col, grid):
        """
        This function should save the value of the control into the
        grid or grid table. It is called only after EndEdit() returns
        a non-None value.
        *Must Override*
        """
        
        val = self._combobox.GetValue()
        grid.GetTable().SetValue(row, col, val)
        # update the table

        self.startValue = ''
        self._combobox.SetValue('')

    def Reset(self):
        self._combobox.SetValue(self.startValue)
        self._combobox.SetInsertionPointEnd()

    def IsAcceptedKey(self, evt):
        """
        Return True to allow the given key to start editing: the base class
        version only checks that the event has no modifiers.  F2 is special
        and will always start the editor.
        """

        ## We can ask the base class to do it
        #return super(MyCellEditor, self).IsAcceptedKey(evt)

        # or do it ourselves
        return (not (evt.ControlDown() or evt.AltDown()) and
                evt.GetKeyCode() != wx.WXK_SHIFT)

    def StartingKey(self, evt):
        """
        If the editor is enabled by pressing keys on the grid, this will be
        called to let the editor do something about that first key if desired.
        """
        key = evt.GetKeyCode()
        ch = None
        
        if key in [wx.WXK_NUMPAD0, wx.WXK_NUMPAD1, wx.WXK_NUMPAD2,
                   wx.WXK_NUMPAD3, wx.WXK_NUMPAD4, wx.WXK_NUMPAD5,
                   wx.WXK_NUMPAD6, wx.WXK_NUMPAD7, wx.WXK_NUMPAD8,
                   wx.WXK_NUMPAD9]:

            ch = ch = chr(ord('0') + key - wx.WXK_NUMPAD0)

        elif key >= 48 and key <= 71 and chr(key) in string.printable:
            ch = chr(key)

        if ch is not None:
            # For this example, replace the text.  Normally we would append it.
            #self._combobox.AppendText(ch)
            self._combobox.SetValue(ch)
            self._combobox.SetInsertionPointEnd()
        else:
            evt.Skip()

    def StartingClick(self):
        """
        If the editor is enabled by clicking on the cell, this method will be
        called to allow the editor to simulate the click on the control if
        needed.
        """
        pass

    def Destroy(self):
        """final cleanup"""
        super(GridCellNumCtrl, self).Destroy()

    def Clone(self):
        """
        Create a new object which is the copy of this one
        *Must Override*
        """
        pass
        
        
class GridButton(gridlib.GridCellRenderer):
    def __init__(self, debug=False):
        gridlib.GridCellRenderer.__init__(self)
        
        self.down = False
        self.click_handled = False

    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        """This is called when the widget is Refreshed"""
        
        dc.Clear()
        if self.down:
            state = wx.CONTROL_PRESSED | wx.CONTROL_SELECTED
        else:
            state = 0

        #if not self.IsEnabled():
        #    state = wx.CONTROL_DISABLED
        #pt = self.ScreenToClient(wx.GetMousePosition())
        #if self.GetClientRect().Contains(pt):
        #    state |= wx.CONTROL_CURRENT

        wx.RendererNative.Get().DrawPushButton(grid, dc, rect, state)
        #extra logic required since a button gets drawn at various times that could be while the mouse button is held down
        if self.down and not self.click_handled:
            self.click_handled = True
            self.HandleClick()

    def HandleClick(self):
        pass

    def GetBestSize(self, grid, attr, dc, row, col):
        text = grid.GetCellValue(row, col)
        dc.SetFont(attr.GetFont())
        w, h = dc.GetTextExtent(text)
        return wx.Size(w, h)


    def Clone(self):
        return MyCustomRenderer()        



#-----------------------------------
#----- Panels ---------------------
#-----------------------------------


class IconPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        '''Displays the Icon Panel options.'''
        iconList = kwargs.pop('iconList')
        wx.Panel.__init__(self, *args, **kwargs)
        #IconBarSizer = wx.GridBagSizer(4,4)
        IconBarSizer = wx.BoxSizer(wx.HORIZONTAL)

        for name, handler in iconList:
            iconloc = ButtonOps().Icons(name)
            icon = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(iconloc), style=wx.BORDER_NONE)
            icon.Bind(wx.EVT_BUTTON, handler)
            iconpos = [('find',(0,1)),
                       ('left',(0,2)),
                       ('right',(0,3)),
                       ('add',(0,4)),
                       ('undo',(0,5)),
                       ('save',(0,6)),
                       ('delete',(0,7)),
                       ('refresh',(0,8)),
                       ('receiving',(0,9)),
                       ('addrmaint',(0,10)),
                       ('print',(0,11)),
                       ('exit',(0,12))]
            
            iconsnum = len(iconList)
            
            distd = iconsnum
            for typd, posit in iconpos:
                if typd in name.lower():
                    flagnorm = wx.EXPAND|wx.ALL
                    span=(0,0)
                    if 'exit' in typd:
                        #IconBarSizer.Add((20,20), (0,21))
                        span=(0,distd)
                        flagnorm = wx.EXPAND
                    #IconBarSizer.Add(icon, posit, span=span, flag=flagnorm, border=5)
                    IconBarSizer.Add(icon, 0, flagnorm) 
        self.SetSizer(IconBarSizer)
        self.Layout()


class TransGridNTotalPanelShow(wx.Panel):
    def __init__(self, parent, id=wx.ID_ANY):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        self.SetName('TransGridNTotalPanel')
        self.grid = POS_Transactions_Grid(self, name='pos_transactions_grid', size=(950, 210))
        self.totals = TransactionTotalsPanel(self)

        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        MainSizer.Add(self.grid, 0)
        MainSizer.Add(self.totals, 0)

        self.SetSizer(MainSizer, 0)
        self.Layout()





class TransactionTotalsPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        
        self.SetName('TransactionTotalsPanel')

        MainSizer = wx.BoxSizer(wx.VERTICAL)
        
        #self.lvl2_2bSizer = wx.BoxSizer(wx.VERTICAL)

        totals_list = [('SubTotal', 'pos_subtotal_txtctrl'),
                       ('Tax', 'pos_tax_txtctrl'),
                       ('Total', 'pos_total_txtctrl')]

        for label, name in totals_list:
            box = wx.StaticBox(self, -1,
                               label=label,
                               style=wx.ALIGN_CENTER)

            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            ctrl = Totals_TxtCtrl(self, name=name)
            
            boxSizer.Add(ctrl, 0, wx.ALL | wx.EXPAND, 5)

            MainSizer.Add(boxSizer, 0,wx.ALL|wx.EXPAND, 5)
       
        self.SetSizer(MainSizer, 0)
        self.Layout()

class AddressTab(wx.Panel):
    def __init__(self, parent, debug=False):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        level1_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        cardinalsList = ['','N','NE','NW','E','S','SE','SW','W']
        suffix_list= ['','Av','Rd','St','Ct','Dr','Blvd','Cir','Aly','Anex','Bluff','Bend','Fwy','Pkwy','Ter','Trail','Way','Hgts']  
        
        lvl1_list = [('Number','addressMaint_houseNumber_txtctrl',70),('Direction','addressMaint_direction_combobox',cardinalsList),
                     ('Street Name','addressMaint_streetName_txtctrl',290),('Suffix', 'addressMaint_suffix_combobox',suffix_list),
                     ('Unit','addressMaint_unit_txtctrl',90)]
        
        
        
        for label,name,sized in lvl1_list:
            box = wx.StaticBox(self, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            
            if 'txtctrl' in name:
                ctrl = wx.TextCtrl(self, -1, name=name, size=(sized,-1),style=wx.TE_PROCESS_ENTER)
                ctrl.Bind(wx.EVT_KILL_FOCUS, EventOps().Capitals)
            if 'combobox' in name:
                ctrl = masked.ComboBox(self, -1, name=name, choices=sized)                 
            
            boxSizer.Add(ctrl, 0)
            
            level1_Sizer.Add(boxSizer, 0, wx.ALL, 3)
                
        
        level2_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        ctrl = wx.TextCtrl(self, -1, name='addressMaint_address0_txtctrl', size=(400,-1), style=wx.TE_READONLY)
        ctrl.SetBackgroundColour('gray')
        basePath = os.path.dirname(os.path.realpath(__file__))+'/' 
        iconloc =ButtonOps().Icons('refresh')
        
        button = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(iconloc), name=name, style=wx.BORDER_NONE)
        button.Bind(wx.EVT_BUTTON, self.AddTogether)
            
        level2_Sizer.Add(ctrl,0,wx.ALL,3)
        level2_Sizer.Add(button, 0, wx.ALL, 3)
        
        level3_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        box = wx.StaticBox(self, -1, label='Address 2')
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        ctrl = wx.TextCtrl(self, -1, name='addressMaint_address2_txtctrl', size=(400, -1))
        ctrl.Bind(wx.EVT_KILL_FOCUS, EventOps().Capitals)
        boxSizer.Add(ctrl, wx.HORIZONTAL)
        level3_Sizer.Add(boxSizer, 0)
        
        level4_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        box = wx.StaticBox(self, -1, label='Address 3')
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        ctrl = wx.TextCtrl(self, -1, name='addressMaint_address3_txtctrl', size=(400, -1))
        boxSizer.Add(ctrl, wx.HORIZONTAL)
        level4_Sizer.Add(boxSizer, 0)
        
        level5_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        level5_list = [('City','addressMaint_city_txtctrl',160),('State','addressMaint_state_txtctrl',75),
                       ('Zipcode','addressMaint_zipcode_txtctrl',120)]
        
        for label,name,sized in level5_list:
            box = wx.StaticBox(self, -1, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            if 'txtctrl' in name:
                if 'state' in name:
                    ctrl = masked.TextCtrl(self, -1, name=name, formatcodes="!", size=(sized, -1))
                if 'city' in name:
                    ctrl = wx.TextCtrl(self, -1, name=name, size=(sized, -1))
                    ctrl.Bind(wx.EVT_KILL_FOCUS, EventOps().Capitals)
                if 'zipcode' in name:
                    ctrl = masked.TextCtrl(self, -1, name=name, size=(sized,-1), mask = '#{5}')
            boxSizer.Add(ctrl, 0)                        
            level5_Sizer.Add(boxSizer, 0, wx.ALL, 3)
       
        
        MainSizer.Add(level1_Sizer, 0)
        MainSizer.Add(level2_Sizer, 0, wx.ALL, 3)
        MainSizer.Add(level3_Sizer, 0, wx.ALL, 3)
        MainSizer.Add(level4_Sizer, 0, wx.ALL, 3)
        MainSizer.Add(level5_Sizer, 0, wx.ALL, 3) 
        
        
        self.SetSizer(MainSizer,0)
        
        self.Layout()
        

    def AddTogether(self, event):
        
        streetNum = wx.FindWindowByName('addressMaint_houseNumber_txtctrl').GetCtrl()
        streetDirection = wx.FindWindowByName('addressMaint_direction_combobox').GetCtrl()
        streetName = wx.FindWindowByName('addressMaint_streetName_txtctrl').GetCtrl()
        streetType = wx.FindWindowByName('addressMaint_suffix_combobox').GetCtrl()
        unitNumber = wx.FindWindowByName('addressMaint_unit_txtctrl').GetCtrl()
        
        if streetNum:
            address0 = streetNum
        if streetDirection:
            address0 +=' '+streetDirection
        if streetName:
            address0 +=' '+streetName
        if streetType:
            address0 +=' '+streetType
        if unitNumber:
            address0 +=' Unit '+unitNumber
                
        wx.FindWindowByName('addressMaint_address0_txtctrl').SetCtrl(address0)        

#--------------------------------------------
#---------- Dialogs -------------------------
#--------------------------------------------
class AddressAccounts(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super(AddressAccounts, self).__init__(*args, **kwargs)
        
        lookupSizer = wx.BoxSizer(wx.VERTICAL)
        
        basePath = os.path.dirname(os.path.realpath(__file__))+'/' 
        IconBar_list =[('FindButton',ButtonOps().Icons('find'), self.OnFind),
                       ('SaveButton',ButtonOps().Icons('save'), self.OnSave),
                       ('UndoButton',ButtonOps().Icons('undo'), self.OnUndo),
                       ('AddButton',ButtonOps().Icons('add'), self.OnAdd),
                       ('DeleteButton',ButtonOps().Icons('delete'), self.OnDelete),
                       ('ExitButton',ButtonOps().Icons('exit'), self.OnExitButton)]
        
        IconBox = wx.StaticBox(self, label='')
        
        IconBarSizer = wx.StaticBoxSizer(IconBox, wx.HORIZONTAL)        
        xx = 0        
        for name,iconloc,handler in IconBar_list:
            icon = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(iconloc), name=name, style=wx.BORDER_NONE)
            icon.Bind(wx.EVT_BUTTON, handler)
            IconBarSizer.Add((80,1),0)
            if re.search('(Save|Delete|Undo)',name, re.I):
                icon.Disable()
            #if re.search('(Left|Right)',name, re.I):
            #    IconBarSizer.Add(icon,0)
            if 'Exit' in name:
                IconBarSizer.Add((150,10), 1)
                IconBarSizer.Add(icon, 0)
            else:
                if xx > 0:
                    IconBarSizer.Add((5,1), 0)
                    IconBarSizer.Add(wx.StaticLine(self, -1, size=(1,35),style=wx.LI_VERTICAL),  0)
                
                IconBarSizer.Add((5,1), 0)
                IconBarSizer.Add(icon, 0)
            xx += 1
        lookupSizer.Add((10,10), 0)    
        


        level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        level1_list = [('Account Number','acctNumber_txtctrl', 240),
                       ('Deactivated','deactivated_checkbox',0)]
        
        for label, name, sized in level1_list:
            if 'checkbox' in name:
                ctrl = wx.CheckBox(self, label=label, name=name)
                level1Sizer.Add(ctrl, 0, wx.ALL|wx.ALIGN_BOTTOM, 10)
            else:        
                box = wx.StaticBox(self, label=label)
                boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
                if 'acctNumber' in name:
                    ctrl = masked.TextCtrl(self, -1, name=name, size=(sized, -1),formatcodes='!',style=wx.TE_PROCESS_ENTER)
                    ctrl.SetFocus()
                else:
                    ctrl = wx.TextCtrl(self, -1, name=name, size=(sized, -1))
                
                boxSizer.Add(ctrl, 0)
                level1Sizer.Add(boxSizer, 0)               
        
        level2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.notebook = wx.Notebook(self, wx.ID_ANY)
        tabOne = AddressTab(self.notebook)
        
        self.notebook.AddPage(tabOne, "Address")
        
        level2Sizer.Add(self.notebook, 1, wx.ALL|wx.EXPAND, 5)
        
        lookupSizer.Add(IconBarSizer, 0, flag=wx.ALL|wx.EXPAND)

        lookupSizer.Add(level1Sizer, 0)
        lookupSizer.Add(level2Sizer, 0, wx.ALL|wx.EXPAND, 5)
        
        self.SetSizer(lookupSizer, 0)
        
        self.Layout()

        
    def OnFind(self, event):
        style = wx.DEFAULT_FRAME_STYLE&(wx.CLOSE_BOX)&(~wx.MAXIMIZE_BOX)
        with FindAddressLookupDialog(self, title="Find Address Form", size=(1000,600), style=style) as fal:
            pout.b('Find Address Form')
            self.addrPicked = None
            fal.ShowModal()
            self.addrPicked = fal.addrPicked
        
        pout.v("Address Lookup D : {}".format(self.addrPicked))
        if self.addrPicked is not None:
            wx.CallAfter(self.OnLoad, event=self.addrPicked)    
    
    
    
    
    def OnSave(self, event):
        acctNum = wx.FindWindowByName('acctNumber_txtctrl').GetCtrl()
        table_list = ['address_accounts']
        query = 'SELECT count(*) FROM address_accounts WHERE addr_acct_num=(?)'
        data = (acctNum,)
        returnd = SQConnect(query,data).ONE()
            
        
        ueryOps().CheckEntryExist('addr_acct_num',acctNum,table_list)
        
        
        save_list = [('addressMaint_houseNumber_txtctrl','street_num'),('addressMaint_direction_combobox','street_direction'),
                     ('addressMaint_streetName_txtctrl','street_name'),('addressMaint_suffix_combobox','street_type'),
                     ('addressMaint_unit_txtctrl','unit'),('addressMaint_address2_txtctrl','address2'),
                     ('addressMaint_address3_txtctrl','address3'),('addressMaint_city_txtctrl','city'),
                     ('addressMaint_state_txtctrl','state'),('addressMaint_zipcode_txtctrl','zipcode'),
                     ('addressMaint_address0_txtctrl','address0')]
        
        for name, field in save_list:
            value = wx.FindWindowByName(name).GetCtrl()
            query = 'UPDATE address_accounts SET {0}=(?) WHERE addr_acct_num=(?)'.format(field)
            data = (value, acctNum)
            returnd = SQConnect(query,data).ONE()
            
            
            
    def OnUndo(self, event):
        acctNum = wx.FindWindowByName('acctNumber_txtctrl').GetCtrl()
        wx.CallAfter(self.OnLoad, event=acctNum)
        
    
    def OnAdd(self, event):
        clear_list = [('addressMaint_houseNumber_txtctrl','street_num'),('addressMaint_direction_combobox','street_direction'),
                      ('addressMaint_streetName_txtctrl','street_name'),('addressMaint_suffix_combobox','street_type'),
                      ('addressMaint_unit_txtctrl','unit'),('addressMaint_address2_txtctrl','address2'),
                      ('addressMaint_address3_txtctrl','address3'),('addressMaint_city_txtctrl','city'),
                      ('addressMaint_state_txtctrl','state'),('addressMaint_zipcode_txtctrl','zipcode'),
                      ('addressMaint_address0_txtctrl','address0')]
        
        
        for name,field in clear_list:
            wx.FindWindowByName(name).ClearCtrl()
            
        for i in ['SaveButton','DeleteButton','UndoButton']:
            wx.FindWindowByName(i).EnableCtrl()

        new_acctNum = AccountOps().AcctNumAuto('address_accounts','addr_acct_num')
        wx.FindWindowByName('acctNumber_txtctrl').SetCtrl(new_acctNum)
        
    def OnDelete(self, event):
        acctNum = wx.FindWindowByName('acctNumber_txtctrl').GetCtrl()
        address0 = wx.FindWindowByName('addressMaint_address0_txtctrl').GetCtrl()
        city = wx.FindWindowByName('addressMaint_city_txtctrl').GetCtrl()
        state = wx.FindWindowByName('addressMaint_state_txtctrl').GetCtrl()
        zipcode = wx.FindWindowByName('addressMaint_zipcode_txtctrl').GetCtrl()
        
        delrec = wx.MessageBox('Delete Account #{0} \n{1}\n{2},{3}  {4}'.format(acctNum,address0,city,state,zipcode),'Delete Record', wx.YES_NO)
        
        if delrec == wx.YES:
            table_list = ['address_accounts']
            
            RecordOps(table_list).DeleteEntryRecord('addr_acct_num',acctNum)
            
            wx.CallAfter(self.OnAdd, event='')
        
    
    
    def OnExitButton(self, event):
        item = wx.FindWindowByName('Address_Maintenance_Frame').Close()
        
        


    def OnLoad(self, event):
        
        EnableList = ['SaveButton','UndoButton','DeleteButton']
        for i in EnableList:
            wx.FindWindowByName(i).EnableCtrl()
        
        
        wx.FindWindowByName('acctNumber_txtctrl').SetCtrl(event)
        
        load_list = [('addressMaint_houseNumber_txtctrl','street_num'),('addressMaint_direction_combobox','street_direction'),
                     ('addressMaint_streetName_txtctrl','street_name'),('addressMaint_suffix_combobox','street_type'),
                     ('addressMaint_unit_txtctrl','unit'),('addressMaint_address2_txtctrl','address2'),
                     ('addressMaint_address3_txtctrl','address3'),('addressMaint_city_txtctrl','city'),
                     ('addressMaint_state_txtctrl','state'),('addressMaint_zipcode_txtctrl','zipcode'),
                     ('addressMaint_address0_txtctrl','address0')]
        
        for name, field in load_list:
            query = 'SELECT {0} FROM address_accounts WHERE addr_acct_num=(?)'.format(field)
            data = (event,)
            returnd = SQConnect(query,data).ONE()
            value = returnd[0]
            
            
            wx.FindWindowByName(name).SetCtrl(value)
                    

class ReturnDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super(ReturnDialog, self).__init__(*args, **kwargs) 
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        Row1_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        Row2_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        Row3_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        in_list = [('&Transaction Number','returndlg_transNum_txtctrl', '#######'),('&Item Number', 'returndlg_itemNum_txtctrl',None)]
        
        for label, name, maskd in in_list:
            box = wx.StaticBox(self, -1, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            if maskd is not None:
                ctrl = RH_MTextCtrl(self, -1, name=name, mask=maskd, size=(125,-1),style=wx.TE_PROCESS_ENTER)
            else:
                ctrl = RH_TextCtrl(self, -1, name=name, size=(125,-1),style=wx.TE_PROCESS_ENTER)
            
            ctrl.Bind(wx.EVT_TEXT_ENTER, self.OnSearch)
                
            if 'transNum' in name:
                ctrl.SetFocus()
            
            boxSizer.Add(ctrl, 0)
            Row1_Sizer.Add(boxSizer, 0, wx.ALL|wx.ALIGN_CENTER, 10)
        
        
        lc = RH_OLV(self, -1, name='returndlg_invList_lc', size=(300,300), style=wx.LC_REPORT|wx.BORDER_SIMPLE)
        lc.SetColumns([
                      ColumnDefn('Trans #', 'center', 110,'transNum'),
                      ColumnDefn('Date','center',90,'dated'),
                      ColumnDefn('Time','center',90,'timed')
                     ])

        lc.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemChoose)    
        lc.Bind(wx.EVT_LIST_ITEM_SELECTED, self.TransLookup)
        
        Row3_Sizer.Add(lc, 0, wx.ALL|wx.ALIGN_LEFT, 5)
        
        grid = gridlib.Grid(self, style=wx.BORDER_SUNKEN, name='returndlg_transterm_grid')
        grid.EnableScrolling(True, True)
        collabel_list = [('Item Number',120),('Description',175),('Qty',75),('Price',75)]
        
        grid.SetRowLabelSize(0)
        grid.CreateGrid(10,len(collabel_list))
        grid.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        
        grid.SetLabelFont(wx.Font(wx.FontInfo(10).Bold()))
#        grid.SetLabelBackgroundColour(Theming('bg'))
#        grid.SetLabelTextColour(Theming('text'))

        idx = 0
        for label, sized in collabel_list:
            grid.SetColLabelValue(idx, label)
            grid.SetColSize(idx, sized)
            idx += 1    
        
        Row3_aSizer = wx.BoxSizer(wx.VERTICAL)
        Row3_aSizer.Add(grid, wx.ALL, 5)
        Row3_bSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        row3b_list = [('Payment Type', 'returndlg_paytype_txtctrl',140),
                      ('Total Price','returndlg_paytotal_txtctrl', 140)]
        for label, name, sized in row3b_list:
            box = wx.StaticBox(self, -1, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            ctrl = RH_TextCtrl(self, -1, name=name, size=(sized,-1))
            ctrl.Disable()
            boxSizer.Add(ctrl, 0)
            Row3_bSizer.Add(boxSizer, 0, wx.ALL, 15)
            
        
        btn = RH_Button(self, -1, label='Cancel')
        btn.Bind(wx.EVT_BUTTON, self.Cancel)


        Row3_aSizer.Add(Row3_bSizer, 0, wx.ALL|wx.ALIGN_CENTER,5)       
        
        Row3_Sizer.Add(Row3_aSizer, 0, wx.ALL, 5)               
        
        MainSizer.Add(Row1_Sizer, 0, wx.ALL|wx.ALIGN_CENTER)
        MainSizer.Add(Row2_Sizer, 0, wx.ALL|wx.ALIGN_CENTER)
        MainSizer.Add(Row3_Sizer, 0, wx.ALL|wx.ALIGN_CENTER)
        MainSizer.Add(btn, 0)
        self.SetSizer(MainSizer, 0)
        self.Layout()

    def Cancel(self,event):
        self.Close()

    def TransLookup(self, event):
        idd, objText = EventOps().LCGetSelected(event)
        
        fields = 'upc, description, unit_price, quantity, total_price'
        returnd = LookupDB('transactions').Specific(objText, 'transaction_id',fields)
        idx = 0
        gridname = 'returndlg_transterm_grid'
        GridOps(gridname).AlterGrid(returnd)
        for upc, description, unit_price, quantity, total_price in returnd:
            setList = [('Item Number',upc),('Description',description),('Qty',quantity),('Price',unit_price)]
            GridOps(gridname).FillGrid(setList, idx)
            idx += 1
                      
        returnd = LookupDB('transaction_payments').Specific(objText, 'transaction_id','pay_method, total_price')
        if returnd is not None:
            (paymethod, paytotal) = returnd
        
            listd = [('returndlg_paytype_txtctrl',paymethod),('returndlg_paytotal_txtctrl', paytotal)]
            for name, value in listd:
                item = wx.FindWindowByName(name).SetCtrl(value)
        
        
     
    def OnSearch(self, event):
        obj = event.GetEventObject()
        name = obj.GetName()
        if 'transNum' in name:
            invNum = wx.FindWindowByName('returndlg_transNum_txtctrl').GetCtrl()
            
            returnd = LookupDB('transactions').Specific(invNum, 'transaction_id', 'transaction_id, date, time')
            if len(returnd) > 0:
                idx = 0
                setList=[]
                for transId, dated, timed in returnd:
                    setList += [{'transNum' : transId, 'dated' : dated, 'timed' : timed}]

                item = wx.FindWindowByName('returndlg_invList_lc').AddEntry(setList)
    
    
        if 'itemNum' in name:
            upc = wx.FindWindowByName('returndlg_itemNum_txtctrl').GetCtrl()
            returnd = LookupDB('item_detailed').Specific(upc, 'upc','upc')
            if not returnd:
                whereFrom = '''upc LIKE (?) OR
                               altlookup LIKE (?) OR
                               description LIKE (?) OR
                               oempart_num LIKE (?) OR
                               part_num LIKE (?)'''
        
                query = "SELECT upc FROM item_detailed WHERE {0}".format(whereFrom)
                data = (upc, upc, upc, upc, upc,)
                returnd = SQConnect(query, data).ALL()
               
            numresult = len(returnd)
            
            if numresult == 0:
                wx.MessageBox('Item Not Found','Info',wx.OK)
                # query = 'SELECT upc FROM item_detailed LIMIT 1'
                # data = ''
                # returnd = SQConnect(query, data).ONE()
                returnd = LookupDB('item_detailed').General('upc', limit=1)
                
                if itemNumber_name is not None:
                    returnd = wx.FindWindowByName('inventory_itemNumber_txtctrl').GetCtrl()
                
                #wx.CallAfter(self.OnItemNumber, event='')
                found = False
                return returnd[0], found
        
            if numresult > 1:
                itemreturnd = list(sum(returnd, ()))
                style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
                ItemLookupD = ItemLookupDialog(self, title="Item Lookup", style=style, itemNumber=upc, size=(1000,800))
                ItemLookupD.ShowModal()
                
        
                try:
                    itempick = ItemLookupD.itemPicked
                    
                    wx.FindWindowByName('returndlg_itemNum_txtctrl').SetCtrl((str(itempick)))                    
                except:
                    pass
                    
                
                ItemLookupD.Destroy()
        
            else:
                itempick =VarOps().DeTupler(returnd)
        
                
                typed = type(itempick)
                
            found = True    
            
            # query = 'SELECT transaction_id, date, time FROM transactions WHERE upc=(?)'
            # data = (itempick,)
            # returnd = SQConnect(query,data).ALL()
            returnd = LookupDB('transactions').Specific(itempick, 'upc', 'transaction_id, date, time')

            list_lc = 'returndlg_invList_lc'
            wx.FindWindowByName(list_lc).ClearCtrl()
            try:
                if len(returnd) > 0:
                    idx = 0
                    for transId, dated, timed in returnd:
                        setList = [{'transNum' : transId, 'dated' : dated, 'timed' : timed}]
                        item = wx.FindWindowByName(list_lc).SetObjects(setList)
        
                    ListCtrl_Ops(list_lc).LCAlternateColor(len(returnd))        
                
                    item = wx.FindWindowByName(list_lc).SetFocus()
            except TypeError as e:
                print(f'ReturnDialog : {e}')
 
 
    def OnItemChoose(self,event):
        obj = event.GetEventObject()
        ids = obj.GetEntry()
        transNum = ids['transNum']
        
        itemNum = wx.FindWindowByName('returndlg_itemNum_txtctrl').GetCtrl()
        grid = wx.FindWindowByName('returndlg_transterm_grid')
        then_price = ''
        for xx in range(grid.GetNumberRows()):
            currentitem = grid.GetCellValue(xx,0)
            print('if {} in {}'.format(itemNum, currentitem)) 
            if itemNum.upper() in currentitem.upper():
                then_price = grid.GetCellValue(xx,3)
                break 
        

        trans_id = { itemNum : 
                               {'Desc':desc,
                                'Qty':qty,
                                'Cost':cost,
                                'Price':price,
                                'SetPrice':setprice,
                                'DiscAllYN':discountAll,
                                'Discount':disccol,
                                'Taxable':ntx,
                                'PriceTree':pricetree,
                                'TotalPrice':total}
                        

        }

        
        self.itemPicked = (objText,itemNum, then_price)
        
        self.Close()
                       
        
    def OnNoInvoice(self, event):
        invReturn = None
        self.Close()
        

class AddressSelectionDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        self.addrList = kwargs.pop('addrList')
        kwargs['size'] = (800, 350)
        super(AddressSelectionDialog, self).__init__(*args, **kwargs)
        
        #self.addrList = addrList
        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        Level1Sizer = wx.BoxSizer(wx.VERTICAL)
        
        #collabel_list = [(0,'Acct Number', 100,''),(1,'Address',220,''),(2,'Unit',50,''),(3,'City', 120,''),(4,'State', 50,''),(5,'Zipcode',70,'')]
        cell_color = Themes('Customers').GetColor('cell')
        #lc = wx.ListCtrl(self, -1, name='customers_addrSelect_lc', size=(650, 250), style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        #ListCtrl_Ops('customers_addrSelect_lc').LCSetHeaders(collabel_list)
        
        lc = RH_OLV(self, -1, name='customers_addrSelect_lc', size=(650, 250), style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        lc.SetColumns([
                     ColumnDefn('Acct Number','center',100, 'acctNum'),
                     ColumnDefn('Address','left',220,'addressd'),
                     ColumnDefn('Unit','center',50,'unitd'),
                     ColumnDefn('City','left',120,'cityd'),
                     ColumnDefn('State','left',50,'stated'),
                     ColumnDefn('Zipcode','left',70,'zipcoded')
        ])
        lc.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.SelectAddressOnCellLeftClick)
        
        ridx = 0
        cidx = 0    
        
        for item,name, sized, null in collabel_list:
            print("CIDX : {2} ; Item : {0} ; Sized : {1}".format(item,sized,cidx))
        
        Level1Sizer.Add(lc, 0 ,wx.ALL, 5)
        
        Level2Sizer = wx.BoxSizer(wx.VERTICAL)
        
        homeLabel = 'The Home Address is shown with a gold background on the list'
        text = wx.StaticText(self, -1, label=homeLabel, size=(120, -1))
        Level2Sizer.Add(text, 0, wx.ALL, 5) 
        
        
        MainSizer.Add(Level1Sizer, 0, wx.ALL, 5)
        MainSizer.Add(Level2Sizer, 0, wx.ALL, 5)
        self.SetSizer(MainSizer,0)
        self.Layout()
       
        wx.CallAfter(self.OnLoad, event='')
    
    def OnLoad(self, event):
        print('--- Addr List --- {}'.format(self.addrList))
        self.addr_dict = {}
        idx = 0
        cell_color = Themes().GetColor('cell')
        lc = wx.FindWindowByName('customers_addrSelect_lc')
        key = 0
        lc.DeleteAllItems()
        for acctNum in self.addrList:
            print('Key : {} ; AcctNum : {} '.format(key, acctNum))
            # query = '''SELECT addr_acct_num,address0, unit, city, state, zipcode 
            #            FROM address_accounts
            #            WHERE addr_acct_num=(?)'''
            # data = (acctNum,)
            # returnd = SQConnect(query, data).ONE()
            returnd = LookupDB('address_accounts').Specific(acctNum, 'addr_acct_num','addr_acct_num, address0, unit, city, state, zipcode')
            (acct_num, addr0, unitd, cityd, stated, zipcoded) = returnd
            
            self.addr_dict = [{'acctNum' : acct_num, 'address0' : addr0, 'unitd' : unitd, 'cityd' : cityd, 'stated' : stated, 'zipcoded' : zipcoded}]
            lc.AddObjects(self.addr_dict)
        #
        #      setList = [(0,acct_num),(1,addr0),(2,unitd),(3,cityd),(4,stated),(5,zipcoded)]
            
        #     ListCtrl_Ops('customers_addrSelect_lc').LCFill(setList,idx)
        #     idx += 1
        #     key += 1
        
        # ListCtrl_Ops('customers_addrSelect_lc').LCAlternateColor(idx)
            
        # homeAddr = len(self.addrList)-1
        # home_color = (209, 201, 94)
        # lc.SetItemBackgroundColour(homeAddr, home_color)
        
        lc.SetFocus()
        lc.Select(0)
        
    def SelectAddressOnCellLeftClick(self, event):
       
        item_id,objText = EventOps().LCGetSelected(event)
        self.addrPicked = objText
        self.Close()
        
                           
class PaymentDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        kwargs['size'] = (800,700)
        super(PaymentDialog, self).__init__(*args, **kwargs)
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        
        ctrl = RH_Button(self,-1, label='C&ustomer\nLookup', name='PaymentDialog_custLookup_btn')
        ctrl.Bind(wx.EVT_BUTTON, self.LookupCustomer)
        ctrl.Disable()
               
        MainSizer.Add(ctrl, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        pay_list = [('Total Paid','PaymentDialog_totalPaid_numctrl',120),
                    ('Discount Taken','PaymentDialog_discountTaken_numctrl',120)]

        box = wx.StaticBox(self, -1, label='Payment Info')
        boxSizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        for label, name, width in pay_list:
            lvlSizer = wx.BoxSizer(wx.HORIZONTAL)
            txt = wx.StaticText(self, -1, label=label)
            ctrl = masked.NumCtrl(self, -1, integerWidth=6, fractionWidth=2, name=name)
            if 'totalPaid' in name:
                ctrl.Bind(wx.EVT_KILL_FOCUS, self.AddedTotal)
                ctrl.SetFocus()
                
            lvlSizer.Add(txt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            lvlSizer.Add(ctrl, 0, wx.ALL, 3)
            boxSizer.Add(lvlSizer, 0, wx.ALL, 5)
            
        MainSizer.Add(boxSizer, 0, wx.ALL, 5)
        
        level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        lvl1_list = [('Acct Number', 'PaymentDialog_acctNumber_txtctrl', 120),
                     ('Acct Name', 'PaymentDialog_acctName_txtctrl', 190),
                     ('Total Due', 'PaymentDialog_totalDue_numctrl', 120)
                     ]
        
        for label, name, width in lvl1_list:
            box = wx.StaticBox(self, -1, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            if 'numctrl' in name:
                ctrl = RH_NumCtrl(self, -1, integerWidth=6, fractionWidth=2, name=name)
            if 'txtctrl' in name:
                ctrl = RH_TextCtrl(self, -1, name=name, size=(width, -1))
        
            if not 'discount' in name:
                ctrl.Disable()    

            boxSizer.Add(ctrl, 0, wx.ALL, 5)
            level1Sizer.Add(boxSizer, 0, wx.ALL, 25)
            
        MainSizer.Add(level1Sizer, 0)
        level2Sizer = wx.BoxSizer(wx.VERTICAL)
        
        #lc = CheckListCtrl(self, name='PaymentDialog_transaction_lc')
        self.resultsOlv = RH_OLV(self, size=(500,300), name='paymentDialog_transactions_olv', style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.resultsOlv.Bind(OLVEvent.EVT_ITEM_CHECKED, self.CheckBoxd)
        self.resultsOlv.SetEmptyListMsg("Nothing Found")
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        level2Sizer.Add(self.resultsOlv, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER, 5)
        MainSizer.Add(level2Sizer, 0, wx.ALL|wx.ALIGN_CENTER)
        level3Sizer = wx.BoxSizer(wx.HORIZONTAL)
        txt = wx.StaticText(self, -1, label="Pay By : ")
        level3Sizer.Add(txt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        btn_list = [('Cash','paymentDialog_paybyCash_btn'),
                    ('Check','payment_paybyCheck_btn'),
                    ('Credit Card','payment_paybyCard_btn')]
        
        for label, name in btn_list:
            btn = RH_Button(self, -1, label=label, name=name)
            btn.Bind(wx.EVT_BUTTON, self.PayBy)
            level3Sizer.Add(btn, 0, wx.ALL, 5)
                
        MainSizer.Add(level3Sizer,0, wx.ALL, 5)
        self.SetSizer(MainSizer,0)
        self.transNums = []
        self.Layout()

    def PayBy(self, event):
        obj = event.GetEventObject()
        name = obj.GetName()
        totalPaid = wx.FindWindowByName('PaymentDialog_totalPaid_numctrl').GetCtrl()
        custNum = wx.FindWindowByName('PaymentDialog_acctNumber_txtctrl').GetCtrl()
        
        style = wx.DEFAULT_FRAME_STYLE & (~wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX) & (~wx.MINIMIZE_BOX)
        if 'Cash' in name:
            if totalPaid > 0:
                yesno = wx.MessageBox('Return Change ?', 'Pay Info', wx.YES_NO)
                if yesno == wx.YES:
                    
                    p = PRx.MiscReceiptPrinted()
                    
                    p.CashDrawerOpen()
                    
                else:
                    query = '''UPDATE customer_accts_receivable
                               SET partial_cash=(?)
                               WHERE cust_num=(?)'''
                    data = [totalPaid, custNum,]
                    
                    returnd = SQConnect(query, data).ONE()
            paymethod = 'CASH'
            save_list = [(paymethod, 'transaction_payments','pay_method')]
                    
                    
        if 'Check' in name:
            dlg = CheckPopup(self, style)
            dlg.ShowModal()
            try:        
                paidCheck = dlg.payment    
            except:
                paidCheck = None
            
            dlg.Destroy()
            if paidCheck is not None:
                paymethod = 'CHECK'
                save_list = [(paymethod, 'transaction_payments', 'pay_method'),
                             (paidCheck[0], 'transaction_payments', 'check_num'),
                             (paidCheck[1], 'transaction_payments', 'dl_number'),
                             (paidCheck[2], 'transaction_payments', 'phone_num'),
                             (paidCheck[3], 'transaction_payments', 'dob')]
       
                     
        if 'Card' in name:
            dlg = CreditPopup(self, style)
            dlg.ShowModal()
            try:
                paidCard = dlg.payment        
            except:
                paidCard = None
                
            dlg.Destroy()
            if paidCheck is not None:
                paymethod = 'CARD'
                save_list = [(paymethod,'transaction_payments','pay_method'),
                             (paidCard[0],'transaction_payments','card1_name'),
                             (paidCard[1],'transaction_payments','card1_type'),
                             (paidCard[2],'transaction_payments','card1_auth')]
                
        paidDate = datetime.datetime.now().date().strftime('%Y-%m-%d')
        paidAdd = (paidDate, 'transaction_payments', 'paid_date')
        save_list.append(paidAdd)
            
        
        for trans_id in self.transNums:
            query = 'SELECT charge FROM transaction_payments WHERE transaction_id=(?)'
            data = [trans_id,]
            returnd = SQConnect(query,data).ONE()
            for meth, field in [('CASH','cash_payment'),('CHECK','check_payment'),('CARD','card1_payment')]:
                if paymethod == meth:
                    pay_field = field
            
            zero_out = '0.00'
            addPay = [(returnd[0], 'transaction_payments',pay_field),
                      (zero_out,'transaction_payments', 'charge')]
            
            save_list += addPay
            
            
            fieldSet, dataSet, table = QueryOps().Commaize(save_list, 'vari')
                    
            query = '''UPDATE {}
                       SET {}
                       WHERE transaction_id=(?)'''.format(table, fieldSet)
            
            data = dataSet + [trans_id,]
            returnd = SQConnect(query,data).ONE()

        self.Close()            
                             
                
    def AddedTotal(self, event):
        btn = wx.FindWindowByName('PaymentDialog_custLookup_btn')
        btn.Enable()
            
        
    def CheckBoxd(self, event):
        obj = self.resultsOlv.GetSelectedObject()
        checked = 'Checked' if self.resultsOlv.IsChecked(obj) else 'Unchecked'
        print(('{} row is {}'.format(obj.transNum, checked)))
        paidBox = wx.FindWindowByName('PaymentDialog_totalPaid_numctrl')
        dueBox = wx.FindWindowByName('PaymentDialog_totalDue_numctrl')
        discBox = wx.FindWindowByName('PaymentDialog_discountTaken_numctrl')
        self.transNums.append(obj.transNum)
        transTotal = obj.total
        paid_get = paidBox.GetValue()
        due_get = dueBox.GetValue()
        disc_get = discBox.GetValue()
            
        if checked == 'Checked':
            disc_sep = disc_get/self.cntRows
            paid_sub = Decimal(paid_get)-(Decimal(transTotal)-Decimal(disc_sep))
            paidBox.ChangeValue(float(paid_sub))
            due_sub = Decimal(due_get)-(Decimal(transTotal)-Decimal(disc_sep))
            dueBox.ChangeValue(float(due_sub))
        else:
            disc_sep = disc_get/self.cntRows
            paid_sub = Decimal(paid_get)+(Decimal(transTotal)+Decimal(disc_sep))
            paidBox.ChangeValue(float(paid_sub))
            due_sub = Decimal(due_get)+(Decimal(transTotal)+Decimal(disc_sep))
            dueBox.ChangeValue(float(due_sub))
            
                    

    def onToggle(self, event):
        """
        Toggle the check boxes
        """
        objects = self.resultsOlv.GetObjects()
        for obj in objects:
            print(self.resultsOlv.IsChecked(obj))
            self.resultsOlv.ToggleCheck(obj)
        self.resultsOlv.RefreshObjects(objects)
 
    def onCheck(self, event):
        """"""
        objects = self.resultsOlv.GetObjects()
 
        for obj in objects:
            self.resultsOlv.SetCheckState(obj, True)
        self.resultsOlv.RefreshObjects(objects)
 
    def onUncheck(self, event):
        """"""
        objects = self.resultsOlv.GetObjects()
 
        for obj in objects:
            self.resultsOlv.SetCheckState(obj, False)
        self.resultsOlv.RefreshObjects(objects)        
 
    def setResults(self,loadData):
        """"""
        transCol = ColumnDefn("Trans #", "center", 120, "transNum")
        dateCol = ColumnDefn("Date", "center", 100, "date")
        timeCol = ColumnDefn("Time", "center", 100, "time")
        totalCol = ColumnDefn("Total", "right", 150, "total")
            
        
        self.resultsOlv.SetColumns([transCol, dateCol, timeCol, totalCol])
        self.resultsOlv.CreateCheckStateColumn()
       # self.resultsOlv.InstallCheckStateColumn(transCol)
        self.resultsOlv.SetObjects(loadData)
 
        olv = wx.FindWindowByName('paymentDialog_transactions_olv').SetFocus()

    def LookupCustomer(self, event):
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
        with CustLookupDialog(self, title="Customer Lookup") as dlg:
            custPicked = None
            dlg.ShowModal()
            custPicked = dlg.itemPicked.upper().strip()
                        
        
        
        wx.FindWindowByName('PaymentDialog_acctNumber_txtctrl').SetCtrl(custPicked)
        query = 'SELECT full_name FROM customer_basic_info WHERE cust_num=(?)'
        data = [custPicked,]
        returnd = SQConnect(query,data).ONE()
        
        wx.FindWindowByName('PaymentDialog_acctName_txtctrl').SetCtrl(returnd[0])
        
                
        query = '''SELECT total_price
                   FROM transaction_payments
                   WHERE cust_num=(?) AND pay_method=(?)'''
        
        data = [custPicked, 'CHARGE',]
        
        returnd = SQConnect(query, data).ALL()
        tot = 0
        
        
        for price in returnd:
            
            tot += price[0]
        
        
        wx.FindWindowByName('PaymentDialog_totalDue_numctrl').SetCtrl(tot)
        
        
        load_data = self.OnLoad(custPicked)
        self.setResults(load_data)

    def OnLoad(self, custNum):
        query = '''SELECT date, time, transaction_id, total_price
                   FROM transaction_payments
                   WHERE cust_num=(?) AND pay_method=(?)'''
        
        data = [custNum, 'CHARGE',]
        returnd = SQConnect(query, data).ALL()
        
        idx = 0    
        open_trans = []
        for date, time, transNum, total_price in returnd:
            open_trans.append(Payment_OLV(date, time, transNum, total_price))
            
        self.cntRows = len(open_trans)
        
        return open_trans
    
           
class CashDrawerDialog(wx.Dialog):
    def __init__(self, parent, title, style, debug=False):
        super(CashDrawerDialog, self).__init__(parent=parent, title=title, size=(400, 400))
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        cards, cash, charged, debitd, checkd, taxd = 0,0,0,0,0,0
        qcards, qcash, qcharged, qdebitd, qcheckd = 0,0,0,0,0
        #dated = '2018-05-29'
        dated = datetime.date.today().strftime('%Y-%m-%d')
        query = 'SELECT card5_payment, cash_payment, card2_payment, card3_payment, card1_payment, card4_payment, debit_payment, check_payment, charge, tax FROM transaction_payments WHERE date = ?;'
        data = (dated,)
        returnd = SQConnect(query,data).ALL()
        
        for item in returnd:
            (crd5, csh, crd2, crd3, crd1, crd4, deb, chk, chrg, taxs) = item
            if crd1 > 0:
                cards += crd1
                qcards += 1
            
            if crd2 > 0:
                cards += crd2
                qcards += 1    
            if crd3 > 0:
                cards += crd3
                qcards += 1    
                
            if crd4 > 0:
                cards += crd4
                qcards += 1    
                
            if crd5 > 0:
                cards += crd5
                qcards += 1    
                
            if csh > 0:
                cash += csh      
                qcash += 1
            if deb > 0:
                debitd += deb
                qdebitd += 1
            
            if chk > 0:
                checkd += chk
                qcheckd += 1
                
            if chrg > 0:
                charged += chrg
                qcharged += 1
                
            if taxs > 0:
                taxd += taxs
            
        title_list = ['In Drawer']
        chk_list = [('Cash',cash),('Check',checkd),('Charge',charged),('Debit',debitd),('Credit Cards',cards),('Tax',taxd)]
        for label, vari in chk_list:
            if vari > 0:
                title_list.append(label)
        title_list.append('Total')
        
        grid = gridlib.Grid(self, -1, 
                            style=wx.BORDER_SUNKEN, 
                            pos=(0,0), 
                            name="pos_cashdrawer_grid")
        
        collabel_list = ['Qty', 'Total']
        grid.CreateGrid(len(title_list), len(collabel_list))
        grid.SetDefaultCellAlignment(wx.ALIGN_CENTRE,wx.ALIGN_CENTRE)
        grid.SetRowLabelAlignment(wx.LEFT, wx.ALIGN_CENTRE)
        grid.SetLabelFont(wx.Font(wx.FontInfo(9).Bold()))
        grid.SetRowLabelSize(120)
        grid.EnableEditing(False)
        #bgcolor = Theming('bg','POS') #(0,0,255)
        #whitetext = Theming('text','POS') #(255,255,255)
        #cell_color = Theming('cell','POS') #(217,241,232)
        #discountColor = (255,255,0)
        
        for idx,rowlabelset in enumerate(title_list):
            
            grid.SetRowLabelValue(idx, rowlabelset)
            for col_idx,collabelset in enumerate(collabel_list):
                grid.SetColLabelValue(col_idx,collabelset)
                
                if col_idx == 1:
                    grid.SetCellAlignment(idx, col_idx, wx.ALIGN_RIGHT, wx.ALIGN_BOTTOM)
                    grid.SetCellValue(idx, col_idx, '0.00')        
        
        
        totald = cards + checkd + charged + debitd + taxd + cash
        qtyd = qcards + qcheckd + qcharged + qdebitd + qcash
        fill_list = [('Cash',cash, qcash),('Check',checkd, qcheckd),('Charge',charged, qcharged),('Debit',debitd,qdebitd),('Credit Cards',cards, qcards),('Tax',taxd, 0),('Total',totald,qtyd)]
        for label, tot, qty in fill_list:
            for row in range(grid.GetNumberRows()):
                if label in grid.GetRowLabelValue(row):
                    grid.SetCellValue(row, 1, str(RO.DoRound(tot, '1.00')))
                    if qty != 0:
                        grid.SetCellValue(row, 0, str(qty))
            
            totald += tot
        
                
                
        GridOps(grid.GetName()).GridAlternateColor('')
        
        level1Sizer.Add(grid, 0, wx.ALIGN_CENTER, 5)	
       
        level2Sizer = wx.BoxSizer(wx.HORIZONTAL)        
        button_list = [('  Print  ','cashdrawer_print_button',self.onPrintButton),
                       ('  Close  ','cashdrawer_close_button',self.onCloseButton)]
        

        for label, name, hdlr in button_list:
            ctrl = RH_Button(self, -1, label=label, name=name)
            ctrl.Bind(wx.EVT_BUTTON, hdlr)
            level2Sizer.Add(ctrl, 0, wx.ALL|wx.ALIGN_CENTER, 30)
            
        
        
        MainSizer.Add(level1Sizer, 0, wx.ALL|wx.ALIGN_CENTER, 30)
        MainSizer.Add(level2Sizer, 0, wx.ALL|wx.ALIGN_CENTER, 30)
        self.SetSizer(MainSizer, 0)
        self.Layout()


    def onPrintButton(self, event):
        grid = wx.FindWindowByName('pos_cashdrawer_grid')
        header = []
        maxcols = grid.GetNumberCols()
        maxrows = grid.GetNumberRows()
        for col in range(maxcols):
            label = grid.GetColLabelValue(col)
            header.append(label)
    
        data = {}
        for row in range(maxrows):
            label = grid.GetRowLabelValue(row)
            data_tup = (label,)
            for col in range(maxcols):
                data_tup +=(grid.GetCellValue(row, col),)
            
            data[row]=data_tup    
                
         
           
        
    def onCloseButton(self, event):
        self.Close()
                
#--------------------------------------------


class VendorFindDialog(wx.Dialog):
    def __init__(self, parent, title, style, size=(1000,800), vendorNum=None, debug=False):
        super(VendorFindDialog, self).__init__(parent=parent, title=title, size=(1000,800))
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        if vendorNum == '' or vendorNum == None:
            wx.CallAfter(self.OnLoad, event=vendorNum)
            
        ctrl = RH_TextCtrl(self, -1, name='vendorFind_search_txtctrl', size=(360,-1), style=wx.TE_PROCESS_ENTER)
        ctrl.Bind(wx.EVT_TEXT_ENTER, self.OnSearchVendor)
        ctrl.SetFocus()
        level1Sizer.Add(ctrl, 0, wx.ALL|wx.CENTER,5)
        
        button = RH_Button(self, -1, label='Search',name='vendorFind_search_button')
        button.Bind(wx.EVT_BUTTON, self.OnSearchVendor)
        level1Sizer.Add(button, 0, wx.ALL, 5)
        
        level2Sizer = wx.BoxSizer(wx.VERTICAL)
        
        collabel_list = [(0,'Vendor Number', 120, ''),(1,'Vendor Name', 120,'')]
        
        lc = RH_OLV(self,-1, name='vendorFind_lc', size=(300,300), style=wx.LC_REPORT)
        #ListCtrl_Ops('vendorFind_lc').LCSetHeaders(collabel_list)
        lc.SetColumns([
                    ColumnDefn('Vendor #','center',120,'vendorNum'),
                    ColumnDefn('Name','left',120,'vendorName')
                    ])
        
        lc.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.LookupOnCellLeftClick)
        
        level2Sizer.Add(lc, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER, 3)
        MainSizer.Add(level1Sizer, 0, wx.ALL|wx.EXPAND|wx.CENTER, 5)
        MainSizer.Add(level2Sizer, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER, 5)
        
        self.SetSizer(MainSizer,0)
        self.Layout()
        
    def OnLoad(self, event):
       
        wx.FindWindowByName('vendorFind_search_txtctrl').SetCtrl(event)
        #wx.CallAfter(self.OnSearchVendor, event='')
        
         
    def LookupOnCellLeftClick(self, event):
       
        item_id,objText = EventOps().LCGetSelected(event)
        obj = event.GetEventObject()
        ddf = obj.GetItem(item_id,1).GetText()
        
        self.itemPicked = ddf
        self.Close()
        
        
    def OnSearchVendor(self, event):
       
        obj = event.GetEventObject()
        named = obj.GetName()
        if 'button' in named:
            named = re.sub('button','txtctrl',named)
        if not named:
            named = 'vendorFind_search_txtctrl' 
        searchItem = wx.FindWindowByName(named).GetCtrl()
        
        query = "SELECT vend_num,name FROM vendor_basic_info WHERE name like ?"
        data = ('%'+searchItem+'%',)
        returnd = SQConnect(query, data).ALL()
        returnd_count = len(returnd)
        
        if returnd_count == 0:
            wx.MessageBox('Name Not Found.','Vendor Lookup', wx.OK)
            return
        
        print("OnSearch VendorName - returned {0} records".format(returnd_count))
        
        xx=0  
        lc_name = 'vendorFind_lc'
        idx = 0         
        for vend_numd, named in returnd:
            setList = [(0,vend_numd),(1,named)]
            ListCtrl_Ops(lc_name).LCFill(setList,idx)
            idx+=1


class ReceivingDialog(wx.Dialog):
    def __init__(self, parent, title, style, debug=False):
        super(ReceivingDialog, self).__init__(parent=parent, title=title, size=(1000,800))
        
        
           
 
        
class ItemLookupDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        self.itemNumber = kwargs.pop('itemNumber')
        super(ItemLookupDialog, self).__init__(*args, **kwargs)
        #self.itemNumber = itemNumber
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        rightSideSizer = wx.BoxSizer(wx.VERTICAL)
        leftSideSizer = wx.BoxSizer(wx.VERTICAL)
        level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        level2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        item_list = [('Item Number : ','itemLookup_itemNumber_txtctrl',140, 'itemLookup_itemNumber_search_button',level1Sizer),
                     ('Item Description : ','itemLookup_itemDescription_txtctrl',240,'itemLookup_itemDescription_search_button',level2Sizer)]
        
        for label,name,sized,button_name,sizer in item_list:
            text = wx.StaticText(self, -1, label=label)
            ctrl = RH_TextCtrl(self, -1, name=name,size=(sized,-1),style=wx.TE_PROCESS_ENTER)
            ctrl.Bind(wx.EVT_TEXT_ENTER, self.LookupItems)
            button = RH_Button(self, -1, label='Search',name=button_name)
            button.Bind(wx.EVT_BUTTON, self.LookupItems)
            sizer.Add(text, 0, wx.ALL, 2)
            sizer.Add(ctrl, 0, wx.ALL, 2)
            sizer.Add(button, 0, wx.ALL, 2)       
        
        level3Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        qualify_list = [('Department','itemLookup_department_combobox'),
                        ('Category','itemLookup_category_combobox'),
                        ('Subcategory','itemLookup_subcategory_combobox'),
                        ('Location','itemLookup_location_combobox'),
                        ('Search','itemLookup_DCS_search_button')]
        
        for label,name in qualify_list:
            if 'button' in name:
                ctrl = RH_Button(self, -1, label=label,name=name)
                ctrl.Bind(wx.EVT_BUTTON, self.LookupItems)
            if 'combobox' in name:
                ctrl = DCS_Combobox(self, name=name, which=label, style=wx.CB_READONLY)
            
            
            level3Sizer.Add(ctrl, 0, wx.ALL, 3)         
            
        level4Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        vendor_count = QueryOps().QueryCheck('vendor_basic_info')
        print("vendor Count : {0}".format(vendor_count))
        setList = [(0,'Number',90,''),(1,'Vendor Name',250,'')]
                
        lc = RH_OLV(self, -1, name='itemLookup_vendor_lc',size=(350, 100), style=wx.LC_REPORT|wx.BORDER_SIMPLE)
        #ListCtrl_Ops('itemLookup_vendor_lc').LCSetHeaders(setList)
        lc.SetColumns([
                     ColumnDefn('Vendor #','center',90,'vendorNum'),
                     ColumnDefn('Name','left',250,'vendorName')
                    ])
        lc.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.VendorOnCellLeftClick)
        
        level4Sizer.Add(lc, 0,wx.ALL|wx.EXPAND|wx.ALIGN_CENTER,3)
       
        level4bSizer = wx.BoxSizer(wx.VERTICAL)
        txt = wx.StaticText(self, -1, label='', name='itemInq_NumberOfItems_text')
        level4bSizer.Add(txt,0,wx.ALL|wx.EXPAND, 3)
        
        level5Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        maxgridcount=5000
        print("Max Grid Count : ",maxgridcount)
        
        cell_color = Themes().GetColor('cell') #(217,241,232)
        lc = RH_OLV(self, -1, name='itemLookup_display_lc', size=(660,300), style=wx.LC_REPORT|wx.BORDER_SIMPLE)
        lc.SetColumns([
                    ColumnDefn('Item #','left',120,'itemNum'),
                    ColumnDefn('Description','left',350,'itemDesc'),
                    ColumnDefn('Price','right',90,'itemPrice'),
                    ColumnDefn('OnHand','right',90,'itemOnHand')
                    ])
        lc.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.LookupOnCellLeftClick)
            
        idx = 0
        
        level5Sizer.Add(lc, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER, 5)
    
        
        sizers = [level1Sizer, level2Sizer, level3Sizer]
        for sizer in sizers:
            rightSideSizer.Add(sizer, 0, wx.ALL|wx.LEFT, 3)
        
        MainSizer.Add(leftSideSizer, 0)
        MainSizer.Add(rightSideSizer, 0)
        MainSizer.Add(level4Sizer, 0, wx.ALL|wx.CENTER, 5)
        MainSizer.Add(level4bSizer, 0,wx.ALL|wx.CENTER, 5)
        MainSizer.Add(level5Sizer,0,wx.ALL|wx.CENTER, 5)
        self.SetSizer(MainSizer)
        self.Layout()
        
        if self.itemNumber is not None:
            wx.CallAfter(self.OnLoad, event=self.itemNumber)
    
    def showFound(self,queryTable,queryWhere,queryData, itemNumber):
        retail_scale = {}
        lc_name = 'itemLookup_display_lc'
        query = 'SELECT upc,description,quantity_on_hand FROM item_detailed WHERE {0}'.format(queryWhere)    
        queryTable = 'item_detailed'
        cnt_items = QueryOps().QueryCheck(queryTable,queryWhere,queryData)
        data=''
        item1 = '{:n}'.format(cnt_items)
        itemCnt = '{0} Records'.format(item1)
        wx.FindWindowByName('itemInq_NumberOfItems_text').SetCtrl(itemCnt)
        returnd = SQConnect(query, data).ALL()
        idx = 0
        
        self.FillOutLC(lc_name, returnd, idx)   
    
    def FillOutLC(self, lc_name, fillout, row):
        olv = wx.FindWindowByName(lc_name)
        lc.DeleteAllItems()
        for upc, desc, qty in fillout:
            retaild = RetailOps().RetailSifting(upc)
            #setList = [(0,upc),(1,desc),(2,retaild['standard_price']['price']),(3,qty)]
            setList = [{
                        'itemNum': upc, 
                        'itemDesc': desc, 
                        'itemPrice': retaild['standard_price']['price'],
                        'itemOnHand':qty
                       }]
            wx.FindWindowByName('itemLookup_display_lc').AddEntry(setList)
            
        lc.SetFocus()
            
    def LookupItems(self, event):
       
        obj = event.GetEventObject()
        named = obj.GetName()
        print("Lookup Items : ",named)
        if 'button' in named:
            named = re.sub('button','txtctrl', named)
        if 'itemNumber' in named:
            print("item Number Lookup")
            itemNumber = obj.GetValue()
            print("Item Number : {0}".format(itemNumber))
            if len(itemNumber) < 3:
                print("yes no question")
                yesno = wx.MessageBox('{0}? Are you Sure? Searching will take awhile...'.format(len(itemNumber)),'Are You Sure?',wx.YES_NO)
                if yesno == wx.NO:
                    return                
            
            queryWhere = QueryOps().ANDSearch(['upc','description','part_num','oempart_num','altlookup'],itemNumber)
            queryData = ''
            queryTable = 'item_detailed'
            
            self.showFound(queryTable,queryWhere,queryData, itemNumber)
            #lc = wx.FindWindowByName('itemLookup_display_lc').SetFocus()
            
        if 'itemDescription' in named:
            print("item Description Lookup")
            named = obj.GetName()
            print("named : ",named)
            if 'button' in named:
                named = re.sub('button','txtctrl',named)
            itemDesc = wx.FindWindowByName(named).GetCtrl()
            print("Item Number : {0}".format(itemDesc))
            if len(itemDesc) < 3:
                print("yes no question")
                yesno = wx.MessageBox('{0} character? Are you Sure? Searching will take awhile...'.format(len(itemDesc)),'Are You Sure?',wx.YES_NO)
                if yesno == wx.NO:
                    return                
            
            queryWhere = QueryOps().ANDSearch('description',itemDesc)
            queryData = ''
            queryTable = 'item_detailed'
            self.showFound(queryTable,queryWhere,queryData, itemDesc)
            #lc = wx.FindWindowByName('itemLookup_display_lc').SetFocus()    
        
        if 'DCS_search' in named:
            print("item DCS Lookup")
            dept = wx.FindWindowByName('itemLookup_department_combobox').GetCtrl()
            cat = wx.FindWindowByName('itemLookup_category_combobox').GetCtrl()
            subcat = wx.FindWindowByName('itemLookup_subcategory_combobox').strip('-').GetCtrl()
            locat = wx.FindWindowByName('itemLookup_location_combobox').GetCtrl()
            var_list = [('DEPARTMENT',dept),('CATEGORY',cat),('SUBCATEGORY',subcat),('LOCATION',locat)]
            startd = ''
            for title,var in var_list:
                if var.lower() == title.lower().strip('-'):
                    var = ''
                
                print("TITLE : {0} = {1}".format(title,var))
                if len(var) > 1:
                    if len(startd) > 1 :
                        startd +=' AND '
                        
                    startd += "{0}='{1}'".format(title.lower(), var)
                  
                                    
            if startd:
                print("Startd : {0}".format(startd))
                queryWhere = startd
                queryData = ''
                queryTable = 'item_options'
                
                #item1 = '{:n}'.format(cnt_items)
                #itemCnt = '{0} Records'.format(item1)
                #CO('itemInq_NumberOfItems_text').SetCtrl(itemCnt)
                #self.showFound(queryTable,queryWhere,queryData)            
                #GO().DisplayLookupItemsinGrid(queryWhere,queryData,queryTable)
        
        lc = wx.FindWindowByName('itemLookup_display_lc').SetFocus()
        
    def OnLoad(self, event):
        '''Load Department, Category, Sub Category Choices.'''
       
        print("FROM PREVIOUS : {0}".format(self.itemNumber))
        check = QueryOps().CheckEntryExist('upc', self.itemNumber, ['item_retails'])
        
        qualify_list =  [('department','itemLookup_department_combobox'),
                        ('category','itemLookup_category_combobox'),
                        ('subcategory','itemLookup_subcategory_combobox'),
                        ('location','itemLookup_location_combobox')]
         
        for field, name in qualify_list:
            query = "SELECT {0} FROM organizations".format(field)
            data = ''
            returnd = SQConnect(query, data).ONE()
            if returnd is not None:
                listd = returnd[0]
                wx.FindWindowByName(name).SetCtrl(listd)     
        
        
        # Load Vendors
        lc_name = 'itemLookup_vendor_lc'
        lc = wx.FindWindowByName(lc_name)
        query = 'SELECT vend_num, name FROM vendor_basic_info'
        data = ''
        returnd = SQConnect(query, data).ALL()
        
        idx = 0
        try:
            for vendNum, vendName in returnd:
                print('vendor Number : {}\nvendor Name : {}'.format(vendNum, vendName))
                setList = [(0,vendNum),(1,vendName)]
                ListCtrl_Ops(lc_name).LCFill(setList, idx)
                idx += 1
            
            ListCtrl_Ops(lc_name).LCAlternateColor(len(returnd))
        except TypeError as e:
            print(f'Loading Vendor Error : {e}')            
    
        if len(self.itemNumber) > 0:
             
            queryWhere = QueryOps().ANDSearch(['upc','description','part_num','oempart_num','altlookup'],self.itemNumber)
            queryData = ''
            queryTable = 'item_detailed'
            
            query = '''SELECT upc,description,quantity_on_hand
                       FROM item_detailed
                       WHERE {0}'''.format(queryWhere)

            data = ''
            returnd = SQConnect(query, data).ALL()
            row = 0
            lcname = 'itemLookup_display_lc'
            
            print(f"item Lookup Display LC : {returnd}")
            
            for upc, desc, qty in returnd:
                retaild = RetailOps().RetailSifting(upc)
                if retaild is not None:
                    print('upc : {}\ndesc : {}\n qty : {}\nretaild : {}'.format(upc, desc, qty, retaild['standard_price']['price']))
                    setList = [(0,upc),(1,desc),(2,retaild['standard_price']['price']), (3,qty)]
                    ListCtrl_Ops(lcname).LCFill(setList, row)
                    row += 1
            
            ListCtrl_Ops(lcname).LCAlternateColor(len(returnd))
            lc = wx.FindWindowByName(lcname).SetFocus()
            
        
                       
    def VendorOnCellLeftClick(self, event):
        obj = event.GetEventObject()
        
        item_id,objText = EventOps().LCGetSelected(event)
        self.itemPicked = objText
          
        itemPicked = objText
            
        query = "SELECT upc,description,quantity_on_hand FROM item_detailed WHERE vendor_info like ?"
        data = ('%'+itemPicked+'%',)
        returnd = SQConnect(query, data).ALL()
        
        lc_name = 'itemLookup_display_lc'
        lc = wx.FindWindowByName(lc_name)
        lc.DeleteAllItems()
            
        if returnd == None or len(returnd) == 0:
            
            self.itemFinalPick = ''
                
        else:
            self.itemsPicked = len(returnd) 
            self.itemFinalPick = returnd
            
            
            xx = 0
            
            
            retail_scale = {}
            for upc in returnd[0]:  
                retail_scale[upc]=RO().RetailSifting(upc)
                
            self.FillOutLC(lc_name, returnd, xx)
                
            ListCtrl_Ops(lc_name).LCAlternateColor(len(returnd))
        
    
    def LookupOnCellLeftClick(self, event):
        obj = event.GetEventObject()
        item_id,objText = EventOps().LCGetSelected(event)
        pout.v(objText)
        self.itemPicked = objText

        self.Close()
        
        
class ReloadDialog(wx.Dialog):
    def __init__(self, debug=False,):
        super(ReloadDialog, self).__init__(size=(550,160))
        lc = RH_OLV(self, -1, name='reload_trans_lc', size=(535,150), style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        lc.SetColumns([
                    ColumnDefn('Transaction #','center',100,'transNum'),
                    ColumnDefn('Date','center',100,'dated'),
                    ColumnDefn('Name','left',120,'named'),
                    ColumnDefn('PO Number','center',140, 'poNum')
        ])
        # collabel_list = [(0,'Transaction #',100),(1,'Date',100),(2,'Name',170),(3,'PO Number',140)]
        # for idx, label, width in collabel_list:
        #     lc.InsertColumn(idx, label, width=width)
            
        lc.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.SelectReload)
            
        btn = RH_Button(self, -1, label='Cancel')
        btn.Bind(wx.EVT_BUTTON, self.Close())

        MainSizer = wx.BoxSizer(wx.VERTICAL)
        MainSizer.Add(lc, 0, wx.ALL, 5)        
        MainSizer.Add(btn, 0)

        self.SetSizer(MainSizer,0)
        self.Layout()
        
        
        wx.CallAfter(self.OnLoad, event='')

    def OnLoad(self, event):
        lc = wx.FindWindowByName('reload_trans_lc')
        query = """SELECT transaction_id, date, cust_num, po_number 
                   FROM transactions 
                   WHERE type_of_transaction='Hold'"""
        data = ''
        returnd = SQConnect(query,data).ALL()
        
        if returnd is None or len(returnd) == 0:
            wx.MessageBox('No Reloadable Transactions Found','Info',wx.OK)
            self.Close()
        
        idx = 0
        y = 1
        self.reload_dict = {}
        cell_color = Themes().GetColor('cell')
        myset = set()
        for trans_id, dated, cust_num, po_num in returnd:
            
            
            
            
            fullName = ''
            if len(cust_num) > 0:
                query = 'SELECT full_name FROM customer_basic_info WHERE cust_num=(?)'
                data = (cust_num,)
                fullName = SQConnect(query,data).ONE()[0]
            if po_num is None:
                po_num = ''
            self.reload_dict[idx] = (trans_id,dated,fullName,po_num)
            if not trans_id in myset:
                setList = [(0,trans_id),(1,dated),(2,fullName),(3,po_num)]
                LC('reload_trans_lc').LCFill(setList,idx)    
            
            myset.add(trans_id)
            idx += 1
        
        ListCtrl_Ops('reload_trans_lc').LCAlternateColor(idx)
            
        lc.SetFocus()          
        lc.Select(0)                     
                   
    def SelectReload(self, event):
        item_id,objText = EventOps().LCGetSelected(event)
        self.trans_id = objText
        self.Close()
        
    def Actions(self, event):
        obj = event.GetObject()
        grid = obj.GetName()
        row = obj.GetRow()
        col = obj.GetCol()
        
        print('({},{})'.format(row,col))
        
        if keycode == wx.WXK_SPACE or keycode == wx.WXK_RETURN:
            pass    
        
        event.Skip()    
        
        
    
    def OnLeftDown(self, evt):
        obj = evt.GetObject()
        name = obj.GetName()
        grid = wx.FindWindowByName(name)
        col, row = self.HitTestCell(evt.GetPosition().x, evt.GetPosition().y)
        if isinstance(grid.GetCellRenderer(row, col), GridButton):
            grid.GetCellRenderer(row, col).down = True
        grid.Refresh()
        evt.Skip()

    def OnLeftUp(self, evt):
        obj = evt.GetObject()
        name = obj.GetName()
        grid = wx.FindWindowByName(name)
        col, row = self.HitTestCell(evt.GetPosition().x, evt.GetPosition().y)
        if isinstance(grid.GetCellRenderer(row, col), GridButton):
            grid.GetCellRenderer(row, col).down = False
            grid.GetCellRenderer(row, col).click_handled = False

        grid.Refresh()
        evt.Skip()

    def HitTestCell(self, x, y):
        obj = evt.GetObject()
        name = obj.GetName()
        grid = wx.FindWindowByName(name)
        x, y = grid.CalcUnscrolledPosition(x, y)
        return grid.XToCol(x),grid.YToRow(y)

        
class PasswordDialog(wx.Dialog):
    def __init__(self, operator='clerk', debug=False):
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
        super(PasswordDialog, self).__init__(parent=None, title='Authorization?',size=(200,90),style=style)
        
        self.op = operator.upper()
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        row1Sizer = wx.BoxSizer(wx.VERTICAL)
        row2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        ctrl = RH_TextCtrl(self, -1, 
                           name='password_txtctrl', 
                           size=(125,-1), 
                           style=wx.TE_PASSWORD|wx.TE_PROCESS_ENTER)
        
        ctrl.Bind(wx.EVT_TEXT_ENTER, self.OnPassword)
        ctrl.SetFocus()
        
        row1Sizer.Add(ctrl, 0, wx.ALL | wx.ALIGN_CENTER, 3)
        
        btn_list = [('Cancel', 'password_cancel_button')]
        
        for label, name in btn_list:
            btn = RH_Button(self, -1, label=label, name=name)
            btn.Bind(wx.EVT_BUTTON, self.ButtonAction)
            
            row2Sizer.Add(btn, 0, wx.ALL|wx.ALIGN_CENTER, 3)
            
        
    
        MainSizer.Add(row1Sizer, 0, wx.ALL | wx.ALIGN_CENTER, 3)
        MainSizer.Add(row2Sizer, 0, wx.ALL| wx.ALIGN_CENTER, 3)
        
        self.SetSizer(MainSizer, 0)
        self.Layout()
    
   # def Operator(self, auth):
   #     self.op = auth
        
    
    def OnPassword(self, event):
        obj = event.GetEventObject()
        named = obj.GetName()
        value = obj.GetValue().strip().lower()
        admin = LookupDB('passwords').Specific('rhp','abuser','admin_key')[0].lower()
        print(f'Admin Key : {admin}')
        manager = LookupDB('passwords').Specific('rhp','abuser','manager_key')[0].lower()
        print(f'Manager Key : {manager}')
        clerk = LookupDB('passwords').Specific('rhp','abuser','clerk_key')[0].lower()
        print(f'Clerk Key : {clerk}')
        self.passwordOK = False
        
        if self.op == 'CLERK':
            if value == manager or value == admin or value == clerk:
                self.passwordOK = True 
              
        if self.op == 'MANAGER':
            if value == manager or value == admin:
                self.passwordOK = True        
        
        if self.op == 'ADMIN':
            if value == admin:
                self.passwordOK = True

        if self.passwordOK is False:
            #box = wx.FindWindowByName('password_txtctrl')
            wx.FindWindowByName('password_txtctrl').SetCtrl('')
        
        if self.passwordOK is True:
            self.Close()

            
    def ButtonAction(self, event):
        obj = event.GetEventObject()
        name = obj.GetName()
        self.passwordOK = False
        
        if 'cancel' in name:
            self.Close()
            

                
class DiscountDialog(wx.Dialog):
    def __init__(self, debug=False):
        super(DiscountDialog, self).__init__(*args,**kw)
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        row0Sizer = wx.BoxSizer(wx.HORIZONTAL)
        row1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        row2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        rb = wx.RadioBox(self, -1, 
                         choices=[], 
                         name='discounts_choices_radiobox', 
                         label='Discount Types',
                         style=wx.RA_SPECIFY_COLS) 
        
        row0Sizer.Add(rb, 0, wx.ALL, 3)                           
        ctrl = RH_TextCtrl(self, -1,
                           name='discount_disc_textctrl',
                           style=wx.TE_RIGHT)
        ctrl.Bind(wx.EVT_KILL_FOCUS, EventOps().OnNumbersOnly)
        
        ctrl.SetFocus()                     
        txt = wx.StaticText(self, -1, 
                            label='%')
        
        font = wx.Font(wx.FontInfo(16))
        txt.SetFont(font)
                                   
        row1Sizer.Add(ctrl,0,wx.ALL|wx.CENTER, 3) 
        row1Sizer.Add(txt,0)
        button_list = [('discount_ok_button','&OK',self.OnOK),
                       ('discount_cancel_button','&Cancel',self.OnCancel)]                       
        
        for name, label, hdlr in button_list:
            btn = RH_Button(self, -1, label=label, name=name)
            btn.Bind(wx.EVT_BUTTON, hdlr)
            row2Sizer.Add(btn,0,wx.ALL, 5)
        
        MainSizer.Add(row0Sizer, 0, wx.ALL|wx.CENTER, 3)                          
        MainSizer.Add(row1Sizer, 0,wx.ALL|wx.CENTER, 3)
        MainSizer.Add(row2Sizer, 0, wx.ALL|wx.CENTER, 3)
        
        self.SetSizer(MainSizer, 0)        
        self.Layout()
    
        wx.CallAfter(self.OnLoad, event='')
        
    def OnLoad(self, event):
        
        query = 'SELECT name, percent FROM discount_options'
        data = ''
        returnd = SQConnect(query,data).ALL()
        choices = []
         
        for name, percent in returnd:
            titl = '{} : {}%'.format(name, percent)
            choices.append(titl)
        
        
            
        rb = wx.FindWindowByName('discounts_choices_radiobox')
        for idx, item in enumerate(choices): 
            print('idx : {} ; item : {} '.format(idx,item))
            rb.SetString(idx, item)
           
    def OnOK(self,event):
        self.discountamt = wx.FindWindowByName('discount_disc_textctrl').GetCtrl()
        self.Close()
        
    def OnCancel(self, event):
        self.discountamt = wx.FindWindowByName('discount_disc_textctrl').GetCtrl()
        self.Close()




####---- Flash Item Add
class FlashAddInventory(wx.Dialog):
    def __init__(self, *args, **kw): 
        super(FlashAddInventory, self).__init__(*args, **kw) 
        
        obj = self.GetParent()
        print('\033[92m OBJ : {0} \033[0m'.format(obj))
         
        # 8 Rows
        FlashCreateSizer = wx.BoxSizer(wx.VERTICAL)
        row1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        row1_list = (('Item Number','flashadd_itemNumber_txtctrl',250),('Description','flashadd_itemDescription_txtctrl',500))
        for label,name,sized in row1_list:
            box = wx.StaticBox(self, -1, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            if 'txtctrl' in name:
                if 'itemNumber' in name:
                    ctrl = masked.TextCtrl(self, -1, name=name, size=(sized, -1), formatcodes="!")
                    ctrl.Bind(wx.EVT_KEY_DOWN, self.onCatchKey)
                else:
                    ctrl = RH_TextCtrl(self, -1, name=name, size=(sized, -1))
                    ctrl.Bind(wx.EVT_KILL_FOCUS, EventOps().CheckMeasurements)
            if 'agepopup' in name:
                ctrl = masked.NumCtrl(self, -1, name=name, value='00', integerWidth=2, fractionWidth=0)
            if 'agepopup' in name:
                boxSizer.Add(ctrl, 0, wx.ALL, 20)            
            else:
                boxSizer.Add(ctrl, 0, wx.ALL, 3)
            if 'itemNumber' in name:
                ctrl.SetFocus()
            row1Sizer.Add(boxSizer, 0, wx.ALL, 3)
             
        
        row2Sizer = wx.BoxSizer(wx.HORIZONTAL)

        
        row2_list = [('Unit Cost','flashadd_avgcost_numctrl',50),
                     ('Department','flashadd_department_combobox',150),('Category','flashadd_category_combobox',150),
                     ('Subcategory','flashadd_subCategory_combobox',150),('Weight','flashadd_weight_numctrl',75),
                     ('Tare Weight','flashadd_tareWeight_numctrl',75)]
        for label,name,sized in row2_list:
            box = wx.StaticBox(self, -1, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            if 'numctrl' in name:
                ctrl = masked.NumCtrl(self, -1, value=0, name=name, integerWidth=9, fractionWidth=3)
            if 'combobox' in name:
                ctrl = masked.ComboBox(self, -1, name=name, choices=[], size=(sized,-1))
            boxSizer.Add(ctrl, 0, wx.ALL,3)
            row2Sizer.Add(boxSizer, 0, wx.ALL, 3)                     
        
        
        row3Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        query = "SELECT name,scheme_list,reduce_by from item_pricing_schemes"
        data = ''
        returnd = SQConnect(query, data).ALL()
        
        
        
        priceschema_list = returnd
        
        box = wx.StaticBox(self, label="Pricing\nSchemes")
        boxSizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        boxSizer.Add((20,20), 0)
        xx=0  
        btn = RH_Button(self, id=wx.ID_ANY, label="RESET", name="details_pricescema_RESET_button")
        btn.Bind(wx.EVT_BUTTON, self.OnPriceSchemes)        
        boxSizer.Add(btn, 0)
               
        for label, scheme_list, reduce_by in priceschema_list:
            btn = RH_Button(self, id=wx.ID_ANY, label=label, name=scheme_list)
            btn.Bind(wx.EVT_BUTTON, self.OnPriceSchemes)        
            boxSizer.Add(btn, 0)
            xx+=1            
        
                
        row3Sizer.Add(boxSizer, 0)
      
        
        grid = Retail_Grid(self, name="flashadd_cost_grid")
         
        row3Sizer.Add(grid, 0)
        
        row3bSizer = wx.BoxSizer(wx.VERTICAL)
        
        itemType_choices = ['Controlled','Non-Controlled','Matrixed','BOM','Tag Along','Serial No. Track','Mfg Coupon']
        posOptions_choices = ['Prompt for Quantity','Assume 1 Sold','Prompt for price - Quantity Calculated','Prompt for scale']
        
        row3_list = [('Item Type','flashadd_itemType_radiobox',itemType_choices),
                     ('POS Options','flashadd_posOptions_radiobox', posOptions_choices)]
        for label,name,choices in row3_list:
            ctrl = wx.RadioBox(self, -1, label=label, name=name, choices=choices, style=wx.RA_SPECIFY_ROWS)
            row3bSizer.Add(ctrl, 0, wx.ALL, 3)
        
        row3Sizer.Add(row3bSizer, 0, wx.ALL, 3)        
            
        row4Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
         
        #ctrl = wx.RadioBox(self, -1, label='POS Options', name='flashadd_posOptions_radiobox', choices=posOptions_choices)
        #row4Sizer.Add(ctrl, 0, wx.ALL, 3)
        
        row5Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
                      
        row5_list = [('QOH','flashadd_quantityOnHand_numctrl',0),('Units in Package','flashadd_unitsInPackage_numctrl',1),
                     ('Override Tax Rate','flashadd_overrideTaxRate_numctrl',0)]
        
        for label, name, sized in row5_list:
            box = wx.StaticBox(self, -1, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            if 'numctrl' in name:
                if re.search('(quantity|units)',name,re.I):
                    ctrl = masked.NumCtrl(self, -1, value=sized, name=name, integerWidth=5, fractionWidth=0)
                if 'override' in name:
                    ctrl = masked.NumCtrl(self, -1, value=0, name=name, integerWidth=3, fractionWidth=3)
            boxSizer.Add(ctrl, 0, wx.ALL, 7)
            row5Sizer.Add(boxSizer, 0, wx.ALL, 3)
            
        taxExemptions_list = [('1','flashadd_taxlvl1_checkbox'),('2','flashadd_taxlvl2_checkbox'),('3','flashadd_taxlvl3_checkbox'),
                             ('4','flashadd_taxlvl4_checkbox'),('Never','flashadd_taxlvlNever_checkbox')]
        
        box = wx.StaticBox(self, -1, label='Tax Level Exemptions')
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        for labeld, named in taxExemptions_list:
            ctrl = RH_CheckBox(self, label=labeld, name=named)
            boxSizer.Add(ctrl, 0, wx.ALL, 3)
        
        row5Sizer.Add(boxSizer, 0, wx.ALL, 3)                                         
        
       
        row6Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        row6_list = [('Vendor Number','flashadd_vendorNum_txtctrl',40),
                     ('Vendor Name','flashadd_vendorName_txtctrl',150)]
        
        box = wx.StaticBox(self, -1, label='Order Number')
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        ctrl = masked.TextCtrl(self, -1, name='flashadd_orderNumber_txtctrl', size=(90,-1),formatcodes='!')
        boxSizer.Add(ctrl, 0, wx.ALL, 3)
        row6Sizer.Add(boxSizer, 0, wx.ALL, 3)
        row5Sizer.Add(row6Sizer, 0,wx.ALL, 3)
        
        box = wx.StaticBox(self, -1, label='Vendor Info')
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        for label, name, sized in row6_list:
            if 'vendorName' in name:
                vendFind = wx.BitmapButton(self, -1, wx.Bitmap(ButtonOps().Icons('Find', 16)))
                vendFind.Bind(wx.EVT_BUTTON, self.onFindVendor)
                boxSizer.Add(vendFind, 0, wx.ALL, 3)
            
            ctrl = RH_TextCtrl(self, -1, name=name, size=(sized,-1))
            if 'vendorName' in name:
                ctrl.SetEditable(False)
                
            boxSizer.Add(ctrl, 0, wx.ALL, 3)
            
        row6Sizer.Add(boxSizer, 0, wx.ALL, 3)
        
                
        row8Sizer = wx.BoxSizer(wx.HORIZONTAL)

        row8_list = [('&ACCEPT','flashadd_accept_button',self.OnAccept),('&CANCEL','flashadd_cancel_button',self.OnCancel)]
        for label, name, hndlr in row8_list:
            ctrl = RH_Button(self, label=label, name=name, size=(90,40))
            ctrl.Bind(wx.EVT_BUTTON, hndlr)
            if 'cancel' in name:
                row8Sizer.Add((80,10),0)
                
            row8Sizer.Add(ctrl, 0, wx.ALL, 3)
            
        sizer_list = [row1Sizer, row2Sizer, row3Sizer, row4Sizer, row5Sizer,  row8Sizer]
        for sizer in sizer_list :
            FlashCreateSizer.Add((5,10),0, wx.ALL, )
            FlashCreateSizer.Add(sizer, 0, wx.ALL|wx.ALIGN_CENTER, 3)
            
       
        self.SetSizer(FlashCreateSizer,0)
        # order = ('flashadd_itemNumber__txtctrl','flashadd_itemDescription_txtctrl','flashadd_department_combobox','flashadd_category_combobox','flashadd_subCategory_combobox')
        # for i in range(len(order) - 1):
        #     ctrl1 = wx.FindWindowByName(order[i])
        #     ctrl2 = wx.FindWindowByName(order[i+1])
            
        #     ctrl2.MoveAfterInTabOrder(ctrl1)
    
        wx.CallAfter(self.OnLoad, event='')
    
    def onCatchKey(self, event):
       
        keycode = event.GetKeyCode()
        if keycode in [wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER, wx.WXK_TAB]:
            self.CheckExists(event=None)
            event.EventObject.Navigate()

        event.Skip()

    
    def CheckExists(self, event):
        name = 'flashadd_itemNumber_txtctrl'
        upc = wx.FindWindowByName(name).GetCtrl()
        
        query = 'SELECT upc, description FROM item_detailed WHERE upc=(?)'
        data = (upc,)
        returnd = SQConnect(query, data).ONE()
        
        if returnd is not None:
            wx.MessageBox('Item Number already in use','Add Item', wx.OK)
            self.Close()
        
        item = wx.FindWindowByName('flashadd_itemDescription_txtctrl').SetFocus()    
        
    
    def OnPriceSchemes(self, event):
       
        grid = wx.FindWindowByName('flashadd_cost_grid')
        WhichScheme = event.GetEventObject()
        
        Scheme_Name = WhichScheme.GetLabel()    
        Scheme_List = WhichScheme.GetName().split("-")          #['1','7','15']
        if Scheme_Name == 'RESET':
            
            reset_list = [('Unit','1'),('Price','0.00'),('Margin %','0.0000')]
            for xx in range(grid.GetNumberRows()):
                fillgrid = GridOps(grid.GetName()).FillGrid(reset_list,row=xx)
                
        else:
            
            if 'PK' in Scheme_List:
                (each, pack, bulk) = Scheme_List
                
                UIPctrl = wx.FindWindowByName('flashadd_unitsInPackage_numctrl').GetValue()
                if not UIPctrl:
                    UIPctrl = 1
                if Decimal(UIPctrl) == Decimal(each):
                    UIPctrl = Decimal(each)*2    
                Bulkd = Decimal(UIPctrl) * Decimal(bulk.strip('X'))
                
                Scheme_List = str(each),str(UIPctrl),str(Bulkd)
                        
            avgCostL = wx.FindWindowByName('flashadd_avgcost_numctrl').GetValue()
            
            query = "SELECT reduce_by from item_pricing_schemes WHERE name=?"
            data = (Scheme_Name,)
            returnd = SQConnect(query, data).ONE()
            Reduceby = returnd
            
            startingMargin_L = '50'
            
            if Decimal(avgCostL) == 0:
                wx.MessageBox('Average Cost Not Set','Info',wx.OK)
                return    
            Schemed = Pricing('C',Scheme_List,Reduceby,avgCostL,startingMargin_L,avgCostL)
            #Debugger('{0}\n Price {1}\n Size of {2}'.format('** Schemed Test Run **',Schemed.Scheme(),len(Schemed.Scheme())))
            schemeLen = len(Schemed.Scheme())
            priceScheme_dict = Schemed.Scheme()
            
            xx = 0
        
            for key in Scheme_List:
                setList = [('Unit',key),('Price',str(Decimal(priceScheme_dict[key][0]))),
                           ('Margin %',str(Decimal(priceScheme_dict[key][1])))]
                fillGrid = GridOps(grid.GetName()).FillGrid(setList,row=xx)           
                xx += 1

    
    
    def OnCellChange(self, event):
       
        
        
        obj = event.GetEventObject()
        named = obj.GetName()
        row = event.GetRow()
        col = event.GetCol()
        
        grid = wx.FindWindowByName(named)
        colname = grid.GetColLabelValue(col)
        grid.Refresh()
        
        if 'details_cost_grid' in named:
            raw_value = grid.GetCellValue(row,col).strip()
            # numeric check
            if all(x in '0123456789.+-' for x in raw_value):
                # convert to float and limit to 2 decimals
                value = Decimal(raw_value)
                if colname == 'Unit':
                    valued = RetailOps().DoRound(value,'1')
                else:
                    valued = RetailOps().DoRound(value,'1.00')
                grid.SetCellValue(row,col,str(valued))
            else:
                basic_list = ['1','$0.00','Margin','0.0000']
                grid.SetCellValue(row,col,basic_list[col])
                GridOps(grid.GetName()).GridFocusNGo(row, col)
                return
            
        #
        
        avgcost = wx.FindWindowByName('flashadd_avgcost_numctrl').GetValue()
        
        
        for yy in range(grid.GetNumberCols()):
            header = grid.GetColLabelValue(yy)
            if 'Unit' in header:
                unit = grid.GetCellValue(row,yy)
            if 'Markup %' in header:
                calcMargin = grid.GetCellValue(row,yy)
            if 'Price' in header:
                retail_from = grid.GetCellValue(row,yy)
                  
            
        if colname == 'Markup %':
            newretail_almost = RetailOps().DoMargin(avgcost,calcMargin,unit) 
            newretail = RetailOps().DoRound(newretail_almost,'1.00')
            newMargin = RetailOps().DoRound(calcMargin,'1.0000') 
            
            set_values = [('Price',newretail),('Markup %',newMargin)]
            
            fillgrid = GridOps(grid.GetName()).FillGrid(set_valuesrow=row)
            
        if colname == 'Price':
            grossMargin = RetailOps().GetMargin(avgcost,retail_from,unit)
            Margindot4 = RetailOps().DoRound(grossMargin,'1.0000') 
            
            grid.SetCellValue(row,3,str(Margindot4))
        
        if colname == 'Unit':
            
            newretail_almost = RetailOps().DoMargin(avgcost,calcMargin,unit)
            newretail = RetailOps().DoRound(newretail_almost, '1.00')
            
            grid.SetCellValue(row,1,str(newretail))
        
        
    def onFindVendor(self, event):
       
        pass
        
    
    def OnAccept(self, event):
       
        ItemNumberd = wx.FindWindowByName('flashadd_itemNumber_txtctrl').GetValue().upper().strip()
        
        table_list = ['item_options','item_detailed','item_detailed2','item_vendor_data','item_notes','item_sales_links','item_cust_instructions','item_options','item_history','item_retails']
        QueryOps().CheckEntryExist('upc',ItemNumberd,table_list)
        
        grid = wx.FindWindowByName('flashadd_cost_grid').OnSave(upc=ItemNumberd)
        
        flashadd_list = [('flashadd_itemDescription_txtctrl','item_detailed','description'),
                         ('flashadd_avgcost_numctrl','item_detailed','avg_cost'),
                         ('flashadd_department_combobox','item_options','department'),('flashadd_category_combobox','item_options','category'),
                         ('flashadd_subCategory_combobox','item_options','subcategory'),('flashadd_weight_numctrl','item_detailed2','weight'),
                         ('flashadd_itemType_radiobox','item_options','item_type'),('flashadd_tareWeight_numctrl','item_detailed2','tare_weight'),
                         ('flashadd_posOptions_radiobox','item_options','posoptions'),('flashadd_quantityOnHand_numctrl','item_detailed','quantity_on_hand'),
                         ('flashadd_unitsInPackage_numctrl','item_options','unitsinpackage'),('flashadd_overrideTaxRate_numctrl','item_detailed2','override_tax_rate'),
                         ('flashadd_taxlvl1_checkbox','item_detailed2','tax1'),('flashadd_taxlvl2_checkbox','item_detailed2','tax2'),
                         ('flashadd_taxlvl3_checkbox','item_detailed2','tax3'),('flashadd_taxlvl4_checkbox','item_detailed2','tax4'),
                         ('flashadd_taxlvlNever_checkbox','item_detailed2','tax_never'),('flashadd_vendorNum_txtctrl','item_vendor_data','vendor1_num'),
                         ('flashadd_orderNumber_txtctrl','item_vendor_data','vendor1_num')]
        #                 
        for name, table, column_header in flashadd_list:
            itemValue = wx.FindWindowByName(name).GetCtrl()
            if 'vendor_data' in table:
                vendor_set = ['vendor1','vendor2','vendor3','vendor4','vendor5','vendor6']
                vendor_info = {}
                    
                for numvend in vendor_set: 
                    vendorID = numvend
                    vendor_info[vendorID]={}
                
                    if vendorID == 'vendor1':
                        vendorOrderNum = wx.FindWindowByName('flashadd_orderNumber_txtctrl').GetValue()
                        vendorNum = wx.FindWindowByName('flashadd_vendorNum_txtctrl').GetValue()
                    else:
                        vendorOrderNum = ''
                        vendorNum = ''
                        
                    vendor_save_list = [(vendorNum,'vendor_num'),('','vendor_name'),
                                        ('','last_retail'),(vendorOrderNum,'order_num'),
                                        ('','last_units_ordered'),('','leadtime'),
                                        ('','minimum_order'),('','last_ordered'),
                                        ('','last_order_date'),('','outstanding')]
                    for vendvalue, vendkey in vendor_save_list:
                        vendor_info[vendorID][vendkey] = vendvalue
            
                itemValue = json.dumps(vendor_info)
            
                   
                
            
            
            RecordOps('item_detailed2').UpdateRecordDate('added_date','upc',ItemNumberd)
            
            query = 'UPDATE {0} SET {1}=? WHERE upc=?'.format(table, column_header)
            data = (itemValue,ItemNumberd,)
            call_db = SQConnect(query, data).ONE()
            
            
    
            self.itemPicked = ItemNumberd
            self.Close()
    
    
    
    def OnCancel(self, event):
       
        self.Close()
    
    def OnLoad(self, event):
       
        load_combobox_list = [('department','flashadd_department_combobox'),
                              ('category','flashadd_category_combobox'),
                              ('subcategory','flashadd_subCategory_combobox')]
        for field, name in load_combobox_list:
            query = "SELECT {0} FROM organizations WHERE abuser='rhp'".format(field)
            data = ''
            returnd = SQConnect(query, data).ALL()
            
            choice_list = []
            
            choice_list = returnd[0]
            item = wx.FindWindowByName(name).SetItems(choice_list)
            



class PayByDialog(wx.Dialog):  
    def __init__(self, parent, title, debug=False):
        super(PayByDialog, self).__init__(parent=parent, size=(500,500), title=title)
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
            
        if 'Cash' in title:
            btn_list = [('Give Change', 'paybyDialog_giveChange_btn', self.CashGiveChange),('Keep on Account','paybyDialog_keepOnAcct_btn', self.KeepOnAcct)]
            for label, name, hdlr in btn_list:
                btn = RH_Button(self, -1, label=label, name=name)
                btn.Bind(wx.EVT_BUTTON, hdlr)
                MainSizer.Add(btn, 0, wx.ALL|wx.ALIGN_CENTER, 25)        
        
        if 'Check' in title:
            ctrl_list = [('Check #','paybyDialog_checkNum_txtctrl')]
        
        if 'Card' in title:
            pass    

        
        self.SetSizer(MainSizer, 0)
        self.Layout()

    def CashGiveChange(self, event):
        pass
    
    def KeepOnAcct(self, event):
        pass
    
    
        
class CustLookupDialog(wx.Dialog):
    style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
    def __init__(self, parent, size=(1150,700), title="Customer Lookup"):
        super(CustLookupDialog, self).__init__(parent=parent, size=size, title=title)
        self.InitUI()
        
        
    def InitUI(self):
       
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        
        level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        lookup_list = [('First Name Lookup', self.OnSearchFName, 'fname_lookup_txtctrl1','Enter 2+ letters of the First Name Only without punctuation',),
                       ('Last Name Lookup', self.OnSearchLName, 'lname_lookup_txtctrl1','Enter 2+ letters of the Last Name Only without punctuation'),
                       ('Phone Lookup', self.OnSearchPhone, 'phone_lookup_txtctrl1','Enter Numbers Only, i.e. 3867752794'),
                       ('Street Name - Address Lookup', self.OnSearchAddress, 'address_lookup_txtctrl1', 'Enter Street Name Only')]
        
        for label,handlr,name,tooltip in lookup_list:
            box = wx.StaticBox(self, -1, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            
            if 'Phone Lookup' in label:
                lookup_txtctrl = RH_MTextCtrl(self, -1, name=name, size=(160,-1), mask='(###) ###-####', style=wx.TE_PROCESS_ENTER)
            else:    
                lookup_txtctrl = RH_TextCtrl(self, -1, name=name, size=(160,-1), style=wx.TE_PROCESS_ENTER)
            
            lookup_txtctrl.SetToolTip(wx.ToolTip(tooltip))
            lookup_txtctrl.Bind(wx.EVT_TEXT_ENTER, handlr)
            if 'First Name' in label:
                lookup_txtctrl.SetFocus()
            
            lookup_button = RH_Button(self, -1, label="Search")
            lookup_button.Bind(wx.EVT_BUTTON, handlr)
            
            boxSizer.Add(lookup_txtctrl, 0, wx.ALL, 3)
            boxSizer.Add(lookup_button, 0, wx.ALL, 3)
            
            level1Sizer.Add(boxSizer, 0, wx.ALL, 5)              
        
        level2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        lc = RH_OLV(self, -1, name='name_lc', size=(1100,500),style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        lc.SetColumns([
                    ColumnDefn('Account #','center',120,'acctNum'),
                    ColumnDefn('Name','left',290,'named'),
                    ColumnDefn('Address 1','left',280,'address1d'),
                    ColumnDefn('Address 2','left',160,'address2d'),
                    ColumnDefn('City','left',120,'cityd'),
                    ColumnDefn('State','left',80,'stated')
                    ])
        
        lc.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.LookupOnCellLeftClick)
               
        level2Sizer.Add(lc, 0)
        
        level3Sizer = wx.BoxSizer(wx.HORIZONTAL)
        numberofcust = wx.StaticText(self, -1, label='Number Here')
        
        return_count = QueryOps().QueryCheck('customer_basic_info')
        
        CustomerCount = "Number of Customers : {0}".format(return_count)
        numberofcust.SetLabel(CustomerCount)
        
       
        level3Sizer.Add(numberofcust, 0, wx.ALL|wx.EXPAND, 5)
        result_text = wx.StaticText(self, -1,label='',name='custLookup_result_text') 
       
        MainSizer.Add(level1Sizer, 0)
        MainSizer.Add(result_text, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        MainSizer.Add(level2Sizer, 0, wx.ALL|wx.ALIGN_CENTER,5)
        MainSizer.Add(level3Sizer, 1, wx.ALL|wx.EXPAND|wx.ALIGN_BOTTOM, 10)
        self.SetSizer(MainSizer, 0)
        self.Layout()
        
    def LookupOnCellLeftClick(self, evt):
       
        item_id,objText = EventOps().LCGetSelected(evt)
        self.itemPicked = objText
        
        if re.match('[A-Z0-9]',self.itemPicked,re.I):
            self.Close()
        
       
    def OnSearchFName(self, event):
       
        cell_color = Themes().GetColor('cell')
        
        fname = wx.FindWindowByName('fname_lookup_txtctrl1').GetCtrl()
        query = "SELECT cust_num,first_name,last_name,address_acct_num from customer_basic_info where first_name LIKE ?" 
        data = (fname,)
        returnd = SQConnect(query, data).ALL()
        pout.v(returnd)
        
        if returnd is None or len(returnd) == 0:
            wx.MessageBox('First Name Not Found.','Customer Lookup by First Name', wx.OK)
            return
            
        
        #returnd.sort(key=itemgetter(1))
        pout.v(f'A Customer : {returnd}')
        pout.v(returnd[0][1])
        
        
        
        results = 'Found {0} Record(s)'.format(len(returnd))
        item = wx.FindWindowByName('custLookup_result_text').SetCtrl(results)
        lc = wx.FindWindowByName('name_lc')
        lc.DeleteAllItems()
        xx=0  
        idx = 0
        cell_color = Themes('Customers').GetColor('cell')
            
        for row in returnd:
            pout.v(f'row : {row}')
            cust_numd, first_named, last_named, addr_acct_numd = row
            fullName = ''         
            if first_named:
                fullName += '{0} '.format(first_named)
            if last_named:
                fullName += '{0} '.format(last_named)    
                                
            
            startTime = datetime.datetime.now()
            
            address0 = address2 = city = state = ''
            if addr_acct_numd != '' or len(addr_acct_numd) > 0:
                # query = 'SELECT address0,address2,city,state FROM address_accounts WHERE addr_acct_num=?'
                # data = (addr_acct_numd,)
                # returnd = SQConnect(query, data).ONE()
                returnd = LookupDB('address_accounts').Specific(addr_acct_numd, 'addr_acct_num','address0, address2, city, state')
                try:
                    address0,address2,city,state = returnd
                except:
                    pout.v(f'Address Output : {returnd}')
            
            #MO().timeStages('Search single letter',startTime)
                
            
            setList = [(0,cust_numd),(1,fullName),(2,address0),(3,address2),(4,city),(5,state)]
            ListCtrl_Ops('name_lc').LCFill(setList,idx)
            xx += 1
        
        ListCtrl_Ops('name_lc').LCAlternateColor(xx)
                
        lc.SetFocus()    
        lc.Select(0)
    
    def OnSearchLName(self, event):
       
        cell_color = Themes().GetColor('cell')
        
        lname = wx.FindWindowByName('lname_lookup_txtctrl1').GetCtrl()
        query = "SELECT cust_num,first_name,last_name,address_acct_num from customer_basic_info where last_name like ?" 
        data = (lname,)
        returnd = SQConnect(query, data).ALL()
        #returnd = list(returnd)
        
        
        
        if returnd is None or len(returnd) == 0:
            wx.MessageBox('Last Name Not Found.','Customer Lookup by Last Name', wx.OK)
            return
        
        returnd.sort(key=itemgetter(2))
        
        results = 'Found {0} Record(s)'.format(returnd_count)
        item = wx.FindWindowByName('custLookup_result_text').SetLabel(results)
        lc = wx.FindWindowByName('name_lc')
        lc.DeleteAllItems()
        xx=0 
                  
        for cust_numd, first_named, last_named, addr_acct_numd, in returnd:
            fullName = ''         
            if first_named:
                fullName += '{0} '.format(first_named)
            if last_named:
                fullName += '{0} '.format(last_named)    
            
            address0 = address2 = city = state = ''
            if addr_acct_numd != '' or len(addr_acct_numd) > 0:
                query = 'SELECT address0,address2,city,state FROM address_accounts WHERE addr_acct_num=?'
                data = (addr_acct_numd,)
                returnd = SQConnect(query, data).ONE()
            
                (address0,address2,city,state) = returnd
            
                                
            set_list = [(0,cust_numd),(1,fullName),(2,address0),(3,address2),(4,city),(5,state)]
            ListCtrl_Ops('name_lc').LCFill(set_list, xx)
            xx += 1
        
        ListCtrl_Ops('name_lc').LCAlternateColor(xx)        
                
        lc.SetFocus()
        lc.Select(0)
        
    def OnSearchPhone(self, event):
       
        cell_color = Themes().GetColor('cell')
        
        ph_num = wx.FindWindowByName('phone_lookup_txtctrl1').GetValue()
        
        if not len(ph_num) >= 3:
            return
        
        query = "SELECT cust_num,first_name,last_name,address_acct_num from customer_basic_info where phone_numbers like ?" 
        data = ('%'+ph_num+'%',)
        returnd = SQConnect(query, data).ALL()
        
        
        if returnd is None or len(returnd) == 0:
            wx.MessageBox('Phone Number Not Found.','Customer Lookup by Phone Number', wx.OK)
            return

        returnd.sort()
        results = 'Found {0} Record(s)'.format(returnd_count)
        item = wx.FindWindowByName('custLookup_result_text').SetLabel(results)
        lc = wx.FindWindowByName('name_lc')
        lc.DeleteAllItems()    
        xx=0  
        
        for cust_numd, first_named, last_named, addr_acct_numd, in returnd:
            fullName = ''         
            if first_named:
                fullName += '{0} '.format(first_named)
            if last_named:
                fullName += '{0} '.format(last_named)    
            
            setList = [('Acct Number',cust_numd),('Name',fullName)]
            
            lc.InsertItem(xx, cust_numd)
            lc.SetItem(xx,1,fullName)
            search_list = [('address0','Address 1'),('address2','Address 2'),('city','City'),('state','State')]
            for field, title in search_list:
                address0 = address2 = city = state = ''
                if addr_acct_numd != '' or len(addr_acct_numd) > 0:
                    query = 'SELECT address0,address2,city,state FROM address_accounts WHERE addr_acct_num=?'
                    data = (addr_acct_numd,)
                    returnd = SQConnect(query, data).ONE()
                    
                    (address0,address2,city,state) = returnd
                
                setList = [(0,cust_numd),(1,fullName),(2,address0),(3,address2),(4, city),(5,state)]
                ListCtrl_Ops('name_lc').LCFill(setList,xx)
                
            xx += 1
        
        ListCtrl_Ops('name_lc').LCAlternateColor(xx)   
        lc.SetFocus()
        lc.Select(0)
        
    def OnSearchAddress(self, event):
        obj = event.GetEventObject()
        
        cell_color = Themes().GetColor('cell')
        
        addrname = obj.GetCtrl()
        if not len(addrname) >= 3:
            return
        
        query = "SELECT addr_acct_num from address_accounts where street_name like ?" 
        data = ('%'+addrname+'%',)
        call_db = SQConnect(query, data)
        returnd = call_db.ALL()
        
        if returnd is None or len(returnd) == 0:
            wx.MessageBox('Street Name Not Found.','Customer Lookup by Street Name', wx.OK)
            return
            
        results = 'Found {0} Record(s)'.format(returnd_count)
        item = wx.FindWindowByName('custLookup_result_text').SetLabel(results)
        lc = wx.FindWindowByName('name_lc')
        lc.DeleteAllItems()
        xx=0           
        dict_xx = 0
        cust_dict = {}
        
            
            
        for address_acct in returnd_list:
            
            query = "SELECT cust_num,first_name,last_name,address_acct_num from customer_basic_info WHERE address_acct_num=?"
            data = (address_acct,)
            cust_returnd = SQConnect(query, data).ALL()
            cust_returnd = list(cust_returnd)
            cust_returnd.sort(key=itemgetter(2))
            cust_returnd_count = len(cust_returnd)
            
            
            
            if cust_returnd_count == 0:
                continue
                
            (cust_numd, first_named, last_named, addr_acct_numd) = cust_returnd[0]
            fullName = ''         
            if first_named:
                fullName += '{0} '.format(first_named)
            if last_named:
                fullName += '{0} '.format(last_named)    
            
            setList = [('Acct Number',cust_numd),('Name',fullName)]
            #GO(grid.GetName()).FillGrid(setList,xx)
            address0 = address2 = city = state = ''
            if addr_acct_numd != '' or len(addr_acct_numd) > 0:
                query = 'SELECT address0,address2,city,state FROM address_accounts WHERE addr_acct_num=?'
                data = (addr_acct_numd,)
                returnd = SQConnect(query, data).ONE()
                (address0,address2,city,state) = returnd
                    
            setList = [(0,cust_numd),(1,fullName),(2,address0),(3,address2),(4,city),(5,state)]
            ListCtrl_Ops('name_lc').LCFill(setList,xx)
            xx += 1
        
        ListCtrl_Ops('name_lc').LCAlternateColor(xx)
                
        lc.SetFocus()
        lc.Select(0)
        
#-------------------------
##
## Item Inquiry
##
##-----------------------
class ItemInquiryDialog(wx.Dialog):
    def __init__(self, debug=False, *args,**kw):
        super(ItemInquiryDialog, self).__init__(size=(825,700),*args, **kw)
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        lookupSizer = wx.BoxSizer(wx.VERTICAL)
        
        basePath = os.path.dirname(os.path.realpath(__file__))+'/' 
        IconBar_list =[('FindButton',ButtonOps().Icons('Find'),self.OnFind),
                       ('ExitButton', ButtonOps().Icons('Exit'),self.OnExitButton)]
        
        IconBox = wx.StaticBox(self)
        
        IconBarSizer = wx.StaticBoxSizer(IconBox, wx.HORIZONTAL)        
        xx = 0        
        for name,iconloc,handler in IconBar_list:
            icon = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(iconloc), name=name, style=wx.BORDER_NONE)
            if 'Find' in name:
                randomId = wx.NewId()   
                self.Bind(wx.EVT_MENU, handler, id=randomId)
                accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('f'), randomId)])
                self.SetAcceleratorTable(accel_tbl)
               
            icon.Bind(wx.EVT_BUTTON, handler)
                    
            IconBarSizer.Add((80,1),0)
            if re.search('(Save|Delete|Add)',name,re.I):
                icon.Disable()
            if 'Left' in name or 'Right' in name:
                IconBarSizer.Add(icon,0)
            elif 'Exit' in name:
                IconBarSizer.Add((150,10), 1)
                IconBarSizer.Add(icon, 0)
            else:
                if xx > 0:
                    IconBarSizer.Add((5,1), 0)
                    IconBarSizer.Add(wx.StaticLine(self, -1, size=(1,35),style=wx.LI_VERTICAL),  0)
                
                IconBarSizer.Add((5,1), 0)
                IconBarSizer.Add(icon, 0)
            xx += 1
        lookupSizer.Add(IconBarSizer, 0, wx.ALL|wx.EXPAND, 3)
        #lookupSizer.Add((10,10), 0)    
        
        level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        level1_list = [('Item Number', 'itemInq_itemNumber_txtctrl',230),('Description','itemInq_description_txtctrl',450)]
        for label,name,sized in level1_list:
            box = wx.StaticBox(self, -1, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            if 'itemNumber' in name:
                ctrl = RH_TextCtrl(self, -1, name=name, size=(sized, -1))
            
                ctrl.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
                
                ctrl.SetFocus()
            if 'description' in name:
                ctrl = RH_TextCtrl(self, -1, name=name, size=(sized, -1))
                ctrl.SetEditable(False)
            
            boxSizer.Add(ctrl, 0, wx.ALL, 3)
            level1Sizer.Add(boxSizer, 0, wx.ALL, 3)
        
        level2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        level2_list = [('Department','itemInq_department_txtctrl',125,'item_options','department'),
                       ('Category','itemInq_category_txtctrl',125,'item_options','category'),
                       ('Sub-Category','itemInq_subcategory_txtctrl',125,'item_options','subcategory'),
                       ('Material','itemInq_material_txtctrl',125,'item_options','location'),
                       ('Select\nF1','itemInq_selectF1_button',self.OnSelectF1,'',''),
                       ('Exit\nF2','itemInq_exitF2_button',self.OnExitButton,'','')]
        
        for label,name,sized,table,field in level2_list:
            if 'txtctrl' in name:
                box = wx.StaticBox(self, -1, label=label)
                boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
                ctrl = RH_TextCtrl(self, -1, name=name, size=(sized, 35), style=wx.TE_READONLY)
                ctrl.tableName = table
                ctrl.fieldName = field
                boxSizer.Add(ctrl, 0, wx.ALL, 3)
                level2Sizer.Add(boxSizer, 0)
            if 'button' in name:
                ctrl = RH_Button(self, -1, label=label, name=name)
                ctrl.Bind(wx.EVT_BUTTON, sized)                   
                level2Sizer.Add(ctrl, 1, wx.ALL|wx.EXPAND, 3)
        
        level3Sizer = wx.BoxSizer(wx.HORIZONTAL)
        level3_list = [('Qty On Hand','itemInq_onHand_numctrl','item_detailed','quantity_on_hand')]
        for label, name, table, field in level3_list:
            box = wx.StaticBox(self, -1, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            ctrl = RH_NumCtrl(self, -1, value=0, name=name, integerWidth=6, fractionWidth=2)
            ctrl.SetEditable(False)
            ctrl.tableName = table
            ctrl.fieldName = field
            boxSizer.Add(ctrl, 0)
            level3Sizer.Add(boxSizer, 0, wx.ALL, 3)
        
        level3Sizer.Add((150,10), 0)
        ctrl = RH_CheckBox(self, -1, label='Do Not Discount', name='itemInq_donotdiscount_checkbox')
        ctrl.Disable()
        level3Sizer.Add(ctrl, 0, wx.ALL|wx.RIGHT, 3)     
        
        level4Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        grid = Retail_Grid(self, name='itemInq_retailPrice_grid', formatted='nomargin')
            
        level4Sizer.Add(grid, 0, wx.ALL|wx.EXPAND, 20)
        
        grid = SalesTracker_Grid(self, name='itemInq_salesTracker_grid')
        
        level4Sizer.Add(grid, 0)       
        
        level5Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        level5_list = [('Sale Begin','itemInq_saleBegin_datectrl','item_detailed2','sale_begin'),
                       ('Sale End','itemInq_saleEnd_datectrl','item_detailed2','sale_end'),
                       ('Time Begin','itemInq_timeBegin_timectrl','item_detailed2','sale_begin_time'),
                       ('Time End','itemInq_timeEnd_timectrl','item_detailed2','sale_end_time')]
        
        for label, name, table, field in level5_list:
            box = wx.StaticBox(self, -1, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            if 'datectrl' in name:
                ctrl = RH_DatePickerCtrl(self, -1, name=name, style=wx.adv.DP_ALLOWNONE)
                ctrl.SetValue(wx.DateTime())
            if 'timectrl' in name:
                if 'Begin' in name:
                    timectrl_value = '12:00am'
                elif 'End' in name:
                    timectrl_value = '11:59pm'
                ctrl = RH_TimeCtrl(self, name=name, display_seconds=False, fmt24hr=False, id=-1,useFixedWidthFont=True,value=timectrl_value)
            ctrl.tableName = table
            ctrl.FieldName = field
            ctrl.Disable()
            boxSizer.Add(ctrl, 0, wx.ALL, 3)
            level5Sizer.Add(boxSizer, 0, wx.ALL|wx.CENTER, 10)                    
        
        MainSizer.Add(lookupSizer, 0, wx.ALL|wx.EXPAND, 3)
        MainSizer.Add(level1Sizer, 0, wx.ALL|wx.EXPAND, 3)
        MainSizer.Add(level2Sizer, 0, wx.ALL|wx.EXPAND, 3)
        MainSizer.Add(level3Sizer, 0, wx.ALL|wx.EXPAND, 3)
        MainSizer.Add(level4Sizer, 0)
        MainSizer.Add(level5Sizer, 0, wx.ALL|wx.ALIGN_CENTER, 3)
        self.SetSizer(MainSizer, 0)
        self.Layout()
        
        
                
    def OnFind(self, event):
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
        ItemLookupD = ItemLookupDialog(self, title="Item Lookup", size=(1000,800), style=style)
        ItemLookupD.ShowModal()
        print("-!-" * 40) 
        try:
            self.itempick = ItemLookupD.itemPicked
            print("self . item pick : ",self.itempick)
          
        except:
            self.itempick = ''
            wx.FindWindowByName('itemInq_itemNumber_txtctrl').SetCtrl(self.itempick)
            ItemLookupD.Destroy()
            
        wx.CallAfter(self.LoadInfo, event=self.itempick)
            
    
    def OnExitButton(self, event):
        self.Close()
    
   
    def OnSelectF1(self, event):
        selected = wx.FindWindowByName('itemInq_itemNumber_txtctrl').GetCtrl()
        self.itempick = selected
        self.Close()
        
    def OnKeyDown(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_RETURN or keycode == wx.WXK_NUMPAD_ENTER: 
            obj = event.GetEventObject()
            named = obj.GetName()
            raw_value = wx.FindWindowByName(named).GetCtrl()
            subbed_value = re.sub('[!@$%^&\*()~\[\]\{\}\=`]','',raw_value)
            new_value = subbed_value.upper()
            
            wx.FindWindowByName(named).SetCtrl(new_value)
            
            wx.CallAfter(self.OnItemNumber, event=named)
        
        event.Skip()
    
    def OnItemNumber(self, event):   
        named = event
            
        itemNumber = wx.FindWindowByName(named).GetCtrl()
        #queryWhere = 'upc=(?)'
        
        cnt_returnd = QueryOps().QueryCheck('item_detailed','upc',(itemNumber,))
        
        if cnt_returnd == 1:
            query = 'SELECT upc FROM item_detailed WHERE upc=(?)'
            data = (itemNumber,)
            returnd = SQConnect(query, data).ONE()[0]
            
            returnd =VarOps().DeTupler(returnd)
                
            wx.CallAfter(self.LoadInfo, event=returnd)     
            return
            
        if cnt_returnd == 0:
            whereFrom = QueryOps().ANDSearch(['upc','description','oempart_num','part_num'],itemNumber)
            query = "SELECT upc FROM item_detailed WHERE {0} LIMIT 5000".format(whereFrom)
            data = ''
            returnd = SQConnect(query, data).ALL()
        
        numresult = len(returnd)
        
        if numresult == 0:
            wx.FindWindowByName(named).SetCtrl('')
            return
            
        print("returnd : {0}".format(returnd))
        if len(returnd) == 1:
            returnd =VarOps().DeTupler(returnd)
            wx.FindWindowByName(named).SetCtrl(returnd)
            
                       
            wx.CallAfter(self.LoadInfo, event=returnd)     
            return
             
        if numresult > 1:
            print("*************** Create Modal Window for Individual Choosing...")
            self.itemNumber = itemNumber
            style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
            ItemLookupD = ItemLookupDialog(self, title="Item Lookup",  size=(1000,800), style=style, itemNumber=self.itemNumber)
            ItemLookupD.ShowModal()
            print("-!-" * 40) 
            try:
                self.itempick = ItemLookupD.itemPicked
                print("self . item pick : ",self.itempick)
            except:
                self.itempick = ''
            
            self.itempick =VarOps().DeTupler(self.itempick)
            
            wx.FindWindowByName('itemInq_itemNumber_txtctrl').SetCtrl(self.itempick)
            ItemLookupD.Destroy()
            
            wx.CallAfter(self.LoadInfo, event=self.itempick)
                
    def LoadInfo(self, event):
        print('Load Returnd : {0}'.format(event))                    
        
        upcd = event
        
        if upcd == '' or upcd == None:
            return
        query = 'SELECT description,quantity_on_hand FROM item_detailed WHERE upc=(?)'
        data = (upcd,)
        returnd = SQConnect(query, data).ONE()
        
        (descriptiond,qoh) = returnd
        
        query = 'SELECT department,category,subcategory,location FROM item_options WHERE upc=(?)'
        data = (upcd,)
        returnd = SQConnect(query, data).ONE()
        
        (department,category,subcategory,location) = returnd
        query = 'SELECT do_not_discount FROM item_detailed2 WHERE upc=(?)'
        data = (upcd,)
        returnd = SQConnect(query, data).ONE()[0]
        
        dnd = returnd
        
        load_list = [('itemInq_description_txtctrl',descriptiond),('itemInq_onHand_numctrl', qoh),
                     ('itemInq_department_txtctrl',department),('itemInq_category_txtctrl',category),
                     ('itemInq_subcategory_txtctrl',subcategory),('itemInq_material_txtctrl',location),
                     ('itemInq_donotdiscount_checkbox',dnd)]
        
        
        retails = RetailOps().RetailSifting(upcd)
            
        for name,varib in load_list:
            wx.FindWindowByName(name).SetCtrl(varib)                 
                     
        
            #retails = {}
        #for key in retail_list:
        #    retails[key] = ('1','0.00')
                
            
        print("Retails : {0}".format(retails))
        grid = wx.FindWindowByName('itemInq_retailPrice_grid')
        
        grid.Load(upc=upcd)
        
        retail_list = ['standard_price','level_(a)_price','level_(b)_price','level_(c)_price','level_(d)_price','level_(e)_price','level_(f)_price',
                       'level_(g)_price','level_(h)_price','level_(i)_price','on_sale_price']
        
        
        for name in retail_list:
            for xx in range(grid.GetNumberRows()):
                field = re.sub('[\(\)]','', name)
                key = re.sub('_price', '', name)
                key2 = re.sub('_', ' ', key)
                xlabel = grid.GetRowLabelValue(xx)
                #print "xlabel : key2 = {} : {}".format(xlabel, key2)
                if key2 in xlabel.lower():
                    print("xlabel : key2 = {} : {} : ({} -- {})".format(xlabel, key2, retails[field][0],retails[field][1]))
                    grid.SetCellValue(xx,0, retails[field][0])
                    grid.SetCellValue(xx,1, retails[field][1])
            #
        #for row in range(grid.GetNumberRows()):
        #    rowLabel = grid.GetRowLabelValue(row).lower()
        #    rowLabelSet = re.sub(' ','_', rowLabel)
        #    grid.SetCellValue(row,0,retails[rowLabelSet][0])
        #    grid.SetCellValue(row,1,retails[rowLabelSet][1])
        item = wx.FindWindowByName('itemInq_itemNumber_txtctrl').SelectAll()    
        
        grid = wx.FindWindowByName('itemInq_salesTracker_grid')
        grid.Load(upcd)
        #wx.CallAfter(self.SalesTracker, event=upcd)
    
    def SalesTracker(self, event):
        
        upcd = event
        
        grid = wx.FindWindowByName('itemInq_salesTracker_grid')
        wx.FindWindowByName(grid.GetName()).ClearCtrl(fillwith='0.000')

        thisyear = datetime.datetime.today().date().year
        lastyear = thisyear-1
        year2ago = thisyear-2
        year3ago = thisyear-3
        year_list = [thisyear, lastyear, year2ago, year3ago]
        for dated in year_list:
            for mnth in range(1,13):
                query = 'SELECT quantity FROM transactions WHERE year(date)=(?) and upc=(?) and month(date)=(?)'
                data = [dated,upcd,mnth,]
                returnd = SQConnect(query,data).ONE()
                
                quantity = returnd
                if returnd is None:
                    continue
                cnt = len(returnd)
                if cnt > 1:
                    lqty = Decimal(0)
                    for qty in returnd:
                        lqty += Decimal(qty)
                elif cnt == 1:
                    lqty = returnd[0]
                else:
                    lqty = 0
                            
                mth = datetime.datetime.strptime(str(mnth), '%m')
                amnth = mth.strftime('%B')
                
                setList=[(str(amnth),str(lqty))]
                
                GridOps(grid.GetName()).FillGrid(setList, col=0)
                                         
        
###-----------------------------------------------------------------------------
class CreditCardPopup(wx.Dialog):
    def __init__(self, debug=False, *args, **kwargs):
        kwargs['title'] = 'CreditCard Popup'
        kwargs['size'] = (300,300)
        super(CreditCardPopup, self).__init__(
                                         *args, **kwargs)
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        check_list = [('Name on Card','creditcardpopup_name_txtctrl',125),
                      ('PayType','creditcardpopup_payType_combobox',['Paypal','Square']),
                      ('Auth #/Last 4','creditcardpopup_authNum_txtctrl',125)] 
        idx = 1
        for label, name, sized in check_list:
            box = wx.StaticBox(self, -1,label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            
            if 'name' in name:
                ctrl = RH_MTextCtrl(self, -1, name=name, formatcodes='!_',size=(sized,-1))
                ctrl.SetFocus()
            if 'payType' in name:
                ctrl = RH_ComboBox(self, -1, name=name, choices=sized,size=(75,-1))     
            if 'authNum' in name: 
                ctrl = RH_MTextCtrl(self, -1, name=name, formatcodes='!_',size=(sized,-1)) 
            
            boxSizer.Add(ctrl, 0, wx.ALL, 3)
            
            MainSizer.Add(boxSizer, 0, wx.ALL|wx.ALIGN_CENTER,3)
        
        level2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_list = [('&Accept\n    F1','checkpopup_accept_button',self.OnAccept),
                       ('&Cancel\n    F12','checkpopup_cancel_button', self.OnCancel)]  
         
        for label, name, hdlr in button_list:
            btn = RH_Button(self, -1, label=label, name=name)
            btn.Bind(wx.EVT_BUTTON, hdlr)
            level2Sizer.Add(btn, 0, wx.ALL, 3)
            
        
        MainSizer.Add(level2Sizer, 0,wx.ALL|wx.ALIGN_CENTER, 5)
         
        self.SetSizer(MainSizer, 0)
        
    def OnAccept(self, event):
        check_list = [('name','creditcardpopup_name_txtctrl',125),
                      ('paytype','creditcardpopup_payType_combobox',['Paypal','Square']),
                      ('auth','creditcardpopup_authNum_txtctrl',125)] 
        
        listd = []
        for label, name, size in check_list:
            value = wx.FindWindowByName(name).GetCtrl()
            listd.append(value)
            
        self.payment = tuple(listd)
            
        
        self.Close()
            
    def OnCancel(self, event):
        self.Close()


class CheckPopup(wx.Dialog):
    def __init__(self, debug=False, *args, **kwargs):
        kwargs['title'] = 'Check Popup'
        kwargs['size'] = (300, 300)
        super(CheckPopup, self).__init__(*args, **kwargs)
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        check_list = [('Check #','checkpopup_checkNum_txtctrl'),
                      ('Driver\'s License #','checkpopup_dlNum_txtctrl'),
                      ('Date of Birth','checkpopup_dob_txtctrl'),
                      ('Phone #','checkpopup_phoneNum_txtctrl')] 
        idx = 1
        for label, name in check_list:
            box = wx.StaticBox(self, -1,label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            
            if re.search('(checkNum|dlNum)',name, re.I):
                ctrl = RH_MTextCtrl(self, -1, name=name, formatcodes='!_',size=(155,-1))
            if 'dob' in name:
                ctrl = RH_MTextCtrl(self, -1, name=name, mask='##/##/####',size=(125,-1))     
            if 'phone' in name: 
                ctrl = RH_MTextCtrl(self, -1, name=name, mask='(###) ###-####',size=(125,-1)) 
            
            if 'checkNum' in name:
                ctrl.SetFocus()
                    
            boxSizer.Add(ctrl, 0, wx.ALL, 3)
            
            MainSizer.Add(boxSizer, 0, wx.ALL|wx.ALIGN_CENTER,3)
        
        level2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_list = [('&Accept\n    F1','checkpopup_accept_button',self.OnAccept),
                       ('&Cancel\n    F12','checkpopup_cancel_button', self.OnCancel)]  
         
        for label, name, hdlr in button_list:
            btn = RH_Button(self, -1, label=label, name=name)
            btn.Bind(wx.EVT_BUTTON, hdlr)
            level2Sizer.Add(btn, 0, wx.ALL, 3)
            
        
        MainSizer.Add(level2Sizer, 0,wx.ALL|wx.ALIGN_CENTER, 5)
         
        self.SetSizer(MainSizer, 0)
        
    def OnAccept(self, event):
        check_list = [('Check #','checkpopup_checkNum_txtctrl'),
                      ('Driver\'s License #','checkpopup_dlNum_txtctrl'),
                      ('Date of Birth','checkpopup_dob_txtctrl'),
                      ('Phone #','checkpopup_phoneNum_txtctrl')] 
        
        listd = []
        for label, name in check_list:  
            value = wx.FindWindowByName(name).GetCtrl()
            listd.append(value)    
        
        self.payment = tuple(listd)    
        self.Close()
    
    def OnCancel(self, event):
        self.Close()

class FinishItDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):#parent, title, size, style, transDict, debug=False): #,ATs=None, addrNum=None, custNum=None, due=None, transNum=None, returnItems=None) :
        transDict = kwargs.pop('transDict')
        super(FinishItDialog, self).__init__(*args, **kwargs) #parent=parent,title=title,size=size,style=style)
        self.due = transDict['due']
        self.ActiveTransactions = transDict['ATs']
        self.addrNum = transDict['addrNum']
        self.custNum = transDict['custNum']
        self.cred = {}
        self.transNum = transDict['transNum']
        self.returnItems = transDict['returnItems']
       
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        levelA_1Sizer = wx.BoxSizer(wx.VERTICAL)
        level1_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        grid = FinishIt_Grid(self, name='finishitdialog_payterm_grid')
        print('CC: [{}]'.format(self.custNum))
        #grid.CreditCheck(custNum=self.custNum)
        grid.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.OnEnter)
        custCredit = QueryOps().CheckCredit(self.custNum)
        
        if custCredit is True or custCredit == 1:
            for xx in range(grid.GetNumberRows()):
                label = grid.GetRowLabelValue(xx)
                if 'Charge' in label:
                    grid.SetReadOnly(xx,0,True)
                    grid.SetRowLabelValue(xx,'No Charge')
                    
        
        grid.SetFocus()
        
        
        levelA_1Sizer.Add(grid, 0, wx.ALL|wx.ALIGN_LEFT, 10)
                        
        
        level1_Sizer.Add(levelA_1Sizer, 0, wx.ALL|wx.EXPAND, 3)
        level2_Sizer = wx.BoxSizer(wx.HORIZONTAL)

        sizerA = wx.BoxSizer(wx.VERTICAL)
        sizerA_list = [('Paid','finishIt_paid_txtctrl'),
                       ('Due','finishIt_due_txtctrl'),
                       ('Change','finishIt_change_txtctrl')]

        for label,name in sizerA_list:
            box = wx.StaticBox(self, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            ctrl = RH_TextCtrl(self, -1,
                               name=name,
                               size=(160,-1),
                               style=wx.TE_READONLY|wx.ALIGN_RIGHT)

            if 'change' in name:
                ctrl.SetForegroundColour(wx.RED)
            
            boxSizer.Add(ctrl, 0,wx.ALL,3)
            sizerA.Add(boxSizer, 0, wx.ALL, 3)


        sizerB = wx.GridSizer(4,3,5,5)
        sizerB_list = [('Reset\nF&1','finishit_reset_button',self.onResetF1),
                       ('Cancel\nF&2','finishit_cancel_button',self.onCancelF2),
                       ('Done\nF&3','finishit_done_button',self.onDoneF3),
                       ('Put on Hold\nF&4','finishit_hold_button',self.onPutOnHoldF4),
                       ('Set C&urrent Line to Amount Due\nF12','finishit_currentline_button',self.onSetAmountDue)]
        

        for label, name, hndlr in sizerB_list:
            button_size = ButtonOps().ButtonSized(sizerB_list)

        
        print("Button Sizes : ",button_size)
        for label, name,hndlr in sizerB_list:
            newLabel = ButtonOps().ButtonCenterText(label)
            btn = RH_Button(self, -1,
                            label=newLabel,
                            name=name,
                            size=(button_size[0],
                            button_size[1]))

            btn.Bind(wx.EVT_BUTTON, hndlr)
            #if 'done' in name:
            #    btn.Disable()
                
            sizerB.Add(btn,0)

        level2_Sizer.Add(sizerA,0)
        level2_Sizer.Add((60,20),0)
        level2_Sizer.Add(sizerB,0)
        
        MainSizer.Add(level1_Sizer, 0)
        MainSizer.Add(level2_Sizer, 0)
        self.SetSizer(MainSizer, 0)
        self.Layout()

        wx.CallAfter(self.onLoad, event='')
    
    def Due(self,due=None):
        self.due = due
        
    def onLoad(self, event):
        wx.FindWindowByName('finishIt_due_txtctrl').SetCtrl(self.due)    
        
    
    
    def OnEnter(self, event):
        obj = event.GetEventObject()
        named = obj.GetName()
        row = event.GetRow()
        col = event.GetCol()
        grid = wx.FindWindowByName(named)  
        svalue = grid.GetCellValue(row,col)
        fvalue = MiscOps().NumbersOnly(svalue)
        print('svalue : {}\nfvalue : {}'.format(svalue, fvalue))
        if fvalue is None:
            grid.SetCellValue(row,col, '')
            return
        
        if fvalue is not None:
            pval = RetailOps().RoundIt(fvalue, '1.00')
            
            grid.SetCellValue(row,col, str(pval))
            
              
#        keycode = event.GetKeyCode()
#        if keycode == wx.WXK_RETURN or keycode == wx.WXK_NUMPAD_ENTER or keycode == wx.WXK_TAB: 
#            wx.CallAfter(self.Actions, event=named)
#        event.Skip()
        
        
        
#    def Actions(self, event):
#       
#        named = event
        add = 0
        listd = [('cash',0),('check',1),('charge',2),('debit',3),('credit1',4),
                 ('credit2',5),('credit3',6),('credit4',7),('credit5',8)]
       
        
        for label, cell in listd:
            value = grid.GetCellValue(cell,0)
            #Debugger("value : {}\n\tname : {}".format(value, name))
                
            if re.search('[0-9]', str(value)):
                #g = re.match('f[nshit]+_(.*)_[texnum]+ctrl',name,re.I)
                #self.cred[g.group(1)] = value
                self.cred[label] = value
                #print 'G : {} = {}'.format(g.group(1),self.cred)
                self.cred['change'] = 0.0            
                add += Decimal(value)
                comp = Decimal(self.due) - Decimal(add)         
                print("Comp : ",comp)
                if comp < 0:
                    if 'cash' in label:
                        change = Decimal(value) + Decimal(comp)
                        #print "change : ",change
                        #CO('finishIt_change_txtctrl').SetCtrl(change)
                        toomuch = Decimal(self.due) * 5
                        toomuch =VarOps().ChangeType(toomuch, 'decimal')
                        value =VarOps().ChangeType(value, 'decimal')
                        
                        if value >= toomuch:
                            result = wx.MessageBox('Are you sure?','Info',wx.OK|wx.CANCEL)
                            if result == wx.CANCEL:
                                wx.CallAfter(self.onResetF1, event='')
                                return  
                        totald = Decimal(self.due) - Decimal(add)
                        totald = RetailOps().DoRound(totald, '1.00')
                        print("{} - {} = {}".format(self.due,add,totald))
                        
                        totald = str(totald)
                        wx.FindWindowByName('finishIt_change_txtctrl').SetCtrl(totald)
                        self.cred['change'] = totald
                        add = RetailOps().DoRound(add, '1.00')    
                        
                        formal_paid = RetailOps().DoRound(value, '1.00')
                        wx.FindWindowByName('finishIt_paid_txtctrl').SetCtrl(formal_paid)
                        
                        wx.CallAfter(self.onDoneF3, event='')
                        print('T {} > {}'.format(totald, self.due))
                        totald =VarOps().ChangeType(totald, 'decimal')
                        value =VarOps().ChangeType(value, 'decimal')
                        if totald > value:
                            setList=[('Cash',self.due)]
                            GridOps(grid.GetName()).FillGrid(setList, col=1)
                            #CO('finish_cash_numctrl').SetCtrl(self.due)
                        
                        self.due =VarOps().ChangeType(self.due, 'decimal')
                        value =VarOps().ChangeType(value, 'decimal')
                        if value > self.due:
                            break
                    else:            
                        new_value = Decimal(value) + Decimal(comp)
                        print("new P : ",new_value)
                        add += Decimal(comp)
                        
                        print("AddIT : ",add)
                        
                        totald = Decimal(self.due) - Decimal(add)
                        totald =VarOps().DoRound(totald, '1.00')
                        print("{} - {} = {}".format(self.due,add,totald))
                        
                        totald = str(totald)
                        wx.FindWindowByName('finishIt_due_txtctrl').SetCtrl(totald)
                        add = RetailOps().DoRound(add, '1.00')    
                        #CO('finishIt_paid_txtctrl').SetCtrl(value)
        
                        
        
    def onResetF1(self, event):
       
        self.cred = {}
        grid = wx.FindWindowByName('finishitdialog_payterm_grid')
        grid.Clear()
            
        grid.SetFocus()
            
    def onCancelF2(self, event):
        
       
        self.Status = 'open'
        self.Close()
        pass

    def onDoneF3(self, event):
       
        grid = wx.FindWindowByName('finishitdialog_payterm_grid')
        listd = [('cash',0),('check',1),('charge',2),('debit',3),('credit1',4),
                 ('credit2',5),('credit3',6),('credit4',7),('credit5',8)]
        
        due_cash = wx.FindWindowByName('finishIt_due_txtctrl').GetCtrl()
        
        for name, cell in listd:
            value = grid.GetCellValue(cell,0)
            #value = HU.GetCtrl(name)
            
            if value == '' or value is None:
                value = 0
            if Decimal(value) > 0:
                style = wx.DEFAULT_FRAME_STYLE & (~wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX) & (~wx.MINIMIZE_BOX)
                get = name
                #print 'Get : ',get[1]
                    
                if 'check' in name:
                    chek_payment = value
                    checkPopup = CheckPopup(self,
                                           style=style)
               
                    checkPopup.ShowModal()
                    
                    try:
                        payInfo = (str(value),) + checkPopup.payment
                        
                    except:
                        checkPopup.Destroy()
                    
                if 'cash' in name:
                    payInfo = due_cash
                    
                if 'charge' in name:
                    payInfo = value                    
                
                if re.search('(credit|debit)', name, re.I):
                    creditPopup = CreditCardPopup(self,
                                           style=style)
               
                    creditPopup.ShowModal()
                    
                    try:
                        payInfo = (str(value),) + creditPopup.payment
                        
                    except:
                        creditPopup.Destroy()
                        
                    
                
                self.cred[get] = payInfo
        print("Creds : ",self.cred)    
                    
                        
        
        
        
        
        result = wx.MessageBox('Finish Transaction?', 'Info', wx.OK|wx.CANCEL)
        poNum = wx.FindWindowByName('pos_PoTab_ponumber_txtctrl').GetCtrl()
        CloseDict = {'ATs': self.ActiveTransactions,
                     'transType' : 'Sale',
                     'payment' : self.cred,
                     'addrNum' : self.addrNum,
                     'custNum' : self.custNum,
                     'transNum' : self.transNum,
                     'returns' : None,
                     'poNum' : None,
                     'stationNum' : None,
                     'drawerNum' : None
                     }
        if result == wx.OK:
            CloseDict['returns'] = self.returnItems
            CloseDict['transType'] = 'Sale'
            ATs = HU.ReadyClose(CloseDict) #ATs=self.ActiveTransactions, transType='Sale',payment=self.cred, addrNum=self.addrNum, custNum=self.custNum, transNum=self.transNum, returns=self.returnItems)
            print("AT : ",ATs)
        
            self.Status = 'closed'
            self.Close()
                   
    def onPutOnHoldF4(self, event):
        poNum = wx.FindWindowByName('pos_PoTab_ponumber_txtctrl').GetCtrl()
        CloseDict['poNum'] = poNum
        ATs = HU.ReadyClose(CloseDict) #ATs=self.ActiveTransactions, transType='Hold', addrNum=self.addrNum, custNum=self.custNum, ponumber=poNum) 
        
        self.Status = 'closed'
        self.Close()

    def onSetAmountDue(self, event):
       
        grid = wx.FindWindowByName('finishitdialog_payterm_grid')
        
        row, col = GridOps(grid.GetName().GetGridCursor())
        grid.SetCellValue(row,col, self.due)
        
        

    def Trans(self, ATs=None, addrNum=None, custNum=None):
        self.ActiveTransactions = ATs
        if addrNum == '':
            self.addrNum = None
        else:
            self.addrNum = addrNum
        
        if custNum == '':
            self.custNum = None
        else:
            self.custNum = custNum
     

class FindAddressLookupDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super(FindAddressLookupDialog, self).__init__(*args, **kwargs)
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        level1_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        box = wx.StaticBox(self, -1, label='Address Search')
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        
        ctrl = wx.TextCtrl(self, -1, name='addrSearch_txtctrl', size=(260,-1),style=wx.TE_PROCESS_ENTER)
        ctrl.Bind(wx.EVT_TEXT_ENTER, self.OnSearchButton)
        ctrl.SetFocus()
        btn = wx.Button(self, -1, label='Search', name='addrSearch_button')
        btn.Bind(wx.EVT_BUTTON, self.OnSearchButton)
        
        boxSizer.Add(ctrl, 0, wx.ALL, 3)
        boxSizer.Add(btn, 0, wx.ALL, 3)
        
        level1_Sizer.Add(boxSizer, 0, wx.ALL, 3)
        
        level1a_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self, -1, label='', name='addrSearch_loading_text')
        level1a_Sizer.Add(text,0)
         
        level2_Sizer = wx.BoxSizer(wx.VERTICAL)
        
        lc = RH_OLV(self, -1, name='addrSearch_lc', size=(760,465), style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        lc.SetColumns([
                       ColumnDefn('Account #', 'center', 120, 'acctNum'),
                       ColumnDefn('Address 1', 'left', 220, 'address1d'),
                       ColumnDefn('Address 2', 'left', 150, 'address2d'),
                       ColumnDefn('City', 'left', 130, 'cityd'),
                       ColumnDefn('State','left', 90, 'stated')
                      ])

        lc.SetSortColumn(1)
        
        
        lc.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnChooserCellLeftClick)      
                
        level2_Sizer.Add(lc, 0)
        MainSizer.Add(level1_Sizer, 0, wx.ALL, 5)
        MainSizer.Add(level1a_Sizer, 0, wx.ALL, 5)        
        MainSizer.Add((20,20),0)
        MainSizer.Add(level2_Sizer, 0, wx.ALL|wx.ALIGN_CENTER, 3)
        self.SetSizer(MainSizer, 0)
        self.Layout()


    def OnSearchButton(self, event):
        addr_search = wx.FindWindowByName('addrSearch_txtctrl').GetValue()
        pout.b('On Search Button')
        #revised_search = re.sub(' ','.*',addr_search)
        whereFrom = 'address0'
            
        
        if len(addr_search) == 0:
            return

        query = "SELECT addr_acct_num,address0,address2,address3,city,state from address_accounts where {0} LIKE (?) OR zipcode=(?)".format(whereFrom)
        data = (addr_search, addr_search,)
        returnd = SQConnect(query, data).ALL()
        
        pout.v(f'Item 0 : {returnd}')                  
        lcname = 'addrSearch_lc'
        lc = wx.FindWindowByName(lcname)
        lc.DeleteAllItems()
        plural = ''
        records_returnd = 0
        pout.v(f'Item 1 : {returnd}')                  
        if returnd:
            records_returnd = len(returnd)
            if records_returnd > 1:
                plural = 'es'
                        
            num_items = wx.FindWindowByName('addrSearch_loading_text')
            num_items.SetLabel('Found '+str(records_returnd)+' Address'+plural)
            row = 0    
            pout.v(f'Item 2: {returnd}')                  
            for addr_acct_numd, address1d, address2d, address3d, cityd, stated in returnd:
                setList = [{'acctNum':addr_acct_numd,'address1d':address1d,'address2d':address2d,'cityd':cityd,'stated':stated}]
                lc.AddObjects(setList)
            
            
        
        
    
    def OnChooserCellLeftClick(self, evt):
        item_id,objText = EventOps().LCGetSelected(evt)
        self.addrPicked = objText
        self.Close()
        
        
        
        
        

        
 
################################################################################
# GUI ELEMENTS 
#
#############################################################        
class Payment_OLV(object):
    def __init__(self, date, time, transNum, total, debug=False):
        self.date = date
        self.time = date
        self.transNum = transNum
        self.total = total
        




class RH_CheckListCtrl(ObjectListView):
    def __init__(self, *args, **kwargs):
        RH_OLV.__init__(self, *args, **kwargs)
        self.index = 0
        colLabel_list = [('Pay This?',135),('Date',90),('Time',90),('Trans #',140),('Total',140)]
        self.SetColumns([
                    ColumnDefn('Pay This?','center',135,'paythisd'),
                    ColumnDefn('Date','center',90,'dated'),
                    ColumnDefn('Time','center',90,'timed'),
                    ColumnDefn('Transaction #','center',140,'transNum'),
                    ColumnDefn('Total','right',140,'totald')
        ])
        self.InstallCheckStateColumn(0)
        self.RefreshObjects()
        # y = 0
        # for label,size in colLabel_list:
        #     self.InsertColumn(y, label, width=size)
        #     y += 1    
        
        
        
    
    def OnLoad(self,custNum):
        query = '''SELECT date, time, transaction_id, total_price
                   FROM transaction_payments
                   WHERE cust_num=(?) AND pay_method=(?)'''
        
        data = [custNum, 'CHARGE',]
        returnd = SQConnect(query, data).ALL()
        
        idx = 0    
        self.Clear()
        for date, time, transNum, total_price in returnd:
            setList = [{'dated':date, 'timed':time, 'transNum':transNum, 'totald':total_price}]
            self.AddObjects(setList)
            
            
            
            
#-------------------------------------------------------------------------------        


class AltLookup(wx.Panel):
    """ AltLookup List Box Panel """
    def __init__(self, *args, **kwargs):
        pout.v(kwargs)
        self.boxlabel = kwargs.pop('boxlabel')
        self.lbsize = kwargs.pop('lbsize')
        self.lbname = kwargs.pop('lbname')
        self.tableName = kwargs.pop('tableName')
        self.fieldName = kwargs.pop('fieldName')
        wx.Panel.__init__(self, *args, **kwargs)
        # pout.v(f'tableName : {self.tableName} ; fieldName : {self.fieldName}')
        box = wx.StaticBox(self, wx.ID_ANY, label=self.boxlabel)
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        
        levelSizer = wx.BoxSizer(wx.HORIZONTAL)
        level1Col2Sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.lb = RH_ListBox(self, -1,
                          size = self.lbsize, 
                          name = self.lbname)
        self.lb.tableName = self.tableName
        self.lb.fieldName = self.fieldName
        self.lb.Bind(wx.EVT_LISTBOX, self.ListBoxSelectItem) 
        levelSizer.Add(self.lb, 0)
        
        self.lbtc = RH_TextCtrl(self, -1, size=(110, -1), style=wx.TE_PROCESS_ENTER)
        self.lbtc.Bind(wx.EVT_TEXT_ENTER, self.ListBoxOnAddButton)
        level1Col2Sizer.Add(self.lbtc, 0, wx.ALL, 3)
        
        self.addbutton = RH_Button(self, -1, label="Add", size=(110,-1))
        self.addbutton.Bind(wx.EVT_BUTTON, self.ListBoxOnAddButton)
        level1Col2Sizer.Add(self.addbutton, 0, wx.ALL, 3)
        
        self.rembutton = RH_Button(self, -1, label="Remove", size=(110,-1))
        self.rembutton.SetForegroundColour('Red')
        self.rembutton.Bind(wx.EVT_BUTTON, self.ListBoxOnRemoveButton)
        level1Col2Sizer.Add(self.rembutton, 0, wx.ALL, 3)
                
        levelSizer.Add(level1Col2Sizer, 0)
        
        boxSizer.Add(levelSizer, 0)
        self.SetSizer(boxSizer)
        self.Layout()

    def OnLoad(self, event):
        self.lb.OnLoad(whereField='abuser', whereValue='rhp')

    def OnSave(self, event):
        self.lb.OnSave(whereField='abuser', whereValue='rhp')

    def Clear(self, event):
        self.lb.Clear()
    
    def ListBoxOnAddButton(self, event):
        if not self.lbtc.GetValue():
            return
                
        num_altlookups = self.lb.GetCount()
        tobe_searched = self.lbtc.GetValue()
        has_found = self.lb.FindString(tobe_searched)
        
        if has_found != -1:
            foundIndex = has_found
            self.lb.EnsureVisible(foundIndex)
            self.addbutton.SetBackgroundColour('Red')
            self.TC_ClearFocus()
        else:
            self.addbutton.SetBackgroundColour('Green')
            self.lb.Append(self.lbtc.GetValue().upper())
            self.TC_ClearFocus()
  
        allstrings = self.lb.GetStrings()

    def TC_ClearFocus(self):
        self.lbtc.Clear()
        self.lbtc.SetFocus()

    def ListBoxSelectItem(self, event):
        selection = self.lb.GetStringSelection()
        self.lbtc.SetCtrl(selection)

    def ListBoxOnRemoveButton(self, event):
        tobe_removed = self.lbtc.GetValue()
        currentItem = self.lb.FindString(tobe_removed)
        if currentItem != -1:
            self.lb.EnsureVisible(currentItem)
            self.lb.Delete(currentItem)
            
        self.TC_ClearFocus()
        

class PhoneNumber_Panel(wx.Panel):
    """PhoneNumber Panel contains all controls necessary to achieve adding phone numbers to accounts. 
       The fieldname & tablename variables are  for the phone olv to save to customer accounts."""
    def __init__(self, *args, **kwargs):
        self.fieldName = kwargs.pop('fieldName')
        self.tableName = kwargs.pop('tableName')
        self.custNum = kwargs.pop('custNum')
        wx.Panel.__init__(self, *args, **kwargs)
        
        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        savebutton = HUD.RH_Icon(icon='save')
        savebutton.Bind(wx.EVT_BUTTON, self.OnSave)

        f_box = wx.StaticBox(self, -1, label="Phone Numbers")
        f_boxSizer = wx.StaticBoxSizer(f_box, wx.VERTICAL)
        
        f_add_boxSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.phtype = RH_Button(self, -1, name="custdatapnl_phonetype_btn")
        self.phtype.listd = ['HOME','CELL','WORK','FAX',
                             'CONTACT1','CONTACT2','CONTACT3']
        f_add_boxSizer.Add(self.phtype, 0)

        self.phonetc = RH_MTextCtrl(self, -1, 
                                mask='(###) ###-####',
                                validRegex = "^\(\d{3}\) \d{3}-\d{4}", 
                                size=(160, -1), 
                                name='custdatapnl_addphone_txtctrl')
        
        f_add_boxSizer.Add(self.phonetc, 0, wx.ALL, 3)

        ctrl = HUD.RH_Icon(icon='add')
        ctrl.Bind(wx.EVT_BUTTON, self.AddPhoneNumber)
        
        f_add_boxSizer.Add(ctrl, 0)
        f_boxSizer.Add(f_add_boxSizer, 0)
        
        self.SetSizer(f_boxSizer, 0)
        self.Layout()

        self.lc = RH_OLV(self, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.lc.SetColumns([ColumnDefn('Type','center',120,'typd'),
                            ColumnDefn('Phone #','center',150,'number')])
        self.lc.fieldName = self.fieldName
        self.lc.tableName = self.tableName

        f_boxSizer.Add(self.lc, 0)
        MainSizer.Add(f_boxSizer, 0, wx.ALL, 3)
        MainSizer.Add(savebutton, 0, wx.ALL, 3)
        self.SetSizer(MainSizer, 0)
        self.Layout()
        
        wx.CallAfter(self.OnLoad, event='')

    def AddPhoneNumber(self, event):
        addphone = [{'typd':self.phtype.GetCtrl(), 'number':self.phonetc.GetCtrl()}]
        self.lc.AddObjects(addphone)

    def OnLoad(self):
        returnd = self.lc.OnLoad('cust_num', self.custNum)
        phones = json.load(returnd[0])
  
    def OnSave(self):
        phones = self.lc.GetObjects()
        ph_json = json.dumps(phones)
        returnd = LookupDB('customer_basic_info').UpdateSingle('phone_numbers',ph_json,'cust_num',self.custNum)


#----------------------------        
class Rental_LC(RH_OLV):
    """ Rental LC of Customers """
    def __init__(self, *args, **kwargs):
        kwargs['size'] = (870, 200)
        kwargs['style'] = wx.LC_REPORT|wx.BORDER_SUNKEN
        RH_OLV.__init__(self, *args, **kwargs)
        
        self.index = 0
        colLabel_list = [('Account Number',135),('Address',300),('Unit',70),
                         ('City',190),('State',70),('Zipcode',90)]
        y = 0
        self.SetColumns([
                        ColumnDefn('Account #','center',135,'acctNum'),
                        ColumnDefn('Address','left',300,'addressd'),
                        ColumnDefn('Unit','center',70,'unitd'),
                        ColumnDefn('City','left',190,'cityd'),
                        ColumnDefn('State','left',70,'stated'),
                        ColumnDefn('Zipcode','left',90,'zipcoded')
                        ])
    
        

    def OnLoad(self, custNum, addrNum=None, debug=False):
        self.DeleteAllItems()
        returnd = LookupDB('customer_basic_info').Specific(custNum, 'cust_num', 'rental_of')
        ret = ""    

        pout.v('Returnd JSON : '.format(returnd))
        
        a = returnd
        b = VarOps().CheckNone(a)
        for value in a:
            fields = 'street_num, street_direction, street_name, street_type, city, state, zipcode, unit'
            returnd = LookupDB('address_accounts').Specific(value, 'addr_acct_num', fields)
            if returnd is not None:
                (snum, sdir, sname, stype, cityd,statd,zipcoded,unitd) = returnd
                address0d = TextOps().AllinaRow(snum, sdir, sname, stype, unit=unitd)
                
                lc_set = {'acctNum' : value, 'addressd':address0d, 'unitd':unitd, 'cityd':cityd, 'stated':statd,'zipcoded':zipcoded}
                self.AddObjects(lc_set)
            
               
    def OnSave(self, custNum, debug=False):
        rows = self.GetObjects()
        #rental_lst = []
        pout.b()
        pout.v(f'Rental Rows : {rows}')
        lst = []
        for row in rows:
            lst += row['acctNum']

        
        value = json.dumps(lst)

        returnd = LookupDB('customer_basic_info').UpdateSingle('rental_of',value, 'cust_num',custNum)
        
        
        
    def Add(self, addrNum):
        print("Index : ",self.index)
        lc_cnt = self.GetItemCount()
        print("Item COunt : ",lc_cnt)
        
        rental_dict = {}
        if lc_cnt == 0:
            rental_dict[lc_cnt] = addrNum
        else:
            for x in range(lc_cnt):
                item = self.GetItem(x,0)
                value = item.GetText()
                rental_dict[x] = value
                
            
            rental_dict[lc_cnt] = addrNum
                
        
        
        deleteItems = self.DeleteAllItems()
        print("Delete All Items : ",deleteItems)
        
        for xx, value in rental_dict.items():
            query = """SELECT address0,city,state,zipcode,unit 
                       FROM address_accounts 
                       WHERE addr_acct_num=(?)"""
            data = (value,)
            returnd = SQConnect(query, data).ONE()
            
            (address0d, cityd,statd,zipcoded,unitd) = returnd
            
            lc_set = [(0,value),(1,address0d),
                        (3,cityd),(4,statd),(5,zipcoded),
                        (2,unitd)]
            for label,vari in lc_set:
                if label == 0:
                    self.InsertItem(xx, vari)
                else:
                    self.SetItem(xx,label,vari)        
                
###-----------------------------------------------------------------------------

class DCS_Combobox(wx.ComboBox):
    """ Dept, Category, SubCategory Comboboxes """
    def __init__(self, parent, name, which, style):
        wx.ComboBox.__init__(self, parent, choices=[], name=name, style=wx.CB_SORT|style)
        
        self.which = which.upper()
    
        wx.CallAfter(self.OnLoad, event='')
    
    def OnLoad(self, event):
        organizer = 'a'
        desc = [('dep','department'),('cat','category'),('sub','subcategory'),
                ('(mat|loc)','location'),('unit','unittype')]
        for term, org in desc:
            if re.match(term ,self.which, re.I):
                organizer = org
                
        print('organizer  : {} = {}'.format(self.which, organizer))
        query = 'SELECT {} FROM organizations where abuser=(?)'.format(organizer)
        data = ['rhp',]
        returnd = SQConnect(query, data).ONE()
                
        choice_list = returnd
        if choice_list is not None:
            print(f'Choice list DCS : {choice_list}')
            choice_list.insert(0, '')
            self.SetItems(choice_list)


class FinishIt_Grid(gridlib.Grid):
    """ Finish It Payment Grid """
    def __init__(self, parent, name):
        gridlib.Grid.__init__(self, parent, style=wx.BORDER_SUNKEN, name=name)
        
        #grid = gridlib.Grid(self, -1, 
        #                     name='finishitdialog_payterm_grid', 
        #                     style=wx.BORDER_SUNKEN)
        
        rowlabel_list = ['Cash','Check','Charge','Debit','Credit','Credit','Credit','Credit']

        self.CreateGrid(len(rowlabel_list),1)
        self.EnableScrolling(False, True)
        for idx, label in enumerate(rowlabel_list):
            print('idx : label , {} : {}'.format(idx, label))
            self.SetRowLabelValue(idx, label)
            self.SetRowSize(idx, 50)
            
        self.SetColSize(0, 160)
        self.SetRowLabelSize(160)
        self.SetColLabelSize(0)
        
        self.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.SetLabelFont(wx.Font(wx.FontInfo(12)))
        GridOps(self.GetName()).GridAlternateColor(len(rowlabel_list))
                    
    
    

    def Clear(self):
        maxrows = self.GetNumberRows()
        maxcols = self.GetNumberCols()
        
        for row in range(maxrows):
            for col in range(maxcols):
                self.SetCellValue(row, col, '')
                        
    
    def CreditCheck(custNum, credit=False):
        print('CheckCredit : {} \ {}'.format(custNum, credit))
        
        if custNum is not None and len(custNum)>0:
            query = 'SELECT freeze_charges FROM customer_accts_receivable WHERE cust_num=(?)'
            data = [custNum,]
            returnd = SQConnect(query,data).ONE()
            
        
            if returnd[0] == 1:
                credit = True
        
        
        if custCredit is False:
            for xx in range(self.GetNumberRows()):
                label = self.GetRowLabelValue(xx)
                if 'Charge' in label:
                    self.SetReadOnly(xx,0,True)
                    self.SetRowLabelValue(xx,'')

        return credit    
            
        
class POS_Acct_Grid(gridlib.Grid):
    """ POS Acct Grid used at the POS Screen"""
    def __init__(self, parent, name, debug=False):
        
        gridlib.Grid.__init__(self, parent, style=wx.BORDER_SUNKEN, name=name)
        rowlabel_list = ['Account Number', 'Address Account', 'Name',
                         'Address 1', 'Address 2', 'City, State, Zip', 'Phone',
                         'A/R/Avail Credit', 'Discount %', 'Ship To']
        self.cntd = 0
        self.CreateGrid(len(rowlabel_list), 1)
        self.EnableScrolling(True, True)
        self.DisableDragRowSize()
        
        self.SetColLabelSize(0)
        self.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.SetLabelFont(wx.Font(wx.FontInfo(9)))
        self.SetColSize(0, MiscOps().WHSup(cell=250)[0])
        self.SetRowLabelSize(MiscOps().WHSup(cell=160)[0])
        self.SetLabelBackgroundColour(Themes().GetColor('bg'))
        self.SetLabelTextColour(Themes().GetColor('text'))
        
        readonly_list = ['Name', 'Address 1', 'Address 2', 'City, State, Zip',
                         'Avail Credit', 'Discount %', 'Ship To']
        for xx in range(self.GetNumberRows()):
                for item in readonly_list:
                    rowName = self.GetRowLabelValue(xx)
                    if item in rowName:
                        self.SetReadOnly(xx, 0, True)

                self.SetCellAlignment(xx, 0, wx.ALIGN_LEFT, wx.ALIGN_CENTER)
        for idx, item in enumerate(rowlabel_list):
            self.SetRowLabelValue(idx, item)

        GridOps(self.GetName()).GridAlternateColor('')

        self.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.OnClickGrid)
        randomId = wx.NewId()
        self.Bind(wx.EVT_MENU, self.onAddAccount, id=randomId)
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_ALT, ord('a'), randomId)])
        self.SetAcceleratorTable(accel_tbl)

        
    def OnClickGrid(self, event):        
        obj = event.GetEventObject()
        named = obj.GetName()
        row = event.GetRow()
        col = event.GetCol()
        #grid = wx.FindWindowByName(named)
        self.cntd += 1
            
        row = self.GetGridCursorRow()
        col = self.GetGridCursorCol()
            
        
        colname = self.GetColLabelValue(col)
        rowname = self.GetRowLabelValue(row)  
                
        subtract = False
        override = 'no'
        taxExempt = False
        print("ColName : ",colname)
        print(f"CLicked + {self.cntd}")
        if self.cntd == 2:
            pass    
        elif 'pos_acct_grid' in named:
           
            if rowname == 'Account Number':
                acctNum = self.GetCellValue(row,col).strip()
                print("Acct Number : ",acctNum)
                count_returnd = CustomerManagement(acctNum).SearchCount()
                if count_returnd == 0:
                    print('None Returnd')
                    self.SetCellValue(row,col,'')
                    GridOps(self.GetName()).GridFocusNGo(row, col)
                    return
                
                elif count_returnd > 0:
                    
                    #style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
                    
                    with CustLookupDialog(self, title="Customer Lookup") as dlg:
                        custPicked = None
                        dlg.ShowModal()
                        custPicked = dlg.itemPicked.upper().strip()
                    
                print("Customer Lookup D : ", custPicked)
                
    
                self.SetCustInfo(custPicked)
                
                infoTab = wx.FindWindowByName('InfoTab').Load(acctNum)
                
            if rowname == 'Address Account':
                print("ON CLICK ADDRESS ACCOUNT CHANGE")

                newAccount = grid.GetCellValue(1,0)
                print("New Account : ",newAccount)
                p = re.search('A[0-9]+',newAccount)
                if p is None:
                    return

                addr_num = p.group(0)
                
                fields = 'address0,city,state,zipcode,unit'
                returnd = QueryOps().LookupDB('address_accounts').Specific(addr_num,'addr_acct_num',fields)
                print('address change : {}'.format(returnd))
                (address0d, cityd, statd, zipd, unitd) = returnd
                acctInfo = SetAcctInfo(grid.GetName())
                acctInfo.address(address0d,unit=unitd)
                acctInfo.cistzi(cityd,statd,zipd)
                
                readonly_list = ['Name','Address 1','Address 2',
                                 'City, State, Zip','A/R/Avail Credit',
                                 'Discount %','Ship To']
                
                GridOps(self.GetName()).GridListReadOnly(readonly_list)
            
            print("DONE & DONE")
            GridOps('pos_transactions_grid').GridFocusNGo(0)
    
    
    
    def onAddAccount(self, event):
        print("On Add Account")
        
        dlg = CustomerAddDialog(self)
        dlg.ShowModal()
        
        try:
            
            self.custPicked = dlg.itemPicked
        
        except:
            print(f'Cust Picked : {self.custPicked}')
        
                    
        
        #self.custPicked = dlg.itemPicked
        print("Customer Add D : ",self.custPicked) 
        dlg.Destroy()
   
   
    def ReadOnly(self, readOnly_list):
        if readOnly_list is not None:
            for xx in range(self.GetNumberRows()):
                    for item in readOnly_list:
                        rowName = self.GetRowLabelValue(xx)
                        if item in rowName:
                            self.SetReadOnly(xx, 0, True)

    
        #self.acctNum = None
        #self.addrAcctNum = None
        #self.fullName = None
        #self.address1 = None
        #self.address2 = None
        #self.csz = None
        #self.discount = None
        #self.availCredit = None
        #self.acctInfoName = acctInfoName

    def SetCustInfo(self, custNum):
        self.custNum = custNum
        query = '''SELECT address_acct_num, rental_of 
                   FROM customer_basic_info
                   WHERE cust_num=(?)'''
        data = [self.custNum,]
        returnd = SQConnect(query, data).ONE()
        if not returnd == None:
            self.addrNum = returnd[0]
            rental_list = returnd[1]
            print('## returned : {}\n\tself.addr : {}\trental_list : {}'.format(returnd, self.addrNum, rental_list))           
            style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
            dlg = AddressSelectionDialog(self, 
                                         title="Address Selection", 
                                         style=style, addrList=rental_list)
            dlg.ShowModal()
                    
            try:
                self.addrNum = dlg.addrPicked.upper().strip()
            except:
                pass
                
            dlg.Destroy()
        
        
            #-- Customer Name
            query = '''SELECT full_name
                       FROM customer_basic_info 
                       WHERE cust_num=(?)'''
        
            data = [self.custNum,]
            returnd = SQConnect(query, data).ONE()
        
            self.full_name = returnd[0]
            ##-- Customer Address 
            query = '''SELECT address0, address2, city, state, zipcode 
                       FROM address_accounts
                       WHERE addr_acct_num=(?)'''
            data = [self.addrNum,]
        
            returnd = SQConnect(query, data).ONE()
        
            (addr0, addr2, city, state, zipcode) = returnd
            self.addr = addr0
            self.addr2 = addr2
            self.csz = '{}, {}  {}'.format(city, state, zipcode)
        
            #-- Customer Sales Options
            query = '''SELECT no_discount, fixed_discount, discount_amt
                       FROM customer_sales_options
                       WHERE cust_num=(?)'''
            data = [self.custNum,]
            returnd = SQConnect(query, data).ONE()
            (no_discount, fixdiscount, disc_amt) = returnd
            discount = None
            if fixdiscount == '1':
                discount = str(discount)
        
            if discount is not None:
                if not '%' in discount:
                    discount = '{}%'.format(discount)
        
            self.discount = discount
        
            self.availCredit = QueryOps().CheckCredit(custNum)
        
            #self.availCredit = availCredit    
            self.addrAcctNum = self.addrNum
        
            self.UpdateSetAcctInfo()
        
    def custAcctNum(self, acctNum=None):
        
        self.acctNum = acctNum
        self.UpdateSetAcctInfo()
        
    def addressAcctNum(self, addrAcctNum):
        
        
        self.addrAcctNum(self, addrAcctNum)
        self.UpdateSetAcctInfo()
            
    def name(self, firstName, lastName=None):
        
        
        self.fullName = firstName
        if lastName is not None:
            self.fullName = '{} {}'.format(firstName, lastName)
        
        self.UpdateSetAcctInfo()
        
    def address(self, addr0, addr1=None, addr2=None, unit=None, debug=False):
        
        if unit == '':
            unit = None
        
        
        self.address1 = addr0
        if addr1 is not None:
            if re.search('unit',addr1, re.I):
                self.address1 = '{}  {}'.format(addr0, addr1)
                
            self.address2 = addr1
        if addr2 is not None:
            if re.search('unit',addr2, re.I):
                self.address2 = '{}  {}'.format(addr1, addr2)
        
        if unit is not None:
            self.address1 = '{} UNIT {}'.format(addr0,unit)
            if re.search('unit', unit, re.I):
                self.address1 = '{} {}'.format(addr0, unit)
               
        self.UpdateSetAcctInfo()

        
    def cistzi(self, cityd, stated=None, zipd=None):
        
        
        self.csz = '{}, {}  {}'.format(cityd, stated, zipd)
        if stated is None:
            self.csz = cityd
            
        self.UpdateSetAcctInfo()

    def discountd(self, fixdiscount='0', discount=None):
        
        
        if fixdiscount == '0':
            discount = None
        
        discount = str(discount)
        if discount is not None:
            if not '%' in discount:
                discount = '{}%'.format(discount)
        
        self.discount = discount
        
        self.UpdateSetAcctInfo()
        

    def availCredit(self, availCredit=None):
        
        
        self.availCredit = availCredit    
        self.UpdateSetAcctInfo()
        
    def UpdateSetAcctInfo(self):
        
        
        #grid = wx.FindWindowByName(self.acctInfoName)
        
        typefind = str(type(self))
        if re.search('grid',typefind, re.I):
            
            listing = [('Account Number',self.custNum),
                       ('Address Account',self.addrAcctNum),
                       ('Name',self.full_name),
                       ('Address 1',self.addr),
                       ('Address 2', self.addr2),
                       ('City, State, Zip',self.csz),
                       ('A/R/Avail Credit',self.availCredit),
                       ('Discount %',self.discount)]
                   
            rows = self.GetNumberRows()
            cols = self.GetNumberCols()
            
            for header, value in listing:
                for row in range(rows):
                    label = self.GetRowLabelValue(row)
                    if label == header:
                        if value is not None:
                            self.SetCellValue(row, cols-1, str(value))        
        
        else:
            acctInfo = '{ad}\n{cs}'.format(ad=self.address0,
                                           cs=self.csz)

            wx.FindWindowByName(self.acctInfoName).GetCtrl( acctInfo)



###----------------------------------------------------------------------------
class Totals_TxtCtrl(RH_TextCtrl):
    """ Sub Totals, Tax & Total Text Ctrls """
    def __init__(self, parent, name):
        """ Constructor """
        RH_TextCtrl.__init__(self, parent, name=name, size=(200, -1), style=wx.TE_READONLY | wx.ALIGN_RIGHT)
        
        font = (wx.Font(wx.FontInfo(18).Bold()))
        if 'pos_total_txtctrl' in name:
            font = (wx.Font(wx.FontInfo(26).Bold()))
        self.SetFont(font)
        self.SetBackgroundColour('Blue')
        self.SetForegroundColour('White')
        self.SetValue('.00')
            
###----------------------------------------------------------------------------
class Tax_Table_Grid(gridlib.Grid):
    """Table Info for Taxes."""
    def __init__(self, parent, name, size):
        gridlib.Grid.__init__(self, parent, style=wx.BORDER_SUNKEN, name=name, size=size)

        colLabel_list = [('Tax Name', 250),
                         ('Min\nSale', 70),
                         ('Max\nSale', 70),
                         ('Item\nMax', 70),
                         ('From\nAmt', 70),
                         ('Tax\nRate', 70),
                         ('From\nAmt', 70),
                         ('Tax\nRate', 70),
                         ('From\nAmt', 70),
                         ('Tax\nRate', 70)]
 
        self.CreateGrid(6, len(colLabel_list))      
        self.DisableDragRowSize()
        self.EnableEditing(True)
        self.SetLabelFont(wx.Font(wx.FontInfo(8)))
        self.SetRowLabelSize(0)
        #self.SetLabelBackgroundColour(Themes().GetColor('bg'))
        #self.SetLabelTextColour(Themes().GetColor('text'))
        #self.SetDefaultCellTextColour(Themes('Inventory').GetColor('text'))

        idx = 0
        for label, sized in colLabel_list:
            self.SetColLabelValue(idx, label)
            self.SetColSize(idx, sized)
            idx += 1
        
        self.Default()
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.OnRightClick)     

        
    def Default(self):
        for x in range(0, 6):
            for y in range(1, self.GetNumberCols()):
                self.SetCellEditor(x, y, gridlib.GridCellFloatEditor(width=6,precision=2))
                self.SetCellAlignment(x,y, wx.ALIGN_RIGHT, wx.ALIGN_BOTTOM)
                blank = '0.00'
                colLabel = self.GetColLabelValue(y)
                if 'Rate' in colLabel:
                    self.SetCellEditor(x, y, gridlib.GridCellFloatEditor(width=5,precision=3))
                    blank = '0.000'
                if 'Item' in colLabel:
                    self.SetCellEditor(x, y, gridlib.GridCellFloatEditor(width=6,precision=0))
                    blank = '0'
                    self.SetCellAlignment(x, y, wx.ALIGN_CENTRE, wx.ALIGN_BOTTOM)
                
                self.SetCellValue(x, y, blank)
        
        GridOps(self.GetName()).GridAlternateColor('')
        

    def OnLoad(self):
        cntret = LookupDB('tax_tables').Count()
        returnd = None
        if cntret > 0:
            for idx in range(cntret):
                fields = '''tax_name, min_sale, max_sale, item_max, 
                            from_amt0, tax_rate0, from_amt1, tax_rate1, 
                            from_amt2, tax_rate2'''
                returnd = LookupDB('tax_tables').General(fields)
        if returnd is not None:
            cnt = len(returnd)
            for i in range(0,cnt):
                vals = returnd[i]
                for y in range(0,9):
                    value = vals[y]
                    a = re.search('[A-Za-z]', str(value))
                    aty = str(type(a))
                    vty = str(type(value))
                    if not a:
                        if y in [1, 2, 4, 6, 8]:
                            value = format(value, '.2f')
                        elif y in [3]:
                            value = format(value, '.0f')
                        
                        elif 'decimal' in vty:
                            value = format(value, '.3f')
                
                    self.SetCellValue(i, y, str(value))
                        
    
    def OnSave(self):
        for x in range(0, 6):
            tax_name = self.GetCellValue(x, 0)
            if len(tax_name) > 0:
                QueryOps().CheckEntryExist('tax_name', tax_name, ['tax_tables'])
                neList = [(1, 'min_sale'),
                        (2, 'max_sale'),
                        (3, 'item_max'),
                        (4, 'from_amt0'),
                        (5, 'tax_rate0'),
                        (6, 'from_amt1'),
                        (7, 'tax_rate1'),
                        (8, 'from_amt2'),
                        (9, 'tax_rate2')]
                for y, field, in neList:
                    val = self.GetCellValue(x, y)
                    returnd = LookupDB('tax_tables').UpdateSingle(field, val, 'tax_name', tax_name)

    def Update(self, tax_dict):
        idx = 0
        self.ClearGrid()
        self.Default()
        for key, value in tax_dict.items():
            for i in range(len(value)):
                self.SetCellValue(idx, i, value[i])
            idx += 1
        
       


    def OnRightClick(self, event):
        obj = event.GetEventObject()
        rowclickd = event.GetRow()
        tax_dict = {}
        
        for x in range(self.GetNumberRows()):
            x_dict = {}
            for y in range(self.GetNumberCols()):
                a = self.GetCellValue(x, y)
                x_dict[y] = self.GetCellValue(x, y)
                
            tax_dict[x] = x_dict
        
        old = tax_dict.pop(rowclickd)
        self.Update(tax_dict)
        RecordOps('tax_tables').DeleteEntryRecord('tax_name', old[0])

        
###----------------------------------------------------------------------------
class TaxHoliday_Grid(gridlib.Grid):
    """Tax Holiday Grid Used on Tax Holiday Pages."""
    def __init__(self, *args, **kwargs):
        gridlib.Grid.__init__(self, *args, **kwargs)
        collabel_list = [('Item Number',200),('Description',775)]
        self.CreateGrid(100, len(collabel_list))
        self.SetDefaultCellAlignment(wx.ALIGN_LEFT,wx.ALIGN_CENTRE)
        self.SetLabelFont( wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.NORMAL) )
        self.SetRowLabelSize(0)
        idx = 0
        for label,sized in collabel_list:
            self.SetColLabelValue(idx, label)         
            self.SetColSize(idx, sized)
            idx += 1

        GridOps(self.GetName()).GridAlternateColor('')
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.OnRightClick)

    def OnRightClick(self, event):
        obj = event.GetEventObject()
        named = obj.GetName()
        row = event.GetRow()
        col = event.GetCol()
        self.DeleteRows(row)
        self.AppendRows()
        
        HUD.GridOps(named).GridAlternateColor('')
    
    def AddItem(self, item):
        newline = GridOps(self.GetName()).CurGridLine(blank=True)
        self.SetCellValue(newline, 0, item['upc'])
        self.SetCellValue(newline, 1, item['desc'])

               

        

class POS_Transactions_Grid(gridlib.Grid):
    """POS Acct Grid used at the POS Screen."""
    def __init__(self, parent, name, size):
        gridlib.Grid.__init__(self, parent, style=wx.BORDER_SUNKEN, name=name, size=size)
        
        colLabel_list = [('Item Number', 200), ('Description', 290),
                         ('Price', 120), ('Quantity', 90), ('Total', 90),
                         ('Discount', 105), ('Tx', 30)]

        self.CreateGrid(100, len(colLabel_list))
        self.EnableScrolling(False, True)
        self.DisableDragRowSize()
        self.SetLabelFont(wx.Font(wx.FontInfo(10)).Bold())
        self.SetRowLabelSize(0)
        self.SetLabelBackgroundColour(Themes().GetColor('bg'))
        self.SetLabelTextColour(Themes().GetColor('text'))
        
        idx = 0
        for label, sized in colLabel_list:
            self.SetColLabelValue(idx, label)
            self.SetColSize(idx, sized)
            idx += 1
        
        col_align_list = [('Price', wx.ALIGN_RIGHT),
                          ('Total', wx.ALIGN_RIGHT),
                          ('Quantity', wx.ALIGN_CENTER),
                          ('Discount', wx.ALIGN_CENTER),
                          ('Tx', wx.ALIGN_CENTER)]

        for xx in range(self.GetNumberRows()):
            readonly_list = ['Price', 'Total']
            for yy in range(self.GetNumberCols()):
                for label, attrib in col_align_list:
                    header = self.GetColLabelValue(yy)
                    if label in header:
                        self.SetCellAlignment(xx, yy, attrib, wx.ALIGN_CENTER)
                for readonly in readonly_list:
                    if readonly in header:
                        self.SetReadOnly(xx, yy, True)

        self.Bind(wx.EVT_KEY_DOWN, self.onTransactionGridKeyPress)
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.OnRightClick)
        
        GridOps(self.GetName()).GridAlternateColor('')

    def Add(self, upc_dict):
        a = GridOps(self.GetName())
        emptyrow = a.FindEmptyRow()
        mergd = False
        for row in range(emptyrow):
            if self.GetCellValue(row, 0) == upc_dict['upc']:
                qty = self.GetCellValue(row, 3)
                new_qty = self.Calculate(qty, upc_dict['qty'], '+')
                disc = self.GetCellValue(row, 5)
                new_disc = upc_dict['disc']
                #pout.v(f'New Discount : {new_disc}')
                if not re.search('%', disc, re.I) or len(new_disc) == 0:
                    disc = None
                else:
                    if '%' in disc:
                        disc = Decimal(disc.strip('%'))
                    if new_disc > disc:
                        disc = new_disc
                    

                new_total = self.Calculate(new_qty, upc_dict['price'], 'x', disc)

                self.SetCellValue(row, 3, str(new_qty))
                self.SetCellValue(row, 4, str(new_total))
                if disc is not None:
                    m = str(disc)+'%'
                    self.SetCellValue(row, 5, m)
                mergd = True

        if mergd is not True:
            setList = [('Item Number', upc_dict['upc']),
                    ('Description',upc_dict['desc']),
                    ('Quantity', upc_dict['qty']),
                    ('Price', upc_dict['price']),
                    ('Total', upc_dict['totalprice']),
                    ('Discount', upc_dict['disc']),
                    ('Tx', upc_dict['ntx'])]
            a.FillGrid(setList, emptyrow)   

        self.Update(upc_dict)             
            
    
    def Calculate(self, num_one, num_two, typed, disc=None):
        a = Decimal(num_one)
        b = Decimal(num_two)
        if '-' in typed:
            c = a - b
        if '+' in typed:
            c = a + b
        if 'x' in typed:
            c = a * b
        if disc is not None and len(disc) > 0:
            #pout.v(f'Discount : {disc}')
            d = (Decimal(disc) * c) + c
            c = d
        
        return RetailOps().Dollars(c)
        

    def Remove(self, upc):
        pass

    def Update(self, t_dict):
        a = GridOps(self.GetName())
        self.ClearGrid()
        t_type = ('SALE', 'RETURN')
        row = 0
        for typ in t_type:
            for transId in t_dict[typ]:
                for upcd in t_dict[typ][transId]:
                    setList = [('Item Number', upcd),
                               ('Description',t_dict[typ][transId][upcd]['Desc']),
                               ('Quantity', t_dict[typ][transId][upcd]['Qty']),
                               ('Price', t_dict[typ][transId][upcd]['Price']),
                               ('Total', t_dict[typ][transId][upcd]['TotalPrice']),
                               ('Discount', t_dict[typ][transId][upcd]['Discount']),
                               ('Tx', t_dict[typ][transId][upcd]['Taxable'])]

                    a.FillGrid(setList, row)
                    row += 1


                
    def onTransactionGridKeyPress(self, event):
        keycode = event.GetKeyCode()
        
        if keycode == wx.WXK_TAB:
            wx.FindWindowByName('pos_repeatLast_button').SetFocus()
        if keycode == wx.WXK_LEFT or keycode == wx.WXK_RIGHT or keycode == wx.WXK_UP or keycode == wx.WXK_DOWN:
            event.Skip()
    
        event.Skip()


    def OnRightClick(self, event):
        print('RIGHT CLICKED')
        obj = event.GetEventObject()
        rowclickd = event.GetRow()
        f_dict = {}
        
        for x in range(self.GetNumberRows()):
            x_dict = {}
            for y in range(self.GetNumberCols()):
                a = self.GetCellValue(x, y)
                x_dict[y] = self.GetCellValue(x, y)
                
            f_dict[x] = x_dict
        
        old = f_dict.pop(rowclickd)
        self.Update(f_dict)
    


###----------------------------------------------------------------------------

class SalesTracker_Grid(gridlib.Grid):
    """ Sales Tracker Grid """
    def __init__(self, parent, name, debug=False):
        """ Constructor """
        gridlib.Grid.__init__(self, parent, style=wx.BORDER_SUNKEN, name=name)
        
        self.EnableScrolling(False,False)
        self.DisableDragRowSize()
        self.CreateGrid(12,4)
        self.EnableEditing(False)
        self.SetColLabelSize(40)
        colLabel_list = ['Current\nYear','Last\nYear','2 Years\nAgo','3 Years\nAgo']
        for idx, label in enumerate(colLabel_list):
            self.SetColLabelValue(idx, label)
        
        self.SetRowLabelSize(90)
        rowLabel_list = ['January','February','March','April','May','June',
                         'July','August','September','October','November',
                         'December']
        
        for idx, label in enumerate(rowLabel_list):
            self.SetRowLabelValue(idx, label)
            
        GridOps(self.GetName()).GridAlternateColor('')
        wx.CallAfter(self.Default,event='')

    def Default(self, event):
        defaultValues = ['0.000','0.000','0.000','0.000']
        for row in range(self.GetNumberRows()):
            for col in range(self.GetNumberCols()):
                self.SetCellValue(row, col, defaultValues[col])
                self.SetCellAlignment(row,col,wx.ALIGN_RIGHT,wx.ALIGN_RIGHT)    
    
    def Load(self, upc=None):
        self.upc = upc
        if self.upc is None:
            return
        
        wx.FindWindowByName(self.GetName()).ClearCtrl(fillwith='0.000')

        thisyear = datetime.datetime.today().date().year
        lastyear = thisyear-1
        year2ago = thisyear-2
        year3ago = thisyear-3
        year_list = [thisyear, lastyear, year2ago, year3ago]
        for dated in year_list:
            for mnth in range(1,13):
                query = '''SELECT quantity 
                           FROM transactions 
                           WHERE year(date)=(?) and upc=(?) and month(date)=(?)'''
                data = [dated,self.upc,mnth,]
                returnd = SQConnect(query,data).ONE()
                #print 'returnd : ',returnd
                quantity = returnd
                if returnd is None:
                    continue
                cnt = len(returnd)
                if cnt > 1:
                    lqty = Decimal(0)
                    for qty in returnd:
                        lqty += Decimal(qty)
                elif cnt == 1:
                    lqty = returnd[0]
                else:
                    lqty = 0
                            
                mth = datetime.datetime.strptime(str(mnth), '%m')
                amnth = mth.strftime('%B')
                #print 'amth : ',amnth
                setList=[(str(amnth),str(lqty))]
                
                GridOps(self.GetName()).FillGrid(setList, col=0)
    


#-------------------------------------------------------------------------------

class Retail_Info(wx.Panel):
    """ Retail Info """
    def __init__(self, nocost=True):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        costd_list = [('Average Cost','details_avgcost_numctrl'),
                      ('Last Cost','details_lastcost_numctrl'),
                      ('Starting Margin','details_startingMargin_numctrl')]
        
        for label,name in costd_list:
            cost_text = wx.StaticText(self, -1, label=label+":")
            ctrl = RH_NumCtrl(self, -1, value=0, 
                                            name=name, 
                                            integerWidth=6, 
                                            fractionWidth=2)
            
            ctrl.SetValue('0.000')

            level1Sizer.Add(cost_text, 0, wx.ALL,2)
            level1Sizer.Add(ctrl, 0, wx.ALL,2)

        level2Sizer = wx.BoxSizer(wx.HORIZONTAL)

        returnd = LookupDB('item_pricing_schemes').General('name, scheme_list, reduce_by')
        priceschema_list = returnd

        box = wx.StaticBox(self, label="Pricing\nSchemes")
        boxSizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        boxSizer.Add((20,20), 0)
        xx=0
        rb = RH_Button(self, id=wx.ID_ANY, label="RESET", 
                                           name="details_pricescema_RESET_button")
        
        rb.Bind(wx.EVT_BUTTON, self.OnPriceSchemes)
        boxSizer.Add(rb, 0)

        for label, scheme_list, reduce_by in priceschema_list:
            rb = RH_Button(self, id=wx.ID_ANY, 
                           label=label, 
                           name=scheme_list)
            
            rb.Bind(wx.EVT_BUTTON, self.OnPriceSchemes)
            boxSizer.Add(rb, 0)
            xx+=1
        
        level2Sizer.Add(boxSizer, 0)

        self.retail_grid =  Retail_Grid(self, name='inv_details_cost_grid')    
        
        MainSizer.Add(level1Sizer, 0, wx.ALL|wx.EXPAND, 5)
        MainSizer.Add(level2Sizer, 0)
        MainSizer.Add(self.retail_grid, 0)

        self.SetSizer(MainSizer,0)
        

           
class Retail_Grid(gridlib.Grid):
    """ Retail Grid to used in a few places """
 
    def __init__(self, parent, name, formatted='margin', debug=False):
        """Constructor"""
        gridlib.Grid.__init__(self, parent, style=wx.BORDER_SUNKEN, name=name)
        self.formatted = formatted.lower()
        
        #self.CreateGrid(12, 8)
        
        rowlabel_list = ['Standard Retail','Price Level (A)', 
                              'Price Level (B)', 'Price Level (C)',
                              'Price Level (D)','Price Level (E)', 
                              'Price Level (F)','Price Level (G)',
                              'Price Level (H)','Price Level (I)',
                              'Sale Price']
        
        if self.formatted == 'margin':
            collabel_list = ['Unit','Price', 'M', 'Margin %']
        
        if self.formatted == 'nomargin':
            collabel_list = ['Unit','Price']
        
        self.CreateGrid(len(rowlabel_list), len(collabel_list))
        self.SetDefaultCellAlignment(wx.ALIGN_CENTRE,wx.ALIGN_CENTRE)
        self.SetLabelFont(wx.Font(wx.FontInfo(9)))
        self.SetRowLabelSize(120)
        module_name = 'Inventory'
        bgcolor = Themes(module_name).GetColor('bg') #(0,0,255)
        whitetext = Themes(module_name).GetColor('text') #(255,255,255)
        cell_color = Themes(module_name).GetColor('cell') #(217,241,232)
        discountColor = (255,255,0)

        
        idx = 0
        for rowlabelset in rowlabel_list:
            self.SetRowLabelValue(idx, rowlabelset)
            idx += 1
            
        idx = 0    
        for collabelset in collabel_list:
            
            self.SetColLabelValue(idx,collabelset)
            minWidths_byColName = {'Price':90,'Unit':60}
            for key, new_width in minWidths_byColName.items():
                if self.GetColLabelValue(idx) == key:
                    old_width = self.GetColSize(idx)
                    if old_width > new_width:
                        increment = "decreased"
                    elif old_width < new_width:
                        increment = "increased"
                    else:
                        increment = "pointlessly changed"

                    
                    self.SetColSize(idx,new_width)

            idx += 1
        if self.formatted == 'margin':
            basic_list = ['1','$0.00','M','0.0000']
        
        if self.formatted == 'nomargin':
            basic_list = ['1','$0.00']
            
        maxrows = self.GetNumberRows()
        maxcols = self.GetNumberCols()
        for row in range(maxrows):
            for col in range(maxcols):
                self.SetCellValue(row, col, basic_list[col])
                if col in [1,3]:
                    self.SetCellAlignment(row, col, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE)
                    

        self.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.OnCellChange)
        GridOps(self.GetName()).GridAlternateColor(maxrows)
        wx.CallAfter(self.OnLoad, event='')
        
     
    def OnLoad(self, event):
        maxrows = self.GetNumberRows()
        maxcols = self.GetNumberCols()
        for row in range(maxrows):
            for col in range(maxcols):
                value = self.GetCellValue(row, col).strip('$')
                if col == 0:
                    if value == 1:
                        value = 1
                    val = self.RoundIt(Decimal(value), '1')
                if col == 1:
                    val = self.RoundIt(Decimal(value), '1.00')
                if col == 3:
                    val = self.RoundIt(Decimal(value), '1.000')
                if col == 2:
                    val = ' '
                self.SetCellValue(row, col, str(val))
                
                   
    def MarginUpdate(self, avg_cost, retail):
        ''' Readjust Margin in margin Column according to avg_cost '''
        gross_profit = Decimal(retail) - Decimal(avg_cost)
        deci_margin = Decimal(gross_profit) / Decimal(retail)
        percentage_margin = Decimal(deci_margin) * Decimal(100)
        
        return percentage_margin
        
        
                
    def OnCellChange(self,event):
       
        
        obj = event.GetEventObject()
        named = obj.GetName()
        row = event.GetRow()
        col = event.GetCol()

        colname = self.GetColLabelValue(col)
        self.Refresh()
        
        if 'inv_details_cost_grid' in named:
            raw_value = self.GetCellValue(row,col).strip()
            # numeric check
            if all(x in '0123456789.+-' for x in raw_value):
                # convert to float and limit to 2 decimals
                valued = Decimal(raw_value)
                if colname == 'Unit':
                    valued = RetailOps().DoRound(valued, '1')
                else:
                    valued = RetailOps().DoRound(valued, '1.00')
                
                self.SetCellValue(row,col,str(valued))
            else:
                basic_list = ['1','$0.00','Margin','0.000']
                self.SetCellValue(row,col,basic_list[col])
                GridFocusNGo(self.GetName(), row, col)
                return

        #

        avgcost = wx.FindWindowByName('details_avgcost_numctrl').GetCtrl()
        
        #if avgcost:

        for yy in range(self.GetNumberCols()):
            header = self.GetColLabelValue(yy)
            if 'Unit' in header:
                unit = self.GetCellValue(row,yy)
            if 'Markup %' in header:
                calcMargin = self.GetCellValue(row,yy)
            if 'Price' in header:
                retail_from = self.GetCellValue(row,yy)

        unit = self.GetCellValue(row, 0)
        if unit == '0':
            unit = '1'
            self.SetCellValue(row, 0, unit)  
               
        if colname == 'Margin %':
            new_margin = self.GetCellValue(row, col)
            retail = self.calcRetail(avgcost, new_margin, unit)
            
            new_retail = self.RoundIt(retail, '1.00')
            margin_format = self.RoundIt(new_margin, '1.000')
            
            self.SetCellValue(row, 1, str(new_retail))
            self.SetCellValue(row, 3, str(margin_format))

            
        if colname == 'Price':
            retail = self.GetCellValue(row, col)
            percentage_margin = self.calcMargin(avgcost, retail, unit)
            
            Margindot4 = self.RoundIt(percentage_margin,'1.000')
            self.SetCellValue(row,3,str(Margindot4))

        if colname == 'Unit':
            retail = self.GetCellValue(row, 1)
            margin = self.GetCellValue(row, 3)
            
            
            if unit == '0' or unit == '':
                unitd = self.RoundIt(unit, '1')
                self.SetCellValue(row, 0, unitd)
                
            newretail_almost = self.calcRetail(avgcost,margin,unit)
            newretail = RetailOps().DoRound(newretail_almost, '1.00')

            self.SetCellValue(row,1,str(newretail))

    def calcMargin(self, avgcost, retail, unit, debug=False):
        if unit == '0':
            unit = '1'    
        actual_retail = Decimal(retail)/Decimal(unit)
            
        gross_profit = Decimal(actual_retail) - Decimal(avgcost)
        if Decimal(actual_retail) == 0:
            percentage_margin = 0
        else:   
            deci_margin = Decimal(gross_profit) / Decimal(actual_retail)
            percentage_margin = Decimal(deci_margin) * Decimal(100)
        
        return percentage_margin
            
            
    def calcRetail(self, avgcost, margin, unit, debug=False):
        almost_margin = Decimal(1) - (Decimal(margin)/100)
        retail = Decimal(avgcost)/(almost_margin)
        retail = Decimal(retail) * Decimal(unit)
            
        #print 'retail 1 : ',retail
        if Decimal(margin) < 0:
            almost_margin = Decimal(1) - Decimal(margin)
            retail = Decimal(avgcost)/(almost_margin)
            retail = Decimal(retail) * Decimal(unit)
                
        #print 'retail 2 : ',retail
            
        return retail
    
    def RoundIt(self, oldmoney, unitd, debug=False):
        noPenny, rndScheme = False, '3'
        #(self.noPenny, self.rndScheme) = HU.LookupDB('TAX','tax_name','tax_tables','no_pennies_rounding, RNDscheme')
        
        if rndScheme == 0:
            rndScheme = 3
        rnd = str(rndScheme)
        
        roundtype = {'1':'ROUND_DOWN','2':'ROUND_HALF_UP','3':'ROUND_UP'}
        newMoney = Decimal(Decimal(oldmoney).quantize(Decimal(unitd), rounding=roundtype[rnd]))
    
        return newMoney

    def CurGridLine(self, blank=False):
        row = 0
        maxRows = self.GetNumberRows()
        for x in range(maxRows):
            value = self.GetCellValue(x,0)
            if value == '' or value is None:
                row = x - 1
                if blank is True:
                    row = x
                
                if row < 0:
                    row = 0    
                
                return row     

    def GetGridCursor(self):
        row = self.GetGridCursorRow()
        col = self.GetGridCursorCol()
    
        return row, col   
    
    def GridFocusNGo(self, row=None, col=0):
        if row == None:
            row = CurGridLine(gridname)+1
        self.SetFocus()
        wx.CallAfter(self.SetGridCursor, row, col) 


    def OnSave(self, event=None, upc=None):
        
        if upc is None:
            return
        
        QueryOps().CheckEntryExist('upc',upc, ['item_retails'])
        
        save_list = [(0, 0, 'item_retails', 'standard_unit'),
                     (0, 1, 'item_retails', 'standard_price'),
                     (1, 0, 'item_retails', 'level_a_unit'),
                     (1, 1, 'item_retails', 'level_a_price'),
                     (2, 0, 'item_retails', 'level_b_unit'),
                     (2, 1, 'item_retails', 'level_b_price'),
                     (3, 0, 'item_retails', 'level_c_unit'),
                     (3, 1, 'item_retails', 'level_c_price'),
                     (4, 0, 'item_retails', 'level_d_unit'),
                     (4, 1, 'item_retails', 'level_d_price'),
                     (5, 0, 'item_retails', 'level_e_unit'),
                     (5, 1, 'item_retails', 'level_e_price'),
                     (6, 0, 'item_retails', 'level_f_unit'),
                     (6, 1, 'item_retails', 'level_f_price'),
                     (7, 0, 'item_retails', 'level_g_unit'),
                     (7, 1, 'item_retails', 'level_g_price'),
                     (8, 0, 'item_retails', 'level_h_unit'),
                     (8, 1, 'item_retails', 'level_h_price'),
                     (9, 0, 'item_retails', 'level_i_unit'),
                     (9, 1, 'item_retails', 'level_i_price'),
                     (10, 0, 'item_retails', 'on_sale_unit'),
                     (10, 1, 'item_retails', 'on_sale_price')]
                     
        for row, col, table, field in save_list:
                ctrl = self.GetCellValue(row, col)
                ctrl = ctrl.strip('$')
                
                query = '''UPDATE {}
                           SET {}={}
                           WHERE upc=(?)'''.format(table, field, ctrl)
                data = (upc,)
                returnd = SQConnect(query, data).ONE()


    def Load(self, event=None, upc=None):
        
        retail_list = ['standard_price','level_(a)_price','level_(b)_price',
                       'level_(c)_price','level_(d)_price','level_(e)_price',
                       'level_(f)_price','level_(g)_price','level_(h)_price',
                       'level_(i)_price','on_sale_price']
        
        retails = RetailOps().RetailSifting(upc)
        
        for name in retail_list:
            for xx in range(self.GetNumberRows()):
                field = re.sub('[\(\)]','', name)
                key = re.sub('_price', '', name)
                key2 = re.sub('_', ' ', key)
                xlabel = self.GetRowLabelValue(xx)
                unitd = str(retails[field]['unit'])
                priced = str(retails[field]['price'])

                #print "xlabel : key2 = {} : {}".format(xlabel, key2)
                if key2 in xlabel.lower():
                    self.SetCellValue(xx,0, unitd)
                    self.SetCellValue(xx,1, priced)
                    #print "xlabel : key2 = {} : {} : ({} -- {})".format(xlabel, key2, retails[field][0],retails[field][1])

    def Clear(self):
        grid_default_list = [('Unit','1'),('Price','$0.00'),
                             ('Margin','Margin'),('Margin %','0.000')]
        
        for xx in range(self.GetNumberRows()):
            GridOps(self.GetName()).FillGrid(grid_default_list,row=xx)

        
        for xx in range(self.GetNumberRows()):
            for yy in range(self.GetNumberCols()):
                self.SetCellValue(xx,yy,'1')                   
        
####-------------
class POSLinks_Grid(gridlib.Grid):
    """ POS Sales Links Grid """
    def __init__(self, parent, name, debug=False):
        gridlib.Grid.__init__(self, parent, style=wx.BORDER_SUNKEN, name=name)
        
        
        poslinks_col_list = [('Item Number',255),
                             ('Description',350)]
                             
        self.EnableScrolling(True,True)
        self.DisableDragRowSize()
        self.SetRowLabelSize(0)
        self.CreateGrid(15,len(poslinks_col_list))
        idx = 0
        for label,sized in poslinks_col_list:
            self.SetColLabelValue(idx, label)
            self.SetColSize(idx, sized)
            idx += 1

        self.EnableEditing(True)
        self.SetLabelFont(wx.Font(wx.FontInfo(9)) )

        GridOps(self.GetName()).GridAlternateColor('')

        self.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.onPOSsalesLinks)

        
    def onPOSsalesLinks(self, event):
        obj = event.GetEventObject()
        named = obj.GetName()
        row = event.GetRow()
        col = event.GetCol()

        grid = wx.FindWindowByName(named)
        colname = grid.GetColLabelValue(col)
        
        if colname == 'Item Number':
            pass            
 
    def OnLoad(self, table, colheader, whereKey, whereValue):
        pass
        
    def OnSave(self, table, colheader, whereKey, whereValue):
        jsn = GridOps(self.GetName()).GRIDtoJSON()
        pout.v(f'POS LINKS JSON : {jsn}')

    
    def Clear(self):
        default_list = [('Item Number', ''),('Description','')]
        
        for xx in range(self.GetNumberRows()):
            GridOps(self.GetName()).FillGrid(default_list,row=xx)

           
class Order_Grid(gridlib.Grid):
    """ Retail Grid to used in a few places """
 
    def __init__(self, parent, name):
        """Constructor"""
        gridlib.Grid.__init__(self, parent, style=wx.BORDER_SUNKEN, name=name)
        self.tableName = None
        self.fieldName = None
        #self.CreateGrid(12, 8)
        rowlabel_list = []
        for month_num in range(1,13):
            month = datetime.date(2016, month_num, 1).strftime('%B')
            rowlabel_list.append(month)
            

        collabel_list = ['Order Point','Max Order']
        self.CreateGrid(len(rowlabel_list), len(collabel_list))
        self.SetDefaultCellAlignment(wx.ALIGN_RIGHT,wx.ALIGN_RIGHT)
        self.SetLabelFont(wx.Font(wx.FontInfo(9)) )
        self.SetRowLabelSize(120)
        for idx, rowlabelset in enumerate(rowlabel_list):
            
            self.SetRowLabelValue(idx, rowlabelset)

        GridOps(self.GetName()).GridAlternateColor('')

        for idx, collabelset in enumerate(collabel_list):
            
            self.SetColLabelValue(idx,collabelset)


        self.AutoSize()
        basic_list = [('Order Point','0'),('Max Order','0')]
        
        for xx in range(self.GetNumberRows()):
            gridFill = GridOps(self.GetName()).FillGrid(basic_list,row=xx)

    def OnSave(self, whereKey, whereValue):
        jsn = GridOps(self.GetName()).GRIDtoJSON()
        
        pout.v(f"ORDER GRID JSON : {jsn}")
        time.sleep(3)
        returnd = LookupDB(self.tableName).UpdateSingle(self.fieldName, jsn, whereKey, whereValue)

    def OnLoad(self, whereKey, whereValue):
        returnd = LookupDB(self.tableName).Specific(whereValue, whereKey, self.fieldName)
        pout.v(f"returnd : {returnd}")
        GridOps(self.GetName()).JSONtoGrid(returnd)



####----------------

class Activity_Grid(gridlib.Grid):
    """ Item Activity """
    def __init__(self, parent, name, debug=False):
        gridlib.Grid.__init__(self, parent, name=name, style=wx.BORDER_SUNKEN)
        
        self.EnableScrolling(False,True)
        self.DisableDragRowSize()
        colLabel_list =['Activity Date','Sales Volume', 'Sales Amount',
                        'Gross Profit']
        

        self.CreateGrid(20,len(colLabel_list))
        self.SetRowLabelSize(0)
        for idx,item in enumerate(colLabel_list):
            self.SetColLabelValue(idx, item)
            self.SetColSize(idx, 120)

        self.EnableEditing(False)
        self.SetLabelFont(wx.Font(wx.FontInfo(9)) )

        GridOps(self.GetName()).GridAlternateColor('')
        
        wx.CallAfter(self.OnLoad, event='')
        
    def OnLoad(self, event):
        maxrows = self.GetNumberRows()
        maxcols = self.GetNumberCols()
        
        for xx in range(maxrows):
            for yy in range(maxcols):
                col_label = self.GetColLabelValue(yy)
                val = self.GetCellValue(xx,yy)
                if not val:
                    continue 
                    
                if 'Activity Date' in col_label:
                    self.SetCellAlignment(xx,yy, wx.CENTER, wx.CENTER)
                    
                if 'Sales Volume' in col_label:
                    value = RetailOps().DoRound(val, '1.000')
                    self.SetCellValue(xx,yy, value)                 
                    self.SetCellAlignment(xx,yy,wx.CENTER, wx.CENTER)
                    
                if 'Sales Amount' in col_label:
                    value = RetailOps().DoRound(val, '1.00')
                    self.SetCellValue(xx,yy, value)             
                    self.SetCellAlignment(xx,yy, wx.RIGHT, wx.CENTER)
                    
                if 'Gross Profit' in col_label: 
                    value = RetailOps().DoRound(val, '1.000')
                    self.SetCellValue(xx,yy, value)             
                    self.SetCellAlignment(xx,yy, wx.RIGHT, wx.RIGHT)
             


class FillIn(object):
    def __init__(self,gridname):
        
        self.grid = wx.FindWindowByName(gridname)
        
    
    
    def POSCustAcctGrid(self,custNum=None):
        
        grid = self.grid
        acctInfo = SetAcctInfo(grid.GetName())
        if custNum is None:
            set_list = [('Account Number','PLACEHOLDER')]
            #grid.SetCellValue(0,0,'PLACEHOLDER')
            GridOps(grid.GetName()).FillGrid(set_list, col=0)
                
            return
                    
        fields = '''cust_num, first_name, last_name,
                    address_acct_num, phone_numbers'''
        returnd = LookupDB('customer_basic_info').Specific(custNum,'cust_num',fields)
                                            
        
        (cust_numd,first_named, last_named, address_acct_numd,phoned_JSON) = returnd
                
        fields = '''street_num, street_direction, street_name,
                    street_type,unit,city,zipcode,state,address2'''
        returnd = LookupDB('address_accounts').Specific(address_acct_numd,'addr_acct_num',fields)
        
                
        (street_numd,street_directiond,street_named,street_typed, unitd,cityd,zipcoded,stated,addressed2) = returnd
        
        print('flname : {} {}'.format(first_named, last_named))
        
        acctInfo.custAcctNum(cust_numd)
        
        acctInfo.name(first_named, last_named)
        #flname = '{0} {1}'.format(first_named, last_named)

        addressed = TextOps().AllinaRow(street_numd,street_directiond,street_named,street_typed,unit=unitd)
        acctInfo.address(addressed)
        acctInfo.cistzi(cityd, stated, zipcoded)
        
        fields = 'fixed_discount, discount_amt'
        returnd = LookupDB('customer_sales_options').Specific(custNum,'cust_num',fields)
        
        fixed_discountd, discount_amtd = '0', None
        
        (fixed_discountd, discount_amtd) = returnd
        
        print('fixed _discoutn : {} {}'.format(fixed_discountd, discount_amtd))
        acctInfo.discountd(fixed_discountd, discount_amtd)        
        
        grid = wx.FindWindowByName('pos_acct_grid')

        rows = grid.GetNumberRows()
        cols = grid.GetNumberCols()

        phoned = phoned_JSON
        print("Phoned : ",phoned)
        phone_list = []
        if phoned:
            for key,value in phoned.items():
                print("Key : {0}, Value : {1}".format(key, value))
                whered = value[0].strip()
                valued = re.sub('[()\ -]+', '', value[1])
                sets = '{}{}{}-{}{}{}-{}{}{}{}'.format(*valued)
                phone_list_tup = '{0} : {1}'.format(whered, sets)
                phone_list.append(phone_list_tup)
                print("Phone List  : ",phone_list)
                print("pHone List 2 : ",phone_list[0])
            grid.SetCellValue(6,0,phone_list[0])
            grid.SetCellEditor(6,0,HU.GridCellComboBox(listd=phone_list))


    def POSAddrAcctGrid(self, custNum, addrAcctNum=None, debug=False):
        
        grid = self.grid
        
        if custNum == '' or custNum is None:
            return
            
        fields = '''cust_num,first_name,last_name,cust_num,
                    address_acct_num,phone_numbers,rental_of'''
        returnd = LookupDB('customer_basic_info').Specific(custNum, 'cust_num',fields)
                
        
        (cust_numd,first_named, last_named, cust_numd,
         address_acct_numd,phoned_JSON,rental_JSON) = returnd

        if addrAcctNum is not None:
            address_acct_numd = addrAcctNum
        fields = '''street_num, street_direction, street_name,
                    street_type, unit, city, zipcode, state,
                    address2'''
        returnd = LookupDB('address_accounts').Specific(address_acct_numd,'addr_acct_num',fields)
                
        (street_numd,street_directiond,street_named,street_typed,unitd,
         cityd,zipcoded,stated,addressed2) = returnd
        
        rental_dict = {}
        if rental_JSON is not None and len(rental_JSON) > 0 and addrAcctNum is None:
            rental_list = rental_JSON
            dict_cnt = len(rental_dict)
            
            
            
            rental_list.append(address_acct_numd)

            addr_choice = []
            for addr_num in rental_list:
                fields = 'address0,city,state,unit'
                returnd = HU.LookupDB('address_accounts').Specific(addr_num,'addr_acct_num',fields)
                        
                (address0d, cityd,statd,unitd) = returnd

                if unitd is None:
                    main_addr = '{}\t{} UNIT {}, {}, {}'.format(addr_num,address0d,unitd,cityd,statd)
                else:
                    main_addr = '{}\t{}, {}, {}'.format(addr_num,address0d,cityd,statd)


                addr_choice.append(main_addr)
                
            grid.SetCellValue(1,0,addr_choice[0])
            grid.SetCellEditor(1,0,HU.GridCellComboBox(addr_choice))
                
            
            style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
            dlg = CDialog.AddressSelectionDialog(self, 
                                                 title="Address Selection", 
                                                 style=style, addrList=rental_list)
            dlg.ShowModal()
                    
            try:
                self.addrPicked = dlg.addrPicked.upper().strip()
            except:
                pass
                
            dlg.Destroy()
                
            
                
            regex = re.compile(self.addrPicked)
            idxs = [i for i, item in enumerate(addr_choice) if re.search(regex, item)]
            
            #choiceKey = addr_choice.index(self.addrPicked)
            
                
            grid.SetCellValue(1,0,addr_choice[idxs[0]])

        else:
            address0d = TextOps().AllinaRow(street_numd, street_directiond,street_named, street_typed, unitd)
            main_addr = '{}\t{}, {}, {}'.format(addrAcctNum,address0d,cityd,stated)

            grid.SetCellValue(1,0,main_addr)
        

        rowname = 'Address Account'
                
        if rowname == 'Address Account':
            if rowname:
                

                newAccount = grid.GetCellValue(1,0)
                
                p = re.search('A[0-9]+',newAccount)
                if p is None:
                    return

                addr_num = p.group(0)
                
                fields = 'address0,city,state,zipcode,unit'
                returnd = LookupDB('address_accounts').Specific(addr_num,'addr_acct_num',fields)
                
                (address0d, cityd,statd,zipd,unitd) = returnd
                acctInfo = SetAcctInfo(grid.GetName())
                cszd = f'{cityd}, {statd}  {zipd}'
                set_list = [('Address 1',address0d),('City, State, Zip',cszd)]
                acctInfo.address(address0d)
                acctInfo.cistzi(cityd,statd,zipd)
                #grid.SetCellValue(3,0,address0d)
                #grid.SetCellValue(5,0,cszd)

                readonly_list = ['Name','Address 1','Address 2',
                                 'City, State, Zip','A/R/Avail Credit',
                                 'Discount %','Ship To']
                
                GridOps(grid.GetName()).GridListReadOnly(readonly_list)

            print("DONE & DONE")
            GridOps('pos_transactions_grid').GridFocusNGo(0)

    
    def POSTransGrid(self, gridname, transId):
        grid = wx.FindWindowByName(gridname)
        query = 'SELECT upc,description,quantity,unit_price,discount,total_price,tax1,tax2,tax3,tax4,tax_never FROM transactions WHERE transaction_id=(?)'
        data = (transId,)
        returnd = HU.SQConnect(query,data).ALL()
        
        idx = 0
        for upc, desc, qty, uprice, disc, totprice,tax1,tax2,tax3,tax4,tax5 in returnd:
            taxd = [tax1, tax2, tax3, tax4, tax5]
            isTaxed = 'Tx'
            for tax in taxd:
                if tax == 1:
                    isTaxed = 'nTx'
                    break
            setList = [('Item Number',upc),('Description',desc),
                       ('Price',HU.RoundIt(uprice, '1.00')),
                       ('Quantity',HU.RoundIt(qty,'1.00')),
                       ('Total',HU.RoundIt(totprice, '1.00')),
                       ('Disc',disc),
                       ('Tx',isTaxed)]
                    
            GridOps(gridname).FillGrid(setList, row=idx)
            idx += 1            
        

class CustomerAddDialog(wx.Dialog):
    def __init__(self, *args, **kwargs): #parent, title="Add Customer", size=(1225,850)):
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
        kwargs['title'] = 'Add Customer'
        kwargs['size'] = (1225, 850)
        kwargs['style'] = style
        super(CustomerAddDialog, self).__init__(*args, **kwargs)
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        level0Sizer = wx.BoxSizer(wx.HORIZONTAL)
        col1Sizer = wx.BoxSizer(wx.VERTICAL)
        col2Sizer = wx.BoxSizer(wx.VERTICAL)
        
        col1_level0Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        cust_box = wx.StaticBox(self, -1, label="Customer Number")
        cust_boxSizer = wx.StaticBoxSizer(cust_box, wx.VERTICAL)
        
        ctrl = RH_MTextCtrl(self, -1,
                            name = 'custadd_custnum_txtctrl',
                            size = (160, -1),
                            formatcodes = "!")
        
        ctrl.tableName = 'customer_basic_info'
        ctrl.fieldName = 'cust_num'
        ctrl.SetToolTip(wx.ToolTip('Optional: User-Define Customer Number'))
        ctrl.SetFocus()
        ctrl.Bind(wx.EVT_KILL_FOCUS,self.OnCustNumCheck)
        
        cust_boxSizer.Add(ctrl, 0, wx.ALL|wx.EXPAND, 3)
        btn_boxSizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_list = [('Check','custadd_custnumchk_button', self.OnCustNumCheck),
                    ('Auto','custadd_custnumauto_button',self.OnCustNumAuto)]
        for label,name,handlr in btn_list:
            btn = RH_Button(self, -1, name=name, label=label)
            btn.Bind(wx.EVT_BUTTON, handlr)
                
            btn_boxSizer.Add(btn, 0)
            
        
        cust_boxSizer.Add(btn_boxSizer, 0)
        
        col1_level0Sizer.Add(cust_boxSizer,0,wx.ALL|wx.EXPAND, 5)
        
        col1_level1Sizer = wx.BoxSizer(wx.VERTICAL)
        col1_level1aSizer = wx.BoxSizer(wx.HORIZONTAL)
        col1_level1bSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        
        
        lvl1_list = [('Prefix','custadd_prefix_btn',70,'customer_basic_info','prefix'),
                     ('First Name/Business Name','custadd_fname_txtctrl', 240,'customer_basic_info','first_name'),
                     ('Middle Initial','custadd_midInitial_txtctrl',50,'customer_basic_info','middle_initial'),
                     ('Last Name','custadd_lname_txtctrl',160,'customer_basic_info','last_name'),
                     ('Suffix','custadd_suffix_txtctrl',60,'customer_basic_info','suffix')]

        for label,named,sized,tableName, fieldName in lvl1_list:
            box = wx.StaticBox(self, -1, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            
            if 'btn' in named:
                ctrl = RH_Button(self, -1, name = named)
                ctrl.listd = ['Mr.','Mrs.','Ms.','Dr.']
            
            if 'txtctrl' in named:
                ctrl = RH_TextCtrl(self, -1, name=named, size=(sized,-1))
            
            ctrl.tableName = tableName
            ctrl.fieldName = fieldName
            ctrl.Bind(wx.EVT_KILL_FOCUS, EventOps().Capitals)
            
            boxSizer.Add(ctrl, 0, wx.ALL, 3)
            if 'suffix' in named:
                tuple_of_names = ('custadd_prefix_combobox',
                                  'custadd_fname_txtctrl',
                                  'custadd_midInitial_txtctrl',
                                  'custadd_lname_txtctrl',
                                  'custadd_suffix_txtctrl')
                
                
            col1_level1aSizer.Add(boxSizer, 0)
        
        ctrl = RH_TextCtrl(self, -1, 
                           name='custdata_fullName_txtctrl', 
                           size=(300,-1))
        
        ctrl.tableName = 'customer_basic_info'                   
        ctrl.fieldName = 'full_name'
        
        col1_level1bSizer.Add(ctrl, 0, wx.ALL) 
        
        col1_level1Sizer.Add(col1_level1aSizer, 0, wx.ALL,1)
        col1_level1Sizer.Add(col1_level1bSizer, 0, wx.ALL,1)
        col1_level0Sizer.Add(col1_level1Sizer, 0, wx.ALL,5)
            
        # ph_box = wx.StaticBox(self, -1, label="Phone Numbers")
        # self.ph_boxSizer = wx.StaticBoxSizer(ph_box, wx.VERTICAL)
        
        # ph_add_boxSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # cbox = RH_Button(self, -1, 
        #                        name = "custadd_phone_btn")
                               
        # cbox.listd = ['CELL','PHONE','FAX','CONTACT','WORK']
        
        # ph_add_boxSizer.Add(cbox, 0, wx.ALL, 5)
        
        # foneNum_txtctrl = RH_MTextCtrl(self, -1, '', 
        #                                   mask = '(###) ###-####', 
        #                                   validRegex = "^\(\d{3}\) \d{3}-\d{4}", 
        #                                   size=(120, -1), 
        #                                   name="custadd_phone_txtctrl")

        # ph_add_boxSizer.Add(foneNum_txtctrl, 0, wx.ALL, 5) 
        
        # btn = RH_Button(self, -1, label="Add")
        # btn.Bind(wx.EVT_BUTTON, self.OnPhoneAdd)
        # ph_add_boxSizer.Add(btn, 0, wx.ALL, 5)
        
        # lc = PhoneNumber_ListCtrl(self, name='custadd_phone_listctrl',size=(240,200))
        
        # self.ph_boxSizer.Add(self.ph_add_boxSizer, 0, wx.ALL, 5)
        # btn = RH_Button(self, -1, label="REMOVE SELECTED")
        # btn.Bind(wx.EVT_BUTTON, self.OnPhoneDel)
        
        # ph_boxSizer.Add(lc, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        # ph_boxSizer.Add(btn, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        custnum = wx.FindWindowByName('custadd_custnum_txtctrl').GetCtrl()
        phone = PhoneNumber_Panel(self, custNum=custnum, tableName='cust_basic_info', fieldName='phone_numbers')
        col2Sizer.Add(phone, 0)
        
        
        col1_level2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        FindButton = RH_Button(self, -1, label="Main Address Search")
        FindButton.Bind(wx.EVT_BUTTON, self.OnMainHouseSearch)
        
        col1_level2Sizer.Add(FindButton, 0)
        
        col1_level3Sizer = wx.BoxSizer(wx.VERTICAL)
        col1_level3bSizer = wx.BoxSizer(wx.HORIZONTAL)
        level3_list = [('custadd_address1_txtctrl',250),
                       ('custadd_unit_txtctrl',100),
                       ('custadd_address2_txtctrl',250),
                       ('custadd_address3_txtctrl',250)]
        
        txt = wx.StaticText(self, -1, label="Main Address")
        ctrl = RH_TextCtrl(self, -1, 
                           name='custadd_addr_acct_num_txtctrl', 
                           size=(120,-1))
        
        col1_level3Sizer.Add(txt, 0, wx.ALL, 5)
        col1_level3bSizer.Add(ctrl, 0, wx.ALL|wx.EXPAND, 5)
        for item,sized in level3_list:
            ctrl = RH_TextCtrl(self, -1, 
                               name=item, 
                               size=(sized, -1),
                               style=wx.TE_READONLY)
            
            
            if 'unit' in item:
                sizer = wx.BoxSizer(wx.HORIZONTAL)
                txt = wx.StaticText(self, -1, label="Unit")
                sizer.Add(txt, 0, wx.ALL|wx.EXPAND, 5)
                sizer.Add(ctrl, 0, wx.ALL|wx.EXPAND, 5)
                col1_level3Sizer.Add(sizer, 0)
            else:     
            
                col1_level3Sizer.Add(ctrl, 0, wx.ALL, 5)
            
            
        
        
        col1_level4Sizer = wx.BoxSizer(wx.HORIZONTAL)
        csz_list = [('City','custadd_city_txtctrl',120),
                    ('State','custadd_state_txtctrl',95),
                    ('Zipcode','custadd_zipcode_txtctrl',90)]

        for labeld,named,width in csz_list:
            txt = wx.StaticText(self, -1, label=labeld)
            
            if 'City' in labeld:
                ctrl = RH_TextCtrl(self, -1, 
                                   name=named, 
                                   size=(width,-1))
                ctrl.Bind(wx.EVT_KILL_FOCUS, EventOps().Capitals)
            elif 'State' in labeld:
                ctrl = RH_MTextCtrl(self, -1, 
                                       name=named, 
                                       size=(width,-1), 
                                       formatcodes = '!')
            elif 'Zipcode' in labeld:
                ctrl = RH_TextCtrl(self, -1, 
                                       name=named, 
                                       size=(width,-1))
                                       
                
            col1_level4Sizer.Add(txt, 0,wx.ALL|wx.EXPAND, 5)
            col1_level4Sizer.Add(ctrl, 0, wx.ALL|wx.EXPAND, 5)    
                
        col1_level5Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        txt = wx.StaticText(self, -1, label="E-mail Address")
        ctrl = RH_MTextCtrl(self, -1, 
                               name="custadd_email_txtctrl", 
                               autoformat="EMAIL", 
                               size=(250, -1))
        
        
        col1_level5Sizer.Add(txt, 0, wx.ALL|wx.EXPAND, 5)
        col1_level5Sizer.Add(ctrl, 0, wx.ALL|wx.EXPAND, 5)
        
        col1_level6Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        level6_list = [('Contact 1', 'custadd_contact1_txtctrl'),
                       ('Contact 2','custadd_contact2_txtctrl')]
        
        for label,name in level6_list:
            txt = wx.StaticText(self, -1, label=label)
            txtctrl = RH_TextCtrl(self, -1, name=name, size=(160, -1))
            col1_level6Sizer.Add(txt, 0, wx.ALL|wx.EXPAND, 5)
            col1_level6Sizer.Add(txtctrl, 0, wx.ALL|wx.EXPAND, 5)
        
        col1_level7Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        level7_list = [('Account Type','custadd_accttype_combobox','organizations','account_types')]
        
        for label,name, tableName, fieldName in level7_list:
            txt = wx.StaticText(self, -1, label=label)
            if 'combobox' in name:
                ctrl = RH_ComboBox(self, -1, name=name, choices=[])
                ctrl.fieldName = fieldName
                ctrl.tableName = tableName
            else:
                ctrl = RH_TextCtrl(self, -1, name=name, size=(120, -1))
                ctrl.fieldName = fieldName
                ctrl.tableName = tableName
            col1_level7Sizer.Add(txt, 0,wx.ALL|wx.EXPAND, 5)
            col1_level7Sizer.Add(ctrl, 0, wx.ALL|wx.EXPAND, 5)
        
        col1_level8Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        level8_list=[('Customer Code','custadd_custcode_combobox', 'organizations','customer_codes'),
                     ('Statement of Terms', 'custadd_statement_terms_txtctrl')]
            
        for label,name in level8_list:
            txt = wx.StaticText(self, -1, label=label)
            if 'combobox' in name:
                ctrl = RH_ComboBox(self, -1, name=name, choices=[])
            else:
                ctrl = RH_TextCtrl(self, -1, name=name, size=(150, -1))
            
            col1_level8Sizer.Add(txt, 0,wx.ALL|wx.EXPAND, 5)
            col1_level8Sizer.Add(ctrl, 0,wx.ALL|wx.EXPAND, 5)
             
            
        col1_level9Sizer = wx.BoxSizer(wx.HORIZONTAL)
        txt = wx.StaticText(self, -1, label="Birthday\n mm/dd")
        ctrl = RH_MTextCtrl(self, -1, 
                               name="custadd_birthday_txtctrl", 
                               mask="##/##", 
                               validRegex="\d{2}/\d{2}")
        
        col1_level9Sizer.Add(txt, 0, wx.ALL|wx.EXPAND, 5)
        col1_level9Sizer.Add(ctrl, 0,wx.ALL|wx.EXPAND, 5)
        
        level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        level1_list = [('SAVE','custadd_save_button',self.OnSaveCustomerAdd),
                       ('RESET FORM','custadd_reset_button',
                            self.OnResetCustomerAdd),
                       ('CANCEL','custadd_cancel_button',
                            self.OnCancelCustomerAdd)]
        
        for label,name,handlr in level1_list:
            btn = RH_Button(self, -1, label=label,name=name)
            btn.Bind(wx.EVT_BUTTON, handlr)
            level1Sizer.Add(btn, 0, wx.ALL|wx.EXPAND|wx.CENTER, 5)
        
        sizer_list = [col1_level0Sizer, col1_level1Sizer, col1_level2Sizer, 
                      col1_level3bSizer, col1_level3Sizer,col1_level4Sizer,
                      col1_level5Sizer,col1_level6Sizer, col1_level7Sizer, 
                      col1_level8Sizer, col1_level9Sizer]
        
        for sizer in sizer_list:
            col1Sizer.Add(sizer, 0)
        
        level0Sizer.Add(col1Sizer, 0)
        level0Sizer.Add(col2Sizer, 0)
        
        MainSizer.Add(level0Sizer, 0, wx.ALL, 0)
        MainSizer.Add(level1Sizer, 0, wx.ALL, 3)
        self.SetSizer(MainSizer, 0)
        self.Layout()    
        wx.CallAfter(self.OnLoad, event='')


    def OnLoad(self, event):
        load_list = [('custadd_accttype_combobox','account_types'),
                     ('custadd_custcode_combobox','customer_codes')]
        
        for name,fieldName in load_list:
            returnd = LookupDB('organizations').General(fieldName)
            print(('#597 Returnd : ',returnd))
            if len(returnd) == 0:
                list_choices = returnd[0][0]
                wx.FindWindowByName(name).SetCtrl(list_choices, debug=True)
        
        
    def OnAddPhoneEntry(self):
        
        cbox = RH_Button(self, -1, 
                               name = "custadd_phone_btn", 
                               size = (120,-1),
                               formatcodes = "!")
        cbox.listd = ['CELL','PHONE','FAX','CONTACT','WORK','TENANT']
        
        self.ph_add_boxSizer.Add(cbox, 0, wx.ALL, 5)
        self.pcnt += 1
        named = f"custadd_phone_txtctrl{self.pcnt}"
        foneNum_txtctrl = RH_MTextCtrl(self, -1, '', 
                                          mask = '(###) ###-####', 
                                          validRegex = "^\(\d{3}\) \d{3}-\d{4}", 
                                          size=(120, -1), 
                                          name=named)

        self.ph_add_boxSizer.Add(foneNum_txtctrl, 0, wx.ALL, 5) 
        self.ph_boxSizer.Add(self.ph_add_boxSizer, 0, wx.ALL, 5)
        self.Layout()
        

    def AddAll(self, event):
        prefix = wx.FindWindowByName('custadd_prefix_btn').GetCtrl()
        fname = wx.FindWindowByName('custadd_fname_txtctrl').GetCtrl()
        lname = wx.FindWindowByName('custadd_lname_txtctrl').GetCtrl()
        suffix = wx.FindWindowByName('custadd_suffix_txtctrl').GetCtrl()
        
        if prefix is None or prefix == '':
            fullName = "{0} {1} {2}".format(fname,lname,suffix)
        else:
            fullName = "{0} {1} {2} {3}".format(prefix,fname,lname,suffix)
        
        wx.FindWindowByName('custName_txtctrl').SetCtrl(fullName)        
   
    def OnCustNumCheck(self, event):
        check_num = wx.FindWindowByName('custadd_custnum_txtctrl')
        check_numval = check_num.GetValue()
        check_btn = wx.FindWindowByName('custadd_custnumchk_button')
        print(("Check Num Name : ",check_numval))
        if check_numval:
            chk = AccountOps().AcctNumCheck('customer_basic_info','cust_num',check_numval)
            print(("Check : ",chk))
            if chk > 0:
                check_btn.SetBackgroundColour('Red') 
                check_num.SetValue('')       
            else:
                check_btn.SetBackgroundColour('Green')
    
    
    def OnCustNumAuto(self, event):
        check_numval = wx.FindWindowByName('custadd_custnum_txtctrl').GetCtrl()
        #check_numval = check_num.GetValue()
        check_btn = wx.FindWindowByName('custadd_custnumauto_button')
        check_btn.SetBackgroundColour('Green')
        chk = AccountOps().AcctNumAuto('customer_basic_info','cust_num',fill0s=10)
        print(("Check Auto : ",chk))
        wx.FindWindowByName('custadd_custnum_txtctrl').SetCtrl(chk)
        
    def OnCancelCustomerAdd(self, event):
        self.Destroy()    
            
    def OnSaveCustomerAdd(self, event):
        """ On Save Customer Add """
        debug = True
        custNum = wx.FindWindowByName('custadd_custnum_txtctrl').GetCtrl()
        check_btn = wx.FindWindowByName('custadd_custnumauto_button')
        colorCustButton = check_btn.GetBackgroundColour()
        print(("color Custom Button Color : ",colorCustButton))
        if custNum is None or custNum == '':
            save_btn = wx.FindWindowByName('custadd_save_button')
            save_btn.SetBackgroundColour('Red')
            
            pass
        else:
            custAdd_list=[('prefix','custadd_prefix_combobox'),
                          ('first_name','custadd_fname_txtctrl'),
                          ('middle_initial','custadd_midInitial_txtctrl'),
                          ('last_name','custadd_lname_txtctrl'),
                          ('suffix','custadd_suffix_txtctrl'),
                          ('address_acct_num','custadd_addr_acct_num_txtctrl'),
                          ('email_addr','custadd_email_txtctrl'),
                          ('tax_exempt_number','custadd_TaxExemptID_txtctrl'),
                          ('typecode','custadd_custcode_combobox'),
                          ('statement_terms','custadd_statement_terms_txtctrl'),
                          ('contact1','custadd_contact1_txtctrl'),
                          ('contact2','custadd_contact2_txtctrl'),
                          ('account_type','custadd_accttype_combobox'),
                          ('birthday','custadd_birthday_txtctrl'),
                          ('phone_numbers','custadd_phone_listctrl')]
                        
            table_list = ['customer_basic_info','customer_accts_receivable',
                          'customer_notes','customer_sales_options',
                          'customer_security','customer_shipto_info']
            
            QueryOps().CheckEntryExist('cust_num',custNum,table_list)
        
            for field,name in custAdd_list:
                value = wx.FindWindowByName(name).GetCtrl()
                # query = '''UPDATE customer_basic_info 
                #            SET {0}=? 
                #            WHERE cust_num=?'''.format(field)
                # data = (value,custNum,)
                # returnd = SQConnect(query, data).ONE()
                value = VarOps().CheckNone(value)
                returnd = LookupDB('customer_basic_info').UpdateSingle(field, value, 'cust_num', custNum)
                print(("ON NEW SAVE : ",returnd))
                          
            #createDate = datetime.date.today()
        
            RecordOps('customer_basic_info').UpdateRecordDate('date_added','cust_num',custNum) 
       
            self.itemPicked = custNum
            
            self.Destroy()
            
    def OnResetCustomerAdd(self, event):
        custAdd_list = [('prefix','custadd_prefix_combobox'),
                        ('first_name','custadd_fname_txtctrl'),
                        ('middle_initial','custadd_midInitial_txtctrl'),
                        ('last_name','custadd_lname_txtctrl'),
                        ('suffix','custadd_suffix_txtctrl'),
                        ('address_acct_num','custadd_addr_acct_num_txtctrl'),
                        ('email_addr','custadd_email_txtctrl'),
                        ('tax_exempt_number','custadd_TaxExemptID_txtctrl'),
                        ('typecode','custadd_custcode_combobox'),
                        ('statement_terms','custadd_statement_terms_txtctrl'),
                        ('contact1','custadd_contact1_txtctrl'),
                        ('contact2','custadd_contact2_txtctrl'),
                        ('account_type','custadd_accttype_combobox'),
                        ('birthday','custadd_birthday_txtctrl'),
                        ('phone_numbers','custadd_phone_listctrl')]
        
        for field, name in custAdd_list:
            ClearCtrl(name)
                
        
        
    def OnMainHouseSearch(self, event):
        print("************** Add Address Info ****************")
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
        title="Search-N-Add Address Form"
        AddAddrLookupD = AddAddressLookupDialog(self, title=title,  style=style)
        AddAddrLookupD.ShowModal()
        
        try:
            AddAddrLookupD.itemPicked
        except:
            AddAddrLookupD.Destroy()
            return
            
        self.addrPicked = AddAddrLookupD.itemPicked
        print(("Address Lookup D : ",self.addrPicked)) 
        AddAddrLookupD.Destroy()
        
        load_addr = [('addr_acct_num','custadd_addr_acct_num_txtctrl'),
                     ('address0','custadd_address1_txtctrl'),
                     ('address2','custadd_address2_txtctrl'),
                     ('address3','custadd_address3_txtctrl'),
                     ('city','custadd_city_txtctrl'),
                     ('state','custadd_state_txtctrl'),
                     ('zipcode','custadd_zipcode_txtctrl')]
        
        for field, name in load_addr:
            # query = """SELECT {0} 
            #            FROM address_accounts 
            #            WHERE addr_acct_num=?""".format(field)
            # data = (self.addrPicked,)
            # returnd = SQConnect(query, data).ONE()
            
            returnd = LookupDB('address_accounts').Specific(self.addrPicked, 'addr_acct_num', field)
            if returnd[0] != None:
                wx.FindWindowByName(name).SetCtrl(returnd[0])
                               
    
    def OnPhoneAdd(self, event):
        debug = False
        typed = wx.FindWindowByName('custadd_phone_combobox').GetCtrl()
        numberplain = wx.FindWindowByName('custadd_phone_txtctrl').GetCtrl()
        number = wx.FindWindowByName('custadd_phone_txtctrl').GetCtrl()
        
        lc = wx.FindWindowByName('custadd_phone_listctrl')
        lc.Add(typed, numberplain, number)
        
    def OnPhoneDel(self, event):
        lc = wx.FindWindowByName('custadd_phone_listctrl')
        lc.Remove()
        
    def Capitals(self, event):
        """ Capitalize First Letters """
        valued = event.GetEventObject()
        raw_value = valued.GetValue()
        named = valued.GetName()
        edit_txtctrl = wx.FindWindowByName(named)
        new_value = raw_value.title()
        edit_txtctrl.ChangeValue(new_value)
            

#-------------------------------------
#-------------------------------------
class AddAddressLookupDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        kw['size'] = (1000, 600)
        super(AddAddressLookupDialog, self).__init__(*args,**kw)
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        
        level0Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        box = wx.StaticBox(self, -1, label="Street Name Search")
        BoxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        
        ctrl = RH_TextCtrl(self, -1, 
                           name='addressLookup_search_txtctrl', 
                           size=(190, -1), 
                           style=wx.TE_PROCESS_ENTER)
        
        ctrl.SetToolTip(wx.ToolTip("Enter Street Name Only"))
        ctrl.Bind(wx.EVT_TEXT_ENTER, self.onAddrSearchButton)
        ctrl.SetFocus()
        BoxSizer.Add(ctrl, 0)
        
        srch_btn = RH_Button(self, -1, 
                        label = "Search", 
                        name = 'addressLookup_search_button')
        
        srch_btn.Bind(wx.EVT_BUTTON, self.onAddrSearchButton)
        add_btn = RH_Button(self, -1, 
                        label="        Add\nNew Address", 
                        name='addressLookup_addNew_button')
        
        add_btn.Bind(wx.EVT_BUTTON, self.onAddAddrButton)
        BoxSizer.Add(srch_btn, 0)
        
        level0Sizer.Add(BoxSizer, 0)
        level0Sizer.Add(add_btn, 0, wx.ALL|wx.EXPAND, 15)
        self.AddSizer = wx.BoxSizer(wx.VERTICAL)
        
        level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        addr0_txtctrl = RH_TextCtrl(self, -1, 
                                    name='addressAdd_address0_txtctrl', 
                                    size=(300,-1), 
                                    style=wx.TE_READONLY)
        
        level1_list = [('House #','addressAdd_houseNum_txtctrl',60,
                            "Enter Numbers Here Only"),
                       ('Direction','addressAdd_cardinalDirection_txtctrl',60,
                            "Please Enter 'N,S,E,W' Only"),
                       ('Street Name','addressAdd_streetName_txtctrl',190, 
                            "Enter the Name of Street Only")]
                       
        for labeld,named,width,tooltip in level1_list:
            box = wx.StaticBox(self, -1, label=labeld)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            if 'txtctrl' in named:
                ctrl = RH_TextCtrl(self, -1, 
                                   name = named,
                                   size = (width,-1), 
                                   style = wx.TE_PROCESS_ENTER)    
            
                if 'Number' in labeld:
                    ctrl.Bind(wx.EVT_KILL_FOCUS, self.OnNumbersOnly)
               
                else:
                    ctrl.Bind(wx.EVT_KILL_FOCUS, EventOps().Capitals)
            if 'combobox' in named:
                direction_list = ['','N','S','E','W','NW','NE','SW','SE']
                ctrl = RH_Button(self, -1, name = named, size = (width,-1))    
                ctrl.listd = direction_list
                ctrl.Bind(wx.EVT_KILL_FOCUS, EventOps().Capitals)            
            ctrl.SetToolTip(wx.ToolTip(tooltip))
            
            boxSizer.Add(ctrl,0)
            
            level1Sizer.Add(boxSizer, 0)
            
        choices_list = ['Av','Rd','St','Ct','Dr','Blvd','Cir','Aly','Anex',
                        'Bluff','Bend','Fwy','Pkwy','Ter','Trail','Way','Hgts']

        box = wx.StaticBox(self, -1, label='Suffix')
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        ctrl = RH_Button(self, -1, name = 'addressAdd_addrSuffix_combobox')
        ctrl.listd = choices_list
        ctrl.Bind(wx.EVT_KILL_FOCUS, EventOps().Capitals)
        boxSizer.Add(ctrl, 0)
        
        level1Sizer.Add(boxSizer, 0)
        box = wx.StaticBox(self, -1, label='Unit')
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        ctrl = RH_TextCtrl(self, -1, 
                           name = 'addressAdd_unit_txtctrl',
                           size = (60, -1),
                           style = wx.TE_PROCESS_ENTER)
        
        ctrl.SetToolTip(wx.ToolTip("Enter Unit Alpha or Numeric"))
        ctrl.Bind(wx.EVT_KILL_FOCUS, EventOps().Capitals)
        ctrl.Bind(wx.EVT_KILL_FOCUS, self.AddAddressTogether)
        boxSizer.Add(ctrl, 0)
        
        level1Sizer.Add(boxSizer, 0)
        
        level2_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        level2_Sizer.Add(addr0_txtctrl,0,wx.ALL, 3)
        
        level2aSizer = wx.BoxSizer(wx.HORIZONTAL)
        box = wx.StaticBox(self, -1, label='Address line 2')
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        ctrl = RH_TextCtrl(self, -1, 
                           name='addressAdd_address2_txtctrl',
                           size=(250,-1))
        
        ctrl.Bind(wx.EVT_KILL_FOCUS, EventOps().Capitals)
            
        boxSizer.Add(ctrl, 0)
        level2aSizer.Add(boxSizer, 0)
        
        level2bSizer = wx.BoxSizer(wx.HORIZONTAL)
        box = wx.StaticBox(self, -1, label='Address line 3')
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        ctrl = RH_TextCtrl(self, -1, 
                           name='addressAdd_address3_txtctrl',
                           size=(250,-1))

        ctrl.Bind(wx.EVT_KILL_FOCUS, EventOps().Capitals)
        boxSizer.Add(ctrl, 0)
        level2bSizer.Add(boxSizer, 0)
        
        level3Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        level3_list = [('City','addressAdd_city_txtctrl',120),
                       ('State','addressAdd_state_txtctrl',80),
                       ('Zipcode','addressAdd_zipcode_txtctrl',90)]
        
        for labeld,named,width in level3_list:
            box = wx.StaticBox(self, -1, label=labeld)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            if 'City' in labeld:
                ctrl = RH_TextCtrl(self, -1, 
                                   name = named, 
                                   size = (width,-1))
                ctrl.Bind(wx.EVT_KILL_FOCUS, EventOps().Capitals)
            elif 'State' in labeld:
                ctrl = RH_MTextCtrl(self, -1, 
                                       name = named, 
                                       size = (width,-1), 
                                       formatcodes = '!')
            elif 'Zipcode' in labeld:
                ctrl = RH_TextCtrl(self, -1, 
                                       name = named, 
                                       size = (width,-1))
                
                ctrl.Bind(wx.EVT_KILL_FOCUS, self.OnNumbersOnly)
            
            boxSizer.Add(ctrl, 0)
            level3Sizer.Add(boxSizer, 0)   
        
        level4Sizer = wx.BoxSizer(wx.HORIZONTAL)
        add_btn = RH_Button(self, -1, 
                            label = "Add Address", 
                            name = 'addressAdd_addAddress_button')
        
        add_btn.Bind(wx.EVT_BUTTON, self.onAddAddressButton)
        reset_btn = RH_Button(self, -1, 
                              label = "RESET FORM", 
                              name = 'addressAdd_resetForm_buttom')
        
        reset_btn.Bind(wx.EVT_BUTTON, self.onResetFormButton)
        level4Sizer.Add(add_btn, 1)
        level4Sizer.Add(reset_btn,1)
        
        self.AddSizer.Add(level1Sizer, 0)
        self.AddSizer.Add(level2_Sizer, 0)
        self.AddSizer.Add((15,15),0)
        self.AddSizer.Add(level2aSizer, 0)
        self.AddSizer.Add((15,15),0)
        self.AddSizer.Add(level2bSizer, 0)
        self.AddSizer.Add((15,15),0)
        self.AddSizer.Add(level3Sizer, 0)
        self.AddSizer.Add((15,15),0)
        self.AddSizer.Add(level4Sizer, 0, wx.ALL|wx.ALIGN_CENTER, 5) 
        
        self.ChoiceSizer = wx.BoxSizer(wx.VERTICAL)
       
        collabel_list = [('Account Number',110),('Address 1',240),
                         ('Address 2',240),('Unit',70),('City',120),
                         ('State',80),('Zipcode',60)]
        rowsnum = 25
        colsnum = len(collabel_list)        
        
        lc = wx.ListCtrl(self, 
                         name='customers_addrLookup_chooser_lc',
                         size=(970, 450),
                         style=wx.LC_REPORT|wx.BORDER_SUNKEN)
                        
        idx = 0
        for label, width in collabel_list:
            lc.InsertColumn(idx, label, width=width)
            idx += 1    
        
        
        lc.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnChooserCellLeftClick)
        
        
        self.ChoiceSizer.Add(lc, 0)
         
        
        
        workingSizer = wx.BoxSizer(wx.HORIZONTAL)
        txt = wx.StaticText(self, -1, label='', name='addAddress_loading_text')
        workingSizer.Add(txt,0,wx.ALL, 3)
        
        MainSizer.Add(level0Sizer, 0)
        MainSizer.Add((10,10),0)
        MainSizer.Add(workingSizer, 0)
        MainSizer.Add(wx.StaticLine(self, -1, size=(900,10),
                      style=wx.LI_HORIZONTAL),  0)
        MainSizer.Add((15,15),0)
        MainSizer.Add(self.AddSizer, 0)
        MainSizer.Add(self.ChoiceSizer, 0)
        
            
        self.SetSizer(MainSizer,0)
        self.Layout()    
        self.AddSizer.ShowItems(show=False)
        self.ChoiceSizer.ShowItems(show=False)
          


   
    def AddAddressTogether(self, event):
        obj = event.GetEventObject()
        named = obj.GetName()
        
        houseNum = wx.FindWindowByName('addressAdd_houseNum_txtctrl').GetCtrl()
        cardDir = wx.FindWindowByName('addressAdd_cardinalDirection_combobox').GetCtrl()
        streetName = wx.FindWindowByName('addressAdd_streetName_txtctrl').GetCtrl()
        suffix = wx.FindWindowByName('addressAdd_addrSuffix_combobox').GetCtrl()
        unit = wx.FindWindowByName('addressAdd_unit_txtctrl').GetCtrl()
        print(f'unit : {unit}')
        address0 = TextOps().AllinaRow(houseNum,cardDir,streetName,suffix,unit)
        
        wx.FindWindowByName('addressAdd_address0_txtctrl').SetCtrl(address0) #new_addr0
        
                 
    def OnChooserCellLeftClick(self, evt):
        debug = False
        item_id,objText = EventOps().LCGetSelected(evt)
        self.itemPicked = objText
        self.Close()
        
        
        
        
    def onAddrSearchButton(self, event):

        print("*************** Create Modal Window for Individual Choosing...")
        
        self.addr_search = wx.FindWindowByName('addressLookup_search_txtctrl').GetCtrl()
        print(("Search Term : ",self.addr_search))
        if self.addr_search:
            cnt = self.addr_search.count(' ')
            if cnt > 0:
                revised_search = re.sub(' ','.*',self.addr_search)
            else:
                revised_search = self.addr_search
            
            startTime = datetime.datetime.now()
            query = """SELECT addr_acct_num,address0,address2,address3,
                              city,state,zipcode,unit from address_accounts 
                              where address0 like ? OR zipcode = ?"""
            
            data = (revised_search, revised_search)
            VarOps().GetTyped(query)
            VarOps().GetTyped(data)
            returnd = SQConnect(query, data).ALL()
            MiscOps().timeStages('After DB Run',startTime)
            #print "Returnd : ",returnd
            
            #splash = Splash()
            #splash.Run()
            lcname = 'customers_addrLookup_chooser_lc'
            lc = wx.FindWindowByName(lcname)
                    
            if not returnd:
                wx.MessageBox('Address Not Found','Address Info', wx.OK)
                
            else:      
                self.AddSizer.ShowItems(show=False)
                txt = wx.FindWindowByName('addAddress_loading_text')
                txt.SetLabel('Found {} Records'.format(len(returnd)))
                self.ChoiceSizer.ShowItems(show=True)
                self.Layout()
                
                
                           
                wx.FindWindowByName(lcname).ClearCtrl()
               
                records_returnd = len(returnd)
                module_name = 'Customers'
                bgcolor = Themes(module_name).GetColor('bg')
                whitetext = Themes(module_name).GetColor('text')
                cell_color = Themes(module_name).GetColor('cell')
                MiscOps().timeStages('Just Before Grid Fill',startTime)
                if records_returnd != 1:
                    plural = 'es'
                else:
                    plural = ''
                found = 'Found {0} Address{1}'.format(records_returnd,plural)
                wx.FindWindowByName('addAddress_loading_text').SetCtrl(found)
                
                    
                for row in range(records_returnd):
                    (addr_acct_numd, address1d, address2d, 
                     address3d, cityd, stated, 
                     zipcoded,unitd) = returnd[row]
                        
                    setList = [(0,addr_acct_numd),
                               (1,address1d),
                               (2,address2d),
                               (3, unitd),
                               (4,cityd),
                               (5,stated),
                               (6,zipcoded)]
                                   
                    ListCtrl_Ops(lcname).LCFill(setList,row)
                     # time.sleep(1)
            lc = wx.FindWindowByName('customers_addrLookup_chooser_lc').SetFocus()
            #splash.Destroy()
            #HU.GridAlternateColor(grid.GetName(),'')
                        
            MiscOps().timeStages('After Grid Fill',startTime)    
        else:
            wx.MessageBox('Address Not Found','Address Info', wx.OK)
            self.AddSizer.ShowItems(show=True)
            self.ChoiceSizer.ShowItems(show=False)
            self.Layout()      
            
    
    def onAddAddrButton(self, event):
        self.AddSizer.ShowItems(show=True)
        self.ChoiceSizer.ShowItems(show=False)
        houseNum = wx.FindWindowByName('addressAdd_houseNum_txtctrl').SetFocus()
        self.Layout()        
        
    def OnCardinalDirections(self, event):
        valued = event.GetEventObject()
        raw_value = valued.GetValue().strip()
        named = valued.GetName()
        edit_txtctrl = wx.FindWindowByName(named)
        # numeric check
        if all(x in 'NSEWnsewnorthsoutheastwest' for x in raw_value):
            self.value = raw_value.title()
            edit_txtctrl.ChangeValue(str(self.value))
        else:
            edit_txtctrl.ChangeValue("")
            edit_txtctrl.SetToolTip(wx.ToolTip("NUMBERS ONLY!!!"))       
    
    def CapitalAll(self, event):   
        valued = event.GetEventObject()
        raw_value = valued.GetValue()
        named = valued.GetName()
        edit_txtctrl = wx.FindWindowByName(named)
        new_value = raw_value.upper()
        edit_txtctrl.ChangeValue(new_value)
    
    def OnNumbersOnly(self, event):
        """
        check for numeric entry accepted result is in self.value
        """
        print("Check for Numbers Only ")
        valued = event.GetEventObject()
        raw_value = valued.GetValue().strip()
        named = valued.GetName()
        edit_txtctrl = wx.FindWindowByName(named)
        # numeric check
        if all(x in '0123456789.+-/' for x in raw_value):
            self.value = raw_value
            edit_txtctrl.ChangeValue(str(self.value))
        else:
            edit_txtctrl.ChangeValue("")
            edit_txtctrl.SetToolTip(wx.ToolTip("NUMBERS ONLY!!!"))       
    
    
    def onAddAddressButton(self, event):
        transaction_zeroes = 9
        debug = True
        countreturn = QueryOps().QueryCheck('address_accounts')
        
        if countreturn == 0:
            countd = 1
        else:
            countd = countreturn+1
        account_num = "A" + str(countd).zfill(transaction_zeroes)
        print(("Account Number : ",account_num))
        table_list = ['address_accounts']
        
        QueryOps().CheckEntryExist('addr_acct_num',account_num,table_list)
        
        savList = [('addressAdd_streetName_txtctrl','street_name'),
                   ('addressAdd_cardinalDirection_combobox','street_direction'),
                   ('addressAdd_houseNum_txtctrl','street_num'),
                   ('addressAdd_addrSuffix_combobox','street_type'),
                   ('addressAdd_address2_txtctrl','address2'),
                   ('addressAdd_address3_txtctrl','address3'),
                   ('addressAdd_city_txtctrl','city'),
                   ('addressAdd_state_txtctrl','state'),
                   ('addressAdd_zipcode_txtctrl','zipcode'),
                   ('addressAdd_address0_txtctrl','address0'),
                   ('addressAdd_unit_txtctrl','unit')]
        
        for name, field in savList:
            value = wx.FindWindowByName(name).GetCtrl()
            query = '''UPDATE address_accounts 
                       SET {0}=(?) 
                       WHERE addr_acct_num=(?)'''.format(field)
            data = (value,account_num,)
            call_db = SQConnect(query, data).ONE()
            
                            
    def onResetFormButton(self, event):
        check_list = ['addressAdd_streetName_txtctrl',
                      'address_cardinalDirection_combobox',
                      'addressAdd_houseNum_txtctrl',
                      'addressAdd_addrSuffix_combobox',
                      'addressAdd_unit_txtctrl',
                      'addressAdd_address2_txtctrl',
                      'addressAdd_address3_txtctrl',
                      'addressAdd_city_txtctrl',
                      'addressAdd_state_txtctrl',
                      'addressAdd_zipcode_txtctrl',
                      'addressAdd_address0_txtctrl']
        for name in check_list:
            wx.FindWindowByName(name).ClearCtrl()        
        
        
        
        pass              


        
     