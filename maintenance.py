#!/usr/bin/env python2
#
#
#
#
#import wxversion
#wxversion.select('2.8')

import wx,re,os 
#import wx.calendar as cal
import wx.grid as gridlib
import sys
import faulthandler
import sqlite3
import json
import pout
import xml.etree.cElementTree as ET
import time
import datetime
from ObjectListView import ObjectListView, ColumnDefn
from wx.lib.masked import TimeCtrl
import wx.lib.masked as masked
from decimal import Decimal, ROUND_HALF_UP
import wx.lib.inspection
import handy_utils as HUD
from button_stuff import ButtonOps
from db_related import LookupDB, SQConnect

 
class GeneralInfoTab(wx.Panel):
    def __init__(self, parent, size=(500,500), debug=False):
        """ General Info Tab """    
        wx.Panel.__init__(self,parent=parent, id=wx.ID_ANY)
        self.SetName('Maintenance_GeneralInfoTab')
        self.LSL = HUD.LoadSaveList()

        MainSizer = wx.BoxSizer(wx.VERTICAL)
        Row1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        Row_underSizer = wx.BoxSizer(wx.HORIZONTAL)
        Row_under2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        Row_under3Sizer = wx.BoxSizer(wx.HORIZONTAL)
        Col1Sizer = wx.BoxSizer(wx.VERTICAL)
        Col3Sizer = wx.BoxSizer(wx.VERTICAL)
        
        name = 'geninfo_storenum_txtctrl'
        tc = HUD.RH_TextCtrl(self, -1, name=name, size=(85, -1), style=wx.TE_PROCESS_ENTER)
        tc.SetHint('StoreNum')
        tc.tableName = 'basic_store_info'
        tc.fieldName = 'store_num'
        tc.Bind(wx.EVT_TEXT_ENTER, self.onLoad)
        self.LSL.Add(name)
        Row_under3Sizer.Add(tc, 0, wx.ALL, 3)
        
        saveicon = HUD.RH_Icon(self, -1, icon='save', style=wx.BORDER_NONE)
        saveicon.Bind(wx.EVT_BUTTON, self.onSave)
        
        Row_under3Sizer.Add(saveicon, 0, wx.ALL, 3)
        Col1Sizer.Add(Row_under3Sizer, 0, wx.ALL, 3)
        
    
        name = 'geninfo_storename_txtctrl'
        tc = HUD.RH_TextCtrl(self, -1, name=name, size=(300, -1))
        tc.SetHint('Store Name')
        tc.tableName = 'basic_store_info'
        tc.fieldName = 'name'
        self.LSL.Add(name)
        Col1Sizer.Add(tc, 0, wx.ALL, 3)

        name = 'geninfo_address1_txtctrl'
        tc = HUD.RH_TextCtrl(self, -1, name=name, size=(300, -1))
        tc.SetHint('Store Address Line 1')
        tc.tableName = 'basic_store_info'
        tc.fieldName = 'address1'
        self.LSL.Add(name)
        Col1Sizer.Add(tc, 0, wx.ALL, 3)

        name = 'geninfo_address2_txtctrl'
        tc = HUD.RH_TextCtrl(self, -1, name=name, size=(300, -1))
        tc.SetHint('Store Address Line 2')
        tc.tableName = 'basic_store_info'
        tc.fieldName = 'address2'
        self.LSL.Add(name)
        Col1Sizer.Add(tc, 0, wx.ALL, 3)

        name = 'geninfo_city_txtctrl'
        tc = HUD.RH_TextCtrl(self, -1, name=name, size=(190,-1))
        tc.SetHint('City')
        tc.tableName = 'basic_store_info'
        tc.fieldName = 'city'
        self.LSL.Add(name)
        Row_underSizer.Add(tc, 0, wx.ALL, 3)
        
        name = 'geninfo_state_txtctrl'
        tc = HUD.RH_MTextCtrl(self, -1, name=name, size=(75, -1), mask='CC', formatcodes='!')
        tc.SetHint('XX')
        tc.tableName = 'basic_store_info'
        tc.fieldName = 'state'
        self.LSL.Add(name)
        Row_underSizer.Add(tc, 0, wx.ALL, 3)

        name = 'geninfo_zipcode_txtctrl'
        tc = HUD.RH_MTextCtrl(self, -1, name=name, size=(90, -1), mask='#####')
        tc.SetHint('Zipcode')
        tc.tableName = 'basic_store_info'
        tc.fieldName = 'zip'
        self.LSL.Add(name)
        Row_underSizer.Add(tc, 0, wx.ALL, 3)
        Col1Sizer.Add(Row_underSizer, 0, wx.ALL, 3)

        name = 'geninfo_phone_txtctrl'
        tc = HUD.RH_MTextCtrl(self, -1, name=name, size=(150, -1), autoformat='USPHONEFULLEXT')
        tc.SetHint('0000000000')
        tc.tableName = 'basic_store_info'
        tc.fieldName = 'phone1'
        self.LSL.Add(name)
        Row_under2Sizer.Add(tc, 0, wx.ALL, 3)

        name = 'geninfo_fax_txtctrl'
        tc = HUD.RH_MTextCtrl(self, -1, name=name, size=(120, -1), autoformat='USPHONEFULLEXT')
        tc.tableName = 'basic_store_info'
        tc.fieldName = 'fax'

        tc.SetHint('0000000000')
        
        self.LSL.Add(name)
        Row_under2Sizer.Add(tc, 0, wx.ALL, 3)
        Col1Sizer.Add(Row_under2Sizer, 0, wx.ALL, 3)

        name = 'geninfo_website_txtctrl'
        tc = HUD.RH_TextCtrl(self, -1, name=name, size=(300, -1))
        tc.SetHint('http://')
        tc.tableName = 'basic_store_info'
        tc.fieldName = 'website'
        self.LSL.Add(name)
        Col1Sizer.Add(tc, 0, wx.ALL, 3)

        slideSizer = wx.BoxSizer(wx.HORIZONTAL)
        name = 'geninfo_logoLoc_filectrl'
        ctrl = HUD.RH_FilePickerCtrl(self, -1, 
                                     name=name,
                                     message='Please Select Logo Location',
                                     wildcard='Images (*.jpg,*.png,*.gif)|*.jpg;*.gif;*.png',
                                     size=(300, -1),
                                     style=wx.FLP_DEFAULT_STYLE)
        self.LSL.Add(name)                                              

        st = wx.StaticText(self, -1, label='  Logo size: 90px x 90px \n  File Extensions: jpg, gif, png')
        st.SetForegroundColour(wx.Colour(169,169,169))
        Col1Sizer.Add(st, 0)
        
        ctrl.Bind(wx.EVT_FILEPICKER_CHANGED, self.LogoPreview)
        ctrl.tableName = 'basic_store_info'
        ctrl.fieldName = 'logo'
        slideSizer.Add(ctrl, 0, wx.ALL, 3)
        
        image = wx.Image(ButtonOps().Icons('empty'), wx.BITMAP_TYPE_ANY)
        imageBitmap = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(image), name='geninfo_logoLoc_image')
        
        slideSizer.Add(imageBitmap, 0, wx.ALL, 3)
        Col1Sizer.Add(slideSizer, 0, wx.ALL, 3)
        
        name = 'geninfo_printonforms_checkbox'
        cb = HUD.RH_CheckBox(self, -1, 
                         name=name,
                         label='print on forms')
        cb.tableName = 'basic_store_info'                         
        cb.fieldName = 'print_on_forms'
        self.LSL.Add(name)
        Col3Sizer.Add(cb, 0)
        
        latecharge_box = wx.StaticBox(self, -1, label='Late Charge')
        latecharge_boxSizer = wx.StaticBoxSizer(latecharge_box, wx.HORIZONTAL)
        name = 'geninfo_latecharge_numctrl'
        numctrl = HUD.RH_NumCtrl(self, -1, 
                                 value=0, 
                                 name=name, 
                                 integerWidth=3, 
                                 fractionWidth=2)
        numctrl.tableName = 'basic_store_info'                                 
        numctrl.fieldName = 'late_charge'
        self.LSL.Add(name)

        latecharge_boxSizer.Add(numctrl, 0,wx.ALL,5)
        
        Col3Sizer.Add(latecharge_boxSizer, 0)
        
        Row1Sizer.Add(Col1Sizer, 0, wx.ALL, 3)
        Row1Sizer.Add(Col3Sizer, 0)
        
        MainSizer.Add(Row1Sizer, 0, wx.ALL|wx.EXPAND, 10)
        self.SetSizer(MainSizer, 0)
        self.Layout()
        

        #wx.CallAfter(self.onLoad, event="")

    def LogoPreview(self, event):
        value = wx.FindWindowByName('geninfo_logoLoc_filectrl').GetCtrl()
        try:
            img = wx.Image(value, wx.BITMAP_TYPE_ANY)
            image = wx.FindWindowByName('geninfo_logoLoc_image')
            image.SetBitmap(wx.Bitmap(img))
            image.Refresh()
        except:
            pass

    def onLoad(self, event):
        storeNum = wx.FindWindowByName('geninfo_storenum_txtctrl').GetCtrl()
        exists = HUD.QueryOps().QueryCheck('basic_store_info', queryWhere='store_num', queryData=storeNum)
        if exists:
            for name in self.LSL.Get():
                    if not 'storenum' in name:
                        item = wx.FindWindowByName(name)
                        item.OnLoad('store_num',storeNum)
                    
            self.LogoPreview(event='')

    def onSave(self, event):
        save_list = self.LSL.Get()
        storeNum = wx.FindWindowByName('geninfo_storenum_txtctrl').GetCtrl()
        for name in save_list:
            pout.v(f'Save Name : {name}')
            item = wx.FindWindowByName(name)
                
            if 'storenum' in name:
                HUD.QueryOps().CheckEntryExist('store_num', storeNum, [item.tableName,])
            else:
                item.OnSave('store_num', storeNum)    
        

class InventoryMaintenanceTab(wx.Panel):
    def __init__(self, parent, size=(500,500), debug=False):
        """ Customer Data Tab """    
        wx.Panel.__init__(self,parent=parent, id=wx.ID_ANY)
        
        self.SetName('InventoryMaintenanceTab')
        
        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        notebook = wx.Notebook(self, wx.ID_ANY,name='InventoryTab_Notebook')
        tabOne = GeneralDetailsTab(notebook)
        tabTwo = PriceOptionsTab(notebook)
        tabThree = MarginTab(notebook)
        tabFour = DiscountOptionsTab(notebook)
        tabFive = CloseoutsTab(notebook)
        
        notebook.AddPage(tabOne, "General Details")
        notebook.AddPage(tabTwo, "Price Options")
        notebook.AddPage(tabThree, "Margin")
        notebook.AddPage(tabFour, 'Discounts')
        notebook.AddPage(tabFive, 'Closeouts')
        
        MainSizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(MainSizer, 0)
        
        self.Layout()
        
    
class MarginTab(wx.Panel):
    def __init__(self, parent, size=(500,500), debug=False):
        """ Margin Tab """
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetName('MarginTab')
        
        self.rbox = HUD.RH_RadioBox(self, -1, 
                           choices=['General','By Cost','By Category'],
                           name='generalMargin_control_rbox', 
                           label='Figuring Initial Starting Margin')
        self.rbox.tableName = 'item_margin'
        self.rbox.fieldName = 'starting_margin_control'
        self.rbox.Bind(wx.EVT_RADIOBOX, self.onBoxChoice)
        
        notebook = wx.Notebook(self, wx.ID_ANY,name='MarginTab_Notebook')
        tabOne = GeneralMarginTab(notebook)
        tabTwo = ByCostTab(notebook)
        tabThree = ByCategoryTab(notebook)
        
        notebook.AddPage(tabOne, "General")
        notebook.AddPage(tabTwo, "By Cost")
        notebook.AddPage(tabThree, "By Category")
        
        MainSizer.Add(self.rbox, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        MainSizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)
        
        
        
        self.SetSizer(MainSizer, 0)
        self.Layout()
    
    def onBoxChoice(self, event):
        idxselection = self.rbox.GetSelection()
        selection = self.rbox.GetStringSelection()
        notebook = wx.FindWindowByName('MarginTab_Notebook')
        tabCount = notebook.GetPageCount()
        notebook.SetSelection(idxselection)    
        #print("Radio Box CHoice : ",selection)
    
