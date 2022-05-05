#!/usr/bin/env python
import wx,re,os 
import wx.grid as gridlib
import sys
import sqlite3
import json
import pout
import datetime
from ObjectListView import ObjectListView, ColumnDefn
import wx.lib.masked as masked
from wx.lib.masked.textctrl import TextCtrl as MTextCtrl
from wx.lib.masked import NumCtrl
import wx.lib.agw.flatnotebook as fnb
from controls import RH_OLV, RH_Button, RH_ListBox, GridOps, Themes, RH_Icon, LoadSaveList, IconList, RH_CheckBox, RH_TextCtrl, RH_FilePickerCtrl, RH_MTextCtrl, RH_RadioBox, RH_ComboBox, RH_NumCtrl
from controls import tSizer, LoadSaveDict
from dialogs import PasswordDialog
from events import EventOps
from decimal import Decimal, ROUND_HALF_UP
import wx.lib.inspection
from db_ops import SQConnect, QueryOps, LookupDB, GetSQLFile, DBConnect, Detupler
from panels import AltLookup, Tax_Table_Grid, TBA
from utils import IconPanel


class ThemesTab(wx.Panel):
    def __init__(self, parent, size=(500,500), debug=False):
        """ Themes Tab """    
        wx.Panel.__init__(self,parent=parent, id=wx.ID_ANY)
        self.SetName('Maintenance_ThemesTab')

    

class HardwareTab(wx.Panel):
    def __init__(self, parent, size=(500,500), debug=False):
        """ Hardware Tab """    
        wx.Panel.__init__(self,parent=parent, id=wx.ID_ANY)
        self.SetName('Maintenance_HardwareTab')

    

class ReceiptTab(wx.Panel):
    def __init__(self, parent, size=(500,500), debug=False):
        """ Receipt Tab """    
        wx.Panel.__init__(self,parent=parent, id=wx.ID_ANY)
        self.SetName('Maintenance_ReceiptTab')

    

class PasswordsTab(wx.Panel):
    def __init__(self, parent, size=(500,500), debug=False):
        """ Passwords Tab """    
        wx.Panel.__init__(self,parent=parent, id=wx.ID_ANY)
        self.SetName('Maintenance_PasswordsTab')

    
class EmployeesTab(wx.Panel):
    def __init__(self, parent, size=(500,500), debug=False):
        """ Employees Tab """    
        wx.Panel.__init__(self,parent=parent, id=wx.ID_ANY)
        self.SetName('Maintenance_EmployeesTab')

    
class TaxInfoTab(wx.Panel):
    def __init__(self, parent, size=(500,500), debug=False):
        """ Tax Info Tab """    
        wx.Panel.__init__(self,parent=parent, id=wx.ID_ANY)
        self.SetName('Maintenance_TaxInfoTab')
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        rclick = 'Right Clicking on a line deletes that Tax Record from db'
        rcs = wx.StaticText(self, -1, label=rclick)
        rcs.SetForegroundColour('RED')
        MainSizer.Add(rcs, 0, wx.ALL|wx.ALIGN_CENTER, 10)
        icon = IconList()
        save = icon.getIcon('save')
        self.si = wx.Button(self, -1, label=save, style=wx.BORDER)
        self.si.SetFont(icon.getFont(size=60))
        self.si.Bind(wx.EVT_BUTTON, self.OnSave)
        MainSizer.Add(self.si, 0, wx.ALL|wx.ALIGN_CENTER, 10)

        self.TaxGrid = Tax_Table_Grid(self, name='taxinfotab_taxinfo_grid', size=(900,500))
        
        MainSizer.Add(self.TaxGrid, 0, wx.ALL|wx.ALIGN_CENTER, 10)
        self.SetSizer(MainSizer,0)
        self.Layout()

    def OnSave(self, evt):
        self.TaxGrid.OnSave()
    
class POSTab(wx.Panel):
    def __init__(self, parent, size=(500,500), debug=False):
        """ POS Tab """    
        wx.Panel.__init__(self,parent=parent, id=wx.ID_ANY)
        self.SetName('Maintenance_POSTab')


