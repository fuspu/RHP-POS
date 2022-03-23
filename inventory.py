import wx
import wx.grid as gridlib
import sys,re
import faulthandler
import json
import time
import numpy
import xml.etree.cElementTree as ET
from wx.lib.masked import NumCtrl, Ctrl, TextCtrl
from controls import RH_TextCtrl, RH_CheckBox, RH_ComboBox, RH_OLV, RH_Button, RH_ListBox, GridOps, Themes, tSizer
import datetime
import pout
from utils import IconPanel, EventOps
from decimal import Decimal, ROUND_HALF_UP
from db_ops import SQConnect
#, LookupDB
#from var_operations import VarOps, LoadSaveList




class MainOptionsTab(wx.Panel):
    def __init__(self, *args, **kwargs):
        """"""
        wx.Panel.__init__(self, *args, **kwargs)
        self.sql_file = './db/INVENTORY.sql'
        self.SetName('MainOptionsTab')
        firstSizer = wx.BoxSizer(wx.VERTICAL)
        secondlevelSizer = wx.BoxSizer(wx.HORIZONTAL)

        # combochoice_list = [('Department', 'genOptions_department_combobox', 'department'),
        #                     ('Category', 'genOptions_category_combobox', 'category'),
        #                     ('Sub-Category', 'genOptions_subcategory_combobox', 'subcategory'),                            
        #                     ('Material', 'genOptions_location_combobox','location'),
        #                     ('Unit Type', 'genOptions_unittype_combobox','unit_type'),
        #                     ('G/L Post', 'genOptions_glpost_txtctrl', 'postacct')]

        choiced = ['                             ']
        self.deptcombo = RH_ComboBox(self, choices=choiced, style=wx.CB_SORT)
        self.deptcombo.tableName = 'item_options'
        self.deptcombo.fieldName = 'department'
        self.deptcombo.sqlfile = 'INVENTORY.sql'
        self.deptcombo.defTable = 'organizations'
        self.deptcombo.defField = 'department'
        tS = tSizer(self, text="Department", ctrl=self.deptcombo)
        secondlevelSizer.Add(tS, 0, wx.ALL|wx.EXPAND, 3)

        self.catcombo = RH_ComboBox(self, choices=choiced, style=wx.CB_SORT)
        self.catcombo.tableName = 'item_options'
        self.catcombo.fieldName = 'category'
        self.catcombo.defTable = 'organizations'
        self.catcombo.defField = 'category'
        self.catcombo.sqlfile = 'INVENTORY.sql'
        tS = tSizer(self, text="Category", ctrl=self.catcombo)
        secondlevelSizer.Add(tS, 0, wx.ALL|wx.EXPAND, 3)

        self.subcatcombo = RH_ComboBox(self, choices=choiced, style=wx.CB_SORT)
        self.subcatcombo.tableName = 'item_options'
        self.subcatcombo.fieldName = 'subcategory'
        self.subcatcombo.defTable = 'organizations'
        self.subcatcombo.defField = 'subcategory'
        tS = tSizer(self, text="SubCategory", ctrl=self.subcatcombo)
        secondlevelSizer.Add(tS, 0, wx.ALL|wx.EXPAND, 3)

        self.matcombo = RH_ComboBox(self, choices=choiced, style=wx.CB_SORT)
        self.matcombo.tableName = 'item_options'
        self.matcombo.fieldName = 'material'
        self.matcombo.defTable = 'organizations'
        self.matcombo.defField = 'material'
        tS = tSizer(self, text="Material", ctrl=self.matcombo)
        secondlevelSizer.Add(tS, 0, wx.ALL|wx.EXPAND, 3)


        self.unitcombo = RH_ComboBox(self, choices=choiced, style=wx.CB_SORT)
        self.unitcombo.tableName = 'item_options'
        self.unitcombo.fieldName = 'unit_type'
        self.unitcombo.defTable = 'organizations'
        self.unitcombo.defField = 'unit_type'
        tS = tSizer(self, text="Unit Type", ctrl=self.unitcombo)
        secondlevelSizer.Add(tS, 0, wx.ALL|wx.EXPAND, 3)


           
        #secondlevelSizer.Add(self.deptcombo, 0, wx.ALL|wx.EXPAND, 3)
        # secondlevelSizer.Add(self.catcombo, 0, wx.ALL|wx.EXPAND, 3)
        # secondlevelSizer.Add(self.subcatcombo, 0, wx.ALL|wx.EXPAND, 3)
        # secondlevelSizer.Add(self.matcombo, 0, wx.ALL|wx.EXPAND, 3)
        # secondlevelSizer.Add(self.unitcombo, 0, wx.ALL|wx.EXPAND, 3)



        thirdlevelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.age_c = Ctrl(self, -1, autoformat='AGE', name="genOptions_agepopup_numctrl")
        self.age_c.tableName = 'item_options'
        self.age_c.fieldName = 'agepopup'
        self.age_c.sqlfile = 'INVENTORY.sql'
        tS = tSizer(self, text="Age", ctrl=self.age_c)
        thirdlevelSizer.Add(tS, 0, wx.ALL|wx.EXPAND, 3)

        fourthlevelSizer = wx.BoxSizer(wx.HORIZONTAL)
        fifthlevelSizer = wx.BoxSizer(wx.HORIZONTAL)
        txt = wx.StaticText(self, -1, label="Units\nin Package")
        self.units_in_pkg_c = NumCtrl(self, -1, 
                             value=1, 
                             name='genOptions_units_in_package_numctrl',
                             min=1,
                             selectOnEntry=True, 
                             style=0, 
                             integerWidth=6,
                             fractionWidth=0)
        self.units_in_pkg_c.tableName = 'item_options'
        self.units_in_pkg_c.fieldName = 'unitsinpackage'       
        self.units_in_pkg_c.Bind(wx.EVT_KILL_FOCUS, self.NeverZero)
        
        fifthlevelSizer.Add(self.units_in_pkg_c, 0, wx.ALL|wx.EXPAND, 5)
        fifthlevelSizer.Add(txt, 0, wx.ALL|wx.EXPAND, 5)

        # flc_list = [('Food Stamp Exempt','genOptions_foodStampExempt_checkbox','foodstampexempt'),
        #             ('Loyalty Exempt','genOptions_loyaltyExempt_checkbox','loyaltyexempt'),
        #             ('Consignment','genOptions_consignment_checkbox','consignment'),
        #             ('Closeout','genOptions_closeout_checkbox','closeout')]
        
        self.foodstampcb = RH_CheckBox(self, label='Food Stamp Exempt')
        self.foodstampcb.tableName = 'item_options'
        self.foodstampcb.fieldName = 'foodstampexempt'
        self.foodstampcb.sqlfile = 'INVENTORY.sql'
        fifthlevelSizer.Add(self.foodstampcb, 0, wx.ALL ,5)
        
        self.loyaltycb = RH_CheckBox(self, label='Loyalty Exempt')
        self.loyaltycb.tableName = 'item_options'
        self.loyaltycb.fieldName = 'loyaltyexempt'
        self.loyaltycb.sqlfile = 'INVENTORY.sql'
        fifthlevelSizer.Add(self.loyaltycb, 0, wx.ALL, 5)
        
        self.consigncb = RH_CheckBox(self, label='Consignment')
        self.consigncb.tableName = 'item_options'
        self.consigncb.fieldName = 'consignment'
        self.consigncb.sqlfile = 'INVENTORY.sql'
        fifthlevelSizer.Add(self.consigncb, 0, wx.ALL, 5)
        
        self.closeoutcb = RH_CheckBox(self, label='Closeout')
        self.closeoutcb.tableName = 'item_options'
        self.closeoutcb.fieldName = 'closeout'
        self.closeoutcb.sqlfile = 'INVENTORY.sql'
        fifthlevelSizer.Add(self.closeoutcb, 0, wx.ALL, 5)

        sixthlevelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.partnumtc = RH_TextCtrl(self, size=(140, -1))
        self.partnumtc.tableName = 'item_detailed'
        self.partnumtc.fieldName = 'part_num'
        self.partnumtc.sqlfile = 'INVENTORY.sql'
        tS = tSizer(self, text="Part #", ctrl=self.partnumtc)
        sixthlevelSizer.Add(tS, 0, wx.ALL, 5)

        self.oemnumtc = RH_TextCtrl(self, size=(140, -1))
        self.oemnumtc.tableName = 'item_detailed'        
        self.oemnumtc.fieldName = 'oempart_num'
        self.oemnumtc.sqlfile = 'INVENTORY.sql'
        tS = tSizer(self, text="OEM #", ctrl=self.oemnumtc)
        sixthlevelSizer.Add(tS, 0, wx.ALL, 5)
        
        self.zonenumtc = RH_TextCtrl(self, size=(140, -1))
        self.zonenumtc.tableName = 'item_options'
        self.zonenumtc.fieldName = 'location'
        self.zonenumtc.sqlfile = 'INVENTORY.sql'
        tS = tSizer(self, text="Zone", ctrl=self.zonenumtc)
        sixthlevelSizer.Add(tS, 0, wx.ALL, 5)

        lvl6b_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.kitnumtc = RH_TextCtrl(self, size=(140, -1))
        self.kitnumtc.tableName = 'item_detailed'
        self.kitnumtc.fieldName = 'kit_num'
        self.kitnumtc.sqlfile = 'INVENTORY.sql'
        tS = tSizer(self, text="Kit #", ctrl=self.kitnumtc)
        lvl6b_Sizer.Add(tS, 0, wx.ALL, 5)
        
        self.piecestc = RH_TextCtrl(self, size=(140, -1))
        self.piecestc.tableName = 'item_detailed'
        self.piecestc.fieldName = 'kit_pieces'
        self.piecestc.sqlfile = 'INVENTORY.sql'
        tS = tSizer(self, text="Kit Pieces", ctrl=self.piecestc)
        lvl6b_Sizer.Add(tS, 0, wx.ALL, 5)

        seventhlevelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.deactivatedcb = RH_CheckBox(self, label="Deactivated")
        self.deactivatedcb.SetForegroundColour('Red')
        self.deactivatedcb.tableName = 'item_options'
        self.deactivatedcb.fieldName = 'deactivated'
        self.deactivatedcb.sqlfile = 'INVENTORY.sql'
        seventhlevelSizer.Add(self.deactivatedcb, 0, wx.ALL, 5)

        numberofitemstxt = wx.StaticText(self, -1, 
                                         label="Number Here",
                                         name='genOptions_numberofitems_text')

        returnd = self.GetInvCount()
        numofItems = "{:,}".format(returnd[0])
        inventoryCount = "Number of Items : {}\t".format(str(numofItems))
        numberofitemstxt.SetLabel(inventoryCount)

        seventhlevelSizer.AddStretchSpacer( prop=3)
        seventhlevelSizer.Add(numberofitemstxt, 0, wx.ALL|wx.EXPAND, 15)


        firstSizer.Add(secondlevelSizer, 0, wx.ALL|wx.EXPAND, 5)
        firstSizer.Add(thirdlevelSizer, 0, wx.ALL|wx.EXPAND, 5)
        firstSizer.Add(fourthlevelSizer, 0, wx.ALL|wx.EXPAND, 5)
        firstSizer.Add(fifthlevelSizer, 0, wx.ALL|wx.EXPAND, 5)
        firstSizer.Add(sixthlevelSizer, 0, wx.ALL|wx.EXPAND, 5)
        firstSizer.Add(lvl6b_Sizer, 0, wx.ALL|wx.EXPAND, 5)
        firstSizer.AddStretchSpacer(prop=1)
        firstSizer.Add(seventhlevelSizer, 1, wx.ALL|wx.EXPAND, 10)


        self.SetSizer(firstSizer)
        firstSizer.Fit(self)
       # self.Layout()

        wx.CallAfter(self.LoadDefaults, event='')

    def NeverZero(self, event):
            """ Field can never be set to zero """
            valued = event.GetEventObject()
            raw_value = valued.GetValue()
            named = valued.GetName()
            edit_ctrl = wx.FindWindowByName(named)
            if raw_value == 0:
                new_value = 1
            else:
                new_value = raw_value

            if re.search('(txtctrl|numctrl)', named, re.I):
                edit_ctrl.SetValue(new_value)
    
    def GetInvCount(self):
        q = 'SELECT COUNT(*) FROM item_detailed'
        d = ()
        r = SQConnect(q, d, self.sql_file).ONE()
        return r

    def onAisleNum(self, event):
        obj = event.GetEventObject()
        name = obj.GetName()
        value = wx.FindWindowByName(name).GetValue()
        
        sectionNums = wx.FindWindowByName('genOptions_sectionNums_combobox')
        locations = wx.FindWindowByName('genOptions_extraPlaces_combobox')
        if value != '0':
            sectionNums.Enable()
            locations.Disable()
            locations.SetValue('')

        else:
            locations.Enable()
            sectionNums.Disable()
            sectionNums.SetValue('')

   
    def LoadDefaults(self, event):
        DeptCat_list = [('department', self.deptcombo),
                        ('category', self.catcombo),
                        ('subcategory', self.subcatcombo),
                        ('location', self.matcombo),
                        ('unittype', self.unitcombo)]

        #for field, item in DeptCat_list:
        
       #     item.LoadDefaults('organizations', field, 'abuser', 'rhp')
            

    def OnSave(self):
        upc = wx.FindWindowByName('inventory_itemNumber_txtctrl').GetCtrl()
        genOpts_list = ['genOptions_department_combobox',
                        'genOptions_category_combobox',
                        'genOptions_subcategory_combobox',
                        'genOptions_location_combobox',
                        'genOptions_glpost_txtctrl',
                        'genOptions_unittype_combobox',
                        'genOptions_itemType_radiobox',
                        'genOptions_agepopup_numctrl',
                        'genOptions_POSoptions_radiobox',
                        'genOptions_units_in_package_numctrl',
                        'genOptions_foodStampExempt_checkbox',
                        'genOptions_loyaltyExempt_checkbox',
                        'genOptions_consignment_checkbox',
                        'genOptions_partNumber_txtctrl',
                        'genOptions_oemNumber_txtctrl',
                        'genOptions_deactivated_checkbox']

        for name, table, field in genOpts_list:
            item = wx.Window.FindWindowByName(name)
            item.OnSave('upc', upc)

    
    def Clear(self):
        genOptions_default_list = ['genOptions_department_combobox',
                                   'genOptions_category_combobox',
                                   'genOptions_subcategory_combobox',
                                   'genOptions_location_combobox',
                                   'genOptions_glpost_txtctrl',
                                   'genOptions_unittype_combobox',
                                   'genOptions_itemType_radiobox',
                                   'genOptions_agepopup_numctrl',
                                   'genOptions_POSoptions_radiobox',
                                   'genOptions_units_in_package_numctrl',
                                   'genOptions_foodStampExempt_checkbox',
                                   'genOptions_loyaltyExempt_checkbox',
                                   'genOptions_consignment_checkbox',
                                   'genOptions_partNumber_txtctrl',
                                   'genOptions_oemNumber_txtctrl',
                                   'genOptions_deactivated_checkbox']

        for name in genOptions_default_list:
            item = wx.FindWindowByName(name)
            item.Clear()
                


