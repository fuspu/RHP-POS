import wx
import re
import pout
import json
import wx.lib.masked as masked
from db_ops import SQConnect, LookupDB
from decimal import Decimal, ROUND_HALF_UP
from ObjectListView import ObjectListView, ColumnDefn


class VarOps(object):
    def __init__(self):
        pass


    def CheckJson(self, jsond):
        a = self.is_json(jsond)
        if a is True:
            return json.loads(jsond)
        else:
            return json

    def is_json(self, myjson):
        try:
            json_object = json.loads(myjson)
        except ValueError as e:
            return False
        except TypeError as e:
            return False
        
        return True

#---------------------------------------------------------------------------------------
class LoadSaveList(object):
    def __init__(self):
        self.listd = ()
        self.lsl_dict = {}

    def Add(self, item):
        self.listd += (item,)
    
    def Show(self):
        pout.v(self.listd)

    def Get(self):
        return self.listd

    def To_Dict(self):
        selects = ()
        for i in self.listd:
            tableName = i.tableName
            fieldName = i.fieldName
            if not tableName in self.lsl_dict:
                self.lsl_dict[tableName] = {}
            
            selects += (fieldName,)
            self.lsl_dict[tableName].update({'selects':selects}) 
            if not fieldName in self.lsl_dict[tableName]:
                self.lsl_dict[tableName][fieldName] = {}
            
            self.lsl_dict[tableName][fieldName] = {'get':i.GetCtrl, 'sqlfile':i.sqlfile, 'saveAs':i.saveAs, 'loadAs':i.loadAs, 'set':'', 'obj':i}

        return self.lsl_dict

    def GetSelectQD(self, tuple_of_fields, where=None):
        lsl = self.To_Dict()
        selects = ','.join(tuple_of_fields)
        for tableName in lsl:
            if tuple_of_fields[0] in lsl[tableName]:
                if where is None:
                    q = f'SELECT {selects} FROM {tableName}'
                    d = ()
                else:
                    q = f'SELECT {selects} FROM {tableName} WHERE {where}=?'
                    d = (lsl[tableName][where]['get'],)
                
                sqlfile = lsl[tableName][tuple_of_fields[0]]['sqlfile']

                # pout.v(sqlfile)
                return q, d, sqlfile

    def UpdateQD(self, tuple_of_fields, where=None):
        lsl = self.To_Dict()
        selects = ','.join(tuple_of_fields)
        setd = ()
        vald = ()
        for tableName in lsl:
            for fld in tuple_of_fields:
                setd += (f'{fld}=?',)
                vald += (lsl[tableName][fld]['get'],)
            
            update_fields = ','.join(setd)
            vald += (lsl[tableName][where]['get'],)
            #update_vals = ','.join(vald)

            for tableName in lsl:
                if tuple_of_fields[0] in lsl[tableName]:
                    q = f'UPDATE {tableName} SET {update_fields} WHERE {where}=?'
                    d = vald
                    sqlfile = lsl[tableName][tuple_of_fields[0]]['sqlfile']
                    # print(q, d, sqlfile)
                    return q, d, sqlfile





#---------------------------------------------------------------------------------------
class LoadSaveDict(dict):
    def __init__(self):
        self = dict()

    def add(self, key, value):
        self[key] = value



#---------------------------------------------------------------------------------------
class RH_LoadSaveSelection(object):
    def __init__(self, *args, **kwargs):
        self.tableName = None
        self.fieldName = None
        self.sqlfile = None
        
    def OnLoad(self, whereField, whereValue):
        returnd = LookupDB(self.tableName).Specific(whereValue, whereField, self.fieldName)
        a = VarOps().GetTyped(returnd)
        if 'tuple' in a:
            returnd = returnd[0]
        if returnd is None:
            returnd = 0
        try:
            self.SetSelection(returnd)
        except TypeError as e:
            pout.v(e)

    def OnSave(self, whereField, whereValue):
        a = self.GetSelection()
        try:
            returnd = LookupDB(self.tableName).UpdateSingle(self.fieldName, a, whereField, whereValue)
        except:
            pout.v(f'Table : {self.tableName} ; Field : {self.fieldName} ; WhereField : {whereField} ; whereValue: {whereValue}')

    def GetCtrl(self):
        return self.GetSelection()

    def SetCtrl(self, value):
        self.SetSelection(value)

    def Clear(self):
        self.SetSelection(0)
