#!/usr/bin/env python
"""
RHP-POS' Point of Sale.

Point of Sale Script for RHP-POS originally was a clone of the POS system used
at my job.  After Multiple Improvements it looks like this, and probably will
change again after awhile.
"""
#
# -*- coding: utf-8 -*-
#
#
#
#import wxversion
#wxversion.select('2.8')

import wx
import re
import sys
import time
#import wx.calendar as cal
import wx.grid as gridlib
import faulthandler
import json
import pout
from functools import partial
import xml.etree.cElementTree as ET
import datetime
import wx.lib.masked as masked
import wx.lib.inspection
import handy_utils as HUD
from customers import CustDialog
from wx.lib.masked import NumCtrl
from button_stuff import ButtonOps
from customers import StartPanel as CustStartPanel
from inventory import StartPanel as InvStartPanel
from maintenance import StartPanel as MaintStartPanel
from vendors import StartPanel as VendStartPanel
from reports import StartPanel as ReportStartPanel
from about import StartPanel as AboutStartPanel
from wx.lib.masked import TimeCtrl
from decimal import Decimal, ROUND_HALF_UP
from db_related import LookupDB



class AcctPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY, style=wx.TAB_TRAVERSAL)
        
        #
        self.phoneList = ['']
        self.SetName('AcctPanel')
        self.CustInfo = {}

        ctrlList = [('Acct # :', 'pos_acctNum_txtctrl', (200,-1)),
                    ('Name :', 'pos_acctName_txtctrl', (200, -1)),
                    ('Address :', 'pos_acctAddr_btn', (200,130)),
                    ('Phone :', 'pos_acctPhone_btn', (200,-1)),
                    ('Discount :', 'pos_acctDisc_txtctrl', (200, -1))]
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        for labeld, named, sized in ctrlList:
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            s = wx.StaticText(self, -1, label=labeld)
            
            if 'txtctrl' in named:
                if 'acctNum' in named:
                        c = HUD.RH_TextCtrl(self, -1, name=named, size=sized, style=wx.TE_PROCESS_ENTER)
                        c.Bind(wx.EVT_TEXT_ENTER, self.acctLookup)
                        randomId = wx.NewId()
                        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_ALT,  ord('A'), randomId )])
                        c.SetAcceleratorTable(accel_tbl)
                        c.Bind(wx.EVT_MENU, self.onAddAccount, id=randomId)
                else:
                        c = HUD.RH_TextCtrl(self, -1, name=named, size=sized)
            if 'btn' in named:
                c = HUD.RH_Button(self, -1, name=named, label='')
            
            sizer.Add(s, 0, wx.ALL|wx.EXPAND, 13)
            sizer.Add(c, 0, wx.ALL|wx.EXPAND, 5)

            MainSizer.Add(sizer, 0, wx.ALL|wx.EXPAND, 0)    
        
        self.SetSizer(MainSizer, 0)
        self.Layout()

    def onLookup(self, event):
        pass
        
    def acctLookup(self, event):
        cst = wx.FindWindowByName('pos_acctNum_txtctrl')
        acctNum = cst.GetValue()
        self.cust = HUD.CustomerManagement(acctNum)
        count_returnd = self.cust.SearchCount()
        if count_returnd == 0:
            print('None Returnd')
            cst.SetValue('Not Found')
            cst.SelectAll()
            return
        
        elif count_returnd > 0:
            
            with HUD.CustLookupDialog(self, title="Customer Lookup") as dlg:
                custPicked = None
                dlg.ShowModal()
                custPicked = dlg.itemPicked.upper().strip()
            
        print("Customer Lookup D : ", custPicked)
        

        self.SetCustInfo(custPicked)
        self.CustAcctNum = custPicked
        
        item = wx.FindWindowByName('pos_acctNum_txtctrl').SetValue(self.CustAcctNum)
        
        

    def SetCustInfo(self, acctnum):
        pout.v(f'Set Cust Info : {acctnum}')

        returnd = HUD.QueryOps().GetQuery('full_name,address_acct_num,rental_of,phone_numbers',
                                          'customer_basic_info',
                                          'cust_num', acctnum)
                                        
                                
        pout.v(f'Returnd : {returnd}')
        #(fullName, addrAcctNum, rentalAccts, phoneNums) = returnd
        #pout.s(fullName)



    def onTab(self, event):    
        ctrl = wx.FindWindowByName('entry_upc_txtctrl')
        ctrl.SetFocus()

#        HUD.GridOps('pos_transaction_grid').GridFocusNGo(0)
        event.Skip()

        
    def onAddAccount(self, event):
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
        dlg = HUD.CustomerAddDialog(self, title="Add Customer", style=style)
        dlg.ShowModal()
        
        try:
            
            self.custPicked = dlg.itemPicked
        
        except:
            print(f'Cust Picked : {self.custPicked}')  
        
                    
        
        self.custPicked = dlg.itemPicked
        
        dlg.Destroy()
   
          