class GeneralMarginTab(wx.Panel):
    def __init__(self, parent, size=(500,500), debug=False):
        """General Margin Tab."""
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.SetName('Margin_GeneralMarginTab')
        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        savebutton = HUD.RH_Icon(self, -1, icon='save', style=wx.BORDER_NONE)
        savebutton.Bind(wx.EVT_BUTTON, self.OnSave)

        txt = wx.StaticText(self, -1, label='General Margin')
        self.margin = HUD.RH_NumCtrl(self, -1, 
                              value=0.00, 
                              name='margin_generalmargin_numctrl', 
                              integerWidth=4,
                              fractionWidth=2)
        self.margin.tableName = 'item_margin'
        self.margin.fieldName = 'general_margin'

        MainSizer.Add(txt, 0, wx.ALL|wx.EXPAND|wx.CENTER, 3)
        MainSizer.Add(self.margin, 0, wx.ALL, 3)
        MainSizer.Add(savebutton, 0, wx.ALL, 3)
        self.SetSizer(MainSizer, 0)
        self.Layout()

        wx.CallAfter(self.OnLoad, event='')
        
    def OnLoad(self, event):
        returnd = self.margin.OnLoad('abuser', 'rhp')
        if returnd is not None:
            self.margin.SetCtrl(returnd)

    def OnSave(self, event):
        HUD.QueryOps().CheckEntryExist('abuser','rhp',['item_margin'])
        save_list = ['generalMargin_control_rbox', 'margin_generalmargin_numctrl']
        for name in save_list:
            item = wx.FindWindowByName(name)
            item.OnSave('abuser', 'rhp')
            

class ByCostTab(wx.Panel):
    def __init__(self, parent, size=(300,300), debug=False):
        """ General Margin """
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        self.SetName('Margin_ByCostTab')
        
        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        lc = HUD.RH_OLV(self, -1, size=(500,200), name='maint_margin_bycost_lc', style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        lc.SetColumns([
                      ColumnDefn('Label','center',100, 'labeld'),
                      ColumnDefn('Greater than >','center',125,'gtd'),
                      ColumnDefn('< Less Than','center',125,'ltd'),
                      ColumnDefn('Margin','center',175,'margind')
        ])
        
        lc.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemChoose)
        
        level2Sizer = wx.BoxSizer(wx.VERTICAL)
        
        action_list = [('Label', 'maint_margin_bycost_label_txtctrl',120, 'margin_by_cost', 'label'),
                       ('Greater Than > ', 'maint_margin_bycost_gt_numctrl',90,'margin_by_cost','greater_than'),
                       ('Less Than <' ,'maint_margin_bycost_lt_numctrl',90, 'margin_by_cost','less_than'),
                       ('Margin ','maint_margin_bycost_margin_numctrl',90, 'margin_by_cost','margin')]

        self.labeltc = HUD.RH_TextCtrl(self, -1, size=(120, -1))
        self.labeltc.SetHint('Label')
        self.gtlt = HUD.RH_ComboBox(self, -1, choices=['<', '>'], size=(90,-1))
        self.margin = HUD.RH_NumCtrl(self, -1, value=0, integerWidth=3, fractionWidth=2, size=(90,-1))

        MainSizer.Add(self.labeltc, 0)
        MainSizer.Add(self.gtlt, 0)
        MainSizer.Add(self.margin, 0)


        # for label, name, sized, tableName, fieldName in action_list:
        #     box = wx.StaticBox(self, -1, label=label)
        #     boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        #     if 'numctrl' in name:
        #         ctrl = HUD.RH_NumCtrl(self, -1, name=name, value='0', integerWidth=3, fractionWidth=2, size=(sized,-1))

        #     if 'txtctrl' in name:
        #         ctrl = HUD.RH_TextCtrl(self, -1, name=name, size=(sized, -1))
        #     ctrl.tableName = tableName
        #     ctrl.fieldName = fieldName                    
        #     boxSizer.Add(ctrl,0, wx.ALL|wx.ALIGN_CENTER, 5)
        #     level2Sizer.Add(boxSizer, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        
        button_list = [('Add','maint_margin_bycost_add_button',self.OnButton),
                      ('Remove','maint_margin_bycost_remove_button',self.OnButton)]
        self.addbutton = HUD.RH_Icon(self, -1, icon='add', style=wx.BORDER_NONE)
        self.addbutton.Bind(wx.EVT_BUTTON, self.OnButton)
        MainSizer.Add(self.addbutton, 0)    
            
        self.rembutton = HUD.RH_Icon(self, -1, icon='delete', style=wx.BORDER_NONE)
        self.rembutton.Bind(wx.EVT_BUTTON, self.OnButton)
            
            #     for label, name, hdlr in button_list:   
            # ctrl = HUD.RH_Button(self, -1, label=label, name=name)
            # ctrl.Bind(wx.EVT_BUTTON, hdlr)
            
            # level2Sizer.Add(ctrl, 0)
                                     
        MainSizer.Add(lc, 0, wx.ALL|wx.EXPAND, 3)
        MainSizer.Add(level2Sizer, 0, wx.ALL|wx.EXPAND, 3)
        
        self.SetSizer(MainSizer, 0)
        self.Layout()
        
        wx.CallAfter(self.OnLoad, event='')
        
    def OnLoad(self, event):
        lc_name = 'maint_margin_bycost_lc'
        lc = wx.FindWindowByName(lc_name)
        lc.Clear()
        setList = []
        query = '''SELECT label, greater_than, less_than, margin 
                   FROM margin_by_cost
                   '''
        data = ''
        returnd = SQConnect(query, data).ALL()
        returnd = LookupDB('margin_by_cost').General('label, greater_than, less_than, margin')
        
        if returnd is not None:
            for labeld, gtd, ltd, margin in returnd:
                setList += [{'labeld' : labeld, 'gtd': gtd, 'ltd': ltd, 'margin': 'margind'}]
                
            item = wx.FindWindowByName(lc_name).SetObjects(setList)

    def OnSave(self):   
        lc = wx.FindWindowByName('maint_margin_bycost_lc')
        objs = lc.GetObjects()

        for line in objs:
            label = lc.GetItem(line, 0).GetText()
            greater_than = lc.GetItem(line, 1).GetText()
            less_than = lc.GetItem(line, 2).GetText()
            margin = lc.GetItem(line, 3).GetText()
            
            HUD.QueryOps().CheckEntryExist('label',label, ['margin_by_cost'])
            
            save_list = [(label,'margin_by_cost','label'),
                         (greater_than,'margin_by_cost','greater_than'),
                         (less_than,'margin_by_cost','less_than'),
                         (margin, 'margin_by_cost','margin')]
                         
            fieldSet, dataSet, table = HUD.QueryOps().Commaize(save_list, typd='vari')
            
            query = '''UPDATE {} 
                       SET {}
                       WHERE label=(?)'''.format(table, fieldSet)
            
            data = dataSet + [label,]
            
            print('query : {}\n data : {}'.format(query, data))           
            returnd = SQConnect(query, data).ONE()
                                               
            
    def OnItemChoose(self, event):            
        pass
    
    def OnButton(self, event):
        obj = event.GetEventObject()
        named = obj.GetName()
        debug=False
        
        active_list = [('Label', 'maint_margin_bycost_label_txtctrl'),
                       ('Greater Than >','maint_margin_bycost_gt_numctrl'),
                       ('Less Than <','maint_margin_bycost_lt_numctrl'),
                       ('Margin','maint_margin_bycost_margin_numctrl')]
        
        print("Button : ",named)
        listctrl = wx.FindWindowByName('maint_margin_bycost_lc')
        if 'add' in named:
           
            line = listctrl.GetItemCount()
        
            for label, name in active_list:
                print("Name : ",name)
                ctrl = wx.FindWindowByName(name)
                value = ctrl.GetValue()
                if not value:
                    ctrl.SetBackgroundColour('RED')     
                    return
                
                print("LIST CTRL : ",listctrl.GetName())
                if '_label_' in name:
                    listctrl.InsertItem(line, str(value))
                    print("Set {0} : {1} on Line {2}".format('Label', value, line))
                
                if '_gt_' in name:
                    listctrl.SetItem(line,1, str(value))
                    print("Set {0} : {1} on Line {2}".format('GT', value, line))
                
                if '_lt_' in name:
                    listctrl.SetItem(line , 2, str(value))
                    print("Set {0} : {1} on Line {2}".format('LT', value, line))
               
                if '_margin_' in name:
                    listctrl.SetItem(line, 3, str(value))
                    print("Set {0} : {1} on Line {2}".format('Margin', value, line))
                
        if 'clear' in named:
            for label, name in active_list:
                print("Clear Name : ",name)
                wx.FindWindowByName(name).ClearCtrl()
        
        if 'remove' in named:
            #lc_name = 'maint_margin_bycost_lc'
            #print "Listctrl Name : ",lc_name
            #listctrl = wx.FindWindowByName(lc_name)
            line = listctrl.GetFirstSelected()
            print("item : ",listctrl)
            
            named = listctrl.GetItemText(line)
            print("Named : ",named)
            
            query = 'DELETE FROM margin_by_cost WHERE label=(?)'
            data = (named,)
            returnd = SQConnect(query, data).ONE()
            
            listctrl.DeleteItem(line)
             
        for label, name in active_list:
            wx.FindWindowByName(name).ClearCtrl()
            
        ctrl = wx.FindWindowByName('maint_margin_bycost_label_txtctrl').SetFocus()


class ByCategoryTab(wx.Panel):
    def __init__(self, parent, size=(500,500), debug=False):
        """ Margin by Category """
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        self.SetName('Margin_ByCategoryTab')
        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        Col1Sizer = wx.BoxSizer(wx.VERTICAL)
        
        col_list = [('Department',125),('Category',125),('Margin',175)]
        grid = gridlib.Grid(self,name='margin_bycategory_grid', style=wx.BORDER_SUNKEN)
        grid.EnableScrolling(True,True)
        grid.DisableDragRowSize()
        grid.SetRowLabelSize(0)
        grid.CreateGrid(1,len(col_list))
        idx = 0
        for label,sized in col_list:
            grid.SetColLabelValue(idx, label)
            grid.SetColSize(idx, sized)
            idx += 1
                
        grid.EnableEditing(True)
        grid.SetLabelFont( wx.Font(wx.FontInfo(9)) )
        
        grid.dept_list = []
        grid.cate_list = []
        
        
        HUD.GridOps(grid.GetName()).GridAlternateColor()
        Col1Sizer.Add(grid, 0, wx.ALL|wx.EXPAND, 3)
        
        
        
        MainSizer.Add(Col1Sizer, 0, wx.ALL|wx.ALIGN_CENTER, 3)
        
        
        
        self.SetSizer(MainSizer, 0)
        self.Layout()        
        
        wx.CallAfter(self.onLoad, event="")
    
    def onLoad(self, event):
        """ Load up By Category Lists """
        
        grid = wx.FindWindowByName('margin_bycategory_grid')
        combo_list = [('department',grid.dept_list),('category',grid.cate_list)]
        
        for field,vari in combo_list: 
            returnd = LookupDB('organizations').Specific('rhp','abuser',field)
            if 'department' in field:
                grid.dept_list = returnd
            if 'category' in field:
                grid.cate_list = returnd
            
        
        pout.v("dept_list : {}".format(grid.dept_list))
        print("cate_list : {}".format(grid.cate_list))
        if returnd is not None:
            grid_list = [('department',grid.dept_list,0,0),('category',grid.cate_list,0,1)]
            for field,vari,x,y in grid_list:
                
                grid.SetCellValue(x,y, field.upper())
                #grid.SetCellEditor(x,y,HUD.GridCellComboBox(vari))
                grid.SetCellEditor(x, y, wx.grid.GridCellChoiceEditor(vari))            

                
