import wx
from ObjectListView import ObjectListView, ColumnDefn, OLVEvent
import wx.grid as gridlib
import pout
from controls import RH_Button, RH_ListBox, RH_TextCtrl, GridOps, Themes, IconList
from db_ops import LookupDB

class TBA(wx.Panel):
    """TO BE ADDED """
    def __init__(self, *args, **kwargs):
        self.thing = kwargs.pop('thing')
        wx.Panel.__init__(self, *args, **kwargs)
        MainSizer = wx.BoxSizer(wx.VERTICAL)

        self.tba = wx.StaticText(self, -1, f'{self.thing.upper()} TO BE ADDED')
        MainSizer.Add(self.tba, 0)

        self.SetSizer(MainSizer)
        self.Layout()

class PhoneNumber_Panel(wx.Panel):
    """PhoneNumber Panel contains all controls necessary to achieve adding phone numbers to accounts. 
       The fieldname & tablename variables are  for the phone olv to save to customer accounts."""
    def __init__(self, *args, **kwargs):
        self.fieldName = kwargs.pop('fieldName')
        self.tableName = kwargs.pop('tableName')
        self.custNum = kwargs.pop('custNum')
        wx.Panel.__init__(self, *args, **kwargs)
        
        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        savebutton = RH_Icon(icon='save')
        savebutton.Bind(wx.EVT_BUTTON, self.OnSave)

        f_box = wx.StaticBox(self, -1, label="Phone Numbers")
        f_boxSizer = wx.StaticBoxSizer(f_box, wx.VERTICAL)
        
        f_add_boxSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.phtype = RH_Button(self, -1, name="custdatapnl_phonetype_btn")
        self.phtype.listd = ['HOME','CELL','WORK','FAX',
                             'CONTACT1','CONTACT2','CONTACT3']
        f_add_boxSizer.Add(self.phtype, 0)

        self.phonetc = RH_MTextCtrl(self, -1, 
                                mask='(###) ###-####',
                                validRegex = "^\(\d{3}\) \d{3}-\d{4}", 
                                size=(160, -1), 
                                name='custdatapnl_addphone_txtctrl')
        
        f_add_boxSizer.Add(self.phonetc, 0, wx.ALL, 3)

        ctrl = RH_Icon(icon='add')
        ctrl.Bind(wx.EVT_BUTTON, self.AddPhoneNumber)
        
        f_add_boxSizer.Add(ctrl, 0)
        f_boxSizer.Add(f_add_boxSizer, 0)
        
        self.SetSizer(f_boxSizer, 0)
        self.Layout()

        self.lc = RH_OLV(self, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.lc.SetColumns([ColumnDefn('Type','center',120,'typd'),
                            ColumnDefn('Phone #','center',150,'number')])
        self.lc.fieldName = self.fieldName
        self.lc.tableName = self.tableName

        f_boxSizer.Add(self.lc, 0)
        MainSizer.Add(f_boxSizer, 0, wx.ALL, 3)
        MainSizer.Add(savebutton, 0, wx.ALL, 3)
        self.SetSizer(MainSizer, 0)
        self.Layout()
        
        wx.CallAfter(self.OnLoad, event='')

    def AddPhoneNumber(self, event):
        addphone = [{'typd':self.phtype.GetCtrl(), 'number':self.phonetc.GetCtrl()}]
        self.lc.AddObjects(addphone)

    def OnLoad(self):
        returnd = self.lc.OnLoad('cust_num', self.custNum)
        phones = json.load(returnd[0])
  
    def OnSave(self):
        phones = self.lc.GetObjects()
        ph_json = json.dumps(phones)
        returnd = LookupDB('customer_basic_info').UpdateSingle('phone_numbers',ph_json,'cust_num',self.custNum)


class AltLookup(wx.Panel):
    """ AltLookup List Box Panel """
    def __init__(self, *args, **kwargs):
        pout.v(kwargs)
        self.boxlabel = kwargs.pop('boxlabel')
        self.lbsize = kwargs.pop('lbsize')
        self.lbname = kwargs.pop('lbname')
        self.tableName = kwargs.pop('tableName')
        self.fieldName = kwargs.pop('fieldName')
        self.loadAs = 'str'
        self.saveAs = 'str'
        wx.Panel.__init__(self, *args, **kwargs)
        # pout.v(f'tableName : {self.tableName} ; fieldName : {self.fieldName}')
        icon = IconList()
        box = wx.StaticBox(self, wx.ID_ANY, label=self.boxlabel)
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        
        levelSizer = wx.BoxSizer(wx.HORIZONTAL)
        level1Col2Sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.lb = RH_ListBox(self, -1,
                          size = self.lbsize, 
                          name = self.lbname)
        self.lb.tableName = self.tableName
        self.lb.fieldName = self.fieldName
        self.lb.Bind(wx.EVT_LISTBOX, self.ListBoxSelectItem) 
        levelSizer.Add(self.lb, 0)
        
        self.lbtc = RH_TextCtrl(self, -1, size=(110, -1), style=wx.TE_PROCESS_ENTER)
        self.lbtc.loadAs = 'str'
        self.lbtc.saveAs = 'str'
        self.lbtc.Bind(wx.EVT_TEXT_ENTER, self.ListBoxOnAddButton)
        level1Col2Sizer.Add(self.lbtc, 0, wx.ALL, 3)
        
        #self.addbutton = RH_Button(self, label="Add", size=30)
        addicon = icon.getIcon('add')
        self.addbutton = wx.Button(self, label=addicon, style=wx.BORDER_NONE)
        self.addbutton.SetFont(icon.getFont(size=30))
        self.addbutton.SetForegroundColour('Green')
        self.addbutton.Bind(wx.EVT_BUTTON, self.ListBoxOnAddButton)
        level1Col2Sizer.Add(self.addbutton, 0, wx.ALL, 3)
        
        remicon = icon.getIcon('minus')
        self.rembutton = wx.Button(self, -1, label=remicon, style=wx.BORDER_NONE)
        self.rembutton.SetFont(icon.getFont(size=30))
        self.rembutton.SetForegroundColour('Red')
        self.rembutton.Bind(wx.EVT_BUTTON, self.ListBoxOnRemoveButton)
        level1Col2Sizer.Add(self.rembutton, 0, wx.ALL, 3)
                
        levelSizer.Add(level1Col2Sizer, 0)
        
        boxSizer.Add(levelSizer, 0)
        self.SetSizer(boxSizer)
        self.Layout()

    def SetItems(self, items):
        self.lb.SetItems(items)
        
    def OnLoad(self, event):
        self.lb.OnLoad(whereField='abuser', whereValue='rhp')

    def OnSave(self, event):
        self.lb.OnSave(whereField='abuser', whereValue='rhp')

    def Clear(self, event):
        self.lb.Clear()
    
    def GetItems(self):
        return self.lb.GetItems()
        
    def ListBoxOnAddButton(self, event):
        if not self.lbtc.GetValue():
            return
                
        num_altlookups = self.lb.GetCount()
        tobe_searched = self.lbtc.GetValue()
        has_found = self.lb.FindString(tobe_searched)
        
        if has_found != -1:
            foundIndex = has_found
            self.lb.EnsureVisible(foundIndex)
            self.addbutton.SetForegroundColour('Red')
            self.TC_ClearFocus()
        else:
            self.addbutton.SetForegroundColour('Green')
            self.lb.Append(self.lbtc.GetValue().upper())
            self.TC_ClearFocus()
  
        allstrings = self.lb.GetStrings()

    def TC_ClearFocus(self):
        self.lbtc.Clear()
        self.lbtc.SetFocus()

    def ListBoxSelectItem(self, event):
        selection = self.lb.GetStringSelection()
        self.lbtc.SetCtrl(selection)

    def ListBoxOnRemoveButton(self, event):
        tobe_removed = self.lbtc.GetValue()
        currentItem = self.lb.FindString(tobe_removed)
        if currentItem != -1:
            self.lb.EnsureVisible(currentItem)
            self.lb.Delete(currentItem)
            
        self.TC_ClearFocus()


class Tax_Table_Grid(gridlib.Grid):
    """Table Info for Taxes."""
    def __init__(self, parent, name, size):
        gridlib.Grid.__init__(self, parent, style=wx.BORDER_SUNKEN, name=name, size=size)

        colLabel_list = [('Tax Name', 250),
                         ('Min\nSale', 70),
                         ('Max\nSale', 70),
                         ('Item\nMax', 70),
                         ('From\nAmt', 70),
                         ('Tax\nRate', 70),
                         ('From\nAmt', 70),
                         ('Tax\nRate', 70),
                         ('From\nAmt', 70),
                         ('Tax\nRate', 70)]
 
        self.CreateGrid(6, len(colLabel_list))      
        self.DisableDragRowSize()
        self.EnableEditing(True)
        self.SetLabelFont(wx.Font(wx.FontInfo(8)))
        self.SetRowLabelSize(0)
        #self.SetLabelBackgroundColour(Themes().GetColor('bg'))
        #self.SetLabelTextColour(Themes().GetColor('text'))
        #self.SetDefaultCellTextColour(Themes('Inventory').GetColor('text'))

        idx = 0
        for label, sized in colLabel_list:
            self.SetColLabelValue(idx, label)
            self.SetColSize(idx, sized)
            idx += 1
        
        self.Default()
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.OnRightClick)     

        
    def Default(self):
        for x in range(0, 6):
            for y in range(1, self.GetNumberCols()):
                self.SetCellEditor(x, y, gridlib.GridCellFloatEditor(width=6,precision=2))
                self.SetCellAlignment(x,y, wx.ALIGN_RIGHT, wx.ALIGN_BOTTOM)
                blank = '0.00'
                colLabel = self.GetColLabelValue(y)
                if 'Rate' in colLabel:
                    self.SetCellEditor(x, y, gridlib.GridCellFloatEditor(width=5,precision=3))
                    blank = '0.000'
                if 'Item' in colLabel:
                    self.SetCellEditor(x, y, gridlib.GridCellFloatEditor(width=6,precision=0))
                    blank = '0'
                    self.SetCellAlignment(x, y, wx.ALIGN_CENTRE, wx.ALIGN_BOTTOM)
                
                self.SetCellValue(x, y, blank)
        
        GridOps(self.GetName()).GridAlternateColor('')
        

    def OnLoad(self):
        cntret = LookupDB('tax_tables').Count()
        returnd = None
        if cntret > 0:
            for idx in range(cntret):
                fields = '''tax_name, min_sale, max_sale, item_max, 
                            from_amt0, tax_rate0, from_amt1, tax_rate1, 
                            from_amt2, tax_rate2'''
                returnd = LookupDB('tax_tables').General(fields)
        if returnd is not None:
            cnt = len(returnd)
            for i in range(0,cnt):
                vals = returnd[i]
                for y in range(0,9):
                    value = vals[y]
                    a = re.search('[A-Za-z]', str(value))
                    aty = str(type(a))
                    vty = str(type(value))
                    if not a:
                        if y in [1, 2, 4, 6, 8]:
                            value = format(value, '.2f')
                        elif y in [3]:
                            value = format(value, '.0f')
                        
                        elif 'decimal' in vty:
                            value = format(value, '.3f')
                
                    self.SetCellValue(i, y, str(value))
                        
    
    def OnSave(self):
        for x in range(0, 6):
            tax_name = self.GetCellValue(x, 0)
            if len(tax_name) > 0:
                QueryOps().CheckEntryExist('tax_name', tax_name, ['tax_tables'])
                neList = [(1, 'min_sale'),
                        (2, 'max_sale'),
                        (3, 'item_max'),
                        (4, 'from_amt0'),
                        (5, 'tax_rate0'),
                        (6, 'from_amt1'),
                        (7, 'tax_rate1'),
                        (8, 'from_amt2'),
                        (9, 'tax_rate2')]
                for y, field, in neList:
                    val = self.GetCellValue(x, y)
                    returnd = LookupDB('tax_tables').UpdateSingle(field, val, 'tax_name', tax_name)

    def Update(self, tax_dict):
        idx = 0
        self.ClearGrid()
        self.Default()
        for key, value in tax_dict.items():
            for i in range(len(value)):
                self.SetCellValue(idx, i, value[i])
            idx += 1
        
       


    def OnRightClick(self, event):
        obj = event.GetEventObject()
        rowclickd = event.GetRow()
        tax_dict = {}
        
        for x in range(self.GetNumberRows()):
            x_dict = {}
            for y in range(self.GetNumberCols()):
                a = self.GetCellValue(x, y)
                x_dict[y] = self.GetCellValue(x, y)
                
            tax_dict[x] = x_dict
        
        old = tax_dict.pop(rowclickd)
        self.Update(tax_dict)
        RecordOps('tax_tables').DeleteEntryRecord('tax_name', old[0])

        