class DetailsTab(wx.Panel):
    def __init__(self, *args, **kwargs):
        """"""
        wx.Panel.__init__(self, *args, **kwargs)
        



class StartPanel(wx.Panel):
    """"""
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.SetName('StartPanel')
        lookupSizer = wx.BoxSizer(wx.VERTICAL)
        
        IconBar_list =[('Save', self.OnSave),
                       ('Undo', self.OnUndo),
                       ('Find', self.OnFind),
                       ('Add', self.OnAdd),
                       ('Delete', self.OnMinus),
                       ('Receiving', self.OnReceive),
                       ('Exit', self.OnExitButton)]

        iconbar = IconPanel(self, iconList=IconBar_list)
        
        lookupSizer.Add(iconbar, 0, wx.EXPAND)
        level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        name = 'inventory_itemNumber_txtctrl'
        self.itemctrl = wx.TextCtrl(self, -1, size=(250,-1), name=name, style=wx.TE_PROCESS_ENTER|wx.TE_PROCESS_TAB)
        self.itemctrl.SetFocus()
        self.itemctrl.SelectAll()
        self.itemctrl.SetHint('Item Number')
        self.itemctrl.SetToolTip(wx.ToolTip('Enter Item Number Here & press Enter'))
        self.itemctrl.Bind(wx.EVT_KEY_DOWN, self.onCatchKey)
        self.itemctrl.fieldName = 'upc'
        self.itemctrl.tableName = 'item_detailed'
        level1Sizer.Add(self.itemctrl, 0, wx.ALL, 3)

        name = 'inventory_General_itemDescription_txtctrl'
        self.desctrl = wx.TextCtrl(self, -1, size=(350,-1), name=name, style=wx.TE_PROCESS_TAB)
        self.desctrl.SetHint('General Item Description')
        self.desctrl.SetToolTip(wx.ToolTip('Enter General Item Description Here'))
        self.desctrl.Bind(wx.EVT_KILL_FOCUS, EventOps().CheckMeasurements)
        self.desctrl.fieldName = 'general_description'
        self.desctrl.tableName = 'item_detailed'
        level1Sizer.Add(self.desctrl, 0, wx.ALL, 3)

        name = 'inventory_Specific_itemDescription_txtctrl'
        self.desctrl = wx.TextCtrl(self, -1, size=(350,-1), name=name, style=wx.TE_PROCESS_TAB)
        self.desctrl.SetHint('Specific Item Description')
        self.desctrl.SetToolTip(wx.ToolTip('Enter Specific Item Description Here'))
        self.desctrl.Bind(wx.EVT_KILL_FOCUS, EventOps().CheckMeasurements)
        self.desctrl.fieldName = 'specifc_description'
        self.desctrl.tableName = 'item_detailed'
        level1Sizer.Add(self.desctrl, 0, wx.ALL, 3)


        # countreturn = HUD.QueryOps().QueryCheck('item_detailed')
        # pout.v(countreturn)
        # if countreturn > 0:
        #     returnd = LookupDB('item_detailed').General('upc',limit=1)
        #     pout.v(str(type(returnd)),returnd)
        #     itemNumber = wx.FindWindowByName('inventory_itemNumber_txtctrl')
        #     itemNumber.SetCtrl(returnd)