class PriceOptionsTab(wx.Panel):
    def __init__(self, parent, size=(500,500), debug=False):
        """ Price Tab """
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        self.SetName('PriceOptionsTab')
        
        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        listboxes = [('Price Schemes','invMaint_priceSchemes_listbox')]
        colLabel_list = [('Name',120),('Scheme',90),('Reduce By',75)]
        
        listctrl = HUD.RH_OLV(self,size=(300,260), name='invMaint_priceSchemes_listctrl', style=wx.LC_REPORT|wx.BORDER_SIMPLE)      
        listctrl.SetColumns([
                            ColumnDefn('Name','left',120,'named'),
                            ColumnDefn('Scheme','center',90,'schemed'),
                            ColumnDefn('Reduce By','center',75,'reduced')
                            ])

        listctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelect)
        idx = 0
        
        explanation = 'Enter a Scheme i.e. \'1-3-10\' According to Starting Margin & Reduced_By will \nset each additional unit qty less by reduced_by percentage separated by \'-\' dashes\n Also \'1-PK-2X\' will result in \'1 & box qty & box qty * 2\''              
        text = wx.StaticText(self,-1,  label=explanation)
        
        editSizer = wx.BoxSizer(wx.HORIZONTAL)
        edit_list = [('Name','invMaint_priceSchemes_listctrl_name_txtctrl'),
                     #('Schemed','invMaint_priceSchemes_listctrl_scheme_txtctrl'),
                     #('Reduce By','invMaint_priceSchemes_listctrl_reduceby_numctrl'),
                     ('Qty','invMaint_priceSchemes_qty1_txtctrl'),
                     ('Operator','invMaint_priceSchemes_opt1_combobox'),
                     ('Margin', 'invMaint_priceSchemes_margin1_txtctrl'),
                     ('Qty','invMaint_priceSchemes_qty2_txtctrl'),
                     ('Operator','invMaint_priceSchemes_opt2_combobox'),
                     ('Margin', 'invMaint_priceSchemes_margin2_txtctrl'),
                     ('Qty','invMaint_priceSchemes_qty3_txtctrl'),
                     ('Operator','invMaint_priceSchemes_opt3_combobox'),
                     ('Margin', 'invMaint_priceSchemes_margin3_txtctrl'),
                     ('Qty','invMaint_priceSchemes_qty4_txtctrl'),
                     ('Operator','invMaint_priceSchemes_opt4_combobox'),
                     ('Margin', 'invMaint_priceSchemes_margin4_txtctrl'),
                     ('Add','invMaint_priceSchemes_listctrl_add_button'),
                     ('Delete','invMaint_priceSchemes_listctrl_delete_button'),
                     ('Clear','invMaint_priceSchemes_listctrl_clear_button')]
                     
        
        for label, name in edit_list:
            box = wx.StaticBox(self, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            if '_reduceby_' in name:
                ctrl = HUD.RH_TextCtrl(self, -1, name=name)
                ctrl.SetToolTip(wx.ToolTip('Enter a Percentage of Margin you wish to Reduce the initial margin by'))
                
            if '_name_' in name:
                ctrl = HUD.RH_MTextCtrl(self, -1, name=name, mask='XXXXXXXXX')
                ctrl.SetToolTip(wx.ToolTip('Enter a Name for the Scheme within 9 characters'))
                ctrl.Bind(wx.EVT_KILL_FOCUS, HUD.EventOps().Capitals)
                
            if '_scheme_' in name:
                ctrl = HUD.RH_TextCtrl(self, -1, name=name)
                ctrl.Bind(wx.EVT_KILL_FOCUS, HUD.EventOps().Capitals)
                #ctrl.SetToolTip(wx.ToolTip('Enter a Scheme i.e. \'1-3-10\' According to Starting Margin & Reduced_By will \nset each additional unit qty less by reduced_by percentage separated by \'-\' dashes\n Also \'1-PK-2X\' will result in \'1 & box qty & box qty * 2\''))     
            
            if 'button' in name:
                ctrl = HUD.RH_Button(self, label=label, name=name)
                ctrl.Bind(wx.EVT_BUTTON, self.onButton)
            
            if 'delete' in name:    
                ctrl.Disable()
                
            if not 'button' in name:
                #boxSizer.Add(ctrl, 0)        
                editSizer.Add(boxSizer, 0)
            else:
                editSizer.Add(ctrl, 0)
        
        MainSizer.Add(listctrl, 0)
        MainSizer.Add(editSizer,0)
        MainSizer.Add(text, 0)
        
        self.SetSizer(MainSizer)
        self.Layout()
    
        wx.CallAfter(self.onLoad, event='')
   
   
    def onLoad(self, event):
        lc_name = 'invMaint_priceSchemes_listctrl'
        listctrl = wx.FindWindowByName(lc_name)
        query = 'SELECT scheme_list,reduce_by,name FROM item_pricing_schemes'
        data = ''
        returnd = SQConnect(query, data).ALL()
        
        idx = 0
        for scheme_list, reduceby, named in returnd:
            setList = [(0,named),(1,scheme_list),(2,str(reduceby))]
            HUD.ListCtrl_Ops(lc_name).LCFill(setList, idx)
            
    
    def OnSave(self):
        print("Pricing Schemes")
        listctrl = wx.FindWindowByName('invMaint_priceSchemes_listctrl')
        count = listctrl.GetItemCount()
        for idx in range(count):
            name_scheme = listctrl.GetItemText(idx)
            print("Get Item {0} : {1}".format(listctrl.GetItem(idx), name_scheme))     
            queryWhere = 'name=(?)'
            queryData = (name_scheme,)
            countd = HUD.QueryOps().QueryCheck('item_pricing_schemes',queryWhere,queryData)
            print("Countd : ",countd)
            if countd == 0:
                name = listctrl.GetItem(idx,0).GetText().strip()
                schemeList = listctrl.GetItem(idx,1).GetText().strip()
                reduceby = listctrl.GetItem(idx,2).GetText()
                print("Name : {0}, Scheme : {1}, ReduceBy : {2}".format(name,schemeList,reduceby))
                query = 'INSERT INTO item_pricing_schemes (name,scheme_list,reduce_by) VALUES ((?),(?),(?))'
                data = (name,schemeList,reduceby,)
                returnd = SQConnect(query, data).ONE()
               
           
    def onItemSelect(self, event):
        delete = wx.FindWindowByName('invMaint_priceSchemes_listctrl_delete_button').Enable()        
                
        
    def onButton(self, event):
        obj = event.GetEventObject()
        named = obj.GetName()
        debug=False
        
        active_list = [('Name','invMaint_priceSchemes_listctrl_name_txtctrl'),
                       ('Schemed','invMaint_priceSchemes_listctrl_scheme_txtctrl'),
                       ('Reduce By','invMaint_priceSchemes_listctrl_reduceby_numctrl')]
        
        print("Button : ",named)
        if 'add' in named:
            listctrl = wx.FindWindowByName('invMaint_priceSchemes_listctrl')
            line = listctrl.GetItemCount()
           
                    
            for label, name in active_list:
                print("Name : ",name)
                ctrl = wx.FindWindowByName(name)
                value = ctrl.GetValue()
                if not value:
                    ctrl.SetBackgroundColour('RED')     
                    return
                
                print("LIST CTRL : ",listctrl.GetName())
                if '_name_' in name:
                    listctrl.InsertItem(line,value)
                    print("Set {0} : {1} on Line {2}".format('Name', value, line))
                
                if '_scheme_' in name:
                    listctrl.SetItem(line , 1, str(value))
                    print("Set {0} : {1} on Line {2}".format('Scheme', value, line))
               
                if '_reduceby_' in name:
                    listctrl.SetItem(line, 2, str(value))
                    print("Set {0} : {1} on Line {2}".format('Reduce By', value, line))
                
        if 'clear' in named:
            for label, name in active_list:
                print("Clear Name : ",name)
                wx.FindWindowByName(name).ClearCtrl()
        
        if 'delete' in named:
            lc_name = 'invMaint_priceSchemes_listctrl'
            print("Listctrl Name : ",lc_name)
            listctrl = wx.FindWindowByName(lc_name)
            line = listctrl.GetFirstSelected()
            print("item : ",listctrl)
            
            named = listctrl.GetItemText(line)
            print("Named : ",named)
            
            query = 'DELETE FROM item_pricing_schemes WHERE name=(?)'
            data = (named,)
            returnd = SQConnect(query, data).ONE()
            
            listctrl.DeleteItem(line)
             
###----------
class CloseoutsTab(wx.Panel):
    def __init__(self, parent, size=(500,500), debug=False):
        """ Closeouts Tab """
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.SetName('CloseoutsTab')
        self.LSL = HUD.LoadSaveList()

        MainSizer = wx.BoxSizer(wx.VERTICAL)
        level1_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        name = 'maintCloseouts_AutoAdd_checkbox'
        ctrl = HUD.RH_CheckBox(self,-1, label='Auto Add Items to Closeouts',name=name)
        self.LSL.Add(name)
        ctrl.tableName = 'closeout_options'
        ctrl.fieldName = 'autoadd'
        level1_Sizer.Add(ctrl,0,wx.ALL,5)
        
        level2_Sizer = wx.BoxSizer(wx.VERTICAL)
         
        name = 'maintCloseouts_startAge_txtctrl'
        tc = HUD.RH_TextCtrl(self, -1, name=name,size=(90,-1))
        self.LSL.Add(name)
        tc.SetHint('0')
        tc.SetToolTip(wx.ToolTip('Please Enter a items Age (in Days) before Auto Closeout Function Begins'))
        tc.tableName = 'closeout_options'
        tc.fieldName = 'start_age'
        level2_Sizer.Add(tc, 0, wx.ALL, 5)
        
        name = 'maintCloseouts_incrementDay_txtctrl'
        tc = HUD.RH_TextCtrl(self, -1, name=name, size=(75,-1))
        self.LSL.Add(name)
        tc.SetHint('0')
        tc.SetToolTip(wx.ToolTip('Please Enter Amount of Days that the discount will countdown before decreasing'))
        tc.tableName = 'closeout_options'
        tc.fieldName = 'discount_percent'
        level2_Sizer.Add(tc, 0, wx.ALL, 3)
        
        name = 'maintCloseouts_DiscountPercent_txtctrl'
        tc = HUD.RH_TextCtrl(self, -1, name=name, size=(75, -1))
        self.LSL.Add(name)
        tc.SetHint('%')
        tc.SetToolTip(wx.ToolTip('Please Enter Percentage that the amount with decrease by each period.'))
        tc.tableName = 'closeout_options'
        tc.fieldName = 'incremental_days'
        lS = wx.BoxSizer(wx.HORIZONTAL)
        lS.Add(tc, 0, wx.ALL, 3)
        suffix = wx.StaticText(self, -1, label='%')
        lS.Add(suffix, 0, wx.ALL|wx.ALIGN_CENTER, 3)
        level2_Sizer.Add(lS, 0, wx.ALL, 3)

        name = 'maintCloseouts_maxoffcost_txtctrl'
        tc = HUD.RH_TextCtrl(self, -1, name=name, size=(75, -1))
        self.LSL.Add(name)
        tc.SetHint('%')
        tc.SetToolTip(wx.ToolTip('Please Enter Bottom Discount threshold'))
        tc.tableName = 'closeout_options'
        tc.fieldName = 'max_cost_percent'
        lS = wx.BoxSizer(wx.HORIZONTAL)
        lS.Add(tc, 0, wx.ALL, 3)
        suffix = wx.StaticText(self, -1, label='%')
        lS.Add(suffix, 0, wx.ALL|wx.ALIGN_CENTER, 3)
        level2_Sizer.Add(lS, 0, wx.ALL, 3)
                
        MainSizer.Add(level1_Sizer, 0, wx.ALL, 5)
        MainSizer.Add(level2_Sizer, 0, wx.ALL, 5)
        self.SetSizer(MainSizer)
        self.Layout()
        
        wx.CallAfter(self.OnLoad, event='')
        
    
    def OnLoad(self, event):
        for name in self.LSL.Get():
            pout.v(f'Name Load : {name}')
            item = wx.FindWindowByName(name).OnLoad('abuser','rhp')

    def OnSave(self):
        for name in self.LSL.Get():
            item = wx.FindWindowByName(name).OnSave('abuser','rhp')
                                     


class DiscountOptionsTab(wx.Panel):
    def __init__(self, parent, size=(500,500), debug=False):
        """ Price Tab """
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.SetName('DiscountOptionsTab')
        
        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.lc = HUD.RH_OLV(self, size=(300,260), name='invMaint_discountOptions_listctrl', style=wx.LC_REPORT|wx.BORDER_SUNKEN)      
        self.lc.SetColumns([
                            ColumnDefn('Name','left',120, 'named'),
                            ColumnDefn('Discount %','center',90,'discountd')
                            ])

        self.lc.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelect)
        
        editSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.tc = HUD.RH_TextCtrl(self, -1)
        self.tc.SetHint('Name')
        self.tc.SetToolTip(wx.ToolTip('Discount Class Name'))
        self.tc.Bind(wx.EVT_KILL_FOCUS, HUD.EventOps().Capitals)
        editSizer.Add(self.tc, 0, wx.ALL, 3)

        self.nc = HUD.RH_TextCtrl(self, -1, style=wx.TE_PROCESS_TAB)
        self.nc.SetHint('%')
        self.nc.SetToolTip(wx.ToolTip('Set Discount Percentage for Discount Class Name'))
        self.nc.Bind(wx.EVT_KILL_FOCUS, HUD.EventOps().OnNumbersOnly)
        editSizer.Add(self.nc, 0, wx.ALL, 3)

        self.addbtn = HUD.RH_Button(self, -1, label='Add')
        self.addbtn.Bind(wx.EVT_BUTTON, self.onAddButton)
        editSizer.Add(self.addbtn, 0, wx.ALL, 3)

        self.rembtn = HUD.RH_Button(self, -1, label='Remove')
        self.rembtn.SetForegroundColour('RED')
        self.rembtn.Bind(wx.EVT_BUTTON, self.onRemButton)
        editSizer.Add(self.rembtn, 0, wx.ALL, 3)
  
        MainSizer.Add(self.lc, 0)
        MainSizer.Add(editSizer,0)
        
        self.SetSizer(MainSizer)
        self.Layout()
    
        wx.CallAfter(self.onLoad, event='')
   
   
    def onLoad(self, event):
        query = 'SELECT name,percent FROM discount_options'
        data = ''
        returnd = SQConnect(query, data).ALL()
        try:
            for named, percent in returnd:
                line = self.lc.GetItemCount()
                setList = [{'named':named, 'discountd':percent}]
                self.lc.AddObjects(setList)
        except:
            print('Not Loaded')
    
    def OnSave(self):
        print("Discount Options")
        listctrl = wx.FindWindowByName('invMaint_discountOptions_listctrl')
        count = listctrl.GetItemCount()
        
        for idx in range(count):
            name_scheme = listctrl.GetItemText(idx)
            print("Get Item {0} : {1}".format(listctrl.GetItem(idx), name_scheme))     
            queryWhere = 'name=(?)'
            queryData = (name_scheme,)
            countd = HUD.QueryOps().QueryCheck('discount_options',queryWhere,queryData)
            print("Countd : ",countd)
            if countd == 0:
                name = listctrl.GetItem(idx,0).GetText().strip()
                percent = listctrl.GetItem(idx,1).GetText().strip()
                print("Name : {0}, Percent : {1}".format(name,percent))
                query = 'INSERT INTO discount_options (name,percent) VALUES ((?),(?))'
                data = (name,percent,)
                returnd = SQConnect(query, data).ONE()

            
    def onItemSelect(self, event):
        delete = wx.FindWindowByName('invMaint_discountOptions_listctrl_delete_button').Enable()        
                

    def onAddButton(self, event):
        named = self.tc.GetCtrl()
        disc = self.nc.GetCtrl()
        setList = [{'named':named, 'discountd':disc}]
        self.lc.AddObjects(setList)


    def onRemButton(self, event):
        selection = self.lb.GetStringSelection()
        self.lbtc.SetCtrl(selection)
        
        tobe_removed = self.tc.GetValue()
        currentItem = self.lc.FindString(tobe_removed)
        if currentItem != -1:
            self.lc.EnsureVisible(currentItem)
            self.lc.Delete(currentItem)

    def onClear(self, event):
        pass
        
    def onButton(self, event):
        obj = event.GetEventObject()
        named = obj.GetName()
        debug=False
        
        active_list = [('Name','invMaint_discountOptions_listctrl_name_txtctrl'),
                       ('Percent','invMaint_discountOptions_listctrl_percent_txtctrl')]
        
        print("Button : ",named)
        if 'add' in named:
            listctrl = wx.FindWindowByName('invMaint_discountOptions_listctrl')
            line = listctrl.GetItemCount()
           
                    
            for label, name in active_list:
                print("Name : ",name)
                ctrl = wx.FindWindowByName(name)
                value = ctrl.GetValue()
                if not value:
                    ctrl.SetBackgroundColour('RED')     
                    return
                
                print("LIST CTRL : ",listctrl.GetName())
                if '_name_' in name:
                    listctrl.InsertItem(line,value)
                    print("Set {0} : {1} on Line {2}".format('Name', value, line))
                
                if '_percent_' in name:
                    listctrl.SetItem(line , 1, str(value))
                    print("Set {0} : {1} on Line {2}".format('Scheme', value, line))
               
                
        if 'clear' in named:
            for label, name in active_list:
                print("Clear Name : ",name)
                wx.FindWindowByName(name).ClearCtrl()
        
        if 'delete' in named:
            lc_name = 'invMaint_discountOptions_listctrl'
            print("Listctrl Name : ",lc_name)
            listctrl = wx.FindWindowByName(lc_name)
            line = listctrl.GetFirstSelected()
            print("item : ",listctrl)
            
            named = listctrl.GetItemText(line)
            print("Named : ",named)
            
            query = 'DELETE FROM discount_options WHERE name=(?)'
            data = (named,)
            returnd = SQConnect(query, data).ONE()
            
            listctrl.DeleteItem(line)
                    


