import pout
import wx


class IconList(object):
    def __init__(self):
        self.a_dict = {'save': '', 
                       'add': '',
                       'exit': '',
                       'find': '',
                       'undo': '',
                       'delete': '',
                       'print': '朗',
                       'empty': '',
                       'refresh': '累',
                       'receiving': '',
                       'pdf': '',
                       'logo': '_',
                       'addrmaint': ''}
    
    def getFont(self):
        fontpath = './fonts/DaddyTimeMono Nerd Font Complete Mono.ttf'
        wx.Font.AddPrivateFont(fontpath)
        f = wx.Font(pointSize=12,
                    family=wx.FONTFAMILY_DEFAULT,
                    style=wx.FONTSTYLE_NORMAL,
                    weight=wx.FONTWEIGHT_NORMAL,
                    underline=False,
                    faceName="DaddyTimeMono",
                    encoding=wx.FONTENCODING_DEFAULT)
        f.SetPixelSize((35,35))
        return f

    def getIcon(self, icon_name):
        return self.a_dict[icon_name]


class RH_Icon(wx.Button):
    def __init__(self, *args, **kwargs):
        typd = kwargs.pop('icon')
        save = IconList().getIcon(typd.lower())
        wx.Button.__init__(self, *args, **kwargs)
        self.SetLabel=save
        #self.SetBitmap(wx.Bitmap(save))

class RH_Button(wx.Button):
    def __init__(self, *args, **kwargs):
        wx.Button.__init__(self, *args, **kwargs) 
        self.listd = None
        self.tableName = None
        self.fieldName = None
        self.DefaultTable = None
        self.DefaultField = None
        self.cnt = 0
        #pout.v(f'Listd : {self.listd} ; CNT : {self.cnt}')
        self.Bind(wx.EVT_BUTTON, self.NextLabel)


class LoadSaveList(object):
    def __init__(self):
        self.listd = []
    
    def Add(self, item):
        self.listd.append(item)
    
    def Show(self):
        pout.v(self.listd)

    def Get(self):
        return self.listd



class IconPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        '''Displays the Icon Panel options.'''
        iconList = kwargs.pop('iconList')
        wx.Panel.__init__(self, *args, **kwargs)
        IconBarSizer = wx.BoxSizer(wx.HORIZONTAL)
        a = IconList()
        f = a.getFont()
        a_dict = {'save': '', 
                 'add': '',
                 'exit': '',
                 'find': '',
                 'undo': '',
                 'delete': '',
                 'print': '朗',
                 'empty': '',
                 'refresh': '累',
                 'receiving': '',
                 'pdf': '',
                 'logo': '{',
                 'addrmaint': f''}
        
        for name, handler in iconList:
            iconloc = a.getIcon(name.lower())
            icon = wx.Button(self, wx.ID_ANY, label=iconloc, style=wx.BORDER_NONE)
            icon.SetFont(f)
            icon.Bind(wx.EVT_BUTTON, handler)
            iconpos = [('find',(0,1)),
                       ('left',(0,2)),
                       ('right',(0,3)),
                       ('add',(0,4)),
                       ('undo',(0,5)),
                       ('save',(0,6)),
                       ('delete',(0,7)),
                       ('refresh',(0,8)),
                       ('receiving',(0,9)),
                       ('addrmaint',(0,10)),
                       ('print',(0,11)),
                       ('exit',(0,12))]
            
            iconsnum = len(iconList)
            
            distd = iconsnum
            for typd, posit in iconpos:
                if typd in name.lower():
                    flagnorm = wx.EXPAND|wx.ALL
                    span=(0,0)
                    if 'exit' in typd:
                        #IconBarSizer.Add((20,20), (0,21))
                        span=(0,distd)
                        flagnorm = wx.EXPAND
                    #IconBarSizer.Add(icon, posit, span=span, flag=flagnorm, border=5)
                    IconBarSizer.Add(icon, 0, flagnorm) 
        self.SetSizer(IconBarSizer)
        #self.Layout()


