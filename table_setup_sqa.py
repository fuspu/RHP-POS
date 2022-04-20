
#!/usr/bin/env python
#-*- coding: utf-8 -*-

#
#
#
#import wxversion
#wxversion.select('2.8')

#import sqlite3
import datetime
import pout
import json
from db_ops import DBConnect, SQConnect
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, Numeric, String, MetaData, ForeignKey, Date, Text, Time, func, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

class tabsup(object):
    def __init__(self):
        self.sql_file = self.create()

    def add(self, keyd, tblname):
        chk = self.chk(keyd, tblname)
        if chk is None:
            q = "INSERT INTO tableSupport ('sql_file', 'table_name') VALUES (?, ?)"
            d = (keyd, tblname,)
            r = DBConnect(q, d, self.sql_file).ONE()

    def chk(self, keyd, tblname):
        q = 'SELECT * FROM tableSupport WHERE sql_file=? AND table_name=?'
        d = (keyd, tblname,)
        r = DBConnect(q, d, self.sql_file).ONE()
        print(q, d, r)
        return r

    def create(self):
        sql_file = './db/SUPPORT.sql'
        engine = create_engine(f'sqlite:///{sql_file}')
        meta = MetaData(engine)
        table_name1  = 'tableSupport' 
        t1 = Table(table_name1, meta,
                Column('id', Integer, primary_key=True, autoincrement=True),
                Column('sql_file', Text),
                Column('table_name', Text),
                )
        meta.create_all()
        return sql_file



ts = tabsup()
################## Customer Related Tables ##########################
# Customer Codes
sql_file = './db/CUSTOMERS.sql'
engine = create_engine(f'sqlite:///{sql_file}')

meta = MetaData(engine)
table_name1  = 'customer_codes' 
ts.add(sql_file, table_name1)

t1 = Table(table_name1, meta,
           Column('id', Integer, primary_key=True, autoincrement=True),
                   Column('customer_code', String(30)),
           )

table_name2  = 'customer_basic_info' 
ts.add(sql_file, table_name2)

t2 = Table(table_name2, meta, 
            Column('cust_num', String(30), primary_key=True),
            Column('first_name', String(30)),
            Column('last_name', String(30)),
            Column('middle_initial', String(6)),
            Column('suffix', String(6)),
            Column('prefix', String(6)),
            Column('address_acct_num', String(90)),
            Column('phone_numbers', Text),
            Column('email_addr', String),
            Column('tax_exempt_number', String(50)),
            Column('typecode', String(12)),
            Column('rental_of', Text),
            Column('statement_terms', Text),
            Column('contact1', String),
            Column('contact2', String),
            Column('account_type', String(20)),
            Column('alt_post_acct', String(20)),
            Column('date_added', Date),
            Column('last_maintained', Date),
            Column('last_layaway', Date),
            Column('birthday', Date),
            Column('Charge_Privilege_expiry', Integer),
            Column('full_name', String(130))
            )

ah = datetime.date.today().strftime('%Y-%m-%d')
names = 'cust_num, first_name, last_name, date_added'
values = f"'Test1', 'Alvin', 'Acres', '{ah}'"

table_name3  = 'address_accounts' 
ts.add(sql_file, table_name3)

#a.CreateTestItem(names, values )
t3 = Table(table_name3, meta, 
           Column('addr_acct_num', String(90), primary_key=True),
           Column('street_num', String(12)),
           Column('street_direction', String(10)),
           Column('street_name', String(60)),
           Column('street_type', String(24)),
           Column('unit', String(24)),
           Column('address0', String),
           Column('address2', String),
           Column('address3', String),
           Column('city', String),
           Column('state', String(3)),
           Column('zipcode', String(16))          
           )
           
table_name4  = 'customer_sales_options' 
ts.add(sql_file, table_name4)

t4 = Table(table_name4, meta, 
           Column('cust_num', String(20), primary_key=True),
           Column('tax_exempt', Integer, default=0),
           Column('tax_direct', Integer, default=0),
           Column('no_checks', Integer, default=0),
           Column('pos_clerk_message', Text),
           Column('salesperson', String(12)),
           Column('no_discount', Integer, default=1),
           Column('fixed_discount', Integer, default=0),
           Column('discount_amt', Numeric(4,2), default=00.00)
        )



table_name5  = 'customer_accts_receivable' 
ts.add(sql_file, table_name5)

t5 = Table(table_name5, meta, 
           Column('cust_num', String(20), primary_key=True),
           Column('credit_limit', Numeric(10,2)),
           Column('freeze_charges', Integer, default=1),
           Column('late_charge_exempt', Integer, default=0),
           Column('print_invoice_detail_on_statement', Integer, default=0),
           Column('last_statement_date', Date),
           Column('last_paid_date', Date),
           Column('last_paid_amt', Numeric(12,2), default=0.00),
           Column('partial_cash', Numeric(12,2), default=0.00)
           )


table_name6  = 'customer_shipto_info' 
ts.add(sql_file, table_name6)

t6 = Table(table_name6, meta, 
           Column('cust_num', String(20), primary_key=True),
           Column('name', String(160)),
           Column('phone', String(30)),
           Column('ship_by', String(12)),
           Column('address_acct_num', String(90)),
           Column('comments', Text)
           )


table_name7  = 'customer_notes' 
ts.add(sql_file, table_name7)

t7 = Table(table_name7, meta, 
           Column('cust_num', String(20), primary_key=True),
           Column('notes', Text)
           )


table_name8  = 'customer_security' 
ts.add(sql_file, table_name8)

t8 = Table(table_name8, meta, 
          Column('cust_num', String(20), primary_key=True),
          Column('security_loc', Text)
)
# # Customer Security Photos & Facial Recognition
# table_name = 'customer_security'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# 		Column('cust_num', String(20), primary_key=True),
# 		Column('security_loc', Text),
# JSON security_loc = {[key] : '/path/to/images/'}

table_name9  = 'customer_penalty_info' 
ts.add(sql_file, table_name9)

t9 = Table(table_name9, meta, 
          Column('cust_num', String(20), primary_key=True),
          Column('date_added', Date),
          Column('unpaid_invoice', Integer),
          Column('last_unpaid_date', Date),
          Column('last_avail_credit', Numeric(20,2)),
          Column('score', String(20))
)

meta.create_all()     

### Insert Test Datas for first
conn = engine.connect()

query = 'SELECT count(*) FROM {}'.format(table_name1)
data = []
cnt = SQConnect(query, data, sql_file=sql_file).ONE()[0]
print(cnt)
if cnt == 0:

    vals = [{'customer_code':'GOOD', 'customer_code':'SPICY', 'customer_code':'HOSTILE'}]
    conn.execute(t1.insert(), vals)

query = 'SELECT count(*) FROM {}'.format(table_name2)
data = []
cnt = SQConnect(query, data, sql_file=sql_file).ONE()[0]

if cnt == 0:
    ah = datetime.date.today().strftime('%Y-%m-%d')
    vals = [{'cust_num':'Test1', 'first_name':'Alvin', 'last_name':'Acres', 'dated_added':ah}]
    conn.execute(t2.insert(), vals)

conn.close()


############### Accounting Related Tables ###################
sql_file = './db/ACCOUNTING.sql'

engine = create_engine(f'sqlite:///{sql_file}')
meta = MetaData(engine)
table_name1  = 'general_ledger' 
ts.add(sql_file, table_name1)

