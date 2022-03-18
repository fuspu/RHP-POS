import wx
import wx.grid as gridlib
import sys,re
import faulthandler
import json
import time
import numpy
from wx.lib.masked import NumCtrl, Ctrl, TextCtrl
from controls import RH_TextCtrl, RH_CheckBox, RH_ComboBox, RH_OLV, RH_Button, RH_ListBox, GridOps, Themes
import datetime
import pout
from utils import IconPanel, EventOps
from decimal import Decimal, ROUND_HALF_UP
from db_ops import SQConnect





class PasswordDialog(wx.Dialog):
    def __init__(self, operator='clerk', debug=False):
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
        super(PasswordDialog, self).__init__(parent=None, title='Authorization?',size=(200,90),style=style)
        
        self.op = operator.upper()
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        row1Sizer = wx.BoxSizer(wx.VERTICAL)
        row2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        ctrl = RH_TextCtrl(self, -1, 
                           name='password_txtctrl', 
                           size=(125,-1), 
                           style=wx.TE_PASSWORD|wx.TE_PROCESS_ENTER)
        
        ctrl.Bind(wx.EVT_TEXT_ENTER, self.OnPassword)
        ctrl.SetFocus()
        
        row1Sizer.Add(ctrl, 0, wx.ALL | wx.ALIGN_CENTER, 3)
        
        btn_list = [('Cancel', 'password_cancel_button')]
        
        for label, name in btn_list:
            btn = RH_Button(self, -1, label=label, name=name)
            btn.Bind(wx.EVT_BUTTON, self.ButtonAction)
            
            row2Sizer.Add(btn, 0, wx.ALL|wx.ALIGN_CENTER, 3)
            
        
    
        MainSizer.Add(row1Sizer, 0, wx.ALL | wx.ALIGN_CENTER, 3)
        MainSizer.Add(row2Sizer, 0, wx.ALL| wx.ALIGN_CENTER, 3)
        
        self.SetSizer(MainSizer, 0)
        self.Layout()
    
   # def Operator(self, auth):
   #     self.op = auth
        
    
    def OnPassword(self, event):
        obj = event.GetEventObject()
        named = obj.GetName()
        value = obj.GetValue().strip().lower()
        admin = LookupDB('passwords').Specific('rhp','abuser','admin_key')[0].lower()
        print(f'Admin Key : {admin}')
        manager = LookupDB('passwords').Specific('rhp','abuser','manager_key')[0].lower()
        print(f'Manager Key : {manager}')
        clerk = LookupDB('passwords').Specific('rhp','abuser','clerk_key')[0].lower()
        print(f'Clerk Key : {clerk}')
        self.passwordOK = False
        
        if self.op == 'CLERK':
            if value == manager or value == admin or value == clerk:
                self.passwordOK = True 
              
        if self.op == 'MANAGER':
            if value == manager or value == admin:
                self.passwordOK = True        
        
        if self.op == 'ADMIN':
            if value == admin:
                self.passwordOK = True

        if self.passwordOK is False:
            #box = wx.FindWindowByName('password_txtctrl')
            wx.FindWindowByName('password_txtctrl').SetCtrl('')
        
        if self.passwordOK is True:
            self.Close()

            
    def ButtonAction(self, event):
        obj = event.GetEventObject()
        name = obj.GetName()
        self.passwordOK = False
        
        if 'cancel' in name:
            self.Close()
            

                
class DiscountDialog(wx.Dialog):
    def __init__(self, debug=False):
        super(DiscountDialog, self).__init__(*args,**kw)
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        row0Sizer = wx.BoxSizer(wx.HORIZONTAL)
        row1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        row2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        rb = wx.RadioBox(self, -1, 
                         choices=[], 
                         name='discounts_choices_radiobox', 
                         label='Discount Types',
                         style=wx.RA_SPECIFY_COLS) 
        
        row0Sizer.Add(rb, 0, wx.ALL, 3)                           
        ctrl = RH_TextCtrl(self, -1,
                           name='discount_disc_textctrl',
                           style=wx.TE_RIGHT)
        ctrl.Bind(wx.EVT_KILL_FOCUS, EventOps().OnNumbersOnly)
        
        ctrl.SetFocus()                     
        txt = wx.StaticText(self, -1, 
                            label='%')
        
        font = wx.Font(wx.FontInfo(16))
        txt.SetFont(font)
                                   
        row1Sizer.Add(ctrl,0,wx.ALL|wx.CENTER, 3) 
        row1Sizer.Add(txt,0)
        button_list = [('discount_ok_button','&OK',self.OnOK),
                       ('discount_cancel_button','&Cancel',self.OnCancel)]                       
        
        for name, label, hdlr in button_list:
            btn = RH_Button(self, -1, label=label, name=name)
            btn.Bind(wx.EVT_BUTTON, hdlr)
            row2Sizer.Add(btn,0,wx.ALL, 5)
        
        MainSizer.Add(row0Sizer, 0, wx.ALL|wx.CENTER, 3)                          
        MainSizer.Add(row1Sizer, 0,wx.ALL|wx.CENTER, 3)
        MainSizer.Add(row2Sizer, 0, wx.ALL|wx.CENTER, 3)
        
        self.SetSizer(MainSizer, 0)        
        self.Layout()
    
        wx.CallAfter(self.OnLoad, event='')
        
    def OnLoad(self, event):
        
        query = 'SELECT name, percent FROM discount_options'
        data = ''
        returnd = SQConnect(query,data).ALL()
        choices = []
         
        for name, percent in returnd:
            titl = '{} : {}%'.format(name, percent)
            choices.append(titl)
        
        
            
        rb = wx.FindWindowByName('discounts_choices_radiobox')
        for idx, item in enumerate(choices): 
            print('idx : {} ; item : {} '.format(idx,item))
            rb.SetString(idx, item)
           
    def OnOK(self,event):
        self.discountamt = wx.FindWindowByName('discount_disc_textctrl').GetCtrl()
        self.Close()
        
    def OnCancel(self, event):
        self.discountamt = wx.FindWindowByName('discount_disc_textctrl').GetCtrl()
        self.Close()




