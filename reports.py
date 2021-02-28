#!/usr/bin/env python2
#
#
#
#
#import wxversion
#wxversion.select('2.8')


import wx,re,os 
#print('wx : {}'.format(wx.version()))

import subprocess
#import wx.calendar as cal
import wx.grid as gridlib
import sys
import faulthandler
#import sqlite3
import json
import xml.etree.cElementTree as ET
import datetime
from wx.lib.masked import TimeCtrl
import wx.lib.masked as masked
from decimal import Decimal, ROUND_HALF_UP
import wx.lib.inspection
import handy_utils as HUD
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, TA_CENTER
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_LEFT
from reportlab.lib.units import inch, mm
from reportlab.platypus import Paragraph, Table, SimpleDocTemplate, Spacer, PageBreak
from db_related import SQConnect
from button_stuff import ButtonOps

class CloseTheStore(object):
    def __init__(self, debug=False):
        self.pagesize = 'landscape'
        self.pathto = '../Docs/Closings'
        self.title = 'Closing'
        


class Reports(object):
    def __init__(self, which, debug=False):
        self.which = which        
        self.pagesize = 'letter'
        self.pathto = '../Docs/Reports'
        self.title = 'Report'
        
                    
class Statements(object):
    def __init__(self, which, debug=False):
        self.which = which
        self.pagesize = 'letter'
        self.pathto = '../Docs/Statements'
        self.title = 'Statement'
        
        
                            
                            
 
class CreatePDF(object):
    def __init__(self, section=None, debug=False):
        

        pdf_list = [('dailyClose', '../Docs/Closings','DayClose','landscape'),
                    ('salesTax','../Docs/Reports','SalesTax_Report','letter'),
                    ('statements','../Docs/Statements','Customer_Statements','letter')]

        self.header = section
        for serch, path, label, orient in pdf_list:
            
            
            if serch in section:    
                a = re.search(serch, section, re.I)
                
            if re.search(serch, section, re.I):
                
             
                self.serch = serch
                self.pdf_loc = path
                self.title = label
                self.orientation = orient
                break
                
        self.dated = datetime.datetime.now().date().strftime('%Y-%m-%d')
        self.pdf_file = '{}/{}_{}.pdf'.format(self.pdf_loc,self.title,self.dated)
        self.width, self.height = letter
        self.styles = getSampleStyleSheet()
        
        
    
    def coord(self, x, y, unit=1):
        """
        http://stackoverflow.com/questions/4726011/wrap-text-in-a-table-reportlab
        Helper class to help position flowables in Canvas objects
        """
        x, y = x * unit, self.height -  y * unit
        return x, y
    
    def Open(self):
        subprocess.call(["xdg-open", self.pdf_file])
        #subprocess.Popen([self.pdf_file])   

    def DailyClose(self):
        ''' Daily Close Section '''
        
        self.header = 'DayClose'
        self.line_two = 'Transaction Report'
        
        check_list = ['closing_daily_allTransactions_checkbox']
        status = False
        for name in check_list:
            
            cb = wx.FindWindowByName(name).GetValue()
            if cb == 1:
                if 'allTrans' in name:
                    status = self.AllTransactions(section='daily')
                
                    
    
        if status is False:
            wx.MessageBox('No Sales Today','Info',wx.OK)
            return
 
    def MonthlyClose(self):
        ''' Monthly Close Section '''
        
        self.header = 'MonthClose'
        self.line_two = 'Transaction Report'
    
        check_list = ['closing_daily_allTransactions_checkbox','closing_daily_cashDrawer_checkbox']
        for name in check_list:
            cb = wx.FindWindowByName(name)
            if cb == 1:
                if 'allTrans' in name:
                    self.AllTransactions(section='monthly')
                if 'cashDrawer' in name:
                    self.CashDrawerSummary(section='monthly')

        if status is False:
           wx.MessageBox('No Sales This Month','Info',wx.OK)
           return
        
    def SalesTax(self):
         ''' sales Tax Section '''
         
         status = self.GetSalesTx()
         self.header = 'Sales Tax Report'
         self.line_two = 'Sales Tax'
        
                   
    def run(self):
        pageSized = (self.height, self.width)
        if self.orientation == 'letter':
            pageSized = (self.width, self.height)
        
        self.doc = SimpleDocTemplate(self.pdf_file, pagesize=pageSized,rightMargin=36,leftMargin=36,
                            topMargin=36,bottomMargin=18)
        #Spacer(1,1*inch)
        self.story = []
        
        today = datetime.datetime.now().date().strftime('%Y-%m-%d')
        
        if 'dailyClose' in self.serch:
            self.dailyClose()