###----------
class GeneralDetailsTab(wx.Panel):
    def __init__(self, parent, size=(500,500), debug=False):
        """ General Details Tab """
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.SetName('GeneralDetailsTab')
        self.LSL = HUD.LoadSaveList()

        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        level1Sizer = wx.BoxSizer(wx.VERTICAL)
        level2Sizer = wx.BoxSizer(wx.VERTICAL)
        level3Sizer = wx.BoxSizer(wx.VERTICAL)
        lbsize = (300, 100)
        
        savebutton = ButtonOps().Icons('save')
        icon = wx.BitmapButton(self, wx.ID_ANY, 
                               wx.Bitmap(savebutton), 
                               style=wx.BORDER_NONE)
        icon.Bind(wx.EVT_BUTTON, self.OnSave)
        level3Sizer.Add(icon, 0, wx.ALL, 3)
        
        name = 'invMaint_department_listbox'                     
        lb = HUD.AltLookup(self, boxlabel='Departments', 
                                 lbsize=lbsize, 
                                 lbname=name, 
                                 tableName='organizations', 
                                 fieldName='department')            
        # lb.tableName = 'organizations'
        # lb.fieldName='department'
        self.LSL.Add(name)
        level1Sizer.Add(lb, 0, wx.ALL, 3)
        
        name = 'invMaint_category_listbox'
        lb = HUD.AltLookup(self, boxlabel='Category', 
                                 lbsize=lbsize, 
                                 lbname=name,
                                 tableName='organizations',
                                 fieldName='category')
        # lb.tableName = 'organizations'
        # lb.fieldName = 'category'
        self.LSL.Add(name)
        level1Sizer.Add(lb, 0, wx.ALL, 3)
        
        name = 'invMaint_subcategory_listbox'
        lb = HUD.AltLookup(self, boxlabel='Sub-Category', 
                                 lbsize=lbsize, 
                                 lbname=name,
                                 tableName='organizations',
                                 fieldName='subcategory')
        # lb.tableName = 'organizations'
        # lb.fieldName = 'subcategory'
        self.LSL.Add(name)
        level1Sizer.Add(lb, 0, wx.ALL, 3)

        name = 'invMaint_location_listbox'
        lb = HUD.AltLookup(self, boxlabel='Location/Material', 
                                 lbsize=lbsize, 
                                 lbname=name,
                                 tableName='organizations',
                                 fieldName='location')
        # lb.tableName = 'organizations'
        # lb.fieldName = 'location'
        self.LSL.Add(name)
        level1Sizer.Add(lb, 0, wx.ALL, 3)

        name = 'invMaint_unittype_listbox'
        lb = HUD.AltLookup(self, boxlabel='Unit Type', 
                                 lbsize=lbsize, 
                                 lbname=name,
                                 tableName='organizations',
                                 fieldName='unittype')
        # lb.tableName = 'organizations'
        # lb.fieldName = 'unittype'
        self.LSL.Add(name)
        level2Sizer.Add(lb, 0, wx.ALL, 3)

        box = wx.StaticBox(self, -1, label='# of Aisles')
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        name='invMaint_aisleNums_txtctrl'
        nc = HUD.RH_MTextCtrl(self, -1, name=name, mask='#{4}')
        nc.tableName = 'organizations'
        nc.fieldName = 'num_of_aisles'
        self.LSL.Add(name)
        boxSizer.Add(nc, 0, wx.ALL, 3)
        level2Sizer.Add(boxSizer, 0, wx.ALL, 3)
        
        box = wx.StaticBox(self, -1, label='# of Sections')
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        name='invMaint_sectionNums_txtctrl'
        nc = HUD.RH_MTextCtrl(self, -1, name=name, mask='#{4}')
        nc.tableName = 'organizations'
        nc.fieldName = 'num_of_sections'
        self.LSL.Add(name)
        boxSizer.Add(nc, 0, wx.ALL, 3)
        level2Sizer.Add(boxSizer, 0, wx.ALL, 3)
        
        MainSizer.Add(level1Sizer, 0, wx.ALL, 3)
        MainSizer.Add(level2Sizer, 0, wx.ALL, 3)
        MainSizer.Add(level3Sizer, 0, wx.ALL, 3)
        self.SetSizer(MainSizer, 0)
        self.Layout()
        
        wx.CallAfter(self.OnLoad, event='')        
    
            
    def OnLoad(self, event):
        for name in self.LSL.Get():
            print(f'Name Load : {name}')
            item = wx.FindWindowByName(name)
            item.OnLoad(whereField='abuser', whereValue='rhp')
            
    def OnSave(self, event):
        for name in self.LSL.Get():
            print(f'Name Save : {name}')
            item = wx.FindWindowByName(name)
            item.OnSave(whereField='abuser', whereValue='rhp')

        