###----------------------------------------------------------------------------
class TaxHoliday_Grid(gridlib.Grid):
    """Tax Holiday Grid Used on Tax Holiday Pages."""
    def __init__(self, *args, **kwargs):
        gridlib.Grid.__init__(self, *args, **kwargs)
        collabel_list = [('Item Number',200),('Description',775)]
        self.CreateGrid(100, len(collabel_list))
        self.SetDefaultCellAlignment(wx.ALIGN_LEFT,wx.ALIGN_CENTRE)
        self.SetLabelFont( wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.NORMAL) )
        self.SetRowLabelSize(0)
        idx = 0
        for label,sized in collabel_list:
            self.SetColLabelValue(idx, label)         
            self.SetColSize(idx, sized)
            idx += 1

        GridOps(self.GetName()).GridAlternateColor('')
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.OnRightClick)

    def OnRightClick(self, event):
        obj = event.GetEventObject()
        named = obj.GetName()
        row = event.GetRow()
        col = event.GetCol()
        self.DeleteRows(row)
        self.AppendRows()
        
        GridOps(named).GridAlternateColor('')
    
    def AddItem(self, item):
        newline = GridOps(self.GetName()).CurGridLine(blank=True)
        self.SetCellValue(newline, 0, item['upc'])
        self.SetCellValue(newline, 1, item['desc'])

               

        