#             print 'Daily Close Active'
#             self.header = 'DayClose'
#             self.line_two = 'Transaction Report'
#             
#             check_list = ['closing_daily_allTransactions_checkbox']
#             status = False
#             for name in check_list:
#                 print 'cb  : ',name
#                 cb = wx.FindWindowByName(name).GetValue()
#                 if cb == 1:
#                     if 'allTrans' in name:
#                         status = self.AllTransactions(section='daily')
#                     
#                     print 'status : ',status    
#         
#             if status is False:
#                 wx.MessageBox('No Sales Today','Info',wx.OK)
#                 return
#  
        if 'monthlyClose' in self.serch:
            self.monthlyClose()
#             print 'Monthly Close Active'
#             self.header = 'MonthClose'
#             self.line_two = 'Transaction Report'
#             
#             check_list = ['closing_daily_allTransactions_checkbox','closing_daily_cashDrawer_checkbox']
#             for name in check_list:
#                 cb = wx.FindWindowByName(name)
#                 if cb == 1:
#                     if 'allTrans' in name:
#                         self.AllTransactions(section='monthly')
#                     if 'cashDrawer' in name:
#                         self.CashDrawerSummary(section='monthly')
#         
#             if status is False:
#                wx.MessageBox('No Sales This Month','Info',wx.OK)
#                return
#             
            
        if 'salesTax' in self.serch:
            self.SalesTax()
