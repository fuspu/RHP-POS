#-*- coding: utf-8 -*-
#import wxversion
#wxversion.select('2.8')

import wx
import os
import re
import json
import sys
import string
import sqlite3
import datetime
#import psycopg2
import wx.grid as gridlib
import wx.lib.masked as masked
import Printer as PRx
import HandyUtilities as HU
import Common_Dialogs as CDialog
from decimal import Decimal, ROUND_HALF_UP, ROUND_UP, ROUND_05UP





class FillIn(object):
    def __init__(self,gridname,debug=True):
        self.grid = wx.FindWindowByName(gridname)
        HU.BeVerbose('Fill In ...')
    
    
    def POSCustAcctGrid(self,custNum=None,debug=True):
        HU.BeVerbose('... POS Cust Acct Grid')
        grid = self.grid
        acctInfo = HU.SetAcctInfo(grid.GetName())
        if custNum is None:
            set_list = [('Account Number','PLACEHOLDER')]
            #grid.SetCellValue(0,0,'PLACEHOLDER')
            HU.FillGrid(grid.GetName(),set_list, col=0)
                
            return
                    
        fields = '''cust_num, first_name, last_name,
                    address_acct_num, phone_numbers'''
        returnd = HU.LookupDB('customer_basic_info').Mode2(custNum,'cust_num',fields)
                                            
        HU.Debugger(returnd,True)
        (cust_numd,first_named, last_named, address_acct_numd,phoned_JSON) = returnd
                
        fields = '''street_num, street_direction, street_name,
                    street_type,unit,city,zipcode,state,address2'''
        returnd = HU.LookupDB('address_accounts').Mode2(address_acct_numd,'addr_acct_num',fields)
        HU.Debugger('Returnd : {} = {}'.format(returnd, len(returnd)),debug)
                
        (street_numd,street_directiond,street_named,street_typed, unitd,cityd,zipcoded,stated,addressed2) = returnd
        
        print('flname : {} {}'.format(first_named, last_named))
        
        acctInfo.custAcctNum(cust_numd)
        
        acctInfo.name(first_named, last_named)
        #flname = '{0} {1}'.format(first_named, last_named)

        addressed = HU.AllinaRow(street_numd,street_directiond,street_named,street_typed,unit=unitd)
        acctInfo.address(addressed)
        acctInfo.cistzi(cityd, stated, zipcoded)
        
        fields = 'fixed_discount, discount_amt'
        returnd = HU.LookupDB('customer_sales_options').Mode2(custNum,'cust_num',fields)
        
        fixed_discountd, discount_amtd = '0', None
        
        (fixed_discountd, discount_amtd) = returnd
        
        print('fixed _discoutn : {} {}'.format(fixed_discountd, discount_amtd))
        acctInfo.discountd(fixed_discountd, discount_amtd)        
        
        grid = wx.FindWindowByName('pos_acct_grid')

        rows = grid.GetNumberRows()
        cols = grid.GetNumberCols()

        phoned = json.loads(phoned_JSON)
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
            grid.SetCellEditor(6,0,HU.GridCellComboBox(phone_list))


    def POSAddrAcctGrid(self, custNum, addrAcctNum=None, debug=True):
        HU.BeVerbose('... POS Addr Acct Grid')
        grid = self.grid
        print('Customer Num : ',custNum)
        if custNum == '' or custNum is None:
            return
            
        fields = '''cust_num,first_name,last_name,cust_num,
                    address_acct_num,phone_numbers,rental_of'''
        returnd = HU.LookupDB('customer_basic_info').Mode2(custNum, 'cust_num',fields)
                
        HU.Debugger(returnd,True)
        (cust_numd,first_named, last_named, cust_numd,
         address_acct_numd,phoned_JSON,rental_JSON) = returnd

        if addrAcctNum is not None:
            address_acct_numd = addrAcctNum
        fields = '''street_num, street_direction, street_name,
                    street_type, unit, city, zipcode, state,
                    address2'''
        returnd = HU.LookupDB('address_accounts').Mode2(address_acct_numd,'addr_acct_num',fields)
                
        (street_numd,street_directiond,street_named,street_typed,unitd,
         cityd,zipcoded,stated,addressed2) = returnd
        
        rental_dict = {}
        if rental_JSON is not None and len(rental_JSON) > 0 and addrAcctNum is None:
            rental_list = json.loads(rental_JSON)
            dict_cnt = len(rental_dict)
            print('dict_cnt : ',dict_cnt)
            print('address_acct_numd : ',address_acct_numd)
            print('rental_dict : ',rental_dict)
            rental_list.append(address_acct_numd)

            addr_choice = []
            for addr_num in rental_list:
                fields = 'address0,city,state,unit'
                returnd = HU.LookupDB('address_accounts').Mode2(addr_num,'addr_acct_num',fields)
                        
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
                
            print("addr _ Choice : {}".format(addr_choice))
                
            regex = re.compile(self.addrPicked)
            idxs = [i for i, item in enumerate(addr_choice) if re.search(regex, item)]
            print('IDXS : ',idxs[0])
            #choiceKey = addr_choice.index(self.addrPicked)
            print('addr_choice[idxs[0]] : ',addr_choice[idxs[0]])
                
            grid.SetCellValue(1,0,addr_choice[idxs[0]])

        else:
            address0d = HU.AllinaRow(street_numd, street_directiond,street_named, street_typed, unitd)
            main_addr = '{}\t{}, {}, {}'.format(addrAcctNum,address0d,cityd,stated)

            grid.SetCellValue(1,0,main_addr)
        print("Address Account")

        rowname = 'Address Account'
                
        if rowname == 'Address Account':
            if rowname:
                print("ON CLICK ADDRESS ACCOUNT CHANGE")

                newAccount = grid.GetCellValue(1,0)
                print("New Account : ",newAccount)
                p = re.search('A[0-9]+',newAccount)
                if p is None:
                    return

                addr_num = p.group(0)
                
                fields = 'address0,city,state,zipcode,unit'
                returnd = HU.LookupDB('address_accounts').Mode2(addr_num,'addr_acct_num',fields)
                print('address change : {}'.format(returnd))
                (address0d, cityd,statd,zipd,unitd) = returnd
                acctInfo = HU.SetAcctInfo(grid.GetName())
                cszd = '{}, {}  {}'.format(cityd,statd,zipd)
                set_list = [('Address 1',address0d),('City, State, Zip',cszd)]
                acctInfo.address(address0d)
                acctInfo.cistzi(cityd,statd,zipd)
                #grid.SetCellValue(3,0,address0d)
                #grid.SetCellValue(5,0,cszd)

                readonly_list = ['Name','Address 1','Address 2',
                                 'City, State, Zip','A/R/Avail Credit',
                                 'Discount %','Ship To']
                
                HU.GridListReadOnly(grid.GetName(),readonly_list)

            print("DONE & DONE")
            HU.GridFocusNGo('pos_transactions_grid',0)

    
    def POSTransGrid(self, gridname, transId):
        grid = wx.FindWindowByName(gridname)
        query = 'SELECT upc,description,quantity,unit_price,discount,total_price,tax1,tax2,tax3,tax4,tax_never FROM transactions WHERE transaction_id = ?'
        data = (transId,)
        returnd = HU.SQConnect(query,data).ALL()
        print('Returnd : ',returnd)
        idx = 0
        for upc, desc, qty, uprice, disc, totprice,tax1,tax2,tax3,tax4,tax5 in returnd:
            taxd = [tax1, tax2, tax3, tax4, tax5]
            isTaxed = 'Tx'
            for tax in taxd:
                if tax == 1:
                    isTaxed = 'nTx'
                    break
            setList = [('Item Number',upc),('Description',desc),('Price',HU.RoundIt(uprice, '1.00')),
                       ('Quantity',HU.RoundIt(qty,'1.00')),('Total',HU.RoundIt(totprice, '1.00')),('Disc',disc),
                       ('Tx',isTaxed)]
                    
            HU.FillGrid(gridname, setList, row=idx)
            idx += 1            
        
        
        
        
        
                          