#---------------------------------------------------------------------------------------
class RH_LoadSaveNum(object):
    def __init__(self, *args, **kwargs):
        self.tableName = None
        self.fieldName = None
        self.sqlfile = None
        

    def OnLoad(self, whereField, whereValue):
        returnd = LookupDB(self.tableName).Specific(whereValue, whereField, self.fieldName)
        a = VarOps().GetTyped(returnd)
        #pout.v(a)
        if 'tuple' in a:
            returnd = returnd[0]
            #pout.v('Tuple Unwound')
        
        a = VarOps().GetTyped(returnd)
        if 'decimal' in a:
            #pout.v('Convert Decimal -> float')
            returnd = float(returnd)
        
        if returnd is None:
            returnd = 0
        
        a = VarOps().GetTyped(returnd)
        #pout.v(a)
        self.SetValue(returnd)

    def OnSave(self, whereField, whereValue):
        a = self.GetValue()
        
        if a is True:
            a = 1
        if a is False:
            a = 0
        try:
            returnd = LookupDB(self.tableName).UpdateSingle(self.fieldName, a, whereField, whereValue)
        except:
            pout.v(f'Table : {self.tableName} ; Field : {self.fieldName} ; WhereField : {whereField} ; whereValue: {whereValue}')

    def GetCtrl(self):
        return self.GetValue()

    def SetCtrl(self, value):
        self.SetValue(int(Decimal(value)))

    def Clear(self):
        self.SetValue(0)
#--------------------------------------------------------------------------------------
class RH_LoadSaveDate(object):
    def __init__(self, *args, **kwargs):
        self.tableName = None
        self.fieldName = None
        self.sqlfile = None
        

    def OnLoad(self, whereField, whereValue):
        returnd = LookupDB(self.tableName).Specific(whereValue, whereField, self.fieldName)
        a = VarOps().GetTyped(returnd)
        if 'tuple' in a:
            returnd = returnd[0]
        
        if returnd is None:
            returnd = datetime.datetime.strptime('01/01/1969', '%m/%d/%Y')
        self.SetValue(returnd)

    def OnSave(self, whereField, whereValue):
        a = self.GetValue()
        pout.v(f'Date Picker Ctrl : {a}')
        b = a.FormatISODate()
        pout.v(f'Date Picker Crtl ISO Date : {b}')
        try:
            returnd = LookupDB(self.tableName).UpdateSingle(self.fieldName, b, whereField, whereValue)
        except:
            pout.v(f'Table : {self.tableName} ; Field : {self.fieldName} ; WhereField : {whereField} ; whereValue: {whereValue}')

    def GetCtrl(self):
        a = self.GetValue()
        b = a.FormatISODate()
        return b

    def SetCtrl(self, value):
        
        self.SetValue(value)

    def Clear(self):
        deflt = wx.DateTime(4,3,1968)
        self.SetValue(deflt)

#--------------------------------------------------------------------------------------
class RH_LoadSaveTime(object):
    def __init__(self, *args, **kwargs):
        self.tableName = None
        self.fieldName = None
        self.sqlfile = None
        self.saveAs = 'str'
        self.loadAs = 'str'

                     
    def CheckSaveLoadAs(self, value, typd):
        conv = self.loadAs
        if typd == 'save':
            conv = self.saveAs

        if 'str' in conv:
            value = str(value)
        elif 'int' in conv:
            value = int(value)
        elif 'float' in conv:
            value = float(value)
        elif 'decimal' in conv:
            value = Decimal(value)
        
        return value

    def GetCtrl(self):
        a = self.GetValue()
        a = self.CheckSaveLoadAs(a, 'save')

        return a
    
    def SetCtrl(self, value):
        if value is None:
            value = ''
        a = self.CheckSaveLoadAs(value, 'load')    
        self.SetValue(a)

    def OnLoad(self, whereField, whereValue):
        returnd = LookupDB(self.tableName).Specific(whereValue, whereField, self.fieldName)
        a = VarOps().GetTyped(returnd)
        pout.v(f'OnLoad Time Returnd : {returnd}')
        if returnd is None:
            returnd = datetime.datetime.strptime('01/01/1969', '%m/%d/%Y')

        date_obj = datetime.datetime.strptime(returnd, '%d-%m-%Y %H:%M:%S')
        self.SetValue(returnd)

    def OnSave(self, whereField, whereValue):
        a = self.GetValue()
        date_str = a.strftime('%d-%m-%Y %H:%M:%S')
        try:
            returnd = LookupDB(self.tableName).UpdateSingle(self.fieldName, b, whereField, whereValue)
        except:
            pout.v(f'Table : {self.tableName} ; Field : {self.fieldName} ; WhereField : {whereField} ; whereValue: {whereValue}')


    def GetCtrl(self):
        a = self.GetValue()
        b = a.FormatIsoTime()
        return b

    def SetCtrl(self, value):
        self.SetValue(value)

    def Clear(self):
        self.SetValue()