#             print 'sales Tax Active'
#             status = self.SalesTax()
#             self.header = 'Sales Tax Report'
#             self.line_two = 'Sales Tax'
#     
        
        HUD.VarOps().GetTyped(self.story)
        
        self.BuildDoc()    
        self.Open()
        
    def BuildDoc(self):    
        self.doc.build(self.story) #, onFirstPage=self.coverPage)
        
    def StoreInfo(self, field):
        query = 'SELECT {} FROM basic_store_info'.format(field)
        data = ''
        returnd = SQConnect(query,data).ONE()
        
        return returnd[0]       
        
        
    def coverPage(self): #, canvas, doc
        """
        Create the document
        """
        
        right = self.styles['Heading1']
        right.alignment=TA_RIGHT
        
        dated = "{}".format(self.dated)
        ptext = '{}'.format(dated)
        p = (Paragraph(ptext, right))
        self.story.append(p)
        
        left = self.styles['Heading1']
        left.alignment=TA_LEFT
        
        #spacer = Spacer(0, 0.25*inch)
        storeName = self.StoreInfo('name')
        ptext = '{}'.format(storeName)
        p = (Paragraph(ptext, left))
        
        self.story.append(p)
        
        normal = self.styles['Normal']
        normal.alignment=TA_CENTER
   
        header_text = " {} ".format(self.header)
        ptext = '<font size=12>{}</font>'.format(header_text)
        self.story.append(Paragraph(ptext, normal))
        #self.story.append(spacer)
 
       #@ self.story.append(Paragraph(ptext, normal))
 
   
        #p = Paragraph(header_text, normal)
        #p.wrapOn(self.c, self.width, self.height)
        #p.drawOn(self.c, *self.coord(100, 100, mm))
        #ptext = """<font size='18'>{}</font>""".format(storeName)
 
        #p = Paragraph(ptext, style=normal)
        #p.wrapOn(self.c, self.width-50, self.height)
        #p.drawOn(self.c, 30, 550)
 
        #ptext = """<font align='left'><b>{}</b></font><font align='right'>{}</font>""".format(self.line_two, dated)
  #      p = Paragraph(ptext, style=normal)
  #      p.wrapOn(self.c, self.width-50, self.height)
  #      p.drawOn(self.c, 330, 575)
 
        
    def GetSalesTx(self):
        """ Sales Tax Report """
        grid = wx.FindWindowByName('closing_monthly_salesTax_grid')
        data = []
        line_data = []
        for row in range(grid.GetNumberRows()):
            label = grid.GetRowLabelValue(row)
            taxable = grid.GetCellValue(row, 0)
            taxempt = grid.GetCellValue(row, 1)
            total = grid.GetCellValue(row, 2)
            line_data.append([label, taxable, taxempt, total])
            
        data.append(line_data)                
        
        self.coverPage()
            
        
        font_size = 8
        centered = ParagraphStyle(name="centered", alignment=TA_RIGHT)
        
        for idx in range(len(data)):
            
            for sec in range(len(data[0])):
                if sec == 0:
                    ptext = "<font size={}><b>{}</b></font>".format(font_size, data[idx][sec])
                    #ptext = data[idx][0]
                    p = Paragraph(ptext, centered)
                    data[idx][sec]=p
                    
                    ptext = "<font size={}>{}</font>".format(font_size-1, data[idx][sec])
                    p = Paragraph(ptext, centered)
                    data[idx][sec]=p
                    
                
            
        
        
        table = Table(data, colWidths=[60, 60, 60,  60])
 
        table.setStyle([('LINEABOVE',(0,-1),(-1,-1), 1, colors.black),])
        
        self.story.append(table)
      