class POS_Transactions_Grid(gridlib.Grid):
    """POS Acct Grid used at the POS Screen."""
    def __init__(self, parent, name, size):
        gridlib.Grid.__init__(self, parent, style=wx.BORDER_SUNKEN, name=name, size=size)
        
        colLabel_list = [('Item Number', 200), ('Description', 290),
                         ('Price', 120), ('Quantity', 90), ('Total', 90),
                         ('Discount', 105), ('Tx', 30)]

        self.CreateGrid(100, len(colLabel_list))
        self.EnableScrolling(False, True)
        self.DisableDragRowSize()
        self.SetLabelFont(wx.Font(wx.FontInfo(10)).Bold())
        self.SetRowLabelSize(0)
        self.SetLabelBackgroundColour(Themes().GetColor('bg'))
        self.SetLabelTextColour(Themes().GetColor('text'))
        
        idx = 0
        for label, sized in colLabel_list:
            self.SetColLabelValue(idx, label)
            self.SetColSize(idx, sized)
            idx += 1
        
        col_align_list = [('Price', wx.ALIGN_RIGHT),
                          ('Total', wx.ALIGN_RIGHT),
                          ('Quantity', wx.ALIGN_CENTER),
                          ('Discount', wx.ALIGN_CENTER),
                          ('Tx', wx.ALIGN_CENTER)]

        for xx in range(self.GetNumberRows()):
            readonly_list = ['Price', 'Total']
            for yy in range(self.GetNumberCols()):
                for label, attrib in col_align_list:
                    header = self.GetColLabelValue(yy)
                    if label in header:
                        self.SetCellAlignment(xx, yy, attrib, wx.ALIGN_CENTER)
                for readonly in readonly_list:
                    if readonly in header:
                        self.SetReadOnly(xx, yy, True)

        self.Bind(wx.EVT_KEY_DOWN, self.onTransactionGridKeyPress)
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.OnRightClick)
        
        GridOps(self.GetName()).GridAlternateColor('')

    def Add(self, upc_dict):
        a = GridOps(self.GetName())
        emptyrow = a.FindEmptyRow()
        mergd = False
        for row in range(emptyrow):
            if self.GetCellValue(row, 0) == upc_dict['upc']:
                qty = self.GetCellValue(row, 3)
                new_qty = self.Calculate(qty, upc_dict['qty'], '+')
                disc = self.GetCellValue(row, 5)
                new_disc = upc_dict['disc']
                #pout.v(f'New Discount : {new_disc}')
                if not re.search('%', disc, re.I) or len(new_disc) == 0:
                    disc = None
                else:
                    if '%' in disc:
                        disc = Decimal(disc.strip('%'))
                    if new_disc > disc:
                        disc = new_disc
                    

                new_total = self.Calculate(new_qty, upc_dict['price'], 'x', disc)

                self.SetCellValue(row, 3, str(new_qty))
                self.SetCellValue(row, 4, str(new_total))
                if disc is not None:
                    m = str(disc)+'%'
                    self.SetCellValue(row, 5, m)
                mergd = True

        if mergd is not True:
            setList = [('Item Number', upc_dict['upc']),
                    ('Description',upc_dict['desc']),
                    ('Quantity', upc_dict['qty']),
                    ('Price', upc_dict['price']),
                    ('Total', upc_dict['totalprice']),
                    ('Discount', upc_dict['disc']),
                    ('Tx', upc_dict['ntx'])]
            a.FillGrid(setList, emptyrow)   

        self.Update(upc_dict)             
            
    
    def Calculate(self, num_one, num_two, typed, disc=None):
        a = Decimal(num_one)
        b = Decimal(num_two)
        if '-' in typed:
            c = a - b
        if '+' in typed:
            c = a + b
        if 'x' in typed:
            c = a * b
        if disc is not None and len(disc) > 0:
            #pout.v(f'Discount : {disc}')
            d = (Decimal(disc) * c) + c
            c = d
        
        return RetailOps().Dollars(c)
        

    def Remove(self, upc):
        pass

    def Update(self, t_dict):
        a = GridOps(self.GetName())
        self.ClearGrid()
        t_type = ('SALE', 'RETURN')
        row = 0
        for typ in t_type:
            for transId in t_dict[typ]:
                for upcd in t_dict[typ][transId]:
                    setList = [('Item Number', upcd),
                               ('Description',t_dict[typ][transId][upcd]['Desc']),
                               ('Quantity', t_dict[typ][transId][upcd]['Qty']),
                               ('Price', t_dict[typ][transId][upcd]['Price']),
                               ('Total', t_dict[typ][transId][upcd]['TotalPrice']),
                               ('Discount', t_dict[typ][transId][upcd]['Discount']),
                               ('Tx', t_dict[typ][transId][upcd]['Taxable'])]

                    a.FillGrid(setList, row)
                    row += 1


                
    def onTransactionGridKeyPress(self, event):
        keycode = event.GetKeyCode()
        
        if keycode == wx.WXK_TAB:
            wx.FindWindowByName('pos_repeatLast_button').SetFocus()
        if keycode == wx.WXK_LEFT or keycode == wx.WXK_RIGHT or keycode == wx.WXK_UP or keycode == wx.WXK_DOWN:
            event.Skip()
    
        event.Skip()


    def OnRightClick(self, event):
        print('RIGHT CLICKED')
        obj = event.GetEventObject()
        rowclickd = event.GetRow()
        f_dict = {}
        
        for x in range(self.GetNumberRows()):
            x_dict = {}
            for y in range(self.GetNumberCols()):
                a = self.GetCellValue(x, y)
                x_dict[y] = self.GetCellValue(x, y)
                
            f_dict[x] = x_dict
        
        old = f_dict.pop(rowclickd)
        self.Update(f_dict)
    


