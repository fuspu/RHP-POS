#!/usr/bin/python3
#
#
#
# Customers
#
#import wxversion
#wxversion.select('2.8')

import wx,re,os
#import wx.animate
#import wx.calendar as cal
import wx.grid as gridlib
import sys
import faulthandler
#import psycopg2
import json
import queue
import pout
import time
from ObjectListView import ObjectListView,ColumnDefn
import xml.etree.cElementTree as ET
from datetime import datetime, timedelta
from wx.lib.masked import TimeCtrl
import wx.lib.masked as masked
from decimal import Decimal, ROUND_HALF_UP
import wx.lib.inspection
import handy_utils as HUD
from operator import itemgetter
from db_related import LookupDB, SQConnect
from button_stuff import ButtonOps
#import sqlite3

class CustomerDataTab(wx.Panel):
    def __init__(self, *args, **kwargs): 
        """ Customer Data Tab """    
        kwargs['size'] = (500,500)
        wx.Panel.__init__(self, *args, **kwargs)
        
        self.SetName('CustomerDataTab')
        
        self.lsl = HUD.LoadSaveList()

        MainSizer = wx.BoxSizer(wx.VERTICAL)
        
        level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        col1Sizer = wx.BoxSizer(wx.VERTICAL)
        col2Sizer = wx.BoxSizer(wx.VERTICAL)
        
        level2_1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        level3_1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        level4_1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        level5_1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        level6_1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        level7_1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        level8_1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        level2_2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        lvl1_list = [('Prefix','custdata_prefix_btn',70,'customer_basic_info','prefix'),
                     ('First Name/Business Name','custdata_fname_txtctrl', 240,'customer_basic_info','first_name'),
                     ('Initial','custdata_midInitial_txtctrl',50,'customer_basic_info','middle_initial'),
                     ('Last Name','custdata_lname_txtctrl',160,'customer_basic_info','last_name'),
                     ('Suffix','custdata_suffix_txtctrl',60,'customer_basic_info','suffix')]
        
        for label, named, sized, tableName, fieldName  in lvl1_list:
            box = wx.StaticBox(self, -1, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            print("Level1 : {0} : {1} : {2}".format(label,named,sized ))
            if 'btn' in named:
                print(("ComboBox Ctrl ",named))
                ctrl = HUD.RH_Button(self, -1, name=named)
                ctrl.listd = ['Mr.','Mrs.','Ms.','Dr.']
                ctrl.tableName = tableName
                ctrl.fieldName = fieldName
            
            if 'txtctrl' in named:
                print(("TextCtrl ",named))
                ctrl = HUD.RH_TextCtrl(self, -1, 
                                   name=named, 
                                   size=(sized,-1))

                ctrl.tableName = tableName
                ctrl.fieldName = fieldName
                ctrl.Bind(wx.EVT_KILL_FOCUS, HUD.EventOps().Capitals)
                ctrl.Bind(wx.EVT_KILL_FOCUS, self.AddAll)
            ctrl.Disable()
            boxSizer.Add(ctrl, 0, wx.ALL, 3)
            
            self.lsl.Add(named)
            level1Sizer.Add(boxSizer, 0)
        
        basePath = os.path.dirname(os.path.realpath(__file__))+'/' 
        iconloc = ButtonOps().Icons('refresh')
        
        box = wx.StaticBox(self, -1, label='Address')
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        aa = '{0}\n'.format(' '*90)
        
        txt = wx.StaticText(self, -1, 
                            label=aa+aa+aa+aa,
                            name='custdata_addressText_text')
        self.lsl.Add('custdata_addressText_text')
        
        boxSizer.Add(txt, 0, wx.ALL, 3)
        level2_1Sizer.Add(boxSizer,0, wx.ALL, 3)    
        
        level2_1bSizer = wx.BoxSizer(wx.VERTICAL)
        ctrl = HUD.RH_TextCtrl(self, -1, 
                               name="custdata_addr_acct_num_txtctrl1", 
                               size=(130,-1), 
                               style=wx.TE_READONLY|wx.TE_CENTER)
        self.lsl.Add("custdata_addr_acct_num_txtctrl1")
        ctrl.tableName = 'customer_basic_info'
        ctrl.fieldName = 'address_acct_num'
        level2_1bSizer.Add((10,10),0)
        level2_1bSizer.Add(ctrl, 0, wx.ALL|wx.ALIGN_CENTER, 3)
        
        btn = wx.Button(self, -1, 
                        label="     Change\nMain Address", 
                        name="Change Main Address Button")
        
        btn.Bind(wx.EVT_BUTTON, self.OnChangeMainAddress)
        btn.Disable()
        level2_1bSizer.Add(btn, 0, wx.ALL|wx.ALIGN_CENTER, 3)
        
        level2_1Sizer.Add(level2_1bSizer, 0, wx.ALL,3)
            
        f_box = wx.StaticBox(self, -1, label="Phone Numbers")
        f_boxSizer = wx.StaticBoxSizer(f_box, wx.VERTICAL)
        
        f_add_boxSizer = wx.BoxSizer(wx.HORIZONTAL)
        ftyp_list = ['HOME','CELL','WORK','FAX',
                     'CONTACT1','CONTACT2','CONTACT3']
        cbox = HUD.RH_Button(self, -1, name="custdata_phonetype_btn")
        cbox.listd = ftyp_list                   
        f_add_boxSizer.Add(cbox, 0)

        ctrl = HUD.RH_MTextCtrl(self, -1, 
                                mask='(###) ###-####',
                                validRegex = "^\(\d{3}\) \d{3}-\d{4}", 
                                size=(160, -1), 
                                name='custdata_addphone_txtctrl')
        
        f_add_boxSizer.Add(ctrl, 0, wx.ALL, 3)

        ctrl = wx.Button(self, label='+')
        ctrl.Bind(wx.EVT_BUTTON, self.AddPhoneNumber)
        f_add_boxSizer.Add(ctrl, 0)


        f_boxSizer.Add(f_add_boxSizer, 0)
        
        lc = HUD.RH_OLV(self, name='custdata_phone_olv', style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        lc.SetColumns([ColumnDefn('Type','center',120,'typd'),
                       ColumnDefn('Phone #','center',150,'number')])

        self.lsl.Add('custdata_phone_olv')
        f_boxSizer.Add(lc, 0)
            
        #level2_2Sizer.Add(lc, 0)
        level2_2Sizer.Add(f_boxSizer, 0)
        
        acct_type_choices = ['Mailing List','Balance Forward','C.O.D']
        
        level4_1_list = [('Alt Post Acct','custdata_alt_post_acct_txtctrl',70,'customer_basic_info','alt_post_acct'),
                         ('Account Type','custdata_acct_type_btn',0,'customer_basic_info','account_type')]
        
        for label, name, sized, tableName, fieldName in level4_1_list:
            txt = wx.StaticText(self, -1, label=label)
            if 'alt_post' in name:
                ctrl = HUD.RH_MTextCtrl(self, -1, 
                                        name=name, 
                                        mask = '###-###', 
                                        validRegex = '\d{3}-\d{3}', 
                                        size = (sized,-1), 
                                        style = wx.TE_READONLY)
                
                
            else:
                if 'btn' in name:
                    ctrl = HUD.RH_Button(self, -1, name=name)
                    ctrl.DefaultField = 'account_type'
                    ctrl.DefaultTable = 'organizations'
                    ctrl.Disable()
                    
            self.lsl.Add(name)
            ctrl.tableName = tableName
            ctrl.fieldName = fieldName
            
            level4_1Sizer.Add(txt, 0, wx.ALL|wx.ALIGN_CENTER, 3)
            level4_1Sizer.Add(ctrl, 0, wx.ALL|wx.ALIGN_CENTER, 3)
            
            
        level6_1_list = [("E-Mail   ",'custdata_email_txtctrl1','EMAIL', 'customer_basic_info','email_addr')]
        for label, name, sized, tableName, fieldName in level6_1_list:
            txt = wx.StaticText(self, -1, label=label)
            if 'email' in name: 
                ctrl = HUD.RH_MTextCtrl(self, -1, 
                                        name = name,
                                        autoformat = sized, 
                                        style = wx.TE_READONLY)
            else:
                ctrl = HUD.RH_TextCtrl(self, -1, 
                                       name = name,
                                       size = (sized,-1), 
                                       style = wx.TE_READONLY)
            
            ctrl.tableName = tableName
            ctrl.fieldName = fieldName

            level6_1Sizer.Add(txt, 0,wx.ALL|wx.ALIGN_CENTER, 3)
            level6_1Sizer.Add(ctrl, 0,wx.ALL|wx.ALIGN_CENTER, 3)
            if not 'taxExempt' in name:
                level6_1Sizer.Add((20,1), 0)
            self.lsl.Add(name)

        level7_1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        lvl7_list = [('Contact 1', 'custdata_contact1_txtctrl','customer_basic_info','contact1'), 
                     ('Contact 2', 'custdata_contact2_txtctrl','customer_basic_info','contact2')]
        
        for label, name, tableName, fieldName in lvl7_list:
            txt = wx.StaticText(self, -1, label=label)
            txtctrl = HUD.RH_TextCtrl(self, -1, 
                                      name = name, 
                                      size = (120,-1), 
                                    style = wx.TE_READONLY)
            
            self.lsl.Add(name)

            txtctrl.tableName = tableName
            txtctrl.fieldName = fieldName

            level7_1Sizer.Add(txt, 0,wx.ALL|wx.ALIGN_CENTER, 3)
            level7_1Sizer.Add(txtctrl, 0,wx.ALL|wx.ALIGN_CENTER, 3)
        
        level8_1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # cbox = wx.ComboBox(self, -1, 
        #                    choices=[], 
        #                    name='custdata_custcode_combobox')    
        cbox = HUD.RH_Button(self, -1, name='custdata_custcode_btn')
        cbox.tableName = 'customer_basic_info'
        cbox.fieldName = 'typecode'
        cbox.DefaultTable = 'customer_codes'
        cbox.DefaultField = 'customer_code'
        cbox.Clear()

        txt = wx.StaticText(self, -1, label="Customer Code")
        
        level8_1Sizer.Add(txt, 0, wx.ALL|wx.ALIGN_CENTER, 3)
        level8_1Sizer.Add(cbox, 0, wx.ALL|wx.ALIGN_CENTER, 3)
        level8_1Sizer.Add((20,-1), 0)
        
        txt = wx.StaticText(self, -1, label="Statement\nof Terms")
        ctrl = HUD.RH_TextCtrl(self, -1, 
                               name='custdata_stmt_terms_txtctrl', 
                               size=(190, -1))
        self.lsl.Add('custdata_stmt_terms_txtctrl')
        ctrl.tableName = 'customer_basic_info'
        ctrl.fieldName = 'statement_terms'

        level8_1Sizer.Add(txt, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        level8_1Sizer.Add(ctrl, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        
        col1Sizer.Add(level2_1Sizer, 0, wx.ALL, 5)
        col1Sizer.Add(level3_1Sizer, 0, wx.ALL, 5)
        col1Sizer.Add(level4_1Sizer, 0, wx.ALL, 5)
        col1Sizer.Add(level5_1Sizer, 0, wx.ALL, 5)
        col1Sizer.Add(level6_1Sizer, 0, wx.ALL, 5)
        col1Sizer.Add(level7_1Sizer, 0, wx.ALL, 5)
        col1Sizer.Add(level8_1Sizer, 0, wx.ALL, 5)
                
        col2Sizer.Add(level2_2Sizer, 0)

        LowestSizer = wx.BoxSizer(wx.HORIZONTAL)
        lowest_list = [('Date Added','custdata_date_added_datectrl','customer_basic_info','date_added'),
                       ('Last Maintained','custdata_last_maintained_datectrl','customer_basic_info','last_maintained'),
                       ('Last Sale','custdata_last_sale_datectrl','customer_basic_info','last_sale'),
                       ('Birthday\n(mm/dd)','custdata_birthday_txtctrl','customer_basic_info','birthday')]
        
        for label, name, tableName, fieldName in lowest_list:
            vertSizer = wx.BoxSizer(wx.VERTICAL)
            txt = wx.StaticText(self, -1, label=label)
            if 'birthday' in name:
                ctrl = HUD.RH_MTextCtrl(self, -1, 
                                       mask='##/##',
                                       name=name)
            else:
                ctrl = HUD.RH_DatePickerCtrl(self, 
                                         name=name, 
                                         style=wx.adv.DP_ALLOWNONE)
            ctrl.tableName = tableName
            ctrl.fieldName = fieldName
            self.lsl.Add(name)

            vertSizer.Add(txt, 0,wx.ALL|wx.ALIGN_CENTER,3)       
            vertSizer.Add(ctrl, 0,wx.ALL|wx.ALIGN_CENTER,3)
            LowestSizer.Add(vertSizer, 0,wx.ALL|wx.ALIGN_CENTER, 5)
            
        ColumnSizer = wx.BoxSizer(wx.HORIZONTAL)
        ColumnSizer.Add(col1Sizer, 0, wx.ALL|wx.EXPAND, 5)
        ColumnSizer.Add(col2Sizer, 0, wx.ALL|wx.EXPAND, 5)
        
        MainSizer.Add(level1Sizer, 0, wx.ALL|wx.EXPAND, 5)
        MainSizer.Add(ColumnSizer, 0, wx.ALL|wx.EXPAND, 5)
        MainSizer.Add(LowestSizer, 0, wx.ALL|wx.EXPAND, 5)

        self.SetSizer(MainSizer, 0)
        self.Layout()
     
        wx.CallAfter(self.OnLoad, event='')
    
    def AddPhoneNumber(self, event):
        item = wx.FindWindowByName('custdata_addphone_txtctrl')
        typd = wx.FindWindowByName('custdata_phonetype_btn')
        olv = wx.FindWindowByName('custdata_phone_olv')
        
        addphone = [{'typd':typd.GetCtrl(), 'number':item.GetCtrl()}]
        olv.AddObjects(addphone)


    def AddAll(self, event):
        
        prefix = wx.FindWindowByName('custdata_prefix_btn').GetCtrl()
        fname = wx.FindWindowByName('custdata_fname_txtctrl').GetCtrl()
        minitial = wx.FindWindowByName('custdata_midInitial_txtctrl').GetCtrl()
        lname = wx.FindWindowByName('custdata_lname_txtctrl').GetCtrl()
        suffix = wx.FindWindowByName('custdata_suffix_txtctrl').GetCtrl()
        
        if prefix is None or prefix == '':
            fullName = "{0} {1} {2} {3}".format(fname, minitial, lname, suffix)
        else:
            fullName = "{0} {1} {2} {3} {4}".format(prefix, fname, minitial, lname, suffix)
        
        wx.FindWindowByName('custName_txtctrl').SetCtrl(fullName.title()) 
        
        
    def OnLoad(self, event):
        pass
        
    
    def OnChangeMainAddress(self, event):
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
        with HUD.AddAddressLookupDialog(self, 
                                        title="Add Address Form",  
                                        style=style) as dlg:
            dlg.ShowModal()
            self.addrPicked = None
            if dlg.itemPicked:
                self.addrPicked = dlg.itemPicked
                
        pout.v(("Address Lookup D : {}".format(self.addrPicked)) )
               
        wx.FindWindowByName('custdata_addr_acct_num_txtctrl1').SetCtrl(self.addrPicked)
        
        returnd = HUD.LookupDB('address_accounts').Specific(self.addrPicked,'addr_acct_num', 'address0,address2,address3,city,state,zipcode')
        addrShow = HUD.MiscOps().ShowAddress(returnd)
        
        wx.FindWindowByName('custdata_addressText_text').SetCtrl(addrShow)
     
    def Load(self,custNum=None,debug=False):
        if custNum is None:
            return
        
        returnd = HUD.LookupDB('customer_basic_info').Specific(custNum, 'cust_num','address_acct_num')
        
        addrNumber = returnd[0]
        loadlist = self.lsl.get()

        
        for name in loadlist:  
            item = wx.FindWindowByName(name)
            item.Clear()
            item.OnLoad(custNum, 'cust_num')
            

### LastSave        
    
             
        
#------------------------------------
    def CHECK(self):
        returnd = HUD.QueryCheck('customer_basic_info','cust_num',(self.supnum,))
        
        if returnd == 0 and re.match('[0-9A-Za-z]+',self.supnum):
            print(("ACCT # : {0} is USABLE".format(self.supnum)))
            new_custnum = self.supnum
        else:
            new_custnum = ''
        
        return new_custnum
            
    
    def AUTO(self):
        transaction_zeroes = 10
        current_count = HUD.QueryCheck('customer_basic_info')
        print((current_count[0]))
        new_custnum = current_count[0]
        while True:
            acct_custNum = str(new_custnum).zfill(transaction_zeroes)
            print(("Check CustNum : {0}".format(acct_custNum)))
            check_custnum = HUD.QueryCheck('customer_basic_info','cust_num',
                                          (acct_custNum,))
            
            if check_custnum == 0:
                print(("Check CustNum : {0} : Doesnt Exist".format(acct_custNum)))
                break
            
            new_custnum += 1
                    
        return acct_custNum
                         
    
#--------------------------
    
class RentalsTab(wx.Panel):
    def __init__(self, *args, **kwargs):
        """ Rentals Tab """
        wx.Panel.__init__(self, *args, **kwargs)
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        box = wx.StaticBox(self, -1, label="Rental House(s)")
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        
#        lc = HUD.Rental_LC(self, name='rentals_listctrl')
        lc = HUD.RH_OLV(self, name='rentals_listctrl', style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        lc.SetColumns([ColumnDefn('Account #','left',135,'acctNum'),
                       ColumnDefn('Address','left',300,'address'),
                       ColumnDefn('Unit','left',70,'address'),
                       ColumnDefn('City','left',190,'city'),
                       ColumnDefn('Zipcode','left',90,'zipcode')])
        

        lc.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onSelected)
                         
        
        aSizer = wx.BoxSizer(wx.VERTICAL)
        
        button_list = [('Add\nRental Address','rentals_add_button', self.OnAddRentalAddress),
                       ('Remove\nRental Address','rentals_remove_button', self.OnRemoveRentalAddress)]
        
        for label,name,hdlr in button_list:
            button = wx.Button(self, -1, label=label, name=name)
            button.Bind(wx.EVT_BUTTON, hdlr)
            button.Disable()
            aSizer.Add(button, 0, wx.ALL, 3)
        
        boxSizer.Add(lc,0)
        boxSizer.Add((10,10),0)
        boxSizer.Add(aSizer, 0)
        
        level1Sizer.Add(boxSizer, 0)
        MainSizer.Add(level1Sizer, 0)

        self.SetSizer(MainSizer)
    
    def onSelected(self, event):
        obj = event.GetEventObject()
        print("LC Row Selected")
        btn = wx.FindWindowByName('rentals_remove_button').Enable()
        
        
    def OnRemoveRentalAddress(self, event):
        lc = wx.FindWindowByName('rentals_listctrl')
        currentItem = lc.GetFirstSelected()
        lc.DeleteItem(currentItem)
        
            
    def OnAddRentalAddress(self, event):
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
        with HUD.AddAddressLookupDialog(self, 
                                        title="Add Address Form",  
                                        style=style) as dlg:
            
            dlg.ShowModal()
            self.addrPicked = None
            if dlg.itemPicked:
                self.addrPicked = dlg.itemPicked
            
        
        print(("Address Lookup D : ",self.addrPicked)) 
        
        
        lc = wx.FindWindowByName('rentals_listctrl')
        if self.addrPicked:
            lc.Add(self.addrPicked)
        
        #print "Index : ",lc.index
        #lc_cnt = lc.GetItemCount()
        #print "Item COunt : ",lc_cnt
        
        #rental_dict = {}
        #if lc_cnt == 0:
        #    rental_dict[lc_cnt] = self.addrPicked
        #else:
        #    for x in range(lc_cnt):
        #        item = lc.GetItem(x,0)
        #        value = item.GetText()
        #        rental_dict[x] = value
        #        print 'Item Value : ',value
            
        #    rental_dict[lc_cnt] = self.addrPicked
                
        #print 'Rental 0 : ',rental_dict
        
        #deleteItems = lc.DeleteAllItems()
        #print "Delete All Items : ",deleteItems
       # 
       # for xx, value in rental_dict.iteritems():
       #     query = """SELECT address0,city,state,zipcode,unit 
       #                FROM address_accounts 
       #                WHERE addr_acct_num=(?)"""
       #     data = (value,)
       #     returnd = SQConnect(query, data).ONE()
       #     
       #     (address0d, cityd,statd,zipcoded,unitd) = returnd
       #     
       #     lc_set = [(0,value),(1,address0d),
       #                 (3,cityd),(4,statd),(5,zipcoded),
       #                 (2,unitd)]
       #     for label,vari in lc_set:
       #         if label == 0:
       #             lc.InsertStringItem(xx, vari)
       #         else:
       #             lc.SetStringItem(xx,label,vari)        
                    
                
                
                
class SalesOptionsTab(wx.Panel):
    def __init__(self, *args, **kwargs):
        """ Sales Options Tab """
        wx.Panel.__init__(self, *args, **kwargs)
        
        self.SetName('SalesOptionsTab')
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        
        level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        tax_box = wx.StaticBox(self, -1, label="Tax Exemption")
        tax_boxSizer = wx.StaticBoxSizer(tax_box, wx.VERTICAL)
        
        taxlevels_list = [('Tax Exempt','salesopt_taxExempt_checkbox','customer_sales_options','tax_exempt'),
                          ('Tax Exempt ID','custdata_taxExemptID_txtctrl1','customer_basic_info','tax_exempt_number')]
        
        for label, name, tableName, fieldName  in taxlevels_list:
            if 'checkbox' in name:
                ctrl = HUD.RH_CheckBox(self, -1, label=label, name=name)
            
            if 'txtctrl' in name:
                ctrl = HUD.RH_TextCtrl(self, -1, name=name, size=(150,-1))
            ctrl.tableName = tableName
            ctrl.fieldName = fieldName
                
            tax_boxSizer.Add(ctrl, 0,wx.ALL|wx.EXPAND,5)
        
        level1Sizer.Add(tax_boxSizer, 0,wx.ALL|wx.EXPAND, 5)                          

        box = wx.StaticBox(self, -1, label='Salesperson')
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        
        query = "SELECT employee_num,employee_name FROM employees"
        data = ''
        returnd = SQConnect(query, data).ALL()
        if returnd:
            employee_choices = []
            print(("Returnd : ",returnd))
            for numd,named in returnd:
                new_emp = "{0} {1}".format(numd,named)
                employee_choices.append(new_emp)
           
        else:
            employee_choices = []
        
        cbox = HUD.RH_Button(self, -1, name='salesopt_employee_btn')
        cbox.listd = employee_choices
        boxSizer.Add(cbox, 0,wx.ALL|wx.EXPAND, 5)
        
        level1Sizer.Add(boxSizer, 0,wx.ALL|wx.EXPAND, 5)
        
        cb = HUD.RH_CheckBox(self, -1, 
                         label='No Checks', 
                         name='salesopt_noChecks_checkbox')
        cb.tableName = 'customer_sales_options'
        cb.fieldName = 'no_checks'
        
        level1Sizer.Add(cb, 0, wx.ALL|wx.EXPAND, 5)
        
        
        level2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        box = wx.StaticBox(self, -1, label="Clerk POS Message")
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        ctrl = HUD.RH_TextCtrl(self, -1, 
                           name = 'salesopt_clerkMessage_txtctrl', 
                           size = (400, 100), 
                           style = wx.TE_MULTILINE)
        
        ctrl.tableName = 'customer_sales_options'
        ctrl.fieldName = 'pos_clerk_message'
        boxSizer.Add(ctrl, 0)
        
        level2Sizer.Add(boxSizer, 0)
        
        level3Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        Discounts_list = [('No Discounts','salesopt_no_discounts_radiobtn','customer_sales_options','no_discount'),
                          ('Fixed Discount %','salesopt_fixed_discount_radiobtn','customer_sales_options','fixed_discount'),
                          ('00.00','salesopt_fixed_discount_numctrl','customer_sales_options','fixed_discount')]
        
        idx=0
        for label, name, tableName, fieldName in Discounts_list:
            if 'radiobtn' in name:
                if idx == 0:
                    ctrl = HUD.RH_RadioButton(self, -1, 
                                          label = label, 
                                          name = name, 
                                          style = wx.RB_GROUP)
                else:
                    ctrl = HUD.RH_RadioButton(self, -1, 
                                          label = label, 
                                          name = name)
            
                idx += 1
            if 'numctrl' in name:
                ctrl = HUD.RH_NumCtrl(self, -1, 
                                      name = name, 
                                      value = 0,
                                      integerWidth = 4,
                                      fractionWidth = 2)
            
            if 'combobox' in name:
                ctrl = wx.ComboBox(self, -1, name=name, choices=[])
            
            ctrl.tableName = tableName
            ctrl.fieldName = fieldName                                         
            
            level3Sizer.Add(ctrl, 0, wx.ALL, 5)

        level4Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        


        Sizer_list = [level1Sizer, level2Sizer, level3Sizer, level4Sizer]
        for sizer in Sizer_list:
            MainSizer.Add(sizer, 0, wx.ALL|wx.EXPAND, 10)
            
        self.SetSizer(MainSizer, 0)
        self.Layout()
       

    def Load(self, custNum):
        load_list = [('salesopt_taxExempt_checkbox','tax_exempt','customer_sales_options'),
                     ('salesopt_employee_btn','salesperson','customer_sales_options'),
                     ('salesopt_noChecks_checkbox','no_checks','customer_sales_options'),
                     ('salesopt_no_discounts_radiobtn','no_discount','customer_sales_options'),
                     ('salesopt_fixed_discount_numctrl','discount_amt','customer_sales_options'),
                     ('salesopt_fixed_discount_radiobtn','fixed_discount','customer_sales_options'),
                     ('salesopt_clerkMessage_txtctrl','pos_clerk_message','customer_sales_options')]
                                    
        for name, field, table in load_list:
            wx.FindWindowByName(name).ClearCtrl()

            returnd = HUD.LookupDB(table).Specific(custNum, 'cust_num', field)
            try:
                wx.FindWindowByName(name).SetCtrl(returnd[0])
            except:
                pout.v(returnd)
                
            
            
            

class AcctsReceivablesTab(wx.Panel):
    def __init__(self, *args, **kwargs):
        """ Accounts Receivables """
        wx.Panel.__init__(self, *args, **kwargs)
        
        self.SetName('Customers_AcctsRecTab')
        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
    
        col1Sizer = wx.BoxSizer(wx.VERTICAL)
        col2Sizer = wx.BoxSizer(wx.VERTICAL)
        col3Sizer = wx.BoxSizer(wx.VERTICAL)
        
        col1_list = [('Credit Limit','acctrec_credit_limit_text'),
                     ('Last Statement Date','acctrec_last_statement_text')]
        for label,name in col1_list:
            if 'text' in name:
                ctrl = wx.StaticText(self, -1, label=label)
            
            col1Sizer.Add(ctrl, 0,wx.ALL|wx.ALIGN_RIGHT,5)
                            
        level2_1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        lvl2_1list = [('Credit Limit','acctrec_credit_limit_numctrl','customer_accts_receivable','credit_limit'),
                      ('Freeze Charge Priviledges','acctrec_freeze_charge_checkbox','customer_accts_receivable','freeze_charges')] 
                  #('Late Charge Exempt','acctrec_late_charge_exempt_checkbox')
        
        for label,name, tableName, fieldName in lvl2_1list:
            if 'text' in name:
                ctrl = wx.StaticText(self, -1, label=label)
            if 'numctrl' in name:
                ctrl = HUD.RH_NumCtrl(self, -1, 
                                      value = 0, 
                                      name = name, 
                                      integerWidth = 6, 
                                      fractionWidth = 2)
                
                ctrl.Disable()
            if 'checkbox' in name:
                ctrl = HUD.RH_CheckBox(self, -1, 
                                   label = label, 
                                   name = name)

            ctrl.tableName = tableName
            ctrl.fieldName = fieldName    

            level2_1Sizer.Add(ctrl, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_LEFT, 5)
        
        col2Sizer.Add(level2_1Sizer, 0)
        level2_2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        lvl2_2List = [('Last Statement','acctrec_last_statement_date_datectrl','customer_accts_receivable','last_statement_date')]
        for label, name, tableName, fieldName  in lvl2_2List:
            ctrl = HUD.RH_DatePickerCtrl(self, -1, 
                                     name = name, 
                                     style = wx.adv.DP_ALLOWNONE|wx.adv.DP_DEFAULT)
            ctrl.tableName = tableName
            ctrl.fieldName = fieldName

            level2_2Sizer.Add(ctrl, 0)
            
            
        col2Sizer.Add(level2_2Sizer, 0,wx.ALL|wx.ALIGN_LEFT, 5)
            
        level2_3Sizer = wx.BoxSizer(wx.HORIZONTAL)    
        
        lvl2_3list = [('Current','acctrec_current_textbox','acctrec_current_numctrl'),
                      ('30-60 Days','acctrec_3060_days_textbox','acctrec_3060_numctrl'),
                      ('60-90 Days','acctrec_6090_days_textbox','acctrec_6090_numctrl'),
                      ('Over 90 Days','acctrec_90plus_textbox','acctrec_90plus_numctrl')]
        
        for label,box,name in lvl2_3list:
            box = wx.StaticBox(self, -1, label=label, style=wx.ALIGN_CENTER)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            
            ctrl = HUD.RH_NumCtrl(self, -1, 
                                  value = 0, 
                                  name = name, 
                                  integerWidth = 6, 
                                  fractionWidth = 2,
                                  style = wx.TE_READONLY)
            
            boxSizer.Add(ctrl, 0, wx.ALL, 5)
            ctrl.SetValue('0.00')             
            level2_3Sizer.Add(boxSizer, 0)
        
        col2Sizer.Add(level2_3Sizer, 0)
        level2_4Sizer = wx.BoxSizer(wx.HORIZONTAL)
        lvl2_4list = [('Activity','acctrec_activity_since_last_statement_numctrl'),
                      ('Activity since last statement','activity_since_last_statement_text')]
       
        for label, name in lvl2_4list:
            if 'text' in name:
                ctrl = wx.StaticText(self, -1, label=label)
            if 'numctrl' in name:
                ctrl = HUD.RH_NumCtrl(self, -1,  
                                      value = 0, 
                                      name = name, 
                                      integerWidth = 6, 
                                      fractionWidth = 2,
                                      style = wx.TE_READONLY)
                
            level2_4Sizer.Add(ctrl, 0, wx.ALL|wx.ALIGN_BOTTOM, 5)
                
        col2Sizer.Add(level2_4Sizer, 0)
        
        level2_5Sizer = wx.BoxSizer(wx.HORIZONTAL)
               
        col2Sizer.Add((50,50),0)
        
        lvl2_6Sizer = wx.BoxSizer(wx.HORIZONTAL)
        box = wx.StaticBox(self, -1, label="Last Paid Info")
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        
        ctrl = HUD.RH_DatePickerCtrl(self, -1, 
                                 name = 'acctrec_lastpaid_date_datectrl',
                                 style = wx.adv.DP_ALLOWNONE)
        
        ctrl.tableName = 'customer_accts_receivable'
        ctrl.fieldName = 'last_paid_date'

        ctrl.Bind(wx.EVT_SET_FOCUS, self.OnFocused)
        ctrl.Disable()
        txt = wx.StaticText(self, -1, label='Last Paid Date')
        boxSizer.Add(ctrl, 0, wx.ALL, 5)
        boxSizer.Add(txt, 0, wx.ALL, 5)
        
        boxSizer.Add(wx.StaticLine(self, -1, 
                                   size=(1,35),
                                   style=wx.LI_VERTICAL), 0)
 
        txt = wx.StaticText(self, -1, label='Last Payment')
        ctrl = HUD.RH_NumCtrl(self, -1, 
                              value = 0, 
                              name = 'custdata_last_payment', 
                              integerWidth = 6, 
                              fractionWidth = 2,
                              style = wx.TE_READONLY)
        

        boxSizer.Add(txt, 0, wx.ALL, 5)
        boxSizer.Add(ctrl, 0, wx.ALL, 5)
        
        col2Sizer.Add(boxSizer, 0)
        
        invdetail_list = ['Store Default', 'No Invoice Detail', 
                          'Print Invoice Detail']
        
        rbox = HUD.RH_RadioBox(self, -1, 
                           label = 'Invoice Detail on Statement', 
                           name = 'acctrec_invdetail_radiobox', 
                           choices = invdetail_list,
                           style = wx.RA_SPECIFY_ROWS)
        
        rbox.tableName = 'customer_accts_receivable'
        rbox.fieldName = 'print_invoice_detail_on_statement'
        
        col3Sizer.Add(rbox, 0)
        
        font = wx.Font(wx.FontInfo(18).Bold())
        box = wx.StaticBox(self, -1, label='Total A/R\n Amount')
        boxSizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        txt = wx.StaticText(self, -1, 
                            label = '$0.00',
                            name = 'acctrec_total_amt_due_text')
        
        txt.SetFont(font)
        box.SetForegroundColour('RED')
        txt.SetForegroundColour('RED')
        boxSizer.Add(txt, 0, wx.ALL, 15)
        
        font = wx.Font(wx.FontInfo(20).Bold())
        txt = wx.StaticText(self, -1, 
                            label = '', 
                            name = 'acctrec_delinquent_text')
        
        txt.SetFont(font)
        
        level3_2Sizer = wx.BoxSizer(wx.VERTICAL)
        level3_2Sizer.Add(boxSizer, 0)
        level3_2Sizer.Add(txt, 0)
        col3Sizer.Add(level3_2Sizer, 0)    
        MainSizer.Add(col1Sizer, 0,wx.ALL,5)
        MainSizer.Add(col2Sizer, 0,wx.ALL,5)
        MainSizer.Add(col3Sizer, 0,wx.ALL,5)
        self.SetSizer(MainSizer, 0)
        self.Layout()
        
        wx.CallAfter(self.OnLoad, event='')
    
    def OnFocused(self, event):
        focal = event.GetEventObject()
        print(("Focal : ",focal.GetName()))
        focal.SetInsertionPoint(0)
        focal.SetSelection(0,-1)
        focal.SetFocus()
        
    
    def OnLoad(self, event):
        current = datetime.now().date()
        Month1 = self.getMonthBefore(current)
        Month2 = self.getMonthBefore(Month1)
        Month3plus = self.getMonthBefore(Month2)
        custNum = wx.FindWindowByName('custNumber_txtctrl').GetCtrl()
         
        lvl2_3list = [(current, 'acctrec_current_numctrl'),
                      (Month1, 'acctrec_3060_numctrl'),
                      (Month2, 'acctrec_6090_numctrl'),
                      (Month3plus,'acctrec_90plus_numctrl')]

        for vari, name in lvl2_3list:
            whereDate = 'MONTH(date)={}'.format(vari.strftime('%m'))
            if 'plus' in name:
                month90 = Month3plus.strftime('%Y-%m-%d')
                whereDate = 'date<{}'.format(month90)
            query = '''SELECT total_price
                       FROM transaction_payments 
                       WHERE cust_num=(?) AND type_of_transaction=(?) AND {}'''.format(whereDate)
                       
            data = [custNum,'CHARGE',]
            
            returnd = SQConnect(query,data).ALL()
            
            total = 0
            print(('returnd : ',returnd))
            # for price in returnd:
            #     total += HUD.DeTupler(price)
                
        
        
            wx.FindWindowByName(name).SetCtrl(total)
        

    def getMonthBefore(self, month):  
        print(('month : ',month))
        HUD.VarOps().GetTyped(month)
        dated = month.replace(day=1) - timedelta(days=1)
        return dated
    
    def Load(self, custNum):
        load_list = [('acctrec_credit_limit_numctrl'), #'credit_limit','customer_accts_receivable'),
                     ('acctrec_freeze_charge_checkbox'), #'freeze_charges','customer_accts_receivable'),
                     ('acctrec_invdetail_radiobox')] #,'print_invoice_detail_on_statement','customer_accts_receivable')]

        for name in load_list:
            #wx.FindWindowByName(name).ClearCtrl()
            #returnd = HUD.LookupDB(table).Specific(custNum, 'cust_num', field)
            #wx.FindWindowByName(name).SetCtrl(returnd[0])
            item = wx.FindWindowByName(name)
            item.Clear()
            item.OnLoad(custNum, 'cust_num')
                                          
                                   
                
            
class ShipToTab(wx.Panel):
    def __init__(self, *args, **kwargs):
        """ Ship To """
        wx.Panel.__init__(self, *args, **kwargs)
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
        
        self.SetName('ShipToTab')
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        btn = wx.Button(self, -1, 
                        label = "Lookup\nShipto Address", 
                        name = 'shipto_addrlookup_btn')
        
        btn.Bind(wx.EVT_BUTTON, self.OnSearchShipto)
        btn.Disable()
        
        level1Sizer.Add(btn, 0, wx.ALL, 5)
        ctrl = HUD.RH_TextCtrl(self, -1, 
                           name = 'shipto_address_acct_num_txtctrl',
                           size = (90, -1))
        
        ctrl.tableName = 'customer_shipto_info'
        ctrl.fieldName = 'address_acct_num'
        ctrl.Disable()
        level1Sizer.Add(ctrl, 0, wx.ALL, 5)
        
        level2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        lvl2_list = [('Name   ','shipto_name_text','',''),
                     ('Name','shipto_name_txtctrl','customer_shipto_info','name'),
                     ('Telephone','shipto_phone_text','',''),
                     ('Telephone','shipto_phone_txtctrl','customer_shipto_info','phone')]

        for label,name, tableName, fieldName in lvl2_list:
            if 'text' in name:
                ctrl = wx.StaticText(self, -1, label=label)
            if 'txtctrl' in name:
                if 'phone' in name:
                    ctrl = HUD.RH_MTextCtrl(self, -1, 
                                            name=name, 
                                            autoformat='USPHONEFULLEXT') 
                    
                else:
                    ctrl = HUD.RH_TextCtrl(self, -1, 
                                           name=name, 
                                           size=(250,-1))
                
                ctrl.Disable()
                ctrl.tableName = tableName
                ctrl.fieldName = fieldName

            level2Sizer.Add(ctrl, 0, wx.ALL|wx.ALIGN_BOTTOM, 5)
        
        level3Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        lvl3_list = [('Address','shipto_addr1_text',250,'',''),
                     ('Address','shipto_addr1_txtctrl',250, 'address_accounts','address0'),
                     ('Ship Method','shipto_shipmethod_text',250,'',''),
                     ('ShipMethod', 'shipto_shipmethod_btn',250,'customer_shipto_info','ship_by')]
        
        for label, name, sized, tableName, fieldName  in lvl3_list:
            if 'text' in name:
                ctrl = wx.StaticText(self, -1, label=label)
            if 'txtctrl' in name:
                ctrl = HUD.RH_TextCtrl(self, -1, 
                                   name=name, 
                                   size=(sized,-1),
                                   style=wx.TE_READONLY) 
            
            if 'btn' in name:
                ctrl = HUD.RH_Button(self, -1, 
                                           name = name)        
            ctrl.tableName = tableName
            ctrl.fieldName = fieldName
            level3Sizer.Add(ctrl, 0, wx.ALL, 5)
        
        level4Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        level4Sizer.Add((52,10), 0,wx.ALL, 5)
        addr2_txtctrl = HUD.RH_TextCtrl(self, -1, 
                                    name = 'shipto_addr2_txtctrl',
                                    size = (250, -1),
                                    style = wx.TE_READONLY)
        ctrl.tableName = 'address_accounts'
        ctrl.fieldname = 'address2'
        level4Sizer.Add(addr2_txtctrl, 0, wx.ALL, 5)
    
        level5Sizer = wx.BoxSizer(wx.HORIZONTAL)
        ctrl = HUD.RH_MTextCtrl(self, -1, 
                                name = "shipto_city_txtctrl", 
                                size = (180, -1),
                                style = wx.TE_READONLY)
        ctrl.tableName = 'address_accounts'
        ctrl.fieldName = 'city'
        level5Sizer.Add((52,10),0,wx.ALL, 5)
        level5Sizer.Add(ctrl, 0, wx.ALL, 5)

        t = wx.StaticText(self, -1, label=', ')
        ctrl = HUD.RH_MTextCtrl(self, -1, 
                                name = 'shipto_state_txtctrl', 
                                formatcodes = '!_', 
                                mask = 'AA&', 
                                style = wx.TE_READONLY)
        ctrl.tableName = 'address_accounts'
        ctrl.fieldName = 'state'
        level5Sizer.Add(t, 0,wx.ALL|wx.ALIGN_BOTTOM)
        level5Sizer.Add(ctrl, 0, wx.ALL, 5)

        ctrl = HUD.RH_MTextCtrl(self, -1, 
                                name = 'shipto_zipcode_txtctrl',
                                mask = '(#{5}|#{5}-#{4})', 
                                style = wx.TE_READONLY)
        ctrl.tableName = 'address_accounts'
        ctrl.fieldName = 'zipcode'
        level5Sizer.Add(ctrl, 0, wx.ALL, 5)
        
        level6Sizer = wx.BoxSizer(wx.HORIZONTAL)
        t = wx.StaticText(self, -1, label="Comment")
        ctrl = HUD.RH_TextCtrl(self, -1, 
                               name = 'shipto_comments_txtctrl', 
                               size = (450,200), 
                               style = wx.TE_MULTILINE)
        
        ctrl.tableName = 'customer_shipto_info'
        ctrl.fieldName = 'comments'
        level6Sizer.Add(t, 0, wx.ALL, 5)
        level6Sizer.Add(ctrl, 0, wx.ALL, 5)
         
        MainSizer.Add(level1Sizer, 0)
        MainSizer.Add(level2Sizer, 0)
        MainSizer.Add(level3Sizer, 0)
        MainSizer.Add(level4Sizer, 0)
        MainSizer.Add(level5Sizer, 0)
        MainSizer.Add(level6Sizer, 0)
        
        self.SetSizer(MainSizer, 0)
        self.Layout()
        
        wx.CallAfter(self.OnLoad, event='')
        
    def OnLoad(self, event):
        query = "SELECT * FROM shipping_methods"
        data = ''
        returnd = SQConnect(query, data).ALL()
        #shipmethchoice = list(sum(returnd, ()))
        #wx.FindWindowByName('shipto_shipmethod_combobox').SetCtrl(shipmethchoice)    
        
    def OnSearchShipto(self, event):
        """ Lookup Address"""
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)    
        title = 'Search-N-Add Address Form'
        with HUD.AddAddressLookupDialog(self, title=title,  style=style) as dlg:
            if dlg.ShowModal() == wx.Close:
                return
            self.addrPicked = None
            if dlg.itemPicked:
                self.addrPicked = dlg.itemPicked

        print(("Address Lookup D : ",self.addrPicked)) 
        cn = wx.FindWindowByName('custName_txtctrl').GetCtrl()
        wx.FindWindowByName('shipto_name_txtctrl').SetCtrl(cn)
        wx.FindWindowByName('shipto_address_acct_num_txtctrl').SetCtrl(self.addrPicked)
        shipto_list = [('shipto_addr1_txtctrl','address0'),
                       ('shipto_addr2_txtctrl','address2'),
                       ('shipto_city_txtctrl','city'),
                       ('shipto_state_txtctrl','state'),
                       ('shipto_zipcode_txtctrl','zipcode')]
        
        for name, field in shipto_list:
            query = """SELECT {0} 
                       FROM address_accounts 
                       WHERE addr_acct_num=(?)""".format(field)
            
            data = (self.addrPicked,)
            returnd = SQConnect(query, data).ONE()[0]
            wx.FindWindowByName(name).SetCtrl(returnd)               
        

    def Load(self, custNum):
        load_list = [('shipto_name_txtctrl','name','customer_shipto_info'),
                      ('shipto_phone_txtctrl','phone','customer_shipto_info'),
                      ('shipto_address_acct_num_txtctrl','address_acct_num','customer_shipto_info'),
                      ('shipto_comments_txtctrl','comments','customer_shipto_info'),
                      ('shipto_shipmethod_btn','ship_by','customer_shipto_info')]
        
        for name, field, table in load_list:
            wx.FindWindowByName(name).ClearCtrl()
            returnd = HUD.LookupDB(table).Specific(custNum, 'cust_num', field)
            try:
                value = returnd[0]
                wx.FindWindowByName(name).SetCtrl( value)
            
                if 'shipto_address_acct_num_txtctrl' in name:
                    if value:
                        address_acct_num = value
                        shipto_list = [('shipto_addr1_txtctrl','address0'),
                                    ('shipto_addr2_txtctrl','address2'),
                                    ('shipto_city_txtctrl','city'),
                                    ('shipto_state_txtctrl','state'),
                                    ('shipto_zipcode_txtctrl','zipcode')]
                        
                        for name2, field2 in shipto_list:
                            returnd = HUD.LookupDB('address_accounts').Specific(address_acct_num,'address_acct_num', field2)
                            try:
                                wx.FindWindowByName(name2).SetCtrl( returnd[0])
                            except:
                                pout.v(returnd)
            except:
                pout.v(returnd)
            
                                        
             
        
class NotesTab(wx.Panel):
    def __init__(self, parent,debug=False):
        """ Notes """
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.SetName('NotesTab')
        yellowback = (246,241,87)
        
        ctrl = HUD.RH_TextCtrl(self, -1, 
                           name='notes_notes_txtctrl', 
                           size=(600,300), 
                           style=wx.TE_MULTILINE)
        ctrl.tableName = 'customer_notes'
        ctrl.fieldName = 'notes'

        ctrl.SetBackgroundColour(yellowback)
        ctrl.Disable()
        
        MainSizer.Add((10,70),0)
        MainSizer.Add(ctrl, 0,wx.ALL|wx.ALIGN_CENTER, 5)
        
        self.SetSizer(MainSizer, 0)
        self.Layout()
            
    def Load(self, custNum):
        load_list = ['notes_notes_txtctrl']
        
        for name in load_list:
            wx.FindWindowByName(name).ClearCtrl()
            item = wx.FindWindowByName(name).OnLoad()
            # returnd = HUD.LookupDB(table).Specific(custNum, 'cust_num', field)
            # wx.FindWindowByName(name).SetCtrl( returnd[0])
            

class TransactionsTab(wx.Panel):
    def __init__(self, parent, debug=False):
        """ Transactions """
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)        
        header_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        P2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        col1Sizer = wx.BoxSizer(wx.VERTICAL)
        col2Sizer = wx.BoxSizer(wx.VERTICAL)
        custNumber = wx.FindWindowByName('custNumber_txtctrl').GetCtrl()
        
        addr_list = [('','transactions_addr_combobox'),
                     ('','transactions_address_text')]
        header_Sizer.Add((150,10),0)
        for label,name in addr_list:
            if 'text' in name:
                ctrl = wx.StaticText(self, -1, label=label, name=name)
                header_Sizer.Add(ctrl,wx.ALL|wx.ALIGN_RIGHT, 5)
            if 'combobox' in name:
                ctrl = wx.ComboBox(self, -1, choices=[label,], name=name,size=(120,-1))
                ctrl.Bind(wx.EVT_COMBOBOX, self.OnAddrCombo)
                header_Sizer.Add(ctrl, 0, wx.ALL|wx.ALIGN_BOTTOM, 5)
                    
        
        inv_text = wx.StaticText(self, -1, label='Invoices')
        col1Sizer.Add(inv_text, 0, wx.ALL, 5)
        lcname = 'customers_transactions_inv_lc'
        #lc = wx.ListCtrl(self, -1, size=(830,165), name=lcname, style=wx.LC_REPORT|wx.BORDER_SIMPLE)
        lc = HUD.RH_OLV(self, -1, size=(830,165), name=lcname, style=wx.LC_REPORT|wx.BORDER_SIMPLE)       
        lc.SetColumns([
                      ColumnDefn('Invoice','center',150,'invoice'),
                      ColumnDefn('Date','center',125,'dated'),
                      ColumnDefn('Time','center',125,'timed'),
                      ColumnDefn('Type','center',125,'typed'),
                      ColumnDefn('Amount','right',150,'amt'),
                      ColumnDefn('Paid','right',125,'paid')
        ])  
        #lc.SetEmptyListMsg('None')                          
        #colLabel_list = [('Invoice',150),('Date',125),('Time',125),('Type',125),('Amount',150),('Paid',125)]
        #idx = 0
        #for label, width in colLabel_list:
        #    lc.InsertColumn(idx, label, width=width)
        #    idx += 1    
         
            
        #HUD.LCAlternateColor(lcname, idx)    
        
        
        lc.Disable()
        col2Sizer.Add(lc, 0,wx.ALL, 5)
        
        payment_text = wx.StaticText(self, -1, label="Payments")
        col1Sizer.Add((10,160),0)
        col1Sizer.Add(payment_text, 0)
        lcname = 'customers_transaction_payments_lc'
        #lc = wx.ListCtrl(self, -1, size=(920, 165), name=lcname, style=wx.LC_REPORT|wx.BORDER_SIMPLE)
        lc = HUD.RH_OLV(self, -1, size=(920,165), name=lcname, style=wx.LC_REPORT|wx.BORDER_DEFAULT)
        lc.SetColumns([
                      ColumnDefn('Invoice','center',150,'invoice'),
                      ColumnDefn('Date','center',125,'dated'),
                      ColumnDefn('Time','center',125,'timed'),
                      ColumnDefn('Type','center',125,'typed'),
                      ColumnDefn('Amount','right',150,'amt'),
                      ColumnDefn('Check / Card #','center',250,'coc_num')
        ])
        
        # colLabel_list = [('Invoice',150),('Date',125),('Time',125),('Type of Payment',125),('Amount',150),('Check or Card Number',250)]
        
        # for label, width in colLabel_list:
        #     lc.InsertColumn(idx, label, width=width)
        #     idx += 1    
        
            
        # HUD.LCAlternateColor(lcname, idx)
        
        
        lc.Disable()
        col2Sizer.Add(lc, 0,wx.ALL, 5)
        
        P2Sizer.Add(col1Sizer, 0)
        P2Sizer.Add(col2Sizer, 0)
        
        MainSizer.Add(header_Sizer, 0, wx.ALL,3)
        MainSizer.Add(P2Sizer,  0)
        

        self.SetSizer(MainSizer, 0)
        self.Layout()


    def OnAddrCombo(self, event):
        print("COMBO ACTIVATED")
        item = event.GetEventObject()
        addr = item.GetStringSelection()
        m = re.match('^A[0-9]+',addr)
        addr_num = m.group(0)
        
        print(("Addr ComboBox : ",addr_num))
        query = """SELECT address0,city,state,zipcode 
                   FROM address_accounts 
                   WHERE addr_acct_num=(?)"""
        
        data = (addr_num,)
        returnd = SQConnect(query, data).ONE()
        if returnd:
           (address0d,cityd,stated,zipcoded) = returnd 
        else:
            address0d,cityd,stated,zipcoded = '','','',''
        
        address_fill = "{0}, {1}, {2}  {3}".format(address0d,cityd,
                                                   stated,zipcoded)
        print(("Address : : ",address_fill))
        item = wx.FindWindowByName('transactions_address_text').SetCtrl(address_fill)
        query = """SELECT date, time, transaction_id,
                          type_of_transaction, total_price 
                   FROM transactions 
                   WHERE address_acct_num=(?)"""
        
        data = (addr_num,)
        returnd = SQConnect(query, data).ALL()
        print(("Returnd from AddrCombo : ",returnd))
        getit_back = sorted(returnd, key=itemgetter(3), reverse=True)
        lcname = 'customers_transactions_inv_lc'
        lc = wx.FindWindowByName(lcname)
        HUD.ClearCtrl(lcname)
        lc.Enable() 
        print(("COMBO Returnd : ",returnd))
        if len(returnd) == 0:
            pass
        
        idx = 0
                
        for dated,timed,transaction_idd,typed,totald in getit_back:
            colval_list = [(0,transaction_idd),(1,dated),  
                           (2,timed),(3,typed),(4,totald)]
            
            
            print(("Transaction ID : ",transaction_idd))
            print(("Date : ",dated))
            print(("Time : ",timed))
            print(("Type : ",typed))
            print(("Total : ",totald))
            HUD.LCFill(lcname, colval_list, idx)                                
            idx += 1         
        
        HUD.LCAlternateColor(lcname,idx)
        query="""SELECT date, time, transaction_id, type_of_transaction,
                        total_price, pay_method 
                 FROM transaction_payments 
                 WHERE address_acct_num=(?) AND total_price<>'0.00'"""
        data = (addr_num,)
        returnd = SQConnect(query, data).ALL()
        
        getit_back = sorted(returnd, key=itemgetter(0), reverse=True)
        lcname = 'customers_transaction_payments_lc'
        lc = wx.FindWindowByName(lcname)
        HUD.ClearCtrl(lcname)
        lc.Enable() 
        print(("COMBO Returnd : ",returnd))
        if len(returnd) == 0:
            pass
        
        idx = 0
        for dated,timed,transaction_idd,typed,totald,paymethd in getit_back:
            
            colval_list = [(0,transaction_idd),(1,dated),
                           (2,timed),(3,paymethd),
                           (4,totald),(5,typed)]
            
            HUD.LCFill(lcname, colval_list, idx)
            
            idx += 1
        
        
        HUD.LCAlternateColor(lcname, idx)        

class RecurringChargesTab(wx.Panel):
    def __init__(self,parent, debug=False):
        """ Recurring Charges """
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        t = wx.StaticText(self, -1, "Still Thinking about this one...")        

		
class PersonnelTab(wx.Panel):
    def __init__(self, parent, debug=False):
        """ Personnel """
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        
        MainSizer.Add((50,50),0)
        col1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        col2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # colLabel_list = [('Name', 200),('Location',230)]              
        # lc = wx.ListCtrl(self, -1, 
        #                  size=(450,200), 
        #                  name="customers_personnel_lc", 
        #                  style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        
        lc = HUD.RH_OLV(self, -1, name='customer_personnel_lc', size=(450,200), style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        lc.SetColumns([ 
                      ColumnDefn('Name','left',200,'name'),
                      ColumnDefn('Location','left',230,'location')
        ])
        # idx = 0
        # for titl, width in colLabel_list:
        #     lc.InsertColumn(idx, titl, width=width)
        #     idx += 1
        
        lc.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect)
                
        col1Sizer.Add((50,50),0)
        col1Sizer.Add(lc, 0,wx.ALL, 10)
        
        sqSize = 200
        box = wx.StaticBox(self, -1, label='Personnel Images', size=(sqSize,sqSize))
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        
        png = wx.StaticBitmap(self, -1, bitmap=wx.Bitmap(sqSize,sqSize),size=(sqSize,sqSize),name='customers_personPics_img')
        boxSizer.Add(png, 0, wx.ALL, 5)
        col1Sizer.Add(boxSizer, 0)
        
        col2Sizer.Add((50,50),0)
        col2_list = [('Name','personnel_name_txtctrl'),
                     ('File Path','personnel_location_text')]
        
        for label,name in col2_list:
            box = wx.StaticBox(self, -1, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            if 'txtctrl' in name:
                ctrl = HUD.RH_TextCtrl(self, -1, name=name, size=(130,-1))
            if 'text' in name:
                ctrl = wx.StaticText(self, -1, name=name, size=(130,-1))
                
            boxSizer.Add(ctrl, 0)
            col2Sizer.Add(boxSizer, 0, wx.ALL,3)        

        btn = wx.Button(self, -1, label='Find')
        btn.Bind(wx.EVT_BUTTON, self.LoadFile)
        col2Sizer.Add(btn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)
        SaveButton = wx.Button(self, -1, label='Save')
        
        
        MainSizer.Add(col1Sizer,0)
        MainSizer.Add(col2Sizer, 0)
        
        self.SetSizer(MainSizer, 0)
        self.Layout()
    
    
    def OnSelect(self, event):
        lc = wx.FindWindowByName('customers_personnel_lc')
        item_id,objText = HUD.LCGetSelected(event)
        trans_id = objText
        imgpath = lc.GetItem(item_id, 1).GetText()
        png = wx.FindWindowByName('customers_personPics_img')
        start_img = wx.Image(imgpath)
        start_img.Rescale(200,200)
        image = wx.BitmapFromImage(start_img)
        img = wx.Bitmap(image, wx.BITMAP_TYPE_ANY)

        print(('Img Path : ',imgpath))
        png.SetBitmap(img)
        
    def LoadFile(self, event):
        wcd = 'Image files (*.png)|*.jpg|'
#         
        save_dlg = wx.FileDialog(self, message='Open Picture', defaultDir='', defaultFile= '', wildcard=wcd, style=wx.OPEN|wx.FD_PREVIEW)
        path = None
        if save_dlg.ShowModal() == wx.ID_OK:
            path = save_dlg.GetPath()
 
        if path is not None:
            wx.FindWindowByName('personnel_location_text').SetCtrl(path)
        else:
            return
            
        lc_name = 'customers_personnel_lc'
        lc = wx.FindWindowByName(lc_name)
    
        idx = lc.GetItemCount()
        print(('idx Geti Count : ',idx))
        named = wx.FindWindowByName('personnel_name_txtctrl').GetCtrl()
        
        setList = [(0,named),(1,path)]
        HUD.LCFill(lc_name, setList, idx)
        
    
    
    def OnSave(self):
        pass    
        
    
class StartPanel(wx.Panel):
    def __init__(self,*args, **kwargs): #parent,From,CustNum):
        self.startFrom = kwargs.pop('From')
        self.custNum = kwargs.pop('CustNum')
        wx.Panel.__init__(self, *args, **kwargs) #parent=parent, id=wx.ID_ANY)
        self.SetName('CustomerStartPanel')
        pout.v(f'_________++++++ Start From : {self.startFrom}')
        try:
            if self.custNum is not None or self.custNum != '':
                pout.b(f'AcctNum : {self.custNum} | {len(self.custNum)}')
        except:
            print('....')    
        self.lsl = HUD.LoadSaveList()
        self.enablelist = HUD.LoadSaveList()

        lookupSizer = wx.BoxSizer(wx.VERTICAL)
        
        basePath = os.path.dirname(os.path.realpath(__file__))+'/' 
        IconBar_list =[('FindButton', ButtonOps().Icons('find'), self.OnFind),
                       ('SaveButton', ButtonOps().Icons('save'), self.OnSave),
                       ('UndoButton', ButtonOps().Icons('undo'), self.OnUndo),
                       ('AddButton', ButtonOps().Icons('add'),   self.OnAdd),
                       ('DeleteButton', ButtonOps().Icons('delete'), self.OnDelete),
                       ('AddressMaintenanceButton', ButtonOps().Icons('addrMaint'), self.OnAddressMaintenance),
                       ('ExitButton', ButtonOps().Icons('exit'),    self.OnExitButton)]
        
        IconBox = wx.StaticBox(self, label='')
        
        IconBarSizer = wx.StaticBoxSizer(IconBox, wx.HORIZONTAL)        
        xx = 0        
        for name,iconloc,handler in IconBar_list:
            if 'Exit' in name and 'Customers.py' in __file__:
                icon = wx.BitmapButton(self, wx.ID_ANY,
                                        wx.Bitmap(iconloc), 
                                        name = name, 
                                        style = wx.BORDER_NONE)
                
                
            else:
                icon = wx.BitmapButton(self, wx.ID_ANY,
                                    wx.Bitmap(iconloc), 
                                    name = name, 
                                    style = wx.BORDER_NONE)
                
            icon.Bind(wx.EVT_BUTTON, handler)
            IconBarSizer.Add((80,1),0)
            if self.custNum is not None:
                disabledButtons = '(SAVE|UNDO|ADD|DELETE)'
            else:
                disabledButtons = ''
            
            if len(disabledButtons) > 0 and re.search(disabledButtons,name, re.I):
                icon.Disable()
            if 'Left' in name or 'Right' in name:
                IconBarSizer.Add(icon,0)
            elif 'Exit' in name:
                IconBarSizer.Add((150,10), 1)
                IconBarSizer.Add(icon, 0)
            else:
                if xx > 0:
                    IconBarSizer.Add((5,1), 0)
                    IconBarSizer.Add(wx.StaticLine(self, -1, 
                                                   size=(1,35),
                                                   style=wx.LI_VERTICAL),  0)
                
                IconBarSizer.Add((5,1), 0)
                IconBarSizer.Add(icon, 0)
            xx += 1
        lookupSizer.Add((10,10), 0)    
        

        level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        level1_list = [('Customer Number','custNumber_txtctrl', 240,'customer_basic_info','cust_num'),
                       ('Customer Name','custName_txtctrl',360,'customer_basic_info','full_name'),
                       ('Deactivated','deactivated_checkbox',0,'','')]
        
        for label, name, sized, tableName, fieldName in level1_list:
            if 'checkbox' in name:
                ctrl = HUD.RH_CheckBox(self, label=label, name=name)
                level1Sizer.Add(ctrl, 0, wx.ALL|wx.ALIGN_BOTTOM, 10)
            else:        
                box = wx.StaticBox(self, label=label)
                boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
                if 'custNumber' in name:
                    ctrl = HUD.RH_TextCtrl(self, -1, 
                                            name = name, 
                                            size = (sized, -1),
                                            style = wx.TE_PROCESS_ENTER)
                    
                    ctrl.Bind(wx.EVT_TEXT_ENTER, self.OnCustNumberLookup)
                    ctrl.SetFocus()
                else:
                    ctrl = HUD.RH_TextCtrl(self, -1, name=name, size=(sized, -1))
                
                boxSizer.Add(ctrl, 0)
                level1Sizer.Add(boxSizer, 0)               
            ctrl.tableName = tableName
            ctrl.fieldName = fieldName

        level2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        #panel = wx.Panel(self)
        self.notebook = wx.Notebook(self, wx.ID_ANY)
        tabOne = CustomerDataTab(self.notebook)
        tabOne_A = RentalsTab(self.notebook)
        tabTwo = SalesOptionsTab(self.notebook)
        tabThree = AcctsReceivablesTab(self.notebook)
        tabFour = ShipToTab(self.notebook)
        tabFive = NotesTab(self.notebook)
        tabSix = TransactionsTab(self.notebook)
        tabSeven = RecurringChargesTab(self.notebook)
        tabEight = PersonnelTab(self.notebook)
        
        self.notebook.AddPage(tabOne, "Customer Data")
        self.notebook.AddPage(tabOne_A, "Rental(s)")
        self.notebook.AddPage(tabTwo, 'Sales Options')
        self.notebook.AddPage(tabThree, "Accounts Receivable")
        self.notebook.AddPage(tabFour, "Ship To:")
        self.notebook.AddPage(tabFive, "Notes")
        self.notebook.AddPage(tabSix, "Transactions")
        self.notebook.AddPage(tabSeven, "")
        self.notebook.AddPage(tabEight, "Personnel")
        
        #self.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)
        
        level2Sizer.Add(self.notebook, 1, wx.ALL|wx.EXPAND, 5)
        
        
        lookupSizer.Add(IconBarSizer, 0, flag=wx.ALL|wx.EXPAND)

        lookupSizer.Add(level1Sizer, 0)
        lookupSizer.Add(level2Sizer, 0, wx.ALL|wx.EXPAND, 5)
        
        self.SetSizer(lookupSizer, 0)
        
        self.Layout()
    
        wx.CallAfter(self.SetCustNumber, event='')
    
    def OnAddressMaintenance(self, event):
        dlg = HUD.AddressAccounts(self, title='Address Accounts', size=(900,650))
        dlg.ShowModal()


    def ChangeFrom(self, From):
        self.startFrom=From
        self.Update()
        self.Refresh()
        
    
    def SetCustNumber(self, event):
        print(("++++ SET CUSTOMER NUMBER ---- ",self.custNum))
        
        if self.custNum is not None and len(self.custNum) > 0:

            wx.FindWindowByName('custNumber_txtctrl').SetCtrl(self.custNum)
            wx.CallAfter(self.OnLoad, event=self.custNum)        
        
    def OnFind(self, event):
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
        title='Customer Lookup'
        CustomerLookupD = HUD.CustLookupDialog(self, title=title)
        CustomerLookupD.ShowModal()
        try:
            CustomerLookupD.itemPicked
        except:
            CustomerLookupD.Destroy()
            return 
               
        self.custPicked = CustomerLookupD.itemPicked.strip()
        print(("Customer Lookup D : ",self.custPicked)) 
        CustomerLookupD.Destroy()
        
        
        wx.FindWindowByName('custNumber_txtctrl').SetCtrl( self.custPicked)
        wx.CallAfter(self.OnLoad, event=self.custPicked)

    def OnCustNumCheck(self, event):
        check_num = wx.FindWindowByName('custNumber_txtctrl')
        check_numval = check_num.GetValue()
        #check_btn = wx.FindWindowByName('custadd_custnumchk_button')
        print(("Check Num Name : ",check_numval))
        if check_numval:
            chk = AccountOps().AcctNumCheck('customer_basic_info','cust_num',check_numval)
            print(("Check : ",chk))
            if chk > 0:
                dial = wx.MessageDialog(None, f'{check_numval} in use. \nAuto Create Customer Number?', 'Question', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
                if dial.ShowModal() == wx.ID_YES:
                    chk = AccountOps().AcctNumAuto('customer_basic_info','cust_num',fill0s=10)
                    check_num.SetValue(chk)       
                else:
                    check_num.SetValue('')
                dial.Destroy()
            else:
                check_num.SetBackgroundColour('Green')
    
         
    def OnCustNumberLookup(self, event):
        obj = event.GetEventObject()
        #item = wx.FindWindowByName(obj.GetName())
        
        custNumber = obj.GetValue().strip()
        obj.ChangeValue(custNumber.upper())
        checkExist = HUD.QueryOps().QueryCheck('customer_basic_info', 'cust_num',(custNumber,))
        pout.v(checkExist)  
        if checkExist == 1:
            wx.CallAfter(self.OnLoad, event='')
        else:
            CustomerLookupD = HUD.CustLookupDialog(self)
            CustomerLookupD.ShowModal()
            try:
                itemPicked = CustomerLookupD.itemPicked
                item.SetValue(itemPicked)
                wx.CallAfter(self.OnLoad, event="")
            except:
                CustomerLookupD.Destroy()
                return     
            
    
    def OnLoad(self,event):
        debug = True
        
        
        try:
            custNumber = wx.FindWindowByName('custNumber_txtctrl').GetCtrl()
        except:
            query = 'SELECT cust_num FROM customer_basic_info limit 1'
            data = ''
            returnd = SQConnect(query, data).ONE()
            custNumber = returnd[0]
            
        load_list = [('custdata_acct_type_btn','account_types','account_type'),
                     ('custdata_custcode_btn','customer_codes','customer_code')]
        
        
        for name, tableName, fieldName in load_list:
            query = "Select {} From {}".format(fieldName, tableName)
            data = ''
            returnd = SQConnect(query, data).ALL()
            if returnd:
                list_choices = returnd
                wx.FindWindowByName(name,list_choices).SetCtrl(debug)

                enabled=True
                if self.startFrom is not None:
                    enabled=False
                    print('++ ++ ENABLED FALSE ++ ++')
                else:
                    print('+++')
                    
                wx.FindWindowByName(name).EnableCtrl(enable=enabled)    
                
        
        
        query = '''SELECT address_acct_num 
                   FROM customer_basic_info 
                   WHERE cust_num=(?)'''
        data  = (custNumber,)
        addrNumber = SQConnect(query, data).ONE()[0] 
        
        load_tabs = ['Customers_AcctsRecTab','CustomerDataTab','SalesOptionsTab','ShipToTab']
        
        try:
            returnd = HUD.LookupDB('address_accounts').Specific(addrNumber, 'addr_acct_num','address0,address2,address3,city,state,zipcode')
            (addr0,addr2,addr3,city,state,zipcode) = returnd
        except:
            addr0 = addr2 = addr3 = city = state = zipcode = ''
        
        addrShow = ''
        addrList = (addr0, addr2, addr3)
        for item in addrList:
            if item:
                addrShow += '{0} \n'.format(item)
        
        if city and state and zipcode:
            addrShow +='{0}, {1}  {2}\n'.format(city, state, zipcode)
        
        for name in load_tabs:
            tab = wx.FindWindowByName(name)
            try:
                tab.Load(custNumber)
            except:
                pout.v('Didn\'t manage to load customer')
        
        custName = wx.FindWindowByName('custName_txtctrl').GetCtrl()            

        if re.search('nobody',custName, re.I):

            tup = ('custdata_prefix_btn','custdata_fname_txtctrl',
                   'custdata_midInitial_txtctrl','custdata_lname_txtctrl',
                   'custdata_suffix_txtctrl')
            HUD.AddAll(tup,'custName_txtctrl')    

    
    
        toEnable_list = ['SaveButton','DeleteButton',
                         'custdata_phone_type_btn',
                         'custdata_phoneNum_txtctrl1',
                         'custdata_phone_listctrl','custdata_phone_del_button',
                         'custdata_acct_type_btn','custadd_phone_button',
                         'custdata_alt_post_acct_txtctrl',
                         'custdata_email_txtctrl1',
                         'custdata_taxExemptID_txtctrl1',
                         'custdata_contact1_txtctrl',
                         'custdata_contact2_txtctrl',
                         'custdata_stmt_terms_txtctrl',
                         'custdata_date_added_datectrl',
                         'custdata_last_maintained_datectrl',
                         'custdata_last_sale_datectrl',
                         'custdata_birthday_txtctrl',
                         'custdata_custcode_btn',
                         'acctrec_credit_limit_numctrl','rentals_add_button',
                         'acctrec_freeze_charge_checkbox',
                         'acctrec_invdetail_radiobox',
                         'shipto_addrlookup_btn','Change Main Address Button',
                         'custdata_prefix_btn','custdata_fname_txtctrl',
                         'custdata_midInitial_txtctrl','custdata_lname_txtctrl',
                         'custdata_suffix_txtctrl','SaveButton','AddButton',
                         'UndoButton','DeleteButton','custdata_refresh_button']
                               
        for name in toEnable_list:
            
            if re.search('(fname|lname|suffix)',name,re.I):
                pass
            
            enabled = True
            
            if self.startFrom is not None:
                enabled = False    
            else:
                print('+++')
            try:    
                wx.FindWindowByName(name).EnableCtrl(enable=enabled)
            except:
                pout.v(name)
           
#---------- Accounting            
        AcctTab = wx.FindWindowByName('Customers_AcctsRecTab')
        AcctTab.OnLoad(event='')
      
        wx.FindWindowByName('Change Main Address Button').EnableCtrl(enable=enabled)
#---------------- Loading Notes Tab

#------------ Loading Transactions Tab

        main_addr0 = wx.FindWindowByName('custdata_addr_acct_num_txtctrl1').GetCtrl()
        
        addr_choice = []
        
        if main_addr0 is not None and len(main_addr0) > 0:
            query = """SELECT address0, city, state, unit 
                       FROM address_accounts 
                       WHERE addr_acct_num=(?)"""
            data = (main_addr0,)
            returnd = SQConnect(query, data).ONE()
                
            (address0d, cityd,statd,unitd) = returnd
            if unitd is None:
                main_addr = '{}    {} UNIT {}, {}, {}'.format(main_addr0,address0d,unitd,cityd,statd)
            else:
                main_addr = '{}    {}, {}, {}'.format(main_addr0,address0d,cityd,statd)
            
            addr_choice.append(main_addr)
            
#------------- Loading Rentals Tab
        lc = wx.FindWindowByName('rentals_listctrl')
        lc.OnLoad(custNum=custNumber)
        
    
            
        named = 'transactions_addr_combobox'
        item = wx.FindWindowByName(named)
        
        item.SetItems(addr_choice)
        item.Enable()
        
        print("<<< GOOD KITTY CAT THINGS >>>")        
        return
        
        
    def OnSave(self, event):
        custNumber = wx.FindWindowByName('custNumber_txtctrl').GetCtrl()
        
        # ------ Saving CustomerData & Rentals Tab Info
        table_list = ['customer_basic_info','customer_sales_options',
                      'customer_accts_receivable','customer_shipto_info',
                      'customer_notes','customer_security']
        
        HUD.QueryOps().CheckEntryExist('cust_num', custNumber, table_list)
        # lc = wx.FindWindowByName('custdata_phone_listctrl').Save(custNumber) 
        
        debug = False
        custdata_txtctrl_list = [('custName_txtctrl'), #'customer_basic_info','full_name'),
                                 ('custdata_addr_acct_num_txtctrl1'), #'customer_basic_info','address_acct_num'),
                                 ('custdata_prefix_btn'), #'customer_basic_info','prefix'),
                                 ('custdata_fname_txtctrl'),#'customer_basic_info','first_name'),
                                 ('custdata_midInitial_txtctrl'), #'customer_basic_info','middle_initial'),
                                 ('custdata_lname_txtctrl'), #'customer_basic_info','last_name'),
                                 ('custdata_suffix_txtctrl'), #'customer_basic_info','suffix'),
                                 ('custdata_email_txtctrl1'), #'customer_basic_info','email_addr'),
                                 ('custdata_taxExemptID_txtctrl1'), #'customer_basic_info','tax_exempt_number'),
                                 ('custdata_contact1_txtctrl'), #'customer_basic_info','contact1'),
                                 ('custdata_contact2_txtctrl'), #'customer_basic_info','contact2'),
                                 ('custdata_stmt_terms_txtctrl'), #'customer_basic_info','statement_terms'),
                                 ('custdata_date_added_datectrl'), #'customer_basic_info','date_added'),
                                 ('custdata_last_maintained_datectrl'), #'customer_basic_info','last_maintained'),
                                 ('custdata_last_sale_datectrl'), #'customer_basic_info','last_sale'),
                                 ('custdata_birthday_txtctrl'), #'customer_basic_info','birthday'),
                                 ('custdata_custcode_btn'), #'customer_basic_info','typecode'),
                                 ('custdata_acct_type_btn'), #'customer_basic_info','account_type'),
                                 ('custdata_alt_post_acct_txtctrl')] #'customer_basic_info','alt_post_acct')]
                                 
        salesOpt_list = [('salesopt_taxExempt_checkbox'), #'customer_sales_options','tax_exempt'),
                         ('salesopt_employee_btn'), #'customer_sales_options','salesperson'),
                         ('salesopt_noChecks_checkbox'), #'customer_sales_options','no_checks'),
                         ('salesopt_no_discounts_radiobtn'), #'customer_sales_options','no_discount'),
                         ('salesopt_fixed_discount_numctrl'), #'customer_sales_options','discount_amt'),
                         ('salesopt_fixed_discount_radiobtn'), #'customer_sales_options','fixed_discount'),
                         ('salesopt_clerkMessage_txtctrl')] #'customer_sales_options','pos_clerk_message')]
                                 
        custrec_list = [('acctrec_credit_limit_numctrl'), #'customer_accts_receivable','credit_limit'),
                        ('acctrec_freeze_charge_checkbox'), #'customer_accts_receivable','freeze_charges'),
                        ('acctrec_invdetail_radiobox')] #'customer_accts_receivable','print_invoice_detail_on_statement')]
                                 
        shipto_list = [('shipto_name_txtctrl'), #'customer_shipto_info','name'),
                       ('shipto_phone_txtctrl'), #'customer_shipto_info','phone'),
                       ('shipto_address_acct_num_txtctrl'), #'customer_shipto_info','address_acct_num'),
                       ('shipto_comments_txtctrl'), #'customer_shipto_info','comments'),
                       ('shipto_shipmethod_btn')] #'customer_shipto_info','ship_by')]
                       
        notes_list = [('notes_notes_txtctrl')]#,'customer_notes','notes')]
        
        list_of_lists = [custdata_txtctrl_list, salesOpt_list, custrec_list, shipto_list, notes_list]
        for listd in list_of_lists:
            for name in listd:
                pout.v(f"Current Save Item : {name}")
                item = wx.FindWindowByName(name)
                item.OnSave('cust_num',custNumber)
        #     debug = True
                                
        #     fieldSet, dataSet, table = HUD.QueryOps().Commaize(listd)

        #     if len(dataSet) > 0:
        #         query = '''UPDATE {} 
        #                    SET {}
        #                    WHERE cust_num=(?)'''.format(table,fieldSet)

        #         data = dataSet + [custNumber,]
        #         call_db = SQConnect(query, data).ONE()
             
            
            
        # lc = wx.FindWindowByName('rentals_listctrl')
        # lc.Save(custNumber, debug=True)
        
                
        HUD.RecordOps('customer_basic_info').UpdateRecordDate('last_maintained','cust_num',
                             custNumber,'custdata_last_maintained_datectrl') 
        
        wx.CallAfter(self.OnLoad, event=custNumber)
                
                        
#------ SalesOptions Tab Save Area
#-------------- Accounts Receivable Tab
#--------------- Saving ShipTo Tab
#----------- Saving Notes Tab
 
 
 
        
    
    def OnUndo(self, event):
        custNumber = wx.FindWindowByName('custNumber_txtctrl').GetValue()
        wx.CallAfter(self.OnLoad, event=custNumber)
        
        
    def OnAdd(self, event):
        custdata_txtctrl_list = [('custNumber_txtctrl'),
                                 ('custName_txtctrl'), #'customer_basic_info','full_name'),
                                 ('custdata_addr_acct_num_txtctrl1'), #'customer_basic_info','address_acct_num'),
                                 ('custdata_prefix_btn'), #'customer_basic_info','prefix'),
                                 ('custdata_fname_txtctrl'),#'customer_basic_info','first_name'),
                                 ('custdata_midInitial_txtctrl'), #'customer_basic_info','middle_initial'),
                                 ('custdata_lname_txtctrl'), #'customer_basic_info','last_name'),
                                 ('custdata_suffix_txtctrl'), #'customer_basic_info','suffix'),
                                 ('custdata_email_txtctrl1'), #'customer_basic_info','email_addr'),
                                 ('custdata_taxExemptID_txtctrl1'), #'customer_basic_info','tax_exempt_number'),
                                 ('custdata_contact1_txtctrl'), #'customer_basic_info','contact1'),
                                 ('custdata_contact2_txtctrl'), #'customer_basic_info','contact2'),
                                 ('custdata_stmt_terms_txtctrl'), #'customer_basic_info','statement_terms'),
                                 ('custdata_date_added_datectrl'), #'customer_basic_info','date_added'),
                                 ('custdata_last_maintained_datectrl'), #'customer_basic_info','last_maintained'),
                                 ('custdata_last_sale_datectrl'), #'customer_basic_info','last_sale'),
                                 ('custdata_birthday_txtctrl'), #'customer_basic_info','birthday'),
                                 ('custdata_custcode_btn'), #'customer_basic_info','typecode'),
                                 ('custdata_acct_type_btn'), #'customer_basic_info','account_type'),
                                 ('custdata_alt_post_acct_txtctrl')] #'customer_basic_info','alt_post_acct')]
                                 
        salesOpt_list = [('salesopt_taxExempt_checkbox'), #'customer_sales_options','tax_exempt'),
                         ('salesopt_employee_btn'), #'customer_sales_options','salesperson'),
                         ('salesopt_noChecks_checkbox'), #'customer_sales_options','no_checks'),
                         ('salesopt_no_discounts_radiobtn'), #'customer_sales_options','no_discount'),
                         ('salesopt_fixed_discount_numctrl'), #'customer_sales_options','discount_amt'),
                         ('salesopt_fixed_discount_radiobtn'), #'customer_sales_options','fixed_discount'),
                         ('salesopt_clerkMessage_txtctrl')] #'customer_sales_options','pos_clerk_message')]
                                 
        custrec_list = [('acctrec_credit_limit_numctrl'), #'customer_accts_receivable','credit_limit'),
                        ('acctrec_freeze_charge_checkbox'), #'customer_accts_receivable','freeze_charges'),
                        ('acctrec_invdetail_radiobox')] #'customer_accts_receivable','print_invoice_detail_on_statement')]
                                 
        shipto_list = [('shipto_name_txtctrl'), #'customer_shipto_info','name'),
                       ('shipto_phone_txtctrl'), #'customer_shipto_info','phone'),
                       ('shipto_address_acct_num_txtctrl'), #'customer_shipto_info','address_acct_num'),
                       ('shipto_comments_txtctrl'), #'customer_shipto_info','comments'),
                       ('shipto_shipmethod_btn')] #'customer_shipto_info','ship_by')]
                       
        notes_list = [('notes_notes_txtctrl')]#,'customer_notes','notes')]

        list_of_lists = [custdata_txtctrl_list, salesOpt_list, custrec_list, shipto_list, notes_list]
        for listd in list_of_lists:
            for name in listd:
                pout.v(f"Current Save Item : {name}")
                item = wx.FindWindowByName(name)
                item.Clear()
        dial = wx.MessageDialog(None, 'Auto Create Customer Number?', 'Question',
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

        custNum = wx.FindWindowByName('custNumber_txtctrl')
        if dial.ShowModal() == wx.ID_YES:
            chk = HUD.AccountOps().AcctNumAuto('customer_basic_info','cust_num',fill0s=10)
            custNum.SetValue(chk)     
        else:
            custNum.SetFocus()

        # debug = True
        # CustomerAdd_D = HUD.CustomerAddDialog(self, title="Add Customer")
        # CustomerAdd_D.ShowModal()
        
        # try:
            
        #     self.custPicked = CustomerAdd_D.itemPicked
        
        # except:
            
        #     CustomerAdd_D.Destroy()
            
        #     return
        
        # self.custPicked = CustomerAdd_D.itemPicked
        # print(("Customer Add D : ",self.custPicked)) 
        # CustomerAdd_D.Destroy()
   
        # #custNumber = wx.FindWindowByName('custNumber_txtctrl').SetValue(self.custPicked)
        # wx.FindWindowByName('custNumber_txtctrl').SetCtrl(self.custPicked)
        

        # customer_tables = ['customer_accts_receivable','customer_basic_info',
        #                    'customer_notes','customer_sales_options',
        #                    'customer_security','customer_shipto_info']
        
        # HUD.QueryOps().CheckEntryExist('cust_num',self.custPicked,customer_tables)
        
        # wx.CallAfter(self.OnLoad, event=self.custPicked)
        
        
    
        
    def OnDelete(self, event):
        addr = wx.FindWindowByName('custdata_addressText_text').GetCtrl()
        custNumber = wx.FindWindowByName('custNumber_txtctrl').GetCtrl()
        delrec = wx.MessageBox('Delete Account #{0} \n{1}'.format(custNumber,addr),
                               'Delete Record', wx.YES_NO)
        
        if delrec == wx.YES:
            customer_tables = ['customer_accts_receivable','customer_basic_info',
                               'customer_notes','customer_sales_options',
                               'customer_security','customer_shipto_info']
            
            UO(customer_tables).DeleteEntryRecord('cust_num',custNumber)
       
        
    def OnExitButton(self, event):
        """ Exit """ 
        if self.startFrom == 'POS':
            dlg = wx.FindWindowByName('CustDialog')
            dlg.Close()
        else:
            framed = wx.FindWindowByName('Customer_Frame')
            framed.Close()
        

class CustomerScreen(wx.Frame):
    def __init__(self,From=None,CustNum=None):
        style = wx.DEFAULT_FRAME_STYLE & (~wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX) & (~wx.MINIMIZE_BOX)
        wx.Frame.__init__(self, None, -1, "RHP Customer Management", size=(1200, 750), style=style)
        
        
        self.panel_one = StartPanel(self,From=From,CustNum=CustNum)
       
        #wx.lib.inspection.InspectionTool().Show()

 
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel_one, 1, wx.EXPAND)
        
        self.SetSizer(self.sizer)
        
 

        self.Layout()

class CustDialog(wx.Dialog):
    def __init__(self, *args, **kwargs): 
        From = kwargs.pop('From')
        CustNum = kwargs.pop('CustNum')
        kwargs['size'] = (1200, 700)
        super(CustDialog, self).__init__(self, *args, **kwargs) 
        
        self.SetName('CustDialog')
        self.panel_one = StartPanel(self, From=From, CustNum=CustNum)
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel_one, 1, wx.EXPAND)
        
        self.SetSizer(self.sizer)
       
        
         
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = CustomerScreen()
    frame.Centre()
    frame.SetName('Customer_Frame')
    frame.Show()
    app.MainLoop()        