#        self.story.append(PageBreak())
        
         
        return True
        
    def AllTransactions(self,section=None):
        """
        Create Daily Closing
        """
        
        if section == 'daily':
            #today = datetime.datetime.strptime('2018-09-01', '%Y-%m-%d')
            
            today = datetime.datetime.now().date().strftime('%Y-%m-%d')
            headers = ["Trans #", "Date", "Time", "Type of<br/>Transaction", "SubTotal",
                        "Tax", "Total","Cust Acct #", "Paid", "PayType"]
        
            query = '''SELECT transaction_id, date, time, type_of_transaction, subtotal_price, tax, total_price, cust_num, paid, pay_method
                       FROM transaction_payments
                       WHERE date=(?)'''
         
            data = [today,]
        
            returnd = SQConnect(query, data).ALL()
       
        if section == 'monthly':
            today = datetime.datetime.now().date().strftime('%m')
            headers = ["Trans #", "Date", "Time", "Type of<br/>Transaction", "SubTotal",
                        "Tax", "Total","Cust Acct #", "Paid", "PayType"]
        
            query = '''SELECT transaction_id, date, time, type_of_transaction, subtotal_price, tax, total_price, cust_num, paid, pay_method
                       FROM transaction_payments
                       WHERE month(date)=(?)'''
         
            data = [today,]
        
            returnd = SQConnect(query, data).ALL()
        
        
        if returnd is None or len(returnd) == 0:
            return False
        
        self.coverPage()    
        line_data = returnd  #headers
        text_data = headers
        d = []
        font_size = 8
        centered = ParagraphStyle(name="centered", alignment=TA_JUSTIFY)
        
        for text in text_data:
            ptext = "<font size={}><b>{}</b></font>".format(font_size, text)
            p = Paragraph(ptext, centered)
            d.append(p)
 
        data = [d]
 
        line_num = 1
 
        formatted_line_data = []
        num_of_trans = len(line_data)
        price = 0
        taxd = 0
        subtotal = 0
        for tax in line_data:
            price += tax[6]
            taxd += tax[5]
            subtotal += tax[4]
        
        trns = '{} Transactions'.format(num_of_trans)    
        last_line = [trns,'','','Totals',RO().DoRound(subtotal,'1.00'),VO().DoRound(taxd, '1.00'),VO().DoRound(price,'1.00'), '','','']
        for x in range(len(line_data)):
            for item in line_data[x]:
                ptext = "<font size={}>{}</font>".format(font_size-1, item)
                p = Paragraph(ptext, centered)
                formatted_line_data.append(p)
            data.append(formatted_line_data)
            formatted_line_data = []
        data.append(last_line)
 
        table = Table(data, colWidths=[60, 60, 60, 75, 60, 
                                       60, 60, 60, 60, 60], repeatRows=1)
 
        table.setStyle([('LINEBELOW',(0,0),(-1,0), 1,colors.black),
                        ('LINEABOVE',(0,-1),(-1,-1), 1, colors.black),])
        
        
        #style = self.styles['Normal']
        #style.alignment=TA_JUSTIFY
        #p = Paragraph('<b>{}</b><b>Date : {}</b>'.format(storeInfo, today))
        style = self.styles['Normal']
        style.alignment=TA_CENTER
        p = Paragraph('<b>All Transactions Report</b>',style)
        
        self.story.append(table)
      
        self.story.append(PageBreak())

    
        cards, cash, charged, debitd, checkd, taxd = 0,0,0,0,0,0
        qcards, qcash, qcharged, qdebitd, qcheckd = 0,0,0,0,0
        #dated = '2018-05-29'
        #dated = datetime.date.today().strftime('%Y-%m-%d')
        
        query = 'SELECT card5_payment, cash_payment, card2_payment, card3_payment, card1_payment, card4_payment, debit_payment, check_payment, charge, tax FROM transaction_payments WHERE date=(?);'
        data = (today,)
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
            
        
        #title_list = ['In Drawer']
        totald = cards + checkd + charged + debitd + taxd + cash
        qtyd = qcards + qcheckd + qcharged + qdebitd + qcash
        
        chk_list = [('Cash',qcash, cash),('Check', qcheckd, checkd),('Charge',qcharged, charged),('Debit',qdebitd,debitd),('Credit Cards',qcards, cards),('Tax','',taxd),('SubTotal','',subtotal),('Total','',price)]
        shuttle = []
        data = ['Payment Type','Qty','Total']
        shuttle.append(data)
        for label, qty, vari in chk_list:
            if vari > 0:
                datad = [label, qty, vari]
                shuttle.append(datad)
        
        #title_list.append('Total')
        
        
        
        style = self.styles['Normal']
        style.alignment=TA_CENTER
        p = Paragraph('<b>Cash Drawer Summary</b>',style)
        table = Table(shuttle, colWidths=[120, 120,120])
        table.setStyle([('LINEBELOW',(0,0),(-1,0), 1,colors.black),
                        ('ALIGN',(2,0),(2,-1), 'RIGHT'),
                        ('LINEABOVE',(0,-1),(-1,-1), 1, colors.black)])
        
        self.story.append(p)
        
        self.story.append(table)
        
        return True
        