###----------------------------------------------------------------------------

class SalesTracker_Grid(gridlib.Grid):
    """ Sales Tracker Grid """
    def __init__(self, parent, name, debug=False):
        """ Constructor """
        gridlib.Grid.__init__(self, parent, style=wx.BORDER_SUNKEN, name=name)
        
        self.EnableScrolling(False,False)
        self.DisableDragRowSize()
        self.CreateGrid(12,4)
        self.EnableEditing(False)
        self.SetColLabelSize(40)
        colLabel_list = ['Current\nYear','Last\nYear','2 Years\nAgo','3 Years\nAgo']
        for idx, label in enumerate(colLabel_list):
            self.SetColLabelValue(idx, label)
        
        self.SetRowLabelSize(90)
        rowLabel_list = ['January','February','March','April','May','June',
                         'July','August','September','October','November',
                         'December']
        
        for idx, label in enumerate(rowLabel_list):
            self.SetRowLabelValue(idx, label)
            
        GridOps(self.GetName()).GridAlternateColor('')
        wx.CallAfter(self.Default,event='')

    def Default(self, event):
        defaultValues = ['0.000','0.000','0.000','0.000']
        for row in range(self.GetNumberRows()):
            for col in range(self.GetNumberCols()):
                self.SetCellValue(row, col, defaultValues[col])
                self.SetCellAlignment(row,col,wx.ALIGN_RIGHT,wx.ALIGN_RIGHT)    
    
    def Load(self, upc=None):
        self.upc = upc
        if self.upc is None:
            return
        
        wx.FindWindowByName(self.GetName()).ClearCtrl(fillwith='0.000')

        thisyear = datetime.datetime.today().date().year
        lastyear = thisyear-1
        year2ago = thisyear-2
        year3ago = thisyear-3
        year_list = [thisyear, lastyear, year2ago, year3ago]
        for dated in year_list:
            for mnth in range(1,13):
                query = '''SELECT quantity 
                           FROM transactions 
                           WHERE year(date)=(?) and upc=(?) and month(date)=(?)'''
                data = [dated,self.upc,mnth,]
                returnd = SQConnect(query,data).ONE()
                #print 'returnd : ',returnd
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
                #print 'amth : ',amnth
                setList=[(str(amnth),str(lqty))]
                
                GridOps(self.GetName()).FillGrid(setList, col=0)
    


#-------------------------------------------------------------------------------

class Retail_Info(wx.Panel):
    """ Retail Info """
    def __init__(self, nocost=True):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        MainSizer = wx.BoxSizer(wx.HORIZONTAL)
        level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        costd_list = [('Average Cost','details_avgcost_numctrl'),
                      ('Last Cost','details_lastcost_numctrl'),
                      ('Starting Margin','details_startingMargin_numctrl')]
        
        for label,name in costd_list:
            cost_text = wx.StaticText(self, -1, label=label+":")
            ctrl = RH_NumCtrl(self, -1, value=0, 
                                            name=name, 
                                            integerWidth=6, 
                                            fractionWidth=2)
            
            ctrl.SetValue('0.000')

            level1Sizer.Add(cost_text, 0, wx.ALL,2)
            level1Sizer.Add(ctrl, 0, wx.ALL,2)

        level2Sizer = wx.BoxSizer(wx.HORIZONTAL)

        returnd = LookupDB('item_pricing_schemes').General('name, scheme_list, reduce_by')
        priceschema_list = returnd

        box = wx.StaticBox(self, label="Pricing\nSchemes")
        boxSizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        boxSizer.Add((20,20), 0)
        xx=0
        rb = RH_Button(self, id=wx.ID_ANY, label="RESET", 
                                           name="details_pricescema_RESET_button")
        
        rb.Bind(wx.EVT_BUTTON, self.OnPriceSchemes)
        boxSizer.Add(rb, 0)

        for label, scheme_list, reduce_by in priceschema_list:
            rb = RH_Button(self, id=wx.ID_ANY, 
                           label=label, 
                           name=scheme_list)
            
            rb.Bind(wx.EVT_BUTTON, self.OnPriceSchemes)
            boxSizer.Add(rb, 0)
            xx+=1
        
        level2Sizer.Add(boxSizer, 0)

        self.retail_grid =  Retail_Grid(self, name='inv_details_cost_grid')    
        
        MainSizer.Add(level1Sizer, 0, wx.ALL|wx.EXPAND, 5)
        MainSizer.Add(level2Sizer, 0)
        MainSizer.Add(self.retail_grid, 0)

        self.SetSizer(MainSizer,0)
        

           