## General Ledger
t1 = Table(table_name1, meta,
           Column('transaction_num', Integer, primary_key=True),
           Column('post_acct', String(10)),
           Column('debit', Numeric(15,2)),
           Column('credit', Numeric(15,2)),
           Column('date', Date),
           Column('memo', String(90)),
           Column('account_desc', String(90))
           )

## Ledger Post Accounts
table_name2  = 'ledger_post_accounts' 
ts.add(sql_file, table_name2)

t2 = Table(table_name2, meta, 
           Column('id', Integer, primary_key=True, autoincrement=True),
           Column('account_major', String(5)),
           Column('account_minor', String(5)),
           Column('account_name', String(30))
           )

## PaidOut Routing
table_name3  = 'paidout_routing' 
ts.add(sql_file, table_name3)

t3 = Table(table_name3, meta, 
           Column('id', Integer, primary_key=True, autoincrement=True),
           Column('account_major', String(5)),
           Column('account_minor', String(5)),
           Column('account_name', String(30))
)

meta.create_all()

# Test Item Creation

conn = engine.connect()

query = 'SELECT count(*) FROM {}'.format(table_name3)
data = []
cnt = SQConnect(query, data, sql_file=sql_file).ONE()[0]

#cnt = select([func.count()]).from_table(t3)
if cnt == 0:
    vals    = [{'account_major':'710', 'account_minor':'020', 'account_name':'GAS VAN'},
               {'account_major':'720', 'account_minor':'050', 'account_name':'POSTAGE'},
               {'account_major':'385', 'account_minor':'010', 'account_name':'DRAW'},
               {'account_major':'710', 'account_minor':'030', 'account_name':'VEHICLE REPAIRS'},
               {'account_major':'620', 'account_minor':'010', 'account_name':'CASUAL LABOR'},
               {'account_major':'145', 'account_minor':'010', 'account_name':'INVENTORY'}]
    conn.execute(t3.insert(), vals)

query = 'SELECT count(*) FROM {}'.format(table_name2)
data = []
cnt = SQConnect(query, data, sql_file=sql_file).ONE()[0]

#cnt = select([func.count()]).from_table(t2)
if cnt == 0:
    vals    = [{'account_major':'100', 'account_minor':'010', 'account_name':'Cash Disbursements'},
               {'account_major':'100', 'account_minor':'010', 'account_name':'Cash Receipts'},
               {'account_major':'100', 'account_minor':'010', 'account_name':'Credit Cards'},
               {'account_major':'300', 'account_minor':'010', 'account_name':'Gift Cards'},
               {'account_major':'000', 'account_minor':'000', 'account_name':'Food Stamps'},
               {'account_major':'100', 'account_minor':'020', 'account_name':'Foreign Cash 1'},
               {'account_major':'100', 'account_minor':'030', 'account_name':'Foreign Cash 2'},
               {'account_major':'100', 'account_minor':'040', 'account_name':'Foreign Cash 3'},
               {'account_major':'300', 'account_minor':'020', 'account_name':'Credit Book'},
               {'account_major':'120', 'account_minor':'010', 'account_name':'Accounts Receivable'},
               {'account_major':'145', 'account_minor':'000', 'account_name':'Inventory'},
               {'account_major':'146', 'account_minor':'000', 'account_name':'Layaway Inventory'},
               {'account_major':'300', 'account_minor':'010', 'account_name':'Accounts Payable'},
               {'account_major':'310', 'account_minor':'010', 'account_name':'Sales Tax Payable'},
               {'account_major':'400', 'account_minor':'000', 'account_name':'Store Sales'},
               {'account_major':'500', 'account_minor':'000', 'account_name':'Cost of Sales'},
               {'account_major':'510', 'account_minor':'000', 'account_name':'Inventory Adjustment'},
               {'account_major':'520', 'account_minor':'010', 'account_name':'A/R Adjustments'},
               {'account_major':'400', 'account_minor':'020', 'account_name':'Late Charge Income'},
               {'account_major':'399', 'account_minor':'010', 'account_name':'Retained Earnings'},
               {'account_major':'350', 'account_minor':'010', 'account_name':'Layaway Liability'},
               {'account_major':'110', 'account_minor':'020', 'account_name':'Late Charge Receivable'},
               {'account_major':'110', 'account_minor':'020', 'account_name':'Transfer Receivable'},
               {'account_major':'300', 'account_minor':'020', 'account_name':'Transfer Payable'},
               {'account_major':'300', 'account_minor':'020', 'account_name':'A/P Paid w/ Credit Card'}]
    
    conn.execute(t2.insert(), vals)
    conn.close()


################ Vendor Related Tables #######################
sql_file = './db/VENDORS.sql'
engine = create_engine(f'sqlite:///{sql_file}')
meta = MetaData(engine)
#Vendor Basic Info
table_name1  = 'vendor_basic_info' 
ts.add(sql_file, table_name1)

t1 = Table(table_name1, meta, 
           Column('vend_num', String(20), primary_key=True),
           Column('name', String(60)),
           Column('address1', String(60)),
           Column('address2', String(60)),
           Column('city', String(30)),
           Column('state', String(3)), 
           Column('zip', String(15)),
           Column('acct_num', Text),
           Column('post_acct', String(12)),
           Column('phone', String(30)),
           Column('fax', String(30)),
           Column('email', String),
           Column('terms_days', Integer, default=10),
           Column('discount_percent', Numeric(3,1), default=0.0),
           Column('contact', Text),
           Column('notes', Text)
           )


# Vendor Invoices
table_name2  = 'vendor_invoices' 
ts.add(sql_file, table_name2)

t2 = Table(table_name2, meta,
            Column('vend_num', String(20), primary_key=True),
            Column('acct_num', String(45)),
            Column('date', Date),
            Column('amount', Numeric(10,2)),
            Column('post_date', String(8)),
            Column('terms_day', Integer, default=0),
            Column('discount_percent', Numeric(3,1), default=00.0),
            Column('invoice_num', String(45)),
            Column('post_acct', Text),
            Column('disc_ok', Integer, default=0),
            Column('pay_after', Date),
            Column('date_paid', Date),
            Column('checknum', Integer),
            Column('payment_type', String(12)),
            Column('banknum', Integer),
            Column('cleared', Integer, default=0),
            Column('paid_in_full', Integer, default=0)
            )



table_name3  = 'vendor_invoice_dist_partials' 
ts.add(sql_file, table_name3)

t3 = Table(table_name3, meta, 
           Column('id', Integer, primary_key=True, autoincrement=True),
           Column('vend_num', String(20)),
           Column('acct_num', String(45)),
           Column('invoice_num', String(45)),
           Column('active', Integer, default=0),
           Column('post_acct', String(10)),
           Column('partialAmount', Numeric(10,2), default=0.00),
           Column('discount_OK', Integer),
           Column('discount_amount', Numeric(10,2), default=0.00)
)

table_name4  = 'vendor_invoice_partials' 
ts.add(sql_file, table_name4)

t4 = Table(table_name4, meta, 
           Column('id', Integer, primary_key=True, autoincrement=True),
           Column('vend_num', String(20)),
           Column('acct_num', String(45)),
           Column('invoice_num', String(45)),
           Column('active', Integer, default=0),
           Column('pay_after', Date),
           Column('pay_amount', Numeric(8,2), default=0.00),
           Column('date_paid', Date),
           Column('check_num', Integer),
           Column('payment_type', String(10))          
          )

meta.create_all()

# Add Test Items
query = 'SELECT count(*) FROM {}'.format(table_name1)
data = []
cnt = SQConnect(query, data, sql_file=sql_file).ONE()[0]

