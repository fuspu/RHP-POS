#!/usr/bin/python2
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
import xml.etree.cElementTree as ET
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from button_stuff import ButtonOps
import wx.lib.inspection
import handy_utils as HUD
from operator import itemgetter
import time

class FindAddressLookupDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super(FindAddressLookupDialog, self).__init__(*args, **kwargs)
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        
        level1_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        box = wx.StaticBox(self, -1, label='Address Search')
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        
        ctrl = HUD.RH_TextCtrl(self, -1, name='addrSearch_txtctrl', size=(260,-1),style=wx.TE_PROCESS_ENTER)
        ctrl.Bind(wx.EVT_TEXT_ENTER, self.OnSearchButton)
        ctrl.SetFocus()
        btn = HUD.RH_Button(self, -1, label='Search', name='addrSearch_button')
        btn.Bind(wx.EVT_BUTTON, self.OnSearchButton)
        
        boxSizer.Add(ctrl, 0, wx.ALL, 3)
        boxSizer.Add(btn, 0, wx.ALL, 3)
        
        level1_Sizer.Add(boxSizer, 0, wx.ALL, 3)
        
        level1a_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self, -1, label='', name='addrSearch_loading_text')
        level1a_Sizer.Add(text,0)
         
        level2_Sizer = wx.BoxSizer(wx.VERTICAL)
        
        lc = HUD.RH_OLV(self, -1, name='addrSearch_lc', size=(760,465), style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        lc.SetColumns([
                       ColumnDefn('Account #', 'center', 120, 'acctNum'),
                       ColumnDefn('Address 1', 'left', 220, 'address1d'),
                       ColumnDefn('Address 2', 'left', 150, 'address2d'),
                       ColumnDefn('City', 'left', 130, 'cityd'),
                       ColumnDefn('State','left', 90, 'stated')
                      ])

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
        if addr_search:
            cnt = addr_search.count(' ')
            if cnt > 0:
                revised_search = re.sub(' ','.*',addr_search)
                whereFrom = 'address0'
            else:
                revised_search = addr_search
                whereFrom = 'street_name'
        
        query = "SELECT addr_acct_num,address0,address2,address3,city,state from address_accounts where {0} LIKE (?) OR zipcode=(?)".format(whereFrom)
        data = (revised_search,revised_search,)
        returnd = HUD.SQConnect(query, data).ALL()
       
        lcname = 'addrSearch_lc'
        lc = wx.FindWindowByName(lcname)
        lc.ClearCtrl()
        records_returnd = len(returnd)
        if records_returnd != 1:
            plural = 'es'
        else:
            plural = ''
                    
        wx.FindWindowByName('addrSearch_loading_text').SetLabel('Found '+str(records_returnd)+' Address'+plural)
        for addr_acct_numd, address1d, address2d, address3d, cityd, stated in returnd:
            setdict = {'acctNum':addr_acct_numd,'address1d':address1d,'address2d':address2d,'cityd':cityd,'stated':stated}
            wx.FindWindowByName(lcname).AddEntry(setdict)
                        
    def OnChooserCellLeftClick(self, evt):
        item_id,objText = HUD.EventOps().LCGetSelected(evt)
        self.addrPicked = objText
        self.Close()
        

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
                ctrl = HUD.RH_TextCtrl(self, -1, name=name, size=(sized,-1),style=wx.TE_PROCESS_ENTER)
                ctrl.Bind(wx.EVT_KILL_FOCUS, HUD.EventOps().Capitals)
            if 'combobox' in name:
                ctrl = HUD.RH_MComboBox(self, -1, name=name, choices=sized)                 
            
            boxSizer.Add(ctrl, 0)
            
            level1_Sizer.Add(boxSizer, 0, wx.ALL, 3)
                
        
        level2_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        ctrl = HUD.RH_TextCtrl(self, -1, name='addressMaint_address0_txtctrl', size=(400,-1), style=wx.TE_READONLY)
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
        ctrl = HUD.RH_TextCtrl(self, -1, name='addressMaint_address2_txtctrl', size=(400, -1))
        ctrl.Bind(wx.EVT_KILL_FOCUS, HUD.EventOps().Capitals)
        boxSizer.Add(ctrl, wx.HORIZONTAL)
        level3_Sizer.Add(boxSizer, 0)
        
        level4_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        box = wx.StaticBox(self, -1, label='Address 3')
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        ctrl = HUD.RH_TextCtrl(self, -1, name='addressMaint_address3_txtctrl', size=(400, -1))
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
                    ctrl = HUD.RH_MTextCtrl(self, -1, name=name, formatcodes="!", size=(sized, -1))
                if 'city' in name:
                    ctrl = HUD.RH_TextCtrl(self, -1, name=name, size=(sized, -1))
                    ctrl.Bind(wx.EVT_KILL_FOCUS, HUD.EventOps().Capitals)
                if 'zipcode' in name:
                    ctrl = HUD.RH_MTextCtrl(self, -1, name=name, size=(sized,-1), mask = '#{5}')
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
   



class StartPanel(wx.Panel):
    def __init__(self,parent, debug=False):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
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
                    ctrl = HUD.RH_MTextCtrl(self, -1, name=name, size=(sized, -1),formatcodes='!',style=wx.TE_PROCESS_ENTER)
                    ctrl.SetFocus()
                else:
                    ctrl = HUD.RH_TextCtrl(self, -1, name=name, size=(sized, -1))
                
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
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
        FindAddrLookupD = FindAddressLookupDialog(self, title="Find Address Form", size=(1000,600), style=style)
        FindAddrLookupD.ShowModal()
    
        try:
            FindAddrLookupD.addrPicked
        except:
            FindAddrLookupD.Destroy()
            return
            
        self.addrPicked = FindAddrLookupD.addrPicked
        
        print("Address Lookup D : ",self.addrPicked) 
        FindAddrLookupD.Destroy()
        wx.CallAfter(self.OnLoad, event=self.addrPicked)    
    
    
    
    
    def OnSave(self, event):
        acctNum = wx.FindWindowByName('acctNumber_txtctrl').GetCtrl()
        table_list = ['address_accounts']
        query = 'SELECT count(*) FROM address_accounts WHERE addr_acct_num=(?)'
        data = (acctNum,)
        returnd = HUD.SQConnect(query,data).ONE()
            
        
        HUD.QueryOps().CheckEntryExist('addr_acct_num',acctNum,table_list)
        
        
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
            returnd = HUD.SQConnect(query,data).ONE()
            
            
            
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
            
        for i in ['SaveButton', 'DeleteButton','UndoButton']:
            wx.FindWindowByName(i).EnableCtrl()
        
        new_acctNum = HUD.AccountOps().AcctNumAuto('address_accounts','addr_acct_num')
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
            
            HUD.RecordOps(table_list).DeleteEntryRecord('addr_acct_num',acctNum)
            
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
            returnd = HUD.SQConnect(query,data).ONE()
            value = returnd[0]
            
            
            wx.FindWindowByName(name).SetCtrl(value)
                    
        
            
        
        





class CustomerScreen(wx.Frame):
    def __init__(self, debug=False):
        style = wx.DEFAULT_FRAME_STYLE & (~wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX) & (~wx.MINIMIZE_BOX)
        wx.Frame.__init__(self, None, -1, "RHP Customer Management", size=(1200,800), style=style)
        
        self.panel_one = StartPanel(self)
       
        #wx.lib.inspection.InspectionTool().Show()

 
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel_one, 1, wx.EXPAND)
        
        self.SetSizer(self.sizer)
        
 

        self.Layout()

       
  
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = CustomerScreen()
    frame.Centre()
    frame.SetName('Address_Maintenance_Frame')
    frame.Show()
    app.MainLoop()        