####---- Flash Item Add
class FlashAddInventory(wx.Dialog):
    def __init__(self, *args, **kw): 
        super(FlashAddInventory, self).__init__(*args, **kw) 
        
        obj = self.GetParent()
        print('\033[92m OBJ : {0} \033[0m'.format(obj))
         
        # 8 Rows
        FlashCreateSizer = wx.BoxSizer(wx.VERTICAL)
        row1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        row1_list = (('Item Number','flashadd_itemNumber_txtctrl',250),('Description','flashadd_itemDescription_txtctrl',500))
        for label,name,sized in row1_list:
            box = wx.StaticBox(self, -1, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            if 'txtctrl' in name:
                if 'itemNumber' in name:
                    ctrl = masked.TextCtrl(self, -1, name=name, size=(sized, -1), formatcodes="!")
                    ctrl.Bind(wx.EVT_KEY_DOWN, self.onCatchKey)
                else:
                    ctrl = RH_TextCtrl(self, -1, name=name, size=(sized, -1))
                    ctrl.Bind(wx.EVT_KILL_FOCUS, EventOps().CheckMeasurements)
            if 'agepopup' in name:
                ctrl = masked.NumCtrl(self, -1, name=name, value='00', integerWidth=2, fractionWidth=0)
            if 'agepopup' in name:
                boxSizer.Add(ctrl, 0, wx.ALL, 20)            
            else:
                boxSizer.Add(ctrl, 0, wx.ALL, 3)
            if 'itemNumber' in name:
                ctrl.SetFocus()
            row1Sizer.Add(boxSizer, 0, wx.ALL, 3)
             
        
        row2Sizer = wx.BoxSizer(wx.HORIZONTAL)

        
        row2_list = [('Unit Cost','flashadd_avgcost_numctrl',50),
                     ('Department','flashadd_department_combobox',150),('Category','flashadd_category_combobox',150),
                     ('Subcategory','flashadd_subCategory_combobox',150),('Weight','flashadd_weight_numctrl',75),
                     ('Tare Weight','flashadd_tareWeight_numctrl',75)]
        for label,name,sized in row2_list:
            box = wx.StaticBox(self, -1, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            if 'numctrl' in name:
                ctrl = masked.NumCtrl(self, -1, value=0, name=name, integerWidth=9, fractionWidth=3)
            if 'combobox' in name:
                ctrl = masked.ComboBox(self, -1, name=name, choices=[], size=(sized,-1))
            boxSizer.Add(ctrl, 0, wx.ALL,3)
            row2Sizer.Add(boxSizer, 0, wx.ALL, 3)                     
        
        
        row3Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        query = "SELECT name,scheme_list,reduce_by from item_pricing_schemes"
        data = ''
        returnd = SQConnect(query, data).ALL()
        
        
        
        priceschema_list = returnd
        
        box = wx.StaticBox(self, label="Pricing\nSchemes")
        boxSizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        boxSizer.Add((20,20), 0)
        xx=0  
        btn = RH_Button(self, id=wx.ID_ANY, label="RESET", name="details_pricescema_RESET_button")
        btn.Bind(wx.EVT_BUTTON, self.OnPriceSchemes)        
        boxSizer.Add(btn, 0)
               
        for label, scheme_list, reduce_by in priceschema_list:
            btn = RH_Button(self, id=wx.ID_ANY, label=label, name=scheme_list)
            btn.Bind(wx.EVT_BUTTON, self.OnPriceSchemes)        
            boxSizer.Add(btn, 0)
            xx+=1            
        
                
        row3Sizer.Add(boxSizer, 0)
      
        
        grid = Retail_Grid(self, name="flashadd_cost_grid")
         
        row3Sizer.Add(grid, 0)
        
        row3bSizer = wx.BoxSizer(wx.VERTICAL)
        
        itemType_choices = ['Controlled','Non-Controlled','Matrixed','BOM','Tag Along','Serial No. Track','Mfg Coupon']
        posOptions_choices = ['Prompt for Quantity','Assume 1 Sold','Prompt for price - Quantity Calculated','Prompt for scale']
        
        row3_list = [('Item Type','flashadd_itemType_radiobox',itemType_choices),
                     ('POS Options','flashadd_posOptions_radiobox', posOptions_choices)]
        for label,name,choices in row3_list:
            ctrl = wx.RadioBox(self, -1, label=label, name=name, choices=choices, style=wx.RA_SPECIFY_ROWS)
            row3bSizer.Add(ctrl, 0, wx.ALL, 3)
        
        row3Sizer.Add(row3bSizer, 0, wx.ALL, 3)        
            
        row4Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
         
        #ctrl = wx.RadioBox(self, -1, label='POS Options', name='flashadd_posOptions_radiobox', choices=posOptions_choices)
        #row4Sizer.Add(ctrl, 0, wx.ALL, 3)
        
        row5Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
                      
        row5_list = [('QOH','flashadd_quantityOnHand_numctrl',0),('Units in Package','flashadd_unitsInPackage_numctrl',1),
                     ('Override Tax Rate','flashadd_overrideTaxRate_numctrl',0)]
        
        for label, name, sized in row5_list:
            box = wx.StaticBox(self, -1, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            if 'numctrl' in name:
                if re.search('(quantity|units)',name,re.I):
                    ctrl = masked.NumCtrl(self, -1, value=sized, name=name, integerWidth=5, fractionWidth=0)
                if 'override' in name:
                    ctrl = masked.NumCtrl(self, -1, value=0, name=name, integerWidth=3, fractionWidth=3)
            boxSizer.Add(ctrl, 0, wx.ALL, 7)
            row5Sizer.Add(boxSizer, 0, wx.ALL, 3)
            
        taxExemptions_list = [('1','flashadd_taxlvl1_checkbox'),('2','flashadd_taxlvl2_checkbox'),('3','flashadd_taxlvl3_checkbox'),
                             ('4','flashadd_taxlvl4_checkbox'),('Never','flashadd_taxlvlNever_checkbox')]
        
        box = wx.StaticBox(self, -1, label='Tax Level Exemptions')
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        for labeld, named in taxExemptions_list:
            ctrl = RH_CheckBox(self, label=labeld, name=named)
            boxSizer.Add(ctrl, 0, wx.ALL, 3)
        
        row5Sizer.Add(boxSizer, 0, wx.ALL, 3)                                         
        
       
        row6Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        row6_list = [('Vendor Number','flashadd_vendorNum_txtctrl',40),
                     ('Vendor Name','flashadd_vendorName_txtctrl',150)]
        
        box = wx.StaticBox(self, -1, label='Order Number')
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        ctrl = masked.TextCtrl(self, -1, name='flashadd_orderNumber_txtctrl', size=(90,-1),formatcodes='!')
        boxSizer.Add(ctrl, 0, wx.ALL, 3)
        row6Sizer.Add(boxSizer, 0, wx.ALL, 3)
        row5Sizer.Add(row6Sizer, 0,wx.ALL, 3)
        
        box = wx.StaticBox(self, -1, label='Vendor Info')
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        for label, name, sized in row6_list:
            if 'vendorName' in name:
                vendFind = wx.BitmapButton(self, -1, wx.Bitmap(ButtonOps().Icons('Find', 16)))
                vendFind.Bind(wx.EVT_BUTTON, self.onFindVendor)
                boxSizer.Add(vendFind, 0, wx.ALL, 3)
            
            ctrl = RH_TextCtrl(self, -1, name=name, size=(sized,-1))
            if 'vendorName' in name:
                ctrl.SetEditable(False)
                
            boxSizer.Add(ctrl, 0, wx.ALL, 3)
            
        row6Sizer.Add(boxSizer, 0, wx.ALL, 3)
        
                
        row8Sizer = wx.BoxSizer(wx.HORIZONTAL)

        row8_list = [('&ACCEPT','flashadd_accept_button',self.OnAccept),('&CANCEL','flashadd_cancel_button',self.OnCancel)]
        for label, name, hndlr in row8_list:
            ctrl = RH_Button(self, label=label, name=name, size=(90,40))
            ctrl.Bind(wx.EVT_BUTTON, hndlr)
            if 'cancel' in name:
                row8Sizer.Add((80,10),0)
                
            row8Sizer.Add(ctrl, 0, wx.ALL, 3)
            
        sizer_list = [row1Sizer, row2Sizer, row3Sizer, row4Sizer, row5Sizer,  row8Sizer]
        for sizer in sizer_list :
            FlashCreateSizer.Add((5,10),0, wx.ALL, )
            FlashCreateSizer.Add(sizer, 0, wx.ALL|wx.ALIGN_CENTER, 3)
            
       
        self.SetSizer(FlashCreateSizer,0)
        # order = ('flashadd_itemNumber__txtctrl','flashadd_itemDescription_txtctrl','flashadd_department_combobox','flashadd_category_combobox','flashadd_subCategory_combobox')
        # for i in range(len(order) - 1):
        #     ctrl1 = wx.FindWindowByName(order[i])
        #     ctrl2 = wx.FindWindowByName(order[i+1])
            
        #     ctrl2.MoveAfterInTabOrder(ctrl1)
    
        wx.CallAfter(self.OnLoad, event='')
    
    def onCatchKey(self, event):
       
        keycode = event.GetKeyCode()
        if keycode in [wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER, wx.WXK_TAB]:
            self.CheckExists(event=None)
            event.EventObject.Navigate()

        event.Skip()

    
    def CheckExists(self, event):
        name = 'flashadd_itemNumber_txtctrl'
        upc = wx.FindWindowByName(name).GetCtrl()
        
        query = 'SELECT upc, description FROM item_detailed WHERE upc=(?)'
        data = (upc,)
        returnd = SQConnect(query, data).ONE()
        
        if returnd is not None:
            wx.MessageBox('Item Number already in use','Add Item', wx.OK)
            self.Close()
        
        item = wx.FindWindowByName('flashadd_itemDescription_txtctrl').SetFocus()    
        
    
    def OnPriceSchemes(self, event):
       
        grid = wx.FindWindowByName('flashadd_cost_grid')
        WhichScheme = event.GetEventObject()
        
        Scheme_Name = WhichScheme.GetLabel()    
        Scheme_List = WhichScheme.GetName().split("-")          #['1','7','15']
        if Scheme_Name == 'RESET':
            
            reset_list = [('Unit','1'),('Price','0.00'),('Margin %','0.0000')]
            for xx in range(grid.GetNumberRows()):
                fillgrid = GridOps(grid.GetName()).FillGrid(reset_list,row=xx)
                
        else:
            
            if 'PK' in Scheme_List:
                (each, pack, bulk) = Scheme_List
                
                UIPctrl = wx.FindWindowByName('flashadd_unitsInPackage_numctrl').GetValue()
                if not UIPctrl:
                    UIPctrl = 1
                if Decimal(UIPctrl) == Decimal(each):
                    UIPctrl = Decimal(each)*2    
                Bulkd = Decimal(UIPctrl) * Decimal(bulk.strip('X'))
                
                Scheme_List = str(each),str(UIPctrl),str(Bulkd)
                        
            avgCostL = wx.FindWindowByName('flashadd_avgcost_numctrl').GetValue()
            
            query = "SELECT reduce_by from item_pricing_schemes WHERE name=?"
            data = (Scheme_Name,)
            returnd = SQConnect(query, data).ONE()
            Reduceby = returnd
            
            startingMargin_L = '50'
            
            if Decimal(avgCostL) == 0:
                wx.MessageBox('Average Cost Not Set','Info',wx.OK)
                return    
            Schemed = Pricing('C',Scheme_List,Reduceby,avgCostL,startingMargin_L,avgCostL)
            #Debugger('{0}\n Price {1}\n Size of {2}'.format('** Schemed Test Run **',Schemed.Scheme(),len(Schemed.Scheme())))
            schemeLen = len(Schemed.Scheme())
            priceScheme_dict = Schemed.Scheme()
            
            xx = 0
        
            for key in Scheme_List:
                setList = [('Unit',key),('Price',str(Decimal(priceScheme_dict[key][0]))),
                           ('Margin %',str(Decimal(priceScheme_dict[key][1])))]
                fillGrid = GridOps(grid.GetName()).FillGrid(setList,row=xx)           
                xx += 1

    
    
    def OnCellChange(self, event):
       
        
        
        obj = event.GetEventObject()
        named = obj.GetName()
        row = event.GetRow()
        col = event.GetCol()
        
        grid = wx.FindWindowByName(named)
        colname = grid.GetColLabelValue(col)
        grid.Refresh()
        
        if 'details_cost_grid' in named:
            raw_value = grid.GetCellValue(row,col).strip()
            # numeric check
            if all(x in '0123456789.+-' for x in raw_value):
                # convert to float and limit to 2 decimals
                value = Decimal(raw_value)
                if colname == 'Unit':
                    valued = RetailOps().DoRound(value,'1')
                else:
                    valued = RetailOps().DoRound(value,'1.00')
                grid.SetCellValue(row,col,str(valued))
            else:
                basic_list = ['1','$0.00','Margin','0.0000']
                grid.SetCellValue(row,col,basic_list[col])
                GridOps(grid.GetName()).GridFocusNGo(row, col)
                return
            
        #
        
        avgcost = wx.FindWindowByName('flashadd_avgcost_numctrl').GetValue()
        
        
        for yy in range(grid.GetNumberCols()):
            header = grid.GetColLabelValue(yy)
            if 'Unit' in header:
                unit = grid.GetCellValue(row,yy)
            if 'Markup %' in header:
                calcMargin = grid.GetCellValue(row,yy)
            if 'Price' in header:
                retail_from = grid.GetCellValue(row,yy)
                  
            
        if colname == 'Markup %':
            newretail_almost = RetailOps().DoMargin(avgcost,calcMargin,unit) 
            newretail = RetailOps().DoRound(newretail_almost,'1.00')
            newMargin = RetailOps().DoRound(calcMargin,'1.0000') 
            
            set_values = [('Price',newretail),('Markup %',newMargin)]
            
            fillgrid = GridOps(grid.GetName()).FillGrid(set_valuesrow=row)
            
        if colname == 'Price':
            grossMargin = RetailOps().GetMargin(avgcost,retail_from,unit)
            Margindot4 = RetailOps().DoRound(grossMargin,'1.0000') 
            
            grid.SetCellValue(row,3,str(Margindot4))
        
        if colname == 'Unit':
            
            newretail_almost = RetailOps().DoMargin(avgcost,calcMargin,unit)
            newretail = RetailOps().DoRound(newretail_almost, '1.00')
            
            grid.SetCellValue(row,1,str(newretail))
        
        
    def onFindVendor(self, event):
       
        pass
        
    
    def OnAccept(self, event):
       
        ItemNumberd = wx.FindWindowByName('flashadd_itemNumber_txtctrl').GetValue().upper().strip()
        
        table_list = ['item_options','item_detailed','item_detailed2','item_vendor_data','item_notes','item_sales_links','item_cust_instructions','item_options','item_history','item_retails']
        QueryOps().CheckEntryExist('upc',ItemNumberd,table_list)
        
        grid = wx.FindWindowByName('flashadd_cost_grid').OnSave(upc=ItemNumberd)
        
        flashadd_list = [('flashadd_itemDescription_txtctrl','item_detailed','description'),
                         ('flashadd_avgcost_numctrl','item_detailed','avg_cost'),
                         ('flashadd_department_combobox','item_options','department'),('flashadd_category_combobox','item_options','category'),
                         ('flashadd_subCategory_combobox','item_options','subcategory'),('flashadd_weight_numctrl','item_detailed2','weight'),
                         ('flashadd_itemType_radiobox','item_options','item_type'),('flashadd_tareWeight_numctrl','item_detailed2','tare_weight'),
                         ('flashadd_posOptions_radiobox','item_options','posoptions'),('flashadd_quantityOnHand_numctrl','item_detailed','quantity_on_hand'),
                         ('flashadd_unitsInPackage_numctrl','item_options','unitsinpackage'),('flashadd_overrideTaxRate_numctrl','item_detailed2','override_tax_rate'),
                         ('flashadd_taxlvl1_checkbox','item_detailed2','tax1'),('flashadd_taxlvl2_checkbox','item_detailed2','tax2'),
                         ('flashadd_taxlvl3_checkbox','item_detailed2','tax3'),('flashadd_taxlvl4_checkbox','item_detailed2','tax4'),
                         ('flashadd_taxlvlNever_checkbox','item_detailed2','tax_never'),('flashadd_vendorNum_txtctrl','item_vendor_data','vendor1_num'),
                         ('flashadd_orderNumber_txtctrl','item_vendor_data','vendor1_num')]
        #                 
        for name, table, column_header in flashadd_list:
            itemValue = wx.FindWindowByName(name).GetCtrl()
            if 'vendor_data' in table:
                vendor_set = ['vendor1','vendor2','vendor3','vendor4','vendor5','vendor6']
                vendor_info = {}
                    
                for numvend in vendor_set: 
                    vendorID = numvend
                    vendor_info[vendorID]={}
                
                    if vendorID == 'vendor1':
                        vendorOrderNum = wx.FindWindowByName('flashadd_orderNumber_txtctrl').GetValue()
                        vendorNum = wx.FindWindowByName('flashadd_vendorNum_txtctrl').GetValue()
                    else:
                        vendorOrderNum = ''
                        vendorNum = ''
                        
                    vendor_save_list = [(vendorNum,'vendor_num'),('','vendor_name'),
                                        ('','last_retail'),(vendorOrderNum,'order_num'),
                                        ('','last_units_ordered'),('','leadtime'),
                                        ('','minimum_order'),('','last_ordered'),
                                        ('','last_order_date'),('','outstanding')]
                    for vendvalue, vendkey in vendor_save_list:
                        vendor_info[vendorID][vendkey] = vendvalue
            
                itemValue = json.dumps(vendor_info)
            
                   
                
            
            
            RecordOps('item_detailed2').UpdateRecordDate('added_date','upc',ItemNumberd)
            
            query = 'UPDATE {0} SET {1}=? WHERE upc=?'.format(table, column_header)
            data = (itemValue,ItemNumberd,)
            call_db = SQConnect(query, data).ONE()
            
            
    
            self.itemPicked = ItemNumberd
            self.Close()
    
    
    
    def OnCancel(self, event):
       
        self.Close()
    
    def OnLoad(self, event):
       
        load_combobox_list = [('department','flashadd_department_combobox'),
                              ('category','flashadd_category_combobox'),
                              ('subcategory','flashadd_subCategory_combobox')]
        for field, name in load_combobox_list:
            query = "SELECT {0} FROM organizations WHERE abuser='rhp'".format(field)
            data = ''
            returnd = SQConnect(query, data).ALL()
            
            choice_list = []
            
            choice_list = returnd[0]
            item = wx.FindWindowByName(name).SetItems(choice_list)
            



class PayByDialog(wx.Dialog):  
    def __init__(self, parent, title, debug=False):
        super(PayByDialog, self).__init__(parent=parent, size=(500,500), title=title)
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
            
        if 'Cash' in title:
            btn_list = [('Give Change', 'paybyDialog_giveChange_btn', self.CashGiveChange),('Keep on Account','paybyDialog_keepOnAcct_btn', self.KeepOnAcct)]
            for label, name, hdlr in btn_list:
                btn = RH_Button(self, -1, label=label, name=name)
                btn.Bind(wx.EVT_BUTTON, hdlr)
                MainSizer.Add(btn, 0, wx.ALL|wx.ALIGN_CENTER, 25)        
        
        if 'Check' in title:
            ctrl_list = [('Check #','paybyDialog_checkNum_txtctrl')]
        
        if 'Card' in title:
            pass    

        
        self.SetSizer(MainSizer, 0)
        self.Layout()

    def CashGiveChange(self, event):
        pass
    
    def KeepOnAcct(self, event):
        pass
    
    
        
class CustLookupDialog(wx.Dialog):
    style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
    def __init__(self, parent, size=(1150,700), title="Customer Lookup"):
        super(CustLookupDialog, self).__init__(parent=parent, size=size, title=title)
        self.InitUI()
        
        
    def InitUI(self):
       
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        
        level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        lookup_list = [('First Name Lookup', self.OnSearchFName, 'fname_lookup_txtctrl1','Enter 2+ letters of the First Name Only without punctuation',),
                       ('Last Name Lookup', self.OnSearchLName, 'lname_lookup_txtctrl1','Enter 2+ letters of the Last Name Only without punctuation'),
                       ('Phone Lookup', self.OnSearchPhone, 'phone_lookup_txtctrl1','Enter Numbers Only, i.e. 3867752794'),
                       ('Street Name - Address Lookup', self.OnSearchAddress, 'address_lookup_txtctrl1', 'Enter Street Name Only')]
        
        for label,handlr,name,tooltip in lookup_list:
            box = wx.StaticBox(self, -1, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            
            if 'Phone Lookup' in label:
                lookup_txtctrl = RH_MTextCtrl(self, -1, name=name, size=(160,-1), mask='(###) ###-####', style=wx.TE_PROCESS_ENTER)
            else:    
                lookup_txtctrl = RH_TextCtrl(self, -1, name=name, size=(160,-1), style=wx.TE_PROCESS_ENTER)
            
            lookup_txtctrl.SetToolTip(wx.ToolTip(tooltip))
            lookup_txtctrl.Bind(wx.EVT_TEXT_ENTER, handlr)
            if 'First Name' in label:
                lookup_txtctrl.SetFocus()
            
            lookup_button = RH_Button(self, -1, label="Search")
            lookup_button.Bind(wx.EVT_BUTTON, handlr)
            
            boxSizer.Add(lookup_txtctrl, 0, wx.ALL, 3)
            boxSizer.Add(lookup_button, 0, wx.ALL, 3)
            
            level1Sizer.Add(boxSizer, 0, wx.ALL, 5)              
        
        level2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        lc = RH_OLV(self, -1, name='name_lc', size=(1100,500),style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        lc.SetColumns([
                    ColumnDefn('Account #','center',120,'acctNum'),
                    ColumnDefn('Name','left',290,'named'),
                    ColumnDefn('Address 1','left',280,'address1d'),
                    ColumnDefn('Address 2','left',160,'address2d'),
                    ColumnDefn('City','left',120,'cityd'),
                    ColumnDefn('State','left',80,'stated')
                    ])
        
        lc.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.LookupOnCellLeftClick)
               
        level2Sizer.Add(lc, 0)
        
        level3Sizer = wx.BoxSizer(wx.HORIZONTAL)
        numberofcust = wx.StaticText(self, -1, label='Number Here')
        
        return_count = QueryOps().QueryCheck('customer_basic_info')
        
        CustomerCount = "Number of Customers : {0}".format(return_count)
        numberofcust.SetLabel(CustomerCount)
        
       
        level3Sizer.Add(numberofcust, 0, wx.ALL|wx.EXPAND, 5)
        result_text = wx.StaticText(self, -1,label='',name='custLookup_result_text') 
       
        MainSizer.Add(level1Sizer, 0)
        MainSizer.Add(result_text, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        MainSizer.Add(level2Sizer, 0, wx.ALL|wx.ALIGN_CENTER,5)
        MainSizer.Add(level3Sizer, 1, wx.ALL|wx.EXPAND|wx.ALIGN_BOTTOM, 10)
        self.SetSizer(MainSizer, 0)
        self.Layout()
        
    def LookupOnCellLeftClick(self, evt):
       
        item_id,objText = EventOps().LCGetSelected(evt)
        self.itemPicked = objText
        
        if re.match('[A-Z0-9]',self.itemPicked,re.I):
            self.Close()
        
       
    def OnSearchFName(self, event):
       
        cell_color = Themes().GetColor('cell')
        
        fname = wx.FindWindowByName('fname_lookup_txtctrl1').GetCtrl()
        query = "SELECT cust_num,first_name,last_name,address_acct_num from customer_basic_info where first_name LIKE ?" 
        data = (fname,)
        returnd = SQConnect(query, data).ALL()
        pout.v(returnd)
        
        if returnd is None or len(returnd) == 0:
            wx.MessageBox('First Name Not Found.','Customer Lookup by First Name', wx.OK)
            return
            
        
        #returnd.sort(key=itemgetter(1))
        pout.v(f'A Customer : {returnd}')
        pout.v(returnd[0][1])
        
        
        
        results = 'Found {0} Record(s)'.format(len(returnd))
        item = wx.FindWindowByName('custLookup_result_text').SetCtrl(results)
        lc = wx.FindWindowByName('name_lc')
        lc.DeleteAllItems()
        xx=0  
        idx = 0
        cell_color = Themes('Customers').GetColor('cell')
            
        for row in returnd:
            pout.v(f'row : {row}')
            cust_numd, first_named, last_named, addr_acct_numd = row
            fullName = ''         
            if first_named:
                fullName += '{0} '.format(first_named)
            if last_named:
                fullName += '{0} '.format(last_named)    
                                
            
            startTime = datetime.datetime.now()
            
            address0 = address2 = city = state = ''
            if addr_acct_numd != '' or len(addr_acct_numd) > 0:
                # query = 'SELECT address0,address2,city,state FROM address_accounts WHERE addr_acct_num=?'
                # data = (addr_acct_numd,)
                # returnd = SQConnect(query, data).ONE()
                returnd = LookupDB('address_accounts').Specific(addr_acct_numd, 'addr_acct_num','address0, address2, city, state')
                try:
                    address0,address2,city,state = returnd
                except:
                    pout.v(f'Address Output : {returnd}')
            
            #MO().timeStages('Search single letter',startTime)
                
            
            setList = [(0,cust_numd),(1,fullName),(2,address0),(3,address2),(4,city),(5,state)]
            ListCtrl_Ops('name_lc').LCFill(setList,idx)
            xx += 1
        
        ListCtrl_Ops('name_lc').LCAlternateColor(xx)
                
        lc.SetFocus()    
        lc.Select(0)
    
    def OnSearchLName(self, event):
       
        cell_color = Themes().GetColor('cell')
        
        lname = wx.FindWindowByName('lname_lookup_txtctrl1').GetCtrl()
        query = "SELECT cust_num,first_name,last_name,address_acct_num from customer_basic_info where last_name like ?" 
        data = (lname,)
        returnd = SQConnect(query, data).ALL()
        #returnd = list(returnd)
        
        
        
        if returnd is None or len(returnd) == 0:
            wx.MessageBox('Last Name Not Found.','Customer Lookup by Last Name', wx.OK)
            return
        
        returnd.sort(key=itemgetter(2))
        
        results = 'Found {0} Record(s)'.format(returnd_count)
        item = wx.FindWindowByName('custLookup_result_text').SetLabel(results)
        lc = wx.FindWindowByName('name_lc')
        lc.DeleteAllItems()
        xx=0 
                  
        for cust_numd, first_named, last_named, addr_acct_numd, in returnd:
            fullName = ''         
            if first_named:
                fullName += '{0} '.format(first_named)
            if last_named:
                fullName += '{0} '.format(last_named)    
            
            address0 = address2 = city = state = ''
            if addr_acct_numd != '' or len(addr_acct_numd) > 0:
                query = 'SELECT address0,address2,city,state FROM address_accounts WHERE addr_acct_num=?'
                data = (addr_acct_numd,)
                returnd = SQConnect(query, data).ONE()
            
                (address0,address2,city,state) = returnd
            
                                
            set_list = [(0,cust_numd),(1,fullName),(2,address0),(3,address2),(4,city),(5,state)]
            ListCtrl_Ops('name_lc').LCFill(set_list, xx)
            xx += 1
        
        ListCtrl_Ops('name_lc').LCAlternateColor(xx)        
                
        lc.SetFocus()
        lc.Select(0)
        
    def OnSearchPhone(self, event):
       
        cell_color = Themes().GetColor('cell')
        
        ph_num = wx.FindWindowByName('phone_lookup_txtctrl1').GetValue()
        
        if not len(ph_num) >= 3:
            return
        
        query = "SELECT cust_num,first_name,last_name,address_acct_num from customer_basic_info where phone_numbers like ?" 
        data = ('%'+ph_num+'%',)
        returnd = SQConnect(query, data).ALL()
        
        
        if returnd is None or len(returnd) == 0:
            wx.MessageBox('Phone Number Not Found.','Customer Lookup by Phone Number', wx.OK)
            return

        returnd.sort()
        results = 'Found {0} Record(s)'.format(returnd_count)
        item = wx.FindWindowByName('custLookup_result_text').SetLabel(results)
        lc = wx.FindWindowByName('name_lc')
        lc.DeleteAllItems()    
        xx=0  
        
        for cust_numd, first_named, last_named, addr_acct_numd, in returnd:
            fullName = ''         
            if first_named:
                fullName += '{0} '.format(first_named)
            if last_named:
                fullName += '{0} '.format(last_named)    
            
            setList = [('Acct Number',cust_numd),('Name',fullName)]
            
            lc.InsertItem(xx, cust_numd)
            lc.SetItem(xx,1,fullName)
            search_list = [('address0','Address 1'),('address2','Address 2'),('city','City'),('state','State')]
            for field, title in search_list:
                address0 = address2 = city = state = ''
                if addr_acct_numd != '' or len(addr_acct_numd) > 0:
                    query = 'SELECT address0,address2,city,state FROM address_accounts WHERE addr_acct_num=?'
                    data = (addr_acct_numd,)
                    returnd = SQConnect(query, data).ONE()
                    
                    (address0,address2,city,state) = returnd
                
                setList = [(0,cust_numd),(1,fullName),(2,address0),(3,address2),(4, city),(5,state)]
                ListCtrl_Ops('name_lc').LCFill(setList,xx)
                
            xx += 1
        
        ListCtrl_Ops('name_lc').LCAlternateColor(xx)   
        lc.SetFocus()
        lc.Select(0)
        
    def OnSearchAddress(self, event):
        obj = event.GetEventObject()
        
        cell_color = Themes().GetColor('cell')
        
        addrname = obj.GetCtrl()
        if not len(addrname) >= 3:
            return
        
        query = "SELECT addr_acct_num from address_accounts where street_name like ?" 
        data = ('%'+addrname+'%',)
        call_db = SQConnect(query, data)
        returnd = call_db.ALL()
        
        if returnd is None or len(returnd) == 0:
            wx.MessageBox('Street Name Not Found.','Customer Lookup by Street Name', wx.OK)
            return
            
        results = 'Found {0} Record(s)'.format(returnd_count)
        item = wx.FindWindowByName('custLookup_result_text').SetLabel(results)
        lc = wx.FindWindowByName('name_lc')
        lc.DeleteAllItems()
        xx=0           
        dict_xx = 0
        cust_dict = {}
        
            
            
        for address_acct in returnd_list:
            
            query = "SELECT cust_num,first_name,last_name,address_acct_num from customer_basic_info WHERE address_acct_num=?"
            data = (address_acct,)
            cust_returnd = SQConnect(query, data).ALL()
            cust_returnd = list(cust_returnd)
            cust_returnd.sort(key=itemgetter(2))
            cust_returnd_count = len(cust_returnd)
            
            
            
            if cust_returnd_count == 0:
                continue
                
            (cust_numd, first_named, last_named, addr_acct_numd) = cust_returnd[0]
            fullName = ''         
            if first_named:
                fullName += '{0} '.format(first_named)
            if last_named:
                fullName += '{0} '.format(last_named)    
            
            setList = [('Acct Number',cust_numd),('Name',fullName)]
            #GO(grid.GetName()).FillGrid(setList,xx)
            address0 = address2 = city = state = ''
            if addr_acct_numd != '' or len(addr_acct_numd) > 0:
                query = 'SELECT address0,address2,city,state FROM address_accounts WHERE addr_acct_num=?'
                data = (addr_acct_numd,)
                returnd = SQConnect(query, data).ONE()
                (address0,address2,city,state) = returnd
                    
            setList = [(0,cust_numd),(1,fullName),(2,address0),(3,address2),(4,city),(5,state)]
            ListCtrl_Ops('name_lc').LCFill(setList,xx)
            xx += 1
        
        ListCtrl_Ops('name_lc').LCAlternateColor(xx)
                
        lc.SetFocus()
        lc.Select(0)
        
#-------------------------
##
## Item Inquiry
##
##-----------------------
class ItemInquiryDialog(wx.Dialog):
    def __init__(self, debug=False, *args,**kw):
        super(ItemInquiryDialog, self).__init__(size=(825,700),*args, **kw)
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        lookupSizer = wx.BoxSizer(wx.VERTICAL)
        
        basePath = os.path.dirname(os.path.realpath(__file__))+'/' 
        IconBar_list =[('FindButton',ButtonOps().Icons('Find'),self.OnFind),
                       ('ExitButton', ButtonOps().Icons('Exit'),self.OnExitButton)]
        
        IconBox = wx.StaticBox(self)
        
        IconBarSizer = wx.StaticBoxSizer(IconBox, wx.HORIZONTAL)        
        xx = 0        
        for name,iconloc,handler in IconBar_list:
            icon = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(iconloc), name=name, style=wx.BORDER_NONE)
            if 'Find' in name:
                randomId = wx.NewId()   
                self.Bind(wx.EVT_MENU, handler, id=randomId)
                accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('f'), randomId)])
                self.SetAcceleratorTable(accel_tbl)
               
            icon.Bind(wx.EVT_BUTTON, handler)
                    
            IconBarSizer.Add((80,1),0)
            if re.search('(Save|Delete|Add)',name,re.I):
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
        lookupSizer.Add(IconBarSizer, 0, wx.ALL|wx.EXPAND, 3)
        #lookupSizer.Add((10,10), 0)    
        
        level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        level1_list = [('Item Number', 'itemInq_itemNumber_txtctrl',230),('Description','itemInq_description_txtctrl',450)]
        for label,name,sized in level1_list:
            box = wx.StaticBox(self, -1, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            if 'itemNumber' in name:
                ctrl = RH_TextCtrl(self, -1, name=name, size=(sized, -1))
            
                ctrl.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
                
                ctrl.SetFocus()
            if 'description' in name:
                ctrl = RH_TextCtrl(self, -1, name=name, size=(sized, -1))
                ctrl.SetEditable(False)
            
            boxSizer.Add(ctrl, 0, wx.ALL, 3)
            level1Sizer.Add(boxSizer, 0, wx.ALL, 3)
        
        level2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        level2_list = [('Department','itemInq_department_txtctrl',125,'item_options','department'),
                       ('Category','itemInq_category_txtctrl',125,'item_options','category'),
                       ('Sub-Category','itemInq_subcategory_txtctrl',125,'item_options','subcategory'),
                       ('Material','itemInq_material_txtctrl',125,'item_options','location'),
                       ('Select\nF1','itemInq_selectF1_button',self.OnSelectF1,'',''),
                       ('Exit\nF2','itemInq_exitF2_button',self.OnExitButton,'','')]
        
        for label,name,sized,table,field in level2_list:
            if 'txtctrl' in name:
                box = wx.StaticBox(self, -1, label=label)
                boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
                ctrl = RH_TextCtrl(self, -1, name=name, size=(sized, 35), style=wx.TE_READONLY)
                ctrl.tableName = table
                ctrl.fieldName = field
                boxSizer.Add(ctrl, 0, wx.ALL, 3)
                level2Sizer.Add(boxSizer, 0)
            if 'button' in name:
                ctrl = RH_Button(self, -1, label=label, name=name)
                ctrl.Bind(wx.EVT_BUTTON, sized)                   
                level2Sizer.Add(ctrl, 1, wx.ALL|wx.EXPAND, 3)
        
        level3Sizer = wx.BoxSizer(wx.HORIZONTAL)
        level3_list = [('Qty On Hand','itemInq_onHand_numctrl','item_detailed','quantity_on_hand')]
        for label, name, table, field in level3_list:
            box = wx.StaticBox(self, -1, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            ctrl = RH_NumCtrl(self, -1, value=0, name=name, integerWidth=6, fractionWidth=2)
            ctrl.SetEditable(False)
            ctrl.tableName = table
            ctrl.fieldName = field
            boxSizer.Add(ctrl, 0)
            level3Sizer.Add(boxSizer, 0, wx.ALL, 3)
        
        level3Sizer.Add((150,10), 0)
        ctrl = RH_CheckBox(self, -1, label='Do Not Discount', name='itemInq_donotdiscount_checkbox')
        ctrl.Disable()
        level3Sizer.Add(ctrl, 0, wx.ALL|wx.RIGHT, 3)     
        
        level4Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        grid = Retail_Grid(self, name='itemInq_retailPrice_grid', formatted='nomargin')
            
        level4Sizer.Add(grid, 0, wx.ALL|wx.EXPAND, 20)
        
        grid = SalesTracker_Grid(self, name='itemInq_salesTracker_grid')
        
        level4Sizer.Add(grid, 0)       
        
        level5Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        level5_list = [('Sale Begin','itemInq_saleBegin_datectrl','item_detailed2','sale_begin'),
                       ('Sale End','itemInq_saleEnd_datectrl','item_detailed2','sale_end'),
                       ('Time Begin','itemInq_timeBegin_timectrl','item_detailed2','sale_begin_time'),
                       ('Time End','itemInq_timeEnd_timectrl','item_detailed2','sale_end_time')]
        
        for label, name, table, field in level5_list:
            box = wx.StaticBox(self, -1, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            if 'datectrl' in name:
                ctrl = RH_DatePickerCtrl(self, -1, name=name, style=wx.adv.DP_ALLOWNONE)
                ctrl.SetValue(wx.DateTime())
            if 'timectrl' in name:
                if 'Begin' in name:
                    timectrl_value = '12:00am'
                elif 'End' in name:
                    timectrl_value = '11:59pm'
                ctrl = RH_TimeCtrl(self, name=name, display_seconds=False, fmt24hr=False, id=-1,useFixedWidthFont=True,value=timectrl_value)
            ctrl.tableName = table
            ctrl.FieldName = field
            ctrl.Disable()
            boxSizer.Add(ctrl, 0, wx.ALL, 3)
            level5Sizer.Add(boxSizer, 0, wx.ALL|wx.CENTER, 10)                    
        
        MainSizer.Add(lookupSizer, 0, wx.ALL|wx.EXPAND, 3)
        MainSizer.Add(level1Sizer, 0, wx.ALL|wx.EXPAND, 3)
        MainSizer.Add(level2Sizer, 0, wx.ALL|wx.EXPAND, 3)
        MainSizer.Add(level3Sizer, 0, wx.ALL|wx.EXPAND, 3)
        MainSizer.Add(level4Sizer, 0)
        MainSizer.Add(level5Sizer, 0, wx.ALL|wx.ALIGN_CENTER, 3)
        self.SetSizer(MainSizer, 0)
        self.Layout()
        
        
                
    def OnFind(self, event):
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
        ItemLookupD = ItemLookupDialog(self, title="Item Lookup", size=(1000,800), style=style)
        ItemLookupD.ShowModal()
        print("-!-" * 40) 
        try:
            self.itempick = ItemLookupD.itemPicked
            print("self . item pick : ",self.itempick)
          
        except:
            self.itempick = ''
            wx.FindWindowByName('itemInq_itemNumber_txtctrl').SetCtrl(self.itempick)
            ItemLookupD.Destroy()
            
        wx.CallAfter(self.LoadInfo, event=self.itempick)
            
    
    def OnExitButton(self, event):
        self.Close()
    
   
    def OnSelectF1(self, event):
        selected = wx.FindWindowByName('itemInq_itemNumber_txtctrl').GetCtrl()
        self.itempick = selected
        self.Close()
        
    def OnKeyDown(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_RETURN or keycode == wx.WXK_NUMPAD_ENTER: 
            obj = event.GetEventObject()
            named = obj.GetName()
            raw_value = wx.FindWindowByName(named).GetCtrl()
            subbed_value = re.sub('[!@$%^&\*()~\[\]\{\}\=`]','',raw_value)
            new_value = subbed_value.upper()
            
            wx.FindWindowByName(named).SetCtrl(new_value)
            
            wx.CallAfter(self.OnItemNumber, event=named)
        
        event.Skip()
    
    def OnItemNumber(self, event):   
        named = event
            
        itemNumber = wx.FindWindowByName(named).GetCtrl()
        #queryWhere = 'upc=(?)'
        
        cnt_returnd = QueryOps().QueryCheck('item_detailed','upc',(itemNumber,))
        
        if cnt_returnd == 1:
            query = 'SELECT upc FROM item_detailed WHERE upc=(?)'
            data = (itemNumber,)
            returnd = SQConnect(query, data).ONE()[0]
            
            returnd =VarOps().DeTupler(returnd)
                
            wx.CallAfter(self.LoadInfo, event=returnd)     
            return
            
        if cnt_returnd == 0:
            whereFrom = QueryOps().ANDSearch(['upc','description','oempart_num','part_num'],itemNumber)
            query = "SELECT upc FROM item_detailed WHERE {0} LIMIT 5000".format(whereFrom)
            data = ''
            returnd = SQConnect(query, data).ALL()
        
        numresult = len(returnd)
        
        if numresult == 0:
            wx.FindWindowByName(named).SetCtrl('')
            return
            
        print("returnd : {0}".format(returnd))
        if len(returnd) == 1:
            returnd =VarOps().DeTupler(returnd)
            wx.FindWindowByName(named).SetCtrl(returnd)
            
                       
            wx.CallAfter(self.LoadInfo, event=returnd)     
            return
             
        if numresult > 1:
            print("*************** Create Modal Window for Individual Choosing...")
            self.itemNumber = itemNumber
            style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
            ItemLookupD = ItemLookupDialog(self, title="Item Lookup",  size=(1000,800), style=style, itemNumber=self.itemNumber)
            ItemLookupD.ShowModal()
            print("-!-" * 40) 
            try:
                self.itempick = ItemLookupD.itemPicked
                print("self . item pick : ",self.itempick)
            except:
                self.itempick = ''
            
            self.itempick =VarOps().DeTupler(self.itempick)
            
            wx.FindWindowByName('itemInq_itemNumber_txtctrl').SetCtrl(self.itempick)
            ItemLookupD.Destroy()
            
            wx.CallAfter(self.LoadInfo, event=self.itempick)
                
    def LoadInfo(self, event):
        print('Load Returnd : {0}'.format(event))                    
        
        upcd = event
        
        if upcd == '' or upcd == None:
            return
        query = 'SELECT description,quantity_on_hand FROM item_detailed WHERE upc=(?)'
        data = (upcd,)
        returnd = SQConnect(query, data).ONE()
        
        (descriptiond,qoh) = returnd
        
        query = 'SELECT department,category,subcategory,location FROM item_options WHERE upc=(?)'
        data = (upcd,)
        returnd = SQConnect(query, data).ONE()
        
        (department,category,subcategory,location) = returnd
        query = 'SELECT do_not_discount FROM item_detailed2 WHERE upc=(?)'
        data = (upcd,)
        returnd = SQConnect(query, data).ONE()[0]
        
        dnd = returnd
        
        load_list = [('itemInq_description_txtctrl',descriptiond),('itemInq_onHand_numctrl', qoh),
                     ('itemInq_department_txtctrl',department),('itemInq_category_txtctrl',category),
                     ('itemInq_subcategory_txtctrl',subcategory),('itemInq_material_txtctrl',location),
                     ('itemInq_donotdiscount_checkbox',dnd)]
        
        
        retails = RetailOps().RetailSifting(upcd)
            
        for name,varib in load_list:
            wx.FindWindowByName(name).SetCtrl(varib)                 
                     
        
            #retails = {}
        #for key in retail_list:
        #    retails[key] = ('1','0.00')
                
            
        print("Retails : {0}".format(retails))
        grid = wx.FindWindowByName('itemInq_retailPrice_grid')
        
        grid.Load(upc=upcd)
        
        retail_list = ['standard_price','level_(a)_price','level_(b)_price','level_(c)_price','level_(d)_price','level_(e)_price','level_(f)_price',
                       'level_(g)_price','level_(h)_price','level_(i)_price','on_sale_price']
        
        
        for name in retail_list:
            for xx in range(grid.GetNumberRows()):
                field = re.sub('[\(\)]','', name)
                key = re.sub('_price', '', name)
                key2 = re.sub('_', ' ', key)
                xlabel = grid.GetRowLabelValue(xx)
                #print "xlabel : key2 = {} : {}".format(xlabel, key2)
                if key2 in xlabel.lower():
                    print("xlabel : key2 = {} : {} : ({} -- {})".format(xlabel, key2, retails[field][0],retails[field][1]))
                    grid.SetCellValue(xx,0, retails[field][0])
                    grid.SetCellValue(xx,1, retails[field][1])
            #
        #for row in range(grid.GetNumberRows()):
        #    rowLabel = grid.GetRowLabelValue(row).lower()
        #    rowLabelSet = re.sub(' ','_', rowLabel)
        #    grid.SetCellValue(row,0,retails[rowLabelSet][0])
        #    grid.SetCellValue(row,1,retails[rowLabelSet][1])
        item = wx.FindWindowByName('itemInq_itemNumber_txtctrl').SelectAll()    
        
        grid = wx.FindWindowByName('itemInq_salesTracker_grid')
        grid.Load(upcd)
        #wx.CallAfter(self.SalesTracker, event=upcd)
    
    def SalesTracker(self, event):
        
        upcd = event
        
        grid = wx.FindWindowByName('itemInq_salesTracker_grid')
        wx.FindWindowByName(grid.GetName()).ClearCtrl(fillwith='0.000')

        thisyear = datetime.datetime.today().date().year
        lastyear = thisyear-1
        year2ago = thisyear-2
        year3ago = thisyear-3
        year_list = [thisyear, lastyear, year2ago, year3ago]
        for dated in year_list:
            for mnth in range(1,13):
                query = 'SELECT quantity FROM transactions WHERE year(date)=(?) and upc=(?) and month(date)=(?)'
                data = [dated,upcd,mnth,]
                returnd = SQConnect(query,data).ONE()
                
                quantity = returnd
                if returnd is None:
                    continue
                cnt = len(returnd)
                if cnt > 1:
                    lqty = Decimal(0)
                    for qty in returnd:
                        lqty += Decimal(qty)
                elif cnt == 1:
                    lqty = returnd[0]
                else:
                    lqty = 0
                            
                mth = datetime.datetime.strptime(str(mnth), '%m')
                amnth = mth.strftime('%B')
                
                setList=[(str(amnth),str(lqty))]
                
                GridOps(grid.GetName()).FillGrid(setList, col=0)
                                         
        
###-----------------------------------------------------------------------------
class CreditCardPopup(wx.Dialog):
    def __init__(self, debug=False, *args, **kwargs):
        kwargs['title'] = 'CreditCard Popup'
        kwargs['size'] = (300,300)
        super(CreditCardPopup, self).__init__(
                                         *args, **kwargs)
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        check_list = [('Name on Card','creditcardpopup_name_txtctrl',125),
                      ('PayType','creditcardpopup_payType_combobox',['Paypal','Square']),
                      ('Auth #/Last 4','creditcardpopup_authNum_txtctrl',125)] 
        idx = 1
        for label, name, sized in check_list:
            box = wx.StaticBox(self, -1,label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            
            if 'name' in name:
                ctrl = RH_MTextCtrl(self, -1, name=name, formatcodes='!_',size=(sized,-1))
                ctrl.SetFocus()
            if 'payType' in name:
                ctrl = RH_ComboBox(self, -1, name=name, choices=sized,size=(75,-1))     
            if 'authNum' in name: 
                ctrl = RH_MTextCtrl(self, -1, name=name, formatcodes='!_',size=(sized,-1)) 
            
            boxSizer.Add(ctrl, 0, wx.ALL, 3)
            
            MainSizer.Add(boxSizer, 0, wx.ALL|wx.ALIGN_CENTER,3)
        
        level2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_list = [('&Accept\n    F1','checkpopup_accept_button',self.OnAccept),
                       ('&Cancel\n    F12','checkpopup_cancel_button', self.OnCancel)]  
         
        for label, name, hdlr in button_list:
            btn = RH_Button(self, -1, label=label, name=name)
            btn.Bind(wx.EVT_BUTTON, hdlr)
            level2Sizer.Add(btn, 0, wx.ALL, 3)
            
        
        MainSizer.Add(level2Sizer, 0,wx.ALL|wx.ALIGN_CENTER, 5)
         
        self.SetSizer(MainSizer, 0)
        
    def OnAccept(self, event):
        check_list = [('name','creditcardpopup_name_txtctrl',125),
                      ('paytype','creditcardpopup_payType_combobox',['Paypal','Square']),
                      ('auth','creditcardpopup_authNum_txtctrl',125)] 
        
        listd = []
        for label, name, size in check_list:
            value = wx.FindWindowByName(name).GetCtrl()
            listd.append(value)
            
        self.payment = tuple(listd)
            
        
        self.Close()
            
    def OnCancel(self, event):
        self.Close()


class CheckPopup(wx.Dialog):
    def __init__(self, debug=False, *args, **kwargs):
        kwargs['title'] = 'Check Popup'
        kwargs['size'] = (300, 300)
        super(CheckPopup, self).__init__(*args, **kwargs)
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        check_list = [('Check #','checkpopup_checkNum_txtctrl'),
                      ('Driver\'s License #','checkpopup_dlNum_txtctrl'),
                      ('Date of Birth','checkpopup_dob_txtctrl'),
                      ('Phone #','checkpopup_phoneNum_txtctrl')] 
        idx = 1
        for label, name in check_list:
            box = wx.StaticBox(self, -1,label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            
            if re.search('(checkNum|dlNum)',name, re.I):
                ctrl = RH_MTextCtrl(self, -1, name=name, formatcodes='!_',size=(155,-1))
            if 'dob' in name:
                ctrl = RH_MTextCtrl(self, -1, name=name, mask='##/##/####',size=(125,-1))     
            if 'phone' in name: 
                ctrl = RH_MTextCtrl(self, -1, name=name, mask='(###) ###-####',size=(125,-1)) 
            
            if 'checkNum' in name:
                ctrl.SetFocus()
                    
            boxSizer.Add(ctrl, 0, wx.ALL, 3)
            
            MainSizer.Add(boxSizer, 0, wx.ALL|wx.ALIGN_CENTER,3)
        
        level2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_list = [('&Accept\n    F1','checkpopup_accept_button',self.OnAccept),
                       ('&Cancel\n    F12','checkpopup_cancel_button', self.OnCancel)]  
         
        for label, name, hdlr in button_list:
            btn = RH_Button(self, -1, label=label, name=name)
            btn.Bind(wx.EVT_BUTTON, hdlr)
            level2Sizer.Add(btn, 0, wx.ALL, 3)
            
        
        MainSizer.Add(level2Sizer, 0,wx.ALL|wx.ALIGN_CENTER, 5)
         
        self.SetSizer(MainSizer, 0)
        
    def OnAccept(self, event):
        check_list = [('Check #','checkpopup_checkNum_txtctrl'),
                      ('Driver\'s License #','checkpopup_dlNum_txtctrl'),
                      ('Date of Birth','checkpopup_dob_txtctrl'),
                      ('Phone #','checkpopup_phoneNum_txtctrl')] 
        
        listd = []
        for label, name in check_list:  
            value = wx.FindWindowByName(name).GetCtrl()
            listd.append(value)    
        
        self.payment = tuple(listd)    
        self.Close()
    
    def OnCancel(self, event):
        self.Close()

class FinishItDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):#parent, title, size, style, transDict, debug=False): #,ATs=None, addrNum=None, custNum=None, due=None, transNum=None, returnItems=None) :
        transDict = kwargs.pop('transDict')
        super(FinishItDialog, self).__init__(*args, **kwargs) #parent=parent,title=title,size=size,style=style)
        self.due = transDict['due']
        self.ActiveTransactions = transDict['ATs']
        self.addrNum = transDict['addrNum']
        self.custNum = transDict['custNum']
        self.cred = {}
        self.transNum = transDict['transNum']
        self.returnItems = transDict['returnItems']
       
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        levelA_1Sizer = wx.BoxSizer(wx.VERTICAL)
        level1_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        grid = FinishIt_Grid(self, name='finishitdialog_payterm_grid')
        print('CC: [{}]'.format(self.custNum))
        #grid.CreditCheck(custNum=self.custNum)
        grid.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.OnEnter)
        custCredit = QueryOps().CheckCredit(self.custNum)
        
        if custCredit is True or custCredit == 1:
            for xx in range(grid.GetNumberRows()):
                label = grid.GetRowLabelValue(xx)
                if 'Charge' in label:
                    grid.SetReadOnly(xx,0,True)
                    grid.SetRowLabelValue(xx,'No Charge')
                    
        
        grid.SetFocus()
        
        
        levelA_1Sizer.Add(grid, 0, wx.ALL|wx.ALIGN_LEFT, 10)
                        
        
        level1_Sizer.Add(levelA_1Sizer, 0, wx.ALL|wx.EXPAND, 3)
        level2_Sizer = wx.BoxSizer(wx.HORIZONTAL)

        sizerA = wx.BoxSizer(wx.VERTICAL)
        sizerA_list = [('Paid','finishIt_paid_txtctrl'),
                       ('Due','finishIt_due_txtctrl'),
                       ('Change','finishIt_change_txtctrl')]

        for label,name in sizerA_list:
            box = wx.StaticBox(self, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            ctrl = RH_TextCtrl(self, -1,
                               name=name,
                               size=(160,-1),
                               style=wx.TE_READONLY|wx.ALIGN_RIGHT)

            if 'change' in name:
                ctrl.SetForegroundColour(wx.RED)
            
            boxSizer.Add(ctrl, 0,wx.ALL,3)
            sizerA.Add(boxSizer, 0, wx.ALL, 3)


        sizerB = wx.GridSizer(4,3,5,5)
        sizerB_list = [('Reset\nF&1','finishit_reset_button',self.onResetF1),
                       ('Cancel\nF&2','finishit_cancel_button',self.onCancelF2),
                       ('Done\nF&3','finishit_done_button',self.onDoneF3),
                       ('Put on Hold\nF&4','finishit_hold_button',self.onPutOnHoldF4),
                       ('Set C&urrent Line to Amount Due\nF12','finishit_currentline_button',self.onSetAmountDue)]
        

        for label, name, hndlr in sizerB_list:
            button_size = ButtonOps().ButtonSized(sizerB_list)

        
        print("Button Sizes : ",button_size)
        for label, name,hndlr in sizerB_list:
            newLabel = ButtonOps().ButtonCenterText(label)
            btn = RH_Button(self, -1,
                            label=newLabel,
                            name=name,
                            size=(button_size[0],
                            button_size[1]))

            btn.Bind(wx.EVT_BUTTON, hndlr)
            #if 'done' in name:
            #    btn.Disable()
                
            sizerB.Add(btn,0)

        level2_Sizer.Add(sizerA,0)
        level2_Sizer.Add((60,20),0)
        level2_Sizer.Add(sizerB,0)
        
        MainSizer.Add(level1_Sizer, 0)
        MainSizer.Add(level2_Sizer, 0)
        self.SetSizer(MainSizer, 0)
        self.Layout()

        wx.CallAfter(self.onLoad, event='')
    
    def Due(self,due=None):
        self.due = due
        
    def onLoad(self, event):
        wx.FindWindowByName('finishIt_due_txtctrl').SetCtrl(self.due)    
        
    
    
    def OnEnter(self, event):
        obj = event.GetEventObject()
        named = obj.GetName()
        row = event.GetRow()
        col = event.GetCol()
        grid = wx.FindWindowByName(named)  
        svalue = grid.GetCellValue(row,col)
        fvalue = MiscOps().NumbersOnly(svalue)
        print('svalue : {}\nfvalue : {}'.format(svalue, fvalue))
        if fvalue is None:
            grid.SetCellValue(row,col, '')
            return
        
        if fvalue is not None:
            pval = RetailOps().RoundIt(fvalue, '1.00')
            
            grid.SetCellValue(row,col, str(pval))
            
              
#        keycode = event.GetKeyCode()
#        if keycode == wx.WXK_RETURN or keycode == wx.WXK_NUMPAD_ENTER or keycode == wx.WXK_TAB: 
#            wx.CallAfter(self.Actions, event=named)
#        event.Skip()
        
        
        
#    def Actions(self, event):
#       
#        named = event
        add = 0
        listd = [('cash',0),('check',1),('charge',2),('debit',3),('credit1',4),
                 ('credit2',5),('credit3',6),('credit4',7),('credit5',8)]
       
        
        for label, cell in listd:
            value = grid.GetCellValue(cell,0)
            #Debugger("value : {}\n\tname : {}".format(value, name))
                
            if re.search('[0-9]', str(value)):
                #g = re.match('f[nshit]+_(.*)_[texnum]+ctrl',name,re.I)
                #self.cred[g.group(1)] = value
                self.cred[label] = value
                #print 'G : {} = {}'.format(g.group(1),self.cred)
                self.cred['change'] = 0.0            
                add += Decimal(value)
                comp = Decimal(self.due) - Decimal(add)         
                print("Comp : ",comp)
                if comp < 0:
                    if 'cash' in label:
                        change = Decimal(value) + Decimal(comp)
                        #print "change : ",change
                        #CO('finishIt_change_txtctrl').SetCtrl(change)
                        toomuch = Decimal(self.due) * 5
                        toomuch =VarOps().ChangeType(toomuch, 'decimal')
                        value =VarOps().ChangeType(value, 'decimal')
                        
                        if value >= toomuch:
                            result = wx.MessageBox('Are you sure?','Info',wx.OK|wx.CANCEL)
                            if result == wx.CANCEL:
                                wx.CallAfter(self.onResetF1, event='')
                                return  
                        totald = Decimal(self.due) - Decimal(add)
                        totald = RetailOps().DoRound(totald, '1.00')
                        print("{} - {} = {}".format(self.due,add,totald))
                        
                        totald = str(totald)
                        wx.FindWindowByName('finishIt_change_txtctrl').SetCtrl(totald)
                        self.cred['change'] = totald
                        add = RetailOps().DoRound(add, '1.00')    
                        
                        formal_paid = RetailOps().DoRound(value, '1.00')
                        wx.FindWindowByName('finishIt_paid_txtctrl').SetCtrl(formal_paid)
                        
                        wx.CallAfter(self.onDoneF3, event='')
                        print('T {} > {}'.format(totald, self.due))
                        totald =VarOps().ChangeType(totald, 'decimal')
                        value =VarOps().ChangeType(value, 'decimal')
                        if totald > value:
                            setList=[('Cash',self.due)]
                            GridOps(grid.GetName()).FillGrid(setList, col=1)
                            #CO('finish_cash_numctrl').SetCtrl(self.due)
                        
                        self.due =VarOps().ChangeType(self.due, 'decimal')
                        value =VarOps().ChangeType(value, 'decimal')
                        if value > self.due:
                            break
                    else:            
                        new_value = Decimal(value) + Decimal(comp)
                        print("new P : ",new_value)
                        add += Decimal(comp)
                        
                        print("AddIT : ",add)
                        
                        totald = Decimal(self.due) - Decimal(add)
                        totald =VarOps().DoRound(totald, '1.00')
                        print("{} - {} = {}".format(self.due,add,totald))
                        
                        totald = str(totald)
                        wx.FindWindowByName('finishIt_due_txtctrl').SetCtrl(totald)
                        add = RetailOps().DoRound(add, '1.00')    
                        #CO('finishIt_paid_txtctrl').SetCtrl(value)
        
                        
        
    def onResetF1(self, event):
       
        self.cred = {}
        grid = wx.FindWindowByName('finishitdialog_payterm_grid')
        grid.Clear()
            
        grid.SetFocus()
            
    def onCancelF2(self, event):
        
       
        self.Status = 'open'
        self.Close()
        pass

    def onDoneF3(self, event):
       
        grid = wx.FindWindowByName('finishitdialog_payterm_grid')
        listd = [('cash',0),('check',1),('charge',2),('debit',3),('credit1',4),
                 ('credit2',5),('credit3',6),('credit4',7),('credit5',8)]
        
        due_cash = wx.FindWindowByName('finishIt_due_txtctrl').GetCtrl()
        
        for name, cell in listd:
            value = grid.GetCellValue(cell,0)
            #value = HU.GetCtrl(name)
            
            if value == '' or value is None:
                value = 0
            if Decimal(value) > 0:
                style = wx.DEFAULT_FRAME_STYLE & (~wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX) & (~wx.MINIMIZE_BOX)
                get = name
                #print 'Get : ',get[1]
                    
                if 'check' in name:
                    chek_payment = value
                    checkPopup = CheckPopup(self,
                                           style=style)
               
                    checkPopup.ShowModal()
                    
                    try:
                        payInfo = (str(value),) + checkPopup.payment
                        
                    except:
                        checkPopup.Destroy()
                    
                if 'cash' in name:
                    payInfo = due_cash
                    
                if 'charge' in name:
                    payInfo = value                    
                
                if re.search('(credit|debit)', name, re.I):
                    creditPopup = CreditCardPopup(self,
                                           style=style)
               
                    creditPopup.ShowModal()
                    
                    try:
                        payInfo = (str(value),) + creditPopup.payment
                        
                    except:
                        creditPopup.Destroy()
                        
                    
                
                self.cred[get] = payInfo
        print("Creds : ",self.cred)    
                    
                        
        
        
        
        
        result = wx.MessageBox('Finish Transaction?', 'Info', wx.OK|wx.CANCEL)
        poNum = wx.FindWindowByName('pos_PoTab_ponumber_txtctrl').GetCtrl()
        CloseDict = {'ATs': self.ActiveTransactions,
                     'transType' : 'Sale',
                     'payment' : self.cred,
                     'addrNum' : self.addrNum,
                     'custNum' : self.custNum,
                     'transNum' : self.transNum,
                     'returns' : None,
                     'poNum' : None,
                     'stationNum' : None,
                     'drawerNum' : None
                     }
        if result == wx.OK:
            CloseDict['returns'] = self.returnItems
            CloseDict['transType'] = 'Sale'
            ATs = HU.ReadyClose(CloseDict) #ATs=self.ActiveTransactions, transType='Sale',payment=self.cred, addrNum=self.addrNum, custNum=self.custNum, transNum=self.transNum, returns=self.returnItems)
            print("AT : ",ATs)
        
            self.Status = 'closed'
            self.Close()
                   
    def onPutOnHoldF4(self, event):
        poNum = wx.FindWindowByName('pos_PoTab_ponumber_txtctrl').GetCtrl()
        CloseDict['poNum'] = poNum
        ATs = HU.ReadyClose(CloseDict) #ATs=self.ActiveTransactions, transType='Hold', addrNum=self.addrNum, custNum=self.custNum, ponumber=poNum) 
        
        self.Status = 'closed'
        self.Close()

    def onSetAmountDue(self, event):
       
        grid = wx.FindWindowByName('finishitdialog_payterm_grid')
        
        row, col = GridOps(grid.GetName().GetGridCursor())
        grid.SetCellValue(row,col, self.due)
        
        

    def Trans(self, ATs=None, addrNum=None, custNum=None):
        self.ActiveTransactions = ATs
        if addrNum == '':
            self.addrNum = None
        else:
            self.addrNum = addrNum
        
        if custNum == '':
            self.custNum = None
        else:
            self.custNum = custNum
     

class FindAddressLookupDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super(FindAddressLookupDialog, self).__init__(*args, **kwargs)
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        level1_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        box = wx.StaticBox(self, -1, label='Address Search')
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        
        ctrl = wx.TextCtrl(self, -1, name='addrSearch_txtctrl', size=(260,-1),style=wx.TE_PROCESS_ENTER)
        ctrl.Bind(wx.EVT_TEXT_ENTER, self.OnSearchButton)
        ctrl.SetFocus()
        btn = wx.Button(self, -1, label='Search', name='addrSearch_button')
        btn.Bind(wx.EVT_BUTTON, self.OnSearchButton)
        
        boxSizer.Add(ctrl, 0, wx.ALL, 3)
        boxSizer.Add(btn, 0, wx.ALL, 3)
        
        level1_Sizer.Add(boxSizer, 0, wx.ALL, 3)
        
        level1a_Sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self, -1, label='', name='addrSearch_loading_text')
        level1a_Sizer.Add(text,0)
         
        level2_Sizer = wx.BoxSizer(wx.VERTICAL)
        
        lc = RH_OLV(self, -1, name='addrSearch_lc', size=(760,465), style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        lc.SetColumns([
                       ColumnDefn('Account #', 'center', 120, 'acctNum'),
                       ColumnDefn('Address 1', 'left', 220, 'address1d'),
                       ColumnDefn('Address 2', 'left', 150, 'address2d'),
                       ColumnDefn('City', 'left', 130, 'cityd'),
                       ColumnDefn('State','left', 90, 'stated')
                      ])

        lc.SetSortColumn(1)
        
        
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
        pout.b('On Search Button')
        #revised_search = re.sub(' ','.*',addr_search)
        whereFrom = 'address0'
            
        
        if len(addr_search) == 0:
            return

        query = "SELECT addr_acct_num,address0,address2,address3,city,state from address_accounts where {0} LIKE (?) OR zipcode=(?)".format(whereFrom)
        data = (addr_search, addr_search,)
        returnd = SQConnect(query, data).ALL()
        
        pout.v(f'Item 0 : {returnd}')                  
        lcname = 'addrSearch_lc'
        lc = wx.FindWindowByName(lcname)
        lc.DeleteAllItems()
        plural = ''
        records_returnd = 0
        pout.v(f'Item 1 : {returnd}')                  
        if returnd:
            records_returnd = len(returnd)
            if records_returnd > 1:
                plural = 'es'
                        
            num_items = wx.FindWindowByName('addrSearch_loading_text')
            num_items.SetLabel('Found '+str(records_returnd)+' Address'+plural)
            row = 0    
            pout.v(f'Item 2: {returnd}')                  
            for addr_acct_numd, address1d, address2d, address3d, cityd, stated in returnd:
                setList = [{'acctNum':addr_acct_numd,'address1d':address1d,'address2d':address2d,'cityd':cityd,'stated':stated}]
                lc.AddObjects(setList)
            
            
        
        
    
    def OnChooserCellLeftClick(self, evt):
        item_id,objText = EventOps().LCGetSelected(evt)
        self.addrPicked = objText
        self.Close()
        
        
        
        
        

        