class SupportTab(wx.Panel):
    def __init__(self, parent, size=(500,500), debug=False):
        """ Customer Data Tab """    
        wx.Panel.__init__(self,parent=parent, id=wx.ID_ANY)
        self.SetName('SupportTab')
        
        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        level1Sizer = wx.BoxSizer(wx.VERTICAL)
        level2Sizer = wx.BoxSizer(wx.VERTICAL)
        
        listboxes = [('Customer Codes','invMaint_customerCodes_listbox'),
                     ('Account Types','invMaint_accountTypes_listbox')]
                     
                     
        for label, name in listboxes:
            print("Current Set Box : ",label)
            box = wx.StaticBox(self, label=label,style=wx.ALIGN_CENTER)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            listbox = wx.ListBox(self, -1,size=(300,100), name=name)
            listbox.Bind(wx.EVT_LISTBOX, HUD.EventOps().ListBoxSelectItem)
            if 'extraPlaces' in name:
                extraList = [('# of Aisles','invMaint_aisleNums_numctrl'),('# of Sections','invMaint_sectionNums_numctrl')]
                for  label2, name2 in extraList:
                    boxPos = wx.StaticBox(self, label=label2, style=wx.ALIGN_CENTER)
                    boxPosSizer = wx.StaticBoxSizer(boxPos, wx.HORIZONTAL)
                    ctrl = masked.NumCtrl(self, -1, value=0, name=name2,integerWidth=4, fractionWidth=0)
                    boxPosSizer.Add(ctrl, 0, wx.ALL, 14)
                    boxSizer.Add(boxPosSizer, 0, wx.ALL, 3)
            
            boxSizer.Add(listbox, 0)
            
            ctrlSizer = wx.BoxSizer(wx.VERTICAL)
            alt_ctrls_list = [('','_txtctrl',''),('Add','_addbutton', HUD.EventOps().ListBoxOnAddButton),
                          ('Remove','_rembutton', HUD.EventOps().ListBoxOnRemoveButton)]
            for labeld,named,hdlr in alt_ctrls_list:
                if 'txtctrl' in named:
                    ctrl = wx.TextCtrl(self, -1, size=(110, -1), name=name+named)
                if 'button' in named:
                    ctrl = wx.Button(self, -1, label=labeld, size=(110,-1), name=name+named)
                    ctrl.Bind(wx.EVT_BUTTON, hdlr)
                    if 'remove' in name:
                        ctrl.SetForegroundColour('Red')
                
                ctrlSizer.Add(ctrl,0, wx.ALL, 2)
            
            boxSizer.Add(ctrlSizer, 0, wx.ALL, 3)
           
            if re.search('(unittype|extraplaces)',name, re.I):
                level2Sizer.Add(boxSizer, 0, wx.ALL, 3)
            else:
                level1Sizer.Add(boxSizer, 0, wx.ALL, 3)             
        
         
        
        MainSizer.Add(level1Sizer, 0, wx.ALL, 3)
        MainSizer.Add(level2Sizer, 0, wx.ALL, 3)
        
       
        
        self.SetSizer(MainSizer, 0)
        self.Layout()
        wx.CallAfter(self.OnLoad, event='')
   
    def OnLoad(self, event):
        load_lists = [('account_types','invMaint_accountTypes_listbox'),('customer_codes','invMaint_customerCodes_listbox')]
        for field, name in load_lists:
            query = "SELECT {0} FROM organizations".format(field)
            data = ''
            returnd = SQConnect(query, data).ALL()
            
            try:
                print("returnd : ",returnd[0][0])                    
                wx.FindWindowByName(name).SetCtrl(returnd[0][0])
            except:
                wx.FindWindowByName(name).SetCtrl('')        

class POSTab(wx.Panel):
    def __init__(self, parent, size=(500,500)):
        """POS Tab """
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        self.SetName('POSTab')
        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        listbox = HUD.AltLookup(self, boxlabel='Card Processors', 
                                      lbsize=(300, 100), 
                                      lbname='postab_processors_listbox',
                                      tableName='organizations',
                                      fieldName='processors')
        #boxSizer.Add(listbox, 0)
        # listbox.tableName = 'organizations'
        # listbox.fieldName = 'processors'
        MainSizer.Add(listbox, 0)
        self.SetSizer(MainSizer, 0)
        self.Layout()

    def OnSave(self):
        lb = wx.FindWindowByName('postab_processors_listbox')
        lb.OnSave()
        

class CustomerMaintenanceTab(wx.Panel):
    def __init__(self, parent, size=(500,500), debug=False):
        """ Customer Data Tab """    
        wx.Panel.__init__(self,parent=parent, id=wx.ID_ANY)
        
        self.SetName('CustomerMaintenanceTab')
        
        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        notebook = wx.Notebook(self, wx.ID_ANY,name='CustomerTab_Notebook')
        tabOne = SupportTab(notebook)
        
        notebook.AddPage(tabOne, "Support")
        MainSizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)
        
        
        self.SetSizer(MainSizer, 0)
        self.Layout()
        

class BookkeepingTab(wx.Panel):
    def __init__(self, parent, size=(500,500), debug=False):
        """ Bookkeeping Tab """    
        wx.Panel.__init__(self,parent=parent, id=wx.ID_ANY)
        
        self.SetName('BookkeepingTab')
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        
        colLabel_list = [('Major', 60),('Minor',60),('Account Name',160)]
        coa_grid = gridlib.Grid(self, -1, size=(300,480),style=wx.BORDER_SUNKEN, name='maintenance_chartofAccounts_grid')
        coa_grid.CreateGrid(1,len(colLabel_list))
        coa_grid.SetRowLabelSize(0)
        coa_grid.EnableEditing(False)
        idx = 0
        for label, sized in colLabel_list:
            coa_grid.SetColLabelValue(idx, label)
            coa_grid.SetColSize(idx, sized)
            idx+=1
        
        MainSizer.Add(coa_grid, 0)
        
        level2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        lvl2_list = [('Major','maintenance_major_txtctrl',60),('Minor','maintenance_minor_txtctrl',60),('Account Name','maintenance_acctname_txtctrl',160)]
        for label,name,sized in lvl2_list:
            box = wx.StaticBox(self, -1, label=label, style=wx.ALIGN_CENTER)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            if 'Account Name' in label:
                ctrl = wx.TextCtrl(self, -1, name=name, size=(sized, -1))
            else:
                ctrl = masked.TextCtrl(self, -1, name=name, size=(sized,-1),mask='###')
            boxSizer.Add(ctrl, 0, wx.ALL, 5)
            
            level2Sizer.Add(boxSizer, 0)        
        
        level2_1Sizer = wx.BoxSizer(wx.VERTICAL)
        addbutton = wx.Button(self, -1, label='Add', name='bookkeeping_add_button')
        addbutton.Bind(wx.EVT_BUTTON, self.onAddAccount)
        
        rembutton = wx.Button(self, -1, label='Remove',name='bookkeeping_remove_button')
        rembutton.Bind(wx.EVT_BUTTON, self.onRemAccount)
        
        level2_1Sizer.Add(addbutton, 0)
        level2_1Sizer.Add(rembutton, 0)
        
        level2Sizer.Add(level2_1Sizer, 0)   
        MainSizer.Add(level2Sizer, 0)
        wx.CallAfter(self.OnLoad, event='')
        
        self.SetSizer(MainSizer, 0)
        self.Layout()
        
    def onAddAccount(self, event):
        major = wx.FindWindowByName('maintenance_major_txtctrl').GetValue()
        minor = wx.FindWindowByName('maintenance_minor_txtctrl').GetValue()
        acctName = wx.FindWindowByName('maintenance_acctname_txtctrl').GetValue().title()
        
        if major and minor and acctName:
            query = "SELECT count(*) FROM ledger_post_accounts WHERE account_major=(?) AND account_minor=(?)"
            data = (major, minor,)
            returnd = SQConnect(query, data).ONE()
            print("Number of Chart Found : ",len(returnd))
            if returnd[0] == 1:
                wx.MessageBox('Account Found','Error', wx.OK)
                item = wx.FindWindowByName('bookkeeping_add_button').SetBackgroundColour('Red')
            else:
                query = "INSERT INTO ledger_post_accounts values ((?), (?), (?));"                    
                data = (major, minor, acctName,)
                returnd = SQConnect(query, data).ONE()
                item = wx.FindWindowByName('bookkeeping_add_button').SetBackgroundColour('Green')
                wx.CallAfter(self.OnLoad, event='')
         
        
        else:
            if not major:
                wx.MessageBox('Major Account not defined.','Error', wx.OK)
                    
            if not minor:   
                wx.MessageBox('Minor Account not defined.','Error', wx.OK)
                
            if not acctName:
                wx.MessageBox('Account Name not defined.','Error', wx.OK)
                   
            return     
                
    def onRemAccount(self, event):
        major = wx.FindWindowByName('maintenance_major_txtctrl').GetValue()
        minor = wx.FindWindowByName('maintenance_minor_txtctrl').GetValue()
        acctName = wx.FindWindowByName('maintenance_acctname_txtctrl').GetValue()
        
        if major and minor:
            query = "SELECT count(*) FROM ledger_post_accounts WHERE account_major=(?) AND account_minor=(?)"
            data = (major, minor,)
            returnd = SQConnect(query, data).ONE()
            print("Number of Chart Found : ",len(returnd))
            if returnd[0] == 1:
                query = "DELETE FROM ledger_post_accounts WHERE account_major=(?) AND account_minor=(?);"                    
                data = (major, minor,)
                returnd = SQConnect(query, data).ONE()
                item = wx.FindWindowByName('bookkeeping_remove_button').SetBackgroundColour('Green')
                wx.CallAfter(self.OnLoad, event='')
            else:
                wx.MessageBox('Account Found','Error', wx.OK)
                item = wx.FindWindowByName('bookkeeping_remove_button').SetBackgroundColour('Red')
            return
                
    def OnLoad(self, event):
        query = "SELECT account_major,account_minor,account_name FROM ledger_post_accounts"
        data = ''
        returnd = SQConnect(query, data).ALL()
        
        grid = wx.FindWindowByName('maintenance_chartofAccounts_grid')
        colsnum = grid.GetNumberCols()
        rowsnum = grid.GetNumberRows()
        #print "Returnd  : ",returnd
        current, new = (grid.GetNumberRows(), len(returnd))

        if new > current:
            grid.AppendRows(new-current)
        
        if new < current:
            grid.DeleteRows(current-new)
         
        bgcolor = (255,255,255)    
        cell_color = (217,241,232)
        returnd.sort()
        print('Number of current rows: ' + str(grid.GetNumberRows()))
        print('Size of myDataList: ', len(returnd))
        
        for zeroed_xx in range(grid.GetNumberRows()):
            for zeroed_yy in range(colsnum):
                grid.SetCellValue(zeroed_xx,zeroed_yy,'')
                grid.SetCellBackgroundColour(zeroed_xx,zeroed_yy,bgcolor)
        
        for row in range(grid.GetNumberRows()):
            for idx in range(colsnum):
                (amajor, aminor, acctname) = returnd[row]
                
                if grid.GetColLabelValue(idx) == 'Major':
                    grid.SetCellValue(row, idx, amajor)
                if grid.GetColLabelValue(idx) == 'Minor':
                    grid.SetCellValue(row, idx, aminor)
                if grid.GetColLabelValue(idx) == 'Account Name':
                    grid.SetCellValue(row, idx, acctname)
                if aminor == '000':
                    for spex in range(colsnum):
                           grid.SetCellFont(row, spex, wx.Font(wx.FontInfo(9).Bold()))         
              #  if row % 2:
              #      for cellstart in range(colsnum):
              #          grid.SetCellBackgroundColour(row,cellstart,cell_color)            
        HUD.GridOps(grid.GetName()).GridAlternateColor('')
        