class Retail_Grid(gridlib.Grid):
    """ Retail Grid to used in a few places """
 
    def __init__(self, parent, name, formatted='margin', debug=False):
        """Constructor"""
        gridlib.Grid.__init__(self, parent, style=wx.BORDER_SUNKEN, name=name)
        self.formatted = formatted.lower()
        
        #self.CreateGrid(12, 8)
        
        rowlabel_list = ['Standard Retail','Price Level (A)', 
                              'Price Level (B)', 'Price Level (C)',
                              'Price Level (D)','Price Level (E)', 
                              'Price Level (F)','Price Level (G)',
                              'Price Level (H)','Price Level (I)',
                              'Sale Price']
        
        if self.formatted == 'margin':
            collabel_list = ['Unit','Price', 'M', 'Margin %']
        
        if self.formatted == 'nomargin':
            collabel_list = ['Unit','Price']
        
        self.CreateGrid(len(rowlabel_list), len(collabel_list))
        self.SetDefaultCellAlignment(wx.ALIGN_CENTRE,wx.ALIGN_CENTRE)
        self.SetLabelFont(wx.Font(wx.FontInfo(9)))
        self.SetRowLabelSize(120)
        module_name = 'Inventory'
        bgcolor = Themes(module_name).GetColor('bg') #(0,0,255)
        whitetext = Themes(module_name).GetColor('text') #(255,255,255)
        cell_color = Themes(module_name).GetColor('cell') #(217,241,232)
        discountColor = (255,255,0)

        
        idx = 0
        for rowlabelset in rowlabel_list:
            self.SetRowLabelValue(idx, rowlabelset)
            idx += 1
            
        idx = 0    
        for collabelset in collabel_list:
            
            self.SetColLabelValue(idx,collabelset)
            minWidths_byColName = {'Price':90,'Unit':60}
            for key, new_width in minWidths_byColName.items():
                if self.GetColLabelValue(idx) == key:
                    old_width = self.GetColSize(idx)
                    if old_width > new_width:
                        increment = "decreased"
                    elif old_width < new_width:
                        increment = "increased"
                    else:
                        increment = "pointlessly changed"

                    
                    self.SetColSize(idx,new_width)

            idx += 1
        if self.formatted == 'margin':
            basic_list = ['1','$0.00','M','0.0000']
        
        if self.formatted == 'nomargin':
            basic_list = ['1','$0.00']
            
        maxrows = self.GetNumberRows()
        maxcols = self.GetNumberCols()
        for row in range(maxrows):
            for col in range(maxcols):
                self.SetCellValue(row, col, basic_list[col])
                if col in [1,3]:
                    self.SetCellAlignment(row, col, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE)
                    

        self.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.OnCellChange)
        GridOps(self.GetName()).GridAlternateColor(maxrows)
        wx.CallAfter(self.OnLoad, event='')
        
     
    def OnLoad(self, event):
        maxrows = self.GetNumberRows()
        maxcols = self.GetNumberCols()
        for row in range(maxrows):
            for col in range(maxcols):
                value = self.GetCellValue(row, col).strip('$')
                if col == 0:
                    if value == 1:
                        value = 1
                    val = self.RoundIt(Decimal(value), '1')
                if col == 1:
                    val = self.RoundIt(Decimal(value), '1.00')
                if col == 3:
                    val = self.RoundIt(Decimal(value), '1.000')
                if col == 2:
                    val = ' '
                self.SetCellValue(row, col, str(val))
                
                   
    def MarginUpdate(self, avg_cost, retail):
        ''' Readjust Margin in margin Column according to avg_cost '''
        gross_profit = Decimal(retail) - Decimal(avg_cost)
        deci_margin = Decimal(gross_profit) / Decimal(retail)
        percentage_margin = Decimal(deci_margin) * Decimal(100)
        
        return percentage_margin
        
        
                
    def OnCellChange(self,event):
       
        
        obj = event.GetEventObject()
        named = obj.GetName()
        row = event.GetRow()
        col = event.GetCol()

        colname = self.GetColLabelValue(col)
        self.Refresh()
        
        if 'inv_details_cost_grid' in named:
            raw_value = self.GetCellValue(row,col).strip()
            # numeric check
            if all(x in '0123456789.+-' for x in raw_value):
                # convert to float and limit to 2 decimals
                valued = Decimal(raw_value)
                if colname == 'Unit':
                    valued = RetailOps().DoRound(valued, '1')
                else:
                    valued = RetailOps().DoRound(valued, '1.00')
                
                self.SetCellValue(row,col,str(valued))
            else:
                basic_list = ['1','$0.00','Margin','0.000']
                self.SetCellValue(row,col,basic_list[col])
                GridFocusNGo(self.GetName(), row, col)
                return

        #

        avgcost = wx.FindWindowByName('details_avgcost_numctrl').GetCtrl()
        
        #if avgcost:

        for yy in range(self.GetNumberCols()):
            header = self.GetColLabelValue(yy)
            if 'Unit' in header:
                unit = self.GetCellValue(row,yy)
            if 'Markup %' in header:
                calcMargin = self.GetCellValue(row,yy)
            if 'Price' in header:
                retail_from = self.GetCellValue(row,yy)

        unit = self.GetCellValue(row, 0)
        if unit == '0':
            unit = '1'
            self.SetCellValue(row, 0, unit)  
               
        if colname == 'Margin %':
            new_margin = self.GetCellValue(row, col)
            retail = self.calcRetail(avgcost, new_margin, unit)
            
            new_retail = self.RoundIt(retail, '1.00')
            margin_format = self.RoundIt(new_margin, '1.000')
            
            self.SetCellValue(row, 1, str(new_retail))
            self.SetCellValue(row, 3, str(margin_format))

            
        if colname == 'Price':
            retail = self.GetCellValue(row, col)
            percentage_margin = self.calcMargin(avgcost, retail, unit)
            
            Margindot4 = self.RoundIt(percentage_margin,'1.000')
            self.SetCellValue(row,3,str(Margindot4))

        if colname == 'Unit':
            retail = self.GetCellValue(row, 1)
            margin = self.GetCellValue(row, 3)
            
            
            if unit == '0' or unit == '':
                unitd = self.RoundIt(unit, '1')
                self.SetCellValue(row, 0, unitd)
                
            newretail_almost = self.calcRetail(avgcost,margin,unit)
            newretail = RetailOps().DoRound(newretail_almost, '1.00')

            self.SetCellValue(row,1,str(newretail))

    def calcMargin(self, avgcost, retail, unit, debug=False):
        if unit == '0':
            unit = '1'    
        actual_retail = Decimal(retail)/Decimal(unit)
            
        gross_profit = Decimal(actual_retail) - Decimal(avgcost)
        if Decimal(actual_retail) == 0:
            percentage_margin = 0
        else:   
            deci_margin = Decimal(gross_profit) / Decimal(actual_retail)
            percentage_margin = Decimal(deci_margin) * Decimal(100)
        
        return percentage_margin
            
            
    def calcRetail(self, avgcost, margin, unit, debug=False):
        almost_margin = Decimal(1) - (Decimal(margin)/100)
        retail = Decimal(avgcost)/(almost_margin)
        retail = Decimal(retail) * Decimal(unit)
            
        #print 'retail 1 : ',retail
        if Decimal(margin) < 0:
            almost_margin = Decimal(1) - Decimal(margin)
            retail = Decimal(avgcost)/(almost_margin)
            retail = Decimal(retail) * Decimal(unit)
                
        #print 'retail 2 : ',retail
            
        return retail
    
    def RoundIt(self, oldmoney, unitd, debug=False):
        noPenny, rndScheme = False, '3'
        #(self.noPenny, self.rndScheme) = HU.LookupDB('TAX','tax_name','tax_tables','no_pennies_rounding, RNDscheme')
        
        if rndScheme == 0:
            rndScheme = 3
        rnd = str(rndScheme)
        
        roundtype = {'1':'ROUND_DOWN','2':'ROUND_HALF_UP','3':'ROUND_UP'}
        newMoney = Decimal(Decimal(oldmoney).quantize(Decimal(unitd), rounding=roundtype[rnd]))
    
        return newMoney

    def CurGridLine(self, blank=False):
        row = 0
        maxRows = self.GetNumberRows()
        for x in range(maxRows):
            value = self.GetCellValue(x,0)
            if value == '' or value is None:
                row = x - 1
                if blank is True:
                    row = x
                
                if row < 0:
                    row = 0    
                
                return row     

    def GetGridCursor(self):
        row = self.GetGridCursorRow()
        col = self.GetGridCursorCol()
    
        return row, col   
    
    def GridFocusNGo(self, row=None, col=0):
        if row == None:
            row = CurGridLine(gridname)+1
        self.SetFocus()
        wx.CallAfter(self.SetGridCursor, row, col) 


    def OnSave(self, event=None, upc=None):
        
        if upc is None:
            return
        
        QueryOps().CheckEntryExist('upc',upc, ['item_retails'])
        
        save_list = [(0, 0, 'item_retails', 'standard_unit'),
                     (0, 1, 'item_retails', 'standard_price'),
                     (1, 0, 'item_retails', 'level_a_unit'),
                     (1, 1, 'item_retails', 'level_a_price'),
                     (2, 0, 'item_retails', 'level_b_unit'),
                     (2, 1, 'item_retails', 'level_b_price'),
                     (3, 0, 'item_retails', 'level_c_unit'),
                     (3, 1, 'item_retails', 'level_c_price'),
                     (4, 0, 'item_retails', 'level_d_unit'),
                     (4, 1, 'item_retails', 'level_d_price'),
                     (5, 0, 'item_retails', 'level_e_unit'),
                     (5, 1, 'item_retails', 'level_e_price'),
                     (6, 0, 'item_retails', 'level_f_unit'),
                     (6, 1, 'item_retails', 'level_f_price'),
                     (7, 0, 'item_retails', 'level_g_unit'),
                     (7, 1, 'item_retails', 'level_g_price'),
                     (8, 0, 'item_retails', 'level_h_unit'),
                     (8, 1, 'item_retails', 'level_h_price'),
                     (9, 0, 'item_retails', 'level_i_unit'),
                     (9, 1, 'item_retails', 'level_i_price'),
                     (10, 0, 'item_retails', 'on_sale_unit'),
                     (10, 1, 'item_retails', 'on_sale_price')]
                     
        for row, col, table, field in save_list:
                ctrl = self.GetCellValue(row, col)
                ctrl = ctrl.strip('$')
                
                query = '''UPDATE {}
                           SET {}={}
                           WHERE upc=(?)'''.format(table, field, ctrl)
                data = (upc,)
                returnd = SQConnect(query, data).ONE()


    def Load(self, event=None, upc=None):
        
        retail_list = ['standard_price','level_(a)_price','level_(b)_price',
                       'level_(c)_price','level_(d)_price','level_(e)_price',
                       'level_(f)_price','level_(g)_price','level_(h)_price',
                       'level_(i)_price','on_sale_price']
        
        retails = RetailOps().RetailSifting(upc)
        
        for name in retail_list:
            for xx in range(self.GetNumberRows()):
                field = re.sub('[\(\)]','', name)
                key = re.sub('_price', '', name)
                key2 = re.sub('_', ' ', key)
                xlabel = self.GetRowLabelValue(xx)
                unitd = str(retails[field]['unit'])
                priced = str(retails[field]['price'])

                #print "xlabel : key2 = {} : {}".format(xlabel, key2)
                if key2 in xlabel.lower():
                    self.SetCellValue(xx,0, unitd)
                    self.SetCellValue(xx,1, priced)
                    #print "xlabel : key2 = {} : {} : ({} -- {})".format(xlabel, key2, retails[field][0],retails[field][1])

    def Clear(self):
        grid_default_list = [('Unit','1'),('Price','$0.00'),
                             ('Margin','Margin'),('Margin %','0.000')]
        
        for xx in range(self.GetNumberRows()):
            GridOps(self.GetName()).FillGrid(grid_default_list,row=xx)

        
        for xx in range(self.GetNumberRows()):
            for yy in range(self.GetNumberCols()):
                self.SetCellValue(xx,yy,'1')                   
        
