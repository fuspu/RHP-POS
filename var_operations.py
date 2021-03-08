#!/usr/bin/env python
#
#
#
import re
import json


class VarOps(object):
    def __init__(self, debug=False):
        pass    

    def DeTupler(self, value):
        typd = str(type(value))
        if value:
            while re.search('(tuple|list)', str(type(value)), re.I):
                value = value[0]

        return value

    def is_json(self, myjson):
        try:
            json_object = json.loads(myjson)
        except (TypeError, ValueError) as e:
            #print(f'JSON Error : {e}')
            return False
        return True

    def CheckJson(self, vari):
        b = self.CheckNone(vari)
        if b is None:
            return None
        #print(f'Before CHECKJSON : {vari[0]}')
        a = self.is_json(vari[0])
        #print(f'AFTER CHeckJSON : {a}')
        if a is True:
            a = json.loads(vari[0])
        else:
            a = vari
        return a
    
    def DoJson(self, vari):
        a = vari
        ta = self.GetTyped(a)
        if re.search('(list|tuple|dict)', ta, re.I):
            a = json.dumps(vari)
        return a

    def GetTyped(self, item, debug=False):
        return str(type(item))
        
    def StrList(self, listd):
        a = listd
        
        if listd is not None:
            a = []
            for i in listd: 
                a.append(str(i))
        
        return a

    def CheckNone(self, val, debug=False):
        a = str(type(val))
        b = self.DeTupler(val)
        if b is None:
            return None
       
        obret = val
        a = str(type(val))
        if 'tuple' in a:
            if len(val) == 0:
                obret = None
            else:
                obret = val[0]
    
        if 'None' in a:
            obret = None

        return obret


    def ChangeType(self, instr, typd):
        rd = str(type(instr))
        final = instr
        if not re.search(rd, typd, re.I):
            if re.match(typd, 'decimal', re.I):
                final = Decimal(instr)
            if re.match(typd, 'string', re.I):
                final = str(instr)
            if re.match(typd, 'float', re.I):
                final = float(instr)
            if re.match(typd, 'integer', re.I):
                final = int(instr)
            
        return final


class LoadSaveList(object):
    def __init__(self):
        self.listd = []
    
    def Add(self, item):
        self.listd.append(item)
    
    def Show(self):
        pout.v(self.listd)

    def Get(self):
        return self.listd

