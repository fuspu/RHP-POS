#!/bin/python
#
#
# Vendors 
#
#import wxversion
#wxversion.select('2.8')

import wx,re 
#import wx.calendar as cal
import wx.grid as gridlib
import sys
import time
import faulthandler
#import psycopg2
import json
from datetime import datetime
from wx.lib.masked import TimeCtrl
import wx.lib.masked as masked
from decimal import Decimal, ROUND_HALF_UP
import wx.lib.inspection
from operator import itemgetter
import handy_utils as HUD
from db_related import SQConnect, LookupDB
from button_stuff import ButtonOps


class VendorDataTab(wx.Panel):
    def __init__(self,parent, debug=False):
        """ Vendor Data """
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        
        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        col1Sizer = wx.BoxSizer(wx.VERTICAL)
        col2Sizer = wx.BoxSizer(wx.VERTICAL)
        
        level1_1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        address_box = wx.StaticBox(self, -1, label='Address')
        address_boxSizer = wx.StaticBoxSizer(address_box, wx.VERTICAL)
        
        address_list = [('Address','vendordata_addr1_txtctrl',350),('','vendordata_addr2_txtctrl',350)]
        for label,name,sized in address_list:
            ctrl = HUD.RH_TextCtrl(self, -1, name=name, size=(sized, -1))
            address_boxSizer.Add(ctrl, 0, wx.ALL, 3)
            
            
        level1_1Sizer.Add((50,50),0)
        level1_1Sizer.Add(address_boxSizer, 0,wx.ALL, 3)
            
        level2_1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        level2_1Sizer.Add((50,50),0)
        csz_list = [('vendordata_city_txtctrl',250), ('vendordata_state_txtctrl',90), ('vendordata_zipcode_txtctrl',90)]
        
        csz_box = wx.StaticBox(self, -1, label="City, State  Zipcode")
        csz_boxSizer = wx.StaticBoxSizer(csz_box, wx.HORIZONTAL)
        for name,sized in csz_list:
            if 'state_txtctrl' in name:
                ctrl = masked.TextCtrl(self, -1, name=name, mask='AA', formatcodes='S!',size=(sized, -1))
            elif 'zipcode_txtctrl' in name:
                ctrl = masked.TextCtrl(self, -1, name=name, size=(sized, -1), autoformat='USZIPPLUS4')
                         
            else:
                ctrl = HUD.RH_TextCtrl(self, -1, name=name, size=(sized, -1),style=wx.TE_PROCESS_ENTER)
                ctrl.Bind(wx.EVT_KILL_FOCUS, self.Capitals)
                    
            csz_boxSizer.Add(ctrl, 0, wx.ALL, 3)
         
        level2_1Sizer.Add(csz_boxSizer, 0)           
                
        
                 
        
        level4_1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        level4_1Sizer.Add((50,50),0)
        
        phone_list = [('Phone Number','vendordata_phonenum_txtctrl'),('Fax Number','vendordata_faxnum_txtctrl')]
        for label, name in phone_list:
            box = wx.StaticBox(self, -1, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            ctrl = masked.TextCtrl(self, -1, name=name, autoformat="USPHONEFULLEXT")
            boxSizer.Add(ctrl, 0, wx.ALL,3)
            level4_1Sizer.Add(boxSizer, 0)
            
        level5_1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        level5_1Sizer.Add((50,50),0)
        contact_box = wx.StaticBox(self, -1, label="Contact")
        contact_boxSizer = wx.StaticBoxSizer(contact_box, wx.HORIZONTAL)
        
        contact_txtctrl = HUD.RH_TextCtrl(self, -1, name='vendordata_contact_txtctrl', size=(400,50),style=wx.TE_MULTILINE)
        contact_boxSizer.Add(contact_txtctrl, 0)
        
        level5_1Sizer.Add(contact_boxSizer, 0)
        
        level6_1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        level6_1Sizer.Add((50,50),0)
        email_box = wx.StaticBox(self, -1, label="E-Mail")
        email_boxSizer = wx.StaticBoxSizer(email_box, wx.HORIZONTAL)
        email_txtctrl = masked.TextCtrl(self, -1, autoformat="EMAIL", name='vendordata_email_txtctrl')
        email_boxSizer.Add(email_txtctrl, 0)
        level6_1Sizer.Add(email_boxSizer, 0)
        
        level1_2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        multi_acct_box = wx.StaticBox(self, -1, 'Account #\'s')
        multi_acct_boxSizer = wx.StaticBoxSizer(multi_acct_box, wx.VERTICAL)
        multi_acct_listbox = wx.ListBox(self, -1, name='vendordata_acctMulti_listbox',size=(200,100),style=wx.LB_SINGLE|wx.LB_SORT)
        multi_acct_listbox.Bind(wx.EVT_LISTBOX, self.OnSelectNumber)
        
        acctAdd_txtctrl = HUD.RH_TextCtrl(self, -1, name='vendordata_acctMulti_txtctrl', size=(200,-1))
        
        addrem_boxSizer = wx.BoxSizer(wx.HORIZONTAL)
        button_list = [('Add', 'vendordata_add_button', self.OnAddAccountNumber), ('Remove','vendordata_rem_button',self.OnRemAccountNumber)]
        
        for label, name, hdlr in button_list:
            btn = HUD.RH_Button(self, -1, label=label, name=name, size=(94, -1))
            btn.Bind(wx.EVT_BUTTON, hdlr)
            if 'Remove' in label:
                btn.Disable()
            
            addrem_boxSizer.Add(btn, 0, wx.ALL|wx.EXPAND, 3)
       
        multi_acct_boxSizer.Add(acctAdd_txtctrl, 0)
        multi_acct_boxSizer.Add(addrem_boxSizer, 0)
        multi_acct_boxSizer.Add(multi_acct_listbox, 0)
        
        level1_2Sizer.Add(multi_acct_boxSizer, 0, wx.ALL|wx.EXPAND, 5)
        
        level2_2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        

        postacct_box = wx.StaticBox(self, -1, label="Post Account")
        postacct_boxSizer = wx.StaticBoxSizer(postacct_box, wx.HORIZONTAL)
        
        post_acct_txtctrl = masked.TextCtrl(self, -1, name='vendordata_postacct_txtctrl' , mask='###-###', formatcodes='Sr')
        postacct_boxSizer.Add(post_acct_txtctrl, 0,wx.ALL, 3)
        level2_2Sizer.Add(postacct_boxSizer, 0,wx.ALL,5)
        
        terms_box = wx.StaticBox(self, -1, label="Terms")
        terms_boxSizer = wx.StaticBoxSizer(terms_box, wx.HORIZONTAL)
        terms_txtctrl = HUD.RH_NumCtrl(self, -1, name='vendordata_terms_numctrl', value=0, integerWidth=4,fractionWidth=0)
        terms_boxSizer.Add(terms_txtctrl, 0, wx.ALL, 3)
        level2_2Sizer.Add(terms_boxSizer, 0,wx.ALL,5)
        
        discount_box = wx.StaticBox(self, -1, label='Discount %')
        discount_boxSizer = wx.StaticBoxSizer(discount_box, wx.HORIZONTAL)
        
        discount_txtctrl = HUD.RH_NumCtrl(self, -1, name='vendordata_discount_numctrl',value=0, integerWidth=4, fractionWidth=1)
        discount_boxSizer.Add(discount_txtctrl, 0)
        level2_2Sizer.Add(discount_boxSizer, 0, wx.ALL, 5)
        
        
        
        col1sizer_list = [(50,25),level1_1Sizer, level2_1Sizer, level4_1Sizer,level5_1Sizer, level6_1Sizer]
        
        for sizer in col1sizer_list:
            col1Sizer.Add(sizer, 0)
        
        col2sizer_list = [level1_2Sizer, level2_2Sizer]
        for sizer in col2sizer_list:
            col2Sizer.Add(sizer, 0)
            
        MainSizer.Add(col1Sizer, 0,wx.ALL, 5)
        MainSizer.Add(col2Sizer, 0,wx.ALL, 5)
        
        self.SetSizer(MainSizer, 0)
        self.Layout()
        
        
    
    def Capitals(self, event):
        """ Capitalize First Letters """
        valued = event.GetEventObject()
        raw_value = valued.GetValue()
        named = valued.GetName()
        edit_txtctrl = wx.FindWindowByName(named)
        new_value = raw_value.title()
        edit_txtctrl.ChangeValue(new_value)
    
    def OnAddAccountNumber(self, event):
        """ Add Account Number to Vendor """
        value = event.GetEventObject()
        named = value.GetName()
        addButton = wx.FindWindowByName(named)
        
        addAcctNumber_txtctrl = wx.FindWindowByName('vendordata_acctMulti_txtctrl')
        addacctnumber = addAcctNumber_txtctrl.GetValue()
        listbox = wx.FindWindowByName('vendordata_acctMulti_listbox')
        oldColor = addButton.GetBackgroundColour()
        
        if not addacctnumber:
            return
        
        total_count = listbox.GetCount()    
        has_found = listbox.FindString(addacctnumber)
        if has_found != -1:
            
            foundIndex = has_found
            listbox.EnsureVisible(foundIndex)
            addButton.SetBackgroundColour('Red')
            
        else:
            
            addButton.SetBackgroundColour('Green')
            listbox.Append(addacctnumber.upper())
            
        addAcctNumber_txtctrl.Clear()
        addAcctNumber_txtctrl.SetFocus() 
        
        allstrings = listbox.GetStrings()
        
            
        
    def OnRemAccountNumber(self, event):
        """ Remove Account Number from Vendor """
        listbox = wx.FindWindowByName('vendordata_acctMulti_listbox')
        addAcctNumber_txtctrl = wx.FindWindowByName('vendordata_acctMulti_txtctrl')
        tobe_removed = listbox.GetSelection()
        
        listbox.EnsureVisible(tobe_removed)
        listbox.Delete(tobe_removed)        
        
        addAcctNumber_txtctrl.Clear()
        addAcctNumber_txtctrl.SetFocus()
  
    def OnSelectNumber(self, event):
        
        wx.FindWindowByName('vendordata_rem_button').EnableCtrl()
            
#---------------------------

class PostAccountHelperDialog(wx.Dialog):
    def __init__(self, debug=False):
        ##super(PostAccountHelperDialog, self).__init__(self)
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        
        
        self.grid = gridlib.Grid(self, -1,size=(350,440),style=wx.BORDER_SUNKEN, name='post_account_helper_grid')
        colLabel_list = ['Major','Minor','Account Name']
        self.grid.CreateGrid(1,len(colLabel_list))
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.OnSelectAccount)
        self.grid.SetRowLabelSize(0)
        self.grid.SetColSize(2, 160)
        self.grid.EnableEditing(False)
        query = 'SELECT account_major,account_minor, account_name FROM ledger_post_accounts'
        data = ''
        returnd = SQConnect(query, data).ALL()
        
        for idx,label in enumerate(colLabel_list):
            self.grid.SetColLabelValue(idx, label) 
        
        colsnum = self.grid.GetNumberCols()
        current, new = (self.grid.GetNumberRows(), len(returnd))
               
        if new > current:
            self.grid.AppendRows(new-current)
        
        idx = 0
        for majord, minord, acctName in returnd:
            for yy in range(colsnum):
                if 'Major' in self.grid.GetColLabelValue(yy):
                    self.grid.SetCellValue(idx,yy,majord)
                if 'Minor' in self.grid.GetColLabelValue(yy):
                    self.grid.SetCellValue(idx, yy, minord)
                if 'Account Name' in self.grid.GetColLabelValue(yy):
                    self.grid.SetCellValue(idx, yy, acctName)
                            
            idx+=1
        
        pa_btn = HUD.RH_Button(self, -1, label='Cancel')
        pa_btn.Bind(wx.EVT_BUTTON, self.OnClose)
        pa_btn.SetToolTip(wx.ToolTip("Post Account Reference"))
        
        MainSizer.Add(self.grid, 0, wx.ALL|wx.CENTER, 5)
        MainSizer.Add(pa_btn, 0, wx.ALL|wx.CENTER, 5)
        
        self.SetSizer(MainSizer, 0)
        self.Layout()
    
        wx.CallAfter(self.OnLoad, event='')
        
    def OnLoad(self, event):
        query = "SELECT account_major,account_minor FROM ledger_post_accounts;"
        data = ''
        returnd = SQConnect(query, data).ALL()
        self.post_acct_list = []
        for majord,minord in returnd:
            item = "{0}-{1}".format(majord,minord)
            #print "Tup : ",tup
            self.post_acct_list.append(item) 
        
        
        
    def OnSelectAccount(self, event):
        obj = event.GetEventObject()
        name = obj.GetName()
        row = event.GetRow()
        col = event.GetCol()
        major = self.grid.GetCellValue(row, 0)
        minor = self.grid.GetCellValue(row, 1)
        self.post_acct = "{}-{}".format(major, minor)
        
        #return self.post_acct
        self.Close() 
    
    def OnClose(self, event):
        self.Close()
                
                
