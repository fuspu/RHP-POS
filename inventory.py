# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Inventory
#

import wx
import wx.grid as gridlib
import sys,re
import faulthandler
import json
import time
import numpy
import xml.etree.cElementTree as ET
import wx.lib.masked as masked
import datetime
import pout
import handy_utils as HUD
from button_stuff import ButtonOps
from decimal import Decimal, ROUND_HALF_UP
from db_related import SQConnect, LookupDB
from var_operations import VarOps, LoadSaveList

global debug
debug = False


class MainOptionsTab(wx.Panel):
    def __init__(self, *args, **kwargs):
        """"""
        wx.Panel.__init__(self, *args, **kwargs)
        
        self.SetName('MainOptionsTab')

        firstSizer = wx.BoxSizer(wx.VERTICAL)
        secondlevelSizer = wx.BoxSizer(wx.HORIZONTAL)

        combochoice_list = [('Department', 'genOptions_department_combobox', 'department'),
                            ('Category', 'genOptions_category_combobox', 'category'),
                            ('Sub-Category', 'genOptions_subcategory_combobox', 'subcategory'),                            
                            ('Material', 'genOptions_location_combobox','location'),
                            ('Unit Type', 'genOptions_unittype_combobox','unit_type'),
                            ('G/L Post', 'genOptions_glpost_txtctrl', 'postacct')]

        for label, name, field in combochoice_list:
            box = wx.StaticBox(self, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            if 'combobox' in name:
                ctrl =  HUD.RH_ComboBox(self, 
                                            name=name, 
                                            choices=['                          ',], 
                                            style=wx.CB_SORT)
                
            if 'txtctrl' in name:
                ctrl = HUD.RH_MTextCtrl(self, -1, 
                                       size=(65, -1), 
                                       mask='###-###', 
                                       name=name)
            
            ctrl.tableName = 'item_options'
            ctrl.fieldName = field
               
            boxSizer.Add(ctrl, 0, wx.ALL,3)
            secondlevelSizer.Add(boxSizer, 0, wx.ALL|wx.EXPAND, 3)



        thirdlevelSizer = wx.BoxSizer(wx.HORIZONTAL)
        ItemTypeChoices = ['Controlled', 'Non-Controlled', 'Matrixed', 'BOM', 
                           'Tag Along', 'Serial No. Track', 'Mfg Coupon']
        
        ctrl = HUD.RH_RadioBox(self, 
                               choices=ItemTypeChoices,
                               label='Item Type', 
                               name="genOptions_itemType_radiobox", 
                               style=wx.RA_SPECIFY_COLS)

        for i in range(2,7):
            ctrl.EnableItem(i,enable=False)
        ctrl.tableName = 'item_options'
        ctrl.fieldName = 'item_type'
        thirdlevelSizer.Add(ctrl, 0, wx.ALL|wx.EXPAND, 3)

        box = wx.StaticBox(self, label="Age")
        sizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        ctrl = HUD.RH_NumCtrl(self, -1, 
                              value=0,  
                              name="genOptions_agepopup_numctrl", 
                              integerWidth=2, 
                              fractionWidth=0)
        ctrl.tableName = 'item_options'
        ctrl.fieldName = 'agepopup'

        sizer.Add(ctrl, 0, wx.ALL|wx.EXPAND, 3)
        thirdlevelSizer.Add(sizer, 0, wx.ALL|wx.EXPAND, 3)

        fourthlevelSizer = wx.BoxSizer(wx.HORIZONTAL)
        POSOptionsChoices = ['Prompt for Quantity', 'Assume 1 Sold', 
                             'Prompt for Price - Quantity Calculated']
        
        ctrl = HUD.RH_RadioBox(self, -1, 
                               choices=POSOptionsChoices, 
                               label='POS Options', 
                               name="genOptions_POSoptions_radiobox", 
                               style=wx.RA_SPECIFY_COLS)
        ctrl.tableName = 'item_options'
        ctrl.fieldName = 'pos_options'
        fourthlevelSizer.Add(ctrl, 0, wx.ALL|wx.EXPAND, 3)

        fifthlevelSizer = wx.BoxSizer(wx.HORIZONTAL)
        txt = wx.StaticText(self, -1, label="Units\nin Package")
        ctrl = HUD.RH_NumCtrl(self, -1, 
                              value=1, 
                              name='genOptions_units_in_package_numctrl',
                              min=1,
                              selectOnEntry=True, 
                              style=0, 
                              integerWidth=6,
                              fractionWidth=0)
        ctrl.tableName = 'item_options'
        ctrl.fieldName = 'unitsinpackage'       
        ctrl.Bind(wx.EVT_KILL_FOCUS, self.NeverZero)
        
        fifthlevelSizer.Add(ctrl, 0, wx.ALL|wx.EXPAND, 5)
        fifthlevelSizer.Add(txt, 0, wx.ALL|wx.EXPAND, 5)

        flc_list = [('Food Stamp Exempt','genOptions_foodStampExempt_checkbox','foodstampexempt'),
                    ('Loyalty Exempt','genOptions_loyaltyExempt_checkbox','loyaltyexempt'),
                    ('Consignment','genOptions_consignment_checkbox','consignment'),
                    ('Closeout','genOptions_closeout_checkbox','closeout')]
        
        for label, name, field in flc_list:
            cb = HUD.RH_CheckBox(self, label=label, name=name)
            cb.tableName = 'item_options'
            cb.fieldName = field
            fifthlevelSizer.Add(cb, 0, wx.ALL|wx.EXPAND, 5)
            if 'foodstampexempt' in name:
                cb.SetValue(True)
        
        sixthlevelSizer = wx.BoxSizer(wx.HORIZONTAL)

        lvl6_list = [('Part Number','genOptions_partNumber_txtctrl', 140, 'item_detailed', 'part_num'),
                     ('OEM Part Number','genOptions_oemNumber_txtctrl', 140, 'item_detailed', 'oempart_num'),
                     ('Aisle #','genOptions_aisleNums_combobox', 50, 'item_detailed', 'aisle_num'),
                     ('4ft Section #','genOptions_sectionNums_combobox', 80,'item_options', 'section_num'),
                     ('Extra Location','genOptions_extraPlaces_combobox', 140, 'item_options', 'extra_places')]
        
        for label, name, sized, table, field in lvl6_list:
            box = wx.StaticBox(self, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            if 'txtctrl' in name:
                ctrl = HUD.RH_TextCtrl(self, -1, 
                                   size = (sized,-1), 
                                   name = name)
            if 'combobox' in name:
                ctrl = HUD.RH_ComboBox(self, -1, 
                                   choices = [], 
                                   name = name,
                                   size = (sized, -1))
                ctrl.Disable()
            if 'aisleNums' in name:
                ctrl.Bind(wx.EVT_COMBOBOX, self.onAisleNum)
                ctrl.Enable()

            ctrl.tableName = table
            ctrl.fieldName = field
            boxSizer.Add(ctrl, 0, wx.ALL|wx.EXPAND, 3)

            sixthlevelSizer.Add(boxSizer, 0, wx.ALL|wx.EXPAND, 5)

        lvl6b_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        lvl6b_list = [('Kit Number','genOptions_kitNumber_txtctrl', 'item_detailed','kit_num'),
                      ('Pieces','genOptions_kitPieces_numctrl', 'item_detailed','kit_pieces')]

        box = wx.StaticBox(self, label='Bin Kits')
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        for label, name, table, field in lvl6b_list:
            text = wx.StaticText(self, label=label)
            if 'txtctrl' in name:
                ctrl = HUD.RH_TextCtrl(self, -1, name=name)
            if 'numctrl' in name:
                ctrl = HUD.RH_NumCtrl(self, -1, 
                                      name = name, 
                                      integerWidth = 3, 
                                      fractionWidth = 0)
            
            ctrl.tableName = table
            ctrl.fieldName = field
            boxSizer.Add(text, 0, wx.ALL, 3)
            boxSizer.Add(ctrl, 0, wx.ALL, 3)

        lvl6b_Sizer.Add(boxSizer, 0)

        seventhlevelSizer = wx.BoxSizer(wx.HORIZONTAL)
        ctrl = HUD.RH_CheckBox(self, -1, 
                                         label="Deactivated",
                                         name="genOptions_deactivated_checkbox")
        ctrl.tableName = 'item_options'
        ctrl.fieldName = 'deactived'
        ctrl.SetForegroundColour('Red')
        seventhlevelSizer.Add(ctrl, 0)

        numberofitemstxt = wx.StaticText(self, -1, 
                                         label="Number Here",
                                         name='genOptions_numberofitems_text')

        returnd = HUD.QueryOps().QueryCheck('item_detailed')
               
        
        numofItems = '{:,}'.format(returnd)
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
        DeptCat_list = [('department', 'genOptions_department_combobox'),
                        ('category', 'genOptions_category_combobox'),
                        ('subcategory', 'genOptions_subcategory_combobox'),
                        ('location', 'genOptions_location_combobox'),
                        ('unittype', 'genOptions_unittype_combobox'),
                        ('extra_places', 'genOptions_extraPlaces_combobox'),
                        ('num_of_aisles', 'genOptions_aisleNums_combobox'),
                        ('num_of_sections', 'genOptions_sectionNums_combobox')]

        for field, name in DeptCat_list:
            print(f'Field : {field} ; Name : {name}')
            item = wx.Window.FindWindowByName(name)
            item.LoadDefaults('organizations', field, 'abuser', 'rhp')
            

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
            
    

        
class page_item_detail(wx.Panel):
    def __init__(self, *args, **kwargs):
        """"""
        wx.Panel.__init__(self, *args, **kwargs)
        self.SetName('PageItemDetailTab')
        

        MainSizer = wx.BoxSizer(wx.VERTICAL)

        level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        level1Col2Sizer = wx.BoxSizer(wx.VERTICAL)

#         altlookupBox = wx.StaticBox(self, label="Alt Lookup")
#         altlookupBoxSizer = wx.StaticBoxSizer(altlookupBox, wx.HORIZONTAL)
#         altlookup =  HUD.AltLookup(self)
#     

   #     altlookupBoxSizer.Add(altlookup, 0)

   #     level1Sizer.Add(altlookupBoxSizer, 0)
        level1Col3Sizer = wx.BoxSizer(wx.VERTICAL)
        level1Col3Sizer.Add((20,20),1)

        lockdisc_list = [('Do Not Discount','details_donotdiscount_checkbox','item_detailed2', 'do_not_discount')]
        
        for label,name, table, field in lockdisc_list:
            ctrl = HUD.RH_CheckBox(self, 
                                   label=label, 
                                   name=name)
            ctrl.tableName = table
            ctrl.fieldName = field
            
            level1Col3Sizer.Add(ctrl, 1)

        level1Sizer.Add(level1Col3Sizer, 1)

        box = wx.StaticBox(self, label="Tax Level Exemptions")
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)

        taxlvl_list =['1','2','3','4','never']
        for item in taxlvl_list:
            taxName = 'details_taxlvl_{}_checkbox'.format(item)
            
            ctrl = HUD.RH_CheckBox(self, label=item, name=taxName)
            ctrl.tableName = 'item_detailed2'
            if 'never' in item:
                item = '_{}'.format(item)
                
            ctrl.fieldName = 'tax{}'.format(item)

            boxSizer.Add(ctrl, 0)


        level1Col4Sizer = wx.BoxSizer(wx.VERTICAL)
        level1Col4Sizer.Add((20,20),0)
        level1Col4Sizer.Add(boxSizer, 1)
        level1Sizer.Add((20,20),0)
        level1Sizer.Add(level1Col4Sizer, 1)

        txt = wx.StaticText(self, label="Tax Override")
        ctrl = HUD.RH_NumCtrl(self, -1, 
                                    value=0, 
                                    name='details_taxoverride_numctrl', 
                                    integerWidth=4, 
                                    fractionWidth=4)
        ctrl.tableName = 'item_detailed2'
        ctrl.fieldName = 'override_tax_rate'
        level1Col4Sizer.Add(txt, 0, wx.ALIGN_CENTER)
        level1Col4Sizer.Add(ctrl, 0, wx.ALIGN_CENTER)

        level1Col5Sizer = wx.BoxSizer(wx.VERTICAL)
        SalesReviewButton = wx.Button(self, -1,
                                      label="Sales Purchase\n\nReview", 
                                      size=(140,60), 
                                      name='details_salesReview_button')
        
        level1Col5Sizer.Add((20,20),1)
        level1Col5Sizer.Add(SalesReviewButton, 0)

        level1Sizer.Add(level1Col5Sizer, 1)

        level1Col6Sizer = wx.BoxSizer(wx.VERTICAL)
        ctrl = HUD.AltLookup(self, lbsize=(150,120), lbname='details_altlookup_listbox', tableName='item_detailed', fieldName='altlookup', boxlabel='Alt Lookups')
        level1Sizer.Add(ctrl, 0)
        
        level2Sizer = wx.BoxSizer(wx.HORIZONTAL)

        costd_list = [('Average Cost','details_avgcost_numctrl', 'item_detailed','avg_cost'),
                      ('Last Cost','details_lastcost_numctrl', 'item_detailed','last_cost'),
                      ('Starting Margin','details_startingMargin_numctrl','item_margin','general_margin')]
        
        for label,name, table, field in costd_list:
            cost_text = wx.StaticText(self, -1, label=label+":")
            ctrl = HUD.RH_NumCtrl(self, -1, value=0, 
                                            name=name, 
                                            integerWidth=6, 
                                            fractionWidth=2)
            ctrl.tableName = table
            ctrl.fieldName = field
            ctrl.SetValue('0.000')

            level2Sizer.Add(cost_text, 0, wx.ALL,2)
            level2Sizer.Add(ctrl, 0, wx.ALL,2)

        level3Sizer = wx.BoxSizer(wx.HORIZONTAL)
        level3ColSub1Sizer = wx.BoxSizer(wx.VERTICAL)
        # query = "SELECT name,scheme_list,reduce_by from item_pricing_schemes"
        # returnd = HUD.SQConnect(query, '').ALL()
        returnd = LookupDB('item_pricing_schemes').General('name, scheme_list, reduce_by')
        pout.v(returnd)
        priceschema_list = returnd

        box = wx.StaticBox(self, label="Pricing\nSchemes")
        boxSizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        boxSizer.Add((20,20), 0)
        xx=0
        rb = wx.Button(self, id=wx.ID_ANY, 
                       label="RESET", 
                       name="details_pricescema_RESET_button")
        
        rb.Bind(wx.EVT_BUTTON, self.OnPriceSchemes)
        boxSizer.Add(rb, 0)
        print(f'Returnd : {returnd}')
        for i in returnd:
            print(i)
        for label, scheme_list, reduce_by in returnd:
            rb = HUD.RH_Button(self, id=wx.ID_ANY, 
                           label=label, 
                           name=scheme_list)
            
            rb.Bind(wx.EVT_BUTTON, self.OnPriceSchemes)
            boxSizer.Add(rb, 0)
            xx+=1

        level3ColSub1Sizer.Add(boxSizer, 0)

        level3Col1Sizer = wx.BoxSizer(wx.VERTICAL)
        
        
        # checking noPenny status & rounding type        
        self.noPenny, self.rndScheme = False, '3'
        
        try:
            #(self.noPenny, self.rndScheme) = LookupDB('tax_tables').Specific('TAX','tax_name','no_pennies_rounding, RNDscheme')
            returnd = LookupDB('tax_tables').Specific('TAX','tax_name','no_pennies_rounding, RNDscheme')
            pout.v(returnd)
        except:
            pout.v('Add Tax Info')
            exit()

        self.roundtype = {'1':'ROUND_DOWN','2':'ROUND_HALF_UP','3':'ROUND_UP'}
        
        if self.rndScheme == 0:
            self.rndScheme = 3
        self.rnd = str(self.rndScheme)
                
        self.retail_grid =  HUD.Retail_Grid(self, name='inv_details_cost_grid')    
        
        level3Col1Sizer.Add(self.retail_grid, 0)
        level3Sizer.Add(level3ColSub1Sizer, 0)
        level3Sizer.Add((10,10),0)
        level3Sizer.Add(level3Col1Sizer, 0)

        level3Col2Sizer = wx.BoxSizer(wx.VERTICAL)

        SalePriceOption_text = wx.StaticText(self, label="Sales Price Option\nBuy X get Y at Sale Price")
        level3Col2Sizer.Add((20,20),0)
        #level3Col2Sizer.Add(PendingPriceChanges_button, 1)
        level3Col2Sizer.Add((20,20),0)
        level3Col2Sizer.Add(SalePriceOption_text, 1)

        buyget_Sizer = wx.BoxSizer(wx.HORIZONTAL)

        buyget_list = [('Buy','details_buy_numctrl','buyX'),
                       ('Get','details_get_numctrl','getY')]
        
        for label,name, field in buyget_list:
            box = wx.StaticBox(self, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.VERTICAL)
            ctrl = HUD.RH_NumCtrl(self, -1, 
                                  value=0, 
                                  name=name, 
                                  integerWidth=3, 
                                  fractionWidth=0)
            ctrl.tableName = 'item_detailed2'
            ctrl.fieldName = field
            boxSizer.Add(ctrl, 0)

            buyget_Sizer.Add(boxSizer, 0)
            buyget_Sizer.Add((5,5), 0)


        level3Col2Sizer.Add(buyget_Sizer, 0)
        level3Sizer.Add((10,10),0)
        level3Sizer.Add(level3Col2Sizer, 0)

        level3Col3Sizer = wx.BoxSizer(wx.VERTICAL)

        order_grid =  HUD.Order_Grid(self, name='inv_details_orderctrl_grid')
        order_grid.tableName = 'item_detailed2'
        order_grid.fieldName = 'orderctrl'

        level3Col3Sizer.Add(order_grid, 0)

        level3Sizer.Add(level3Col3Sizer, 0)

        self.eidx = 0
        self.sidx = 0
        level3Col4Sizer = wx.BoxSizer(wx.VERTICAL)
        box = wx.StaticBox(self, label="Sale Info", style=wx.TE_CENTER)
        boxSizer = wx.StaticBoxSizer(box, wx.VERTICAL)


   # ---- Date Controls on Item Detail(1)
        dateCtrls_list = [('details_saleDateBegin_datectrl', 'Begin', self.OnSaleBeginDateChange, 'item_detailed2','sale_begin'),
                          ('details_saleDateEnd_datectrl','   End', self.OnSaleEndDateChange, 'item_detailed2', 'sale_end')]
        
        for dateName, label, handler, table, field in dateCtrls_list:
            saledate_Sizer = wx.BoxSizer(wx.HORIZONTAL)
            saledate_text = wx.StaticText(self, -1, label=label)
            datepicker = HUD.RH_DatePickerCtrl(self, name=dateName, 
                                           style=wx.adv.DP_ALLOWNONE)
            datepicker.tableName = table
            datepicker.fieldName = field

            datepicker.Bind(wx.adv.EVT_DATE_CHANGED, handler)
            datepicker.Bind(wx.EVT_LEFT_DCLICK, self.onDoubleClick)
            datepicker.SetValue(wx.DateTime(1,1,1969))

            saledate_Sizer.Add(saledate_text, 0)
            saledate_Sizer.Add((10,10),0)
            saledate_Sizer.Add(datepicker, 0)

            boxSizer.Add(saledate_Sizer, 0,wx.ALL,3)

        level3Col4Sizer.Add(boxSizer, 0)

        level3Sizer.Add((30,30),0)

  # ---- Time Controls on Item Detail(1)
        timectrls_list = [('details_saleTimeBegin_timectrl', 'Daily From: ', '12:00am',self.OnSaleBeginTimeChange, 'item_detailed2','sale_begin_time'),
                          ('details_saleTimeEnd_timectrl', 'Daily To:     ','11:59pm',self.OnSaleEndTimeChange, 'item_detailed2','sale_end_time')]

        for timeName, time_text, timectrl_value, handler, table, field in timectrls_list:
            saletime_Sizer = wx.BoxSizer(wx.HORIZONTAL)
            
            timeCtrl_text = wx.StaticText(self, -1, label=time_text)
            timeCtrl = HUD.RH_TimeCtrl(self,-1, 
                                       display_seconds=False, 
                                       fmt24hr=False,
                                       useFixedWidthFont=True,
                                       value=timectrl_value, 
                                       pos=(250,70), 
                                       name=timeName)
            timeCtrl.tableName = table
            timeCtrl.fieldName = field
            timeCtrl.Bind(wx.lib.masked.timectrl.EVT_TIMEUPDATE, handler)

            saletime_Sizer.Add(timeCtrl_text, 0,wx.ALL,3)
            saletime_Sizer.Add(timeCtrl, 0,wx.ALL,3)

            boxSizer.Add(saletime_Sizer, 0)

        level3Sizer.Add(level3Col4Sizer, 0)

        MainSizer.Add(level1Sizer, 0)
        MainSizer.Add((5,5),0)
        MainSizer.Add(level2Sizer, 0)
        MainSizer.Add((5,5),0)
        MainSizer.Add(level3Sizer, 0)
        self.SetSizer(MainSizer)



    def OnLoad(self):
        upc = wx.FindWindowByName('inventory_itemNumber_txtctrl').GetCtrl()
        details_default_list = ['details_altlookup_listbox',
                                'details_altlookup_listbox_txtctrl',
                                'details_donotdiscount_checkbox',
                                'details_taxlvl_1_checkbox',
                                'details_taxlvl_2_checkbox',
                                'details_taxlvl_3_checkbox',
                                'details_taxlvl_4_checkbox',
                                'details_taxlvl_never_checkbox',
                                'details_taxoverride_numctrl',
                                'details_avgcost_numctrl',
                                'details_lastcost_numctrl',
                                'details_startingMargin_numctrl',
                                'details_buy_numctrl',
                                'details_get_numctrl',
                                'inv_details_orderctrl_grid',
                                'details_saleDateBegin_datectrl',
                                'details_saleDateEnd_datectrl',
                                'details_saleTimeBegin_timectrl',
                                'details_saleTimeEnd_timectrl']
        for name in details_default_list:
            item = wx.FindWindowByName(name)
            item.OnLoad('upc', upc)
        
    def OnSave(self):
        upc = wx.FindWindowByName('inventory_itemNumber_txtctrl').GetCtrl()
        details_default_list = ['details_altlookup_listbox',
                                'details_altlookup_listbox_txtctrl',
                                'details_donotdiscount_checkbox',
                                'details_taxlvl_1_checkbox',
                                'details_taxlvl_2_checkbox',
                                'details_taxlvl_3_checkbox',
                                'details_taxlvl_4_checkbox',
                                'details_taxlvl_never_checkbox',
                                'details_taxoverride_numctrl',
                                'details_avgcost_numctrl',
                                'details_lastcost_numctrl',
                                'details_startingMargin_numctrl',
                                'details_buy_numctrl',
                                'details_get_numctrl',
                                'inv_details_orderctrl_grid',
                                'details_saleDateBegin_datectrl',
                                'details_saleDateEnd_datectrl',
                                'details_saleTimeBegin_timectrl',
                                'details_saleTimeEnd_timectrl']
        for name in details_default_list:
            item = wx.FindWindowByName(name)
            item.OnSave('upc', upc)

    def Clear(self):
        details_default_list = ['details_altlookup_listbox',
                                'details_altlookup_listbox_txtctrl',
                                'details_donotdiscount_checkbox',
                                'details_taxlvl_1_checkbox',
                                'details_taxlvl_2_checkbox',
                                'details_taxlvl_3_checkbox',
                                'details_taxlvl_4_checkbox',
                                'details_taxlvl_never_checkbox',
                                'details_taxoverride_numctrl',
                                'details_avgcost_numctrl',
                                'details_lastcost_numctrl',
                                'details_startingMargin_numctrl',
                                'details_buy_numctrl',
                                'details_get_numctrl',
                                'inv_details_orderctrl_grid',
                                'details_saleDateBegin_datectrl',
                                'details_saleDateEnd_datectrl',
                                'details_saleTimeBegin_timectrl',
                                'details_saleTimeEnd_timectrl']
        
        for name in details_default_list:
            item = wx.FindWindowByName(name)
            item.Clear()
  
 
    def onDoubleClick(self, event):
        obj = event.GetEventObject()
        name = obj.GetName()
        today = datetime.date.today()
        wx.FindWindowByName(name).SetCtrl(today)


    def OnCellChange(self,event):
        debug = False
        
        obj = event.GetEventObject()
        named = obj.GetName()
        row = event.GetRow()
        col = event.GetCol()

        grid = wx.FindWindowByName(named)
        colname = grid.GetColLabelValue(col)
        grid.Refresh()
        
        if 'inv_details_cost_grid' in named:
            raw_value = grid.GetCellValue(row,col).strip()
            # numeric check
            if all(x in '0123456789.+-' for x in raw_value):
                # convert to float and limit to 2 decimals
                valued = Decimal(raw_value)
                if colname == 'Unit':
                    if valued == '0':
                        valued = '1'
                    valued = RO.DoRound(valued, '1')
                    
                else:
                    valued = RO.DoRound(valued, '1.00')
                
                grid.SetCellValue(row,col,str(valued))
            else:
                basic_list = ['1','$0.00','Margin','0.0000']
                grid.SetCellValue(row,col,basic_list[col])
                HUD.GridOps(grid.GetName()).GridFocusNGo(row, col)
                return

        #

        avgcost = wx.FindWindowByName('details_avgcost_numctrl').GetCtrl()
        
        #if avgcost:

        for yy in range(grid.GetNumberCols()):
            header = grid.GetColLabelValue(yy)
            if 'Unit' in header:
                unit = grid.GetCellValue(row,yy)
            if 'Margin %' in header:
                calcMargin = grid.GetCellValue(row,yy)
            if 'Price' in header:
                retail_from = grid.GetCellValue(row,yy)

        if colname == 'Margin %':
            if Decimal(calcMargin) == 0:
                newretail_almost = avgcost
                newretail = RO.DoRound(newretail_almost, '1.00')
                newMargin = '0.000'

            else:
                newretail_almost = RO.DoMargin(avgcost,calcMargin,unit)
                newretail = RO.DoRound(newretail_almost,'1.00')
                newMargin = RO.DoRound(calcMargin,'1.000')
            set_values = [('Price',newretail), ('Margin %',newMargin)]

            fillgrid = HUD.GridOps(grid.GetName()).FillGrid(set_values,row=row)

        if colname == 'Price':
            grossMargin = RO.GetMargin(avgcost,retail_from,unit)
            Margindot4 = RO.DoRound(grossMargin,'1.000')
            
            grid.SetCellValue(row,3,str(Margindot4))

        if colname == 'Unit':
            

            newretail_almost = RO.DoMargin(avgcost,calcMargin,unit)
            newretail = RO.DoRound(newretail_almost, '1.00')

            grid.SetCellValue(row,1,str(newretail))


    def OnSaleBeginTimeChange(self, event):
        debug = False
        onSaleTimeBegin = event.GetEventObject().GetValue()
        

    def OnSaleEndTimeChange(self, event):
        debug = False
        onSaleTimeEnd = event.GetEventObject().GetValue()
        

    def OnSaleBeginDateChange(self, event):
        debug = False
        fdateCtrl = event.GetEventObject()
        onSaleDateBegin = fdateCtrl.GetValue().FormatISODate()
        

    def OnSaleEndDateChange(self, event):
        debug = False
        fdateCtrl = event.GetEventObject()
        onSaleDateEnd = fdateCtrl.GetValue().FormatISODate()
        

    def OnCompareButtonAltLookup(self, event):
        debug = False
        
        pass

    def OnPriceSchemes(self, event):
        debug = False
        grid = wx.FindWindowByName('inv_details_cost_grid')
        WhichScheme = event.GetEventObject()
        

        Scheme_Name = WhichScheme.GetLabel()
        Scheme_List = WhichScheme.GetName().split("-")
        
        if Scheme_Name == 'RESET':
            
            reset_list = [('Unit','1'),('Price','0.00'),('Margin %','0.0000')]
            for xx in range(grid.GetNumberRows()):
                fillgrid = HUD.GridOps(grid.GetName()).FillGrid(reset_list,row=xx)

        else:
            
            if 'PK' in Scheme_List:
                (each, pack, bulk) = Scheme_List
                
                UIPctrl = wx.FindWindowByName('genOptions_units_in_package_numctrl').GetCtrl()
                if not UIPctrl:
                    UIPctrl = 1
                if Decimal(UIPctrl) == Decimal(each):
                    UIPctrl = Decimal(each)*2
                Bulkd = Decimal(UIPctrl) * Decimal(bulk.strip('X'))
                
                Scheme_List = str(each),str(UIPctrl),str(Bulkd)

            currPrice = wx.FindWindowByName('inv_details_cost_grid').GetCellValue(0,1)

            avgCostL = wx.FindWindowByName('details_avgcost_numctrl').GetCtrl()
            
            # query = "SELECT reduce_by from item_pricing_schemes WHERE name=(?)"
            # data = (Scheme_Name,)
            # returnd = HUD.SQConnect(query, data).ONE()
            returnd = LookupDB('item_pricing_schemes').Specific(Scheme_Name, 'name','reduce_by')
            type(returnd)
            
            if '-' in returnd[0]:
                Reduceby = returnd[0].split('-')
            else:
                Reduceby = list(returnd)

            

            startingMargin_L = wx.FindWindowByName('details_startingMargin_numctrl').GetCtrl()
            if startingMargin_L == 0:
                startingMargin_L = HUD.RetailOps().StartingMargin('details_startingMargin_numctrl')

            

            if Decimal(avgCostL) == 0:
                wx.MessageBox('Average Cost Not Set','Info',wx.OK)
                return
            Schemed = HUD.Pricing('C',Scheme_List,Reduceby,avgCostL,startingMargin_L,currPrice)
            
            schemeLen = len(Schemed.Scheme())
            priceScheme_dict = Schemed.Scheme()

            xx = 0

            for key in Scheme_List:
                setList = [('Unit',key),('Price',str(Decimal(priceScheme_dict[key][0]))),
                           ('Margin %',str(Decimal(priceScheme_dict[key][1])))]
                fillGrid = HUD.GridOps(grid.GetName()).FillGrid(setList,row=xx)
                xx += 1


#-------------------------------------
class page_detail_pg2(wx.Panel):
    def __init__(self, *args, **kwargs):
        """"""
        wx.Panel.__init__(self, *args, **kwargs)
        self.SetName('PageDetailPage2Tab')
        self.nameList = HUD.LoadSaveList()

        MainSizer = wx.BoxSizer(wx.HORIZONTAL)

        Duo1Sizer = wx.BoxSizer(wx.VERTICAL)

        D1level1Sizer = wx.BoxSizer(wx.HORIZONTAL)

        cb_list = [('Credit Book Exempt','details2_creditbookExempt_checkbox', 'item_detailed2', 'credit_book_exempt'),
                   ('Delete when out','details2_deleteWhenOut_checkbox','item_detailed2','delete_when_out')]
        
        for label, name, table, field in cb_list:
            ctrl = HUD.RH_CheckBox(self,-1, 
                               label=label, 
                               name=name)
            ctrl.tableName = table
            ctrl.fieldName = field
            self.nameList = name    
            D1level1Sizer.Add(ctrl, 0)
            D1level1Sizer.Add((10,10), 0)

        D1level2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        QuantityData_box = wx.StaticBox(self, label="Quantities")
        QuantityDataSizer = wx.StaticBoxSizer(QuantityData_box, wx.HORIZONTAL)

        txtctrl_list = [('On Hand','details2_onHand_numctrl','item_detailed','quantity_on_hand'),
                        ('Committed','details2_committed_numctrl','item_detailed', 'quantity_committed'),
                        ('On Layaway','details2_onLayaway_numctrl','item_detailed','quantity_on_layaway')]
        
        for label, name, table, field in txtctrl_list:
            Sizer = wx.BoxSizer(wx.VERTICAL)
            text = wx.StaticText(self, label=label)
            ctrl = HUD.RH_NumCtrl(self, -1, 
                                  value=0,
                                  name=name, 
                                  integerWidth=6, 
                                  fractionWidth=3)
            ctrl.tableName = table
            ctrl.fieldName = field
            self.nameList = name

            Sizer.Add(text, 0, wx.ALL|wx.ALIGN_CENTER,2)
            Sizer.Add(ctrl, 0, wx.ALL|wx.ALIGN_CENTER,2)
            QuantityDataSizer.Add(Sizer, 0,wx.ALL, 2)
            QuantityDataSizer.Add((20,20),0)


        D1level2Sizer.Add(QuantityDataSizer, 0)

        D1level3Sizer = wx.BoxSizer(wx.HORIZONTAL)

        OperationDates_box = wx.StaticBox(self, label="Operation Dates")
        OpDateSizer = wx.StaticBoxSizer(OperationDates_box, wx.HORIZONTAL)
        opdat_list =[('Last Sale','details2_lastSale_datectrl','item_detailed2','last_saledate'),
                     ('Last Return','details2_lastReturn_datectrl','item_detailed2','last_returndate'),
                     ('Last Maint','details2_lastMaint_datectrl','item_detailed2','maintdate'),
                     ('Added','details2_added_datectrl','item_detailed2','added_date')]
        
        for label, name, table, field in opdat_list:
            OPSizer = wx.BoxSizer(wx.VERTICAL)
            OP_text = wx.StaticText(self, label=label)
            ctrl = HUD.RH_DatePickerCtrl(self, name=name, style=wx.adv.DP_ALLOWNONE)
            ctrl.tableName = table
            ctrl.fieldName = field
            self.nameList = name

            OPSizer.Add(OP_text, 0, wx.ALL|wx.ALIGN_CENTER, 2)
            OPSizer.Add(ctrl, 0, wx.ALL|wx.ALIGN_CENTER, 2)

            OpDateSizer.Add(OPSizer, 0)
            OpDateSizer.Add((20,20), 0)

        D1level3Sizer.Add(OpDateSizer, 0)

        D1level4Sizer = wx.BoxSizer(wx.HORIZONTAL)


        box = wx.StaticBox(self, label="Commission Data")
        boxSizer = wx.StaticBoxSizer(box, wx.VERTICAL)

        CD_1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        ctrl = HUD.RH_CheckBox(self, -1, 
                               label="Override other commissions with %:", 
                               name="details2_commissionOverride_checkbox")
        ctrl.tableName = 'item_detailed2'
        ctrl.fieldName = 'override_commission'
        self.nameList = 'details2_commissionOverride_checkbox'
        CD_1Sizer.Add(ctrl, 0)

        ctrl = HUD.RH_NumCtrl(self, -1, 
                                 value=0, 
                                 name='details2_commissionOverride_numctrl', 
                                 integerWidth=5, 
                                 fractionWidth=3)
        ctrl.tableName = 'item_detailed2'
        ctrl.fieldName = 'over_commission'
        self.nameList = 'details2_commissionOverride_numctrl'
        
        CD_1Sizer.Add(ctrl, 0)
        boxSizer.Add(CD_1Sizer, 0)

        CD_2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self, label="or fixed amount:")
        ctrl = HUD.RH_NumCtrl(self, -1, 
                                value=0, 
                                name="details2_commissionFixedAmt_numctrl", 
                                integerWidth=5, 
                                fractionWidth=2)
        ctrl.tableName = 'item_detailed2'
        ctrl.fieldName = 'over_fixd_comm'
        self.nameList = "details2_commissionFixedAmt_numctrl"
        CD_2Sizer.Add(text, 0)
        CD_2Sizer.Add(ctrl, 0)

        boxSizer.Add(CD_2Sizer, 0, wx.ALL|wx.ALIGN_RIGHT,2)

        D1level4Sizer.Add(boxSizer, 0)


        Duo1Sizer.Add((20,20),0)
        Duo1Sizer.Add(D1level1Sizer, 0)
        Duo1Sizer.Add((20,20),0)
        Duo1Sizer.Add(D1level2Sizer, 0)
        Duo1Sizer.Add((20,20),0)
        Duo1Sizer.Add(D1level3Sizer, 0)
        Duo1Sizer.Add((20,20),0)
        Duo1Sizer.Add(D1level4Sizer, 0)

        Duo2Sizer = wx.BoxSizer(wx.VERTICAL)

        D2level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self, label="Case Break #")
        ctrl = HUD.RH_TextCtrl(self, -1, 
                               value='', 
                               size=(120,-1), 
                               name="details2_casebreaknum_txtctrl")
        ctrl.tableName = 'item_detailed2'
        ctrl.fieldName = 'case_break_num'
        self.nameList = "details2_casebreaknum_txtctrl"

        D2level1Sizer.Add(text,0)
        D2level1Sizer.Add(ctrl, 0)

        D2level2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        ctrl = HUD.RH_CheckBox(self, -1, 
                               label='Substitute with :', 
                               name="details2_subitem_checkbox")
        ctrl.tableName = 'item_detailed2'
        ctrl.fieldName = 'substituteYN'
        self.nameList = "details2_subitem_checkbox"
        D2level2Sizer.Add(ctrl, 0)

        ctrl = HUD.RH_TextCtrl(self, -1, 
                           size=(120, -1), 
                           name="details2_subitem_txtctrl")
        ctrl.tableName = 'item_detailed2'
        ctrl.fieldName = 'substitute_num'
        self.nameList = "details2_subitem_txtctrl"
        D2level2Sizer.Add(ctrl, 0)

        D2level3Sizer = wx.BoxSizer(wx.HORIZONTAL)
        D2level3_list = [('Store\nLocation', 'details2_storeloc_txtctrl', 120, 'item_detailed2', 'location')]
                        
        spacerd = len(D2level3_list)
        
        cntd = 1
        for label, name, sized, table, field in D2level3_list:
            text = wx.StaticText(self, label=label)
            if 'weight' in name:
                ctrl = HUD.RH_NumCtrl(self, -1, 
                                      value=0, 
                                      name=name, 
                                      integerWidth=5, 
                                      fractionWidth=3)
            
            else:
                ctrl = HUD.RH_TextCtrl(self, -1, name=name)
            ctrl.tableName = table
            ctrl.fieldName = field
            self.nameList = name
            D2level3Sizer.Add(text, 0, wx.ALL|wx.ALIGN_CENTER, 2)
            D2level3Sizer.Add(ctrl, 0, wx.ALL, 3)
            cntd += 1
            if cntd < spacerd:
                D2level3Sizer.Add((10,10), 0)


        D2level4_box = wx.StaticBox(self, label="Product Image")
        D2level4_boxSizer = wx.StaticBoxSizer(D2level4_box, wx.VERTICAL)
        imageload = HUD.ButtonOps().Icons('empty')
        self.png = wx.StaticBitmap(self, -1, 
                                   wx.Bitmap(imageload, wx.BITMAP_TYPE_ANY), 
                                   size=(300,300), 
                                   style=wx.SUNKEN_BORDER)


        ctrl = HUD.RH_FilePickerCtrl(self, wx.ID_ANY,
                                     message='Please select PNG', 
                                     wildcard='*.png', 
                                     size=(500,20),
                                     name='details2_imageloc_txtctrl')
        ctrl.tableName = 'item_detailed2'
        ctrl.fieldName = 'image_loc'
        self.nameList = 'details2_imageloc_txtctrl'
        
        D2level4_boxSizer.Add(self.png, 0)
        D2level4_boxSizer.Add(ctrl, 0)

        Duo2Sizer.Add(D2level1Sizer, 0, flag=wx.ALIGN_RIGHT)
        Duo2Sizer.Add((10,10),0)
        Duo2Sizer.Add(D2level2Sizer, 0, flag=wx.ALIGN_RIGHT)
        Duo2Sizer.Add((10,10),0)
        Duo2Sizer.Add(D2level3Sizer, 0, flag=wx.ALIGN_RIGHT)
        Duo2Sizer.Add((10,10),0)
        Duo2Sizer.Add(D2level4_boxSizer, 0, flag=wx.ALIGN_RIGHT)

        MainSizer.Add(Duo1Sizer, 0)
        MainSizer.Add(Duo2Sizer, 0)

        self.SetSizer(MainSizer)

    def OnNumbersOnly(self, event):
        """
        check for numeric entry and limit to 2 decimals
        accepted result is in self.value
        """
        debug = False
        
        valued = event.GetEventObject()
        raw_value = valued.GetValue().strip()
        # numeric check
        if all(x in '0123456789.+-' for x in raw_value):
            # convert to float and limit to 2 decimals
            self.value = round(float(raw_value), 2)
            self.edit.ChangeValue(str(self.value))
        else:
            self.edit.ChangeValue("Numbers only")


    def OnLoad(self, event):
        upc = wx.FindWindowByName('inventory_itemNumber_txtctrl').GetCtrl()
        ctrl_listd = self.nameList.get()
        for name in ctrl_listd:
            item = wx.FindWindowByName(name)
            item.OnLoad(whereField='upc', whereValue=upc)
        
        
    def OnSave(self):
        upc = wx.FindWindowByName('inventory_itemNumber_txtctrl').GetCtrl()
        ctrl_listd = self.nameList.get()
        for name in ctrl_listd:
            item = wx.FindWindowByName(name)
            item.OnSave(whereField='upc',whereValue=upc)
    
    def Clear(self):
        ctrl_listd = self.nameList.get()
        for name in ctrl_listd:
            item = wx.FindWindowByName(name)
            item.Clear()

        