#--------------------------------------------------------------------------------------
class RH_LoadSavePath(object):
    def __init__(self, *args, **kwargs):
        self.tableName = None
        self.fieldName = None
        self.sqlfile = None
        self.saveAs = 'str'
        self.loadAs = 'str'

                     
    def CheckSaveLoadAs(self, value, typd):
        conv = self.loadAs
        if typd == 'save':
            conv = self.saveAs

        if 'str' in conv:
            value = str(value)
        elif 'int' in conv:
            value = int(value)
        elif 'float' in conv:
            value = float(value)
        elif 'decimal' in conv:
            value = Decimal(value)
        
        return value

    def GetCtrl(self):
        a = self.GetPath()
        a = self.CheckSaveLoadAs(a, 'save')
        return a
    
    def SetCtrl(self, value):
        if value is None:
            value = ''
        
        value = self.CheckSaveLoadAs(value, 'load')    
        self.SetPath(value)
    
    def OnLoad(self, whereField, whereValue):
        val = LookupDB(self.tableName).Specific(whereValue, whereField, self.fieldName)
        self.SetCtrl(val)
        
    def OnSave(self, whereField, whereValue):
        setTo = self.GetPath()
        pout.b(f'WhereField : {whereField} --> WhereValue : {whereValue}')
        pout.v(f'tableName : {self.tableName} ; fieldName : {self.fieldName}')
        try:
            item = LookupDB(self.tableName).UpdateSingle(self.fieldName, setTo, whereField, whereValue)
        except:
            pout.v(f'Table : {self.tableName} ; Field : {self.fieldName} ; WhereField : {whereField} ; whereValue: {whereValue}')

    # def GetCtrl(self):
    #     return self.GetPath()
    
    # def SetCtrl(self, value):
    #     typd = str(type(value))
    #     if value is None:
    #         value = ''
    #     if 'tuple' in typd:
    #         value = value[0]
    #     self.SetPath(str(value))

    def Clear(self):
        self.Clear()


#--------------------------------------------------------------------------------------
class RH_LoadSaveString(object):
    def __init__(self, *args, **kwargs):
        self.tableName = None
        self.fieldName = None
        self.sqlfile = None
        self.saveAs = 'str'
        self.loadAs = 'str'
        pout.b(self.loadAs)
                     
    def CheckSaveLoadAs(self, value, typd):
        conv = self.loadAs
        if typd == 'save':
            conv = self.saveAs

        pout.v('CheckSaveLoadAs : ', value, self.loadAs)

        if 'str' in conv:
            value = str(value)
        elif 'int' in conv:
            value = int(value)
        elif 'float' in conv:
            value = float(value)
        elif 'decimal' in conv:
            value = Decimal(value)
        
        return value


    def GetCtrl(self):
        a = self.GetValue()
        a = self.CheckSaveLoadAs(a, 'save')
        return a
    
    def SetCtrl(self, value):
        if value is None:
            value = ''
        pout.v(value)
        a = self.CheckSaveLoadAs(value, 'load')    
        pout.v(a)
        self.SetValue(a)



    def OnLoad(self, whereField, whereValue):
        val = LookupDB(self.tableName).Specific(whereValue, whereField, self.fieldName)
        
        self.SetCtrl(val)


    def OnSave(self, whereField, whereValue):
        setTo = self.GetValue()
        
        pout.b(f'WhereField : {whereField} --> WhereValue : {whereValue}')
        pout.v(f'tableName : {self.tableName} ; fieldName : {self.fieldName}')
        try:
            item = LookupDB(self.tableName).UpdateSingle(self.fieldName, setTo, whereField, whereValue)
        except:
            pout.v(f'Table : {self.tableName} ; Field : {self.fieldName} ; WhereField : {whereField} ; whereValue: {whereValue}')

    # def GetCtrl(self):
    #     a = self.GetValue()
    #     a = self.CheckSaveLoadAs(a, 'save')
    #     return a
    
    # def SetCtrl(self, value):
    #     if value is None:
    #         value = ''
    #     a = self.CheckSaveLoadAs(value, 'load')    
    #     self.SetValue(a)

    def Clear(self):
        self.Clear()