class InfoTab(wx.Panel):
    def __init__(self, *args, **kwargs):
        """ Info Tab for Top Panel """
        wx.Panel.__init__(self, *args, **kwargs)
        
        self.SetName('InfoTab')
        
        
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)

        aSizer = wx.BoxSizer(wx.HORIZONTAL)
        listd = [('P.O.Number', 'pos_PoTab_ponumber_txtctrl', 240),
                 ('Authorized Person', 'pos_PoTab_authpeeps_combobox', 150)]

        for label, name, sized in listd:
            box = wx.StaticBox(self, -1, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            if 'combobox' in name:
                ctrl = wx.ComboBox(self, -1, name=name)
            if 'txtctrl' in name:
                ctrl = wx.TextCtrl(self, -1, name=name, size=(sized, -1))

            boxSizer.Add(ctrl, 0, wx.ALL, 5)
            aSizer.Add(boxSizer, 0, wx.ALL, 5)

        
        notes_txtctrl = wx.TextCtrl(self, -1,
                                    name='pos_InfoTab_notes_txtctrl',
                                    size=HUD.MiscOps().WHSup(widget=(725, 120)),
                                    style=wx.TE_MULTILINE)

        notes_txtctrl.SetBackgroundColour(HUD.Themes().GetColor('info'))
        notes_txtctrl.Disable()

        MainSizer.Add(notes_txtctrl, 0)
        MainSizer.Add(aSizer, 0, wx.ALL, 5)

        self.SetSizer(MainSizer, 0)
        self.Layout()


    def Load(self, custNum):
        
        returnd = LookupDB('customer_sales_options').Specific(custNum, 'cust_num','pos_clerk_message')
        returnd = HUD.VarOps().DeTupler(returnd)
        
        wx.FindWindowByName('pos_InfoTab_notes_txtctrl').SetCtrl(returnd)
        
        
class NotesTab(wx.Panel):
    def __init__(self, *args, **kwargs):
        """ Info Tab for Top Panel """
        wx.Panel.__init__(self, *args, **kwargs)
        self.SetName('NoteTab')
        self.noteTab_dict = {'BEGIN':None, 'After':{}, 'END':None}
                      
        MainSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.ctrl = HUD.RH_TextCtrl(self, -1,
                                   name='pos_NotesTab_notes_txtctrl',
                                   size=(625, 150),
                                   style=wx.TE_MULTILINE)

        self.ctrl.SetBackgroundColour(HUD.Themes().GetColor('note'))
        level2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        box = wx.StaticBox(self, label='Positioning')
        boxSizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        listd = [('Beginning','notes_begin_button',self.onBeginButton),
                 ('      After\nCurrent Line','notes_acurrentLine_button',self.onAfterLine),
                 ('End','notes_end_button',self.onEndButton)]
                 
        for label, name, hdlr in listd:
            btn = wx.Button(self, -1, label=label, name=name)
            btn.Bind(wx.EVT_BUTTON, hdlr)
            boxSizer.Add(btn, 0, wx.ALL, 3)
            
        level2Sizer.Add(boxSizer, 0, wx.ALL, 3)
            
        MainSizer.Add(self.ctrl, 0, wx.ALL, 5)
        MainSizer.Add(level2Sizer, 0, wx.ALL, 5)
        self.SetSizer(MainSizer, 0)
        self.Layout()
    
    def onBeginButton(self, event):
        notepad = 'pos_NotesTab_notes_txtctrl'
        memo = self.ctrl.GetCtrl()
        linePos = 'BEGIN'
        self.noteTab_dict['Begin'] = memo
        # HUD.CurrentNotes().TempSet(linePos, memo)
        self.ctrl.Clear()
        self.GoUPC()
    
    def onAfterLine(self, event):
        notepad = 'pos_NotesTab_notes_txtctrl'
        memo = self.ctrl.GetCtrl()
        row = HUD.GridOps('pos_transactions_grid').CurGridLine()
        linePos = 'A{}'.format(row)
        self.noteTab_dict['After'][row] = memo
        # HUD.CurrentNotes().TempSet(linePos, memo)
        self.ctrl.Clear()
        self.GoUPC()

    def onEndButton(self, event):
        notepad = 'pos_NotesTab_notes_txtctrl'
        memo = self.ctrl.GetCtrl()
        linePos = 'END'
        
        self.noteTab_dict['End'] = memo
        #HUD.CurrentNotes().TempSet(linePos, memo)
        self.ctrl.Clear()
        self.GoUPC()
   
    def GoUPC(self):
        wx.FindWindowByName('entry_upc_txtctrl').SetFocus()
     

class PennyTab(wx.Panel):
    def __init__(self, *args, **kwargs):
        """Info Tab for Top Panel."""
        wx.Panel.__init__(self, *args, **kwargs)
        self.SetName('PennyTab')
        


class FRTab(wx.Panel):
    def __init__(self, *args, **kwargs):
        """Info Tab for Top Panel."""
        wx.Panel.__init__(self, *args, **kwargs)
        self.SetName('FRTab')
        

class NotePanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        
        self.SetName('NotePanel')
        
        MainSizer = wx.BoxSizer(wx.HORIZONTAL)

        #rightpanel = wx.Panel(self)
        rsNotebook = wx.Notebook(self, -1,
                                 name="pos_RightPanel_notebook",
                                 size=(750, 225))

        rsTabOne = InfoTab(rsNotebook)
        rsTabTwo = NotesTab(rsNotebook)
        rsTabThree = PennyTab(rsNotebook)
        rsTabFour = FRTab(rsNotebook)

        rsNotebook.AddPage(rsTabOne, 'Info')
        rsNotebook.AddPage(rsTabTwo, 'Notes')
        rsNotebook.AddPage(rsTabThree, 'Pennies')
        rsNotebook.AddPage(rsTabFour, 'FR')
        
        
        MainSizer.Add(rsNotebook, 1, wx.ALL | wx.EXPAND, 5)
    
        self.SetSizer(MainSizer, 0)
        self.Layout()   
        


        
    
class DefaultOptionsPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)

        self.SetName('DefaultOptionsPanel')

        MainSizer = wx.BoxSizer(wx.VERTICAL)

        listd = [('Order Type', 'pos_ordertype_txtctrl', 150),
                 ('Tax Type', 'pos_taxtype_txtctrl', 150),
                 ('Discount Type', 'pos_discounttype_combobox',
                    ['None', 'Discount by Line', 'Discount All'])]
                 #('Paper Type', 'pos_papertype_combobox', ['Paper Tape',
                                                           #'Invoice'])]
        for label, name, sized in listd:
            box = wx.StaticBox(self, -1, label=label, style=wx.ALIGN_CENTER)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            if 'txtctrl' in name:
                ctrl = wx.TextCtrl(self, -1,
                                   name=name,
                                   size=(sized, -1),
                                   style=wx.TE_READONLY | wx.TE_CENTER)

            if 'combobox' in name:
                ctrl = wx.ComboBox(self, -1,
                                   name=name,
                                   choices=sized,
                                   size=(120, -1))

                ctrl.Bind(wx.EVT_COMBOBOX, self.onComboBox)
                ctrl.SetSelection(0)

                if 'discount' in name:
                    disc_txtctrl = masked.NumCtrl(self, -1,
                                                  value=0,
                                                  name='''pos_discountpercent_txtctrl''',
                                                  integerWidth=3,
                                                  fractionWidth=0)

                    disc_txt = wx.StaticText(self, -1, label='%')

            font = wx.Font(wx.FontInfo(14).Bold())
            ctrl.SetBackgroundColour('Blue')
            ctrl.SetForegroundColour('White')
            ctrl.SetFont(font)

            boxSizer.Add(ctrl, 0, wx.ALL, 3)
            if 'discount' in name:
                
                boxSizer.Add(disc_txtctrl, 0)
                boxSizer.Add(disc_txt, 0)
                disc_txtctrl.Disable()
                disc_txtctrl.SetBackgroundColour('Gray')
        
            MainSizer.Add(boxSizer, 0, wx.ALL|wx.EXPAND, 3)
            
            self.SetSizer(MainSizer, 0)
            self.Layout()
            
    def onComboBox(self, event):
        
        obj = event.GetEventObject()
        named = obj.GetName()
        discountbox = 'pos_discounttype_combobox'
        if discountbox in named:
            choiced = wx.FindWindowByName(discountbox).GetValue()
            
            if choiced == 'Discount All':
                item = wx.FindWindowByName('pos_discountpercent_txtctrl')
                item.Enable()
                item.SetBackgroundColour('White')
            if choiced != 'Discount All':
                item = wx.FindWindowByName('pos_discountpercent_txtctrl')
                item.Disable()
                item.SetBackgroundColour('Gray')

        


class TransactionPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        
        
        self.SetName('TransactionPanel')
        #self.SetBackgroundColour('Red')
                
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        entrySizer = wx.BoxSizer(wx.HORIZONTAL)
        
        ctrl_list = [('UPC','entry_upc_txtctrl', (120,-1)),
                     ('Description','entry_desc_txtctrl',(200,-1)),
                     ('Set\nPrice','entry_setprice_checkbox', None),
                     ('Discount','entry_discount_txtctrl', (70,-1)),
                     ('Disc\nAll', 'entry_discountAll_checkbox', None),
                     ('Price', 'entry_price_txtctrl', (70,-1)),
                     ('Quantity','entry_qty_txtctrl',(60,-1)),
                     ('Add to Cart','entry_addcart_btn', self.AddtoCart)]
        
        fontsize, blk = HUD.MiscOps().WHSup(font=8)
        fontd = wx.Font(wx.FontInfo(fontsize))
        for label, name, sized in ctrl_list:
            container = wx.BoxSizer(wx.VERTICAL)
            
            if 'checkbox' in name:
                ctrl = HUD.RH_CheckBox(self,-1, name=name, label=label)
                if 'setprice' in name:
                    ctrl.Bind(wx.EVT_CHECKBOX, self.SetPrice)
                                
            
            if 'btn' in name:
                ctrl = HUD.RH_Button(self, -1, label=label, name=name)
                if sized is not None:
                    ctrl.Bind(wx.EVT_BUTTON, sized)

            if 'txtctrl' in name:
                txt = wx.StaticText(self, -1, label=label)
                txt.SetFont(fontd)
                container.Add(txt, 0, wx.ALL, 1)
            
                if 'discount' in name:
                    ctrl = HUD.RH_NumCtrl(self, -1, name=name, integerWidth=3, fractionWidth=0, selectOnEntry=False)
                
                elif 'qty' in name:
                    ctrl = HUD.RH_NumCtrl(self, -1, name=name, integerWidth=5, fractionWidth=4, selectOnEntry=False, style=wx.TE_PROCESS_ENTER)
                
                elif 'price' in name:
                    ctrl = HUD.RH_NumCtrl(self, -1, name=name, integerWidth=5, fractionWidth=2, selectOnEntry=False)
                
                else:
                    ctrl = HUD.RH_TextCtrl(self, -1, name=name, size=sized, style=wx.TE_PROCESS_ENTER)

                if 'upc' in name:
                    ctrl.Bind(wx.EVT_TEXT_ENTER, self.lookupUPC)
                    randomId = wx.Window.NewControlId() #wx.NewId()
                    tabbackId =wx.Window.NewControlId() #wx.NewId()
        
                    ctrl.Bind(wx.EVT_MENU, self.onAddItem, id=randomId)
                    ctrl.Bind(wx.EVT_MENU, self.TabBack, id=tabbackId)
                    accel_tbl = wx.AcceleratorTable([(wx.ACCEL_ALT, ord('a'), randomId),(wx.ACCEL_SHIFT, wx.WXK_TAB,tabbackId)])
                    ctrl.SetAcceleratorTable(accel_tbl)

                if 'price' in name:
                    ctrl.Disable()
                if 'desc' in name:
                    ctrl.SetEditable(False)
                if 'qty' in name:
                    ctrl.Bind(wx.EVT_TEXT_ENTER, self.qtydone)
            
            ctrl.SetFont(fontd)
            container.Add(ctrl, 0, wx.BOTTOM, 3)
            
            aligm = wx.ALIGN_BOTTOM
            if 'checkbox' in name:
                aligm = wx.ALIGN_CENTER_VERTICAL
            
            entrySizer.Add(container, 0, wx.ALL, 5)
            
        self.grid = HUD.POS_Transactions_Grid(self, name='pos_transactions_grid', size=(950, 210))   
        #self.gridpanel = HUD.TransGridNTotalPanel(self)
        
        MainSizer.Add(entrySizer, 0, wx.ALL|wx.EXPAND, 10)
        MainSizer.Add(self.grid, 0, wx.BOTTOM, 5)
        
        
        self.SetSizer(MainSizer, 0)
        self.Layout()
        
        wx.CallAfter(self.LoadDefaults,event='')
    
    def AddtoCart(self, event):
        upc = wx.FindWindowByName('entry_upc_txtctrl').GetCtrl()
        desc = wx.FindWindowByName('entry_desc_txtctrl').GetCtrl()
        setprice = wx.FindWindowByName('entry_setprice_checkbox').GetCtrl()
        discount = wx.FindWindowByName('entry_discount_txtctrl').GetCtrl()
        discountAll = wx.FindWindowByName('entry_discountAll_checkbox').GetCtrl()
        # ntx = wx.FindWindowByName('entry_taxexempt_checkbox').GetCtrl()
        qty = wx.FindWindowByName('entry_qty_txtctrl').GetCtrl()
        price = wx.FindWindowByName('entry_price_txtctrl').GetCtrl()
        
        pricetree = self.item_model['retails']
        cost = self.item_model['cost']
        upcd = self.item_model['upc']
        taxable = self.item_model['taxable']
        if self.trans_id is None:
            self.trans_id = HUD.AccountOps().TransNumAuto(fill0s=8)
            self.trans_dict = {'SALE': {self.trans_id:{ } },'RETURN':{} }

        if Decimal(qty) > 0:
            tprice = Decimal(price)*Decimal(qty)
            totalprice = HUD.RetailOps().DoRound(tprice)
            total, disccol = HUD.RetailOps().LevelDiscount(upcd, qty, discount, totalprice)
            ntx = 'Tx'
            if taxable == False:
                ntx = 'nTx'
            upcinfo = {
                    'upc': upcd,
                    'Desc':desc,
                    'Qty':qty,
                    'Cost':cost,
                    'Price':price,
                    'SetPrice':setprice,
                    'DiscAllYN':discountAll,
                    'Discount':disccol,
                    'Taxable':ntx,
                    'PriceTree':pricetree,
                    'TotalPrice':total
                    }

            if upcd in self.trans_dict['SALE'][self.trans_id]:
                origqty = self.trans_dict['SALE'][self.trans_id][upcd]['Qty']
                newqty = origqty + qty

                self.trans_dict['SALE'][self.trans_id][upcd]['Qty'] = newqty
                totprice = Decimal(self.trans_dict['SALE'][self.trans_id][upcd]['TotalPrice']) + totalprice
                total, disccol = HUD.RetailOps().LevelDiscount(upcd, newqty, discount, totprice)
                self.trans_dict['SALE'][self.trans_id][upcd]['TotalPrice'] = total
                
            else:
                self.trans_dict['SALE'][self.trans_id][upcd]=upcinfo
                                                        
            pout.v(self.trans_dict)
            
            self.trans_dict = self.grid.Update(self.trans_dict)
            
            for i in ['entry_setprice_checkbox','entry_desc_txtctrl','entry_upc_txtctrl',
                    'entry_qty_txtctrl','entry_price_txtctrl']:
                wx.FindWindowByName(i).Clear()
            
            if discountAll == 0:
                wx.FindWindowByName('entry_discount_txtctrl').ClearCtrl()
        
            wx.FindWindowByName('entry_upc_txtctrl').SetFocus()
            
        else:
            wx.FindWindowByName('entry_qty_txtctrl').SetFocus()
     

    def lookupUPC(self, event):
        obj = event.GetEventObject()
        named = obj.GetName()
        value = obj.GetValue()
         
        self.item_model = HUD.InvMan(value).Run()
        pout.v(self.item_model)
        if self.item_model is None:
            wx.FindWindowByName('entry_upc_txtctrl').SetCtrl('Not Found')
            wx.FindWindowByName('entry_upc_txtctrl').SelectAll()
        else:
            wx.FindWindowByName('entry_upc_txtctrl').SetCtrl(self.item_model['upc'])
            wx.FindWindowByName('entry_desc_txtctrl').SetCtrl(self.item_model['desc'])
            wx.FindWindowByName('entry_price_txtctrl').SetCtrl(self.item_model['retails']['standard_price']['price'])
            
            wx.FindWindowByName('entry_setprice_checkbox').SetFocus()
        
    def qtydone(self, event):
        pass
        
        
    def SetPrice(self, event):
        obj = event.GetEventObject()
        state = obj.GetValue()
        ctrl = wx.FindWindowByName('entry_price_txtctrl')
        ctrl.Enable()
        if state is False:
            ctrl.Disable()
                        
    
    def TabBack(self,event):
        wx.FindWindowByName('AcctPanel').Focus()
        
    def LoadDefaults(self, event):
        # Current Action Item Variables
        self.trans_id = None
        self.activeTrans = True
        #custNum = HUD.GridOps('pos_acct_grid').GetCell('Account Number', 0)
        custNum = wx.FindWindowByName('pos_acctNum_txtctrl').GetCtrl()
        #----Tax & Disc Related
        s = HUD.CustomerChecks(custNum)
        self.Taxable = s.TaxStatus()
        self.AltTax = False
        self.DiscbyLine = False
        self.DiscAll, self.DiscAmtAll = s.DiscountStatus()
        self.DiscAmtOnce = 0
        #---- During Sale Types
        self.ReturnNext = False
        self.QuantitySet = False
        self.SetPrice = False
        self.TaxExemptNext = False
        self.returnItems = {}
        
        
        default_value_list = [('pos_ordertype_txtctrl','Sale'),
                              ('pos_taxtype_txtctrl','Taxable')]

        for name,value in default_value_list:
            item = wx.FindWindowByName(name).SetCtrl(value)

        self.buttonList = ['pos_repeatLast_button',
                           'pos_deleteLast_button',
                           'pos_returnNext_button',
                           'pos_itemDirect_button',
                           'pos_quantity_button',
                           'pos_price_button',
                           'pos_discount_button',
                           'pos_slsChange_button',
                           'pos_cancel_button',
                           'pos_finish_button',
                           'pos_coupon_button',
                         
                           'pos_customerInquiry_button2',
                           'pos_itemInquiry_button',
                           'pos_writeMemo_button',
                           'pos_taxExemptNextItem_button',
                           'pos_discountInvoice_button']
                  
     
    # def onTotalTransactions(self, gridName, row,debug=False):
    #     grid = wx.FindWindowByName(gridName)
    #     GrandTotal = 0
    #     TaxTotal = 0
    #     SubTotal = 0
    #     col = HUD.GridOps(grid.GetName()).GetColNumber('Quantity')
                
    #     upc = None
    #     a = HUD.GridOps(gridName)
    #     upc = a.GetCell('Item Number', row)
    #     im = InventoryManagement(upc.strip())
        
    #     if upc is not None or not upc == '':
    #         description = im.LookupDB('upc','item_detailed','description')
            
    #         qty = a.GetCell('Quantity', row)
    #         now_retail = a.GetCell(gridName, 'Price', row)
    #         raw_value = a.GetCell(gridName, 'Quantity', row)
    #         curr_discount = a.GetCell(gridName, 'Discount', row)
    #             # numeric check
    #         if raw_value == '0' or raw_value == '':
    #             for cols in range(grid.GetNumberCols()):
    #                 grid.SetCellValue(row, cols, '')
                    
    #             a.GridFocusNGo(row)
    #             return
           
    #         if all(x in '0123456789.+-' for x in raw_value):
    #             # convert to float and limit to 2 decimals
    #             valued =HUD.RetailOps().DoRound(raw_value, '1.00')
    #             grid.SetCellValue(row, col, str(valued))
    #         else:
    #             grid.SetCellValue(row, col, '')
    #             a.GridFocusNGo(row, col)
    #             return

    #         item_Number = a.GetCell('Item Number', row)
    #         testget =wx.FindWindowByName('pos_ordertype_txtctrl').GetCtrl()

    #         retailsd =HUD.RetailOps().RetailSifting(upc)
            
    #         buy_qty = grid.GetCellValue(row, col)
            
    #         if '-' in buy_qty:
    #             self.ReturnNext = True
                
    #         if self.ReturnNext is True:
                
    #             subtract = True
    #             buy_qty = buy_qty.strip('-')
    #         else:
    #             subtract = False

    #         price_breaker = 0
    #         volume_discount = 0
    #         price_level = ''

    #         last_check = 99999
            
    #         if self.SetPrice is False:
    #             for key, value in retailsd.items():
    #                 dollas = value[1].strip('$')
    #                 if dollas == '0.00' or dollas == 0:
    #                     continue
                
    #                 if Decimal(buy_qty) == 0:
    #                     for yy in range(grid.GetNumberCols()):
    #                         grid.SetCellValue(row, yy, '')
                        
    #                     a.GridFocusNGo(row)
    #                     self.SetPrice = False
    #                     return
                            
    #                 if Decimal(dollas) > 0:
    #                     self.SetPrice = False
    #                     avg_costd = Decimal(value[1].strip('$')) / Decimal(value[0])
    #                     avg_cost_special =HUD.RetailOps().DoRound(avg_costd, '1.00')
    #                     if Decimal(buy_qty) >= Decimal(value[0]):
    #                         price_breaker = avg_cost_special
    #                         volume_discount = value[0]
    #                         if 'level_' in key:
    #                             query = key.replace('_', ' ')
    #                             stopwords = ['price', 'level']
    #                             querywords = query.split()
    #                             resultwords  = [word for word in querywords if word.lower() not in stopwords]
    #                             price_level  = ' '.join(resultwords).strip('()').upper()
    #                         else:
    #                             price_level = ''

    #         if Decimal(price_breaker) >= Decimal(now_retail):
                
    #             price_breaker = now_retail
                
    #         tax_able = HUD.RetailOps().GetTaxable(upc.strip(),self.Taxable,price_level)
    #         discount_col = HUD.GridOps(gridname).GetCell('Discount',row)
            
    #         if self.SetPrice is True:
    #             price_breaker = now_retail
    #             price_level = ''
    #             volume_discount = 0
    #             priceBreakdown = ''
    #             vol_price = ''
    #             discount_col = ''
    #         else:
    #             if Decimal(volume_discount) > 1:
    #                 vol_price = '{0}/{1}'.format(volume_discount,price_breaker)
    #                 priceBreakdown = Decimal(price_breaker)/Decimal(volume_discount)
                    
    #                 discount_col = '{} - {}'.format(price_level, vol_price)
            
                        
    #         setlist = [('Tx',tax_able[1]),('Discount',discount_col)]
    #         HUD.GridOps(grid.GetName()).FillGrid(setlist,row=row)
            
    #             # Get Total
    #         transaction_type =wx.FindWindowByName('pos_ordertype_txtctrl').GetCtrl()
    #         subtract = False
    #         override = 'no'

    #         if transaction_type == 'Return' or self.ReturnNext == True:
    #             subtract = True
    #             override = 'yes'

    #         tpriced = Decimal(buy_qty)*Decimal(price_breaker)
    #         total_price =HUD.RetailOps().DoRound(tpriced, '1.00')
    #         setlist = [('Total',total_price),('Tx',tax_able[1])]
    #         HUD.GridOps(grid.GetName()).FillGrid(setlist,row=row)
    #         taxed = tax_able[0]
                
    #         if subtract is True:
    #             current_price = self.transaction.Subtract(total_price,taxed,override)
    #             qty = HUD.GridOps(grid.GetName()).GetCell('Quantity',row)
    #             if not '-' in qty:
    #                 new_qty = '-{}'.format(qty)
    #                 setList = [('Quantity',new_qty)]
    #                 HUD.GridOps(grid.GetName()).FillGrid(setList, row=row)    
    #         else:
    #             current_price = self.transaction.Add(total_price,taxed,override)

    #         doit = self.transaction.Be_Current(current_price)
                
    #         for yy in range(grid.GetNumberCols()-1):
    #             grid.SetReadOnly(row,yy,True)

    #         GrandTotal = 0
    #         TaxTotal = 0
    #         SubTotal = 0

    #         self.SetPrice = False
    #         self.ReturnNext = False
    #         ButtonOps().ButtonToggle('pos_quantity_button')
    #         ButtonOps().ButtonToggle('pos_price_button')
    #         ButtonOps().ButtonToggle('pos_returnNext_button')
    
    
    def OnRightClick(self, event):
        pass
        
    def onAddItem(self, event):
        
        
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
        FlashAdd_D = HUD.FlashAddInventory(self, title="Add Item",
                                               size=(1000, 800),
                                               style=style)
        FlashAdd_D.ShowModal()

        FlashAdd_D.Destroy()


class DefaultButtonPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        
        self.SetName('DefaultButtonPanel')
        
        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        #lvl1_1aSizer = wx.BoxSizer(wx.HORIZONTAL)
        #lvl1_1bSizer = wx.BoxSizer(wx.HORIZONTAL)
                     
        lvl1_list = [('Sale\nF&1', 'pos_sale_button', self.onSaleF1, wx.WXK_F1),
                     ('Return\nF&2', 'pos_return_button', self.onReturnF2, wx.WXK_F2),
                     ('Quote\nF&5', 'pos_quote_button', self.onQuoteF5, wx.WXK_F5),
                     ('Tax Type\nF&6', 'pos_taxtype_button', self.onTaxTypeF6, wx.WXK_F6),
                     ('Print Form\nF&8', 'pos_printform_button', self.onPrintFormF8, wx.WXK_F8),
                     ('Payment\nF1&0', 'pos_payment_button', self.onPaymentF10, wx.WXK_F10),
                     ('&Pay Out\nF12', 'pos_payout_button', self.onPayOutF12, wx.WXK_F12),
                     ('Cash\n&Drawer', 'pos_cashdrawer_button', self.onCashDrawer, None),
                     ('&Reload Held\nTransaction', 'pos_reloadtransaction_button',self.onReloadTransaction, None),
                     ('&Customer\nInquiry', 'pos_customerInquiry_button', self.onCustomerInquiry, None),
                     ('&Item Inquiry', 'pos_iteminquiry_button', self.onItemInquiry, None),
                     ('&Open\nDrawer', 'pos_opendrawer_button', self.onOpenDrawer, None),
                     ('&Exit', 'pos_exit_button', self.onExit, None)]
        
        cntcol = len(lvl1_list)
        if not Decimal(cntcol) % 2 == 0:
            cntcol += 1
        colnum =HUD.RetailOps().DoRound(cntcol, '1')/2
        
        gs = wx.GridSizer(2, int(colnum), 5,5)
        lvlnum = 1
        bar_width = 950
        num_of_levels=2
        min_buttonWidth = 50
        button_gap = 3
        buttonWidth = ButtonOps().ButtonWidth_onRow(len(lvl1_list),bar_width,num_of_levels,min_buttonWidth, button_gap)
        lvl3_list = ButtonOps().ListAdjustEven(lvl1_list)
        #print 'lvl1_list : ',lvl3_list
        entries = {}
        idx = 2
        cnt = 0
        acceler = {}
        
        #self.Lvl3_1aSizer.Add(grid, 0)
        for label, name, hdlr, shortcut in lvl1_list:
            randomId = wx.Window.NewControlId() #wx.NewId()
                                
            labeld = ButtonOps().ButtonCenterText(label)
            btn = wx.Button(self, 
                            id=randomId,
                            label=labeld,
                            name=name,
                            size=(buttonWidth, 65))
           
            if hdlr == '':
                btn.Bind(wx.EVT_BUTTON, self.onBlank)
            else:
                btn.Bind(wx.EVT_BUTTON, hdlr)
                if shortcut is not None:
                    self.Bind(wx.EVT_MENU, hdlr, id=randomId)
                    acceler[idx] = wx.AcceleratorEntry(wx.ACCEL_NORMAL, shortcut, randomId)
            gs.Add(btn, 0)
            lvlnum += 1
            idx += 1
        listd = []
        #print 'Acceler \n ** {}'.format(acceler)
        for key ,value in acceler.items():
            listd.append(value)
        accel_tbl = wx.AcceleratorTable(listd)
        
        #print 'Acceler \n @@ {}'.format(accel_tbl.IsOk())
         
        self.SetAcceleratorTable(accel_tbl)
        MainSizer.Add(gs, 1)
        #MainSizer.Add(lvl1_1aSizer, 0)
        #MainSizer.Add(lvl1_1bSizer, 0)
        
        btn = wx.Button(self, -1,
                        label='&Begin\nTransaction',
                        name='pos_beginTransaction_button',
                        size=(200, 150))

        btn.Bind(wx.EVT_BUTTON, self.OnBeginTransaction)

        MainSizer.Add(btn, 0, wx.ALL, 10)
        self.SetSizer(MainSizer, 0)
        self.Layout()
     


    def OnBeginTransaction(self, event):
        
        self.trans_dict = {}
        self.TransDict = {}
        self.TransDict['CustInfo'] = {}
        self.TransDict['ItemDetails'] = {}
        self.TransDict['Notes'] = {}
        self.TransDict['Payments'] = {}
        self.trans_dict['notes']=[]
        
        enable_list = ['AcctPanel','TransactionPanel','NotePanel','TransactionButtonPanel','TransactionTotalsPanel']
                       
        element_list = ['pos_acctAddr_btn', 'pos_acctPhone_btn']
        disable_list = []
        list_of_lists = [('enable_list', enable_list),
                         ('disable_list', disable_list)]
        
        for name in element_list:
            wx.FindWindowByName(name).Enable()
            
            
        tab = wx.FindWindowByName('ActiveTab')
        trans_btn_tab = wx.FindWindowByName('TransactionButtonPanel')
        hide_list = [tab.default_options_panel, tab.default_button_panel]
        show_list = [tab.transaction_totals_panel, tab.transaction_button_panel]
        enable_list = [tab.acct_panel, tab.note_panel, tab.transaction_panel]
        
        list_of_lists = [('hide_list',hide_list),('show_list',show_list),('enable_list',enable_list)]
        for label, listd in list_of_lists:
            for panel in listd:
                if 'hide' in label:
                    panel.Hide()
                
                if 'show' in label:
                    panel.Show()
                    
                if 'enable' in label:
                    panel.Enable()
                    
                if 'disable' in label:
                    panel.Disable()
                    
        tab.Layout()
        self.Layout()
          
        #wx.FindWindowByName('acctinfo_lookupCust_btn').SetFocus()      
        wx.FindWindowByName('pos_acctNum_txtctrl').SetFocus()
        
         
        
        evttypd = str(type(event))  
        
        if re.search('(str|unicode)',evttypd,re.I) and re.match('[0-9]+',event):
            
            query = 'SELECT po_number FROM transactions WHERE transaction_id = ?'
            data = (event,)
            sql_file = 'Transactions.db'
            returnd = SQConnect(query, data, sql_file).ONE()
            wx.FindWindowByName('pos_PoTab_ponumber_txtctrl').SetCtrl( returnd[0])
            
            wx.CallAfter(trans_btn_tab.ReloadTransaction, event=event)
            
        
        
        self.Layout()
   
    
    def onBlank(self, event):
        pass
    
    def onSaleF1(self, event):
        wx.FindWindowByName('pos_ordertype_txtctrl').SetCtrl('Sale')
        

    def onReturnF2(self, event):
        wx.FindWindowByName('pos_ordertype_txtctrl').SetCtrl('Return')
        
    def onQuoteF5(self, event):
        wx.FindWindowByName('pos_ordertype_txtctrl').SetCtrl('Quote')

        
    def onTaxTypeF6(self, event):
        statuses = ['Taxable', 'Non-Taxable']
        current = HUD.MiscOps().ToggleState('pos_taxtype_txtctrl', statuses)
        self.Taxable = True
        if current != 'Taxable':
            self.Taxable = False
    

    def onPrintFormF8(self, event):
        result = wx.MessageBox('Print Last Transaction','Info', wx.YES_NO)
        if result == wx.YES:
            HUD.PrintOps().printLast()
  

    def onPaymentF10(self, event):
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
        with HUD.PaymentDialog(self, title="Payment on Account", style=style) as dlg:
            dlg.ShowModal()


    def onPayOutF12(self, event):
        pass


    def onCashDrawer(self, event):
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
        with HUD.CashDrawerDialog(self, title="Cash Drawer Info", style=style) as dlg:
            dlg.ShowModal()
        
    def onReloadTransaction(self, event):
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
        dlg = HUD.ReloadDialog(self, title="Reload Transaction", style=style)
        dlg.ShowModal()
        
        tab = wx.FindWindowByName('TransactionPanel')
        deftab = wx.FindWindowByName('DefaultButtonPanel')
        
        try:
            self.trans_id = dlg.trans_id
            wx.CallAfter(deftab.OnBeginTransaction, event=self.trans_id)
        except:
            pass
            
        dlg.Destroy()

   
    def onCustomerInquiry(self, event):
        
        acctNum = HUD.GridOps('pos_acct_grid').GetCell('Account Number',0)
        nb = wx.FindWindowByName('MainFrame_notebook')
        self.From='POS'
        nb.ChangeSelection(2)
        

    def onItemInquiry(self, event):
        
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
        ItemInq = HUD.ItemInquiryDialog(self,
                                            title="Item Inquiry",
                                            style=style)
        ItemInq.ShowModal()

        try:
            self.nextItem = ItemInq.itempick
        except:
            self.nextItem = None
        
        ItemInq.Destroy()
        
        
        gridname = 'pos_transactions_grid'
        
        tab = wx.FindWindowByName('TransactionPanel')
        if tab.nextItem is not None and tab.activeTrans is True:
            
            row = HUD.GridOps(gridname).CurGridLine(blank=True)
            
            setList = [('Item Number', self.nextItem)]
            HUD.GridOps(gridname).FillGrid(setList, row=row)
            wx.CallAfter(tab.OnClickGrid, event=gridname)
            
            #HU.GridFocusNGo(gridname,row+1)            


    def onOpenDrawer(self, event):
        pass

    def onExit(self, event):
        
        tab = wx.FindWindowByName('MainFrame_notebook')
        tab.SetSelection(6)
        tab.SetFocus()
        #wx.FindWindowByName('MainFrame_notebook').SetSelection(1)
        #wx.FindWindowByName('pos_NotesTab_notes_txtctrl').SetFocus()
        
        #item = wx.FindWindowByName('POS_frame')
        #item.Destroy()

class TransactionButtonPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        
        self.SetName('TransactionButtonPanel')
        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        tab = wx.FindWindowByName('TransactionPanel')
        lvl3_1clist = [('Repeat Last\nF&1', 'pos_repeatLast_button',
                            self.onRepeatLastF1, wx.WXK_F1),
                       ('Delete Last\nF&2', 'pos_deleteLast_button',
                            self.onDeleteLastF2, wx.WXK_F2),
                       ('Return Next\nF&3', 'pos_returnNext_button',
                           self.onReturnNextF3, wx.WXK_F3),
                       ('Item Direct\nF&4', 'pos_itemDirect_button',
                           self.onItemDirectF4, wx.WXK_F4),
                       ('Quantity\nF&5', 'pos_quantity_button',
                           self.onQuantityF5, wx.WXK_F5),
                       ('Price\nF&6', 'pos_price_button',
                           self.onPriceF6, wx.WXK_F6),
                       ('Discount\nF&7', 'pos_discount_button',
                           self.onDiscountF7, wx.WXK_F7),
                       ('Sls Change\nF&8', 'pos_slsChange_button',
                           self.onSlsChangeF8, wx.WXK_F8),
                       ('Cancel\nF&9', 'pos_cancel_button',
                           self.onCancelF9, wx.WXK_F9),
                       ('&Finish\nF10', 'pos_finish_button',
                           self.onFinishF10, wx.WXK_F10),
                       ('Coupon\nF11', 'pos_coupon_button',
                           self.onCouponF11, wx.WXK_F11),
                       ('&Customer\nInquiry', 'pos_customerInquiry_button2',
                           self.onCustomerInquiry, None),
                       ('&Item Inquiry', 'pos_itemInquiry_button',
                           self.onItemInquiry, None),
                       ('&Write Memo', 'pos_writeMemo_button',
                           self.onWriteMemo, None),
                       ('&Tax Exempt\nNext Item',
                           'pos_taxExemptNextItem_button',
                           self.onTaxExemptNextItem, None),
                       ('&Discount\nInvoice', 'pos_discountInvoice_button',
                           self.onDiscountInvoice, None)]
        
        cntcol = len(lvl3_1clist)
        if not Decimal(cntcol) % 2 == 0:
            cntcol += 1
        colnum =HUD.RetailOps().DoRound(cntcol, '1')/2
        gs = wx.GridSizer(2, int(colnum), 5,5)
        
        btn_cnt = len(lvl3_1clist)
        bar_width = 925
        num_of_levels=2
        min_buttonWidth = 50
        button_gap = 3
        buttonWidth = ButtonOps().ButtonWidth_onRow(btn_cnt,bar_width,num_of_levels,min_buttonWidth, button_gap)
        
        btn_num = 1
        idx = 0
        cnt = 0
        acceler = {}
        lvl3_1clist = ButtonOps().ListAdjustEven(lvl3_1clist)
        for label, name, hdlr, accel in lvl3_1clist:
            randomId = wx.Window.NewControlId() #wx.NewId()
            btn = wx.Button(self, id=randomId,
                            label=label,
                            name=name,
                            size=(buttonWidth, 65))
            if hdlr == '':
                btn.Bind(wx.EVT_BUTTON, self.onBlank)
            else:
                btn.Bind(wx.EVT_BUTTON, hdlr)
                if accel is not None:
                    self.Bind(wx.EVT_MENU, hdlr, id=randomId) #, id=randomId
                    acceler[idx] = wx.AcceleratorEntry(wx.ACCEL_NORMAL, accel, randomId)
                    
            gs.Add(btn, 0)
            btn_num += 1
            idx += 1
        listd = []
     
        for key ,value in acceler.items():
            listd.append(value)
        accel_tbl = wx.AcceleratorTable(listd)
        
        self.SetAcceleratorTable(accel_tbl)
        
        MainSizer.Add(gs, 0, wx.ALL|wx.EXPAND, 5)

        col2_Sizer = wx.BoxSizer(wx.VERTICAL)
        paid_list = [('Paid', 'pos_paid_txtctrl'),
                    ('Change', 'pos_change_txtctrl')]
        
        col2_Sizer.Add((wx.StaticLine(self, wx.ID_ANY,
                                             style=wx.LI_HORIZONTAL)), 0,
                                             wx.ALL | wx.EXPAND, 10)
        for label, name in paid_list:
            box = wx.StaticBox(self, -1,
                               label=label,
                               style=wx.ALIGN_CENTER)

            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            ctrl = wx.TextCtrl(self, -1,
                               name=name,
                               size=(200, -1),
                               style=wx.ALIGN_RIGHT | wx.TE_READONLY)

            ctrl.SetValue('.00')
            font = wx.Font(wx.FontInfo(18).Bold())
            ctrl.SetFont(font)
            fg_colord = 'White'
            bg_colord = 'Blue'
            if 'Change' in label:
                fg_colord = 'Red'
                bg_colord = 'White'

            ctrl.SetBackgroundColour(bg_colord)
            ctrl.SetForegroundColour(fg_colord)

            boxSizer.Add(ctrl, 0)

            col2_Sizer.Add(boxSizer, 0)
        MainSizer.Add((15,10),0)
        MainSizer.Add(col2_Sizer, 0, wx.ALL|wx.EXPAND, 5)


        self.SetSizer(MainSizer, 0)
        self.Layout()
        

    def onBlank(self, event):
        pass


    def ReloadTransaction(self, event):
        
        
        tab = wx.FindWindowByName('TransactionPanel')        
        self.transNum = event
        query = 'SELECT address_acct_num, cust_num FROM transactions WHERE transaction_id=?'
        data = (self.transNum,)
        sql_file = 'Transactions.db'
        returnd = SQConnect(query, data, sql_file).ONE()
        
        (addrAcctNum, custNum) = returnd
        
        grid_trans = wx.FindWindowByName('pos_transactions_grid')
        grid_acct = wx.FindWindowByName('pos_acct_grid')
        fillit = HUD.FillIn(grid_acct.GetName())
        
        if len(custNum) > 0:
            grid_acct.SetCellValue(0,0,custNum)
            
            grid_acct.SetCellValue(1,0,addrAcctNum)
            
        
            fillit.POSCustAcctGrid(custNum)
            fillit.POSAddrAcctGrid(custNum,addrAcctNum=addrAcctNum)
        
        fillit.POSTransGrid('pos_transactions_grid',self.transNum)
        cur = TRA.LoadDict(tab.ActiveTransactions)
        #HU.LoadDict(tab.ActiveTransactions)
        
        tab.transaction.Clear()
        cur.RefreshTransactions('pos_transactions_grid')
        tab.transaction.AddAll(tab.ActiveTransactions)
        
        row = HUD.GridOps('pos_transactions_grid').CurGridLine(blank=True)
        HUD.GridOps('pos_transaction_grid').GridFocusNGo(row)            
    
        
    def onRepeatLastF1(self, event):
        
        
    
        gridname = 'pos_transactions_grid'
        row,col = HUD.GridOps(gridname).GetGridCursor()
        grid = wx.FindWindowByName(gridname)
        if not row == 0:
            
            last_upc = grid.GetCellValue(row - 1, col)
            grid.SetCellValue(row, col, last_upc)
            grid.SetFocus()
            tab = wx.FindWindowByName('TransactionPanel')
            wx.CallAfter(tab.OnClickGrid, event=grid.GetName())
        else:
            grid.SetFocus()
        
    
    def onDeleteLastF2(self, event):
        
        gridname = 'pos_transactions_grid'
        row, col = HUD.GridOps(gridname).GetGridCursor()
        tab = wx.FindWindowByName('TransactionPanel')
                    
        last = len(tab.ActiveTransactions) - 1
        
        
        if last >= 0:
            tab.ActiveTransactions.pop(last)
            cur = HUD.Transactional(tab.ActiveTransactions).RefreshDict()
            
            cur.RefreshTransactions(gridname)
            tab.transaction.Clear()
            tab.transaction.AddAll(tab.ActiveTransactions)
            rowd = len(tab.ActiveTransactions)
            HUD.GridOps(gridname).GridFocusNGo(rowd)
        
    
    def onReturnNextF3(self, event):
        
        obj = event.GetEventObject()
        named = obj.GetName()
        tab = wx.FindWindowByName('TransactionPanel')
        tab.ReturnNext = ButtonOps().ButtonToggle(named, tab.ReturnNext)
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
        dlg = HUD.ReturnDialog(self, title="Return",
                                    size=(900, 550),
                                    style=style)

        dlg.ShowModal()
        
        try:
            picked = dlg.itemPicked
        except:
            picked = None
        
        dlg.Destroy()
        
        cnt = len(tab.returnItems)
        
        tab.returnItems[cnt]=picked
        
        gridname = 'pos_transactions_grid'
        row, col = HUD.GridOps(gridname).GetGridCursor()
        
        
        grid = wx.FindWindowByName(gridname)
        if picked is not None:
            grid.SetCellValue(row, col, tab.returnItems[cnt][1])
            grid.SetCellValue(row, col+2, tab.returnItems[cnt][2])
            wx.CallAfter(tab.OnClickGrid, event='pos_transactions_grid')
        
        HUD.GridOps(gridname).GridFocusNGo(row)
        
    
    def onItemDirectF4(self, event):
        pass    
        
    def onQuantityF5(self, event):
        
        obj = event.GetEventObject()
        named = obj.GetName()
        tab = wx.FindWindowByName('TransactionPanel')
        gridname = 'pos_transactions_grid'
        row,col = HUD.GridOps(gridname).GetGridCursor()
        
        
        tab.QuantitySet = ButtonOps().ButtonToggle(named,tab.QuantitySet)
        
        HUD.GridOps(gridname).GridFocusNGo(gridname,row)
        
        
    def onPriceF6(self, event):
        
        
        obj = event.GetEventObject()
        named = obj.GetName()
        tab = wx.FindWindowByName('TransactionPanel')
        grid = wx.FindWindowByName('pos_transactions_grid')
        rowd = len(tab.ActiveTransactions)
        tab.SetPrice = ButtonOps().ButtonToggle(named,tab.SetPrice)
        
        grid.SetReadOnly(rowd,2,False)
        HUD.GridOps(grid.GetName().GridFocusNGo(rowd))
        
        
    def onDiscountF7(self, event):
        
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
        tab = wx.FindWindowByName('TransactionPanel')
        Disc_D = HUD.DiscountDialog(self, title="Discount",
                                               size=(400, 400),
                                               style=style)

        Disc_D.ShowModal()
        Disc_D.Destroy()
        
        tab.DiscAmtOnce = Disc_D.discountamt
        gridName = 'pos_transactions_grid'
        row = HUD.GridOps(gridName).FindEmptyRow()
        HUD.GridOps(gridName).GridFocusNGo(row)

        
    def onSlsChangeF8(self, event):
        pass   
    
    def onCancelF9(self, event):
        
        
        tab = wx.FindWindowByName('TransactionPanel')
        tab.transaction.Clear()
        HUD.CurrentNotes().Clear()
        dlg = HUD.PasswordDialog('clerk')
        #dlg.Operator('clerk')
        dlg.ShowModal()
        dlg.Destroy()
        
        
        if dlg.passwordOK == True:
            self.OnCancelTransaction(event='')
        
     
    def onCouponF11(self, event):
        pass   
    
    def onItemLookupF12(self, event):
        
        
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
        tab = wx.FindWindowByName('TransactionPanel')
        ItemInq = HUD.ItemInquiryDialog(self,
                                            title="Item Inquiry",
                                            style=style)
        ItemInq.ShowModal()

        try:
            tab.nextItem = ItemInq.itempick
        except:
            tab.nextItem = None
        
        ItemInq.Destroy()
        
        
        gridname = 'pos_transactions_grid'
        
        tab = wx.FindWindowByName('TransactionPanel')
        
        if tab.nextItem is not None and tab.activeTrans is True:
            
            row = HUD.GridOps(gridname).CurGridLine(blank=True)
            
            setList = [('Item Number', tab.nextItem)]
            HUD.GridOps(gridname).FillGrid(setList, row=row)
            wx.CallAfter(tab.OnClickGrid, event=gridname)
            
            #HU.GridFocusNGo(gridname,row+1)            
        
    
    
    def onCustomerInquiry(self, event):
        
        
        acctNum = HUD.GridOps('pos_acct_grid').GetCell('Account Number',0)
            
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
        dlg = CustDialog(self,style,From='POS',CustNum=acctNum)
        
        dlg.ShowModal()

        dlg.Destroy()
    
    
    def onFinishF10(self, event):
        
        due =wx.FindWindowByName('pos_total_txtctrl').GetCtrl()
        
        
        if not due == '.00':
            a = HUD.GridOps('pos_acct_grid').GetCell('Address Account',0)
            addrNum = None
            if re.search('A[0-9]',a):
                b = re.search('A[0-9]+',a)
                addrNum = b.group(0).strip()
            
            custNum = HUD.GridOps('pos_acct_grid').GetCell('Account Number', 0)
            
            try:
                self.transNum
            except: 
                self.transNum = None
            
            style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
            transtab = wx.FindWindowByName('TransactionPanel')
            notetab = wx.FindWindowByName('NoteTab')
            self.trans_dict = {'transNum' : self.transNum, 
                               'custNum' : custNum,
                               'addrNum' : addrNum,
                               'ATs' : transtab.ActiveTransactions,
                               'due' : due,
                               'returnItems' : tab.returnItems
                              }
            
            self.TransDict['CustInfo'] = {'transNum' : self.transNum,
                                          'custNum' : custNum,
                                          'addrNum' : addrNum,
                                          'due' : due,
                                          'returnItems' : transtab.returnItems
                                          }
                                          
            self.TransDict['ItemDetails'] = {'ATs' : transtab.ActiveTransactions,
                                             'due' : due,
                                             'returnItems' : transtab.returnItems
                                            }
            
            self.TransDict['Notes'] = notetab.noteTab
                          
            #trans_dict['ATs'] = tab.ActiveTransactions
            #trans_dict['custNum'] = custNum
            #trans_dict['addrNum'] = addrNum
            #trans_dict['due'] = due
            #trans_dict['returnItems'] = tab.returnItems
            #trans_dict['transNum'] = self.transNum
            
            FinishIt_D = HUD.FinishItDialog(self,
                                        title="Transaction - Finish It",
                                        size=(1200, 670),
                                        style=style,
                                        transDict = self.trans_dict)
                                        #ATs=tab.ActiveTransactions, 
                                        #addrNum=addrNum, 
                                        #custNum=custNum, 
                                        ##due=due,
                                        #transNum=self.transNum,
                                        #returnItems=tab.returnItems)

            FinishIt_D.ShowModal()
            
            self.status = 'open'
            try:
                self.status = FinishIt_D.Status
            except:
                FinishIt_D.Destroy()
                           
            FinishIt_D.Destroy()           
            
            if self.status.lower() == 'closed':
                
                wx.CallAfter(self.OnCloseTransaction, event='')     
            
            if self.status.lower() == 'open':
                
                HUD.GridOps('pos_transactions_grid').GridFocusNGo(0)
        else:
            HUD.GridOps('pos_transaction_grid').GridFocusNGo(0)
            
            
            
    def onItemInquiry(self, event):
        
        
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
        tab = wx.FindWindowByName('TransactionPanel')
        ItemInq = HUD.ItemInquiryDialog(self,
                                            title="Item Inquiry",
                                            style=style)
        ItemInq.ShowModal()

        try:
            tab.nextItem = ItemInq.itempick
        except:
            tab.nextItem = None
        
        ItemInq.Destroy()
        
        
        gridname = 'pos_transactions_grid'
        
        if tab.nextItem is not None and tab.activeTrans is True:
            
            row = HUD.GridOps(gridname).CurGridLine(blank=True)
            
            setList = [('Item Number', tab.nextItem)]
            HUD.GridOps(gridname).FillGrid(setList, row=row)
            wx.CallAfter(tab.OnClickGrid, event=gridname)
            
            #HU.GridFocusNGo(gridname,row+1)            
        
    
    def onWriteMemo(self, event):
        
        
        wx.FindWindowByName('pos_RightPanel_notebook').SetSelection(1)
        wx.FindWindowByName('pos_NotesTab_notes_txtctrl').SetFocus()
        
        
    def onTaxExemptNextItem(self, event):
        pass    
        
    def onDiscountInvoice(self, event):
        pass
    
    def OnCancelTransaction(self, event):
        
        tab = wx.FindWindowByName('TransactionPanel')
        try:
            transNum = self.trans_id
        except:
            transNum = None
        
        if transNum is not None:
            delrec = wx.MessageBox('Delete Transaction #{0}'.format(transNum),
                                   'Delete Transaction', wx.YES_NO)
            
            if delrec == wx.YES:
                query = 'UPDATE transactions set type_of_transaction="VOID" WHERE transaction_id = ?'
                data = (transNum,)
                sql_file = 'Transactions.db'
                SQConnect(query, data, sql_file).ONE()
        
        
        wx.CallAfter(self.OnCloseTransaction, event='')            
                
    def OnCloseTransaction(self, event):   
        debug=False 
        wx.FindWindowByName('pos_RightPanel_notebook').SetSelection(0)
        wx.FindWindowByName('pos_PoTab_ponumber_txtctrl').ClearCtrl()

        disable_list = ['AcctPanel', 'TransactionPanel', 'NotePanel', 'TransactionButtonPanel', 'TransactionTotalsPanel']

        tab = wx.FindWindowByName('ActiveTab')
        
        show_list = [tab.default_options_panel, tab.default_button_panel]
        hide_list = [tab.transaction_totals_panel, tab.transaction_button_panel]
        disable_list = [tab.acct_panel, tab.note_panel, tab.transaction_panel]
        enable_list = []
        list_of_lists = [('hide_list',hide_list),('show_list',show_list),('enable_list',enable_list),('disable_list',disable_list)]
        for label, listd in list_of_lists:
            for panel in listd:
                if 'hide' in label:
                    panel.Hide()
                
                if 'show' in label:
                    panel.Show()
                    
                if 'enable' in label:
                    panel.Enable()
                
                if 'disable' in label:
                    panel.Disable()
                    
                
        
        tab.Layout()
        
                    
        totalList = ['pos_subtotal_txtctrl',
                    'pos_tax_txtctrl',
                    'pos_total_txtctrl']
        for totalName in totalList:
           wx.FindWindowByName(totalName).SetCtrl('.00')            
        for i in ['pos_acct_grid', 'pos_transactions_grid']:
            wx.FindWindowByName(i).ClearCtrl()
        
        self.Layout()

        tab = wx.FindWindowByName('TransactionPanel')
        wx.CallAfter(tab.LoadDefaults, event='')
    
        
