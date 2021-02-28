# -*- coding: utf-8 -*-
#!/bin/python
#
# Inventory
#
# import wxversion
# wxversion.select('2.8')

import sys,re
import json
import numpy
import MySQLdb
import datetime
import HandyUtilities as HUD
from decimal import Decimal, ROUND_HALF_UP
import argparse
import csv
import time


class ImportCSV(object):
    """ Import CSV Files to db"""
    def __init__(self, csvfile):
        self.csvfile = csvfile

    def Inventory(self,typd):
        with open(self.csvfile) as f:
            reader = csv.DictReader(f)
            for row in reader:
                query = '''SELECT count(*),upc 
                           FROM item_detailed 
                           WHERE altlookup LIKE (?) 
                           OR part_num=(?)
                           OR oempart_num=(?)
                           OR vendor1_ordernum=(?)
                           OR vendor2_ordernum=(?)
                           OR vendor3_ordernum=(?)
                           OR vendor4_ordernum=(?)
                           OR vendor5_ordernum=(?)
                           OR vendor6_ordernum=(?)
                         '''
                lookupc = row['Number']
                
                data = [lookupc, lookupc, lookupc, lookupc, lookupc, lookupc, lookupc, lookupc, lookupc,]
                returnd = HUD.SQConnect(query, data).ONE()
                
                if returnd[0] > 0:
                    lookupc = returnd[1]
                        
                table_list = ['item_retails','item_detailed', 
                             'item_detailed2', 'item_options',
                             'item_vendor_data','item_notes',
                             'item_sales_links','item_cust_instructions',
                             'item_history']
                             
                
                returnd = HUD.QueryOps().CheckEntryExist('upc',lookupc, table_list)
                if returnd is True:
                    if typd == 'prices':
                       query = '''UPDATE item_retails 
                                  SET standard_price=(?),
                                      level_a_unit=(?),
                                      level_a_price=(?),
                                      level_b_unit=(?),
                                      level_b_price=(?)
                                  WHERE upc=(?)'''
                       
                       data = [row['Price1'],row['Units2'],row['Price2'],row['Units3'],row['Price3'],lookupc,]
                       returnd = HUD.SQConnect(query, data).ONE()
                        
                       query = '''UPDATE item_detailed 
                                  SET avg_cost=(?) 
                                  WHERE upc=(?)'''
                        
                       data = [row['AvgCost'],lookupc]
                       returnd = HUD.SQConnect(query, data).ONE()

                    if typd == 'descriptions':
                       query = '''UPDATE item_detailed 
                                   SET description=(?) 
                                   WHERE upc=(?)'''
                                   
                       data = [row['Description'], lookupc,]
                       returnd = HUD.SQConnect(query, data).ONE()
                        
                       query = '''UPDATE item_options
                                  SET department=(?),
                                      category=(?),
                                      subcategory=(?)
                                  WHERE upc=(?)'''
                       data = [row['Department'], row['Category'], row['SubCat'], lookupc,]
                       returnd = HUD.SQConnect(query, data).ONE()
                        
                    
       
    def Customers(self):
        with open(self.csvfile) as f:
            reader = csv.DictReader(csvfile)
            for row in reader:
                table_list = []
        
    def Transactions(self):
        with open(self.csvfile) as f:
            reader = csv.DictReader(csvfile)
            for row in reader:
                table_list = []
                
    
      


parser = argparse.ArgumentParser(description='Import CSV files with headers')

parser.add_argument("-v", "--verbose", help="Be Verbose", action="store_true")
parser.add_argument("-s", "--section", help="Section", action="store")
parser.add_argument("-f", "--csvfile", help="CSV File to Import", action="store")

args = parser.parse_args()

if args.section is None:    
    print('Nothing to Import\n Try: Import_CSV.py -h for help') 
    sys.exit(0)

if re.match('Inventory', args.section, re.I):
    c = ImportCSV(args.csvfile)
    typdList = ['price','description']
    for typ in typdList:
        if re.search(typ, args.csvfile, re.I):
            typd = typ
            
    c.Inventory(typd)
    
elif re.match('Customers',args.section, re.I):
    c = ImportCSV(args.csvfile)
    c.Customers()

elif re.match('Transactions', args.section, re.I):
    c = ImportCSV(args.csvfile)
    c.Transactions()

else:
    print('Cant Import {}'.format(args.section))
    
    