#--------------------------------------------------------------------------------------
class RH_LoadSaveCombo(object):
    def __init__(self, *args, **kwargs):
        self.tableName = None
        self.fieldName = None
        self.defTable = None
        self.defField = None
        self.sqlfile = None
        

    def LoadDefaults(self, tableName, fieldName, whereField, whereValue):
        if self.defTable is not None and self.defField is not None:
            returnd = LookupDB(self.defTable).Specific(whereValue, whereField, self.defField)
            
            jsond = VarOps().CheckJson(returnd)        
            d = VarOps().GetTyped(jsond)
        print(f'jsond : {d}')
        if re.search('(list|tuple)', d, re.I):
            c = True
        a = VarOps().StrList(jsond)
        if jsond is not None and c is True:
            self.AppendItems(a)
            
    def OnLoad(self, whereField, whereValue):
        returnd = LookupDB(self.tableName).Specific(whereValue, whereField, self.fieldName)
        jsond = VarOps().CheckJson(returnd)
        d = VarOps().GetTyped(jsond)
        print(f'jsond : {d}')
        if re.search('(list|tuple)', d, re.I):
            c = True
        a = VarOps().StrList(jsond)
        if jsond is not None and c is True:
            self.AppendItems(a)
        
    def OnSave(self, whereField, whereValue):
        a = self.GetSelection()        
        b = VarOps().DoJson(a)
        try:
            returnd = LookupDB(self.tableName).UpdateSingle(self.fieldName, b, whereField, whereValue)        
        except:
            pout.v(f'Table : {self.tableName} ; Field : {self.fieldName} ; WhereField : {whereField} ; whereValue: {whereValue}')

    def GetCtrl(self):
        return self.GetSelection()

    def SetCtrl(self, value):
        self.SetSelection(value)

    def Clear(self):
        self.Clear()

#--------------------------------------------------------------------------------------
class RH_LoadSaveListBox(object):
    def __init__(self, *args, **kwargs):
        self.tableName = None
        self.fieldName = None
        self.sqlfile = None
        
    def OnLoad(self, whereField, whereValue):
        returnd = LookupDB(self.tableName).Specific(whereValue, whereField, self.fieldName)
        pout.v(returnd[0])
        jsond = VarOps().CheckJson(returnd[0])
        pout.v(returnd)
        pout.v(returnd[0])
        j = json.loads(returnd)
        
        pout.v(f'RH_LoadSaveListBox : {j}')
        
        if jsond is not False:
            self.AppendItems(j)

        
    def OnSave(self, whereField, whereValue):
        a = self.GetSelection()        
        #b = VarOps().DoJson(a)
        try:
            returnd = LookupDB(self.tableName).UpdateSingle(self.fieldName, b, whereField, whereValue)
        except:
            pout.v(f'Table : {self.tableName} ; Field : {self.fieldName} ; WhereField : {whereField} ; whereValue: {whereValue}')

    def GetCtrl(self):
            return self.GetSelection()

    def SetCtrl(self, value):
        self.SetSelection(value)

    def Clear(self):
        self.Clear()
    
    def GetItems(self):
        return [self.GetString(i) for i in range(listBox.GetCount())]
    

#--------------------------------------------------------------------------
class RH_LoadSaveListCtrl(object):
    def __init__(self, *args, **kwargs):
        self.tableName = None
        self.fieldName = None
        self.sqlfile = None
        
    def OnLoad(self, whereField, whereValue):
        returnd = LookupDB(self.tableName).Specific(whereValue, whereField, self.fieldName)
        jsond = VarOps().CheckJson(returnd)
        self.AppendItems(jsond)
        
    def OnSave(self, whereField, whereValue):
        a = self.GetValue()        
        b = VarOps().DoJson(a)
        try:
            returnd = LookupDB(self.tableName).UpdateSingle(self.fieldName, b, whereField, whereValue)
        except:
            pout.v(f'Table : {self.tableName} ; Field : {self.fieldName} ; WhereField : {whereField} ; whereValue: {whereValue}')

    def Clear(self):
        self.DeleteAllItems()

class RH_LoadSaveOLV(object):
    def __init__(self, *args, **kwargs):
        self.tableName = None
        self.fieldName = None
        self.sqlfile = None
        
    def OnLoad(self, whereField, whereValue):
        returnd = LookupDB(self.tableName).Specific(whereValue, whereField, self.fieldName)
        try:
            jsond = json.loads(returnd)
            self.SetObjects(jsond)
        except:
            print('returnd Not JSON\'d')
            pout.v(jsond)
    
    def OnSave(self, whereField, whereValue):
        b = self.GetObjects()
        jsond = json.dumps(b)
        pout.v(f'GetSelectedObjects : {b}')
        try:
            returnd = LookupDB(self.tableName).UpdateSingle(self.fieldname, jsond, whereField, whereValue)
        except:
            pout.v(f'Table : {self.tableName} ; Field : {self.fieldName} ; WhereField : {whereField} ; whereValue: {whereValue}')

    def GetEntry(self):
        return self.GetSelectedObject()

    def GetAll(self):
        return self.GetObjects()
    
    def AddEntry(self, listdicts):
        old = self.GetObjects()
        new = old + listdicts
        self.SetObjects(new)
    
    def Clear(self):
        self.DeleteAllItems()