class DailyTab(wx.Panel):
    def __init__(self, parent, debug=False):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.SetName('DailyTab')
        

        MainSizer = wx.BoxSizer(wx.VERTICAL)
        
        level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        basePath = os.path.dirname(os.path.realpath(__file__))+'/'
        iconloc = ButtonOps().Icons('pdf', 48)
        
        box = wx.StaticBox(self, -1, label='PDF Report')
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        
        icon = wx.BitmapButton(self, wx.ID_ANY, 
                               wx.Bitmap(iconloc),
                               name='closing_daily_pdf_button', 
                               style=wx.BORDER_NONE, size=(100,100))
                               
        
        icon.Bind(wx.EVT_BUTTON, self.OnPrint)
        
        boxSizer.Add(icon, 0, wx.ALL|wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL, 25)
        
        level1Sizer.Add(boxSizer, 0, wx.ALL, 5)
        
        level2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        
        level3Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        options = wx.StaticBox(self, -1, label='Report Options')
        boxSizer = wx.StaticBoxSizer(options, wx.HORIZONTAL)
        
        gbs = wx.GridSizer(4,5, 5,5)
        cb_list = [('Transactions','closing_daily_allTransactions_checkbox'),
                   ('Cash Drawer Totals','closing_daily_CashDrawer_checkbox')]
        
        for label, name in cb_list:
            ctrl = wx.CheckBox(self, -1, label=label, name=name)
            gbs.Add(ctrl, 0)
            
        
        boxSizer.Add(gbs, 0, wx.ALL|wx.EXPAND, 5)
        level3Sizer.Add(boxSizer, 0)
        sizer_list = [level1Sizer, level2Sizer, level3Sizer]
        for sizr in sizer_list:
            MainSizer.Add(sizr, 0, wx.ALL|wx.EXPAND, 5)
        #MainSizer.Add(level1Sizer, 0, wx.ALL|wx.EXPAND, 5)
        
        #MainSizer.Add((100,100),0)
        #MainSizer.Add(level3Sizer, 0, wx.ALL|wx.EXPAND, 5)
        
        self.SetSizer(MainSizer)
        self.Layout()
        
        wx.CallAfter(self.OnLoad, event='')

    def OnLoad(self, event):
        cb_list = [('closing_daily_allTransactions_checkbox', 'reports_closing_daily','all_transactions'),
                   ('closing_daily_CashDrawer_checkbox','reports_closing_daily','cash_drawer_totals'),
                   ('closing_daily_custInvoices_checkbox','reports_closing_daily','customer_invoiced')]

        for name, table, field in cb_list:
            query = '''SELECT {} 
                       FROM {}
                       WHERE abuser=(?)'''.format(field, table)
            data = ['rhp',]
            returnd = SQConnect(query, data).ONE()
        
            wx.FindWindowByName(name).SetCtrl(returnd[0])
                    
    def OnPrint(self, event):
        
        t = CreatePDF(section='dailyClose')
        t.run()
        
        
class WeeklyTab(wx.Panel):
    def __init__(self, parent, debug=False):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.SetName('WeeklyTab')
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        basePath = os.path.dirname(os.path.realpath(__file__))+'/'
        iconloc = ButtonOps().Icons('print')
        box = wx.StaticBox(self, -1, label='Print Report')
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        icon = wx.BitmapButton(self, wx.ID_ANY, 
                               wx.Bitmap(iconloc),
                               name='password_save_button', 
                               style=wx.BORDER_NONE, size=(100,100))
                               
        icon.Bind(wx.EVT_BUTTON, self.OnPrint)
        boxSizer.Add(icon, 0, wx.ALL|wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL, 25)
        level1Sizer.Add(boxSizer, 0, wx.ALL, 5)
        level2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        options = wx.StaticBox(self, -1, label='Report Options')
        boxSizer = wx.StaticBoxSizer(options, wx.HORIZONTAL)
        gbs = wx.GridSizer(4,5, 5,5)
        cb_list = [('Sales Breakdown','closing_weekly_salesBreakdown_checkbox'),
                   ('Inventory Top10','closing_weekly_inv_Top10_checkbox'),
                   ('Inventory Losers 10','closing_weekly_losers10_checkbox'),
                   ('Most Requested Items','closing_weekly_mostRequested_checkbox')]
        
        for label, name in cb_list:
            ctrl = wx.CheckBox(self, -1, label=label, name=name)
            gbs.Add(ctrl, 0)
        
        boxSizer.Add(gbs, 0, wx.ALL|wx.EXPAND, 5)
        level2Sizer.Add(boxSizer, 0)
        MainSizer.Add(level1Sizer, 0)
        MainSizer.Add((100,100),0)
        MainSizer.Add(level2Sizer, 0)
        self.SetSizer(MainSizer)
        self.Layout()

    def OnPrint(self, event):
        pass