class InventoryTab(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.SetName('InventoryTab')
        
        self.panel_one = InvStartPanel(self)



        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel_one, 1, wx.EXPAND)

        self.SetSizer(self.sizer)



        self.Layout()

class CustomersTab(wx.Panel):
    def __init__(self, *args, **kwargs):
        From = 'POS'
        CustNum = None 
        wx.Panel.__init__(self, *args, **kwargs)
        self.SetName('CustomersTab')
        
        oneSizer = wx.BoxSizer(wx.HORIZONTAL)
        txt = wx.StaticText(self, -1, label='Mode : ')
        oneSizer.Add(txt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        btn_list = [('Query','custTab_queryMode_btn',self.OnQueryMode),('Maintenance','custTab_maintMode_btn',self.OnMaintMode)]
        for label, name, hdlr in btn_list:
            ctrl = wx.Button(self, -1, label=label, name=name)
            ctrl.Bind(wx.EVT_BUTTON, hdlr)
            if 'query' in name:
                ctrl.Disable()
            
            oneSizer.Add(ctrl, 0)
        
        self.panel_one = CustStartPanel(self,From=From,CustNum=CustNum)
        
        #wx.lib.inspection.InspectionTool().Show()

 
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(oneSizer, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.sizer.Add(self.panel_one, 1, wx.EXPAND)
        
        self.SetSizer(self.sizer)

        self.Layout()


    def OnQueryMode(self, event):
        custNum = wx.FindWindowByName('custNumber_txtctrl').GetValue()
        if len(custNum) == 0:
            custNum = None
            
        self.panel_one.Destroy()
        self.panel_one = CustStartPanel(self, From='POS', CustNum=None)
        self.sizer.Add(self.panel_one,1,wx.EXPAND)
        self.Layout()
        
        self.ButtonToggle('Query')
        
    def OnMaintMode(self, event):
        dlg = HUD.PasswordDialog('clerk')
        dlg.ShowModal()
        dlg.Destroy()
        
        
        if dlg.passwordOK == True:
            custNum = wx.FindWindowByName('custNumber_txtctrl').GetValue()
            if len(custNum) == 0:
                custNum = None
                
            self.panel_one.Destroy()
            self.panel_one = CustStartPanel(self, From=None, CustNum=custNum)
            self.sizer.Add(self.panel_one,1,wx.EXPAND)
            self.Layout()
 
            self.ButtonToggle('Maintenance')
            
    def ButtonToggle(self, Mode):
        qBtn = wx.FindWindowByName('custTab_queryMode_btn')
        mBtn = wx.FindWindowByName('custTab_maintMode_btn')
        if Mode == 'Query':
            qBtn.Disable()
            mBtn.Enable()
        else:
            qBtn.Enable()
            mBtn.Disable()
                
        
 
 
        
class VendorsTab(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.SetName('VendorsTab')
        
        self.panel_one = VendStartPanel(self)
        #wx.lib.inspection.InspectionTool().Show()
        #print "VERSION : ",wx.version()
 
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel_one, 1, wx.EXPAND)
        
        self.SetSizer(self.sizer)
        
 

        self.Layout()


class MaintenanceTab(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.SetName('MaintenanceTab')
        
        self.panel_one = MaintStartPanel(self)
       
#        wx.lib.inspection.InspectionTool().Show()

 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel_one, 1, wx.EXPAND,5)
        
        self.SetSizer(sizer)
        
 

        self.Layout()


class ReportsTab(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.SetName('ReportsTab')
        
        self.panel_one = ReportStartPanel(self)
       
#        wx.lib.inspection.InspectionTool().Show()

 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel_one, 1, wx.EXPAND,5)
        
        self.SetSizer(sizer)
        
 

        self.Layout()


class AboutTab(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.SetName('AboutTab')
        
        self.panel_one = AboutStartPanel(self)
       
#        wx.lib.inspection.InspectionTool().Show()

 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel_one, 1, wx.EXPAND,5)
        
        self.SetSizer(sizer)
        
 

        self.Layout()




class ActiveTab(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.SetName('ActiveTab')
        
        self.acct_panel = AcctPanel(self)
        self.acct_panel.Disable()
        self.note_panel = NotePanel(self)
        self.note_panel.Disable()
        self.transaction_panel = TransactionPanel(self)
        self.transaction_panel.Disable()
        self.default_options_panel = DefaultOptionsPanel(self)
        self.transaction_totals_panel = HUD.TransactionTotalsPanel(self)
        self.transaction_totals_panel.Hide()
        self.default_button_panel = DefaultButtonPanel(self)
        self.transaction_button_panel = TransactionButtonPanel(self)
        self.transaction_button_panel.Hide()        
        
        self.Top_Hsizer = wx.BoxSizer(wx.HORIZONTAL)
        
        Hsizer_list = [self.acct_panel, self.note_panel]
        for sizr in Hsizer_list:
            self.Top_Hsizer.Add(sizr, 0, wx.ALL, 1)
            
        
        self.Mid_Hsizer = wx.BoxSizer(wx.HORIZONTAL)
        m_Hsizer_list = [self.transaction_panel, self.default_options_panel, self.transaction_totals_panel]
        for sizr in m_Hsizer_list:
            self.Mid_Hsizer.Add(sizr, 0, wx.ALL, 5)
        
        
        self.Vsizer = wx.BoxSizer(wx.VERTICAL)
        
        Vsizer_list = [self.default_button_panel, self.transaction_button_panel]
        self.Vsizer.Add(self.Top_Hsizer, 0, wx.EXPAND, 1)
        self.Vsizer.Add(self.Mid_Hsizer, 0, wx.EXPAND, 1)
        for sizr in Vsizer_list:
            self.Vsizer.Add(sizr, 0, wx.ALL, 1)
            
        #self.panel_two_b.Hide()
        self.SetSizer(self.Vsizer)

        self.Layout()

    


class PointofSale(wx.Frame):
    def __init__(self, size=(1225,850), debug=False):
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX) & (~wx.MINIMIZE_BOX)
        wx.Frame.__init__(self, None, -1, "RHP PoS", name='POS_Frame', size=size, style=style)
        
        #wx.lib.inspection.InspectionTool().Show()
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        Nb = wx.Notebook(self, -1, name="MainFrame_notebook")

        rsTabOne = InventoryTab(Nb)
        rsTabTwo = ActiveTab(Nb)
        rsTabThree = CustomersTab(Nb)
        rsTabFour = VendorsTab(Nb)
        rsTabFive = MaintenanceTab(Nb)
        rsTabSix = ReportsTab(Nb)
        rsTabSeven = AboutTab(Nb)
        
        Nb.AddPage(rsTabTwo, 'Point of Sale')
        Nb.AddPage(rsTabOne, 'Inventory')
        Nb.AddPage(rsTabThree, 'Customers')
        Nb.AddPage(rsTabFour, 'Vendors')
        Nb.AddPage(rsTabFive, 'Maintenance')
        Nb.AddPage(rsTabSix, 'Reports')
        Nb.AddPage(rsTabSeven, 'About')
        
        Nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.MainOnPageChanged)

        MainSizer.Add(Nb, 1, wx.ALL | wx.EXPAND, 5)
    
        self.SetSizer(MainSizer, 0)
        self.Layout()
        
        item = wx.FindWindowByName('pos_sale_button').SetFocus()    


    def MainOnPageChanged(self, event):
        
        obj = event.GetEventObject()
        named = obj.GetName()
        notebook = wx.FindWindowByName(named)
        old = notebook.GetPageText(event.GetOldSelection())
        new = notebook.GetPageText(event.GetSelection())
        
        auth_list = [('inventory','clerk'),('vendors','manager'),('maintenance','admin'),('reports','manager')]
        for section, auth in auth_list:
            if section in new.lower():
                
                dlg = HUD.PasswordDialog(auth)
                #dlg.Operator(auth)
                dlg.ShowModal()
                
                if dlg.passwordOK is False:
                    event.Veto()
                
                dlg.Destroy()
                
                return        
        
    
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = PointofSale(size=(1225, 850))
    frame.Centre()
    frame.SetName('POS_frame')
    frame.Show()
    app.MainLoop()