class TaxInfoTab(wx.Panel):
    def __init__(self, parent, size=(500,500), debug=False):
        """ Customer Data Tab """    
        wx.Panel.__init__(self,parent=parent, id=wx.ID_ANY)
        
        self.SetName('TaxInfoTab')
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
            
        #tax_list = [('State Sales Tax', 'taxMaint_statestx_numctrl'),('County Sales Tax','taxMaint_countystx_numctrl'),
        #            ('VAT','taxMaint_vat_numctrl')]
        box = wx.StaticBox(self, -1, label='Tax Rounding')
        boxSizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        cb = HUD.RH_CheckBox(self, -1, label='No Pennies', name='taxMain_noPennies_checkbox')
        cb.tableName = 'tax_tables'
        cb.fieldName = 'no_pennies_rounding'
        cb.Bind(wx.EVT_CHECKBOX, self.PennyBox)
        
        lowest_coin = 'Penny'
        
        t1 = '1. Do Not Round to the Next {lc}.'.format(lc=lowest_coin)
        t2 = '2. Round half up or down {lc}.'.format(lc=lowest_coin)
        t3 = '3. Round any up to next {lc}.'.format(lc=lowest_coin)  
        t = '{}\n{}\n{}'.format(t1,t2,t3)
        txt = wx.StaticText(self, -1, label=t, name='taxMain_coinRound_text', style=wx.ALIGN_LEFT)
        ctrl = HUD.RH_ComboBox(self, -1, choices=['1','2','3'], name='taxMain_rndScheme_combobox', size=(75, -1))
        ctrl.tableName = 'tax_tables'
        ctrl.fieldName = 'RNDscheme'
        boxSizer.Add(txt, 0)
        boxSizer.Add(ctrl, 0)
        
        MainSizer.Add(cb, 0, wx.ALL, 5)
        MainSizer.Add(boxSizer, 0, wx.ALL, 5)
        
        box = wx.StaticBox(self, -1, label='Tax Info')
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        print("*"*80)
        print('Tax Tables')
        print("*"*80)
        grid = HUD.Tax_Table_Grid(self, name='taxMain_taxTable_grid', size=(890,300))     
        boxSizer.Add(grid, 0, wx.ALL|wx.EXPAND, 5)      
        # tax_list = [('Min\nSale','taxMain_minSale_numctrl'),
        #             ('Max\nSale','taxMain_maxSale_numctrl'),
        #             ('Item\nMax','taxMain_itemMax_numctrl'),
        #             ('From\nAmt','taxMain_fromAmt0_numctrl'),
        #             ('Tax\nRate','taxMain_taxRate0_numctrl'),
        #             ('From\nAmt','taxMain_fromAmt1_numctrl'),
        #             ('Tax\nRate','taxMain_taxRate1_numctrl'),
        #             ('From\nAmt','taxMain_fromAmt2_numctrl'),
        #             ('Tax\nRate','taxMain_taxRate2_numctrl')]
                    
        # for label,name in tax_list:
        #     sizer = wx.BoxSizer(wx.VERTICAL)
        #     text = wx.StaticText(self, -1, label=label)
        #     ctrl = masked.NumCtrl(self, -1, name=name, integerWidth=4, fractionWidth=4)
        #     sizer.Add(text, 0, wx.ALL|wx.ALIGN_CENTER, 3)
        #     sizer.Add(ctrl, 0, wx.ALL|wx.ALIGN_CENTER, 3)
        #     boxSizer.Add(sizer, 0)
        #     if re.search('taxRate[01]',name, re.I):
        #         st = wx.StaticLine(self, wx.ID_ANY, size=(5,75),style=wx.LI_VERTICAL)
        #         boxSizer.Add(st, wx.ALL | wx.EXPAND, 5)              
        
        MainSizer.Add(boxSizer, 0)
        
        self.SetSizer(MainSizer, 0)
        self.Layout()

        wx.CallAfter(self.OnLoad, event='')
        
        
    def PennyBox(self, event):
        obj = event.GetEventObject()
        named = obj.GetName()
        value = obj.GetCtrl()
        lowest_coin = 'Penny'
        if value == 1:
            lowest_coin = 'Nickel'
        
        t1 = '1. Do Not Round to the Next {lc}.'.format(lc=lowest_coin)
        t2 = '2. Round half up to next {lc}.'.format(lc=lowest_coin)
        t3 = '3. Round any up to next {lc}.'.format(lc=lowest_coin)  
        t = '{}\n{}\n{}'.format(t1,t2,t3)
        wx.FindWindowByName('taxMain_coinRound_text').SetCtrl(t)


    def OnLoad(self, event):
        #self.PennyBox()
        
                    #  ('no_pennies_rounding','taxMain_noPennies_checkbox','tax_tables'),
                    #  ('RNDscheme','taxMain_rndScheme_combobox','tax_tables'),
                    #  ('min_sale','taxMain_minSale_numctrl','tax_tables'),
                    #  ('max_sale','taxMain_maxSale_numctrl','tax_tables'),
                    #  ('item_max','taxMain_itemMax_numctrl','tax_tables'),
                    #  ('from_amt0','taxMain_fromAmt0_numctrl','tax_tables'),
                    #  ('tax_rate0','taxMain_taxRate0_numctrl','tax_tables'),
                    #  ('from_amt1','taxMain_fromAmt1_numctrl','tax_tables'),
                    #  ('tax_rate1','taxMain_taxRate1_numctrl','tax_tables'),
                    #  ('from_amt2','taxMain_fromAmt2_numctrl','tax_tables'),
                    #  ('tax_rate2','taxMain_taxRate2_numctrl','tax_tables')]
        
        tax_list = [('no_pennies_rounding','taxMain_noPennies_checkbox','tax_tables'),
                   ('RNDscheme','taxMain_rndScheme_combobox','tax_tables')]
                #    ('min_sale','taxMain_minSale_numctrl','tax_tables'),
                #    ('max_sale','taxMain_maxSale_numctrl','tax_tables'),
                #    ('item_max','taxMain_itemMax_numctrl','tax_tables'),
                #    ('from_amt0','taxMain_fromAmt0_numctrl','tax_tables'),
                #    ('tax_rate0','taxMain_taxRate0_numctrl','tax_tables'),
                #    ('from_amt1','taxMain_fromAmt1_numctrl','tax_tables'),
                #    ('tax_rate1','taxMain_taxRate1_numctrl','tax_tables'),
                #    ('from_amt2','taxMain_fromAmt2_numctrl','tax_tables'),
                #    ('tax_rate2','taxMain_taxRate2_numctrl','tax_tables')]

        grid = wx.FindWindowByName('taxMain_taxTable_grid').OnLoad()

        for field, name, table in tax_list:
            query = 'SELECT {0} FROM {1} WHERE tax_name=(?)'.format(field, table) 
            data = ('TAX',)         
            
            returnd = SQConnect(query, data).ONE()
            print("Name : {0} : {1}".format(name,returnd))
            try:
                wx.FindWindowByName(name).SetCtrl(str(returnd[0]))
            except:
                print('None')
    def OnSave(self):
        print("Save Tax Info")
        save_list = [('taxMain_noPennies_checkbox','tax_tables','no_pennies_rounding'),
                     ('taxMain_rndScheme_combobox','tax_tables','RNDscheme')]
                    #  ('taxMain_minSale_numctrl','tax_tables','min_sale'),
                    #  ('taxMain_maxSale_numctrl','tax_tables','max_sale'),
                    #  ('taxMain_itemMax_numctrl','tax_tables','item_max'),
                    #  ('taxMain_fromAmt0_numctrl','tax_tables','from_amt0'),
                    #  ('taxMain_taxRate0_numctrl','tax_tables','tax_rate0'),
                    #  ('taxMain_fromAmt1_numctrl','tax_tables','from_amt1'),
                    #  ('taxMain_taxRate1_numctrl','tax_tables','tax_rate1'),
                    #  ('taxMain_fromAmt2_numctrl','tax_tables','from_amt2'),
                    #  ('taxMain_taxRate2_numctrl','tax_tables','tax_rate2')]
                    
        fieldSet, dataSet, table = HUD.QueryOps().Commaize(save_list)
        grid = wx.FindWindowByName('taxMain_taxTable_grid').OnSave()

        query = '''UPDATE {} 
                   SET {}
                   WHERE tax_name=(?)'''.format(table, fieldSet)
        
        data = dataSet + ['TAX',]
        returnd = SQConnect(query, data).ONE() 
                
        
class EmployeesTab(wx.Panel):
    def __init__(self, parent, size=(500,500), debug=False):
        """ Customer Data Tab """    
        wx.Panel.__init__(self,parent=parent, id=wx.ID_ANY)
        
        self.SetName('EmployeesTab')
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        lc_box = wx.StaticBox(self, -1, label="Employee Maintenance")
        lc_boxSizer = wx.StaticBoxSizer(lc_box, wx.VERTICAL)
        
        addinfo_boxSizer = wx.BoxSizer(wx.HORIZONTAL)
        ARbutton_boxSizer = wx.BoxSizer(wx.VERTICAL)
        addinfo_list = [('Acct Number','maint_employee_num_txtctrl',70, 'employees','employee_num'),
                        ('Name','maint_employee_name_txtctrl',180, 'employees','employee_name'),
                        ('D.O.B','maint_employee_dob_txtctrl',60, 'employees','date_of_birth'),
                        ('SSN#','maint_employee_ssn_txtctrl',60, 'employees','ssn'),
                        ('Add','maint_emp_add_button',10,'',''),
                        ('Remove','maint_emp_remove_button',10,'','')]
                        
        for label,name,sized, tableName, fieldName in addinfo_list:
            if 'maint_employee_num_txtctrl' in name:
                num_boxSizer = wx.BoxSizer(wx.VERTICAL)
                txtctrl = HUD.RH_TextCtrl(self, -1, name=name, size=(sized,-1))

                txtctrl.SetToolTip(wx.ToolTip('Enter an Account Number or click \'Auto\' to Assign one'))
                num_boxSizer.Add(txtctrl, 0)
        
                numbtn_boxSizer = wx.BoxSizer(wx.HORIZONTAL)
        
                numbtn_list = [('Check',self.OnEmpNumCheck),('Auto', self.OnEmpNumAuto)]
                for label,handlr in numbtn_list:
                    btn = HUD.RH_Button(self, -1, label=label)
                    btn.Bind(wx.EVT_BUTTON, handlr)
                    numbtn_boxSizer.Add(btn, 0)
            
                num_boxSizer.Add(numbtn_boxSizer, 0)
                addinfo_boxSizer.Add(num_boxSizer, 0)
                
            elif 'button' in name:
                
                btn = HUD.RH_Button(self, -1, label=label, name=name)
                if 'add_button' in name:
                    btn.Bind(wx.EVT_BUTTON, self.OnAddEmployee)
                    
                elif 'remove_button' in name:
                    btn.Bind(wx.EVT_BUTTON, self.OnRemoveEmployee)
        
                ARbutton_boxSizer.Add(btn, 0)
            
            elif 'ssn' in name:
                txtctrl = HUD.RH_MTextCtrl(self, -1,  name=name, mask='###-##-####', validRegex='\d{3}-\d{2}-\d{4}', size=(sized, -1))
                
                addinfo_boxSizer.Add(txtctrl, 0)
            elif 'dob' in name:
                txtctrl = HUD.RH_MTextCtrl(self, -1,  name=name, mask='##/##/####', validRegex='\d{2}/\d{2}/\d{4}', size=(sized, -1))
                addinfo_boxSizer.Add(txtctrl, 0)    
            else:  
                txtctrl = HUD.RH_TextCtrl(self, -1, name=name, size=(sized, -1)) 
                addinfo_boxSizer.Add(txtctrl, 0)
            
            if not 'button' in name:
                txtctrl.tableName = tableName
                txtctrl.fieldName = fieldName

            txtctrl.Bind(wx.EVT_SET_FOCUS, self.startfirst)
        
        addinfo_boxSizer.Add(num_boxSizer, 0)
        
        
        
        addinfo_boxSizer.Add(ARbutton_boxSizer, 0)
        lc_boxSizer.Add(addinfo_boxSizer, 0)
        
        lc = HUD.RH_OLV(self, -1, name='maint_employee_listctrl',style=wx.LC_REPORT|wx.BORDER_SIMPLE)
        lc.SetColumns([
                     ColumnDefn('Employee #','center',90, 'employee_num'),
                     ColumnDefn('Name','left',120,'named'),
                     ColumnDefn('D.O.B','left',90,'dob')
                    ])

        lc_boxSizer.Add(lc, 0)
        MainSizer.Add(lc_boxSizer, 0)
        
        
        self.SetSizer(MainSizer, 0)
        self.Layout()
    
    def startfirst(self, event):
        txtctrl = event.GetEventObject()
        txtctrl.SetInsertionPoint(0)
        
        
             
    def OnEmpNumCheck(self, event):
        pass
   
    def OnEmpNumAuto(self, event):
        pass
        
    def OnAddEmployee(self, event):
        pass
    
    def OnRemoveEmployee(self, event):
        pass 
        