class EventOps(object):
    def __init__(self):
        '''Collection of Events.'''
        

    def OnNumbersOnly(self, event):
            """
            check for numeric entry accepted result is in self.value
            """
            
            valued = event.GetEventObject()
            raw_value = valued.GetValue().strip()
            if raw_value == '' or raw_value == None:
                raw_value = '0'
            named = valued.GetName()
            edit_txtctrl = wx.FindWindowByName(named)
            # numeric check
            if re.match('[Xx]', raw_value):
                raw_value = "10"
                #edit_txtctrl.ChangeValue(str(raw_value))


            if all(x in '0123456789.+-/' for x in raw_value):
                # convert to float and limit to 2 decimals
                value = Decimal(raw_value)
                if 'discount' in named:
                    if value > 100:
                        value = 10

                edit_txtctrl.ChangeValue(str(value))
            #else:
            #    edit_txtctrl.ChangeValue("")
            #    edit_txtctrl.SetToolTip(wx.ToolTip("NUMBERS ONLY!!!"))


    def LCGetSelected(self, event):
        debug=False
        obj = event.GetEventObject()
        named = obj.GetName()
        item_id = obj.GetFirstSelected()
        
        objText = obj.GetItemText(item_id)
        return item_id, objText

    def ListBoxOnAddButton(self, event):
        
        obj = event.GetEventObject()
        print(f'OBJ : {obj}')
        
        addbutton_name = obj.GetName()
        print(f'addbutton name : {obj.GetName()}')
        listbox_name = re.sub('_addbutton', '', addbutton_name)
        tc_name = re.sub('_addbutton', '_txtctrl', addbutton_name)
        lc_txtctrl = wx.FindWindowByName(tc_name)
        if not lc_txtctrl.GetValue():
            return
        print(f'List Box Name : {listbox_name}')
        listbox = wx.FindWindowByName(listbox_name)
        num_altlookups = listbox.GetCount()
        

        tobe_searched = lc_txtctrl.GetValue()
        has_found = listbox.FindString(tobe_searched)
        addbutton = wx.FindWindowByName(addbutton_name)
        if has_found != -1:
            
            foundIndex = has_found
            listbox.EnsureVisible(foundIndex)
            addbutton.SetBackgroundColour('Red')
            lc_txtctrl.Clear()
            lc_txtctrl.SetFocus()
        else:
            
            addbutton.SetBackgroundColour('Green')
            listbox.Append(lc_txtctrl.GetValue().upper())
            lc_txtctrl.Clear()
            lc_txtctrl.SetFocus()

        allstrings = listbox.GetStrings()
        


    def ListBoxSelectItem(self, event):
        obj = event.GetEventObject()
        obj_name = obj.GetName()
        tc_name = re.sub('_listbox', '_listbox_txtctrl', obj_name)
        addbutton_name = re.sub('_listbox', '_listbox_addbutton', obj_name)
        rembutton_name = re.sub('_listbox', '_listbox_rembutton', obj_name)
        listbox_name = obj_name
        
        lc_txtctrl = wx.FindWindowByName(tc_name)
        addbutton = wx.FindWindowByName(addbutton_name)
        rembutton = wx.FindWindowByName(rembutton_name)
        listbox = wx.FindWindowByName(listbox_name)
        selection = listbox.GetStringSelection()
        wx.FindWindowByName(tc_name).SetCtrl(selection)


    def ListBoxOnRemoveButton(self, event):
        obj = event.GetEventObject()
        rembutton_name = obj.GetName()
        tc_name = re.sub('_rembutton', '_txtctrl', rembutton_name)
        addbutton_name = re.sub('_rembutton', '_addbutton', rembutton_name)
        listbox_name = re.sub('_rembutton', '', rembutton_name)
        
        
        lc_txtctrl = wx.FindWindowByName(tc_name)
        addbutton = wx.FindWindowByName(addbutton_name)
        rembutton = wx.FindWindowByName(rembutton_name)
        listbox = wx.FindWindowByName(listbox_name)

        tobe_removed = lc_txtctrl.GetValue()
        currentItem = listbox.FindString(tobe_removed)
        
        if currentItem != -1:
            listbox.EnsureVisible(currentItem)
            listbox.Delete(currentItem)
            

        lc_txtctrl.Clear()
        lc_txtctrl.SetFocus()

        
    def Capitals(self, event):
        """ Capitalize First Letters """
        valued = event.GetEventObject()
        raw_value = valued.GetValue()
        named = valued.GetName()
        edit_ctrl = wx.FindWindowByName(named)
        new_value = raw_value.title()
        exempt_list = [' llc', ' ltd', ' corp ', 'sr ',
                    ' S.R. ', ' rv ', 'pk', 'x']
        for exempt in exempt_list:
            if re.search(exempt, new_value, re.I):
                new_exempt = exempt.upper()
                new_value = re.sub(exempt, new_exempt, new_value, flags=re.I)
                
        if 'combobox' in named:
            edit_ctrl.SetValue(new_value)
        if 'txtctrl' in named:
            edit_ctrl.ChangeValue(new_value)


    def CheckMeasurements(self, event):
        valued = event.GetEventObject()
        raw_value = valued.GetValue()
        named = valued.GetName()
        edit_ctrl = wx.FindWindowByName(named)

        repl_list = [('"', 'in'), ("'", 'ft')]
        for start, finish in repl_list:
            if re.search(start, raw_value, re.I):
                raw_value = re.sub(start, finish, raw_value)
                

        new_value = raw_value
        if 'combobox' in named:
            edit_ctrl.SetValue(new_value)
        if 'txtctrl' in named:
            edit_ctrl.ChangeValue(new_value)
