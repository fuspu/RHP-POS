#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#
#
# Printer Cutter
#
import re,wx
import datetime
import json
import pout
from db_related import SQConnect
from decimal import Decimal
from escpos.printer import Usb

import binascii

class MiscReceiptPrinted(object):
    def __init__(self, debug=False):
        self.p = Usb(0x0409,0x005a) #printerAddr
         
    def CashDrawerSummary(self):
        pass

    def CashDrawerOpen(self):
        print('CashDrawerOpen')
        self.p.qr("RHP-POS is pretty basic")
        self.p.cut()        
    
        
            
        
class TransactionReceiptPrinted(object):
    def __init__(self,transactionNum,transType='Sales',stationNum='1',drawerNum='1',debug=False,dated=None, timed=None, reprint=False):
        self.transNum = transactionNum
        self.transType = transType
        self.debug = debug
        self.dated = dated
        self.reprint = reprint
        
        if re.search(":", str(self.dated)):
            self.dated = None
        self.timed = timed
        
        self.divider = '-'*40
        query = 'SELECT printer_address FROM Maintenance'
        data = ''
        a = 0x04b8
        b = 0x0202
        
        self.p = Usb(a, b)
        
        
    def Header(self,custNum=None, addrNum=None):
        """ Prints Receipt Header """
        query = '''SELECT name, address1, address2, city, state, zip, phone1, 
                          phone2,website,logo 
                   FROM basic_store_info'''
        data = ''
        returnd = SQConnect(query, data).ONE()
        
        (self.storeName, addr1, addr2, city,state,zipd,
         phone1,phone2, website, logo) = returnd
        
        if self.dated is None:                 
            datetimed = datetime.datetime.now().strftime('%m/%d/%Y %I:%M %p')
        else:
            pout.v('TransNum : {}\nself.dated : {}\nself.Timed : {}'.format(self.transNum, self.dated, self.timed),self.debug)
            todate = '{}/{}/{}'.format(self.dated.month,self.dated.day,self.dated.year)#('%m/%d/%Y')
            totime = self.timed.strftime('%I:%M %p')
            datetimed = '{} {}'.format(todate,totime)
              
        ph1,ph2 = '',''
        
        if phone1 is not None and len(phone1) > 0:
            ph1 = '{}-{}-{}'.format(phone1[:3],phone1[3:6],phone1[6:10])
        if phone2 is not None and len(phone2) > 0:
            ph2 = '{}-{}-{}'.format(phone2[:3],phone2[3:6],phone2[6:10])
        reprint = ''
        if self.reprint is True:
            reprint = 'Reprint'
        transactionHeader = '\n{2} {1} {0} {3}'.format(datetimed,self.transNum,self.transType,reprint)
        address = ''
        csz = '{}, {}  {}'.format(city, state, zipd)
        parts = [self.storeName, addr1, addr2, csz, ph1, ph2, website]
        header = ''
        print('parts : ',parts)
        for smth in parts:
            print('smth : ',smth)
            if smth is not None and len(smth) > 1:
                header += '\n {}'.format(smth)
                    
        
        
        self.p.set('CENTER')
        try:
            self.p.image(logo)
        except:
            pass
        self.p.text(header.ljust(40))
        self.p.text('\n')
        #-------- Address Check & Set    
        print('Address Check  : ',addrNum)
        if addrNum is not None:
            query = 'SELECT address0,address2,address3,city,state,zipcode FROM address_accounts WHERE addr_acct_num=(?)'
            data = (addrNum,)
            returnd = SQConnect(query, data).ONE()
            
            (addr0,addr2,addr3,cityd,stated,zipd) = returnd
            
            csz = '{}, {}  {}'.format(cityd, stated, zipd)
        else:
            csz = addr0 = addr2 = addr3 = ''
            
            
        #--------- Cust Num Check & Set  
        print('CustNum Check : "{}"=={}'.format(custNum, len(custNum)))
        if custNum is not None and len(custNum) > 0:
            query = 'SELECT full_name FROM customer_basic_info WHERE cust_num=(?)'
            data = (custNum,)
            returnd = SQConnect(query,data).ONE()
            
            addrList = [returnd[0], addr0, addr2, addr3, csz]
            addrLine = ''
            for item in addrList:
                if item is not None and len(item) > 1:
                    addrLine += '\n {}'.format(item)
                            
            
            self.p.set('LEFT')
            self.p.text(addrLine.ljust(40))
            self.p.text('\n')
            
        storeHeaderB = [transactionHeader,self.divider]
        
        for piece in storeHeaderB:
            self.p.set('LEFT')
            piece += '\n'
            self.p.charcode("MULTILINGUAL")
            self.p.text(piece)
        
            
        query = """SELECT note 
                   FROM transaction_notes 
                   WHERE transaction_id=(?) AND line_position='BEGIN'"""
        
        data = ('CURRENT',)
        if self.reprint is True:
            data = (self.transNum,)
        
        returnd = SQConnect(query,data).ALL()
        print('Note Returnd : ',returnd)
        if returnd is not None:
            for note in returnd:
                note = HU.DeTupler(note)
                self.p.set('LEFT',font='b')
                self.p.text(note+'\n')
                       
        self.p.set('LEFT',font='a')
    
    def TransactionLine(self,lineNum,itemNum,qty,description,price):
        ''' Transaction Lines are Formatted & Printed Here '''
        col1 = str(qty).ljust(7)
        col3 = str(price).rjust(7)
        col1space = str(' ').ljust(7)
        descLen = len(str(description))
        if descLen > 52 and descLen < 75:
            chk = str(description)[:26]
            idx = chk.rfind(' ')
            firstline = str(description)[:idx].ljust(26)
            desc2 = str(description)[26:]
            chk2 = desc2[:26]
            idx2 = chk2.rfind(' ')
            secondline = desc2[:idx2].ljust(26)
            thirdline = desc2[idx2:].ljust(26)
                   
            
            transLine = '{}{}\n{}{}\n{}{}{}\n'.format(col1,firstline,col1space,secondline,col1space,thirdline,col3)
            
        elif descLen > 26 and descLen <= 52:
            chk = description[:26]
            idx = chk.rfind(' ')
            firstline = str(description)[:idx].ljust(26)
            secondline = str(description)[idx:].ljust(26)
            transLine = '{}{}\n{}{}{}\n'.format(col1, firstline, col1space,secondline, col3)
            
        else:
            col2 = str(description)[:26].ljust(26)
            transLine = '{}{}{}\n'.format(col1,col2,col3)
        
        print(transLine)
        self.p.set('LEFT')
        self.p.text(transLine)
        #----- Item Info
        p_o_list = ['info','warranty','return']
        for typd in p_o_list:
            query = """SELECT {}, {}
                       FROM item_cust_instructions WHERE upc=(?)""".format('print_'+typd+'_options',typd+'_box')
                       
            data = (itemNum,)
            returnd = SQConnect(query,data).ALL()
            print('info returnd : ',returnd[0][0])
            try:
                (print_options, info_box) = returnd
                toPrint = 'yes'
            except:
                toPrint = 'no'
            
            if toPrint == 'yes':
                print('info_box : ',info_box)
                
                print('key : {}'.format(info_box))
                self.p.set('LEFT',font='b')
                for xi in [info_box, print_options]:
                    textd = str(xi)
                    print('l textd  : ',len(textd))
                    if len(textd) > 0:
                        keytext = '{} : \n'.format(key)
                        self.p.text(keytext)
                        self.p.text(textd+'\n')
            

        #----- Notes        
        query = """SELECT note 
                   FROM transaction_notes 
                   WHERE transaction_id=(?) AND line_position=(?)"""
        linePos = 'A{}'.format(lineNum)           
        data = ('CURRENT',linePos,)
        
        if self.reprint is True:
            data = (self.transNum, linePos,)
        
        returnd = SQConnect(query,data).ALL()
        
        if returnd is not None:
            for note in returnd:
                note = HU.DeTupler(note)
                self.p.set('LEFT',font='b')
                self.p.text(note+'\n')
        
        self.p.set('LEFT',font='a')
    def InfoLine(self,info):
        col1 = ' '.ljust(7)
        col2 = str(info).ljust(33)
        
        transLine = '{}{}{}\n'.format(col1, col2)
        self.p.set('LEFT', font='a')
        self.p.text(transLine)
        
    
    def SubTotal(self, itemQty, subtotal, taxes, total):
        #----- End Notes        
        query = """SELECT note 
                   FROM transaction_notes 
                   WHERE transaction_id=(?) AND line_position=(?)"""
        data = ('CURRENT','END',)
        if self.reprint is True:
            data = (self.transNum, 'END',)
            
        returnd = SQConnect(query,data).ALL()
        
        if returnd is not None:
            for note in returnd:
                note = HU.DeTupler(note)
                self.p.set('LEFT',font='b')
                self.p.text(note+'\n')
        
        self.p.set('LEFT',font='a')
        #------ End Notes END
        
        self.p.text(self.divider+'\n')
        if Decimal(itemQty) == 1:
            qty = '{0} Item'.format(itemQty)
        else:
            qty = '{0} Items'.format(itemQty)
            
        col1 = str(qty).ljust(9)
        sbt = len(str(subtotal))
        
        rj3 = 9
        rj2 = 20
        if sbt >= 4:
            rj3 = 11
            rj2 = 20
            
        if sbt >= 6:
            rj3 = 11
            rj2 = 17
        
        if sbt >= 8:
            rj3 = 5
            rj2 = 11
                    
        col2 = 'Sub Total'.rjust(rj2)
            
        print('sbt : {} => {}'.format(sbt, rj3))
        col3 = str(subtotal).rjust(rj3)
        lineSubtotal = '{}{}{}\n'.format(col1,col2,col3)
        
        self.p.set('LEFT')
        self.p.text(lineSubtotal)
        
        col1 = ' '.ljust(9)
        if Decimal(taxes) > 0:
            col2 = 'Tax'.rjust(20)
            col3 = str(HU.RoundIt(taxes,'1.00')).rjust(11)
            lineTax = '{}{}{}\n'.format(col1,col2,col3)
            self.p.set('LEFT')
            self.p.text(lineTax)
        
        col2 = 'Total'.rjust(20)
        col3 = str(HU.RoundIt(total, '1.00')).rjust(11)
        lineTotal = '{}{}{}\n'.format(col1,col2,col3)
        self.p.set('LEFT')
        self.p.text(lineTotal)
        
        self.p.text(self.divider+'\n')
   
    def Change(self, paid_amt,payment_type,change_returnd=None):
        HU.Debugger('payment_type : {}'.format(payment_type),True)
        if len(payment_type) > 0:
            for key, value in payment_type.items():
                print('Payment Type : ',key.title())
                paymentType = key.title()
                print('Payment Value : ',value)
                typd = str(type(value))
                if 'float' in typd:
                    paymentValue = HU.RoundIt(value, '1.00')
                if re.search('(tuple|list)',typd):    
                    if len(value) > 1:
                        paymentValue = HU.RoundIt(value[0], '1.00')
                    else:
                        paymentValue = HU.RoundIt(value, '1.00')
                if re.search('(str|unicode)', typd):
                    paymentValue = HU.RoundIt(value, '1.00')                    
                if value == 0:
                    continue
                if re.match('charge',paymentType, re.I):
                    col1 = ' '.rjust(7)
                else:
                    col1 = 'Paid'.rjust(18)
                col2 = paymentType[:10].rjust(10)
                col3 = str(paymentValue).rjust(12)
                if 'Cash' in paymentType:
                    col3 = str(paid_amt).rjust(12)
                
                    
                if not 'Change' in paymentType:
                    linePaid = '{}{}{}\n'.format(col1,col2,col3)
                    self.p.set('LEFT')
                    self.p.text(linePaid)
                
        
        if len(change_returnd) > 0 and not change_returnd == None:
            col1 = ''.rjust(18)
            col2 = 'Change'.rjust(10)
            print('change_back : {} : L{}'.format(change_returnd, len(change_returnd)))
            col3 = str(HU.RoundIt(change_returnd,'1.00')).rjust(12)
            lineChange = '{}{}{}\n'.format(col1,col2,col3)
            
            self.p.set('LEFT')
            self.p.text(lineChange)
            
    
    def PayInfo(self, payment_type):
        InfoLine=[]
        if 'Check' in paymentType:
            InfoLine.append('Chk#{}'.format(value[1]))
        if re.search('(Credit|Debit)',paymentType):
            InfoLine.append('{} #{}\n{}\n'.format(value[1],value[2],value[0]))
        
        return InfoLine    
   
    def FinishPrint(self):          
        
        query = 'SELECT return_policy, conditions, thanks FROM pos_messages'
        data = ''
        returnd = SQConnect(query, data).ONE()
        print('Returnd : ',returnd)
        try:
            (returnPolicy, conditions, ThanksLine) = returnd
        except:
            returnPolicy, conditions, ThanksLine = 'a','a','a'
        #returnPolicy = '\n\nReturn Policy\nRefund & Exchange Policy\nRequirements:\n   1. Receipt\n   2. Original Package in GOOD condition\n   3. All Parts Included'
        
        #conditions = '\n\n*** REFUNDS ARE SUBJECT TO 10% RESTOCKING FEE ***\n*** NO RETURNS ON SPECIAL ORDERS ***\n'
                          
        #ThanksLine = "\n\nThanks for Shopping at {} \nWe Appreciate Your Business!\n".format(self.storeName)
        
        self.p.set('LEFT',font='b')
        self.p.text(returnPolicy+'\n')
        self.p.set('CENTER',text_type='B', font='b')
        self.p.text(conditions+'\n')
        self.p.set('CENTER',text_type='A', font='a')
        self.p.text(ThanksLine+'\n')
        self.p.cut()
