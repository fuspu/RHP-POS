
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
from controls import RH_OLV, RH_Button, RH_ListBox, GridOps, Themes, RH_Icon, LoadSaveList, IconList, RH_CheckBox, RH_TextCtrl, RH_FilePickerCtrl, RH_MTextCtrl, RH_RadioBox
from controls import tSizer, LoadSaveDict
from dialogs import PasswordDialog
from events import EventOps
from decimal import Decimal, ROUND_HALF_UP
import wx.lib.inspection
from db_ops import SQConnect, QueryOps, LookupDB, GetSQLFile
from panels import AltLookup, Tax_Table_Grid
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

        # name='invMaint_zone_txtctrl'
        # self.aisleNums_nc = RH_MTextCtrl(self, -1, name=name, mask='#{4}')
        # self.aisleNums_nc.tableName = 'zone'
        # self.aisleNums_nc.fieldName = 'zone'
        # tS = tSizer(self, text='Zone', ctrl=self.aisleNums_nc)
        # self.LSL.Add(self.aisleNums_nc)
        # level2Sizer.Add(tS, 0, wx.ALL, 3)
        
        # name='invMaint_sectionNums_txtctrl'
        # self.sectionNums_nc = RH_MTextCtrl(self, -1, name=name, mask='#{4}')
        # self.sectionNums_nc.tableName = 'organizations'
        # self.sectionNums_nc.fieldName = 'num_of_sections'
        # self.LSL.Add(self.sectionNums_nc)
        # tS = tSizer(self, text='# of Sections', ctrl=self.sectionNums_nc)
        # level2Sizer.Add(tS, 0, wx.ALL, 3)
        
        MainSizer.Add(level1Sizer, 0, wx.ALL, 3)
        MainSizer.Add(level2Sizer, 0, wx.ALL, 3)
        MainSizer.Add(level3Sizer, 0, wx.ALL, 3)
        
        self.SetSizer(MainSizer)
        self.Layout()
        
        wx.CallAfter(self.OnLoad, event='')        
    
            
    def OnLoad(self, event):
        load_list = [(self.dept_lb, 'organizations', 'id'),
                     (self.cat_lb, 'category', 'id'),
                     (self.subcat_lb, 'subcategory', 'id'),
                     (self.material_lb, 'material', 'id'),
                     (self.location_lb, 'location', 'id'),
                     (self.zone_lb, 'zone', 'id'),
                     (self.unit_lb, 'unittype', 'id'),]
        
        for ctrl, tablename, fieldname in load_list:
            ctrl.OnLoad('')
            
        # for item in self.LSL.Get():
        #     #item = wx.FindWindowByName(name)
        #     item.OnLoad('')
            
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
            val = json.dumps(value)
            pout.v(value)
            pout.v(val)
            for i in value:
                q = f'UPDATE organizations SET {fieldname}=? WHERE abuser=?'
                d = (val, 'rhp',)
                pout.v(q)
                d = (i,)
                pout.v(d)
                r = SQConnect(q, d, './db/SUPPORT.sql').ONE()
                pout.v(r)

            
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

class GeneralMarginTab(wx.Panel):
    def __init__(self, parent, debug=False):
        """MarginGeneral Details Tab for the Inventory"""
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.SetName('MaintInvPricingMarginTab_GeneralMarginTab')


class MarginTab(wx.Panel):
    def __init__(self, parent, debug=False):
        """MarginGeneral Details Tab for the Inventory"""
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.SetName('MaintInvPricingTab_MarginTab')
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetName('MarginTab')
        
        self.rbox = RH_RadioBox(self, -1, 
                           choices=['General','By Cost','By Category'],
                           name='generalMargin_control_rbox', 
                           label='Figuring Initial Starting Margin')
        self.rbox.tableName = 'item_margin'
        self.rbox.fieldName = 'starting_margin_control'
        self.rbox.Bind(wx.EVT_RADIOBOX, self.onBoxChoice)
        
        self.nb = wx.Notebook(self, wx.ID_ANY,name='MarginTab_Notebook')
        self.nb.AddPage(GeneralMarginTab(self.nb), "General")
        self.nb.AddPage(ByCostTab(self.nb), "By Cost")
        self.nb.AddPage(ByCategoryTab(self.nb), "By Category")
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
        listd = self.LSL.To_Dict()
        q,d, sqlfile = self.LSL.UpdateQD(listd['basic_store_info']['selects'], 'store_num')
        r = SQConnect(q, d, sqlfile).ONE()



        # sqlfile = self.storenum_tc.sqlfile
        # storenumd = self.storenum_tc.GetCtrl()
        # named = self.storename_tc.GetCtrl()
        # addr1 = self.address1_tc.GetCtrl()
        # addr2 = self.address2_tc.GetCtrl()
        # cityd = self.city_tc.GetCtrl()
        # stated = self.state_tc.GetCtrl()
        # zipd = self.zipcode_tc.GetCtrl()
        # phon1d = self.phone1_tc.GetCtrl()
        # phon2d = self.phone2_tc.GetCtrl()
        # faxd = self.fax_tc.GetCtrl()
        # emaild = self.email_tc.GetCtrl()
        # sited = self.website_tc.GetCtrl()
        # logod = self.filepicker_c.GetCtrl()

        q = '''UPDATE basic_store_info 
               SET name=?
               WHERE store_num=?'''
        # address1=?, address2=?, city=?, state=?, zipcode=?, phone1=?, phone2=?, fax=?, email=?, website=?, logo=?
        pout.v(q)
        # addr1, addr2, cityd, stated, zipd, phon1d, phon2d, faxd, emaild, sited, logod,
        d = [named, storenumd,]
        pout.v(d)
        r = SQConnect(q, d, sqlfile).ONE()
        pout.v(r)


    
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
