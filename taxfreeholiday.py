#!/bin/env python
#
#
# Tax Free Holiday
#
# import wxversion
# wxversion.select('2.8')

import wx
#import wx.calendar as cal
import wx.grid as gridlib
import sys,re
import faulthandler
#import psycopg2
import json
import pout
import xml.etree.cElementTree as ET
import wx.lib.masked as masked
import datetime
import handy_utils as HUD
from wx.lib.masked import TimeCtrl
from decimal import Decimal, ROUND_HALF_UP
import time
from db_related import SQConnect
from button_stuff import ButtonOps

#
class page_TaxHoliday_sheet(wx.Panel):
    def __init__(self, parent, ids=1, debug=False):
        """"""
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.ids = str(ids)
        debug = False
        lookupSizer = wx.BoxSizer(wx.VERTICAL)
        IconBar_list =[('Save', self.OnSave),
                       ('Exit', self.OnExitButton)]
        iconbar = HUD.IconPanel(self, iconList=IconBar_list)
        lookupSizer.Add(iconbar, 0, wx.ALL|wx.EXPAND, 3)

        level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        box = wx.StaticBox(self, -1, label='Name of TaxHoliday')
        boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
        ctrl = HUD.RH_TextCtrl(self, -1, name='taxfree_'+self.ids+'_txtctrl', size=(300,-1))
        boxSizer.Add(ctrl, 0)
        lookupSizer.Add(boxSizer, 0, wx.ALL|wx.CENTER, 5)

        startstop_list = [('Start Date','taxfree'+self.ids+'_start_datectrl'),
                          ('Stop Date','taxfree'+self.ids+'_stop_datectrl')]
        for label, name in startstop_list:
            box = wx.StaticBox(self, -1, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            ctrl = HUD.RH_DatePickerCtrl(self, -1, name=name, dt=wx.DateTime())
            boxSizer.Add(ctrl, 0, wx.ALL, 3)
            level1Sizer.Add(boxSizer, 0, wx.ALL, 3)    
            level1Sizer.Add((40,1), 1)
        
        cb = wx.CheckBox(self, -1, name='taxfree'+self.ids+'_active_checkbox', label='Enabled' )
        level1Sizer.Add(cb, 3)
        
        level1_2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        ctrl = HUD.RH_TextCtrl(self, -1, name='taxfree_textsearch')
        ctrl.SetHint('Search')
        btn = HUD.RH_Button(self, -1, name='taxfree_search_button')
        btn.Bind(wx.EVT_BUTTON, self.SearchSingle)

        level1_2Sizer.Add(ctrl, 0)
        level1_2Sizer.Add(btn, 0)        

        level1_5Sizer = wx.BoxSizer(wx.HORIZONTAL)
        cmbo_list = [('Dept','taxfree'+self.ids+'_department_combobox'),
                     ('Category','taxfree'+self.ids+'_category_combobox'),
                     ('Sub-Category','taxfree'+self.ids+'_subcategory_combobox')]
        
        for label, name in cmbo_list:
            box = wx.StaticBox(self, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            ctrl = wx.ComboBox(self, -1, choices=[], name=name)
            boxSizer.Add(ctrl, 0, wx.ALL, 3)
            level1_5Sizer.Add(boxSizer, 0, wx.ALL,3)
            
        btn = wx.Button(self, -1, label='Find && Add',name='taxfree'+self.ids+'_find_button')
        btn.Bind(wx.EVT_BUTTON, self.FindAdd)
        level1_5Sizer.Add(btn, 0, wx.ALL, 3)

        level2Sizer = wx.BoxSizer(wx.HORIZONTAL)

        
        grid = HUD.TaxHoliday_Grid(self, style=wx.BORDER_SUNKEN, size=(1000,500), name="taxfree"+self.ids+"_grid")
#        grid.EnableScrolling(True,True)
#        grid.DisableDragRowSize()
        # collabel_list = [('Item Number',200),('Description',575),('Price',200)]
        # grid.CreateGrid(100, len(collabel_list))
        # grid.SetDefaultCellAlignment(wx.ALIGN_LEFT,wx.ALIGN_CENTRE)
        # grid.SetLabelFont( wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.NORMAL) )
        # grid.SetRowLabelSize(0)
        # idx = 0
        # for label,sized in collabel_list:
        #     grid.SetColLabelValue(idx, label)         
        #     grid.SetColSize(idx, sized)
        #     idx += 1

        # HUD.GridOps(grid.GetName()).GridAlternateColor('')
        # grid.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.OnFind)
        # grid.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.OnRightClick)
        level2Sizer.Add(grid, 0, wx.ALL, 3)

    


        
        lookupSizer.Add(level1Sizer, 0, wx.ALL|wx.CENTER, 3)
        lookupSizer.Add(level1_2Sizer, 0, wx.ALL|wx.CENTER, 3)
        lookupSizer.Add(level1_5Sizer, 0, wx.ALL|wx.CENTER, 3)
        lookupSizer.Add(level2Sizer, 0, wx.ALL|wx.CENTER, 3)
        self.SetSizer(lookupSizer)
        self.Layout()
    
        wx.CallAfter(self.OnLoad, event='')

    def SearchSingle(self, event):
        ctrl = wx.FindWindowByName('taxfree_textsearch')
        value = ctrl.GetCtrl()

        self.item_model = HUD.InvMan(value).Run()
        if self.item_model is None:
            ctrl.SetCtrl('Not Found')
            ctrl.SelectAll()
        else:
            grid = wx.FindWindowByName('taxfree'+self.ids+'_grid')
            grid.AddItem(item=self.item_model)


    def OnLoad(self, event):            
        dcs_list = [('department','taxfree'+self.ids+'_department_combobox'),
                    ('category','taxfree'+self.ids+'_category_combobox'),
                    ('subcategory','taxfree'+self.ids+'_subcategory_combobox')]

        for column_name, ctrlName in dcs_list:
            query = 'SELECT {0} FROM organizations'.format(column_name)
            data = ''
            returnd = HUD.SQConnect(query, data).ALL()
            a = HUD.VarOps().DeTupler(returnd)
            
            list_ret = json.loads(a)
            pout.v(f'column Name : {column_name}')
            pout.v(f'ctrlName :  {ctrlName}')
            pout.v(f'returnd :  {returnd}')
            pout.v(f'list Ret :  {list_ret}')
            
            ctrl = wx.FindWindowByName(ctrlName).SetItems(list_ret)
    
        query = 'SELECT begin_date, end_date, upc, active FROM tax_holiday WHERE id="{}"'.format(self.ids)
        data = ''
        returnd = HUD.SQConnect(query, data).ALL()
        
        if returnd[0][2] is not None:
            pout.v(f'returnd :  {returnd[0]}')
            (begind, endd, upcd, actived) = returnd[0]
            
            pout.v(f'UPCD :  {upcd}')
            load_upc = json.loads(upcd)
            pout.v(f'LOAD_UPC :  {load_upc}')
            
            print('{} {} {}'.format('#'*40,self.ids,'#'*40))
            
            wx.FindWindowByName('taxfree'+self.ids+'_start_datectrl').SetCtrl(begind)
            wx.FindWindowByName('taxfree'+self.ids+'_stop_datectrl').SetCtrl(endd)
            wx.FindWindowByName('taxfree'+self.ids+'_active_checkbox').SetCtrl(actived)
            row = 0
            
            for item in load_upc:
                query = 'SELECT upc, description FROM item_detailed WHERE upc="{}"'.format(item)
                data = ''
                returnd = HUD.SQConnect(query, data).ONE()
                
                (upcd, desc) = returnd
                
                ret2 = HUD.RetailOps().RetailSifting(upcd)
                #ret2 = json.loads(retaild)
                setList = [('Item Number', upcd),('Description', desc),('Price',ret2['standard_price'][1])]
                HUD.GridOps('taxfree'+set.ids+'_grid').FillGrid(setList, row)
                row += 1
                pout.v(f'Ret2 :  {ret2}')
                

        print('{}{}{}'.format('='*40,self.ids,'='*40))
    
            
    def FindAdd(self, event):
        
        grid = wx.FindWindowByName('taxfree'+self.ids+'_grid')
        row = HUD.GridOps(grid.GetName()).CurGridLine(blank=True)
        dept = wx.FindWindowByName('taxfree'+self.ids+'_department_combobox').GetValue()
        cate = wx.FindWindowByName('taxfree'+self.ids+'_category_combobox').GetValue()
        subcate = wx.FindWindowByName('taxfree'+self.ids+'_subcategory_combobox').GetValue()
        if subcate == '' and cate == '' and dept == '':
            wx.MessageBox('at least a department must be selected', 'Info', wx.OK)
            return
        
        subcatd = ''
        catd = ''
        deptd = ''
        whereFrom = ''
        dataFrom = []    
        if subcate != '':
            subcatd = 'subcategory'
        if cate != '':
            catd = 'category'
        if dept != '':
            deptd = 'department'
        listd = [(subcatd, subcate),(catd, cate),(deptd, dept)]
        aa = len(listd)
        item_count = 0
        tcount = 0
        for item, value in listd:
            pout.v(f'item :  {item}')
            pout.v(f'value :  {value}')
            pout.v(f'aa :  {aa}')
            #print 'idx : ',idx
            if item_count >= 1 and tcount > 0:
                whereFrom += ' and '
            
            if item != '':
                whereFrom += '{}=\"{}\"'.format(item, value)
                item_count += 1
               
            
            tcount += 1
            
        
        
        query = 'SELECT upc FROM item_options WHERE {}'.format(whereFrom)
        data = ''
        returnd = HUD.SQConnect(query,data).ALL()
        
        pout.v(f'After returnd :  {returnd}')
        countd = len(returnd)
        maxrows = grid.GetNumberRows()
        
        if maxrows < countd:
            grid.AppendRows(countd)
            
        for item in returnd :
            query = 'SELECT upc, description FROM item_detailed WHERE upc=?'
            data = (item,)
            returndd = HUD.SQConnect(query, data).ALL()
            pout.v(f'returndd :  {returndd[0]}')
            
            
            (upc, desc) = returndd[0]
            
            #retaild = json.loads(retails)
            retaild = HUD.RetailOps().RetailSifting(upc)
            
            setList = [('Item Number',upc),('Description',desc),('Price',retaild['standard_price'][1])]
            #print setList
            HUD.GridOps(grid.GetName()).FillGrid(setList, row)
            grid.SetCellAlignment(row,2, wx.ALIGN_CENTER, wx.ALIGN_CENTER)
            row += 1   
            
        
        #if cate is not None or cate != '':
        #    for upc, cated, subcated in returnd:
                              
    
            
    
    def OnSave(self, event):
        beginDate = wx.FindWindowByName('taxfree'+self.ids+'_start_datectrl').GetCtrl()
        endDate = wx.FindWindowByName('taxfree'+self.ids+'_stop_datectrl').GetCtrl()
        activd = wx.FindWindowByName('taxfree'+self.ids+'_active_checkbox').GetCtrl()
        grid = wx.FindWindowByName('taxfree'+self.ids+'_grid')
        maxrows = HUD.GridOps(grid.GetName()).CurGridLine(blank=True)
        pout.v(f'Max Rows :  {maxrows}')
        valued = []
        for xx in range(maxrows):
            LabelKey = grid.GetRowLabelValue(xx).replace(" ", "_").lower()
            #header = grid.GetColLabelValue(yy)
            value = grid.GetCellValue(xx, 0)
            valued.append(value)
            pout.v(f'Row value :  {value}')

        upc_list = json.dumps(valued)
        
        
        query = 'update tax_holiday SET begin_date=?, end_date=?, upc=?, active=? WHERE id=?'
        data = (beginDate, endDate, upc_list, activd, self.ids,)
        returnd = HUD.SQConnect(query,data).ONE()
         
        
    def OnExitButton(self, event):
        item = wx.FindWindowByName('Inventory_Frame').Close()
        
        
##


class StartPanel(wx.Panel):
    """"""
    def __init__(self, parent, debug=False):
        wx.Panel.__init__(self, parent=parent)
        
        lookupSizer = wx.BoxSizer(wx.VERTICAL)
        
         
        IconBar_list =[('Save', ButtonOps().Icons('save'), self.OnSave),
                       ('Undo', ButtonOps().Icons('undo'), self.OnUndo),
                       ('Add', ButtonOps().Icons('add'), self.OnAdd),
                       ('Exit', ButtonOps().Icons('Exit'), self.OnExitButton)]
        
        IconBox = wx.StaticBox(self)
        
        IconBarSizer = wx.StaticBoxSizer(IconBox, wx.HORIZONTAL)        
        xx = 0        
        for name,iconloc,handler in IconBar_list:
            icon = wx.BitmapButton(self, wx.ID_ANY, wx.Bitmap(iconloc), style=wx.BORDER_NONE)
            icon.Bind(wx.EVT_BUTTON, handler)
            IconBarSizer.Add((80,1),0)
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
        
        level1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        startstop_list = [('Start Date','taxfree_start_datectrl'),('Stop Date','taxfree_stop_datectrl')]
        for label, name in startstop_list:
            box = wx.StaticBox(self, -1, label=label)
            boxSizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)
            ctrl = HUD.RH_DatePickerCtrl(self, -1, name=name, dt=wx.DateTime())
            boxSizer.Add(ctrl, 0, wx.ALL, 3)
            level1Sizer.Add(boxSizer, 0, wx.ALL, 3)    

        level2Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        grid = gridlib.Grid(self, style=wx.BORDER_SUNKEN, size=(1000,500), name="taxfree_grid")
#        grid.EnableScrolling(True,True)
#        grid.DisableDragRowSize()
        collabel_list = [('Item Number',200),('Description',575),('Prompt',200)]
        grid.CreateGrid(100, len(collabel_list))
        grid.SetDefaultCellAlignment(wx.ALIGN_CENTRE,wx.ALIGN_CENTRE)
        grid.SetLabelFont( wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.NORMAL) )
        grid.SetRowLabelSize(0)
        idx = 0
        for label,sized in collabel_list:
            grid.SetColLabelValue(idx, label)         
            grid.SetColSize(idx, sized)
            idx += 1

        HUD.GridOps(grid.GetName()).GridAlternateColor('')
        
        level2Sizer.Add(grid, 0, wx.ALL, 3)

    


        lookupSizer.Add(IconBarSizer, 0, wx.ALL|wx.EXPAND, 3)
        lookupSizer.Add(level1Sizer, 0, wx.ALL|wx.CENTER, 3)
        lookupSizer.Add(level2Sizer, 0, wx.ALL|wx.CENTER, 3)
        self.SetSizer(lookupSizer)
        self.Layout()
    
    def OnAdd(self, event):
        pass
    
    def OnFind(self, event):
        pass
    
    def OnUndo(self, event):
        pass
    
    def OnSave(self, event):
        pass
        
    def OnExitButton(self, event):
        item = wx.FindWindowByName('Inventory_Frame').Close()
            