#------------------
class InvoiceAddDialog(wx.Dialog):
    def __init__(self, debug=False):
        ##super(InvoiceAddDialog, self).__init__(*args, **kw)
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        

        t = wx.StaticText(self, -1, label='Invoice #')
        ctrl = HUD.RH_TextCtrl(self, -1, name='invadd_invoiceNum_txtctrl', size=(290,-1),style=wx.TE_PROCESS_ENTER)
        ctrl.Bind(wx.EVT_TEXT_ENTER, self.OnClose)
        ctrl.SetFocus()
        level1Sizer.Add(t, 0, wx.ALL, 5)
        level1Sizer.Add(ctrl, 0, wx.ALL, 5)
        
        level2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        okbutton = HUD.RH_Button(self, -1, label="&OK")
        okbutton.Bind(wx.EVT_BUTTON, self.OnClose)
        
        cancelbutton = HUD.RH_Button(self, -1, label="&Cancel")
        cancelbutton.Bind(wx.EVT_BUTTON, self.OnClose)
        
        level2Sizer.Add(okbutton, 0, wx.ALL, 5)
        level2Sizer.Add((60,-1), 0)
        level2Sizer.Add(cancelbutton, 0, wx.ALL, 5)
        
        
        MainSizer.Add(level1Sizer, 0, wx.ALL|wx.CENTER, 5)
        MainSizer.Add(level2Sizer, 0, wx.ALL|wx.CENTER, 5)
        
        self.SetSizer(MainSizer, 0)
        self.Layout()  
        
        
        
    def OnClose(self, event):
        
        self.itemPicked = wx.FindWindowByName('invadd_invoiceNum_txtctrl').GetValue()
        
        self.Close()
                                 