#----------------------------------------
class vendorTab(wx.Panel):
    def __init__(self, *args, **kwargs):
        """"""
        vendorID = kwargs.pop('vendorID')
        wx.Panel.__init__(self, *args, **kwargs)
        named = 'Vendor{}DataTab'.format(vendorID)
        self.SetName(named)
        
        self.num = vendorID
        self.vendorID = 'vendor'+str(vendorID)

        MainSizer = wx.BoxSizer(wx.VERTICAL)
        level1Sizer = wx.BoxSizer(wx.HORIZONTAL)

        level1bSizer = wx.BoxSizer(wx.HORIZONTAL)

        level2Sizer = wx.BoxSizer(wx.HORIZONTAL)

        text = wx.StaticText(self, -1, label="Vendor #")
        level2Sizer.Add(text, 0)

        vendor_ctrlList = [('vendordata_{}_vendorNum_txtctrl'.format(self.vendorID),60,wx.TE_PROCESS_ENTER),
                           ('vendordata_{}_vendorName_txtctrl'.format(self.vendorID),180,wx.TE_READONLY)]
        for name,sized,style in vendor_ctrlList:
            ctrl = HUD.RH_TextCtrl(self, -1, size=(sized, -1), name=name, style=style)
            if 'vendorNum' in name:
                ctrl.Bind(wx.EVT_TEXT_ENTER, self.CheckVendorName)
                ctrl.SetFocus()

            level2Sizer.Add(ctrl, 0)
            level2Sizer.Add((10,10),0)

        level3Sizer = wx.BoxSizer(wx.HORIZONTAL)

        vendorpagetxt_list = [('Order #', 'vendordata_{}_orderNum_txtctrl'.format(self.vendorID),120),
                              ('Last Retail\nUnit Price:', 'vendordata_{}_lastRetail_numctrl'.format(self.vendorID),120),
                              ('Last Unit\nUnit Cost:', 'vendordata_{}_lastCost_numctrl'.format(self.vendorID), 120)]
                              #('Retail Units\nin Order:','vendordata_'+self.vendorID+'_retailUnits_numctrl',80)]

        for label,name,sized in vendorpagetxt_list:
            text = wx.StaticText(self, -1, label=label)
            if 'numctrl' in name:
                ctrl = HUD.RH_NumCtrl(self, -1, value=0, name=name, integerWidth=6, fractionWidth=2)
            else:
                ctrl = HUD.RH_MTextCtrl(self, -1, size=(sized,35), name=name, formatcodes='!')
            level3Sizer.Add(text, 0)
            level3Sizer.Add(ctrl, 0)

        level4Sizer = wx.BoxSizer(wx.HORIZONTAL)

        lvl4_list = [('Lead Time','vendordata_'+self.vendorID+'_leadtime_numctrl'),
                     ('Minimum Order','vendordata_'+self.vendorID+'_minimumOrder_numctrl')]

        for label,name in lvl4_list:
            text = wx.StaticText(self, -1, label=label)
            ctrl = HUD.RH_NumCtrl(self, -1, value=0, name=name, integerWidth=3, fractionWidth=0)
            level4Sizer.Add(text, 0)
            level4Sizer.Add(ctrl, 0)
            level4Sizer.Add((20,10),0)

        level5Sizer = wx.BoxSizer(wx.HORIZONTAL)

        lvl5_list = [('Last Order','vendordata_'+self.vendorID+'_lastOrder_numctrl'),
                     ('Date','vendordata_'+self.vendorID+'_lastOrder_datectrl')]
                     #('Outstanding','vendordata_'+self.vendorID+'_outstanding_numctrl')]
        for label,name in lvl5_list:
            text = wx.StaticText(self, wx.ID_ANY, label=label)
            if 'datectrl' in name:
                ctrl = HUD.RH_DatePickerCtrl(self, name=name, style=wx.adv.DP_ALLOWNONE)
                ctrl.SetValue(wx.DateTime(1,1,1969))
            if 'numctrl' in name:
                ctrl = HUD.RH_NumCtrl(self, -1, value=0, name=name, integerWidth=3, fractionWidth=0)
            level5Sizer.Add(text, 0)
            level5Sizer.Add(ctrl, 0)
            level5Sizer.Add((20,10), 0)

        sizer_list = [level1Sizer, level2Sizer, level3Sizer, level4Sizer, level5Sizer]
        for sizer in sizer_list:
            MainSizer.Add(sizer, 0)
            MainSizer.Add((10,10),0)

        self.SetSizer(MainSizer)


    def CheckVendorName(self, event):
        debug = False
        obj = event.GetEventObject()
        named = obj.GetName()
        vendorNum = obj.GetValue().upper().strip()
        
        
        queryWhere = 'vend_num=(?) OR name LIKE (?)'
        queryData = (vendorNum,vendorNum,)
        cnt_returnd = HUD.QueryOps().QueryChecks('vendor_basic_info',queryWhere,queryData)
        if cnt_returnd == 0:
            wx.FindWindowByName(named).SetCtrl('')
            return

        if cnt_returnd == 1:
            query = 'SELECT vend_num,name FROM vendor_basic_info WHERE vend_num=(?) OR name LIKE (?)'
            data = (vendorNum,vendorNum,)
            returnd = HUD.SQConnect(query, data).ONE()
            
            
            (vendor_numd, vendor_named) = returnd[0]

        elif cnt_returnd > 1:

            style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
            VendorLookup_D =  HUD.VendorFindDialog(self, title="Customer Lookup",  vendNumber=vendorNum,style=style)
            VendorLookup_D.ShowModal()
            try:
                VendorLookup_D.itemPicked
                VendorLookup_D.Destroy()
            except:
                VendorLookup_D.Destroy()
                return

            self.vendPicked = VendorLookup_D.itemPicked.upper().strip()
            
            self.vendPicked = self.vendPicked.ljust(5)
            # query = 'SELECT vend_num,name FROM vendor_basic_info WHERE vend_num=(?)'
            # data = (self.vendPicked,)
            # returnd = HUD.SQConnect(query, data).ONE()
            returnd = LookupDB('vendor_basic_info').Specific(self.vendPicked, 'vend_num', 'vend_num, name')
            
            (vendor_numd, vendor_named) = returnd

        vendor_name_list = [('vendordata_{}_vendorNum_txtctrl'.format(self.vendorID),vendor_numd),
                            ('vendordata_{}_vendorName_txtctrl'.format(self.vendorID),vendor_named)]
        for name,value in vendor_name_list:
            

            item = wx.FindWindowByName(name)
            item.SetValue(value)



    def OnLoad(self):
        
        upc = wx.FindWindowByName('inventory_itemNumber_txtctrl').GetCtrl()
        
                
        for i in range(1,7):
            vendor_list = [('vendordata_vendor{}_vendorNum_txtctrl'.format(i), 'vendorNum'),
                       ('vendordata_vendor{}_orderNum_txtctrl'.format(i), 'orderNum'),
                       ('vendordata_vendor{}_lastRetail_numctrl'.format(i), 'lastRetail'),
                       ('vendordata_vendor{}_lastCost_numctrl'.format(i), 'lastCost'),
                       ('vendordata_vendor{}_leadtime_numctrl'.format(i), 'leadTime'),
                       ('vendordata_vendor{}_minimumOrder_numctrl'.format(i), 'minOrder'),
                       ('vendordata_vendor{}_lastOrder_datectrl'.format(i), 'lastOrder')]
            
            selfield = f'vendor{i}'
            returnd = LookupDB('item_detailed').Specific(upc, 'upc', selfield)
            try:
                vend_dict = json.loads(returnd)
            except TypeError as e:
                print(e)
            
            for item, key in vendor_list:
                ctrl = wx.FindWindowByName(item).SetCtrl(vend_dict[key])
            
            
        # for name, table, field in vendor_list:
        #     # query = '''SELECT {}
        #     #            FROM {}
        #     #            WHERE upc=(?)'''.format(field, table)
        
        #     # data = [upc,]
        #     # returnd = HUD.SQConnect(query, data).ONE()
        #     #returnd = LookupDB(table).Specific(upc, 'upc', field)
        #     #ret = VarOps().DeTupler(returnd)
        #     #wx.FindWindowByName(name).SetCtrl(ret)
        #     pout.v(f"Name : {name} ; Table : {table} ; Field : {field} ; UPC : {upc}")
        #     item = wx.Window.FindWindowByName(name)
        #     item.OnLoad(table, field, 'upc', upc)
            

    
    def OnSave(self):
        upc = wx.FindWindowByName('inventory_itemNumber_txtctrl').GetCtrl()
        vend_dict = {}
        
        for i in range(1,7):
            vendor_list = [('vendordata_vendor{}_vendorNum_txtctrl'.format(i), 'vendorNum'),
                           ('vendordata_vendor{}_orderNum_txtctrl'.format(i),  'orderNum'),
                           ('vendordata_vendor{}_lastRetail_numctrl'.format(i), 'lastRetail'),
                           ('vendordata_vendor{}_lastCost_numctrl'.format(i),   'lastCost'),
                           ('vendordata_vendor{}_leadtime_numctrl'.format(i),   'leadTime'),
                           ('vendordata_vendor{}_minimumOrder_numctrl'.format(i), 'minOrder'),
                           ('vendordata_vendor{}_lastOrder_datectrl'.format(i), 'lastOrder')]
        
            dm = HUD.DictMaker()
            for name, key in vendor_list:
                val = wx.FindWindowByName(name).GetCtrl()
                dm.add(key, val)

            setField = f'vendor{i}'
            vend_dict = dm.get()
            pout.b('DM : {}'.format(vend_dict))
            vend_dict_JSON = json.dumps(vend_dict)
            LookupDB('item_detailed').UpdateSingle(setField, vend_dict_JSON, 'upc', upc)

            
            #item = wx.Window.FindWindowByName(name)
            #item.OnSave(table, field, 'upc', upc)                   
        # fieldSet, dataSet, table = HUD.QueryOps().Commaize(vendor_list)
        
        # # query = '''UPDATE {}
        # #            SET {}
        # #            WHERE upc=(?)'''.format(table, fieldSet)
        
        # data = dataSet + [upc,]
        # # returnd = HUD.SQConnect(query, data).ONE()
        # returnd = LookupDB(table).UpdateGroup(fieldSet, 'upc', data)

        
    def Clear(self):
        vendor_list = ['vendor1','vendor2','vendor3','vendor4','vendor5','vendor6']
        for num in vendor_list:
            vendordata_default_list = ['vendordata_{}_vendorNum_txtctrl'.format(num),
                                       'vendordata_{}_vendorName_txtctrl'.format(num),
                                       'vendordata_{}_lastRetail_numctrl'.format(num),
                                       'vendordata_{}_orderNum_txtctrl'.format(num),
                                       'vendordata_{}_lastRetail_numctrl'.format(num),
                                       'vendordata_{}_retailUnits_numctrl'.format(num),
                                       'vendordata_{}_leadtime_numctrl'.format(num),
                                       'vendordata_{}_minimumOrder_numctrl'.format(num),
                                       'vendordata_{}_lastOrder_numctrl'.format(num),
                                       'vendordata_{}_lastOrder_datectrl'.format(num),
                                       'vendordata_{}_outstanding_numctrl'.format(num)]

            for name in vendordata_default_list:
                clear = wx.FindWindowByName(name).Clear()