class tSizer(wx.BoxSizer):
    def __init__(self, parent, text, ctrl):
        super().__init__(wx.VERTICAL)
        
        self.text = wx.StaticText(parent, label=text)
        self.Add(self.text, 0)
        self.Add(ctrl, 0)
  

class RH_LoadSaveOrgs(object):
    def __init__(self, *args, **kwargs):
        self.tableName = None
        self.fieldName = None
        self.sqlfile = None
        
class RH_Orgs(ObjectListView, RH_LoadSaveOrgs):
    def __init__(self, *args, **kwargs):
        ObjectListView.__init__(self, *args, **kwargs)
        self.SetEmptyListMsg('No One Home')
       # self.evenRowsBackColor(RH_lineColor)


class RH_OLV(ObjectListView, RH_LoadSaveOLV):
    def __init__(self, *args, **kwargs):
        ObjectListView.__init__(self, *args, **kwargs)
        self.SetEmptyListMsg('No One Home')
       # self.evenRowsBackColor(RH_lineColor)


class IconList(object):
    def __init__(self, *args, **kwargs):
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
                       'addrmaint': '',
                       'minus': ''}
    
    def getFont(self, size=40):
        fontpath = './fonts/DaddyTimeMono Nerd Font Complete Mono.ttf'
        wx.Font.AddPrivateFont(fontpath)
        f = wx.Font(pointSize=12,
                    family=wx.FONTFAMILY_DEFAULT,
                    style=wx.FONTSTYLE_NORMAL,
                    weight=wx.FONTWEIGHT_NORMAL,
                    underline=False,
                    faceName="DaddyTimeMono",
                    encoding=wx.FONTENCODING_DEFAULT)
        f.SetPixelSize((size,size))
        return f

    def getIcon(self, icon_name):
        return self.a_dict[icon_name]
        
class RH_Icon(wx.Button):
    def __init__(self, parent, *args, **kwargs):
        typd = kwargs.pop('label')
        size = kwargs.pop('fontsize')
        super().__init__()
        # wx.Button.__init__(parent, *args, **kwargs)
        # IconList.__init__(parent, *args, **kwargs)
        
        icon = IconList()
        self.SetFont(icon.getFont(size=size))
        self.SetLabel = icon.getIcon(typd.lower())


class RH_Button(wx.Button):
    def __init__(self, *args, **kwargs):
        self.icon = kwargs.pop('label')
        self.fontsize = kwargs.pop('size')
        wx.Button.__init__(*args, **kwargs) 
        self.SetCtrl(self.icon)
        self.listd = None
        self.tableName = None
        self.fieldName = None
        self.DefTable = None
        self.DefField = None
        self.cnt = 0
        #pout.v(f'Listd : {self.listd} ; CNT : {self.cnt}')
        self.Bind(wx.EVT_BUTTON, self.NextLabel)
        
    def DefaultChoices(self):
        returnd = LookupDB(self.DefTable).General(self.DefField)
        try:
            self.listd = returnd[0]
        except:
            pout.v(returnd)

    def NextLabel(self, evt):
        obj = evt.GetEventObject()
        if self.listd is not None:
            maxd = len(self.listd)
            self.SetLabel(self.listd[self.cnt])
            self.cnt += 1
            if self.cnt >= maxd:
                self.cnt = 0
        
    def OnSave(self, whereField, whereValue):
        a = self.GetLabel()
        try:
            returnd = LookupDB(self.tableName).UpdateSingle(self.fieldName, a, whereField, whereValue)
        except:
            pout.v(f'Table : {self.tableName} ; Field : {self.fieldName} ; WhereField : {whereField} ; whereValue: {whereValue}')
    
    def OnLoad(self, whereField, whereValue):
        returnd = LookupDB(self.tableName).Specific(whereValue, whereField, self.fieldName)
        a = VarOps().GetTyped(returnd)
        if 'tuple' in a:
            returnd = returnd[0]
        if returnd is None:
            returnd = ''
        try:
            self.SetLabel(returnd)
        except TypeError as e:
            pout.v(e)

    def GetCtrl(self):
        return self.GetLabel()

    def SetCtrl(self, value):
        self.SetLabel(value)

    def Clear(self):
        a = ''
        self.SetLabel('')