####-------------
class POSLinks_Grid(gridlib.Grid):
    """ POS Sales Links Grid """
    def __init__(self, parent, name, debug=False):
        gridlib.Grid.__init__(self, parent, style=wx.BORDER_SUNKEN, name=name)
        
        
        poslinks_col_list = [('Item Number',255),
                             ('Description',350)]
                             
        self.EnableScrolling(True,True)
        self.DisableDragRowSize()
        self.SetRowLabelSize(0)
        self.CreateGrid(15,len(poslinks_col_list))
        idx = 0
        for label,sized in poslinks_col_list:
            self.SetColLabelValue(idx, label)
            self.SetColSize(idx, sized)
            idx += 1

        self.EnableEditing(True)
        self.SetLabelFont(wx.Font(wx.FontInfo(9)) )

        GridOps(self.GetName()).GridAlternateColor('')

        self.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.onPOSsalesLinks)

        
    def onPOSsalesLinks(self, event):
        obj = event.GetEventObject()
        named = obj.GetName()
        row = event.GetRow()
        col = event.GetCol()

        grid = wx.FindWindowByName(named)
        colname = grid.GetColLabelValue(col)
        
        if colname == 'Item Number':
            pass            
 
    def OnLoad(self, table, colheader, whereKey, whereValue):
        pass
        
    def OnSave(self, table, colheader, whereKey, whereValue):
        jsn = GridOps(self.GetName()).GRIDtoJSON()
        pout.v(f'POS LINKS JSON : {jsn}')

    
    def Clear(self):
        default_list = [('Item Number', ''),('Description','')]
        
        for xx in range(self.GetNumberRows()):
            GridOps(self.GetName()).FillGrid(default_list,row=xx)

           
class Order_Grid(gridlib.Grid):
    """ Retail Grid to used in a few places """
 
    def __init__(self, parent, name):
        """Constructor"""
        gridlib.Grid.__init__(self, parent, style=wx.BORDER_SUNKEN, name=name)
        self.tableName = None
        self.fieldName = None
        #self.CreateGrid(12, 8)
        rowlabel_list = []
        for month_num in range(1,13):
            month = datetime.date(2016, month_num, 1).strftime('%B')
            rowlabel_list.append(month)
            

        collabel_list = ['Order Point','Max Order']
        self.CreateGrid(len(rowlabel_list), len(collabel_list))
        self.SetDefaultCellAlignment(wx.ALIGN_RIGHT,wx.ALIGN_RIGHT)
        self.SetLabelFont(wx.Font(wx.FontInfo(9)) )
        self.SetRowLabelSize(120)
        for idx, rowlabelset in enumerate(rowlabel_list):
            
            self.SetRowLabelValue(idx, rowlabelset)

        GridOps(self.GetName()).GridAlternateColor('')

        for idx, collabelset in enumerate(collabel_list):
            
            self.SetColLabelValue(idx,collabelset)


        self.AutoSize()
        basic_list = [('Order Point','0'),('Max Order','0')]
        
        for xx in range(self.GetNumberRows()):
            gridFill = GridOps(self.GetName()).FillGrid(basic_list,row=xx)

    def OnSave(self, whereKey, whereValue):
        jsn = GridOps(self.GetName()).GRIDtoJSON()
        
        pout.v(f"ORDER GRID JSON : {jsn}")
        time.sleep(3)
        returnd = LookupDB(self.tableName).UpdateSingle(self.fieldName, jsn, whereKey, whereValue)

    def OnLoad(self, whereKey, whereValue):
        returnd = LookupDB(self.tableName).Specific(whereValue, whereKey, self.fieldName)
        pout.v(f"returnd : {returnd}")
        GridOps(self.GetName()).JSONtoGrid(returnd)