#------------------
class VendorAddDialog(wx.Dialog):
    def __init__(self, parent, debug=False):
        #super(VendorAddDialog, self).__init__(*args, **kw)
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        

        cust_box = wx.StaticBox(self, -1, label="Vendor Number")
        cust_boxSizer = wx.StaticBoxSizer(cust_box, wx.VERTICAL)
        
        custnum_txtctrl = masked.TextCtrl(self, -1, name='vendoradd_vendornum_txtctrl',size=(160, -1),formatcodes="!")
        custnum_txtctrl.SetToolTip(wx.ToolTip('Optional: User-Define Vendor Number'))
        custnum_txtctrl.SetFocus()
        custnum_txtctrl.Bind(wx.EVT_KILL_FOCUS,self.OnVendorNumCheck)
        
        cust_boxSizer.Add(custnum_txtctrl, 0, wx.ALL|wx.EXPAND, 3)
        btn_boxSizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_list = [('Check','vendoradd_vendornumchk_button', self.OnVendorNumCheck),('Auto','vendoradd_vendornumauto_button',self.OnVendorNumAuto)]
        for label,name,handlr in btn_list:
            btn = HUD.RH_Button(self, -1, name=name, label=label)
            btn.Bind(wx.EVT_BUTTON, handlr)
                
            btn_boxSizer.Add(btn, 0)
            
        
        cust_boxSizer.Add(btn_boxSizer, 0, wx.ALL, 3)
        
        level1Sizer.Add(cust_boxSizer, 0, wx.ALL, 3)
        
        name_box = wx.StaticBox(self, -1, label="Name")
        name_boxSizer = wx.StaticBoxSizer(name_box, wx.HORIZONTAL)
        name_txtctrl = HUD.RH_TextCtrl(self, -1, name="vendoradd_name_txtctrl", size=(320, -1))
        name_boxSizer.Add(name_txtctrl, 0,wx.ALL, 3)
        
        level1Sizer.Add(name_boxSizer, 0,wx.ALL, 5)
        level2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        button_list = [('Add',self.onAddVendor),('Reset Form',self.onResetForm),('Cancel',self.onAddVendorCancel)]
        
        for label,handlr in button_list:
            button = HUD.RH_Button(self, -1, label=label)
            button.Bind(wx.EVT_BUTTON, handlr)
            
            level2Sizer.Add(button, 0,wx.ALL|wx.CENTER,5)
            
        MainSizer.Add(level1Sizer, 0)
        MainSizer.Add((40,40),0)
        MainSizer.Add(level2Sizer, 0,wx.ALL|wx.CENTER,5)
        self.SetSizer(MainSizer, 0)
        self.Layout()

    def onAddVendor(self,event):
        vendnum = wx.FindWindowByName('vendoradd_vendornum_txtctrl').GetValue()
        vendname = wx.FindWindowByName('vendoradd_name_txtctrl').GetValue()
        if not vendnum:
            
            return
        
        if not vendname:
            
            return
        
        query = "INSERT INTO vendor_basic_info (vend_num,name) VALUES ((?),(?));"
        data = (vendnum, vendname,)
        call_db = SQConnect(query, data).ONE()
        
        self.itemPicked = vendnum
        
        self.Close()
    
    
    def onResetForm(self, event):
        vendnum = wx.FindWindowByName('vendoradd_vendornum_txtctrl').Clear()
        vendname = wx.FindWindowByName('vendoradd_name_txtctrl').Clear()
        
        
    def onAddVendorCancel(self, event):
        
        self.Close() 
    
    def OnVendorNumCheck(self, event):
        check_num = wx.FindWindowByName('vendoradd_vendornum_txtctrl')
        check_numval = check_num.GetValue()
        check_btn = wx.FindWindowByName('vendoradd_vendornumchk_button')
        
        if check_numval:
            chk = VendorNumCheck(check_numval).CHECK()
            
            if chk is  not None:
                check_btn.SetBackgroundColour('Green') 
                
            else:
                check_btn.SetBackgroundColour('Red')
                check_num.SetValue('')       
    
    def OnVendorNumAuto(self, event):
        check_btn = wx.FindWindowByName('vendoradd_vendornumchk_button')
        check_num = wx.FindWindowByName('vendoradd_vendornum_txtctrl')
        check_numval = check_num.GetValue()
        auto_btn = wx.FindWindowByName('vendoradd_vendornumauto_button')
        check_btn.SetBackgroundColour(wx.NullColor)
        auto_btn.SetBackgroundColour('Green')
        chk = VendorNumCheck(check_numval).AUTO()
        
        check_num.SetValue(chk)

#------------------------
class VendorNumCheck(object):
    def __init__(self, parent, supnum, debug=False):
        
        self.supnum = supnum
               
    
    def CHECK(self):
        query = 'SELECT COUNT(*) FROM {} WHERE {}=(?)'.format('vendor_basic_info','vend_num')
        data = (self.supnum,)
        returnd = SQConnect(query,data).ONE()
        
        #returnd = HUD.QueryCheck('vendor_basic_info','vend_num',self.supnum)
        if returnd[0] == 0 and re.match('[0-9A-Za-z]+',self.supnum):
            
            new_vendnum = self.supnum
        else:
            new_vendnum = None
        
        return new_vendnum
            
    
    def AUTO(self):
        acct_vendNum = HUD.AccountOps().AcctNumAuto('vendor_basic_info','vend_num',fill0s=5)
                    
        return acct_vendNum
                         
    