class RH_lineColor(wx.Colour):
    def __init__(self,*args, **kwargs):
        kwargs['red'] = 157
        kwargs['green'] = 224
        kwargs['blue'] = 173
        kwargs['alpha'] = 255
        wx.Colour.__init__(self, *args, **kwargs)
        self.Get()


#--------------------------------------------------------------------------        
class RH_FilePickerCtrl(wx.FilePickerCtrl, RH_LoadSavePath):
    def __init__(self, *args, **kwargs):
        wx.FilePickerCtrl.__init__(self, *args, **kwargs)

#-------------------------------------------------------------------------    
class RH_OLV(ObjectListView, RH_LoadSaveOLV):
    def __init__(self, *args, **kwargs):
        ObjectListView.__init__(self, *args, **kwargs)
        self.SetEmptyListMsg('No One Home')
       # self.evenRowsBackColor(RH_lineColor)

#--------------------------------------------------------------------------
class RH_DatePickerCtrl(wx.adv.DatePickerCtrl, RH_LoadSaveDate):
    def __init__(self, *args, **kwargs):
        wx.adv.DatePickerCtrl.__init__(self, *args, **kwargs)
    

#--------------------------------------------------------------------------------------
class RH_DateCtrl(wx.adv.DatePickerCtrl, RH_LoadSaveDate):
    def __init__(self, *args, **kwargs):
        wx.adv.DatePickerCtrl.__init__(self, *args, **kwargs)
        

#--------------------------------------------------------------------------
class RH_TimeCtrl(masked.TimeCtrl, RH_LoadSaveTime):
    def __init__(self, *args, **kwargs):
        masked.TimeCtrl.__init__(self, *args, **kwargs)


#--------------------------------------------------------------------------
class RH_CheckBox(wx.CheckBox, RH_LoadSaveNum):
    def __init__(self, *args, **kwargs):
        wx.CheckBox.__init__(self, *args, **kwargs)
    
#--------------------------------------------------------------------------
class RH_RadioButton(wx.RadioButton, RH_LoadSaveNum):
    def __init__(self, *args, **kwargs):
        wx.RadioButton.__init__(self, *args, **kwargs)


#--------------------------------------------------------------------------
class RH_RadioBox(wx.RadioBox, RH_LoadSaveSelection):
    def __init__(self, *args, **kwargs):
        wx.RadioBox.__init__(self, *args, **kwargs)
   
        
#--------------------------------------------------------------------------
class RH_ComboBox(wx.ComboBox, RH_LoadSaveCombo):
    def __init__(self, *args, **kwargs):
        wx.ComboBox.__init__(self, *args, **kwargs)


#--------------------------------------------------------------------------
class RH_ListCtrl(wx.ListCtrl, RH_LoadSaveListCtrl):
    def __init__(self, *args, **kwargs):
        wx.ListCtrl.__init__(self, *args, **kwargs)


#--------------------------------------------------------------------------
class RH_ListBox(wx.ListBox, RH_LoadSaveListBox):
    def __init__(self, *args, **kwargs):
         wx.ListBox.__init__(self, *args, **kwargs)


#--------------------------------------------------------------------------
class RH_TextCtrl(wx.TextCtrl, RH_LoadSaveString):
    def __init__(self, *args, **kwargs):
        wx.TextCtrl.__init__(self, *args, **kwargs)


#--------------------------------------------------------------------------
class RH_MComboBox(masked.combobox.ComboBox, RH_LoadSaveCombo):
    def __init__(self, *args, **kwargs):
        masked.combobox.ComboBox.__init__(self, *args, **kwargs)


#--------------------------------------------------------------------------
class RH_MTextCtrl(masked.textctrl.TextCtrl, RH_LoadSaveString):
    def __init__(self, *args, **kwargs):
        masked.textctrl.TextCtrl.__init__(self, *args, **kwargs)
        

#--------------------------------------------------------------------------        
class RH_NumCtrl(wx.lib.masked.NumCtrl, RH_LoadSaveNum):
    def __init__(self, *args, **kwargs):
        wx.lib.masked.NumCtrl.__init__(self, *args, **kwargs)