####----------------

class Activity_Grid(gridlib.Grid):
    """ Item Activity """
    def __init__(self, parent, name, debug=False):
        gridlib.Grid.__init__(self, parent, name=name, style=wx.BORDER_SUNKEN)
        
        self.EnableScrolling(False,True)
        self.DisableDragRowSize()
        colLabel_list =['Activity Date','Sales Volume', 'Sales Amount',
                        'Gross Profit']
        

        self.CreateGrid(20,len(colLabel_list))
        self.SetRowLabelSize(0)
        for idx,item in enumerate(colLabel_list):
            self.SetColLabelValue(idx, item)
            self.SetColSize(idx, 120)

        self.EnableEditing(False)
        self.SetLabelFont(wx.Font(wx.FontInfo(9)) )

        GridOps(self.GetName()).GridAlternateColor('')
        
        wx.CallAfter(self.OnLoad, event='')
        
    def OnLoad(self, event):
        maxrows = self.GetNumberRows()
        maxcols = self.GetNumberCols()
        
        for xx in range(maxrows):
            for yy in range(maxcols):
                col_label = self.GetColLabelValue(yy)
                val = self.GetCellValue(xx,yy)
                if not val:
                    continue 
                    
                if 'Activity Date' in col_label:
                    self.SetCellAlignment(xx,yy, wx.CENTER, wx.CENTER)
                    
                if 'Sales Volume' in col_label:
                    value = RetailOps().DoRound(val, '1.000')
                    self.SetCellValue(xx,yy, value)                 
                    self.SetCellAlignment(xx,yy,wx.CENTER, wx.CENTER)
                    
                if 'Sales Amount' in col_label:
                    value = RetailOps().DoRound(val, '1.00')
                    self.SetCellValue(xx,yy, value)             
                    self.SetCellAlignment(xx,yy, wx.RIGHT, wx.CENTER)
                    
                if 'Gross Profit' in col_label: 
                    value = RetailOps().DoRound(val, '1.000')
                    self.SetCellValue(xx,yy, value)             
                    self.SetCellAlignment(xx,yy, wx.RIGHT, wx.RIGHT)