#--------------------------
class PasswordsTab(wx.Panel):
    def __init__(self, parent, size=(500,500), debug=False):
        """ Passwords Tab """    
        wx.Panel.__init__(self,parent=parent, id=wx.ID_ANY)
        
        self.SetName('PasswordsTab')
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        row1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn = wx.Button(self, -1, 
                        label='Load Passwords', 
                        name='password_load_button')
        
        btn.Bind(wx.EVT_BUTTON, self.OnLoadPasswords)
        
        row1Sizer.Add(btn, 0,wx.ALL|wx.CENTER, 3)
        
        basePath = os.path.dirname(os.path.realpath(__file__))+'/'
        iconloc = ButtonOps().Icons('save')
        icon = wx.BitmapButton(self, wx.ID_ANY, 
                               wx.Bitmap(iconloc), 
                               name='password_save_button', 
                               style=wx.BORDER_NONE)
                               
        icon.Bind(wx.EVT_BUTTON, self.OnSavePasswords)
        icon.Disable()
        row1Sizer.Add(icon, 0, wx.ALL|wx.CENTER, 3)
        
        
        row2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        major_list = [('Admin Key','password_admin_txtctrl'),
                      ('Manager Key','password_manager_txtctrl'),
                      ('Clerk Key','password_clerk_txtctrl')]
        
        for label, name in major_list:
            box = wx.StaticBox(self, -1, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            ctrl = wx.TextCtrl(self, -1, name=name, size=(90,-1))
            boxSizer.Add(ctrl, 0)
            row2Sizer.Add(boxSizer, 0, wx.ALL|wx.CENTER, 3)              
        
        
        row3Sizer = wx.BoxSizer(wx.HORIZONTAL)
        minor_list = [('Drawer Access','password_drawerAccess_cbox','req_drawer_access'),
                      ('Coupons','password_coupon_cbox','req_coupons'),
                      ('Cash Check','password_cashCheck_cbox','req_cash_check'),
                      ('Cancel Transaction','password_cancelTrans_cbox','req_cancel_trans'),
                      ('GiftCard Override','password_giftCardOverride_cbox','req_giftcard_override')]
                      
        box = wx.StaticBox(self, label='Password Protected')
        boxSizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        for label, named, field in minor_list:
            cb = HUD.RH_CheckBox(self, -1, label=label, name=named)
            cb.tableName = 'passwords'
            cb.fieldName = field
            boxSizer.Add(cb, 0, wx.ALL|wx.LEFT, 3)
            
        row3Sizer.Add(boxSizer, 0, wx.ALL|wx.CENTER, 3)
        
        
            
                      
        
        MainSizer.Add(row1Sizer, 0)
        MainSizer.Add(row2Sizer, 0)     
        MainSizer.Add(row3Sizer, 0)
        self.SetSizer(MainSizer, 0)
        self.Layout()
        
        
    def OnLoadPasswords(self, event):
        dlg = HUD.PasswordDialog('admin')
        #dlg.Operator('admin')
        dlg.ShowModal()
        dlg.Destroy()
        
        print('dlg.passwordOK : ',dlg.passwordOK)
        if dlg.passwordOK == True:
            wx.FindWindowByName('password_save_button').EnableCtrl()
            
            major_list = [('Admin Key','password_admin_txtctrl','admin_key'),
                          ('Manager Key','password_manager_txtctrl','manager_key'),
                          ('Clerk Key','password_clerk_txtctrl','clerk_key')]
           
            for label,named,field in major_list:
                item = LookupDB('passwords').Specific('rhp','abuser',field)
                print('Item : ',item)
                wx.FindWindowByName(named).SetCtrl(item[0])
                
            minor_list = [('Drawer Access','password_drawerAccess_cbox','req_drawer_access'),
                          ('Coupons','password_coupon_cbox','req_coupons'),
                          ('Cash Check','password_cashCheck_cbox','req_cash_check'),
                          ('Cancel Transaction','password_cancelTrans_cbox','req_cancel_trans'),
                          ('GiftCard Override','password_giftCardOverride_cbox','req_giftcard_override')]
            
            for label,named,field in minor_list:
                item = LookupDB('passwords').Specific('rhp','abuser',field)
                print('Item : ',item)
                wx.FindWindowByName(named).SetCtrl(item[0])
            
        
    
    def OnSavePasswords(self, event):
        
        HUD.QueryOps().CheckEntryExist('abuser','rhp',['passwords'])
        
        major_list = [('Admin Key','password_admin_txtctrl','admin_key'),
                      ('Manager Key','password_manager_txtctrl','manager_key'),
                      ('Clerk Key','password_clerk_txtctrl','clerk_key')]
                               
        for label,name,field in major_list:
            item = wx.FindWindowByName(name).GetCtrl()
            query = "UPDATE {tb} SET {fn}=(?) WHERE abuser='rhp'".format(tb='passwords',fn=field)
            data = (item,)    
            returnd = SQConnect(query, data).ONE()
            
       
        minor_list = [('Drawer Access','password_drawerAccess_cbox','req_drawer_access'),
                      ('Coupons','password_coupon_cbox','req_coupons'),
                      ('Cash Check','password_cashCheck_cbox','req_cash_check'),
                      ('Cancel Transaction','password_cancelTrans_cbox','req_cancel_trans'),
                      ('GiftCard Override','password_giftCardOverride_cbox','req_giftcard_override')]
                      
        
        for label, named, field in minor_list:
            item = wx.FindWindowByName(named).GetCtrl()
            query = "UPDATE {} SET {}=(?) WHERE abuser='rhp'".format('passwords',field)
            data = (item,)
            print('query : {} = {}'.format(query,data))
            SQConnect(query, data).ONE()
            
#--------------------------
class ReceiptTab(wx.Panel):
    def __init__(self, parent, size=(500,500), debug=True):
        """ Receipt Note Tab """
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.SetName('ReceiptTab')
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        
        do_list = [('Return Policy', 'receipt_returnPolicy_txtctrl','pos_messages','return_policy'),
                   ('Conditions', 'receipt_conditions_txtctrl','pos_messages','conditions'),
                   ('Thanks','receipt_thanks_txtctrl','pos_messages','thanks'),
                   ('Charge Agreement','receipt_chargeAgreement_txtctrl','pos_messages','charge_agreement'),
                   ('Check Policy', 'receipt_checkPolicy_txtctrl','pos_messages','check_policy'),
                   ('Credit Card Agreement','receipt_creditcardAgreement_txtctrl','pos_messages','credit_card_agreement'),
                   ('Special Event', 'receipt_specialEvent_txtctrl','pos_messages','special_event')]
        
        for label, name, tableName, fieldName in do_list:
            box = wx.StaticBox(self, -1, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            
            ctrl = HUD.RH_TextCtrl(self, -1, 
                               name=name, 
                               size=(400,50), 
                               style=wx.TE_MULTILINE)            
            ctrl.tableName = tableName
            ctrl.fieldName = fieldName
            boxSizer.Add(ctrl, 0, wx.ALL, 5)
            MainSizer.Add(boxSizer, 0)
        
        self.SetSizer(MainSizer, 0)
        self.Layout()     
        
        wx.CallAfter(self.OnLoad, event='')
        
    def OnLoad(self, event):
        ''' Loading POS Messages stored in pos_messages table in CONFIG.sql '''
      
        
    
        do_list = [('return_policy', 'receipt_returnPolicy_txtctrl','pos_messages'),
                   ('conditions', 'receipt_conditions_txtctrl','pos_messages'),
                   ('thanks','receipt_thanks_txtctrl','pos_messages'),
                   ('charge_agreement','receipt_chargeAgreement_txtctrl','pos_messages'),
                   ('check_policy', 'receipt_checkPolicy_txtctrl','pos_messages'),
                   ('credit_card_agreement','receipt_creditcardAgreement_txtctrl','pos_messages'),
                   ('special_event','receipt_specialEvent_txtctrl','pos_messages')]
   
        for field, name, table in do_list:
            query = 'SELECT {} FROM pos_messages WHERE abuser=(?)'.format(field)
            data = ('rhp',)
            returnd = SQConnect(query,data).ONE()
            
            print("returnd : ",returnd)
            if returnd is not None:
                wx.FindWindowByName(name).SetCtrl(returnd)
                
    def OnSave(self):
        HUD.QueryOps().CheckEntryExist('abuser','rhp',['pos_messages'])
        
        
    
        do_list = [('receipt_returnPolicy_txtctrl','pos_messages','return_policy',),
                   ('receipt_conditions_txtctrl','pos_messages','conditions'),
                   ('receipt_thanks_txtctrl','pos_messages','thanks'),
                   ('receipt_chargeAgreement_txtctrl','pos_messages','charge_agreement'),
                   ('receipt_checkPolicy_txtctrl','pos_messages','check_policy'),
                   ('receipt_creditcardAgreement_txtctrl','pos_messages','credit_card_agreement'),
                   ('receipt_specialEvent_txtctrl','pos_messages','special_event')]
   
        fieldSet, dataSet, table = HUD.QueryOps().Commaize(do_list)
         
        query = '''UPDATE {}
                   SET {} 
                   WHERE abuser=(?)'''.format(table, fieldSet)
        data = dataSet + ['rhp',]
        
        returnd = SQConnect(query, data).ONE()
          
        print('returnd : {}'.format(returnd))
            
            
            
            
#--------------------------
class HardwareTab(wx.Panel):
    def __init__(self, parent, size=(500,500), debug=False):
        """ Hardware Data Tab """    
        wx.Panel.__init__(self,parent=parent, id=wx.ID_ANY)
        self.SetName('HardwareTab')
        self.LSL = HUD.LoadSaveList()
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        
        note =  '''Finding usb vendorID and productID
        1. Make sure your printer is off.
        2. Run 'lsusb', Note what exists. 
        3. Turn on Printer, Run 'lsusb', Note what is new
        -- Formatted (????:????)
        4. Run 'lsusb -vvv -d ????:???? | grep iInterface'
        -- iIterface             ?
        5. Run 'lsusb -vvv -d ????:???? | grep bEndpointAddress | grep IN'
        -- bEndpointAddress ?x?? EP ? IN
        -- IN : ?x??
        6. Run 'lsusb -vvv -d ????:???? | grep bEndpointAddress | grep OUT'
        -- bEndpointAddress ?x?? EP ? OUT
        -- OUT : ?x??
'''
        txt = wx.StaticText(self, -1, label=note)
                   
        MainSizer.Add(txt, 0)
        name = 'maint_vendorID_txtctrl'
        tc = HUD.RH_TextCtrl(self, -1, name=name, size=(125,-1))
        tc.SetHint('Vendor Id')
        tc.SetToolTip(wx.ToolTip('Hardware ID of Receipt Printer'))
        tc.tableName = 'hardware_config'
        tc.fieldName = 'vendor_id'
        self.LSL.Add(name)
        MainSizer.Add(tc, 0, wx.ALL, 3)

        name = 'maint_productID_txtctrl'
        tc = HUD.RH_TextCtrl(self, -1, name=name, size=(125,-1))
        tc.SetHint('Product Id')
        tc.SetToolTip(wx.ToolTip('Product ID of Receipt Printer'))
        tc.tableName = 'hardware_config'
        tc.fieldName = 'product_id'
        self.LSL.Add(name)
        MainSizer.Add(tc, 0, wx.ALL, 3)

        name = 'maint_interfaceID_txtctrl'
        tc = HUD.RH_TextCtrl(self, -1, name=name, size=(125, -1))
        tc.SetHint('Interface ID')
        tc.SetToolTip(wx.ToolTip('Interface ID of Receipt Printer\nRun "lsusb -vvv -d ????:???? | grep iInterface"'))
        tc.tableName = 'hardware_config'
        tc.fieldName = 'interface_id'
        self.LSL.Add(name)
        MainSizer.Add(tc, 0, wx.ALL, 3)

        name = 'maint_iEndpoint_txtctrl'
        tc = HUD.RH_TextCtrl(self, -1, name=name, size=(125, -1))
        tc.SetHint('input EndPoint')
        tc.SetToolTip(wx.ToolTip('Interface Input Endpoint\nRun "lsusb -vvv -d ????:???? | grep bEndpointAddress | grep IN" '))
        tc.tableName = 'hardware_config'
        tc.fieldName = 'input_endpoint'
        self.LSL.Add(name)
        MainSizer.Add(tc, 0, wx.ALL, 3)

        name = 'maint_oEndpoint_txtctrl'
        tc = HUD.RH_TextCtrl(self, -1, name=name, size=(125, -1))
        tc.SetHint('output EndPoint')
        tc.SetToolTip(wx.ToolTip('Interface Output Endpoint\nRun "lsusb -vvv -d ????:???? | grep bEndpointAddress | grep OUT"'))
        tc.tableName = 'hardware_config'
        tc.fieldName = 'output_endpoint'
        self.LSL.Add(name)
        MainSizer.Add(tc, 0, wx.ALL, 3)

        self.SetSizer(MainSizer, 0)
        self.Layout()

        wx.CallAfter(self.OnLoad, event='')
    
    def OnLoad(self, event):
        for name in self.LSL.Get():
            item = wx.FindWindowByName(name).OnLoad('abuser', 'rhp')
            
                

#--------------------------

class ThemesTab(wx.Panel):
    def __init__(self, parent, size=(500,500),debug=True):
        """ Customer Data Tab """    
        wx.Panel.__init__(self,parent=parent, id=wx.ID_ANY)
        self.SetName('ThemesTab')
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        
        dept_list = ['POS','INVENTORY','CUSTOMERS','VENDORS']
        for label in dept_list:
            grid = gridlib.Grid(self, name='maint_theme_'+label+'_test_grid', style=wx.BORDER_SUNKEN)
            grid.DisableDragRowSize()
            grid.CreateGrid(2, 2)
        
            box = wx.StaticBox(self, -1, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.VERTICAL)
            hboxSizer = wx.BoxSizer(wx.HORIZONTAL)
            pick_list = [('Background','maint_theme_'+label+'_bg_colorctrl'),
                         ('Text','maint_theme_'+label+'_text_colorctrl'),
                         ('Alternate','maint_theme_'+label+'_cell_colorctrl')]
                         
            for cplabel, named in pick_list:
                boxd = wx.StaticBox(self, -1, label=cplabel, style=wx.ALIGN_RIGHT)
                boxdSizer = wx.StaticBoxSizer(boxd, wx.HORIZONTAL)
                cp = wx.ColourPickerCtrl(self, -1, name=named, style=wx.CLRP_USE_TEXTCTRL|wx.CLRP_SHOW_LABEL)
                if 'Background' in cplabel:
                    cp.SetColour(grid.GetLabelBackgroundColour())
                if 'Text' in cplabel:
                    cp.SetColour(grid.GetLabelTextColour())
                    
                cp.Bind(wx.EVT_COLOURPICKER_CHANGED, self.OnColourChange)
                boxdSizer.Add(cp, 0)
                
                hboxSizer.Add(boxdSizer, 0, wx.ALL, 1)
            
            hboxSizer.Add(grid,0, wx.ALL, 1)
                     
            boxSizer.Add(hboxSizer, 0, wx.ALL|wx.EXPAND, 1)
            
            MainSizer.Add(boxSizer, 0, wx.ALL, 1)            
            
        
        
        #MainSizer.Add(, 0, wx.ALL, 5)
        
        self.SetSizer(MainSizer, 0)
        self.Layout()
        wx.CallAfter(self.OnLoad, event='')

    def OnLoad(self, event):
        
        
        bg = '#ffffff'
        text = '#000000'
        cell = '#d6fcd7'
        category = ['POS','INVENTORY','CUSTOMERS','VENDORS']
        for cats in category:
            bg = HUD.Themes(cats).GetColor('bg')
            text = HUD.Themes(cats).GetColor('text')
            cell = HUD.Themes(cats).GetColor('cell')
            
#             print('CATA : ',cats)
#             query = 'SELECT bg, text, cell FROM themes WHERE theme_name=?'
#             print('query : ',query)
#             data = (cats,)
#             print('data : ',data)
#             returnd = HU.SQConnect(query, data).ONE()
#             print('returnd : ',returnd)
#             if returnd is not None:
#                 (bg,text,cell) = returnd
#             
#             print('BG : {} \;/ TEXT : {} \;/ CELL : {}'.format(bg, text, cell))    
            pick_list = [('Background','maint_theme_'+cats+'_bg_colorctrl', bg),
                         ('Standard Background','maint_theme_'+cats+'_text_colorctrl', text),
                         ('Cell Alternate','maint_theme_'+cats+'_cell_colorctrl', cell)]
            
            for label, named, vari in pick_list:
               ctrl = wx.FindWindowByName(named)
               
#                vari = re.sub('[b\']','',vari)
#                print('VARI : {}'.format(vari))
               ctrl.SetColour(vari)
               
        
        for cats in category:    
            
            testnamed = 'maint_theme_'+cats+'_test_grid'
            
            grid = wx.FindWindowByName(testnamed)    
            grid.SetLabelBackgroundColour(HUD.Themes(cats).GetColor('bg'))
            grid.SetLabelTextColour(HUD.Themes(cats).GetColor('text'))
            HUD.GridOps(grid.GetName()).GridAlternateColor(2)

    def OnColourChange(self, event):
        debug = False
        obj = event.GetEventObject()
        named = obj.GetName()
        
        item = wx.FindWindowByName(named)
        possib_list = ['_bg_', '_text_','_cell_']
        for srch in possib_list:
            if srch in named:
                whois = named.strip('maint_theme_').strip(srch+'colorctrl')
                print('Theme WhoIs : {} \n Named: {}'.format(whois, named))
                grid = wx.FindWindowByName('maint_theme_'+whois+'_test_grid')
                if '_bg_' in named:
                    grid.SetLabelBackgroundColour(item.GetColour())
                if '_text_' in named:
                    grid.SetLabelTextColour(item.GetColour())
                if '_alt_' in named:
                    for xx in range(grid.GetNumberRows()):
                        for yy in range(grid.GetNumberCols()):
                            if xx % 2:
                                grid.SetCellBackgroundColour(xx,yy,item.GetColour())
                                
        grid.Refresh()                         
        
     
    
    def OnSave(self):
        theme_list = ['POS','INVENTORY','CUSTOMERS','VENDORS']
        sub_list = ['bg','text','cell']
        dicted = {}
        
        for category in theme_list:
            
            HUD.QueryOps().CheckEntryExist('theme_name',category, ['themes'],debug=True)
            for sublistd in sub_list:
                named = 'maint_theme_'+category+'_'+sublistd+'_colorctrl'
                
                value = wx.FindWindowByName(named).GetColour()
                ss = value.GetAsString(wx.C2S_HTML_SYNTAX).encode('ascii')
                
                
                
                
                query = 'UPDATE themes SET {0} = ? WHERE theme_name = ?'.format(sublistd)  
                
                data = (str(ss),category,)
                
                returnd = SQConnect(query,data).ONE()
          
#--------------------------

class StartPanel(wx.Panel):
    def __init__(self,parent, debug=False):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        
        lookupSizer = wx.BoxSizer(wx.VERTICAL)
                
        IconBar_list =[('ExitButton', ButtonOps().Icons('exit'), self.OnExitButton)]
        
        IconBox = wx.StaticBox(self, label='')
        
        IconBarSizer = wx.StaticBoxSizer(IconBox, wx.HORIZONTAL)        
        xx = 0        
        for name,iconloc,handler in IconBar_list:
            icon = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(iconloc), name=name, style=wx.BORDER_NONE)                
            icon.Bind(wx.EVT_BUTTON, handler)
            IconBarSizer.Add((80,1),0)
            if 'Left' in name or 'Right' in name:
                IconBarSizer.Add(icon,0)
            elif 'Exit' in name and __file__ == 'Maintenance.py':
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
        
        

        level2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        notebook = wx.Notebook(self, wx.ID_ANY,name='Main_Notebook')
        tabOne = GeneralInfoTab(notebook)
        tabTwo = InventoryMaintenanceTab(notebook)
        tabThree = CustomerMaintenanceTab(notebook)
        tabThreeHalf = POSTab(notebook)
        tabFive = TaxInfoTab(notebook)
        tabSix = EmployeesTab(notebook)
        tabSix_half = PasswordsTab(notebook) 
        tabSeven = ThemesTab(notebook)
        tabEight = ReceiptTab(notebook)
        tabNine = HardwareTab(notebook)
        
        tab_list = [(tabOne, 'General Info'),
                    (tabTwo, 'Inventory Maintenance'),
                    (tabThree, 'Customer Maintenance'),
                    (tabThreeHalf, 'POS'),
                    (tabFive, 'Tax Info'),
                    (tabSix, 'Employees'),
                    (tabSix_half, 'Passwords'),
                    (tabSeven, 'Themes'),
                    (tabEight, 'Receipt'),
                    (tabNine, 'Hardware')]
        
        for tab, label in tab_list:
            notebook.AddPage(tab, label)
        
        #self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        
        level2Sizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)
        
        lookupSizer.Add(IconBarSizer, 0, flag=wx.ALL|wx.EXPAND)

        lookupSizer.Add(level1Sizer, 0)
        lookupSizer.Add(level2Sizer, 0, wx.ALL|wx.EXPAND, 5)
        
        self.SetSizer(lookupSizer, 0)
        
        self.Layout()


    def OnSave(self, event):
        tabSave_list = ['ThemesTab','Maintenance_GeneralInfoTab',
                        'InventoryMaintenanceTab','PriceOptionsTab',
                        'DiscountOptionsTab','Margin_GeneralMarginTab',
                        'Margin_ByCostTab','TaxInfoTab','ReceiptTab','CloseoutsTab']
        
        for name in tabSave_list:
            tab = wx.FindWindowByName(name)
            tab.OnSave()
                                    