class GeneralDetailsTab(wx.Panel):
    def __init__(self, parent, debug=False):
        """General Details Tab for the Inventory"""
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.SetName('MaintInvTab_GeneralDetailsTab')
        self.LSL = LoadSaveList()
        self.sqlfile = './db/SUPPORT.sql'

        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        level1Sizer = wx.BoxSizer(wx.VERTICAL)
        level2Sizer = wx.BoxSizer(wx.VERTICAL)
        level3Sizer = wx.BoxSizer(wx.VERTICAL)
        
        icon = IconList()
        save = icon.getIcon('save')
        self.si = wx.Button(self, -1, label=save, style=wx.BORDER_NONE)
        self.si.SetFont(icon.getFont(size=60))
        self.si.Bind(wx.EVT_BUTTON, self.OnSave)
        level3Sizer.Add(self.si, 0, wx.ALL, 3)

        lbsize = (300, 100)
        
        name = 'invMaint_department_listbox'                     
        self.dept_lb = AltLookup(self, boxlabel='Departments', 
                                 lbsize=lbsize, 
                                 lbname=name, 
                                 tableName='organizations', 
                                 fieldName='department')            
        self.LSL.Add(self.dept_lb)
        level1Sizer.Add(self.dept_lb, 0, wx.ALL, 3)
        
        name = 'invMaint_category_listbox'
        self.cat_lb = AltLookup(self, boxlabel='Category',
                                 lbsize=lbsize,
                                 lbname=name,
                                 tableName='organizations',
                                 fieldName='category')
        self.LSL.Add(self.cat_lb)
        level1Sizer.Add(self.cat_lb, 0, wx.ALL, 3)
        
        name = 'invMaint_subcategory_listbox'
        self.subcat_lb = AltLookup(self, boxlabel='Sub-Category', 
                                 lbsize=lbsize, 
                                 lbname=name,
                                 tableName='organizations',
                                 fieldName='subcategory')
        self.LSL.Add(self.subcat_lb)
        level1Sizer.Add(self.subcat_lb, 0, wx.ALL, 3)

        name = 'invMaint_material_listbox'
        self.material_lb = AltLookup(self, boxlabel='Material', 
                                 lbsize=lbsize, 
                                 lbname=name,
                                 tableName='organizations',
                                 fieldName='material')
        self.LSL.Add(self.material_lb)
        level1Sizer.Add(self.material_lb, 0, wx.ALL, 3)

        name = 'invMaint_location_listbox'
        self.location_lb = AltLookup(self, boxlabel='Location', 
                                 lbsize=lbsize, 
                                 lbname=name,
                                 tableName='organizations',
                                 fieldName='location')
        self.LSL.Add(self.location_lb)
        level2Sizer.Add(self.location_lb, 0, wx.ALL, 3)

        name = 'invMaint_zone_listbox'
        self.zone_lb = AltLookup(self, boxlabel='Zone', 
                                 lbsize=lbsize, 
                                 lbname=name,
                                 tableName='organizations',
                                 fieldName='zone')
        self.LSL.Add(self.zone_lb)
        level2Sizer.Add(self.zone_lb, 0, wx.ALL, 3)

        name = 'invMaint_unittype_listbox'
        self.unit_lb = AltLookup(self, boxlabel='Unit Type', 
                                 lbsize=lbsize, 
                                 lbname=name,
                                 tableName='organizations',
                                 fieldName='unittype')
        self.LSL.Add(self.unit_lb)
        level2Sizer.Add(self.unit_lb, 0, wx.ALL, 3)

        MainSizer.Add(level1Sizer, 0, wx.ALL, 3)
        MainSizer.Add(level2Sizer, 0, wx.ALL, 3)
        MainSizer.Add(level3Sizer, 0, wx.ALL, 3)
        
        self.SetSizer(MainSizer)
        self.Layout()
        
        wx.CallAfter(self.OnLoad, event='')        
    
            
    def OnLoad(self, event):
        load_list = [(self.dept_lb, 'department', 'id'),
                     (self.cat_lb, 'category', 'id'),
                     (self.subcat_lb, 'subcategory', 'id'),
                     (self.material_lb, 'material', 'id'),
                     (self.location_lb, 'location', 'id'),
                     (self.zone_lb, 'zone', 'id'),
                     (self.unit_lb, 'unittype', 'id'),]
        
        for ctrl, tablename, fieldname in load_list:
            q = f'SELECT id FROM {tablename}'
            d = ()
            r = SQConnect(q, d, self.sqlfile).ALL()

            if len(r) > 0:
                a = Detupler(r).ListIt()
                ctrl.SetItems(a)

            
    def OnSave(self, event):
        save_list = [(self.dept_lb, 'department', 'department'),
                     (self.cat_lb, 'category', 'category'),
                     (self.subcat_lb, 'subcategory', 'subcategory'),
                     (self.material_lb, 'material', 'material'),
                     (self.location_lb, 'location', 'location'),
                     (self.zone_lb, 'zone', 'zone'),
                     (self.unit_lb, 'unittype', 'unittype'),]
        
        for ctrl, tablename, fieldname in save_list:
            value = ctrl.GetItems()
            for i in value:
                try:
                    q = f'INSERT INTO {tablename} VALUES (?);'
                    d = (i,)
                    r = DBConnect(q, d, self.sqlfile).ONE()
                except sqlite3.Error as error:
                    print('delt', error)    
            
        # for item in self.LSL.Get():
        #     #item = wx.FindWindowByName(name)
        #     item.OnSave('')


class ByCategoryTab(wx.Panel):
    def __init__(self, parent, debug=False):
        """Margin ByCategory Tab for the Inventory"""
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.SetName('MaintInvPricingMarginTab_ByCategoryTab')

class ByCostTab(wx.Panel):
    def __init__(self, parent, debug=False):
        """Margin ByCost Tab for the Inventory"""
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.SetName('MaintInvPricingMarginTab_ByCostTab')

class ByVendorTab(wx.Panel):
    def __init__(self, parent, debug=False):
        """Margin ByVendor Tab for the Inventory"""
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.SetName('MaintInvPricingMarginTab_ByVendorTab')