class POS_Acct_Grid(gridlib.Grid):
    """ POS Acct Grid used at the POS Screen"""
    def __init__(self, parent, name, debug=False):
        
        gridlib.Grid.__init__(self, parent, style=wx.BORDER_SUNKEN, name=name)
        rowlabel_list = ['Account Number', 'Address Account', 'Name',
                         'Address 1', 'Address 2', 'City, State, Zip', 'Phone',
                         'A/R/Avail Credit', 'Discount %', 'Ship To']
        self.cntd = 0
        self.CreateGrid(len(rowlabel_list), 1)
        self.EnableScrolling(True, True)
        self.DisableDragRowSize()
        
        self.SetColLabelSize(0)
        self.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.SetLabelFont(wx.Font(wx.FontInfo(9)))
        self.SetColSize(0, MiscOps().WHSup(cell=250)[0])
        self.SetRowLabelSize(MiscOps().WHSup(cell=160)[0])
        self.SetLabelBackgroundColour(Themes().GetColor('bg'))
        self.SetLabelTextColour(Themes().GetColor('text'))
        
        readonly_list = ['Name', 'Address 1', 'Address 2', 'City, State, Zip',
                         'Avail Credit', 'Discount %', 'Ship To']
        for xx in range(self.GetNumberRows()):
                for item in readonly_list:
                    rowName = self.GetRowLabelValue(xx)
                    if item in rowName:
                        self.SetReadOnly(xx, 0, True)

                self.SetCellAlignment(xx, 0, wx.ALIGN_LEFT, wx.ALIGN_CENTER)
        for idx, item in enumerate(rowlabel_list):
            self.SetRowLabelValue(idx, item)

        GridOps(self.GetName()).GridAlternateColor('')

        self.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.OnClickGrid)
        randomId = wx.NewId()
        self.Bind(wx.EVT_MENU, self.onAddAccount, id=randomId)
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_ALT, ord('a'), randomId)])
        self.SetAcceleratorTable(accel_tbl)

        
    def OnClickGrid(self, event):        
        obj = event.GetEventObject()
        named = obj.GetName()
        row = event.GetRow()
        col = event.GetCol()
        #grid = wx.FindWindowByName(named)
        self.cntd += 1
            
        row = self.GetGridCursorRow()
        col = self.GetGridCursorCol()
            
        
        colname = self.GetColLabelValue(col)
        rowname = self.GetRowLabelValue(row)  
                
        subtract = False
        override = 'no'
        taxExempt = False
        print("ColName : ",colname)
        print(f"CLicked + {self.cntd}")
        if self.cntd == 2:
            pass    
        elif 'pos_acct_grid' in named:
           
            if rowname == 'Account Number':
                acctNum = self.GetCellValue(row,col).strip()
                print("Acct Number : ",acctNum)
                count_returnd = CustomerManagement(acctNum).SearchCount()
                if count_returnd == 0:
                    print('None Returnd')
                    self.SetCellValue(row,col,'')
                    GridOps(self.GetName()).GridFocusNGo(row, col)
                    return
                
                elif count_returnd > 0:
                    
                    #style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
                    
                    with CustLookupDialog(self, title="Customer Lookup") as dlg:
                        custPicked = None
                        dlg.ShowModal()
                        custPicked = dlg.itemPicked.upper().strip()
                    
                print("Customer Lookup D : ", custPicked)
                
    
                self.SetCustInfo(custPicked)
                
                infoTab = wx.FindWindowByName('InfoTab').Load(acctNum)
                
            if rowname == 'Address Account':
                print("ON CLICK ADDRESS ACCOUNT CHANGE")

                newAccount = grid.GetCellValue(1,0)
                print("New Account : ",newAccount)
                p = re.search('A[0-9]+',newAccount)
                if p is None:
                    return

                addr_num = p.group(0)
                
                fields = 'address0,city,state,zipcode,unit'
                returnd = QueryOps().LookupDB('address_accounts').Specific(addr_num,'addr_acct_num',fields)
                print('address change : {}'.format(returnd))
                (address0d, cityd, statd, zipd, unitd) = returnd
                acctInfo = SetAcctInfo(grid.GetName())
                acctInfo.address(address0d,unit=unitd)
                acctInfo.cistzi(cityd,statd,zipd)
                
                readonly_list = ['Name','Address 1','Address 2',
                                 'City, State, Zip','A/R/Avail Credit',
                                 'Discount %','Ship To']
                
                GridOps(self.GetName()).GridListReadOnly(readonly_list)
            
            print("DONE & DONE")
            GridOps('pos_transactions_grid').GridFocusNGo(0)
    
    
    
    def onAddAccount(self, event):
        print("On Add Account")
        
        dlg = CustomerAddDialog(self)
        dlg.ShowModal()
        
        try:
            
            self.custPicked = dlg.itemPicked
        
        except:
            print(f'Cust Picked : {self.custPicked}')
        
                    
        
        #self.custPicked = dlg.itemPicked
        print("Customer Add D : ",self.custPicked) 
        dlg.Destroy()
   
   
    def ReadOnly(self, readOnly_list):
        if readOnly_list is not None:
            for xx in range(self.GetNumberRows()):
                    for item in readOnly_list:
                        rowName = self.GetRowLabelValue(xx)
                        if item in rowName:
                            self.SetReadOnly(xx, 0, True)

    
        #self.acctNum = None
        #self.addrAcctNum = None
        #self.fullName = None
        #self.address1 = None
        #self.address2 = None
        #self.csz = None
        #self.discount = None
        #self.availCredit = None
        #self.acctInfoName = acctInfoName

    def SetCustInfo(self, custNum):
        self.custNum = custNum
        query = '''SELECT address_acct_num, rental_of 
                   FROM customer_basic_info
                   WHERE cust_num=(?)'''
        data = [self.custNum,]
        returnd = SQConnect(query, data).ONE()
        if not returnd == None:
            self.addrNum = returnd[0]
            rental_list = returnd[1]
            print('## returned : {}\n\tself.addr : {}\trental_list : {}'.format(returnd, self.addrNum, rental_list))           
            style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX)
            dlg = AddressSelectionDialog(self, 
                                         title="Address Selection", 
                                         style=style, addrList=rental_list)
            dlg.ShowModal()
                    
            try:
                self.addrNum = dlg.addrPicked.upper().strip()
            except:
                pass
                
            dlg.Destroy()
        
        
            #-- Customer Name
            query = '''SELECT full_name
                       FROM customer_basic_info 
                       WHERE cust_num=(?)'''
        
            data = [self.custNum,]
            returnd = SQConnect(query, data).ONE()
        
            self.full_name = returnd[0]
            ##-- Customer Address 
            query = '''SELECT address0, address2, city, state, zipcode 
                       FROM address_accounts
                       WHERE addr_acct_num=(?)'''
            data = [self.addrNum,]
        
            returnd = SQConnect(query, data).ONE()
        
            (addr0, addr2, city, state, zipcode) = returnd
            self.addr = addr0
            self.addr2 = addr2
            self.csz = '{}, {}  {}'.format(city, state, zipcode)
        
            #-- Customer Sales Options
            query = '''SELECT no_discount, fixed_discount, discount_amt
                       FROM customer_sales_options
                       WHERE cust_num=(?)'''
            data = [self.custNum,]
            returnd = SQConnect(query, data).ONE()
            (no_discount, fixdiscount, disc_amt) = returnd
            discount = None
            if fixdiscount == '1':
                discount = str(discount)
        
            if discount is not None:
                if not '%' in discount:
                    discount = '{}%'.format(discount)
        
            self.discount = discount
        
            self.availCredit = QueryOps().CheckCredit(custNum)
        
            #self.availCredit = availCredit    
            self.addrAcctNum = self.addrNum
        
            self.UpdateSetAcctInfo()
        
    def custAcctNum(self, acctNum=None):
        
        self.acctNum = acctNum
        self.UpdateSetAcctInfo()
        
    def addressAcctNum(self, addrAcctNum):
        
        
        self.addrAcctNum(self, addrAcctNum)
        self.UpdateSetAcctInfo()
            
    def name(self, firstName, lastName=None):
        
        
        self.fullName = firstName
        if lastName is not None:
            self.fullName = '{} {}'.format(firstName, lastName)
        
        self.UpdateSetAcctInfo()
        
    def address(self, addr0, addr1=None, addr2=None, unit=None, debug=False):
        
        if unit == '':
            unit = None
        
        
        self.address1 = addr0
        if addr1 is not None:
            if re.search('unit',addr1, re.I):
                self.address1 = '{}  {}'.format(addr0, addr1)
                
            self.address2 = addr1
        if addr2 is not None:
            if re.search('unit',addr2, re.I):
                self.address2 = '{}  {}'.format(addr1, addr2)
        
        if unit is not None:
            self.address1 = '{} UNIT {}'.format(addr0,unit)
            if re.search('unit', unit, re.I):
                self.address1 = '{} {}'.format(addr0, unit)
               
        self.UpdateSetAcctInfo()

        
    def cistzi(self, cityd, stated=None, zipd=None):
        
        
        self.csz = '{}, {}  {}'.format(cityd, stated, zipd)
        if stated is None:
            self.csz = cityd
            
        self.UpdateSetAcctInfo()

    def discountd(self, fixdiscount='0', discount=None):
        
        
        if fixdiscount == '0':
            discount = None
        
        discount = str(discount)
        if discount is not None:
            if not '%' in discount:
                discount = '{}%'.format(discount)
        
        self.discount = discount
        
        self.UpdateSetAcctInfo()
        

    def availCredit(self, availCredit=None):
        
        
        self.availCredit = availCredit    
        self.UpdateSetAcctInfo()
        
    def UpdateSetAcctInfo(self):
        
        
        #grid = wx.FindWindowByName(self.acctInfoName)
        
        typefind = str(type(self))
        if re.search('grid',typefind, re.I):
            
            listing = [('Account Number',self.custNum),
                       ('Address Account',self.addrAcctNum),
                       ('Name',self.full_name),
                       ('Address 1',self.addr),
                       ('Address 2', self.addr2),
                       ('City, State, Zip',self.csz),
                       ('A/R/Avail Credit',self.availCredit),
                       ('Discount %',self.discount)]
                   
            rows = self.GetNumberRows()
            cols = self.GetNumberCols()
            
            for header, value in listing:
                for row in range(rows):
                    label = self.GetRowLabelValue(row)
                    if label == header:
                        if value is not None:
                            self.SetCellValue(row, cols-1, str(value))        
        
        else:
            acctInfo = '{ad}\n{cs}'.format(ad=self.address0,
                                           cs=self.csz)

            wx.FindWindowByName(self.acctInfoName).GetCtrl( acctInfo)