#            wx.CallAfter(self.OnItemNumber, event=None, upc=itemNumber.GetValue().strip())

        lookupSizer.Add(level1Sizer, 0)

        level2Sizer = wx.BoxSizer(wx.HORIZONTAL)

        notebook = wx.Notebook(self, -1, name='inventory_main_notebook')
        tabOne = MainOptionsTab(notebook)
        notebook.AddPage(tabOne, "General Options",)
        tabTwo = DetailsTab(notebook)

        notebook.AddPage(tabTwo, "Details")

        notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)

        level2Sizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)


        lookupSizer.Add(level2Sizer, 0, wx.ALL|wx.EXPAND, 5)

        self.SetSizer(lookupSizer)
        self.Layout()

    def OnSave(self, evt):
        pass

    def OnUndo(self, evt):
        pass

    def OnFind(self, evt):
        pass

    def OnAdd(self, evt):
        pass
    
    def OnMinus(self, evt):
        pass

    def OnReceive(self, evt):
        pass

    def OnExitButton(self, evt):
        pass

    def onCatchKey(self, evt):
        pass

    def OnPageChanged(self, evt):
        pass



class InventoryScreen(wx.Frame):
    def __init__(self, *args, **kwargs):
        kwargs['style'] = wx.DEFAULT_FRAME_STYLE & (~wx.CLOSE_BOX | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX)
        kwargs['title'] = "RHP Inventory Management"
        kwargs['size'] = (1200, 800)
        wx.Frame.__init__(self, None, *args, **kwargs)
        
        self.panel_one = StartPanel(self)



        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel_one, 1, wx.EXPAND)

        self.SetSizer(self.sizer)



        self.Layout()



# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = InventoryScreen()
    frame.Centre()
    frame.SetName('Inventory_Frame')
    frame.Show()
    app.MainLoop()