#cnt = select([func.count()]).from_table(t1)
if cnt == 0:
    conn = engine.connect()
    vals = [{'vend_num':0, 'name':'Test Account'}]
    conn.execute(t1.insert(), vals)    
    conn.close()

######################## Support Tables ####################
# sql_file = './db/SUPPORT.sql'

# engine = create_engine(f'sqlite:///{sql_file}')
# meta = MetaData(engine)

# # Organizations
# table_name1  = 'organizations' 
# ts.add(sql_file, table_name1)

# t1 = Table(table_name1, meta, 
#           Column('abuser', String(10), primary_key=True),
#           Column('department', Text),
#           Column('category', Text), 
#           Column('subcategory', Text),
#           Column('material', Text),
#           Column('zone', Text),
#           Column('location', Text),
#           Column('unittype', Text),
#           Column('num_of_aisles', Integer, default=0),
#           Column('extra_places', Text),
#           Column('num_of_sections', Integer, default=0),
#           Column('customer_codes', Text),
#           Column('shipping_methods', Text),
#           Column('account_types', Text)
# )


# table_name2 = 'item_num_registry'
# ts.add(sql_file, table_name2)

# t2 = Table(table_name2, meta, 
#            Column('internal_num', String(30), primary_key=True),
#            Column('upc', String(30)))
        

# meta.create_all()



# Add Initial Items
# query = 'SELECT count(*) FROM {}'.format(table_name1)
# data = []
# cnt = SQConnect(query, data, sql_file=sql_file).ONE()[0]

# if cnt == 0:
#     conn = engine.connect()
#     depts = json.dumps(['HARDWARE', 'PLUMBING', 'ELECTRICAL', 'FASTENERS'])
#     cats = json.dumps(['TOOLS', 'PARTS', 'BOLTS', 'FIXTURES'])
#     subcats = json.dumps(['HAND', 'UNDERSINK', 'SAE', 'SAE'])
#     mats = json.dumps(['BRASS', 'STAINLESS', 'STEEL', 'ALUMINUM'])
#     zones = json.dumps(['PAINT1' ,'ELEC1', 'HDWE1', 'FASTENER1', 'PLBG1'])
#     units = json.dumps(['EA', 'RL', 'BX', 'EA'])
#     custcodes = json.dumps(['GOOD', 'BAD', 'HOSTILE'])
#     ships = json.dumps(['UPS', 'FEDEX', 'TRUCK', 'DRONE'])
#     accounttypes = json.dumps(['RESIDENTAL', 'COMMERCIAL', 'INDUSTRIAL', 'GOVT'])
#     vals = [{'abuser':'rhp', 'name':'Test Account', 'department':depts, 'category':cats, 'subcategory':subcats, 'material':mats, 'zone':zones, 'unittype':units, 'customer_codes':custcodes, 'shipping_methods':ships, 'account_types':accounttypes }]
#     conn.execute(t1.insert(), vals)    
#     conn.close()



####################### Organization Tables ##################
sql_file = './db/SUPPORT.sql'
engine = create_engine(f'sqlite:///{sql_file}')
meta = MetaData(engine)

# Department
table_name1  = 'department' 
ts.add(sql_file, table_name1)

t1 = Table(table_name1, meta,
           Column('id', String(30), primary_key=True)
)
           

# Category
table_name2  = 'category' 
ts.add(sql_file, table_name2)

t2 = Table(table_name2, meta,
           Column('id', String(30), primary_key=True)
)

# SubCategory
table_name3  = 'subcategory' 
ts.add(sql_file, table_name3)

t3 = Table(table_name3, meta,
           Column('id', String(30), primary_key=True)
)

# Material
table_name4  = 'material' 
ts.add(sql_file, table_name4)

t4 = Table(table_name4, meta,
           Column('id', String(30), primary_key=True)
)

# Zones
table_name5  = 'zone' 
ts.add(sql_file, table_name5)

t3 = Table(table_name5, meta,
           Column('id', String(30), primary_key=True)
)

# Location
table_name6  = 'location' 
ts.add(sql_file, table_name6)

t6 = Table(table_name6, meta,
           Column('id', String(30), primary_key=True)
)

# Unit Types
table_name7  = 'unittype' 
ts.add(sql_file, table_name7)

t7 = Table(table_name7, meta,
           Column('id', String(30), primary_key=True)           
)

# Aisle Number
table_name8  = 'aisle_num' 
ts.add(sql_file, table_name8)

t8 = Table(table_name8, meta,
           Column('id', String(30), primary_key=True)
)

# Customer Codes
table_name9  = 'customer_codes' 
ts.add(sql_file, table_name9)

t9 = Table(table_name9, meta,
           Column('id', String(30), primary_key=True)
           )

# Shipping Methods
table_name10  = 'shipping_methods' 
ts.add(sql_file, table_name10)

t10 = Table(table_name10, meta,
           Column('id', String(30), primary_key=True)
           )

# Account Types
table_name11  = 'account_types' 
ts.add(sql_file, table_name11)

t3 = Table(table_name11, meta,
           Column('id', String(30), primary_key=True)
           )




meta.create_all()


############### Item Related Tables #########################
sql_file = './db/INVENTORY.sql'

engine = create_engine(f'sqlite:///{sql_file}')
meta = MetaData(engine)

#item retails table
table_name1  = 'item_retails' 
ts.add(sql_file, table_name1)

t1 = Table(table_name1, meta, 
        Column('upc', String(90), primary_key=True),
        Column('standard_unit', Integer, default=1),
        Column('standard_price', Numeric(10,2), default=0.00),
        Column('level_a_unit', Integer, default=1),
        Column('level_a_price', Numeric(10,2), default=0.00),
        Column('level_b_unit', Integer, default=1),
        Column('level_b_price', Numeric(10,2), default=0.00),
        Column('level_c_unit', Integer, default=1),
        Column('level_c_price', Numeric(10,2), default=0.00),
        Column('level_d_unit', Integer, default=1),
        Column('level_d_price', Numeric(10,2), default=0.00),
        Column('level_e_unit', Integer, default=1),
        Column('level_e_price', Numeric(10,2), default=0.00),
        Column('level_f_unit', Integer, default=1),
        Column('level_f_price', Numeric(10,2), default=0.00),
        Column('level_g_unit', Integer, default=1),
        Column('level_g_price', Numeric(10,2), default=0.00),
        Column('level_h_unit', Integer, default=1),
        Column('level_h_price', Numeric(10,2), default=0.00),
        Column('level_i_unit', Integer, default=1),
        Column('level_i_price', Numeric(10,2), default=0.00),
        Column('compare_unit', Integer, default=1),
        Column('compare_price', Numeric(10,2), default=0.00),
        Column('on_sale_unit', Integer, default=1),
        Column('on_sale_price', Numeric(10,2), default=0.00)
)

                  
# Item Detailed table
#   JSON'd Vendors
#   vendors = { '1' = 
#                   id : 0-9A-Z
#                   ordernum : ordernum
#                   last_cost : 0.00
#                   lead_time : 0 in days
#             }
#
table_name2  = 'item_detailed' 
ts.add(sql_file, table_name2)

t2 = Table(table_name2, meta, 
        Column('upc', String(90), primary_key=True),
        Column('general_description', String(150)),
        Column('specific_description', String(150)),
        Column('avg_cost', Numeric(10,3), default=0.000),
        Column('last_cost', Numeric(10,3), default=0.000),
        Column('quantity_on_hand', Numeric(12,3), default=0.000),
        Column('quantity_committed', Numeric(12,3), default=0.000),
        Column('quantity_on_layaway', Numeric(12,3), default=0.000),
        Column('part_num', String(90)),
        Column('oempart_num', String(90)),
        Column('kit_num', String(90)),
        Column('kit_pieces', Integer, default=1)
)
# a.CreateTestItem('upc, description',"'0', 'Test Item'")