class InvoicesTab(wx.Panel):
    def __init__(self,parent, debug=False):
        """ Invoices """
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        level1_list = [('Date','invoices_date_datectrl'),('Total','invoices_total_txtctrl'),('Post Date','invoices_postdate_txtctrl'),
                       ('Terms : Days','invoices_terms_txtctrl'),('Discount %','invoices_discount_txtctrl') ]
        
        for label,name in level1_list:
            text = wx.StaticText(self, -1, label=label)
            if 'Date' in label:
                if 'Post' in label:
                    ctrl = HUD.RH_MTextCtrl(self, -1, name=name, mask='##-####', formatcodes='DF')
                else:
                    ctrl = HUD.RH_DatePickerCtrl(self, -1, name=name, style=wx.adv.DP_SHOWCENTURY)
                    ctrl.SetValue(wx.DateTime.Now())
                    #ctrl = masked.TextCtrl(self, -1, name=name, mask='##/##/####', formatcodes='DF')
            else:
                if 'Terms' in label:
                    level1Sizer.Add((90,-1),0)
                    ctrl = HUD.RH_NumCtrl(self, -1, value=0, name=name, integerWidth=3, fractionWidth=0)
                if 'Discount' in label:
                    ctrl = HUD.RH_NumCtrl(self, -1, value=0, name=name, integerWidth=3, fractionWidth=1)
                if 'Total' in label:    
                    ctrl = HUD.RH_NumCtrl(self, -1, value=0, name=name, integerWidth=6, fractionWidth=2)
                    ctrl.Bind(wx.EVT_KILL_FOCUS, self.OnDoneTotal)
                    
            level1Sizer.Add(text, 0, wx.ALL, 3)
            level1Sizer.Add(ctrl, 0, wx.ALL, 3)
            
        level2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        level2_1Sizer = wx.BoxSizer(wx.VERTICAL)
        level2_2Sizer = wx.BoxSizer(wx.VERTICAL)
        
        acct_combobox = HUD.RH_ComboBox(self, -1, choices=[],name='invoices_acctNum_combobox')
        acct_combobox.Bind(wx.EVT_COMBOBOX, self.OnAcctNum)
        level2_1Sizer.Add(acct_combobox, 0)
        
        font = wx.Font(wx.FontInfo(15).Bold())
        inv_text = wx.StaticText(self, -1, label='',name='invoices_inv_text')
        inv_text.SetFont(font)
        inv_text.SetForegroundColour('BLUE')
        
        lc = HUD.RH_OLV(self, -1, name='invoices_inv_lc', size=(230, 350), style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        lc.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.SelectInvoice)
        a = HUD.ListCtrl_Ops('invoices_inv_lc')
        a.LCSetHeaders(header_list)
        lc.SetColumns([
                      ColumnDefn('Date','center',90,'dated'),
                      ColumnDefn('Invoice #','center',120,'invNum')                      
                     ])  

        
        level2_1Sizer.Add(inv_text, 0,wx.ALL|wx.EXPAND, 5)
        
        level2_1Sizer.Add(lc, 0,wx.ALL|wx.EXPAND, 5)
        
        level2Sizer.Add(level2_1Sizer, 0,wx.ALL|wx.EXPAND, 5)
        
        t1 = wx.StaticText(self, -1, label='Accounting Distributions')
        
        level2_2Sizer.Add(t1, 0, wx.ALL|wx.CENTER, 5)
        level2_2bSizer = wx.BoxSizer(wx.HORIZONTAL)
        level2_2cSizer = wx.BoxSizer(wx.VERTICAL)
        
        acctdist_grid = gridlib.Grid(self, -1, size=(415,120),style=wx.BORDER_SUNKEN, name='invoices_acctdist_grid')
        colLabel_list = [('Post Acct',120),('Amount',90),('Disc. OK',90),('Discount',90)]
        acctdist_grid.CreateGrid(1,len(colLabel_list))
        acctdist_grid.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.OnMouseLeftDown)
        acctdist_grid.SetRowLabelSize(0)
        
        right_money_list = [1,3]
        center_list = [0,2]
        for row in range(acctdist_grid.GetNumberRows()):
            for col in right_money_list:
                acctdist_grid.SetCellAlignment(row,col,wx.ALIGN_RIGHT,wx.ALIGN_RIGHT)
            for col in center_list:
                acctdist_grid.SetCellAlignment(row,col,wx.ALIGN_CENTER,wx.ALIGN_CENTER)
        
        acctdist_grid.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.OnGrid1GridCellChange)
        idx = 0
        for label,sized in colLabel_list:
            acctdist_grid.SetColLabelValue(idx, label)
            acctdist_grid.SetColSize(idx,sized)
            idx+=1
        
        level2_2bSizer.Add(acctdist_grid, 0, wx.ALL|wx.CENTER, 5)
        ctrl = wx.CheckBox(self, -1, label='Take Discount?', name='invoices_discount_checkbox')
        ctrl.Bind(wx.EVT_CHECKBOX, self.OnDiscountCheck)
        
        level2_2cSizer.Add(ctrl, 0, wx.ALL, 10)    
        ctrl = HUD.RH_Button(self, -1, label='     Reset\nDistributions', name='invoices_acctdist_reset_button')
        ctrl.Bind(wx.EVT_BUTTON, self.ResetGrid)
        
        level2_2cSizer.Add(ctrl, 0, wx.ALL, 10)
        level2_2bSizer.Add(level2_2cSizer, 0)
        
        level2_2Sizer.Add(level2_2bSizer, 0,wx.ALL|wx.CENTER, 5)
        
        
        
        pa_btn = HUD.RH_Button(self, -1, label='?')
        pa_btn.SetToolTip(wx.ToolTip("Post Account Listing"))
        pa_btn.Bind(wx.EVT_BUTTON, self.OnPostAcctButtonHelp)
        
        level2_2Sizer.Add(pa_btn, 0, wx.ALL, 5)
        
        t1 = wx.StaticText(self, -1, label='Payment Allocation')
        
        level2_2Sizer.Add(t1, 0, wx.ALL|wx.CENTER, 5)
        
        level2_2dSizer = wx.BoxSizer(wx.HORIZONTAL)
        payalloc_grid = gridlib.Grid(self, -1, size=(-1,150),style=wx.BORDER_SUNKEN, name='invoices_payalloc_grid')
        colLabel_list = [('Pay Amount',100),('Pay After',80),('Date Paid',80),('Check #',70)]
        payalloc_grid.CreateGrid(1,len(colLabel_list))
        payalloc_grid.DisableDragRowSize()
        
        payalloc_grid.SetColFormatBool(5)
        
        payalloc_grid.SetRowLabelSize(0)
        idx = 0
        for heading,sized in colLabel_list:
            payalloc_grid.SetColLabelValue(idx, heading)
            payalloc_grid.SetColSize(idx,sized)
            idx += 1 
        
        for row in range(payalloc_grid.GetNumberRows()):
            
            if col in [0]:
                payalloc_grid.SetCellAlignment(row,0,wx.ALIGN_RIGHT,wx.ALIGN_RIGHT)
            if col in [1,2,3]:
                payalloc_grid.SetCellAlignment(row,0,wx.ALIGN_CENTER,wx.ALIGN_CENTER)
                
        ctrl = HUD.RH_Button(self, -1, label='     Reset\nAllocations', name='invoices_payalloc_reset_button')
        ctrl.Bind(wx.EVT_BUTTON, self.ResetGrid)
        
        level2_2dSizer.Add(payalloc_grid, 0, wx.ALL|wx.CENTER, 5)
        level2_2dSizer.Add(ctrl, 0, wx.ALL|wx.CENTER, 5)
        
        level2_2Sizer.Add(level2_2dSizer, 0, wx.ALL|wx.CENTER, 5)
        
        level2Sizer.Add(level2_2Sizer, 0)
        
        
        MainSizer.Add(level1Sizer, 0, wx.ALL|wx.EXPAND, 5)
        MainSizer.Add(level2Sizer, 0, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(MainSizer, 0)
        self.Layout()

    def ResetGrid(self, event):
        obj = event.GetEventObject()
        name = obj.GetName()
        if 'acctdist' in name:
            gridname = 'invoices_acctdist_grid'
        if 'payalloc' in name:
            gridname = 'invoices_payalloc_grid'
        
        grid = wx.FindWindowByName(gridname)
        len1 = ['1']
        HUD.AlterGrid(grid.GetName(), len1)
        total =wx.FindWindowByName('invoices_total_txtctrl').GetCtrl()
        
        if 'acctdist' in name:
            grid.SetCellValue(0,1,str(HUD.DoRound(total, '1.00')))
        if 'payalloc' in name:
            grid.SetCellValue(0,0,str(HUD.DoRound(total, '1.00')))
        
        
    def OnDiscountCheck(self,event):
        obj = event.GetEventObject()
        val = obj.GetValue()
        grid = wx.FindWindowByName('invoices_acctdist_grid')
        terms = wx.FindWindowByName('invoices_terms_txtctrl').GetCtrl()
        
        discount =wx.FindWindowByName('invoices_discount_txtctrl').GetCtrl()        
        
        maxrows = grid.GetNumberCols()

        if val == 1:
            if terms > 0 and discount > 0:
                for row in range(maxrows):
                    grid.SetCellBackgroundColour(row, 2, 'green')
    
            #old_money = grid.GetCellValue(0,1)
            #discount =                  
        if val == 0:
            for row in range(maxrows):
                grid.SetCellBackgroundColour(row, 2, 'red')
         
        grid.Refresh()       
        
    def OnGrid1GridCellChange(self, event):
        grid = wx.FindWindowByName('invoices_acctdist_grid')
        invoice_total = wx.FindWindowByName('invoices_total_txtctrl').GetValue()
            
        Row = event.GetRow()
        Col = event.GetCol()
        
        if Col == 1:
            
            new_rem = 0
            dist_total = grid.GetCellValue(Row,Col)
            #new_total = Decimal(invoice_total)-Decimal(new_rem)
            number_of_rows = grid.GetNumberRows()
            idx = 0
                
            while idx < number_of_rows:
                
                #new_total -= Decimal(grid.GetCellValue(idx,Col))
                new_rem += Decimal(grid.GetCellValue(idx, Col))
                idx += 1
                   
            differ_total = Decimal(invoice_total)-Decimal(new_rem)
               
           # print " {0} - {1} = {2}".format(invoice_total, dist_total, differ_total)
            
            
            if differ_total > 0:
                grid.AppendRows(1)
                
                newrow = grid.GetNumberRows()-1
                grid.SetCellValue(newrow,1,str(HUD.DoRound(differ_total, '1.00')))
                grid.SetCellAlignment(newrow,1,wx.ALIGN_RIGHT,wx.ALIGN_RIGHT)
                
                #HUD.GridAlternateColor(grid.GetName(),'')        
                
       
       
        event.Skip()

        
    def OnPostAcctButtonHelp(self, event):
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
        PostAccountHelper_D = PostAccountHelperDialog(self, title="Post Account Helper Popup",size=(360,500), style=style)
        PostAccountHelper_D.ShowModal()
        
        try:
            PostAccountHelper_D.post_acct
            PostAccountHelper_D.Destroy()
        except:
            PostAccountHelper_D.Destroy()
        
        grid = wx.FindWindowByName('invoices_acctdist_grid')
        grid.SetCellValue(0,0,PostAccountHelper_D.post_acct)
        
        
        
    def SelectInvoice(self, event):
        item_id,objText = HUD.LCGetSelected(event)
        obj = event.GetEventObject()
        entry = obj.GetEntry()
        dated = entry['dated']
        invoice_num = entry['invNum']
        self.ClearInvoicePanel()
        vendor_num = wx.FindWindowByName('vendNumber_txtctrl').GetValue()
        acct_num = wx.FindWindowByName('invoices_acctNum_combobox').GetValue()
        if invoice_num:
            doit = Invoices(vendor_num,invoice_num,acct_num).Fill()
    
    def OnMouseLeftDown(self, event):
        obj = event.GetEventObject()
        row = event.GetRow()
        col = event.GetCol()
        name = obj.GetName()
        grid = wx.FindWindowByName(name)
        oldval = grid.GetCellValue(row, col)
        #print "ON Mouse Down Left"
        #acctdist_grid = wx.FindWindowByName('invoices_acctdist_grid')
        
        if col == 0:
            grid.SetCellAlignment(row, col, wx.ALIGN_CENTER, wx.ALIGN_CENTER)
            newval = oldval
            if not '-' in oldval:
                cntval = oldval[:6]
                listval = list(cntval)
                newval = '{}{}{}-{}{}{}'.format(*listval)
                
            grid.SetCellValue(row,col, newval)    
            
        if col == 1:
            oldval = grid.GetCellValue(row,col)
            
            if all(x in '0123456789.+-/' for x in oldval):
            # convert to float and limit to 2 decimals
                
                if not '.' in oldval:
                    x = len(oldval)-2
                    dol = oldval[:x]
                    cen = oldval[-2:]
                    oldval = '{}.{}'.format(dol, cen)
                    
                newval = HUD.DoRound(oldval, '1.00')
                grid.SetCellValue(row, col, str(newval))
            
            else:
                grid.SetCellValue(row,col, '')
                    
        if col == 2:                 
            if re.match('[A-Za-z]', oldval):
                grid.SetCellBackgroundColour(row,col, 'green')
            if re.match('[0-9]', oldval):   
                grid.SetCellBackgroundColour(row,col,'red')



    def OnDoneTotal(self, event):
        to_be_set = wx.FindWindowByName('invoices_total_txtctrl').GetValue()
        gridname = 'invoices_acctdist_grid'
        headerName = 'Amount'
        
        cell = GridCellSet(HUD.DoRound(to_be_set,'1.00'), 'invoices_acctdist_grid', 'Amount')
        cell = GridCellSet(HUD.DoRound(to_be_set,'1.00'), 'invoices_payalloc_grid', 'Pay Amount')  
        
    def OnAcctNum(self, event):
        """ COMBOBOX ACCT NUMBER """
        valued = event.GetEventObject()
        raw_value = valued.GetValue()       
        #print "combobox raw Value : ",raw_value
        query = "SELECT date,invoice_num FROM vendor_invoices WHERE acct_num=(?)"
        data = (raw_value,)
        returnd = SQConnect(query,data).ALL()
        lc_name = 'invoices_inv_lc'
        idx = 0
        wx.FindWindowByName(lc_name).ClearCtrl()        
        self.ClearInvoicePanel()
        for date, invNum in returnd:
            setList = [(0,date), (1, invNum)]
            HUD.LCFill(lc_name, setList, idx)
            idx += 1
    
    def ClearInvoicePanel(self):  
        clear_list = ['invoices_date_datectrl','invoices_total_txtctrl','invoices_postdate_txtctrl','invoices_terms_txtctrl','invoices_discount_txtctrl', 'invoices_acctdist_grid','invoices_payalloc_grid']
         
        for name in clear_list:
            wx.FindWindowByName(name).ClearCtrl()
            
            
 
class AcctDistrib(object):
    def __init__(self,total, debug=False):
        
        self.total = Decimal(total)
        
    def Subtract(self,amount):
        self.amount = amount
        
        self.total -= Decimal(self.amount)
        
        return self.total   
        
        
        
        
        
        
#-------------------------------------------                            
def GridCellSet(to_be_set,gridname,headerName):
    """ Grid Cell Set """
    grid = wx.FindWindowByName(gridname)
    colsnum = grid.GetNumberCols()
    rowsnum = grid.GetNumberRows()
        
        
    for xx in range(rowsnum):
        for yy in range(colsnum):
            header = grid.GetColLabelValue(yy)
            if headerName in header:
                grid.SetCellValue(xx,yy, str(to_be_set))
   
               
            
class Invoices(object):
    def __init__(self,vendor_num,invoice_num,acct_num, debug=False):
        """ Fill Invoices """
        
        self.vendor_num = vendor_num
        self.inv_num = invoice_num
        self.acct_num = acct_num
        
        
    def Fill(self):
        
        item = wx.FindWindowByName('invoices_inv_text').SetLabel(self.inv_num)
        loadList = [('invoices_date_datectrl','date', 'vendor_invoices'),
                    ('invoices_total_txtctrl','amount','vendor_invoices'),
                    ('invoices_postdate_txtctrl','post_date','vendor_invoices'),
                    ('invoices_terms_txtctrl','terms_days','vendor_invoices'),
                    ('invoices_discount_txtctrl','discount_percent','vendor_invoices'),
                    ('invoices_acctnum_combobox','acct_num', 'vendor_invoices')]
        
        
        
        dated = ""
        for name, field, table in loadList:
            query = 'SELECT {} FROM {} WHERE vend_num=(?) AND acct_num=(?) AND invoice_num=(?)'.format(field, table)
            data = (self.vendor_num,self.acct_num,self.inv_num,)
            returnd = SQConnect(query, data).ONE()
            
            if not returnd:
                continue 
                
            if 'date_datectrl' in name:
                dated = returnd[0]
                
            if 'postdate' in name:
                if not returnd[0]:
                    value = "{0}-{1}".format(str(dated.month).zfill(2),str(dated.year))
                    wx.FindWindowByName(name).SetCtrl(value)
                                
            else:
                wx.FindWindowByName(name).SetCtrl( returnd[0])
                   
    #
        saveGrid  = [('invoices_acctdist_grid', 'vendor_invoice_dist_partials',[('Post Acct','post_acct'),('Amount','amt'),('Disc. OK','disc_ok'),('Discount','disc_amt')]), 
                     ('invoices_payalloc_grid', 'vendor_invoice_partials', [('Pay Amount','pay_amount'),('Pay After', 'pay_after'),('Date Paid','date_paid'),('Check #','check_num')])]
                
        
        for gridname, table, labelnfields in saveGrid:
            actives = []
            for i in range(1,9):
                part = 'part{}_active'.format(i)
                
                query = 'SELECT {} FROM {} WHERE vend_num=(?) AND acct_num=(?) AND invoice_num=(?)'.format(part, table)
                
                data = [self.vendor_num, self.acct_num, self.inv_num,]
                
                returnd = SQConnect(query, data).ONE()
                
                if returnd is None:
                    continue
                if returnd[0] == 1:
                    actives.append(i)
                
            grid = wx.FindWindowByName(gridname)
            setList = []
            for label, name in labelnfields:
                for xi in actives:
                    part = 'part{}_{}'.format(xi, name)
                    query = 'SELECT {} FROM {} WHERE vend_num=(?) AND acct_num=(?) AND invoice_num=(?)'.format(part, table)
                    data = [self.vendor_num, self.acct_num, self.inv_num,]
                    returnd = SQConnect(query, data).ONE()
                    setList += [(label,str(returnd[0]))]
                    
            
            
            
            for xx in actives:
                HUD.FillGrid(gridname, setList, xx-1)
            
            
class NotesTab(wx.Panel):
    def __init__(self,parent, debug=False):
        """ Notes """
        
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)