#--------------------------------------------------------------------------
class GridOps(object):
    def __init__(self, gridname, debug=False):
        self.gridname = gridname
        self.grid = wx.FindWindowByName(gridname)
        
    def GRIDtoJSON(self):
        xcnt = self.grid.GetNumberRows()
        ycnt = self.grid.GetNumberCols()
        dictd = {}
        for x in range(xcnt):
            rowLabel = self.grid.GetRowLabelValue(x)
            dictd[rowLabel] = {}
            for y in range(ycnt):
                colLabel = self.grid.GetColLabelValue(y)
                celldata = self.grid.GetCellValue(x, y)
                dictd [rowLabel][colLabel]=celldata
            
            
        return json.dumps(dictd)
    
    def JSONtoGRID(self, JSONFile):
        dictd = json.loads(JSONFile)
        x = 0
        y = 0
        for x in range(xcnt):
            rowLabel = self.grid.GetRowLabelValue()
            for y in range(ycnt):
                colLabel = self.grid.GetColLabelValue()
                celldata = dictd[rowLabel][colLabel]
                pout.v(f'Row : {rowLabel} ; Col : {colLabel} ; Data : {celldata}')
                self.grid.SetCellValue(x,y,celldata)    
            
            


    def CurGridLine(self, blank=False):
        row = 0
        maxRows = self.grid.GetNumberRows()
        for x in range(maxRows):
            value = self.grid.GetCellValue(x,0)
            if value == '' or value is None:
                row = x - 1
                if blank is True:
                    row = x
                
                if row < 0:
                    row = 0    
                
                return row     

    def GetGridCursor(self):
        row = self.grid.GetGridCursorRow()
        col = self.grid.GetGridCursorCol()
        
        return row, col   
        
    def GridFocusNGo(self, row=None, col=0):
        cur_row = self.CurGridLine()
        if row == None and cur_row != 0:
            row = self.CurGridLine()+1
        else:
            row = cur_row
            
        self.grid.SetFocus()
        wx.CallAfter(self.grid.SetGridCursor, row, col) 

    def FillGrid(self, setlist, row=None,col=None, debug=False):
        
        if row is not None:
            for yy in range(self.grid.GetNumberCols()):
                header = self.grid.GetColLabelValue(yy)
                
                for title, value in setlist:
                    if title in header:
                        self.grid.SetCellValue(int(row), yy, str(value))

        if col is not None:
            for xx in range(grid.GetNumberRows()):
                header = self.grid.GetRowLabelValue(xx)
                
                
                for title, value in setlist:
                    if title in header:
                        self.grid.SetCellValue(xx, int(col),str(value))                    
                    
    def GridAlternateColor(self, result=None):
        bgcolor = Themes(self.gridname).GetColor('bg')
        whitetext = Themes(self.gridname).GetColor('text')
        cell_color = Themes(self.gridname).GetColor('cell')
        
        if result is None:
            result = self.grid.GetNumberRows()
            
        colorlength = result
        
        if not str(result).isdigit():
            colorlength = self.grid.GetNumberRows()
        for xx in range(colorlength):
            for yy in range(self.grid.GetNumberCols()):
                try:
                    self.grid.SetCellBackgroundColour(xx, yy, bgcolor)
                except:
                    print(f'bgcolor : {bgcolor}')
        
        for xx in range(colorlength):
            if xx % 2:
                for yy in range(self.grid.GetNumberCols()):
                    try:
                        self.grid.SetCellBackgroundColour(xx, yy, cell_color)
                    except:
                        print(f'bgcolor : {bgcolor}')
    
    def GridHomeColor(self, row):
        bgcolor = (0, 0, 255)
        whitetext = (255, 255, 255)
        home_color = (209, 201, 94)
        
        for yy in range(self.grid.GetNumberCols()):
            self.grid.SetCellBackgroundColour(row, yy, home_color) 

    def GridListReadOnly(self, header_list, rowcol='row'):
        if 'row' in rowcol:
            for xx in range(self.grid.GetNumberRows()):
                for item in header_list:
                    rowName = self.grid.GetRowLabelValue(xx)
                    if rowName == item:
                        self.grid.SetReadOnly(xx,0,True)
                
        if 'col' in rowcol:
            for yy in range(self.grid.GetNumberCols()):
                for item in header_list:
                    colName = self.grid.GetColLabelValue(yy)
                    if rowName == item:
                        self.grid.SetReadOnly(0,yy,True)

    def DecimalOnly(self, colname, row, col, value=None):
        if value is None:
            value = GridOps(self.grid.GetName).GetCell(colname,row)
        
        if re.search(r'[0-9]', value, re.I):
            new_value = RoundIt(value, '1.00')
            setList = [(colname,new_value)]
            self.FillGrid(setList, row=row)
            return 'OK',new_value
        
        else:
            setList = [(colname,'')]
            self.FillGrid(setList,row=row)
            wx.CallAfter(self.grid.SetGridCursor, row, col)    

    def FindEmptyRow(self):
        rows = self.grid.GetNumberRows()
        
        for xx in range(rows):
            cell = self.grid.GetCellValue(xx, 0)
            if cell == '' or cell is None:
                return xx    
        
    def DisplayItemsinGrid(self, headers, itemList):
        if itemList:
            self.grid.ClearGrid()
            yy = 0
            for xx in range(len(itemList)):
                
                for yy in range(self.grid.GetNumberCols()):
                    
                    grid_header = self.grid.GetColLabelValue(yy)
                    
                    if re.search(headers[yy], grid_header, re.I):
                        if 'price' in grid_header:
                            self.grid.SetCellValue(xx, yy,
                                            itemList['standard_price']['price'])
                        else:
                            self.grid.SetCellValue(xx, yy, itemList[xx][yy])
                        
                            

    def AlterGrid(self, returnd):
        if returnd is None:
            current = self.grid.GetNumberRows()
            self.grid.DeleteRows(0, current, True)
        else:
            current, new = (self.grid.GetNumberRows(), len(returnd))

            if new > current:
                self.grid.AppendRows(new - current)

            if new < current:
                self.grid.DeleteRows(0, current - new, True)

        wx.FindWindowByName(grid.GetName()).ClearCtrl()
        self.GridAlternateColor()

    def GridCellLabelSet(self, col_list, tname='POS'):
        bgcolor = Themes(tname).GetColor('bg')
        textcolor = Themes(tname).GetColor('whitetext')
        sized = self.GridCol_Sized(col_list)
        self.GridAlternateColor('')
        
        

        for xx, yy, label in col_list:
            
            self.grid.SetColSize(yy, sized[yy])
            self.grid.SetCellValue(xx, yy, label)
            self.grid.SetCellBackgroundColour(xx, yy, bgcolor)
            self.grid.SetCellTextColour(xx, yy, textcolor)
            self.grid.SetCellFont(xx, yy, wx.Font(wx.FontInfo(12).Bold()))
            self.grid.SetReadOnly(xx, yy, True)
            self.grid.SetRowSize(xx, 50)

        self.grid.SetColSize(1, 150)
        self.grid.SetReadOnly(0, 1, False)

    def GridCol_Sized(self, col_list, debug=False):
        last_size = {}
        size = {}
        sized = {}
        ListSize = len(col_list)
        last_yy = 0
        for xx, yy, label in col_list:
            last_size[yy] = 0
            size[yy] = 0

        for xx, yy, label in col_list:
            if not last_size[yy]:
                last_size[yy] = 0
            size[yy] = len(label)
            if size[yy] > last_size[yy]:
                last_size[yy] = size[yy]

        for key, value in list(last_size.items()):
            sized[key] = value * 12
            

        return sized

    def GetCell(self, title, rowcol):
        colsnum = self.grid.GetNumberCols()
        checkColName = self.grid.GetColLabelValue(0)
        if re.match('[A-Z]', checkColName) and len(checkColName) == 1:
            rowsnum = self.grid.GetNumberRows()
            for row in range(rowsnum):
                if title in self.grid.GetRowLabelValue(row):
                    now_retail = self.grid.GetCellValue(row, rowcol)
        else:
            for col in range(colsnum):
                if title in self.grid.GetColLabelValue(col):
                    now_retail = self.grid.GetCellValue(rowcol, col)

        return now_retail.strip()


    def GetColNumber(self, title):
        rowcol = self.grid.GetNumberCols()
        for col in range(rowcol):
            if title in self.grid.GetColLabelValue(col):
                colnum = col
                break

        return colnum



