#!/usr/bin/env python3
"""
Item Related Objects.
"""
#-*- coding: utf-8 -*-

import re
from datetime import datetime
from db_related import DBConnect


class Item_Lookup(object):
    """
    Returned Item Lookup Dictionary Structure:
        item = {
                upc: text
                description: text
                cost: decimal
                price: decimal
                taxable: True or False
                on_hand_qty: decimal
                stx: decimal
                
                }
    """
    def __init__(self, upc):
        self.upc = upc


    def GetBasics(self):
        query = '''SELECT upc, description, cost, retail, taxable, onhandqty 
                   FROM item_detailed 
                   WHERE upc=(?)'''
        data = [self.upc,]
        returnd = DBConnect(query, data).ALL()
        