# Closeouts
table_name3  = 'closeouts' 
ts.add(sql_file, table_name3)

t3 = Table(table_name3, meta, 
            Column('upc', String(90), primary_key=True),
              Column('avg_cost', Numeric(10,3), default=0.000),
              Column('last_retail', Numeric(10,3), default=0.000),
              Column('downtrend', Integer, default=30),
              Column('lose_percent', Integer, default=3),
              Column('closeout_date', Date)
)

#Alt Lookups
table_name4  = 'altlookups' 
ts.add(sql_file, table_name4)

#a = TableAware(table_name, sql_file, dbtype='sqlite3')
t4 = Table(table_name4, meta, 		
        Column('upc', String(90), primary_key=True),
        Column('altlookup1', String(90)),
        Column('altlookup2', String(90)),
        Column('altlookup3', String(90)),
        Column('altlookup4', String(90)),
        Column('altlookup5', String(90)),
        Column('altlookup6', String(90)),
        Column('altlookup7', String(90)),
        Column('altlookup8', String(90)),
        Column('altlookup9', String(90)),
        Column('altlookup10', String(90)),
        Column('altlookup11', String(90)),
        Column('altlookup12', String(90)),
        Column('altlookup13', String(90)),
        Column('altlookup14', String(90)),
        Column('altlookup15', String(90)),
        Column('altlookup16', String(90))
)
                 
                  
# Flexible Retail Program
table_name5  = 'flexible_update' 
ts.add(sql_file, table_name5)

#a = TableAware(table_name, sql_file, dbtype='sqlite3')
t5 = Table(table_name5, meta,
        Column('upc', String(90), primary_key=True),
        Column('avg_cost', Numeric(10,3), default=0.000),
        Column('max_margin', Numeric(10,3), default=0.000),
        Column('last_update', Date)
)


# Tax Holiday Table
table_name6  = 'tax_holiday' 
ts.add(sql_file, table_name6)

#a = TableAware(table_name, sql_file, dbtype='sqlite3')
t6 = Table(table_name6, meta,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('name', String(90)),
        Column('begin_date', Date),
        Column('end_date', Date),
        Column('upc', Text),
        Column('active', Integer)
)



#for i in range(1,7):
#    a.CreateTestItem('id',"'{}'".format(i)) 

# Item Detailed2 table
table_name7  = 'item_detailed2' 
ts.add(sql_file, table_name7)

t7 = Table(table_name7, meta,
        Column('upc', String(90), primary_key=True),
        Column('do_not_discount', Integer, default=0),
        Column('lock_prices', Integer, default=0),
        Column('tax1', Integer, default=0),
        Column('tax2', Integer, default=0),
        Column('tax3', Integer, default=0),
        Column('tax4', Integer, default=0),
        Column('tax_never', Integer, default=0),
        Column('override_tax_rate', Numeric(5,4), default=0.0000),
        Column('sale_begin', Date),
        Column('sale_end', Date),
        Column('sale_begin_time', Time),
        Column('sale_end_time', Time),
        Column('buyX', Integer, default=0),
        Column('getY', Integer, default=0),
        Column('deactivate_when_out', Integer, default=0),
        Column('case_break_num', String(90)),
        Column('substituteYN', Integer, default=0),
        Column('substitute_num', String(90)),
        Column('location', String(45)),
        Column('weight', Numeric(6,3), default=0.000),
        Column('tare_weight', Numeric(6,3), default=0.000),
        Column('image_location', String(250)),
        Column('last_saledate', Date),
        Column('last_returndate', Date),
        Column('maint_date', Date),
        Column('added_date', Date),
        Column('override_commission', Integer, default=0),
        Column('over_commission', Numeric(6,4), default=0.0000),
        Column('over_fixd_comm', Numeric(6,2), default=0.00),
        Column('priceschema', String(3)),
        Column('orderctrl', Text)
)

#a.CreateTestItem('upc', "'0'")


# Consignment Options - Consignment Page Options 
table_name8  = 'consignments' 
ts.add(sql_file, table_name8)

#a = TableAware(table_name, sql_file, dbtype='sqlite3')
t8 = Table(table_name8, meta,
        Column('upc', String(90), primary_key=True),
        Column('vendor_num', String(90)),
        Column('override_fee', Numeric(6,3))
)


# Item Options - info you gotta know to make sense of other things
table_name9  = 'item_options' 
ts.add(sql_file, table_name9)

#a = TableAware(table_name, sql_file, dbtype='sqlite3')
t9 = Table(table_name9, meta,
        Column('upc', String(90), primary_key=True),
        Column('department', String(15)),
        Column('category', String(15)),
        Column('subcategory', String(15)),
        Column('material', String(15)),
        Column('location', String(15)),
        Column('postacct', String(12)),
        Column('unit_type', String(10)),
        Column('item_type', String(15)),
        Column('agepopup', Integer, default=0),
        Column('posoptions', Text),
        Column('consignment', Integer, default=0),
        Column('unitsinpackage', Integer, default=1),
        Column('foodstampexempt', Integer, default=1),
        Column('loyaltyexempt', Integer, default=0),
        Column('deactivated', Integer, default=0),
        Column('aisle_num', String(3)),
        Column('extra_places', String(30)),
        Column('section_num', String(15)),
        Column('closeout', Integer,  default=0),
        Column('assume_1_sold', Integer, default=0),
        Column('Prompt for Qty',Integer, default=0),
        Column('Prompt for Price', Integer, default=0)
)
        

#a.CreateTestItem('upc', "'0'")

# POSoptions via JSON
#   Prompt for Quantity = Y/N
#   Assume 1 Sold = Y/N
#   Prompt for Price, Quantity Calculated = Y/N
#   Prompt for scale = Y/N


# Item Pricing Schemes table
table_name10  = 'item_pricing_schemes' 
ts.add(sql_file, table_name10)

#a = TableAware(table_name, sql_file, dbtype='sqlite3')
t10 = Table(table_name10, meta,
        Column('name', String(10), primary_key=True),
        Column('scheme_list', Text),
        Column('reduce_by', String(90), default="2.5")
)

#a.CreateTestItem('name, scheme_list, reduce_by', "'1-3-10','1-3-10', 2.50")

                  
# Item Vendor Data
table_name11  = 'item_vendor_data' 
ts.add(sql_file, table_name11)

#a = TableAware(table_name, sql_file, dbtype='sqlite3')
t11 = Table(table_name11, meta, 
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('upc', String(90)),
        Column('vendor_num', String(10)), 
        Column('order_num', String(90)),
        Column('lead_time', Integer),
        Column('minimum_order', Integer),
        Column('last_order_qty', Integer),
        Column('last_order_date', Date),
        Column('last_received_qty', Integer),
        Column('last_received_date', Date),
        Column('units_in_order', Integer)
        )

# Item Notes
table_name12  = 'item_notes' 
ts.add(sql_file, table_name12)

#a = TableAware(table_name, sql_file, dbtype='sqlite3')
t12 = Table(table_name12, meta,
        Column('upc', String(90), primary_key=True),
        Column('notes', Text)
)

#a.CreateTestItem('upc', "'0'")

# Item POS Sales Links
table_name13  = 'item_sales_links' 
ts.add(sql_file, table_name13)