#----------------------------------

class page_vendordata(wx.Panel):
    def __init__(self, *args, **kwargs):
        """"""
        wx.Panel.__init__(self, *args, **kwargs)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        nestednb = wx.Notebook(self, wx.ID_ANY, name='vendordata_vendor_notebook')

        vendorTabs = [1, 2, 3, 4, 5, 6]
        for tab in vendorTabs:
            page = vendorTab(nestednb, vendorID=tab)
            nestednb.AddPage(page, "Vendor {}".format(tab))
        
        #page1 = vendorTab(nestednb, vendorID=1)
        #page2 = vendorTab(nestednb, vendorID=2)
        #page3 = vendorTab(nestednb, vendorID=3)
        #page4 = vendorTab(nestednb, vendorID=4)
        #page5 = vendorTab(nestednb, vendorID=5)
        #page6 = vendorTab(nestednb, vendorID=6)

        #nestednb.AddPage(page1, "Vendor 1")
        #nestednb.AddPage(page2, "Vendor 2")
        #nestednb.AddPage(page3, "Vendor 3")
        #nestednb.AddPage(page4, "Vendor 4")
        #nestednb.AddPage(page5, "Vendor 5")
        #nestednb.AddPage(page6, "Vendor 6")

        sizer.Add(nestednb, 1, wx.ALL|wx.EXPAND, 5)

        self.SetSizer(sizer)
        self.Layout()