#--------------------------
# Hardware Configs
#-----------------
        #HU.CheckEntryExist('abuser','rhp',['hardware_config'])
        
        #id_list = [('maintenance_vendorID_txtctrl', 'hardware_config', 'vendor_id'),
        #           ('maintenance_productID_txtctrl', 'hardware_config', 'product_id'),
        #           ('maintenance_interfaceID_txtctrl', 'hardware_config','interface_id'),
        #           ('maintenance_iEndpoint_txtctrl', 'hardware_config','input_endpoint'),
        #           ('maintenance_oEndpoint_txtctrl', 'hardware_config','output_endpoint')]

        #fieldSet, dataSet, table = HU.Commaize(id_list)
        
        #query = '''UPDATE {}
        #           SET {}
        #           WHERE abuser=(?)'''.format(table, fieldSet)
                   
        #data = dataSet + ['rhp',]
        
        #returnd = HU.SQConnect(query, data).ONE()
        
        #print 'returnd : {}'.format(returnd)




    def OnUndo(self, event):
            pass
        
    def OnExitButton(self, event):
        if __file__ == "Maintenance.py":
            item = wx.FindWindowByName('Maintenance_Frame')
            item.Close()
        else:
            tab = wx.FindWindowByName('MainFrame_notebook')
            tab.SetSelection(6)
            tab.SetFocus()
            



class MaintenanceScreen(wx.Frame):
    def __init__(self):
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX) & (~wx.MINIMIZE_BOX)
        wx.Frame.__init__(self, None, wx.ID_ANY, title="RHP Maintenance", size=(1200, 800), style=style)
        
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