#a = TableAware(table_name13, sql_file, dbtype='sqlite3')
t13 = Table(table_name13, meta,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('upc', String(90)),
        Column('sales_link_upc', String(90)),
        Column('message', String(90))
)

#a.CreateTestItem('upc', "'0'")


# Item Customer Instructions
table_name14  = 'item_cust_instructions' 
ts.add(sql_file, table_name14)

#a = TableAware(table_name, sql_file, dbtype='sqlite3')
t14 = Table(table_name14, meta,
        Column('upc', String(90), primary_key=True),
        Column('print_info_options', Integer),
        Column('print_return_options', Integer),
        Column('print_warranty_options', Integer),
        Column('info_dialog', String(45)),
        Column('return_dialog', String(45)),
        Column('warranty_dialog', String(45)),
        Column('info_box', Text),
        Column('return_box', Text),
        Column('warranty_box', Text)
)

#a.CreateTestItem('upc', "'0'")


# Item History
table_name15  = 'item_history' 
ts.add(sql_file, table_name15)

#a = TableAware(table_name, sql_file, dbtype='sqlite3')
t15 = Table(table_name15, meta,
        Column('upc', String(90), primary_key=True),
        Column('year', Integer),
        Column('January', Numeric(20,3)),
        Column('February', Numeric(20,3)),
        Column('March', Numeric(20,3)),
        Column('April', Numeric(20,3)),
        Column('May', Numeric(20,3)),
        Column('June', Numeric(20,3)),
        Column('July', Numeric(20,3)),
        Column('August', Numeric(20,3)),
        Column('September', Numeric(20,3)),
        Column('October', Numeric(20,3)),
        Column('November', Numeric(20,3)),
        Column('December', Numeric(20,3))
)

#a.CreateTestItem('upc', "'0'")

meta.create_all()

# Test Item Create
lst = [(t1, table_name1), (t2, table_name2), (t3, table_name3), (t4, table_name4),
       (t5, table_name5), (t6, table_name6), (t7, table_name7), (t8, table_name8),
       (t9, table_name9), (t10, table_name10), (t11, table_name11), (t12, table_name12),
       (t13, table_name13), (t14, table_name14), (t15, table_name15)]

idx = 1
for tname, xix in lst:
    query = 'SELECT count(*) FROM {}'.format(xix)
    data = []
    cnt = SQConnect(query, data, sql_file=sql_file).ONE()[0]
    
    if cnt == 0:
        conn = engine.connect()
        
        vals = [{'upc':'0'}]
        if idx == 2:
            vals = [{'upc':'0', 'general_description':'Test Item'}]
        
        if idx == 6:
            vals = []
            c = {}
            for xi in range(1,7):
                c = {'id': xi}
                vals.append(c)

        if idx == 10:
            vals = [{'name':'1-3-10', 'scheme_list':'1-3-10', 'reduce_by':2.50}]
            
        pout.v(f'{tname} == {vals} == {idx}')
        conn.execute(tname.insert(), vals)
        conn.close()
    idx += 1
    

############# Transaction Related Tables #####################
sql_file = './db/TRANSACTIONS.sql'

engine = create_engine(f'sqlite:///{sql_file}')
meta = MetaData(engine)

# Transaction Ctrl Number
table_name1  = 'transaction_control' 
ts.add(sql_file, table_name1)

#a = TableAware(table_name, sql_file, dbtype='sqlite3')
t1 = Table(table_name1, meta,
        Column('abuser', String(10), primary_key=True),
        Column('trans_num', Integer)
)
#a.CreateTestItem('abuser, trans_num', "'rhp', 1")
vals1 = [{'abuser':'rhp', 'trans_num':'1'}]    

# Transactions
table_name2  = 'transactions' 
ts.add(sql_file, table_name2)

#a = TableAware(table_name, sql_file, dbtype='sqlite3')
t2 = Table(table_name2, meta,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('transaction_id', String(15)),
        Column('date', Date),
        Column('salesperson', Integer),
        Column('time', Time),
        Column('cust_num', String(30)),
        Column('address_acct_num', String(90)),
        Column('upc', String(90)),
        Column('general_description', String(150)),
        Column('specific_description', String(150)),
        Column('quantity', Numeric(20,3)),
        Column('avg_cost', Numeric(20,3)),
        Column('unit_price', Numeric(20,2)),
        Column('total_price', Numeric(20,2)),
        Column('pricetree', Text),
        Column('discount', String(20)),
        Column('type_of_transaction', String(15)),
        Column('tax1', Integer, default=0),
        Column('tax2', Integer, default=0),
        Column('tax3', Integer, default=0),
        Column('tax4', Integer, default=0),
        Column('tax_never', Integer, default=0),
        Column('tax_exempt', Integer,  default=0),
        Column('po_number', String(120))
)

#fieldnames = '''transaction_id, date, salesperson, time, cust_num, address_acct_num, 
#upc, description, quantity, avg_cost, unit_price, total_price, pricetree, discount, type_of_transaction,
#tax1, tax2, tax3, tax4, tax_never, tax_exempt, po_number'''
#values = """'00000000', '20201016', '1', '10:10:00', '37047734', '', 
# 'BEEFSTICK', 'Jack Links BeefStick',3, 0.65, 0.99, 2.97,'',0, 'SALE',
# 1, 1, 1, 1, 1, 1, ''"""
# a.CreateTestItem(fieldnames, values)

    
#CreateTable(sql_file, table_name, column_info)
# per item entry per row, no primary_key=True

#Transaction Payments
table_name3  = 'transaction_payments' 
ts.add(sql_file, table_name3)

#a = TableAware(table_name, sql_file, dbtype='sqlite3')
t3 = Table(table_name3, meta,
        Column('transaction_id', String(15), primary_key=True),
        Column('paid', Numeric(20,2), default=0.00),
        Column('discount_taken', Numeric(20,2), default=0.00),
        Column('subtotal_price', Numeric(20,2), default=0.00),
        Column('tax', Numeric(20,2), default=0.00),
        Column('total_price', Numeric(20,2), default=0.00),
        Column('paid_date', Date),
        Column('date', Date),
        Column('time', Time),
        Column('cust_num', String(30)),
        Column('address_acct_num', String(90)),
        Column('pay_method', String(15)),
        Column('change_back', Numeric(20,2)),
        Column('type_of_transaction', String(15)),
        Column('cash_payment', Numeric(20,2)),
        Column('check_payment', Numeric(20,2)),
        Column('check_num', String(30)),
        Column('dl_number', String(90)),
        Column('phone_num', String(15)),
        Column('dob', String(12)),
        Column('charge', Numeric(20,2), default=0.00),
        Column('card1_payment', Numeric(20,2), default=0.00),
        Column('auth1_num', String(60)),
        Column('card1_type', String(60)),
        Column('card1_numbers', String(36)),
        Column('card2_payment', Numeric(20,2), default=0.00),
        Column('auth2_num', String(60)),
        Column('card2_numbers', String(36)),
        Column('card2_type', String(60)),
        Column('card3_payment', Numeric(20,2), default=0.00),
        Column('auth3_num', String(60)),
        Column('card3_numbers', String(36)),
        Column('card3_type', String(60)),
        Column('card4_payment', Numeric(20,2), default=0.00),
        Column('auth4_num', String(60)),
        Column('card4_numbers', String(36)),
        Column('card4_type', String(60)),
        Column('card5_payment', Numeric(20,2), default=0.00),
        Column('auth5_num', String(60)),
        Column('card5_numbers', String(36)),
        Column('card5_type', String(60)),
        Column('debit_payment', Numeric(20,2), default=0.00),
        Column('auth6_num', String(60)),
        Column('debit_numbers', String(36)),
        Column('debit_type', String(60))
)


