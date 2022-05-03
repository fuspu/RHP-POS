import re
import wx
from decimal import Decimal
import pout

class EventOps(object):
    def __init__(self):
        '''Collection of Events.'''
        
    def FormatPhoneNumber(self, event):
        obj = event.GetEventObject()
        val = obj.GetValue().strip()
        if len(val) == 3:
            pout.v(len(val))
            new_val = f'({val})'
            print(f"new_val = '({val})'")
           
        elif len(val) == 6:
            pout.v(len(val))
            new_val = f'({val[1]}{val[2]}{val[3]}) {val[5]}'
            print(f"new_val = '({val[1]}{val[2]}{val[3]}) {val[5]}'")
        

        elif len(val) == 10:
            pout.v(len(val))
            new_val = f'({val[1]}{val[2]}{val[3]}) {val[6]}{val[7]}{val[8]}-{val[9]}'
            print(f"new_val = '({val[1]}{val[2]}{val[3]}) {val[6]}{val[7]}{val[8]}-{val[9]}'")
            
        elif not re.search('([0-9]|\-.|\(.|\(\)|\).)', val):
            new_val = ''
            
        else:
            pout.v(len(val))
            new_val = val
            print(f"new_val = {val}")
            

        obj.ChangeValue(new_val)
        obj.SetInsertionPointEnd() 

    def OnNumbersOnly(self, event):
            """
            check for numeric entry accepted result is in self.value
            """
            valued = event.GetEventObject()
            raw_value = valued.GetValue().strip()
            print(f'raw_value : {raw_value} ')
            
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
