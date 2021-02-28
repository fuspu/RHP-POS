#!/usr/bin/env python2
#
#
#
#
#import wxversion
#wxversion.select('2.8')


import wx,re,os 
print('wx : {}'.format(wx.version()))

#import wx.calendar as cal
import wx.grid as gridlib
import sys
import faulthandler
import sqlite3
import json
import xml.etree.cElementTree as ET
import datetime
from wx.lib.masked import TimeCtrl
import wx.lib.masked as masked
from decimal import Decimal, ROUND_HALF_UP
import wx.lib.inspection
import HandyUtilities as HUD




class StartPanel(wx.Panel):
    def __init__(self, parent, debug=False):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.dbg = HUD.Debugger(debug)
        
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        MenuSizer = wx.BoxSizer(wx.HORIZONTAL)
        if __file__ == "About.py":
            iconList = [('ExitButton', HUD.ButtonOps().Icons('exit'),    self.OnExitButton)]
            for name,iconloc,handler in iconList:
                icon = wx.BitmapButton(self, wx.ID_ANY,
                                        wx.Bitmap(iconloc), 
                                        name = name, 
                                        style = wx.BORDER_NONE)
                icon.Bind(wx.EVT_BUTTON, handler)
                MenuSizer.Add(icon, 0, wx.RIGHT, 5)
        
        MainSizer.Add(MenuSizer, 0, wx.ALL, 5)
        
        txt = wx.StaticText(self, -1, label='RHP-POS started as a Project to help me learn Python.  \nThe original design was based on the POS software my job is using, then it slowly morphed into this.')
        MainSizer.Add(txt,0,wx.ALL, 5)
        
        
        line = wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL, size=(1200,5))
        MainSizer.Add(line, 0, wx.ALL, 5)
        
        txt = wx.StaticText(self, -1, label='Credits')
        txt.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, "Ubuntu"))
        MainSizer.Add(txt, 0, wx.ALIGN_CENTER, 5)
        
        IconList = ["Icon made by Pixel perfect from www.flaticon.com","Icon made by Surang from www.flaticon.com"]
        for credit in IconList:
            txt = wx.StaticText(self, -1, credit)    
            MainSizer.Add(txt, 0)
        
        
        MainSizer.Add((100,100))
        
        
        self.SetSizer(MainSizer)
        
        self.Layout()
        
    def OnPrintButton(self, event):
        pass
        
    def OnExitButton(self, event):
        frame = wx.FindWindowByName('RHP_POS_Frame')
        frame.Close()
        
        
        

    
    def ReportsOnPageChanged(self, event):
        pass
        

class AboutScreen(wx.Frame):
    def __init__(self):
        style = wx.DEFAULT_FRAME_STYLE & (wx.CLOSE_BOX) & (~wx.MAXIMIZE_BOX) & (~wx.MINIMIZE_BOX)
        wx.Frame.__init__(self, None, -1, "RHP Maintenance", size=(1200,700), style=style)
        debug = False
        self.panel_one = StartPanel(self)
       
#        wx.lib.inspection.InspectionTool().Show()

 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel_one, 1, wx.EXPAND,5)
        
        self.SetSizer(sizer)
        
 

        self.Layout()

       
  
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = AboutScreen()
    frame.Centre()
    frame.SetName('RHP_POS_Frame')
    frame.Show()
    app.MainLoop()        