#Transaction Notes
table_name4  = 'transaction_notes' 
ts.add(sql_file, table_name4)

#a = TableAware(table_name, sql_file, dbtype='sqlite3')
t4 = Table(table_name4, meta,
        Column('station_num', String(3)),
        Column('transaction_id', String(15)),
        Column('line_position', String(15)),
        Column('note', Text)            
)

meta.create_all()

# query = 'SELECT count(*) FROM {}'.format(table_name2)
# data = []
# cnt = SQConnect(query, data, sql_file=sql_file).ONE()[0]

# #select([func.count()]).from_table(t2):
# if cnt == 0: 
#     conn = engine.connect()
#     conn.execute(t2.insert(), vals2)
#     conn.close()

############## General Operations Related Tables ##############
sql_file = './db/CONFIG.sql'
engine = create_engine(f'sqlite:///{sql_file}')
meta = MetaData(engine)

vals = {}
# Store info
table_name1  = 'basic_store_info' 
ts.add(sql_file, table_name1)

#a = TableAware(table_name, sql_file, dbtype='sqlite3')
t1 = Table(table_name1, meta,
        Column('store_num', Integer, primary_key=True),
        Column('name', String(90)),
        Column('address1', String(90)),
        Column('address2', String(90)),
        Column('city', String(30)),
        Column('state', String(3)),
        Column('zip', String(15)),
        Column('phone1', String(30)),
        Column('phone2', String(30)),
        Column('fax', String(30)),
        Column('email', String(150)),
        Column('print_on_forms', Integer, default=0),
        Column('late_charge', Numeric(3,2)),
        Column('cust_id_title', String(50)),
        Column('penny_tally', Numeric(12,2)),
        Column('website', Text),
        Column('logo', Text)
)
vals[1] = [{'store_num': '0', 'name':'RHP Hardware', 'address1':'111 Hill St', 'city':'Ipsum City', 'state':'OH', 'zip':'45632' }]
#a.CreateTestItem("store_num, name, address1, city, state, zip","0,'ABC Hardware','111 Hill St','Ipsum City','OH','45632'")

# POS Controls
table_name2  = 'pos_controls' 
ts.add(sql_file, table_name2)

#a = TableAware(table_name, sql_file, dbtype='sqlite3')
t2 = Table(table_name2, meta,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('print_receipt_ondemand', Integer, default=0),
        Column('prompt_for_qty', Integer, default=0),
        Column('add_cust', Integer, default=0),
        Column('add_items', Integer, default=0),
        Column('payment_on_acct', Integer, default=0),
        Column('verify_assigned_discounts', Integer, default=0),
        Column('report_out_of_stock', Integer, default=0),
        Column('disable_credit_security', Integer, default=0),
        Column('print_signature_line', Integer, default=0),
        Column('skip_finished_question', Integer, default=0),
        Column('print_item_count', Integer, default=0),
        Column('track_salesperson', Integer, default=0),
        Column('mailing_list_capture', Integer, default=0),
        Column('disable_open_drawer', Integer, default=0),
        Column('dept_totals_by_drawer', Integer, default=0),
        Column('omit_cust_addr', Integer, default=0),
        Column('print_totals_on_logoff', Integer, default=0),
        Column('save_cleared_totals_to_reconcile', Integer, default=0),
        Column('verify_parts_explosion', Integer, default=0),
        Column('display_parts_explosion', Integer, default=0),
        Column('print_kit_parts', Integer, default=0),
        Column('print_kit_parts_price', Integer, default=0),
        Column('discount_omit_price', Integer, default=0),
        Column('trap_zips', Integer, default=0),
        Column('prompt_for_cost', Integer, default=0),
        Column('print_item_num', Integer, default=0),
        Column('support_eos_discount', Integer, default=0),
        Column('no_alt_tax', Integer, default=0),
        Column('notify_if_cost_gt_price', Integer, default=0),
        Column('omit_you_saved_line', Integer, default=0),
        Column('offer_on_hold_options', Integer, default=0),
        Column('print_void_trans', Integer, default=0),
        Column('exclude_layaways', Integer, default=0),
        Column('exclude_orders', Integer, default=0),
        Column('exclude_quotes', Integer, default=0),
        Column('exclude_hold', Integer, default=0)
)
vals[2] = [{'id':1}]

# POS Messages
table_name3  = 'pos_messages' 
ts.add(sql_file, table_name3)

#a = TableAware(table_name, sql_file, dbtype='sqlite3')
t3 = Table(table_name3, meta,
        Column('abuser', String(10), primary_key=True),
        Column('conditions', Text),
        Column('return_policy', Text),
        Column('warranty', Text),
        Column('charge_agreement', Text),
        Column('credit_card_agreement', Text),
        Column('thanks', Text),
        Column('check_policy', Text),
        Column('layaway_policy', Text),
        Column('gift_loyalty', Text),
        Column('special_event', Text)
)

return_policy='30 Day Return, Package unopened, item unused'
charge_agree='You agree to pay in full every month before the 30th'
cc_agree='The way of the future, Hooray for a cashless society'
thanks='Thank you for your business'
check_policy='Nope, no thanks, never, NO CHECKS!!!!'
vals[3] = [{'abuser':'rhp', 'return_policy':return_policy, 'charge_agreement':charge_agree, 'credit_card_agreement':cc_agree, 'thanks':thanks, 'check_policy':check_policy}]
#a.CreateTestItem('abuser, return_policy, charge_agreement, credit_card_agreement, thanks, check_policy', f"'rhp','{return_policy}','{charge_agree}','{cc_agree}','{thanks}','{check_policy}'")


# Store Closing Options
table_name4  = 'store_closing_options' 
ts.add(sql_file, table_name4)

#a = TableAware(table_name, sql_file, dbtype='sqlite3')
t4 = Table(table_name4, meta,
        Column('combined_trans_detail', Integer, default=0),
        Column('trans_by_pay_type', Integer, default=0),
        Column('trans_by_salesperson', Integer, default=0),
        Column('trans_by_drawer', Integer, default=0),
        Column('tax_audit_report', Integer, default=0),
        Column('item_sales_by_deptcat', Integer, default=0),
        Column('deptcat_option', Integer, default=0),
        Column('exit_after_closing', Integer, default=0),
        Column('do_not_print_hardcopy', Integer, default=0)
)


table_name5  = 'reports_closing_daily' 
ts.add(sql_file, table_name5)

#a = TableAware(table_name, sql_file, dbtype='sqlite3')
t5 = Table(table_name5, meta,
        Column('abuser', String(10), primary_key=True),
        Column('all_transactions', Integer,  default=1),
        Column('cash_drawer_totals', Integer,  default=1),
        Column('customer_invoiced', Integer,  default=0)
)

#a.CreateTestItem('abuser', "'rhp'")
vals[5] = [{'abuser':'rhp'}]

table_name6  = 'reports_closing_weekly' 
ts.add(sql_file, table_name6)

#a = TableAware(table_name, sql_file, dbtype='sqlite3')
t6 = Table(table_name6, meta,
        Column('abuser', String(10), primary_key=True),
        Column('sales_breakdown', Integer,  default=1),
        Column('inventory_top10', Integer,  default=1),
        Column('inventory_losers10', Integer,  default=1),
        Column('inventory_most_requested', Integer,  default=1)                 
) 