class InventoryScreen(wx.Frame):
    def __init__(self, debug=False):
        style = wx.DEFAULT_FRAME_STYLE #& (wx.CLOSE_BOX) & (wx.MAXIMIZE_BOX) & (wx.MINIMIZE_BOX)
        wx.Frame.__init__(self, None, -1, "Tax Free Holiday Worksheet", size=(1200,800), style=style)
                
        sizer = wx.BoxSizer(wx.VERTICAL)

        nestednb = wx.Notebook(self, wx.ID_ANY, name='taxHolidays_notebook')

        page1 = page_TaxHoliday_sheet(nestednb, ids=1)
        page2 = page_TaxHoliday_sheet(nestednb, ids=2)
        page3 = page_TaxHoliday_sheet(nestednb, ids=3)
        page4 = page_TaxHoliday_sheet(nestednb, ids=4)
        page5 = page_TaxHoliday_sheet(nestednb, ids=5)
        page6 = page_TaxHoliday_sheet(nestednb, ids=6)
        
        nestednb.AddPage(page1, "Tax Holiday 1")
        nestednb.AddPage(page2, "Tax Holiday 2")
        nestednb.AddPage(page3, "Tax Holiday 3")
        nestednb.AddPage(page4, "Tax Holiday 4")
        nestednb.AddPage(page5, "Tax Holiday 5")
        nestednb.AddPage(page6, "Tax Holiday 6")
        
        sizer.Add(nestednb, 1, wx.ALL|wx.EXPAND, 5)
        #self.SetSizer(sizer)
        #self.Layout()

        
 
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(sizer, 1, wx.EXPAND)
        
        self.SetSizer(self.sizer)
        
 

        self.Layout()

       
  
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = InventoryScreen()
    frame.Centre()
    frame.SetName('TaxHoliday_Frame')
    frame.Show()
    app.MainLoop()        