class StartPanel(wx.Panel):
    def __init__(self,parent, debug=False):
        
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        lookupSizer = wx.BoxSizer(wx.VERTICAL)
        
         
        IconBar_list =[('FindButton', ButtonOps().Icons('find'), self.OnFind),
                       ('SaveButton', ButtonOps().Icons('save'), self.OnSave),
                       ('UndoButton', ButtonOps().Icons('undo'),self.OnUndo),
                       ('AddButton', ButtonOps().Icons('add'), self.OnAdd),
                       ('DeleteButton', ButtonOps().Icons('delete'), self.OnDelete),
                       ('PrintCheck', ButtonOps().Icons('print'), self.OnPrintCheck),
                       ('ExitButton', ButtonOps().Icons('exit'), self.OnExitButton)]
        
        IconBox = wx.StaticBox(self, label='')
        
        IconBarSizer = wx.StaticBoxSizer(IconBox, wx.HORIZONTAL)        
        xx = 0        
        for name,iconloc,handler in IconBar_list:
            icon = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(iconloc), name=name, style=wx.BORDER_NONE)
            icon.Bind(wx.EVT_BUTTON, handler)
            IconBarSizer.Add((80,1),0)
            if re.match('(Save|Delete|Undo|PrintCheck)', name): #'Save' in name or 'Delete' in name or 'Undo' in name or 'Add' in name:
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
        lookupSizer.Add((10,10), 0)    
        

        level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        cust_num_box = wx.StaticBox(self, label="Vendor Number")
        cust_num_BoxSizer = wx.StaticBoxSizer(cust_num_box, wx.HORIZONTAL)
        self.custNumber = HUD.RH_TextCtrl(self, -1, name="vendNumber_txtctrl", size=(240, -1), style=wx.TE_PROCESS_ENTER)
        self.custNumber.SetFocus()
        self.custNumber.Bind(wx.EVT_TEXT_ENTER, self.OnLoad)
        cust_num_BoxSizer.Add(self.custNumber, 0)
        
        level1Sizer.Add(cust_num_BoxSizer, 0)
        
        cust_name_box = wx.StaticBox(self, label="Vendor Name")
        cust_name_BoxSizer = wx.StaticBoxSizer(cust_name_box, wx.HORIZONTAL)     
        self.custName = HUD.RH_TextCtrl(self, -1, name="vendName_txtctrl", size=(360,-1))
        cust_name_BoxSizer.Add(self.custName, 0)
        
        level1Sizer.Add(cust_name_BoxSizer, 0)
        
        deactivated_cb = wx.CheckBox(self, label="Deactivated", name="deactivated_cb1")
        level1Sizer.Add(deactivated_cb, 0, wx.ALL|wx.ALIGN_CENTER)
        
        level2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        #panel = wx.Panel(self)
        self.notebook = wx.Notebook(self, wx.ID_ANY, name='the_notebook')
        tabOne = VendorDataTab(self.notebook)
        tabTwo = InvoicesTab(self.notebook)
        tabThree = NotesTab(self.notebook)
        
        self.notebook.AddPage(tabOne, "Vendor Data")
        self.notebook.AddPage(tabTwo, "Invoices")
        self.notebook.AddPage(tabThree, "Notes")
        
        #self.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)
        self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        level2Sizer.Add(self.notebook, 1, wx.ALL|wx.EXPAND, 5)
        
        lookupSizer.Add(IconBarSizer, 0, flag=wx.ALL|wx.EXPAND)

        lookupSizer.Add(level1Sizer, 0)
        lookupSizer.Add(level2Sizer, 0, wx.ALL|wx.EXPAND, 5)
        
        self.SetSizer(lookupSizer, 0)
        
        self.Layout()

        
    def OnPageChanged(self, event):
        old = self.notebook.GetPageText(event.GetOldSelection())
        new = self.notebook.GetPageText(event.GetSelection())
        here = wx.FindWindowByName('the_notebook')
        now = here.GetPageText(here.GetSelection())
        
        
        #if new == 1:

        #else:
            
                
        
        event.Skip()

    def OnFind(self,event):
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
        VendorFind_D =  HUD.VendorFindDialog(self, title="Vendor Lookup", style=style, vendorNum=None)
        VendorFind_D.ShowModal()
        
        try:
            VendorFind_D.itemPicked
        except:
            VendorFind_D.Destroy()
            return
        
        self.vendPicked = VendorFind_D.itemPicked
        
        VendorFind_D.Destroy()
        
        item = wx.FindWindowByName('vendNumber_txtctrl').SetValue(self.vendPicked)
        
        wx.CallAfter(self.OnLoad, event=self.vendPicked)    
    
    def OnSave(self, event):
        """ ON Save """
        vendorNum = wx.FindWindowByName('vendNumber_txtctrl').GetValue()
        HUD.CheckEntryExist('vend_num',vendorNum, ['vendor_basic_info', 'vendor_invoice_dist_partials','vendor_invoice_partials', 'vendor_invoices'])
        here = wx.FindWindowByName('the_notebook')
        now = here.GetPageText(here.GetSelection())
        
        if 'Vendor Data' in now:
            save_list = [('vendName_txtctrl','name'),('vendordata_addr1_txtctrl','address1'),('vendordata_addr2_txtctrl','address2'),
                         ('vendordata_city_txtctrl','city'),('vendordata_state_txtctrl','state'),('vendordata_zipcode_txtctrl','zip'),
                         ('vendordata_acctMulti_listbox','acct_num'),('vendordata_postacct_txtctrl','post_acct'),
                         ('vendordata_terms_numctrl','terms_days'),('vendordata_discount_numctrl','discount_percent'),
                         ('vendordata_contact_txtctrl','contact'),('vendordata_phonenum_txtctrl','phone'),
                         ('vendordata_faxnum_txtctrl','fax'),('vendordata_email_txtctrl','email')]
        
            for name,field in save_list:
                value =wx.FindWindowByName(name).GetCtrl()
                query = 'UPDATE vendor_basic_info SET {0}=(?) WHERE vend_num=(?)'.format(field)
                data = (value,vendorNum,)
                returnd = SQConnect(query,data).ONE()    
                
            
            
        if 'Invoices' in now:
            
            save_list = [('invoices_date_datectrl', 'vendor_invoices', 'date'),
                         ('invoices_total_txtctrl', 'vendor_invoices','amount'),
                         ('invoices_postdate_txtctrl', 'vendor_invoices','post_date'),
                         ('invoices_terms_txtctrl', 'vendor_invoices','terms_days'),
                         ('invoices_discount_txtctrl', 'vendor_invoices','discount_percent'),
                         ('vendNumber_txtctrl', 'vendor_invoices', 'vend_num'),
                         ('invoices_acctNum_combobox', 'vendor_invoices', 'acct_num')]
            
            inv_num = wx.FindWindowByName('invoices_inv_text').GetLabel()
            acctNum = wx.FindWindowByName('invoices_acctNum_combobox').GetValue()
            tryit = wx.FindWindowByName('invoices_total_txtctrl').GetValue()
            
            
            
            
            fieldSet, dataSet, table = HUD.Commaize(save_list)

            if len(dataSet) > 0:
                query = '''UPDATE {} 
                           SET {}
                           WHERE invoice_num=(?) AND acct_num=(?) AND vend_num=(?)'''.format(table,fieldSet)

                data = dataSet + [inv_num,acctNum,vendorNum,]
                call_db = SQConnect(query, data).ONE()
                
                

            setup_list = ['vendor_invoice_dist_partials', 'vendor_invoice_partials']
            for table in setup_list:
                query = 'SELECT invoice_num FROM {} WHERE vend_num=(?)'.format(table)
                data = [vendorNum,]
                returnd = SQConnect(query, data).ONE()
                
                if not returnd[0] or returnd[0] is None:
                    query = 'UPDATE {} SET {}=(?),{}=(?) WHERE vend_num=(?)'.format(table, 'invoice_num', 'acct_num')
                    data = [inv_num, acctNum, vendorNum,]
                    returnd = SQConnect(query,data).ONE()
                    
            
            saveGrid  = [('invoices_acctdist_grid', 'vendor_invoice_dist_partials',[('Post Acct','post_acct'),('Amount','amt'),('Disc. OK','disc_ok'),('Discount','disc_amt')]), 
                         ('invoices_payalloc_grid', 'vendor_invoice_partials', [('Pay Amount','pay_amount'),('Pay After', 'pay_after'),('Date Paid','date_paid'),('Check #','check_num')])]
            
            
            for gridname, table, labelnfields in saveGrid:
                gridDist = {}
                idx = 0
                setList = []
                rowActive = 1
                skip = False
                grid = wx.FindWindowByName(gridname)
                
                for label, fields in labelnfields:
                    
                    for xx in range(grid.GetNumberRows()):
                        for yy in range(grid.GetNumberCols()):
                            col_label = grid.GetColLabelValue(yy)
                            
                            if label in col_label:
                                val = grid.GetCellValue(xx,yy)
                                if re.search('Amount', label, re.I):
                                    if val == '' or val == None:
                                        
                                        skip = True
                                    else:
                                           
                                        skip = False
                                        
                                if skip == False:
                                    part = 'part{}_{}'.format(xx+1, fields)
                                    
                                    setList += [(table, part, val)]
                                    if xx > 0:
                                        rowActive += 1
                            



                            
                
                
                for table, field, value in setList:
                    query = 'UPDATE {} SET {}=(?) WHERE invoice_num=(?) AND acct_num=(?) AND vend_num=(?)'.format(table, field)
                    
                    data = [value, inv_num, acctNum, vendorNum,]
                    
                    returnd = SQConnect(query, data).ONE()
                

                for table, field, value in setList:
                    part = 'part{}_active'.format(rowActive)
                    query = 'UPDATE {} SET {}=1 WHERE invoice_num=(?) AND acct_num=(?) AND vend_num=(?)'.format(table, part)
                    data = [inv_num, acctNum, vendorNum,]
                
    
    def OnAdd(self, event):
        here = wx.FindWindowByName('the_notebook')
        now = here.GetPageText(here.GetSelection())
        if 'Vendor Data' in now: 
            style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
            VendorAdd_D = VendorAddDialog(self, title="Add Vendor", size=(550,180), style=style)
            VendorAdd_D.ShowModal()
        
            try:
                VendorAdd_D.itemPicked
            except:
                VendorAdd_D.Destroy()
                return
        
            self.vendPicked = VendorAdd_D.itemPicked
            item = wx.FindWindowByName('vendNumber_txtctrl').SetValue(self.vendPicked)
        
            wx.CallAfter(self.OnLoad, event=self.vendPicked)
        if 'Invoices' in now:
                
            style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
            InvoiceAdd_D = InvoiceAddDialog(self, title="Add Invoice",size=(400,90), style=style)
            InvoiceAdd_D.ShowModal()
        
            try:
                InvoiceAdd_D.itemPicked
            except:
                InvoiceAdd_D.Destroy()
                return
        
            self.invoicePicked = InvoiceAdd_D.itemPicked
            
            item = wx.FindWindowByName('invoices_date_datectrl').SetFocus()
            
            now = datetime.now()
            now_post_date = "{0}-{1}".format(str(now.month).zfill(2),now.year)
            fill_list = [('invoices_inv_text',self.invoicePicked),('invoices_postdate_txtctrl',now_post_date)]
            for name, value in fill_list:
                wx.FindWindowByName(name).SetCtrl( value)
            
            
                             
            todo_list = [('vendordata_terms_numctrl','invoices_terms_numctrl'),('vendordata_discount_numctrl','invoices_discount_numctrl')]
            for get, put in todo_list:
                value =wx.FindWindowByName(get).GetCtrl()
                wx.FindWindowByName(put).SetCtrl( value)
                
            HUD.CheckEntryExist('invoice_num',self.invoicePicked.upper().strip(), ['vendor_invoices'])
            
            
                
            #terms_day = wx.FindWindowByName('vendordata_terms_numctrl').GetValue()
            #item = wx.FindWindowByName('invoices_terms_numctrl').SetValue(terms_day)
            #discount = wx.FindWindowByName('vendordata_discount_numctrl').GetValue()
            #item = wx.FindWindowByName('invoices_discount_numctrl').SetValue(discount)
                            
    def OnLoad(self, event):
        
        
        
        to_clear_list = ['invoices_inv_lc','invoices_acctdist_grid','invoices_payalloc_grid','invoices_acctNum_combobox','invoices_inv_text']
        for name in to_clear_list:
            wx.FindWindowByName(name).ClearCtrl()
            
            
        vendNumber = wx.FindWindowByName('vendNumber_txtctrl').GetCtrl()
        
        if not vendNumber:
            return
        
        button_list = ['SaveButton','AddButton','UndoButton','DeleteButton','PrintCheck']
        for name in button_list:
            button = wx.FindWindowByName(name).Enable()
            
        
             
        load_list = [('vendName_txtctrl','name'),('vendordata_addr1_txtctrl','address1'),
                     ('vendordata_addr2_txtctrl','address2'),('vendordata_city_txtctrl','city'),
                     ('vendordata_state_txtctrl','state'),('vendordata_zipcode_txtctrl','zip'),
                     ('vendordata_postacct_txtctrl','post_acct'),('vendordata_faxnum_txtctrl','fax'),('vendordata_phonenum_txtctrl','phone'),
                     ('vendordata_email_txtctrl','email'),('vendordata_terms_numctrl','terms_days'),
                     ('vendordata_discount_numctrl','discount_percent'),('vendordata_contact_txtctrl','contact'),
                     ('vendordata_acctMulti_listbox','acct_num')]
        
        for name, field in load_list:
            query = "SELECT {0} FROM vendor_basic_info WHERE vend_num=(?)".format(field)
            data = (vendNumber,)
            returnd = SQConnect(query,data).ONE()
            if returnd is None or len(returnd) == 0:
                return
            
                
            wx.FindWindowByName(name).ClearCtrl()
            wx.FindWindowByName(name).SetCtrl(returnd[0])

            if 'acctMulti_listbox' in name:
                if returnd[0]:
                    acct_listing = json.loads(returnd[0])
                    inv_combobox = wx.FindWindowByName('invoices_acctNum_combobox')
                    inv_combobox.SetItems(acct_listing)
                    inv_combobox.SetSelection(0)
         
                    acct_wanted = inv_combobox.GetStringSelection()
            
                    query = "SELECT date,invoice_num FROM vendor_invoices WHERE acct_num=(?)"
                    data = (acct_wanted,)
                    returnd = SQConnect(query, data).ALL()
                    
                    idx = 0
                    lc_name = 'invoices_inv_lc'
                    for dated, invd in returnd:
                        if idx == 0:
                            inv_num = invd
                            
                        setList = [(0,dated),(1,invd)]
                        HUD.LCFill(lc_name, setList, idx)
                        idx += 1
                        
                                     
                    vendor_num = wx.FindWindowByName('vendNumber_txtctrl').GetValue()
                    acct_num = wx.FindWindowByName('invoices_acctNum_combobox').GetValue()
                    
                    lc = wx.FindWindowByName(lc_name)
                    invoice_num = inv_num
                    
                        
                    doit = Invoices(vendor_num,invoice_num,acct_num).Fill()
                
                
                    
        
        
        
        
    def OnUndo(self, event):
        wx.CallAfter(self.OnLoad, event=None)
    
    def OnDelete(self, event):
        pass
    
    def OnPrintCheck(self, event):
        vendorNum =wx.FindWindowByName('vendNumber_txtctrl').GetCtrl()
        acct_num = wx.FindWindowByName('invoices_acctNum_combobox').GetValue()
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
        PrintCheck_D = PrintCheckDialog(self, title="Check Writing",size=(800,500), style=style, vendorNum=vendorNum, acctNum=acct_num)
        PrintCheck_D.ShowModal()
        
        try:
            PrintCheck_D.differList
            
        except:
            PrintCheck_D.Destroy()
        
        self.differList = PrintCheck_D.differList
        
        
        PrintCheck_D.Destroy()
    
        
        
    
    
    
            
    def OnExitButton(self, event):
        item = wx.FindWindowByName('Vendor_Frame').Close()
        #self.Parent.Close()
    
    