vals[6] = [{'abuser':'rhp'}]

#a.CreateTestItem('abuser', "'rhp'")

#
# table_name = 'reports_closing_monthly'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# 		Column('abuser', String(10), primary_key=True),
# 		Column('sales_breakdown', Integer,  default=1),
# 		Column('inventory_top50', Integer,  default=1),
# 		Column('inventory_losers50', Integer,  default=1),
# 		Column('inventory_most_requested', Integer,  default=1),
# 		Column('tax_report', Integer,  default=1),

# a.CreateTestItem('abuser', "'rhp'")

#
# table_name7  = 'reports_closing_quarterly' 
# ts.add(sql_file, table_name7)

# #a = TableAware(table_name, sql_file, dbtype='sqlite3')
# t7 = Table(table_name7, meta, 
#         Column('abuser', String(10), primary_key=True),
#         Column('sales_breakdown', Integer,  default=1),
#         Column('inventory_top100', Integer,  default=1),
#         Column('inventory_losers100', Integer,  default=1)
# )

# vals[7] = [{'abuser':'rhp'}]
# #a.CreateTestItem('abuser', "'rhp'")

# #
# table_name8  = 'reports_closing_yearly' 
# ts.add(sql_file, table_name8)

# #a = TableAware(table_name, sql_file, dbtype='sqlite3')
# t8 = Table(table_name8, meta, 
#         Column('abuser', String(10), primary_key=True),
#         Column('year', Date),
#         Column('sales_breakdown', Integer,  default=1),
#         Column('inventory_top250', Integer,  default=1),
#         Column('inventory_losers250', Integer,  default=1)
# )
# vals[8] = [{'abuser':'rhp'}]
# #a.CreateTestItem('abuser', "'rhp'")

#
#Payment Methods
table_name9  = 'payment_methods' 
ts.add(sql_file, table_name9)

#a = TableAware(table_name, sql_file, dbtype='sqlite3')
t9 = Table(table_name9, meta, 
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('cash', Integer, default=0),
        Column('checks', Integer, default=0),
        Column('house_charges', Integer, default=0),
        Column('credit_cards', Integer, default=0),
        Column('credit_book', Integer, default=0),
        Column('food_stamps', Integer, default=0),
        Column('foreign_cash', Integer, default=0),
        Column('loyalty_card', Integer, default=0),
        Column('giftcard', Integer, default=0),
        Column('check_setup_def_state', String(20)),
        Column('check_setup_def_guarrantor', String(20))
)


table_name10  = 'tax_tables' 
ts.add(sql_file, table_name10)

#a = TableAware(table_name, sql_file, dbtype='sqlite3')
t10 = Table(table_name10, meta, 
        Column('tax_name', String(20), primary_key=True),
        Column('GLsub', Integer, default=000),
        Column('RNDscheme', Integer, default=0),
        Column('APscheme', Integer, default=0),
        Column('no_pennies_rounding', Integer, default=0),
        Column('min_sale', Numeric(5,2), default=0.00),
        Column('max_sale', Numeric(5,2), default=0.00),
        Column('item_max', Numeric(5,2), default=0.00),
        Column('from_amt0', Numeric(5,2), default=0.00),
        Column('tax_rate0', Numeric(6,5), default=0.00000),
        Column('from_amt1', Numeric(5,2), default=0.00),
        Column('tax_rate1', Numeric(6,5), default=0.00000),
        Column('from_amt2', Numeric(5,2), default=0.00),
        Column('tax_rate2', Numeric(6,5), default=0.00000)
)



# Passwords
table_name11  = 'passwords' 
ts.add(sql_file, table_name11)

#a = TableAware(table_name, sql_file, dbtype='sqlite3')
t11 = Table(table_name11, meta, 
        Column('abuser', String(15), primary_key=True, default="'rhp'"),
        Column('admin_key', String(15)),
        Column('manager_key', String(15)),
        Column('clerk_key', String(15)),
        Column('acctreceivable', String(15)),
        Column('inventoryctrl', String(15)),
        Column('acctpayable', String(15)),
        Column('financials', String(15)),
        Column('employees', String(15)),
        Column('store_controls_maint', String(15)),
        Column('profit_pic', String(15)),
        Column('close_the_store', String(15)),
        Column('cash_drawer_display', String(15)),
        Column('restrict_data_access', String(15)),
        Column('exceed_credit', String(15)),
        Column('tools_menu', String(15)),
        Column('req_drawer_access', Integer, default=0),
        Column('req_cash_check', Integer, default=0),
        Column('req_cancel_trans', Integer, default=0),
        Column('req_coupons', Integer, default=0),
        Column('req_giftcard_override', Integer, default=0)
)
vals[11] = [{'abuser':'rhp', 'admin_key':'rhp', 'manager_key':'god', 'clerk_key':'123'}]
#a.CreateTestItem('abuser, admin_key, manager_key, clerk_key', "'rhp', 'rhp', 'god', '123'")


#Closeouts Options
table_name12  = 'closeout_options' 
ts.add(sql_file, table_name12)

#a = TableAware(table_name, sql_file, dbtype='sqlite3')
t12 = Table(table_name12, meta, 
        Column('abuser', String(90), primary_key=True),
        Column('autoadd', Integer,  default=0),
        Column('start_age', String(11), default='365'),
        Column('discount_percent', String(11), default='10'),
        Column('max_cost_percent', String(11), default='90'),
        Column('incremental_days', String(11), default='30')
)

vals[12] = [{'abuser':'rhp'}]
#a.CreateTestItem('abuser', "'rhp'")


# Misc Options
table_name13  = 'misc_options' 
ts.add(sql_file, table_name13)

#a = TableAware(table_name, sql_file, dbtype='sqlite3')
t13 = Table(table_name13, meta, 
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('inventory_price_label_on', Integer, default=0),
        Column('inventory_shelf_label_spool', Integer, default=0),
        Column('inventory_omit_label_prices', Integer, default=0),
        Column('ap_canadian_cheques', Integer, default=0)
)



# Themes
table_name14  = 'themes' 
ts.add(sql_file, table_name14)

#a = TableAware(table_name, sql_file, dbtype='sqlite3')
t14 = Table(table_name14, meta, 
        Column('theme_name', String(25), primary_key=True),
        Column('bg', String(50), default="'#ffffff'"),
        Column('text', String(50), default="'#000000'"),
        Column('cell', String(50), default="'#d6fcd7'"),
        Column('info', String(50), default="'#f8fda9'"),
        Column('note', String(50), default="'#e8f4f0'")
)
vals[14] = [{'theme_name':'INVENTORY'}, {'theme_name':'CUSTOMERS'}, {'theme_name':'VENDORS'},{'theme_name':'POS'}]

                
# Employees
table_name15  = 'employees' 
ts.add(sql_file, table_name15)

#a = TableAware(table_name, sql_file, dbtype='sqlite3')
t15 = Table(table_name15, meta, 
        Column('num', String(6), primary_key=True),
        Column('name', String(160)),
        Column('date_of_birth', Date),
        Column('ssn', String(15))
)
dob = datetime.datetime.strptime('20121222', '%Y%m%d')
vals[15] = [{'num':'0', 'name':'Alvin Acres', 'date_of_birth':dob, 'ssn':'234422341'}]

# Discount Class
table_name16  = 'discount_class' 
ts.add(sql_file, table_name16)

t16 = Table(table_name16, meta, 
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('class_name', String(90)),
        Column('department', String(15)),
        Column('category', String(15)),
        Column('subcategory', String(15)),
        Column('price_level', String(15)),
        Column('percentage', Numeric(5,2))
        )