class GeneralMarginTab(wx.Panel):
    def __init__(self, parent, debug=False):
        """MarginGeneral Details Tab for the Inventory"""
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.SetName('MaintInvPricingMarginTab_GeneralMarginTab')
        MainSizer = wx.BoxSizer(wx.VERTICAL)

        self.genmargin = RH_NumCtrl(self, -1, size=(50,-1), min=0, max=100, allowNegative=False)
        tS = tSizer(self, 'General Margin', self.genmargin)
        MainSizer.Add(tS, 0)
        self.SetSizer(MainSizer)
        self.Layout()

class MarginTab(wx.Panel):
    def __init__(self, parent, debug=False):
        """MarginGeneral Details Tab for the Inventory"""
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.SetName('MaintInvPricingTab_MarginTab')
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetName('MarginTab')
        
        self.rbox = RH_RadioBox(self, -1, 
                           choices=['General','By Cost','By Category', 'By Vendor'],
                           name='generalMargin_control_rbox', 
                           label='Figuring Initial Starting Margin')
        self.rbox.tableName = 'item_margin'
        self.rbox.fieldName = 'starting_margin_control'
        self.rbox.Bind(wx.EVT_RADIOBOX, self.onBoxChoice)
        
        self.nb = wx.Notebook(self, wx.ID_ANY,name='MarginTab_Notebook')
        self.nb.AddPage(GeneralMarginTab(self.nb), "General")
        self.nb.AddPage(ByCostTab(self.nb), "By Cost")
        self.nb.AddPage(ByCategoryTab(self.nb), "By Category")
        self.nb.AddPage(ByVendorTab(self.nb), "By Vendor")
        MainSizer.Add(self.rbox, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        MainSizer.Add(self.nb, 1, wx.ALL|wx.EXPAND, 5)
        
        
        
        self.SetSizer(MainSizer, 0)
        self.Layout()
    
    def onBoxChoice(self, event):
        idxselection = self.rbox.GetSelection()
        selection = self.rbox.GetStringSelection()
        # notebook = wx.FindWindowByName('MarginTab_Notebook')
        tabCount = self.nb.GetPageCount()
        self.nb.SetSelection(idxselection)    
        #print("Radio Box CHoice : ",selection)
    

class DiscountOptionsTab(wx.Panel):
    def __init__(self, parent, debug=False):
        """Discount Options Tab for the Pricing Sections of the Inventory"""
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.SetName('MaintInvPricingTab_DiscOptionsTab')
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.tba = wx.StaticText(self, -1, 'Discount Options TO BE ADDED')
        
        MainSizer.Add(self.tba, 0)
        self.SetSizer(MainSizer)
        self.Layout()

class CloseoutsTab(wx.Panel):
    def __init__(self, parent, debug=False):
        """Closeouts Tab for the Pricing Sections of the Inventory"""
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.SetName('MaintInvPricingTab_CloseoutsTab')

class PriceOptionsTab(wx.Panel):
    def __init__(self, parent, debug=False):
        """Pricing Options Tab for the Inventory"""
        wx.Panel.__init__(self,parent=parent, id=wx.ID_ANY)
        self.SetName('Maintenance_PriceOptionsTab')
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        self.tba = wx.StaticText(self, -1, 'TO BE ADDED')
        MainSizer.Add(self.tba, 0)

        # listboxes = [('Price Schemes','invMaint_priceSchemes_listbox')]
        # colLabel_list = [('Name',120),('Scheme',90),('Reduce By',75)]
        # self.priceSchemes_lc = RH_OLV(self,size=(300,260), name='invMaint_priceSchemes_listctrl', style=wx.LC_REPORT|wx.BORDER_SIMPLE)      
        # self.priceSchemes_lc.SetColumns([
        #                     ColumnDefn('Name','left',120,'named'),
        #                     ColumnDefn('Scheme','center',90,'schemed'),
        #                     ColumnDefn('Reduce By','center',75,'reduced')
        #                     ])

        # self.priceSchemes_lc.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelect)
        # idx = 0
        
        # explanation = 'Enter a Scheme i.e. \'1-3-10\' According to Starting Margin & Reduced_By will \nset each additional unit qty less by reduced_by percentage separated by \'-\' dashes\n Also \'1-PK-2X\' will result in \'1 & box qty & box qty * 2\''              
        # text = wx.StaticText(self, -1, label=explanation)
        
        # editSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # edit_list = [('Name','invMaint_priceSchemes_listctrl_name_txtctrl'),
        #              #('Schemed','invMaint_priceSchemes_listctrl_scheme_txtctrl'),
        #              #('Reduce By','invMaint_priceSchemes_listctrl_reduceby_numctrl'),
        #             #  ('Qty','invMaint_priceSchemes_qty1_txtctrl'),
        #             #  ('Operator','invMaint_priceSchemes_opt1_combobox'),
        #             #  ('Margin', 'invMaint_priceSchemes_margin1_txtctrl'),
        #              ('Qty','invMaint_priceSchemes_qty2_txtctrl'),
        #              ('Operator','invMaint_priceSchemes_opt2_combobox'),
        #              ('Margin', 'invMaint_priceSchemes_margin2_txtctrl'),
        #              ('Qty','invMaint_priceSchemes_qty3_txtctrl'),
        #              ('Operator','invMaint_priceSchemes_opt3_combobox'),
        #              ('Margin', 'invMaint_priceSchemes_margin3_txtctrl'),
        #              ('Qty','invMaint_priceSchemes_qty4_txtctrl'),
        #              ('Operator','invMaint_priceSchemes_opt4_combobox'),
        #              ('Margin', 'invMaint_priceSchemes_margin4_txtctrl'),
        #              ('Add','invMaint_priceSchemes_listctrl_add_button'),
        #              ('Delete','invMaint_priceSchemes_listctrl_delete_button'),
        #              ('Clear','invMaint_priceSchemes_listctrl_clear_button')]

        # name = 'invMaint_priceSchemes_listctrl_name_texctrl'
        # self.name_tc = RH_TextCtrl(self, -1, name=name)             
        # self.name_tc.SetToolTip(wx.ToolTip('Enter a Percentage of Margin you wish to Reduce the initial margin by'))
        # self.name_tc.Bind(wx.EVT_KILL_FOCUS, EventOps().Capitals)
        # tS = tSizer(self, 'Scheme Name', self.name_tc)
        # editSizer.Add(tS, 0)

        # name = 'invMaint_priceSchemes_qty1_textctrl'
        # self.qty1_tc = RH_TextCtrl(self, -1, name=name)
        # tS = tSizer(self, 'Qty', self.qty1_tc)
        # editSizer.Add(tS, 0)

        # name = 'invMaint_priceSchemes_opt1_combobox'
        # self.opt1_cbox = RH_ComboBox(self, -1, choices=[], name=name)
        # tS = tSizer(self, 'Operator', self.opt1_cbox)
        # editSizer.Add(tS, 0)
        
        # name = 'invMaint_priceSchemes_margin1_textctrl'
        # self.margin1_tc = RH_TextCtrl(self, -1, name=name)
        # tS = tSizer(self, 'Margin', self.margin1_tc)
        # editSizer.Add(tS, 0)

        # # name = 'invMaint_priceSchemes_qty2_textctrl'
        # # self.qty1_tc = RH_TextCtrl(self, -1, name=name)
        # # editSizer.Add(self.qty1_tc, 0)

        # # name = 'invMaint_priceSchemes_opt2_combobox'
        # # self.opt1_cbox = RH_ComboBox(self, -1, choices=[], name=name)
        # # editSizer.Add(self.opt1_cbox)
        
        # # name = 'invMaint_priceSchemes_margin2_textctrl'
        # # self.margin1_tc = RH_TextCtrl(self, -1, name=name)
        # # editSizer.Add(self.margin1_tc)



        # # icon = IconList()
        # # for label, name in edit_list:
        # #     box = wx.StaticBox(self, label=label)
        # #     boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        # #     if '_reduceby_' in name:
        # #         ctrl = RH_TextCtrl(self, -1, name=name)
        # #         ctrl.SetToolTip(wx.ToolTip('Enter a Percentage of Margin you wish to Reduce the initial margin by'))
                
        # #     if '_name_' in name:
        # #         ctrl = RH_MTextCtrl(self, -1, name=name, mask='XXXXXXXXX')
        # #         ctrl.SetToolTip(wx.ToolTip('Enter a Name for the Scheme within 9 characters'))
        # #         ctrl.Bind(wx.EVT_KILL_FOCUS, EventOps().Capitals)
                
        # #     if '_scheme_' in name:
        # #         ctrl = RH_TextCtrl(self, -1, name=name)
        # #         ctrl.Bind(wx.EVT_KILL_FOCUS, EventOps().Capitals)
        # #         #ctrl.SetToolTip(wx.ToolTip('Enter a Scheme i.e. \'1-3-10\' According to Starting Margin & Reduced_By will \nset each additional unit qty less by reduced_by percentage separated by \'-\' dashes\n Also \'1-PK-2X\' will result in \'1 & box qty & box qty * 2\''))     
            
        # #     if 'button' in name:
        # #         save = icon.getIcon(label.lower())
        # #         self.si = wx.Button(self, -1, label=save, style=wx.BORDER_NONE)
        # #         self.si.SetFont(icon.getFont(size=60))
        # #         self.si.Bind(wx.EVT_BUTTON, self.onButton)
        
        # #         # ctrl = RH_Button(self, label=label, name=name, size=(20))
        # #         # ctrl.Bind(wx.EVT_BUTTON, self.onButton)
            
        # #     if 'delete' in name:    
        # #         ctrl.Disable()
                
        # #     if not 'button' in name:
        # #         #boxSizer.Add(ctrl, 0)        
        # #         editSizer.Add(boxSizer, 0)
        # #     else:
        # #         editSizer.Add(ctrl, 0)
        
        # MainSizer.Add(self.priceSchemes_lc, 0)
        # MainSizer.Add(editSizer,0)
        # MainSizer.Add(text, 0)
        
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
            ListCtrl_Ops(lc_name).LCFill(setList, idx)
            
    
    def OnSave(self):
        print("Pricing Schemes")
        listctrl = wx.FindWindowByName('invMaint_priceSchemes_listctrl')
        count = listctrl.GetItemCount()
        for idx in range(count):
            name_scheme = listctrl.GetItemText(idx)
            print("Get Item {0} : {1}".format(listctrl.GetItem(idx), name_scheme))     
            queryWhere = 'name=(?)'
            queryData = (name_scheme,)
            countd = QueryOps().QueryCheck('item_pricing_schemes',queryWhere,queryData)
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


class InventoryMaintenanceTab(wx.Panel):
    def __init__(self, parent, size=(1150,750), debug=False):
        """ Customer Data Tab """    
        super(InventoryMaintenanceTab, self).__init__(parent)
        wx.Panel.__init__(self,parent=parent, id=wx.ID_ANY)
        self.SetName('Maintenance_InvTab')
        
        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        # windowstyle = fnb.FNB_NO_X_BUTTON|fnb.FNB_NO_NAV_BUTTONS|fnb.FNB_NODRAG|fnb.FNB_FF2
        # nb = fnb.FlatNotebook(self, wx.ID_ANY,name='InvTab_Notebook', agwStyle=windowstyle)
        nb = wx.Notebook(self, wx.ID_ANY, name='InvTab_Notebook', style=8)
        nb.AddPage(GeneralDetailsTab(nb), "General Details")
        nb.AddPage(PriceOptionsTab(nb), "Price Options")
        nb.AddPage(MarginTab(nb), "Margin")
        nb.AddPage(DiscountOptionsTab(nb), "Discounts")
        nb.AddPage(CloseoutsTab(nb), "Closeouts")
        
        MainSizer.Add(nb, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(MainSizer)
        
        self.Layout()

    

class CustomerMaintenanceTab(wx.Panel):
    def __init__(self, parent, debug=False):
        """ General Info Tab """
        super(CustomerMaintenanceTab, self).__init__(parent)    
        wx.Panel.__init__(self,parent=parent, id=wx.ID_ANY)
        self.SetName('Maintenance_CustomerTab')

    

class GeneralInfoTab(wx.Panel):
    def __init__(self, parent, debug=False):
        """ General Info Tab """    
        super(GeneralInfoTab, self).__init__(parent)
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.SetName('Maintenance_GeneralInfoTab')
        self.LSL = LoadSaveList()

        MainSizer = wx.BoxSizer(wx.VERTICAL)
        Row1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        Row_underSizer = wx.BoxSizer(wx.HORIZONTAL)
        Row_under2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        Row_under3Sizer = wx.BoxSizer(wx.HORIZONTAL)
        Col1Sizer = wx.BoxSizer(wx.VERTICAL)
        Col3Sizer = wx.BoxSizer(wx.VERTICAL)
        
        name = 'geninfo_storenum_txtctrl'
        self.storenum_tc = RH_TextCtrl(self, -1, name=name, size=(85, -1), style=wx.TE_PROCESS_ENTER)
        self.storenum_tc.tableName = 'basic_store_info'
        self.storenum_tc.fieldName = 'store_num'
        self.storenum_tc.sqlfile = './db/CONFIG.sql'
        self.storenum_tc.loadAs = 'str'
        self.storenum_tc.saveAs = 'int'

        self.storenum_tc.Bind(wx.EVT_TEXT_ENTER, self.onLoad)
        self.LSL.Add(self.storenum_tc)
        tS = tSizer(self, 'Store Number', self.storenum_tc)
        Row_under3Sizer.Add(tS, 0, wx.ALL, 3)
        
        icon = IconList()
        save = icon.getIcon('save')
        self.si = wx.Button(self, -1, label=save, style=wx.BORDER_NONE)
        self.si.SetFont(icon.getFont(size=60))
        self.si.Bind(wx.EVT_BUTTON, self.onSave)
        #self.sih = RH_Button(self, -1, label=save, fontsize=50)

        #self.saveicon = RH_Icon(self, -1, label='save', fontsize=50)
        #self.saveicon.Bind(wx.EVT_BUTTON, self.onSave)
        
        Row_under3Sizer.Add(self.si, 0, wx.ALL, 3)
        #Row_under3Sizer.Add(self.saveicon, 0, wx.ALL, 3)
        sl = wx.StaticLine(self, -1, size=(350, 1), style=wx.LI_HORIZONTAL)
        Col1Sizer.Add(Row_under3Sizer, 0, wx.ALL, 3)
        Col1Sizer.Add(sl, 0)
        
        name = 'geninfo_storename_txtctrl'
        self.storename_tc = RH_TextCtrl(self, -1, name=name, size=(300, -1))
        self.storename_tc.tableName = 'basic_store_info'
        self.storename_tc.fieldName = 'name'
        self.storename_tc.sqlfile = './db/CONFIG.sql'
        self.storename_tc.loadAs = 'str'
        self.storename_tc.saveAs = 'str'
        self.LSL.Add(self.storename_tc)
        tS = tSizer(self, 'Store Name', self.storename_tc)
        Col1Sizer.Add(tS, 0, wx.ALL, 3)

        name = 'geninfo_address1_txtctrl'
        self.address1_tc = RH_TextCtrl(self, -1, name=name, size=(300, -1))
        self.address1_tc.tableName = 'basic_store_info'
        self.address1_tc.fieldName = 'address1'
        self.address1_tc.sqlfile = './db/CONFIG.sql'
        self.address1_tc.loadAs = 'str'
        self.address1_tc.saveAs = 'str'
        self.LSL.Add(self.address1_tc)
        tS = tSizer(self, 'Address Line 1', self.address1_tc)
        Col1Sizer.Add(tS, 0, wx.ALL, 3)

        name = 'geninfo_address2_txtctrl'
        self.address2_tc = RH_TextCtrl(self, -1, name=name, size=(300, -1))
        self.address2_tc.tableName = 'basic_store_info'
        self.address2_tc.fieldName = 'address2'
        self.address2_tc.sqlfile = './db/CONFIG.sql'
        self.address2_tc.loadAs = 'str'
        self.address2_tc.saveAs = 'str'
        self.LSL.Add(self.address2_tc)
        tS = tSizer(self, 'Address Line 2', self.address2_tc)
        Col1Sizer.Add(tS, 0, wx.ALL, 3)

        name = 'geninfo_city_txtctrl'
        self.city_tc = RH_TextCtrl(self, -1, name=name, size=(190,-1))
        self.city_tc.tableName = 'basic_store_info'
        self.city_tc.fieldName = 'city'
        self.city_tc.sqlfile = './db/CONFIG.sql'
        self.city_tc.loadAs = 'str'
        self.city_tc.saveAs = 'str'
        self.LSL.Add(self.city_tc)
        tS = tSizer(self, 'City', self.city_tc)
        Row_underSizer.Add(tS, 0, wx.ALL, 3)
        
        name = 'geninfo_state_txtctrl'
        self.state_tc = RH_MTextCtrl(self, -1, name=name, size=(75, -1), mask='CC', formatcodes='!')
        self.state_tc.tableName = 'basic_store_info'
        self.state_tc.fieldName = 'state'
        self.state_tc.sqlfile = './db/CONFIG.sql'
        self.state_tc.loadAs = 'str'
        self.state_tc.saveAs = 'str'
        self.LSL.Add(self.state_tc)
        tS = tSizer(self, 'State', self.state_tc)
        Row_underSizer.Add(tS, 0, wx.ALL, 3)

        name = 'geninfo_zipcode_txtctrl'
        self.zipcode_tc =RH_MTextCtrl(self, -1, name=name, size=(90, -1), mask='#####')
        self.zipcode_tc.tableName = 'basic_store_info'
        self.zipcode_tc.fieldName = 'zip'
        self.zipcode_tc.sqlfile = './db/CONFIG.sql'
        self.zipcode_tc.loadAs = 'str'
        self.zipcode_tc.saveAs = 'str'
        self.LSL.Add(self.zipcode_tc)
        tS = tSizer(self, 'Zipcode', self.zipcode_tc)
        Row_underSizer.Add(tS, 0, wx.ALL, 3)
        Col1Sizer.Add(Row_underSizer, 0, wx.ALL, 3)

        name = 'geninfo_phone1_txtctrl'
        self.phone1_tc = RH_MTextCtrl(self, -1, name=name, size=(200, -1), mask='(###) ###-#### x:########')
        self.phone1_tc.tableName = 'basic_store_info'
        self.phone1_tc.fieldName = 'phone1'
        self.phone1_tc.sqlfile = './db/CONFIG.sql'
        self.phone1_tc.loadAs = 'str'
        self.phone1_tc.saveAs = 'str'
        self.LSL.Add(self.phone1_tc)
        tS = tSizer(self, 'Phone 1', self.phone1_tc)
        Row_under2Sizer.Add(tS, 0, wx.ALL, 3)

        name = 'geninfo_phone2_txtctrl'
        self.phone2_tc = RH_MTextCtrl(self, -1, name=name, size=(200,-1), mask='(###) ###-#### x:########')
        self.phone2_tc.tableName = 'basic_store_info'
        self.phone2_tc.fieldName = 'phone2'
        self.phone2_tc.sqlfile = './db/CONFIG.sql'
        self.phone2_tc.loadAs = 'str'
        self.phone2_tc.saveAs = 'str'
        self.LSL.Add(self.phone2_tc)
        tS = tSizer(self, 'Phone 2', self.phone2_tc)
        Row_under2Sizer.Add(tS, 0, wx.ALL, 3)

        name = 'geninfo_fax_txtctrl'
        self.fax_tc =RH_MTextCtrl(self, -1, name=name, size=(200, -1), mask='(###) ###-####')
        self.fax_tc.tableName = 'basic_store_info'
        self.fax_tc.fieldName = 'fax'
        self.fax_tc.sqlfile = './db/CONFIG.sql'
        self.fax_tc.loadAs = 'str'
        self.fax_tc.saveAs = 'str'
        self.LSL.Add(self.fax_tc)
        tS = tSizer(self, 'Fax', self.fax_tc)
        Row_under2Sizer.Add(tS, 0, wx.ALL, 3)
        Col1Sizer.Add(Row_under2Sizer, 0, wx.ALL, 3)

        name = 'geninfo_email_txtctrl'
        self.email_tc = RH_MTextCtrl(self, -1, name=name, size=(150, -1), autoformat='EMAIL')
        self.email_tc.SetMaxLength(150)
        self.email_tc.tableName = 'basic_store_info'
        self.email_tc.fieldName = 'email'
        self.email_tc.sqlfile = './db/CONFIG.sql'
        self.email_tc.loadAs = 'str'
        self.email_tc.saveAs = 'str'
        self.LSL.Add(self.email_tc)
        tS = tSizer(self, 'Email', self.email_tc)
        Col1Sizer.Add(tS, 0, wx.ALL, 3)

        name = 'geninfo_website_txtctrl'
        self.website_tc = RH_TextCtrl(self, -1, name=name, size=(300, -1))
        self.website_tc.tableName = 'basic_store_info'
        self.website_tc.fieldName = 'website'
        self.website_tc.sqlfile = './db/CONFIG.sql'
        self.website_tc.loadAs = 'str'
        self.website_tc.saveAs = 'str'
        self.LSL.Add(self.website_tc)
        #self.website_tc.SetValidRegex('^((https?|ftp|smtp):\/\/)?(www.)?[a-z0-9]+\.[a-z]+(\/[a-zA-Z0-9#]+\/?)*$')
        ts = tSizer(self, text='Website URL', ctrl=self.website_tc)
        Col1Sizer.Add(ts, 0, wx.ALL, 3)
        
        slideSizer = wx.BoxSizer(wx.HORIZONTAL)
        name = 'geninfo_logoLoc_filectrl'
        self.filepicker_c = RH_FilePickerCtrl(self, -1, 
                                     name=name,
                                     message='Please Select Logo Location',
                                     wildcard='Images (*.jpg,*.png,*.gif)|*.jpg;*.gif;*.png',
                                     size=(300, -1),
                                     style=wx.FLP_DEFAULT_STYLE)
        st = wx.StaticText(self, -1, label='  Logo size: (90px, 90px) \n  File Extensions: jpg, gif, png')
        st.SetForegroundColour(wx.Colour(169,169,169))
        Col1Sizer.Add(st, 0)
        self.filepicker_c.Bind(wx.EVT_FILEPICKER_CHANGED, self.LogoPreview)
        self.filepicker_c.tableName = 'basic_store_info'
        self.filepicker_c.fieldName = 'logo'
        self.filepicker_c.sqlfile = './db/CONFIG.sql'
        self.filepicker_c.loadAs = 'str'
        self.filepicker_c.saveAs = 'str'
        self.LSL.Add(self.filepicker_c)
        
        tS = tSizer(self, 'Logo File Location', self.filepicker_c)
        slideSizer.Add(tS, 0, wx.ALL, 3)
        
        image = wx.Image('./images/empty-300x300.png', wx.BITMAP_TYPE_ANY)
        self.imageBitmap = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(image), name='geninfo_logoLoc_image')
        
        slideSizer.Add(self.imageBitmap, 0, wx.ALL, 3)
        Col1Sizer.Add(slideSizer, 0, wx.ALL, 3)
        
        # name = 'geninfo_printonforms_checkbox'
        # self.printonforms_cb = RH_CheckBox(self, -1, name=name, label='print on forms')
        # self.LSL.Add(name)
        # Col3Sizer.Add(self.printonforms_cb, 0)
        
        # name = 'geninfo_latecharge_numctrl'
        # self.latecharge_nc = NumCtrl(self, -1, value=0, name=name, integerWidth=3, fractionWidth=2)
        # self.LSL.Add(name)
        # tS = tSizer(self, 'Late Charge', self.latecharge_nc)
        # Col3Sizer.AddSpacer(35)
        # Col3Sizer.Add(tS, 0)
        
        Row1Sizer.Add(Col1Sizer, 0, wx.ALL, 3)
        Row1Sizer.Add(Col3Sizer, 0)
        
        MainSizer.Add(Row1Sizer, 0, wx.ALL|wx.EXPAND, 10)
        self.SetSizerAndFit(MainSizer, 0)
        self.Layout()
        

        wx.CallAfter(self.onLoad, event="")

    def LogoPreview(self, event):
        value = self.filepicker_c.GetCtrl()
        img = './images/empty-300x300.png'
        if os.path.isfile(value):
            img = value
        
        try:
            image = wx.Image(img, wx.BITMAP_TYPE_ANY)
            self.imageBitmap.SetBitmap(wx.Bitmap(image))
            self.imageBitmap.Refresh()
        except:
            pass
    
    
    def onLoad(self, event):
        storeNum = self.storenum_tc.GetValue()
        listd = self.LSL.To_Dict()
        print(listd)
        q, d, sqlfile = self.LSL.GetSelectQD(listd['basic_store_info']['selects'])
        r = SQConnect(q, d, sqlfile).ONE()

        for key in listd:
            # selects = ','.join(listd[key]['selects'])
            # q = f'SELECT {selects} FROM {key}'
            # d = ()
            print(q,d, sqlfile)
            r = SQConnect(q, d, sqlfile).ONE()

            idx = 0            
            for i in listd[key]['selects']:
                listd[key][i].update({'set':r[idx]})
                idx += 1

            pout.v(listd)

            for i in listd[key]:
                print(f'listd[{key}][{i}]')
                if not 'selects' in i:
                    setItem = listd[key][i]['set']
                    objItem = listd[key][i]['obj']
                    objItem.SetCtrl(setItem)
            
        
    def onSave(self, event):
        # listd = self.LSL.To_Dict()
        # q,d, sqlfile = self.LSL.UpdateQD(listd['basic_store_info']['selects'], 'store_num')
        # pout.v(q, d, sqlfile)
        # r = SQConnect(q, d, sqlfile).ONE()
        
        sqlfile = self.storenum_tc.sqlfile
        storenumd = self.storenum_tc.GetCtrl()
        named = self.storename_tc.GetCtrl()
        addr1 = self.address1_tc.GetCtrl()
        addr2 = self.address2_tc.GetCtrl()
        cityd = self.city_tc.GetCtrl()
        stated = self.state_tc.GetCtrl()
        zipd = self.zipcode_tc.GetCtrl()
        phon1d = self.phone1_tc.GetCtrl()
        phon2d = self.phone2_tc.GetCtrl()
        faxd = self.fax_tc.GetCtrl()
        emaild = self.email_tc.GetCtrl()
        sited = self.website_tc.GetCtrl()
        logod = self.filepicker_c.GetCtrl()

        q = '''UPDATE basic_store_info 
               SET name=?, address1=?, address2=?, city=?, state=?, zip=?, phone1=?, phone2=?, fax=?, email=?, website=?, logo=?
               WHERE store_num=?'''
        d = (named, addr1, addr2, cityd, stated, zipd, phon1d, phon2d, faxd, emaild, sited, logod, storenumd,)
        r = SQConnect(q, d, sqlfile).ONE()
        

    
class StartPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        lookupSizer = wx.BoxSizer(wx.VERTICAL)
        IconBar_list =[('Exit', self.OnExitButton)]
        iconbar = IconPanel(self, iconList=IconBar_list)
        IconBox = wx.StaticBox(self, label='')
        IconBarSizer = wx.StaticBoxSizer(IconBox, wx.HORIZONTAL)        
        xx = 0        
        IconBarSizer.Add(iconbar, 0, wx.ALL, 3)
        level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        windowstyle = fnb.FNB_NO_X_BUTTON|fnb.FNB_NO_NAV_BUTTONS|fnb.FNB_NODRAG|fnb.FNB_FF2
                
        #notebook = fnb.FlatNotebook(self, wx.ID_ANY, name='Main_Notebook', agwStyle=windowstyle)
        self.nb = wx.Notebook(self, wx.ID_ANY, name='Main_Notebook')
        self.nb.AddPage(GeneralInfoTab(self.nb), "General Info")
        #self.nb.AddPage(GeneralDetailsTab(self.nb), 'General Details Tab')
        self.nb.AddPage(InventoryMaintenanceTab(self.nb), "Inventory Maintenance")
        self.nb.AddPage(CustomerMaintenanceTab(self.nb), "Customer Maintenance")
        self.nb.AddPage(POSTab(self.nb), "POS")
        self.nb.AddPage(TaxInfoTab(self.nb), "Tax Info")
        self.nb.AddPage(EmployeesTab(self.nb), "Employees")
        self.nb.AddPage(PasswordsTab(self.nb), "Passwords")
        self.nb.AddPage(ReceiptTab(self.nb), "Receipts")
        self.nb.AddPage(HardwareTab(self.nb), "Hardware")
        self.nb.AddPage(ThemesTab(self.nb), "Themes")

        level1Sizer.Add(self.nb, 1, wx.EXPAND, 5)
        lookupSizer.Add(IconBarSizer, 0, wx.ALL|wx.EXPAND, 5)
        lookupSizer.Add(level1Sizer, 0, wx.ALL|wx.EXPAND, 5)
        
        self.SetSizer(lookupSizer, 0)
        
        self.Layout()


    def OnExitButton(self, evt):
        """On Exit Button """

        item = wx.FindWindowByName('Maintenance_Frame')
        item.Close()
        item.Destroy()
        

class MaintenanceScreen(wx.Frame):
    def __init__(self):
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX) & (~wx.MINIMIZE_BOX)
        wx.Frame.__init__(self, None, wx.ID_ANY, title="RHP Maintenance", size=(1200, 800), style=style)
        self.panel_one = StartPanel(self, size=(1200,800))
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel_one, 0, wx.ALL|wx.EXPAND, 5)
        self.SetSizerAndFit(self.sizer, 0)
        self.Layout()
       
  
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    
    frame = MaintenanceScreen()
    frame.Centre()
    frame.SetName('Maintenance_Frame')
    frame.Show()
    app.MainLoop()        