#------------------------------------------------------------------------------
class PrintCheckDialog(wx.Dialog):
    def __init__(self, parent, title, size, style, vendorNum, acctNum, debug=False):
        #super(PrintCheckDialog, self).__init__(parent=parent, title=title, size=size, style=style)
        
        self.vendorNum = vendorNum
        self.acctNum = acctNum
        query = 'SELECT invoice_num FROM vendor_invoices WHERE vend_num=(?) AND acct_num=(?)'
        data = [self.vendorNum, self.acctNum,]
        returnd = SQConnect(query,data).ALL()
        if not returnd:
            wx.MessageBox('No Invoices Found', 'Info Box', wx.OK)
            self.Close()
        
        
        self.inv_list = returnd
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        
        btn = HUD.RH_Button(self, -1, label='Write Check', name='checkdialog_writecheck_button')
        btn.Bind(wx.EVT_BUTTON, self.WriteCheck)
        MainSizer.Add(btn, 0, wx.ALL|wx.ALIGN_RIGHT, 50)
                
        box = wx.StaticBox(self, -1, label='Check Number')
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        
        ctrl = HUD.RH_TextCtrl(self, -1, name='checkdialog_checknum_txtctrl', size=(150,-1))
        boxSizer.Add(ctrl, 0)
        
        MainSizer.Add(boxSizer, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        MainSizer.Add((50,50), 0)
        
        grid = gridlib.Grid(self, -1, 
                            style=wx.BORDER_SUNKEN, 
                            pos=(0,0), 
                            name="checkdialog_check_grid")
        
        invs = len(self.inv_list)
        collabel_list = ['Date', 'Invoice #', 'Amount','Yet Paid','Pay Amt']
        grid.CreateGrid(invs, len(collabel_list))
        grid.SetDefaultCellAlignment(wx.ALIGN_CENTRE,wx.ALIGN_CENTRE)
        grid.SetRowLabelAlignment(wx.LEFT, wx.ALIGN_CENTRE)
        grid.SetLabelFont( wx.Font(wx.FontInfo(9)) )
        grid.SetRowLabelSize(0)
        grid.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.GridChanged)
        
        for idx, label in enumerate(collabel_list):
            grid.SetColLabelValue(idx, label)
        
        for row in range(grid.GetNumberRows()):
            for col in range(grid.GetNumberCols()):
                if col in [0,1,2,3]:
                    grid.SetReadOnly(row,col, True)
                    
        
        MainSizer.Add(grid, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        
        
        btn = HUD.RH_Button(self, -1, label='Close', name='checkdialog_close_button')
        btn.Bind(wx.EVT_BUTTON, self.CloseButton)
        
        MainSizer.Add(btn, 0, wx.ALL|wx.ALIGN_CENTER, 50)
        
        
        self.SetSizer(MainSizer)
        self.Layout()

        wx.CallAfter(self.OnLoad, event='')
            
    def OnLoad(self, event):
        
        gridname = 'checkdialog_check_grid'
        idx = 0
        for inv in self.inv_list:
            query = 'SELECT date, invoice_num, amount FROM vendor_invoices WHERE vend_num=(?) AND acct_num=(?) AND invoice_num=(?)'
            data = [self.vendorNum, self.acctNum, inv,]
            returnd = SQConnect(query, data).ONE()
            
            (dated, invd, amtd) = returnd
            
            setList = [('Date',dated),('Invoice #',invd),('Amount',amtd),('Yet Paid',amtd),('Pay Amt',amtd)]
            HUD.FillGrid(gridname, setList, idx)
                    
            idx += 1        

        HUD.GridAlternateColor(gridname,self.inv_list)
     
    def GridChanged(self, event):
        obj = event.GetEventObject()
        name = obj.GetName()
        
        row = event.GetRow()
        col = event.GetCol()
        
        grid = wx.FindWindowByName(name)
        
        colname = grid.GetColLabelValue(col)
        full_amt = grid.GetCellValue(row, 2)
        
        if colname == 'Pay Amt':
            gonna_pay = grid.GetCellValue(row, col)
            differ = Decimal(full_amt)-Decimal(gonna_pay)
            if differ < 0:
                grid.SetCellValue(row, 4, str(HUD.DoRound(full_amt, '1.00')))
                differ = 0
            else:
                grid.SetCellValue(row, 4, str(HUD.DoRound(gonna_pay, '1.00')))

            grid.SetCellValue(row, 3, str(HUD.DoRound(differ, '1.00')))
        
        

    def CloseButton(self, event):
        self.Close()
    
    def WriteCheck(self, event):
        
        self.differList = [] 
        chk_num =wx.FindWindowByName('checkdialog_checknum_txtctrl').GetCtrl()
        dated = datetime.today().date()
        
        grid = wx.FindWindowByName('checkdialog_check_grid')
        
        for xx in range(grid.GetNumberRows()):
            inv_num = grid.GetCellValue(xx, 1)
            differ_amt = grid.GetCellValue(xx,3)
            self.differList += [(inv_num, differ_amt, chk_num, dated)]
            
        
        self.PrintCheck
        
        self.Close()
        
    def PrintCheck(self, event):
        pass
#------------------------------------------------------------------------------

class CustomerScreen(wx.Frame):
    def __init__(self, debug=False):
        style = wx.DEFAULT_FRAME_STYLE & (~wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX) & (~wx.MINIMIZE_BOX)
        wx.Frame.__init__(self, None, -1, "RHP Vendor Management", size=(1200,800), style=style)
        
        self.panel_one = StartPanel(self)
        #wx.lib.inspection.InspectionTool().Show()
        #print "VERSION : ",wx.version()
 
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel_one, 1, wx.EXPAND)
        
        self.SetSizer(self.sizer)
        
 

        self.Layout()

       
  
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = CustomerScreen()
    frame.Centre()
    frame.SetName('Vendor_Frame')
    frame.Show()
    app.MainLoop()        