# Item Margin
table_name17  = 'item_margin' 
ts.add(sql_file, table_name17)

#a = TableAware(table_name, sql_file, dbtype='sqlite3')
t17 = Table(table_name17, meta, 
        Column('abuser', String(15), primary_key=True),
        Column('starting_margin_control', Integer, default=0),
        Column('general_margin', Numeric(6,3), default=50.0000),
        Column('by_category', Text)
)

vals[17] = [{'abuser':'rhp'}]

# Margin By Category
table_name18  = 'margin_by_category' 
ts.add(sql_file, table_name18)

#a = TableAware(table_name, sql_file, dbtype='sqlite3')
t18 = Table(table_name18, meta, 
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('department', String(15)),
        Column('category', String(15)),
        Column('subcategory', String(15)),
        Column('margin', Numeric(10,3))
)


#Margin by Cost                  
table_name19  = 'margin_by_cost' 
ts.add(sql_file, table_name19)

#a = TableAware(table_name, sql_file, dbtype='sqlite3')
t19 = Table(table_name19, meta, 
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('label', String(15)),
        Column('greater_than', Numeric(10,2)),
        Column('less_than', Numeric(10,2)),
        Column('margin', Numeric(10,2))
)


# Discount Options
table_name20  = 'discount_options' 
ts.add(sql_file, table_name20)

#a = TableAware(table_name, sql_file, dbtype='sqlite3')
t20 = Table(table_name20, meta, 
        Column('name', String(45), primary_key=True),
        Column('percent', Numeric(3,2), default=0.00)
)


# Hardware Configs
table_name21  = 'hardware_config' 
ts.add(sql_file, table_name21)

#a = TableAware(table_name21, sql_file, dbtype='sqlite3')
t21 = Table(table_name21, meta, 
        Column('abuser', String(15), primary_key=True),
        Column('vendor_id', String(15)), 
        Column('product_id', String(15)),
        Column('interface_id', String(15)),
        Column('input_endpoint', String(15)),
        Column('output_endpoint', String(15))
)

meta.create_all()

lst = [(t1, table_name1), (t2, table_name2), (t3, table_name3), (t4, table_name4),
       (t5, table_name5), (t6, table_name6), (t7, table_name7), (t8, table_name8),
       (t9, table_name9), (t10, table_name10), (t11, table_name11), (t12, table_name12),
       (t13, table_name13), (t14, table_name14), (t15, table_name15), (t16, table_name16),
       (t17, table_name17), (t18, table_name18), (t19, table_name19), (t20, table_name20),
       (t21, table_name21)]


for i, (ti, tname) in enumerate(lst, start=1):
    try:
        if vals[i]:
            query = 'SELECT count(*) FROM {}'.format(tname)
            data = []
            cnt = SQConnect(query, data, sql_file=sql_file).ONE()[0]

            if cnt == 0:
                conn = engine.connect()
                conn.execute(ti.insert(), vals[i])
                conn.close()
    except KeyError as ke:
        print(ke)
    except TypeError as te:
        print(te)

# ############## Table Support ######################
# sql_file = './db/SUPPORT.sql'

# engine = create_engine(f'sqlite:///{sql_file}')
# meta = MetaData(engine)
# table_name1  = 'tableSupport' 

# t1 = Table(table_name1, meta,
#            Column('id', Integer, primary_key=True, autoincrement=True),
#            Column('sql_file', Text),
#            Column('table_name', Text),
#            )

# meta.create_all()


# query = 'SELECT count(*) FROM {}'.format(t1)
# data = []
# cnt = SQConnect(query, data, sql_file=sql_file).ONE()[0]
# print(cnt)
# if cnt == 0:
#     vals = ts.get()
#     pout.v(vals)
#     #conn.execute(t1.insert(), vals)

# a.CreateTestItem('sql_file, table_name','CUSTOMERS.sql, customer_codes')
# a.CreateTestItem('sql_file, table_name','CUSTOMERS.sql, customer_basic_info', extra=True)
# a.CreateTestItem('sql_file, table_name','CUSTOMERS.sql, address_accounts')
# a.CreateTestItem('sql_file, table_name','CUSTOMERS.sql, customer_sales_options')
# a.CreateTestItem('sql_file, table_name','CUSTOMERS.sql, customer_accts_receivable')
# a.CreateTestItem('sql_file, table_name','CUSTOMERS.sql, customer_shipto_info')
# a.CreateTestItem('sql_file, table_name','CUSTOMERS.sql', 'customer_notes'),
#                ('CUSTOMERS.sql', 'customer_security'),
#                ('ACCOUNTING.sql', 'general_ledger'),
#                ('ACCOUNTING.sql', 'ledger_post_accounts'),
#                ('ACCOUNTING.sql', 'paidout_routing'),
#                ('VENDORS.sql', 'vendor_basic_info'),
#                ('VENDORS.sql', 'vendor_invoices'),
#                ('VENDORS.sql', 'vendor_notes'),
#                ('SUPPORT.sql', 'organizations'),
#                ('SUPPORT.sql', 'department_list'),
#                ('SUPPORT.sql', 'category_list'),
#                ('SUPPORT.sql', 'subcategory_list'),
#                ('SUPPORT.sql', 'location_list'),
#                ('SUPPORT.sql', 'unittype_list'),
#                ('SUPPORT.sql', 'shipping_methods'),
#                ('SUPPORT.sql', 'account_types'),
#                ('INVENTORY.sql', 'item_detailed'),
#                ('INVENTORY.sql', 'item_detailed2'),
#                ('INVENTORY.sql', 'item_options'),
#                ('INVENTORY.sql', 'item_pricing_schemes'),
#                ('INVENTORY.sql', 'item_vendor_data'),
#                ('INVENTORY.sql', 'item_notes'),
#                ('INVENTORY.sql', 'item_sales_links'),
#                ('INVENTORY.sql', 'item_cust_instructions'),
#                ('INVENTORY.sql', 'item_history'),
#                ('TRANSACTIONS.sql', 'transactions'),
#                ('TRANSACTIONS.sql', 'transaction_payments'),
#                ('TRANSACTIONS.sql', 'transaction_notes'),
#                ('CONFIG.sql', 'basic_store_info'),
#                ('CONFIG.sql', 'pos_controls'),
#                ('CONFIG.sql', 'pos_messages'),
#                ('CONFIG.sql', 'store_closing_options'),
#                ('CONFIG.sql', 'payment_methods'),
#                ('CONFIG.sql', 'tax_tables'),
#                ('CONFIG.sql', 'passwords'),
#                ('CONFIG.sql', 'misc_options'),
#                ('CONFIG.sql', 'employees'),
#                ('CONFIG.sql', 'discount_class'),
#                ('CONFIG.sql', 'item_margin'),
#                ('CONFIG.sql', 'discount_options'),
#                ('CONFIG.sql', 'themes')]


# for sqlfile, tableName in do_list:
#     query = 'SELECT COUNT(*) FROM tableSupport WHERE sql_file=(?) AND table_names=(?)'
#     data = (sqlfile, tableName)
#     cnt_returnd = HU.SQConnect(query, data, sql_file).ONE()
#     cnt = HU.DeTupler(cnt_returnd)
#     if cnt == 0:
#         query = 'INSERT INTO tableSupport (sql_file, table_names) VALUES (?,?)'
#         data = (sqlfile, tableName)
#         HU.SQConnect(query, data, sql_file).ONE()
        