class Themes(object):
    def __init__(self, tname='POS', debug=False):
        self.tname = self.GetThemeName(tname)
        pout.v(self.tname)

    def GetColor(self, color_for):
        note_color = '#f8fda9'
        info_color = '#e8f4f0'
        returnd = None
        returnd = LookupDB('themes').Specific(self.tname, 'theme_name', color_for)
        print(f'GetColor {self.tname} : Returnd : {returnd}')
        return returnd
        # (bg, text, cell) = returnd
        
        # bg = re.sub('[b\']','',bg)
        # text = re.sub('[b\']','',text)
        # cell = re.sub('[b\']','',cell)
        
        
        # if returnd is None:
        #     bg = '#fffff'
        #     text = '#00000'
        #     cell = '#d9f1e8'
        
        # listd = [('info', info_color),('note',note_color),('cell',cell),('text',text),('bg',bg)]
        # for label, color in listd:
        #     if label in color_for:
        #         return color
       
    def GetThemeName(self,ctrlname):
        tname='POS'
        
        if re.match('cus[tomers_]+', ctrlname, re.I):
            tname = 'CUSTOMERS'
        
        if re.match('In[ventory_]+', ctrlname, re.I):
            tname = 'INVENTORY'
        
        if re.match('Ven[dors_]+', ctrlname, re.I):
            tname = 'VENDORS'
    
        return tname            



