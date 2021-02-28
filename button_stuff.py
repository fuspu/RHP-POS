# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
#
#
#
import re



class ButtonOps(object):
    def __init__(self, debug=False):
        pass    

    def ButtonWidth_onRow(self, button_cnt, bar_width, num_of_levels=2, minWidth=50, button_gap=3):
        if button_cnt % 2 != 0:
            button_cnt += 1
        lvl_cnt = button_cnt/num_of_levels
        add_width = (((lvl_cnt*minWidth)+(lvl_cnt*button_gap))-bar_width)/lvl_cnt
        button_width = minWidth+abs(add_width)
        
        return int(button_width)

    def ButtonSized(self, button_list):

        tup_item_cnt = len(button_list[0])
        list_cnt = len(button_list)
        last_size = 0
        multiplier = 0
        
        for major in range(list_cnt):
            for minor in range(tup_item_cnt):
                valued = button_list[major][minor]
                styled = str(type(valued))
                if re.search('(str|unicode)', styled):
                    types = '(button|text|radiobox|radiobtn|ctrl)'
                    if not re.search(types, valued):
                        if len(valued) > last_size:
                            last_size = len(valued)
                        if valued.count('\n') > multiplier:
                            multiplier = valued.count('\n') + 1

        wsize = last_size * 9
        hsize = 25 * multiplier

        return wsize, hsize

    def ButtonToggle(self, buttonName, state=True):
        btn = wx.FindWindowByName(buttonName)
        downColor = (121, 145, 183)
        upColor = (wx.NullColour) #212, 226, 247
        if state is not True:
            btn.SetBackgroundColour(downColor)
            return True
        else:
            btn.SetBackgroundColour(upColor)
            return False

    def ButtonCenterText(self, label):
        labels = label.split('\n')
        labelNum = len(labels)
        
        if labelNum > 1:
            lab1_W = len(labels[0])
            lab2_W = len(labels[1])
            
            
            if lab1_W >= 6 and lab1_W < 10:
                if lab2_W > 5:
                    spaces = 2
                else:
                    spaces = 3
                    
            if lab1_W <=5:
                if lab2_W > 5:
                    spaces = 0
                else:    
                    spaces = 2
            
            if lab1_W >= 10: 
                if lab2_W > 10:
                    spaces = 0
                else:
                    spaces = 6
                    
            spaced=''
            for spc in range(spaces):
                spaced += ' '   
                
            labeld = '{}\n{}{}'.format(labels[0], spaced, labels[1])
        else:
            labeld = label     
                    
        
        return labeld

    def ListAdjustEven(self, listd):
        list_cnt = len(listd)
        entr_cnt = len(listd[0])
        
        if list_cnt % 2 != 0:
            value = ('',)
            for i in range(entr_cnt-1):
                value += ('',)
            #value = ('','','')
            listd.append(value)
        
        return listd
                    
    def ButtonOff(self, names, state=True):
        typ = str(type(names))
        print(('typd : ',typ))
        if re.search('(unicode|str)', typ, re.I):
            item = wx.FindWindowByName(names)
            if state is True:
                item.Disable()
            else:
                item.Enable()
                
        if 'list' in typ:
            for name in names:
                print(('button name : ',name))
                item = wx.FindWindowByName(name)
                if state is True:
                    item.Disable()
                else:
                    item.Enable()

    def Icons(self, typd, size=24):
        """Available Icon Sizes are as follows:
        128x128, 16x16, 24x24, 36x36, 48x48
        """
        sized = f'{size}x{size}'
        icondir = './icons'
        logodir = '../logos'
        a_dict = {'save': f'{icondir}/{sized}/{sized}_Save.png', 
                 'add': f'{icondir}/{sized}/{sized}_Add.png',
                 'exit': f'{icondir}/{sized}/{sized}_Exit.png',
                 'find': f'{icondir}/{sized}/{sized}_Binocular2_Black.png',
                 'undo': f'{icondir}/{sized}/{sized}_Undo.png',
                 'delete': f'{icondir}/{sized}/{sized}_Minus.png',
                 'print': f'{icondir}/{sized}/{sized}_Printer.png',
                 'empty': f'{icondir}/empty-300x300.png',
                 'refresh': f'{icondir}/{sized}/{sized}_Refresh.png',
                 'receiving': f'{icondir}/{sized}/{sized}_Receiving.png',
                 'pdf': f'{icondir}/{sized}/{sized}_PDF.png',
                 'logo': f'{logodir}',
                 'addrmaint': f'{icondir}/{sized}/{sized}_AddrMap_Color.png'}
                 
        loc = a_dict[typd.lower()]
        return loc


    def TextIcons(self, typd, size=24):
        """Available Icon Sizes are as follows:
        128x128, 16x16, 24x24, 36x36, 48x48
        """
        sized = f'{size}x{size}'
        fontdir = './fonts'
        iconfont = 'ttf-font-awesome'
        exitIcon = '\f52b'
        #t.SetFont(wx.Font(sized, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Ubuntu")
        t.SetFont(wx.Font(sized, wx.SWISS, wx.NORMAL, wx.NORMAL, False, u'fa-solid-900'))

        aList = [('save', f'{icondir}/{sized}/{sized}_Save.png'), 
                 ('add', f'{icondir}/{sized}/{sized}_Add.png'),
                 ('exit', f'{icondir}/{sized}/{sized}_Exit.png'),
                 ('find', f'{icondir}/{sized}/{sized}_Binocular2_Black.png'),
                 ('undo', f'{icondir}/{sized}/{sized}_Undo.png'),
                 ('delete', f'{icondir}/{sized}/{sized}_Minus.png'),
                 ('print', f'{icondir}/{sized}/{sized}_Printer.png'),
                 ('empty', f'{icondir}/empty-300x300.png'),
                 ('storeAwning',f'{icondir}/Store_awning_sm.png'),
                 ('refresh', f'{icondir}/{sized}/{sized}_Refresh.png'),
                 ('receiving', f'{icondir}/{sized}/{sized}_Receiving.png'),
                 ('pdf', f'{icondir}/{sized}/{sized}_PDF.png'),
                 ('logo',f'{logodir}')]
                 
        for icon, loc in aList:
            if typd.lower() == icon:
                return loc