#----------------------------------------


class page_notes(wx.Panel):
    def __init__(self, *args, **kwargs):
        """"""
        wx.Panel.__init__(self, *args, **kwargs)
        
        self.SetName('NotesTab')
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        self.ItemNumberd = wx.FindWindowByName('inventory_itemNumber_txtctrl').GetCtrl()
        
        yellowback = (246,241,87)
        self.ctrl = HUD.RH_TextCtrl(self, -1, 
                                size=(700,500), 
                                name="notes_notes_txtctrl", 
                                style=wx.TE_MULTILINE)
        
        self.ctrl.SetBackgroundColour(yellowback)
        MainSizer.Add(self.ctrl, 0, wx.ALL|wx.ALIGN_CENTER, 5)

        self.SetSizer(MainSizer)

    def OnLoad(self, event):
        # query = '''SELECT {}
        #            FROM {}
        #            WHERE upc=(?)'''.format('notes','item_notes')
        # data = [self.ItemNumberd,]
        # returnd = HUD.SQConnect(query, data).ONE()
        returnd = LookupDB('item_notes').Specific(self.ItemNumberd, 'upc', 'notes')
        ret = VarOps().DeTupler(returnd)
        self.ctrl.SetValue(ret) #CO('notes_notes_txtctrl').SetCtrl(ret)
        
    
    def OnSave(self):
        returnd = LookupDB('item_notes').UpdateSingle('notes',self.ctrl.GetValue(),'upc',self.ItemNumberd)

        
    
    def Clear(self):
        notes_default_list = ['notes_notes_txtctrl']
        for name in notes_default_list:
            clear = wx.FindWindowByName(name).ClearCtrl()

        