class MonthlyTab(wx.Panel):
    def __init__(self, parent, debug=False):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.SetName('MonthlyTab')
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        #pdfbtn = PDFButton(self, name='closing_monthly_pdf_button')
        
        basePath = os.path.dirname(os.path.realpath(__file__))+'/'
        iconloc = ButtonOps().Icons('PDF', 48)
        
        box = wx.StaticBox(self, -1, label='')
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        
        icon = wx.BitmapButton(self, wx.ID_ANY, 
                               wx.Bitmap(iconloc),
                               name='closing_monthly_pdf_button', 
                               style=wx.BORDER_NONE, size=(100,100))
                               
        
        icon.Bind(wx.EVT_BUTTON, self.OnPrint)
        
        boxSizer.Add(icon, 0, wx.ALL|wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL, 25)
        
        level1Sizer.Add(boxSizer, 0, wx.ALL, 5)
        
        grid = gridlib.Grid(self, -1, name='closing_monthly_salesTax_grid',style=wx.BORDER_SUNKEN, size=(450, 350))
        rowLabel_set = []
        for x in range(1,13):
            rowLabel_set.append(datetime.datetime.strptime(str(x), '%m').strftime('%B'))
        
        rowLabel_set.append('Total')
        colLabel_set = ['Taxable','Tax Exempt', 'Taxes']
        
        #

        grid.CreateGrid(len(rowLabel_set), len(colLabel_set))
        for idx, label in enumerate(colLabel_set):
            grid.SetColLabelValue(idx, label)
            grid.SetColSize(idx, 120)        
        
        grid.SetDefaultCellAlignment(wx.ALIGN_RIGHT, wx.ALIGN_RIGHT)
        
        grid.EnableEditing(False)
        for label in rowLabel_set:
            for row in range(grid.GetNumberRows()):
                grid.SetRowLabelValue(row, rowLabel_set[row])
        
        HUD.GridOps(grid.GetName()).GridAlternateColor('')        
        #grid.AutoSize()
        
        level1Sizer.Add(grid, 0, wx.ALL|wx.EXPAND, 5)
        MainSizer.Add(level1Sizer, 0, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(MainSizer)
        self.Layout()
        
        wx.CallAfter(self.OnLoad, event='')
        
    def OnLoad(self, event):
        """ Load Sales Tax Grid """
        grid = wx.FindWindowByName('closing_monthly_salesTax_grid')
        thisYear = datetime.datetime.now().date().strftime('%Y')
        taxset = [('Taxable',0),('Tax Exempt',1)]
        for status,val in taxset:
            for row in range(grid.GetNumberRows()-1):
                label = grid.GetRowLabelValue(row)
                mnth = datetime.datetime.strptime(label, '%B').strftime('%m')
                query = '''SELECT total_price
                           FROM transactions
                           WHERE tax_exempt=(?) AND YEAR(date)=(?) AND MONTH(date)=(?)'''
                data = [val, thisYear, mnth,]
                returnd = SQConnect(query, data).ALL()
                tot = 0
                #print 'returnd : ',returnd
                if returnd is not None:
                    for item in returnd:
                        #print 'teim : ',item
                        item = HUD.VarOps().DeTupler(item)
                        tot += item
                
                grid.SetCellValue(row, val, str(tot))
        t1 = 0
        t2 = 0
        t3 = 0
        for row in range(grid.GetNumberRows()-1):
            
            taxable = grid.GetCellValue(row, 0)
            if taxable == '':
                taxable = 0
            
            taxrate = 0.065
            taxes = HUD.RetailOps().DoRound(Decimal(taxable)*Decimal(taxrate), '1.00')
                
            grid.SetCellValue(row, 2, str(taxes))
        
            a = grid.GetCellValue(row, 0)
            if a == '':
                a = 0
            b = grid.GetCellValue(row, 1)
            if b == '':
                b = 0
            c = grid.GetCellValue(row, 2)
            if c == '':
                c = 0     
            t1 += Decimal(a)
            t2 += Decimal(b)
            t3 += Decimal(c)
            
        for idx, i in enumerate([t1,t2,t3]):
            grid.SetCellValue(row+1, idx, str(i))


    def OnPrint(self,event):
        t = CreatePDF(section='salesTax')
        t.run()           
            
        


class QuarterlyTab(wx.Panel):
    def __init__(self, parent, debug=False):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.SetName('QuarterlyTab')
        



class YearlyTab(wx.Panel):
    def __init__(self, parent, debug=False):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.SetName('YearlyTab')
        


class ClosingTab(wx.Panel):
    def __init__(self, parent, debug=False):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.SetName('ClosingTab')
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        
        clnb = wx.Notebook(self, -1, name='closingtab_notebook')
        TabOne = DailyTab(clnb)
        TabTwo = WeeklyTab(clnb)
        TabThree = MonthlyTab(clnb)
        TabFour = QuarterlyTab(clnb)
        TabFive = YearlyTab(clnb)
        
        tab_list = [(TabOne,'End of Day'),(TabTwo,'End of Week'),(TabThree,'End of Month'),(TabFour,'End of Quarter'),(TabFive,'End of Year')]
        
        for tab, label in tab_list:
            clnb.AddPage(tab, label)
        
        #clnb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.ReportsOnPageChanged)
        
        MainSizer.Add(clnb, 0, wx.ALL|wx.EXPAND, 5)
        
        self.SetSizer(MainSizer)
        self.Layout()
        
        
        
    def ClosingOnPageChanged(self, event):
        pass
        
        
           

class InventoryTab(wx.Panel):
    def __init__(self, parent, debug=False):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        

class VendorsTab(wx.Panel):
    def __init__(self, parent, debug=False):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        

class CustomersTab(wx.Panel):
    def __init__(self, parent, debug=False):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        




class StartPanel(wx.Panel):
    def __init__(self, parent, debug=False):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        

        MainSizer = wx.BoxSizer(wx.VERTICAL)
        
        
        
        repnb = wx.Notebook(self, -1, name='Reports_Notebook')
        
        TabOne = ClosingTab(repnb)
        TabTwo = InventoryTab(repnb)
        TabThree = CustomersTab(repnb)
        TabFour = VendorsTab(repnb)
        
        page_list = [(TabOne, 'Closing'),(TabTwo,'Inventory'),(TabThree,'Customers'),(TabFour,'Vendors')]
        for tab, label in page_list:
            repnb.AddPage(tab, label)
        
        repnb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.ReportsOnPageChanged)

        MainSizer.Add(repnb, 1, wx.ALL|wx.EXPAND, 5)
    
        
        
        
        self.SetSizer(MainSizer)
        
        self.Layout()
        
    def OnPrintButton(self, event):
        pass
        
    def OnExitButton(self, event):
        pass        

    
    def ReportsOnPageChanged(self, event):
        pass
        

class MaintenanceScreen(wx.Frame):
    def __init__(self, debug=False):
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX) & (~wx.MINIMIZE_BOX)
        wx.Frame.__init__(self, None, -1, "RHP Maintenance", size=(1200,700), style=style)
        
        self.panel_one = StartPanel(self)
       
#        wx.lib.inspection.InspectionTool().Show()

 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel_one, 1, wx.EXPAND,5)
        
        self.SetSizer(sizer)
        
 

        self.Layout()

       
  
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MaintenanceScreen()
    frame.Centre()
    frame.SetName('Maintenance_Frame')
    frame.Show()
    app.MainLoop()        