#----------------------------------------

class page_pos_saleslinks(wx.Panel):
    def __init__(self, *args, **kwargs):
        """"""
        wx.Panel.__init__(self, *args, **kwargs)
        self.SetName('posSalesLinks_Tab')
        MainSizer = wx.BoxSizer(wx.VERTICAL)

        Level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.grid = HUD.POSLinks_Grid(self, name='inv_posSalesLinks_poslinks_grid')

        Level1Sizer.Add(self.grid, 0)
        
        MainSizer.Add(Level1Sizer, 0, wx.ALL|wx.ALIGN_CENTER,10)
        self.SetSizer(MainSizer)

    

#----------------------------------------
class custInstructionTab(wx.Panel):
    def __init__(self, *args, **kwargs):
        """"""
        infoType = kwargs.pop('infoType')
        wx.Panel.__init__(self, *args, **kwargs)
        self.tabType = infoType
        named = f'CustInstruct_{self.tabType}_Tab'
        self.SetName(named)
        

        MainSizer = wx.BoxSizer(wx.VERTICAL)
        Level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.ItemNumberd = wx.FindWindowByName('inventory_itemNumber_txtctrl').GetCtrl()

        Level2Sizer = wx.BoxSizer(wx.HORIZONTAL)

        idx = 0
        print_choices = ['Always Print','Prompt Before Printing']
        radiobox = HUD.RH_RadioBox(self, -1, 
                               label='Print Options',
                               choices=print_choices, 
                               name='custinst_'+self.tabType+'_printOptions_radiobox')

        Level2Sizer.Add(radiobox, 0)

        std_dialog_combobox = HUD.RH_ComboBox(self, -1, name='custinst_'+self.tabType+'_stdDialog_combobox')

        Level2Sizer.Add((250,10),0)
        Level2Sizer.Add(std_dialog_combobox, 0, wx.ALL|wx.EXPAND|wx.ALIGN_RIGHT, 5)

        ctrl = HUD.RH_TextCtrl(self, -1, size=(800,300),name='custinst_'+self.tabType+'_custinstruct_txtctrl',style=wx.TE_MULTILINE)

        infoButton = wx.FindWindowByName('custinst_custInfo_button')


        MainSizer.Add(Level1Sizer, 0)

        MainSizer.Add(Level2Sizer, 0, wx.ALL, 15)
        
        MainSizer.Add(ctrl, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.SetSizer(MainSizer)

        wx.CallAfter(self.OnLoad, event='')
    
    def OnLoad(self, event):
        
        custInst_list = ['Info','ReturnPolicy','Warranty']
        for typed in custInst_list:
            irw = re.sub('Policy', '', typed, flags=re.I).lower()
            clist = [('print_{}_options'.format(irw),'custinst_{}_printOptions_radiobox'.format(typed), 'item_cust_instructions'),
                     ('{}_box'.format(irw),'custinst_{}_custinstruct_txtctrl'.format(typed), 'item_cust_instructions')]
            
            for field, name, table in clist:
                returnd = LookupDB('table').Specific(self.ItemNumberd,'upc',field)
                ret = VarOps().DeTupler(returnd)
                
                wx.FindWindowByName(name).SetCtrl(ret)
                
                
    def OnSave(self, upc):
        
        custInst_list = ['Info','ReturnPolicy','Warranty']
        for typed in custInst_list:
            irw = re.sub('Policy', '', typed, flags=re.I).lower()
            clist = [('print_{}_options'.format(irw),'custinst_{}_printOptions_radiobox'.format(typed), 'item_cust_instructions'),
                     ('{}_box'.format(irw),'custinst_{}_custinstruct_txtctrl'.format(typed), 'item_cust_instructions')]
            
            for field, name, table in clist:
                item = wx.FindWindowByName(name).GetCtrl()
                
                # query = '''UPDATE {} 
                #            SET {}=(?)
                #            WHERE upc=(?)
                #         '''.format(table, field)
                # data = [item, self.ItemNumberd,]
                # returnd = HUD.SQConnect(query, data).ONE()
                returnd = LookupDB(table).UpdateSingle(field, item, 'upc',self.ItemNumberd)
                
                
    def Clear(self):
        custInst_list = ['Info','ReturnPolicy','Warranty']
        for typed in custInst_list:
            custinst_default_list = ['custinst_'+typed+'_printOptions_radiobox','custinst_'+typed+'_custinstruct_txtctrl']
            for name in custinst_default_list:
                clear = wx.FindWindowByName(name).ClearCtrl()

        

class page_customer_instructions(wx.Panel):
    def __init__(self, *args, **kwargs):
        """"""
        wx.Panel.__init__(self, *args, **kwargs)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        nestednb = wx.Notebook(self, wx.ID_ANY, name='custinst_info_notebook')

        tabType = [("Info", "Information"), ("ReturnPolicy", "Return Policy"), ("Warranty", "Warranty")]
        
        for field_part, header in tabType:
            page = custInstructionTab(nestednb, infoType=field_part)
            nestednb.AddPage(page, header)
        

        sizer.Add(nestednb, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(sizer)
        self.Layout()

    def OnLoad(self, event):
        pass        
        
    def OnSave(self, event):
        pass
        
    def Clear(self):
        pass
        

#----------------------------------------

class page_consignment(wx.Panel):
    def __init__(self, *args, **kwargs):
        """"""
        wx.Panel.__init__(self, *args, **kwargs)
        
        self.SetName('PageConsignmentTab')
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)

        Level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        consign_list = [('Vendor # ','consignment_vendor_txtctrl'),
                        ('Override Standard Fee :',
                            'consignment_overrideFee_txtctrl')]
        
        for label, name in consign_list:
            text = wx.StaticText(self, -1, label=label)
            txtctrl = HUD.RH_TextCtrl(self, -1, size=(80,-1), name=name)
            Level1Sizer.Add(text, 0,wx.ALL,5)
            Level1Sizer.Add(txtctrl, 1,wx.ALL, 5)
            Level1Sizer.Add((30,30),0)

        MainSizer.Add(Level1Sizer, 0)

        self.SetSizer(MainSizer)
        
    def OnLoad(self, event):
        conList = [('consignment_vendor_txtctrl','')]
        pass
        
    def OnSave(self, event):
        pass
        
    def Clear(self):    
        consign_list = ['consignment_vendor_txtctrl',
                        'consignment_overrideFee_txtctrl']
        
        for name in consign_list:
            wx.FindWindowByName(name).ClearCtrl()
            
        
#----------------------------------------

class page_8(wx.Panel):
    def __init__(self, *args, **kwargs):
        """"""
        wx.Panel.__init__(self, *args, **kwargs)
        
#----------------------------------------

class page_daily_movement(wx.Panel):
    def __init__(self, *args, **kwargs):
        """"""
        wx.Panel.__init__(self, *args, **kwargs)
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        date_list = [('Begin Date','inv_dailyMovement_movement_start_datectrl'), ('End Date','inv_dailyMovement_movement_end_datectrl')]
        for label, name in date_list:
            box = wx.StaticBox(self, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            
            datectrl = HUD.RH_DatePickerCtrl(self, -1, name=name, style=wx.adv.DP_ALLOWNONE)
            today = datetime.date.today()
            datectrl.SetValue(wx.DateTime().Today())
            
            boxSizer.Add(datectrl, 0)
            level1Sizer.Add(boxSizer, 0, wx.ALL|wx.CENTER, 5)
        
        button = wx.Button(self, -1, label='GO', name='inv_dailyMovement_go_button')
        button.Bind(wx.EVT_BUTTON, self.checkTransactions)
        level1Sizer.Add((10,10), 0)
        level1Sizer.Add(button, 0, wx.ALL|wx.ALIGN_CENTER, 3)

        MainSizer.Add(level1Sizer, 0, wx.ALL|wx.CENTER, 3)
        
        grid =  HUD.Activity_Grid(self,name='inv_dailyMovement_movement_grid')
                            
        MainSizer.Add(grid, 0, wx.ALL|wx.LEFT, 5)

        #graph =  HUD.SalesGraph(self)

        #MainSizer.Add(graph, 0, wx.ALL|wx.RIGHT, 5)
        
        self.SetSizer(MainSizer)

    def ActivityCheck(self, event):
        debug = False
        pass

    def checkTransactions(self, event):
        """ Check Transactions for Item Sold on this Date """
        itemNumber = wx.FindWindowByName('inventory_itemNumber_txtctrl').GetCtrl()
        debug = True
        fields = 'date,quantity,total_price'
        # query = 'SELECT date, quantity, avg_cost, total_price FROM transactions WHERE upc=(?)'
        # data = (itemNumber,)
        # returnd = HUD.SQConnect(query,data).ALL()
        returnd = LookupDB('transactions').Specific(itemNumber, 'upc', 'date,quantity,avg_cost,total_price')
        begin_date = wx.FindWindowByName('inv_dailyMovement_movement_start_datectrl').GetCtrl()
        end_date = wx.FindWindowByName('inv_dailyMovement_movement_end_datectrl').GetCtrl()
        gridname = 'inv_dailyMovement_movement_grid'
        
        
        
        VarOps().GetTyped(returnd)
        HUD.GridOps(gridname).AlterGrid(returnd)
        if returnd is not None:
            idx = 0
            accum = {}
            for dated, qty, avgcost, price in returnd:
                if dated is None:
                    continue
                
                
                VarOps().GetTyped(begin_date)
                
                VarOps().GetTyped(dated)
                
                VarOps().GetTyped(end_date)
                
                gross_profit = Decimal(qty)*(Decimal(price) - Decimal(avgcost))
                begin = datetime.datetime.strptime(begin_date, '%Y-%m-%d').date()
                end = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
                
                if begin <= dated <= end:
                    if dated in accum:
                        qty_d = accum[dated][0] + qty
                        accum[dated][0]=qty_d
                        accum[dated][2] += Decimal(gross_profit)
                        
                    else:
                        accum[dated]=[qty, avgcost, gross_profit]
                    
            
            idx = 0
            for key, value in list(accum.items()):
                setList = [('Activity Date',key),('Sales Volume',value[0]),('Sales Amount',value[1]), ('Gross Profit', RO.DoRound(value[2], '1.00'))]
                HUD.GridOps(gridname).FillGrid(setList,row=idx)
                idx += 1


#----------------------------------------

class DetailsTab(wx.Panel):
    def __init__(self, *args, **kwargs):
        """"""
        wx.Panel.__init__(self, *args, **kwargs)
        
        sizer = wx.BoxSizer(wx.VERTICAL)

        nestednb = wx.Notebook(self, wx.ID_ANY, name='inventory_details_notebook')

        tabType = [('Item Detail', page_item_detail),
                   ('Item Detail(2)', page_detail_pg2),
                   ('Vendor Data', page_vendordata),
                   ('Notes', page_notes),
                   ('POS Sales Links', page_pos_saleslinks),
                   ('Consignment', page_consignment),
                   ('', page_8),
                   ('Movement', page_daily_movement)]
         
        for title, tabpage in tabType:
            page = tabpage(nestednb)
            nestednb.AddPage(page, title)
            
#         page1 = page_item_detail(nestednb)
#         page2 = page_detail_pg2(nestednb)
#         page3 = page_vendordata(nestednb)
#         page4 = page_notes(nestednb)
#         page5 = page_pos_saleslinks(nestednb)
#         page6 = page_customer_instructions(nestednb)
#         page7 = page_consignment(nestednb)
#         page8 = page_8(nestednb)
#         page9 = page_daily_movement(nestednb)
#             

        
#         nestednb.AddPage(page1, "Item_Detail")
#         nestednb.AddPage(page2, "Item_Detail(2)")
#         nestednb.AddPage(page3, "Vendor Data")
#         nestednb.AddPage(page4, "Notes")
#         nestednb.AddPage(page5, "POS Sales Links")
#         nestednb.AddPage(page6, "Customer Instructions")
#         nestednb.AddPage(page7, "Consignment")
#         nestednb.AddPage(page8, "           ")
#         nestednb.AddPage(page9, "Daily Movement")

        sizer.Add(nestednb, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(sizer)
        self.Layout()

    #----------------------------------------------------------------------




class StartPanel(wx.Panel):
    """"""
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.SetName('StartPanel')
        lookupSizer = wx.BoxSizer(wx.VERTICAL)
        debug = False

        IconBar_list =[('Save', self.OnSave),
                       ('Undo', self.OnUndo),
                       ('Find', self.OnFind),
                       ('Add', self.OnAdd),
                       ('Delete', self.OnMinus),
                       ('Receiving', self.OnReceive),
                       ('Exit', self.OnExitButton)]

        iconbar = HUD.IconPanel(self, iconList=IconBar_list)
        
        lookupSizer.Add(iconbar, 0, wx.EXPAND)
        level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        name = 'inventory_itemNumber_txtctrl'
        ctrl = HUD.RH_TextCtrl(self, -1, size=(250,-1), name=name, style=wx.TE_PROCESS_ENTER|wx.TE_PROCESS_TAB)
        ctrl.SetFocus()
        ctrl.SelectAll()
        ctrl.SetHint('Item Number')
        ctrl.SetToolTip(wx.ToolTip('Enter Item Number Here & press Enter'))
        ctrl.Bind(wx.EVT_KEY_DOWN, self.onCatchKey)
        ctrl.fieldName = 'upc'
        ctrl.tableName = 'item_detailed'
        level1Sizer.Add(ctrl, 0, wx.ALL, 3)

        name = 'inventory_itemDescription_txtctrl'
        ctrl = HUD.RH_TextCtrl(self, -1, size=(350,-1), name=name, style=wx.TE_PROCESS_TAB)
        ctrl.SetHint('Item Description')
        ctrl.SetToolTip(wx.ToolTip('Enter Item Description Here'))
        ctrl.Bind(wx.EVT_KILL_FOCUS, HUD.EventOps().CheckMeasurements)
        ctrl.fieldName = 'description'
        ctrl.tableName = 'item_detailed'
        level1Sizer.Add(ctrl, 0, wx.ALL, 3)

        # for label, name, sized, table, field in lvl1_list:
        #     box = wx.StaticBox(self, label=label)
        #     boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        #     if 'itemNumber' in name:
        #         ctrl = HUD.RH_TextCtrl(self, -1, 
        #                            size=(sized, 21), 
        #                            name=name, 
        #                            style=wx.TE_PROCESS_ENTER|wx.TE_PROCESS_TAB)
                
        #         ctrl.SetFocus()
        #         ctrl.SelectAll()
        #         ctrl.Bind(wx.EVT_KEY_DOWN, self.onCatchKey)

        #     if 'itemDescription' in name:
        #         ctrl = HUD.RH_TextCtrl(self, -1, 
        #                            size=(sized, 21), 
        #                            name=name, 
        #                            style=wx.TE_PROCESS_TAB)
                
        #         ctrl.Bind(wx.EVT_KILL_FOCUS, HUD.EventOps().CheckMeasurements)
        #     ctrl.fieldName = field
        #     ctrl.tableName = table
        #     boxSizer.Add(ctrl, 0, wx.EXPAND|wx.ALL,3)
        #     level1Sizer.Add(boxSizer, 0, wx.ALL,3)
        
        countreturn = HUD.QueryOps().QueryCheck('item_detailed')
        pout.v(countreturn)
        if countreturn > 0:
            returnd = LookupDB('item_detailed').General('upc',limit=1)
            pout.v(str(type(returnd)),returnd)
            itemNumber = wx.FindWindowByName('inventory_itemNumber_txtctrl')
            itemNumber.SetCtrl(returnd)

            wx.CallAfter(self.OnItemNumber, event=None, upc=itemNumber.GetValue().strip())

        lookupSizer.Add(level1Sizer, 0)

        level2Sizer = wx.BoxSizer(wx.HORIZONTAL)

        notebook = wx.Notebook(self, -1, name='inventory_main_notebook')
        tabOne = MainOptionsTab(notebook)
        notebook.AddPage(tabOne, "General Options")
        tabTwo = DetailsTab(notebook)

        notebook.AddPage(tabTwo, "Details")

        notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)

        level2Sizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)


        lookupSizer.Add(level2Sizer, 0)

        self.SetSizer(lookupSizer)
        self.Layout()

    def OnPageChanged(self, event):
        debug = False
        obj = event.GetEventObject()
        named = obj.GetName()
        notebook = wx.FindWindowByName(named)
        old = notebook.GetPageText(event.GetOldSelection())
        new = notebook.GetPageText(event.GetSelection())
        
        itemNumber = wx.FindWindowByName('inventory_itemNumber_txtctrl')

        
        if 'General Options' in new :
            itemNumber.SetEditable(True)
            
        else:
            itemNumber.SetEditable(False)
            
        event.Skip()


    def OnUndo(self, event):
        debug = False
        wx.CallAfter(self.OnItemNumber, event='')

    def OnExitButton(self, event):
        debug = False
        item = wx.FindWindowByName('Inventory_Frame')
        item.Close()



    def OnFind(self, event):
        debug = False
        itemNumber = wx.FindWindowByName('inventory_itemNumber_txtctrl').GetCtrl()

        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
        ItemLookupD =  HUD.ItemLookupDialog(self, 
                                               title="Item Lookup", 
                                               style=style, 
                                               itemNumber=itemNumber)
        
        ItemLookupD.ShowModal()
        try:
            self.itempick = ItemLookupD.itemPicked
            ItemLookupD.Destroy()
        except:
            ItemLookupD.Destroy()
        else:
            wx.CallAfter(self.OnItemNumber, event='')

        itemNum = wx.FindWindowByName('inventory_itemNumber_txtctrl').SetCtrl(self.itempick.upper().strip())
        wx.CallAfter(self.OnItemNumber,event=None, upc=self.itempick)

    def OnReceive(self, event):
        debug = False
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
        recdlg =  HUD.ReceivingDialog(self,
                                       title='Receiving Utility',
                                       style=style)

        recdlg.ShowModal()
        
                                               
        
    def OnMinus(self, event):
        """ Delete Record """
        debug = False
        itemNumberd = wx.FindWindowByName('inventory_itemNumber_txtctrl').GetCtrl().strip()
        itemDesc = wx.FindWindowByName('inventory_itemDescription_txtctrl').GetCtrl()

        yesno = wx.MessageBox('Delete Item #{0} ?'.format(itemNumberd),'Delete Item',wx.YES_NO)
        if yesno == wx.YES:
            table_list = ['item_options','item_detailed','item_detailed2',
                          'item_vendor_data','item_notes','item_sales_links',
                          'item_cust_instructions','item_options','item_history']
            
            for table in table_list:
                query = "DELETE FROM {0} WHERE upc=(?)".format(table)
                data = (itemNumberd,)
                countreturn = HUD.SQConnect(query, data).ONE()

                

        query = 'select upc from item_detailed limit 1'
        data = ''
        getNew = HUD.SQConnect(query, data).ONE()[0]
        
        wx.FindWindowByName('inventory_itemNumber_txtctrl').SetCtrl(getNew)
        wx.CallAfter(self.OnItemNumber, event='')


    def OnAdd(self, event):
        debug = False
        
        item_list = ['inventory_itemDescription_txtctrl',
                     'inventory_itemNumber_txtctrl']
        
        for name in item_list:
            item = wx.FindWindowByName(name)
            item.SetEditable(True)
            item.Clear()
        
        tab_list = ['MainOptionsTab','PageItemDetailTab','inv_details_cost_grid','PageDetailPage2Tab','NotesTab','posSalesLinks_Tab','PageConsignmentTab']
        
        for name in tab_list:
            tab = wx.FindWindowByName(name)
            print(f'Tab : {name}')
            tab.Clear()

        for i in range(1,7):
            tab = wx.FindWindowByName('Vendor{}DataTab'.format(i))
            tab.Clear()
                
        
        custInst_list = ['Info','ReturnPolicy','Warranty']
        for item in custInst_list:
            tab = wx.FindWindowByName('CustInstruct_{}_Tab'.format(item))
            if VarOps().CheckNone(tab) is not None:
                tab.Clear()
        
   #---- Flash Add Dialog
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
        FlashAdd_D =  HUD.FlashAddInventory(self, title="Add Item", size=(1000,800), style=style)
        FlashAdd_D.ShowModal()
        #
        try:
            self.itemPicked = FlashAdd_D.itemPicked
            item = wx.FindWindowByName('inventory_itemNumber_txtctrl').SetValue(str(self.itemPicked))
            FlashAdd_D.Destroy()
        except:
            FlashAdd_D.Destroy()
            return



#EndOnAdd


    def OnSave(self, event):
        debug = True
        
        ItemNumberd = wx.FindWindowByName('inventory_itemNumber_txtctrl').GetCtrl().upper().strip()


        table_list = ['item_options','item_detailed','item_detailed2','item_vendor_data','item_notes',
                      'item_sales_links','item_cust_instructions','item_options','item_history', 'item_retails']
        HUD.QueryOps().CheckEntryExist('upc',ItemNumberd,table_list)
        
        #retail_grid =  HUD.Retail_Grid(self, name='inv_details_cost_grid')    
        #retail_grid.OnSave(upc=ItemNumberd)
        
        #Retails Grid
        grid = wx.FindWindowByName('inv_details_cost_grid')
        grid.OnSave(upc=ItemNumberd)
        
        a = '-'*60
        
        #General Options TabPage
        save_list1 = [('genOptions_department_combobox'),
                      ('genOptions_category_combobox'),
                      ('genOptions_subcategory_combobox'),
                      ('genOptions_location_combobox'),
                      ('genOptions_glpost_txtctrl'),
                      ('genOptions_unittype_combobox'),
                      ('genOptions_itemType_radiobox'),
                      ('genOptions_agepopup_numctrl'),
                      ('genOptions_POSoptions_radiobox'),
                      ('genOptions_units_in_package_numctrl'),
                      ('genOptions_foodStampExempt_checkbox'),
                      ('genOptions_loyaltyExempt_checkbox'),
                      ('genOptions_consignment_checkbox'),
                      ('genOptions_aisleNums_combobox'),
                      ('genOptions_extraPlaces_combobox'),
                      ('genOptions_sectionNums_combobox'),
                      ('genOptions_deactivated_checkbox'),
                      ('genOptions_closeout_checkbox'),
                      ('genOptions_partNumber_txtctrl'),
                      ('genOptions_oemNumber_txtctrl'),
                      ('inventory_itemDescription_txtctrl'),
                      ('genOptions_kitNumber_txtctrl'),
                      ('genOptions_kitPieces_numctrl')]
        
        for name in save_list1:
            item = wx.Window.FindWindowByName(name)
            item.OnSave('upc', ItemNumberd)
        # save_lists = [save_list1, save_list2]
        # for listd in save_lists:
        #     for name,table,column_header in listd:
        #         if 'listbox' in name:
        #             LCO(name).ListBoxClearSpaces()
            
        #     fieldSet, dataSet, table = HUD.QueryOps().Commaize(listd)

            # if len(dataSet) > 0:
            #     query = '''UPDATE {} 
            #                SET {}
            #                WHERE upc=(?)'''.format(table,fieldSet)

            #     data = dataSet + [ItemNumberd,]
            #     call_db = HUD.SQConnect(query, data).ONE()
                

        
        
        fieldSet=''
        dataSet = []
       
        numv = 0
        for num in range(1,7):
            tab = wx.FindWindowByName('Vendor{}DataTab'.format(num))
            tab.OnSave()
 
        
        retail_list = [('inv_details_cost_grid','item_detailed','retails')]
        
        save_list0 = [('details_altlookup_listbox','item_detailed', 'altlookup'),
                      ('details_avgcost_numctrl','item_detailed','avg_cost'),
                      ('details_lastcost_numctrl','item_detailed','last_cost')]
        
        save_list1 = [('details_donotdiscount_checkbox','item_detailed2','do_not_discount'),
                      ('details_taxlvl_1_checkbox','item_detailed2','tax1'),
                      ('details_taxlvl_2_checkbox','item_detailed2','tax2'),
                      ('details_taxlvl_3_checkbox','item_detailed2','tax3'),
                      ('details_taxlvl_4_checkbox','item_detailed2','tax4'),
                      ('details_taxlvl_never_checkbox','item_detailed2','tax_never'),
                      ('details_taxoverride_numctrl','item_detailed2','override_tax_rate'),
                      ('details_buy_numctrl','item_detailed2','buyx'),
                      ('details_get_numctrl','item_detailed2','gety'),
                      ('details_saleDateBegin_datectrl','item_detailed2','sale_begin'),
                      ('details_saleDateEnd_datectrl','item_detailed2','sale_end'),
                      ('details_saleTimeBegin_timectrl','item_detailed2','sale_begin_time'),
                      ('details_saleTimeEnd_timectrl','item_detailed2','sale_end_time'),
                      ('inv_details_orderctrl_grid','item_detailed2','orderctrl')]

        save_list = [save_list0, save_list1]
        for listd in save_list:
            for name,table,column_header in listd:
                pout.v(f'Name : {name}')
                if 'listbox' in name:
                    HUD.ListBox_Ops(name).ListBoxClearSpaces()
    
                item = wx.FindWindowByName(name)
                item.OnSave(table, column_header, 'upc', ItemNumberd)
                # fieldSet, dataSet, table = HUD.QueryOps().Commaize(listd)
                # if len(dataSet) > 0:
                #     query = 'UPDATE {0} SET {1} WHERE upc=(?)'.format(table,fieldSet)
                #     data = dataSet + [ItemNumberd,]
                #     call_db = HUD.SQConnect(query, data).ONE()
                    

        save_list2 = [('details2_creditbookExempt_checkbox', 'item_detailed2','credit_book_exempt'),
                              ('details2_deleteWhenOut_checkbox', 'item_detailed2','delete_when_out'),
                              ('details2_lastSale_datectrl','item_detailed2','last_saledate'),
                              ('details2_lastReturn_datectrl','item_detailed2','last_returndate'),
                              ('details2_lastMaint_datectrl','item_detailed2','maintdate'),
                              ('details2_added_datectrl','item_detailed2','added_date'),
                              ('details2_commissionOverride_checkbox','item_detailed2','override_commission'),
                              ('details2_commissionOverride_numctrl','item_detailed2','over_commission'),
                              ('details2_commissionFixedAmt_numctrl','item_detailed2','over_fixd_comm'),
                              ('details2_casebreaknum_txtctrl','item_detailed2','case_break_num'),
                              ('details2_subitem_checkbox','item_detailed2','substituteyn'),
                              ('details2_subitem_txtctrl','item_detailed2','substitute_num'),
                              ('details2_storeloc_txtctrl','item_detailed2','location')]
                            #   ('details2_weight_numctrl','item_detailed2','weight'),
                            #   ('details2_tareweight_numctrl','item_detailed2','tare_weight')]
                              
        save_list3 = [('details2_onHand_numctrl','item_detailed','quantity_on_hand'),
                              ('details2_committed_numctrl','item_detailed','quantity_committed'),
                              ('details2_onLayaway_numctrl','item_detailed','quantity_on_layaway')]
                              
        save_list4 = [('inv_posSalesLinks_poslinks_grid','item_sales_links','sales_links')]
                        
        save_list5 = [('notes_notes_txtctrl','item_notes','notes')]
        
        save_list = [save_list2, save_list3, save_list4, save_list5]
        for listd in save_list:
            for name, table, field in listd:
                item = wx.FindWindowByName(name)
                pout.v(f"name : {name}")
                item.OnSave(table, field, 'upc', ItemNumberd)
            

        HUD.RecordOps('item_detailed2').UpdateRecordDate('maintdate','upc',ItemNumberd,
                            'details2_lastMaint_datectrl')

        for item in ['Info','ReturnPolicy','Warranty']:
            tabname = f'CustInstruct_{item}_tab'
            tab = wx.FindWindowByName(tabname)
            pout.v(f"item : {item} ; tabName : {tabname}")
            tab.OnSave(ItemNumberd)


        # a = wx.FindWindowByName('PageAltLookups')
        # a.OnSave()

    

    def onCatchKey(self, event):
        debug = False
        keycode = event.GetKeyCode()
        if keycode in [wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER, wx.WXK_TAB]:
            self.OnItemNumber(event=None)
            event.EventObject.Navigate()

        event.Skip()

    def ItemLookup(self, upc, itemNumber_name=None):
        debug = False
        upc    
        if upc == None:
            return
        
        query = 'SELECT upc FROM item_detailed WHERE upc=(?)'
        data = (upc,)
        returnd = HUD.SQConnect(query, data).ONE()
        
        if not returnd:
            whereFrom = '''upc LIKE (?) OR
                           altlookup LIKE (?) OR
                           description LIKE (?) OR
                           oempart_num LIKE (?) OR
                           part_num LIKE (?)'''
    
            query = "SELECT upc FROM item_detailed WHERE {0}".format(whereFrom)
            
            data = (upc, upc, upc, upc, upc,)
            
            returnd = HUD.SQConnect(query, data).ALL()
    
                
        numresult = len(returnd)
    
    
        
        if numresult == 0:
            wx.MessageBox('Item Not Found','Info',wx.OK)
            query = 'SELECT upc FROM item_detailed LIMIT 1'
            data = ''
            returnd = HUD.SQConnect(query, data).ONE()
            if itemNumber_name is not None:
                wx.FindWindowByName('inventory_itemNumber_txtctrl').SetCtrl(returnd[0])
            
            #wx.CallAfter(self.OnItemNumber, event='')
            found = False
            return returnd[0], found
    
        if numresult > 1:
            itemreturnd = list(sum(returnd, ()))
            #Debugger("{0} Create Modal Window for Individual Choosing...".format('*'*15))
            style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
            ItemLookupD =  HUD.ItemLookupDialog(self, title="Item Lookup", style=style, itemNumber=upc)
            ItemLookupD.ShowModal()
            
            itempick = ItemLookupD.itemPicked
            
    
            try:
                itempick
            except:
                if itemNumber_name is not None:   
                    wx.FindWindowByName('inventory_itemNumber_txtctrl').SetCtrl((str(self.itempick)))
                
                
            ItemLookupD.Destroy()
    
        else:
            itempick = VarOps().DeTupler(returnd)
    
            
            typed = type(itempick)
            
        found = True    
        
        return itempick, found


    def OnItemNumber(self, event, upc=None):
        msg = "*** Check Table for Item Number & fill Variables with data ***"
        
        itemNumber_name = 'inventory_itemNumber_txtctrl'
        focus = wx.FindWindowByName(itemNumber_name).SetFocus()
        ItemNumberd = wx.FindWindowByName(itemNumber_name).GetCtrl().upper().strip()
        wx.FindWindowByName(itemNumber_name).SetCtrl(ItemNumberd)
        
        
        self.itempick, found = self.ItemLookup(ItemNumberd, itemNumber_name)
        #       
       
        
        
        if found is False:
            wx.CallAfter(self.OnItemNumber, event='')
            
        
        if self.itempick:
            wx.FindWindowByName('inventory_itemNumber_txtctrl').SetCtrl(str(self.itempick).strip())
            
            
            genOptions_load_list = [('genOptions_department_combobox',
                                        'item_options', 'department'),
                                    ('genOptions_category_combobox',
                                        'item_options', 'category'),
                                    ('genOptions_subcategory_combobox',
                                        'item_options', 'subcategory'),
                                    ('genOptions_location_combobox',
                                        'item_options', 'location'),
                                    ('genOptions_glpost_txtctrl',   
                                        'item_options', 'postacct'),
                                    ('genOptions_unittype_combobox',
                                        'item_options', 'unit_type'),
                                    ('genOptions_itemType_radiobox',
                                        'item_options', 'item_type'),
                                    ('genOptions_agepopup_numctrl',
                                        'item_options', 'agepopup'),
                                    ('genOptions_POSoptions_radiobox',
                                        'item_options', 'posoptions'),
                                    ('genOptions_units_in_package_numctrl',
                                        'item_options', 'unitsinpackage'),
                                    ('genOptions_foodStampExempt_checkbox',
                                        'item_options', 'foodstampexempt'),
                                    ('genOptions_loyaltyExempt_checkbox',
                                        'item_options', 'loyaltyexempt'),
                                    ('genOptions_consignment_checkbox',
                                        'item_options', 'consignment'),
                                    ('genOptions_partNumber_txtctrl',
                                        'item_detailed', 'part_num'),
                                    ('genOptions_oemNumber_txtctrl',
                                        'item_detailed', 'oempart_num'),
                                    ('genOptions_deactivated_checkbox',
                                        'item_options', 'deactivated'),
                                    ('genOptions_aisleNums_combobox',
                                        'item_options', 'aisle_num'),
                                    ('genOptions_extraPlaces_combobox',
                                        'item_options', 'extra_places'),
                                    ('genOptions_sectionNums_combobox',
                                        'item_options', 'section_num'),
                                    ('inventory_itemDescription_txtctrl',
                                        'item_detailed', 'description'),
                                    ('genOptions_kitNumber_txtctrl',
                                        'item_detailed', 'kit_num'),
                                    ('genOptions_kitPieces_numctrl',
                                        'item_detailed', 'kit_pieces')]

        for name, table, column_header in genOptions_load_list:
            query = '''SELECT {0} 
                       FROM {1} 
                       WHERE upc=(?)'''.format(column_header,table)
            
            data = (self.itempick,)
            returnd = HUD.SQConnect(query, data).ONE()
            pout.v(f'Name :{name} ; returnd : {returnd}') 
            
            a = wx.FindWindowByName(name).ReturndSet(returnd,0)
            

        details_load_list = ['details_altlookup_listbox',
                             'details_donotdiscount_checkbox',
                             'details_taxlvl_1_checkbox',
                             'details_taxlvl_2_checkbox',
                             'details_taxlvl_3_checkbox',
                             'details_taxlvl_4_checkbox',
                             'details_taxlvl_never_checkbox',
                             'details_taxoverride_numctrl',
                             'details_avgcost_numctrl',
                             'details_lastcost_numctrl',
                             'details_buy_numctrl',
                             'details_get_numctrl',
                             'details_saleDateBegin_datectrl',
                             'details_saleDateEnd_datectrl',
                             'details_saleTimeBegin_timectrl',
                             'details_saleTimeEnd_timectrl',
                             'inv_details_orderctrl_grid']

        for name in details_load_list:
            item = wx.FindWindowByName(name)
            pout.b(name)
            item.OnLoad(whereField='upc', whereValue=self.itempick)
            
        

        details2_load_list = [('details2_creditbookExempt_checkbox', 'item_detailed2','credit_book_exempt'),
                              ('details2_deleteWhenOut_checkbox', 'item_detailed2','delete_when_out'),
                              ('details2_onHand_numctrl','item_detailed', 'quantity_on_hand'),
                              ('details2_committed_numctrl','item_detailed', 'quantity_committed'),
                              ('details2_onLayaway_numctrl','item_detailed', 'quantity_on_layaway'),
                              ('details2_lastSale_datectrl','item_detailed2', 'last_saledate'),
                              ('details2_lastReturn_datectrl','item_detailed2', 'last_returndate'),
                              ('details2_lastMaint_datectrl','item_detailed2', 'maintdate'),
                              ('details2_added_datectrl','item_detailed2', 'added_date'),
                              ('details2_commissionOverride_checkbox', 'item_detailed2','override_commission'),
                              ('details2_commissionOverride_numctrl', 'item_detailed2','over_commission'),
                              ('details2_commissionFixedAmt_numctrl', 'item_detailed2','over_fixd_comm'),
                              ('details2_casebreaknum_txtctrl', 'item_detailed2','case_break_num'),
                              ('details2_subitem_checkbox','item_detailed2', 'substituteyn'),
                              ('details2_subitem_txtctrl','item_detailed2', 'substitute_num'),
                              ('details2_storeloc_txtctrl','item_detailed2', 'location'),
                              ('inv_posSalesLinks_poslinks_grid','item_sales_links', 'sales_links'),
                              ('notes_notes_txtctrl','item_notes','notes')]
                            #   ('details2_weight_numctrl','item_detailed2', 'weight'),
                            #   ('details2_tareweight_numctrl','item_detailed2', 'tare_weight'),

        for name,table,column_header in details2_load_list:
            

            query = 'SELECT {0} FROM {1} WHERE upc=(?)'.format(column_header,table)
            data = (self.itempick,)
            returnd = HUD.SQConnect(query, data).ONE()
            a = wx.FindWindowByName(name).ReturndSet(returnd,0)

    #--- Alt Lookups ----#
        # a = wx.FindWindowByName('PageAltLookups')
        # a.OnLoad()
        
    #---- Vendor ----#
        for numvend in range(1,7):
            tab = wx.FindWindowByName('Vendor{}DataTab'.format(numvend))
            tab.OnLoad()
            
        

   #---- Customer Info ----#
        item_box_list = [('custinst_Info_custinstruct_txtctrl', 'item_cust_instructions', 'info_box'),
                         ('custinst_ReturnPolicy_custinstruct_txtctrl', 'item_cust_instructions', 'return_box'),
                         ('custinst_Warranty_custinstruct_txtctrl', 'item_cust_instructions','warranty_box'),
                         ('custinst_Info_printOptions_radiobox', 'item_cust_instructions','print_info_options'),
                         ('custinst_ReturnPolicy_printOptions_radiobox','item_cust_instructions','print_return_options'),
                         ('custinst_Warranty_printOptions_radiobox','item_cust_instructions','print_warranty_options'),
                         ('custinst_Info_stdDialog_combobox', 'item_cust_instructions','info_dialog'),
                         ('custinst_Return_stdDialog_combobox','item_cust_instructions','return_dialog'),
                         ('custinst_Warranty_stdDialog_combobox','item_cust_instructions','warranty_dialog')]

        for name, table, field in item_box_list:
            query = '''SELECT {}
                       FROM {}
                       WHERE upc=(?)'''.format(field, table)
            data = (self.itempick,)

            returnd = HUD.SQConnect(query, data).ONE()
            
            ret = VarOps().CheckNone(returnd)
            wx.FindWindowByName(name).SetCtrl(ret)
        
#----------- Cost Grid Load
        HUD.QueryOps().CheckEntryExist('upc', self.itempick.upper().strip(), ['item_retails'])
        
        grid = wx.FindWindowByName('inv_details_cost_grid')
        grid.Load(upc=self.itempick)
                
#--------         


    # def MarginUpdate(self, avg_cost, retail, unit, debug=False):
    #     ''' Readjust Margin in margin Column according to avg_cost '''
    #     actual_retail = Decimal(retail)/Decimal(unit)
    #     gross_profit = Decimal(actual_retail) - Decimal(avg_cost)
    #     deci_margin = Decimal(gross_profit) / Decimal(actual_retail)
    #     perc_margin = Decimal(deci_margin) * Decimal(100)
    #     percentage_margin = RO.DoRound(perc_margin, '1.000')
    #     return percentage_margin
   
   


#EndSetVariables



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
