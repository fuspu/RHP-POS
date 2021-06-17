
#!/usr/bin/env python
#-*- coding: utf-8 -*-

#
#
#
#import wxversion
#wxversion.select('2.8')

#import sqlite3
import handy_utils as HUD
import datetime
import pout
from db_related import TableAware, SQConnect, Tabling

################## Support Table ####################################
sql_file = '../db/SUPPORT.sql'
table_name = 'tableSupport'
cols = 'sql_file TEXT, table_name TEXT'
a = Tabling(table_name, cols, sql_file)
a.CreateTable()
a.AddSupport(table_name, sql_file)

################## Customer Related Tables ##########################
# Customer Codes
#################
sql_file = '../db/CUSTOMERS.sql'
table_name = 'customer_codes'
col_list = 'customer_code TEXT'
a = Tabling(table_name, col_list, sql_file)
a.CreateTable()

testcol = 'customer_code'
testdata = 'GOOD'
a.InsertTestData('customer_code', 'GOOD')
a.InsertTestData('customer_code', 'SPICY')
a.InsertTestData('customer_code', 'HOSTILE')


table_name = 'customer_basic_info'
cols_list = '''cust_num text primary key,
               first_name text,
               last_name text,
               middle_initial text,
               suffix text,
               prefix text,
               address_acct_num text,
               phone_numbers text,
               email_addr text,
               tax_exempt_number text,
               typecode text,
               rental_of text,
               statement_terms text,
               contact1 text,
               contact2 text,
               account_type text,
               alt_post_acct text,
               date_added text,
               last_maintained text,
               last_sale text,
               last_layaway text,
               birthday text,
               charge_priviledge_expiry, integer,
               full_name text'''
a = Tabling(table_name, cols_list, sql_file)       
a.CreateTable()

col_list = 'cust_num, first_name, last_name, date_added'
ah = datetime.date.today().strftime('%Y-%m-%d')
data_list = f"Test1, Alvin, Acres, {ah}"
a.InsertTestData(col_list, data_list)

# # Address Accounts

table_name = 'address_accounts'
cols_list = '''addr_acct_num text,
               street_num text,
               street_direction text,
               street_name text,
               street_type text,
               unit text,
               address0 text,
               address2 text,
               address3 text,
               city text,
               state text,
               zipcode text,
               transactions text'''
a = Tabling(table_name, cols_list, sql_file)

# # Customer Sales Options
table_name = 'customer_sales_options'
cols_list = '''cust_num char
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('cust_num', char=20, primary_key=True)
# a.AddField('tax_exempt', integer=11, defaults=0)
# a.AddField('tax_direct', integer=11, defaults=0)
# a.AddField('no_checks', integer=11, defaults=0)
# a.AddField('pos_clerk_message', text='')
# a.AddField('salesperson', char=12)
# a.AddField('no_discount', integer=11, defaults=1)
# a.AddField('fixed_discount', integer=11, defaults=0)
# a.AddField('discount_amt', decimal=(4,2), defaults=00.00)


# # Customer Accounts Receivables
# table_name = 'customer_accts_receivable'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('cust_num', char=20, primary_key=True)
# a.AddField('credit_limit', decimal=(10,2))
# a.AddField('freeze_charges', integer=11, defaults=1)
# a.AddField('late_charge_exempt', integer=11, defaults=0)
# a.AddField('print_invoice_detail_on_statement', integer=11, defaults=0)
# a.AddField('last_statement_date', date='')
# a.AddField('last_paid_date', date='')
# a.AddField('last_paid_amt', decimal=(12,2), defaults=0.00)
# a.AddField('partial_cash', decimal=(12,2), defaults=0.00)


# # Customer Ship To Info
# table_name = 'customer_shipto_info'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('cust_num', char=20, primary_key=True)
# a.AddField('name', char=160)
# a.AddField('phone', char=30)
# a.AddField('ship_by', char=12)
# a.AddField('address_acct_num', char=90)
# a.AddField('comments', text='')


# # Customer Notes
# table_name = 'customer_notes'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('cust_num', char=20, primary_key=True)
# a.AddField('notes', text='')


# # Customer Security Photos & Facial Recognition
# table_name = 'customer_security'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('cust_num', char=20, primary_key=True)
# a.AddField('security_loc', text='')

# # JSON security_loc = {[key] : '/path/to/images/'}

# # Customer Penalty & Info
# table_name = 'customer_penalty_info'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('cust_num', char=20, primary_key=True)
# a.AddField('date_added', date='')
# a.AddField('unpaid_invoice', integer=11)
# a.AddField('last_unpaid_date', date='')
# a.AddField('last_avail_credit', decimal=(20,2))
# a.AddField('score', char=20)

                  
# ############### Accounting Related Tables ###################
# sql_file = '../db/ACCOUNTING.sql'

# # General Ledger
# table_name = 'general_ledger'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('transaction_num', integer=11, primary_key=True)
# a.AddField('post_acct', char=10)
# a.AddField('debit', decimal=(15,2))
# a.AddField('credit', decimal=(15,2))
# a.AddField('date', date='')
# a.AddField('memo', char=90)
# a.AddField('account_desc', char=90)


# # Accounts
# table_name = 'ledger_post_accounts'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('account_major', char=5)
# a.AddField('account_minor', char=5)
# a.AddField('account_name', char=30)

# #print('Table Aware : {}'.format(a))
# returnd = a.CheckEntries()
# #returnd = CheckEntries(sql_file, table_name)
# #print('Ledger Post Accounts : {0}'.format(returnd))
# InsertInto = 'INSERT INTO ledger_post_accounts values '
# if returnd == 0:
#     do_list = [InsertInto + "('100', '010', 'Cash Disbursements');",
#                InsertInto + "('100', '010', 'Cash Receipts');",
#                InsertInto + "('100', '010', 'Credit Cards');",
#                InsertInto + "('300', '010', 'Gift Cards');",
#                InsertInto + "('000', '000', 'Food Stamps');",
#                InsertInto + "('100', '020', 'Foreign Cash 1');",
#                InsertInto + "('100', '030', 'Foreign Cash 2');",
#                InsertInto + "('100', '040', 'Foreign Cash 3');",
#                InsertInto + "('300', '020', 'Credit Book');",
#                InsertInto + "('120', '010', 'Accounts Receivable');",
#                InsertInto + "('145', '000', 'Inventory');",
#                InsertInto + "('146', '000', 'Layaway Inventory');",
#                InsertInto + "('300', '010', 'Accounts Payable');",
#                InsertInto + "('310', '010', 'Sales Tax Payable');",
#                InsertInto + "('400', '000', 'Store Sales');",
#                InsertInto + "('500', '000', 'Cost of Sales');",
#                InsertInto + "('510', '000', 'Inventory Adjustment');",
#                InsertInto + "('520', '010', 'A/R Adjustments');",
#                InsertInto + "('400', '020', 'Late Charge Income');",
#                InsertInto + "('399', '010', 'Retained Earnings');",
#                InsertInto + "('350', '010', 'Layaway Liability');",
#                InsertInto + "('110', '020', 'Late Charge Receivable');",
#                InsertInto + "('110', '020', 'Transfer Receivable');",
#                InsertInto + "('300', '020', 'Transfer Payable');",
#                InsertInto + "('300', '020', 'A/P Paid w/ Credit Card');"]

#     data = ''
#     for query in do_list:
#         SQConnect(query, data, sql_file).ONE()

# #Paidout
# table_name = 'paidout_routing'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('account_major', char=5)
# a.AddField('account_minor', char=5)
# a.AddField('account_name', char=30)


# returnd = a.CheckEntries()
# InsertInto = 'INSERT INTO paidout_routing values '
# if returnd == 0:
#     do_list = [InsertInto + "('710', '020', 'GAS VAN');",
#                InsertInto + "('720', '050', 'POSTAGE');",
#                InsertInto + "('385', '010', 'DRAW');",
#                InsertInto + "('710', '030', 'VEHICLE REPAIRS');",
#                InsertInto + "('620', '010', 'CASUAL LABOR');",
#                InsertInto + "('145', '010', 'INVENTORY');"]

#     data = ''
#     for query in do_list:
#         SQConnect(query, data, sql_file).ONE()

# ################ Vendor Related Tables #######################
# sql_file = '../db/VENDORS.sql'

# #Vendor Basic Info
# table_name = 'vendor_basic_info'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('vend_num', char=20, primary_key=True)
# a.AddField('name', char=60)
# a.AddField('address1', char=60)
# a.AddField('address2', char=60)
# a.AddField('city', char=30)
# a.AddField('state', char=3)
# a.AddField('zip', char=15)
# a.AddField('acct_num', text='')
# a.AddField('post_acct', char=12)
# a.AddField('phone', char=30)
# a.AddField('fax', char=30)
# a.AddField('email', char=50)
# a.AddField('terms_days', integer=11, defaults=10)
# a.AddField('discount_percent', decimal=(3,1), defaults=0.0)
# a.AddField('contact', text='')

# returnd = a.CheckEntries()
# a.CreateTestItem('vend_num, name', "'0', 'Test Account'")


# # Vendor Invoices
# table_name = 'vendor_invoices'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('vend_num', char=20)
# a.AddField('acct_num', varchar=45)
# a.AddField('date', date='')
# a.AddField('amount', decimal=(10,2))
# a.AddField('post_date', char=8)
# a.AddField('terms_days', integer=11, defaults=0)
# a.AddField('discount_percent', decimal=(3,1), defaults=00.0)
# a.AddField('invoice_num', char=45)
# a.AddField('post_acct', text='')
# a.AddField('disc_ok', integer=11, defaults=0)
# a.AddField('pay_after', date='')
# a.AddField('date_paid', date='')
# a.AddField('checknum', integer=11)
# a.AddField('payment_type', char=12)
# a.AddField('banknum', integer=11)
# a.AddField('cleared', integer=11, defaults=0)
# a.AddField('paid_in_full', bool=True,  defaults=0)


# # Vendor Invoice Distributions Data
# # JSON'd
# # partials = {parts : {
# #                      active : active_amt,
# #                      post_acct : 100-001,
# #                      partialAmt : 0.00,
# #                      discOK : T or F,
# #                      discAmt : 0.00,
# #                     }
# #             }
# table_name = 'vendor_invoice_dist_partials'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('vend_num', char=20)
# a.AddField('acct_num', char=45)
# a.AddField('invoice_num', char=45)
# a.AddField('parts', text='')


# # Vendor Invoice PayAllocation Data
# # JSON'd
# # partials = {parts : {
# #                      active : True or False,
# #                      pay_after : date,
# #                      pay_amt : 0.00,
# #                      date_paid : date,
# #                      check_num : 0.00
# #                      }
# #             }

# table_name = 'vendor_invoice_partials'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('vend_num', char=20)
# a.AddField('acct_num', char=45)
# a.AddField('invoice_num', char=45)
# a.AddField('parts', text='')


# # Vendor Notes
# table_name = 'vendor_notes'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('vend_num', char=20, primary_key=True)
# a.AddField('notes', text='')


# ######################## Support Tables ####################
# sql_file = '../db/SUPPORT.sql'


# # Organizations
# table_name = 'organizations'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('abuser', char=10, primary_key=True)
# a.AddField('department', char=30)
# a.AddField('category', char=30)
# a.AddField('subcategory', char=30)
# a.AddField('location', char=30)
# a.AddField('unittype', char=30)
# a.AddField('num_of_aisles', char=11, defaults='0')
# a.AddField('extra_places', char=30)
# a.AddField('num_of_sections', char=11, defaults='0')
# a.AddField('customer_codes', char=30)
# a.AddField('account_types', char=30)


# returnd = HUD.QueryOps().CheckEntryExist('abuser','rhp',[table_name])

# a.CreateTestItem('abuser, department, category, subcategory',"'rhp', 'Hardware','Tools','Wrenches'")

# # # Listing of Departments for Items
# # table_name = 'department_list'
# # column_info = [('department', 'text')

# # a = TableAware(sql_file, table_name, column_info)
# # a.Run()
# # #CreateTable(sql_file, table_name, column_info)


# # # Listing of Categories for Items
# # table_name = 'category_list'
# # column_info = [('category', 'text')

# # a = TableAware(sql_file, table_name, column_info)
# # a.Run()
# # #CreateTable(sql_file, table_name, column_info)


# # # Listing of SubCategory for Items
# # table_name = 'subcategory_list'
# # column_info = '(subcategory text='')'

# # a = TableAware(sql_file, table_name, column_info)
# # a.Run()
# # #CreateTable(sql_file, table_name, column_info)


# # # Listing of Location/Materials for Items
# # table_name = 'location_list'
# # column_info = '(location text='')'

# # a = TableAware(sql_file, table_name, column_info)
# # a.Run()
# # #CreateTable(sql_file, table_name, column_info)


# # # Listing of Unit Types
# # table_name = 'unittype_list'
# # column_info = '(unittype char(5))'

# # a = TableAware(sql_file, table_name, column_info)
# # a.Run()
# # #CreateTable(sql_file, table_name, column_info)


# # Listing of Shipping Methods
# table_name = 'shipping_methods'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('method', char=50)


# # Listing of Account Types
# table_name = 'account_types'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('account_type', char=90)


# ############### Item Related Tables #########################
# sql_file = '../db/INVENTORY.sql'

# #item retails table
# table_name = 'item_retails'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('upc', char=90, primary_key=True)
# a.AddField('standard_unit', integer=11, defaults=1)
# a.AddField('standard_price', decimal=(10,2), defaults=0.00)
# a.AddField('level_a_unit', integer=11, defaults=1)
# a.AddField('level_a_price', decimal=(10,2), defaults=0.00)
# a.AddField('level_b_unit', integer=11, defaults=1)
# a.AddField('level_b_price', decimal=(10,2), defaults=0.00)
# a.AddField('level_c_unit', integer=11, defaults=1)
# a.AddField('level_c_price', decimal=(10,2), defaults=0.00)
# a.AddField('level_d_unit', integer=11, defaults=1)
# a.AddField('level_d_price', decimal=(10,2), defaults=0.00)
# a.AddField('level_e_unit', integer=11, defaults=1)
# a.AddField('level_e_price', decimal=(10,2), defaults=0.00)
# a.AddField('level_f_unit', integer=11, defaults=1)
# a.AddField('level_f_price', decimal=(10,2), defaults=0.00)
# a.AddField('level_g_unit', integer=11, defaults=1)
# a.AddField('level_g_price', decimal=(10,2), defaults=0.00)
# a.AddField('level_h_unit', integer=11, defaults=1)
# a.AddField('level_h_price', decimal=(10,2), defaults=0.00)
# a.AddField('level_i_unit', integer=11, defaults=1)
# a.AddField('level_i_price', decimal=(10,2), defaults=0.00)
# a.AddField('compare_unit', integer=11, defaults=1)
# a.AddField('compare_price', decimal=(10,2), defaults=0.00)
# a.AddField('on_sale_unit', integer=11, defaults=1)
# a.AddField('on_sale_price', decimal=(10,2), defaults=0.00)

                  
# # Item Detailed table
# #   JSON'd Vendors
# #   vendors = { '1' = 
# #                   id : 0-9A-Z
# #                   ordernum : ordernum
# #                   last_cost : 0.00
# #                   lead_time : 0 in days
# #             }
# #
# table_name = 'item_detailed'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('upc', char=90, primary_key=True)
# a.AddField('description', char=150)
# a.AddField('avg_cost', decimal=(10,3), defaults=0.000)
# a.AddField('last_cost', decimal=(10,3), defaults=0.000)
# a.AddField('size_A', char=30)
# a.AddField('size_B', char=30)
# a.AddField('altlookup', text='')
# a.AddField('quantity_on_hand', decimal=(12,3), defaults=0.000)
# a.AddField('quantity_committed', decimal=(12,3), defaults=0.000)
# a.AddField('quantity_on_layaway', decimal=(12,3), defaults=0.000)
# a.AddField('part_num', char=90)
# a.AddField('oempart_num', char=90)
# a.AddField('kit_num', char=90)
# a.AddField('kit_pieces', integer=11, defaults=1)
# a.AddField('vendor1', text='')
# a.AddField('vendor2', text='')
# a.AddField('vendor3', text='')
# a.AddField('vendor4', text='')
# a.AddField('vendor5', text='')
# a.AddField('vendor6', text='')

# a.CreateTestItem('upc, description',"'0', 'Test Item'")


# # Closeouts
# table_name = 'closeouts'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('upc', char=90, primary_key=True)
# a.AddField('avg_cost', decimal=(10,3), defaults=0.000)
# a.AddField('last_retail', decimal=(10,3), defaults=0.000)
# a.AddField('closeout_date', date='')
                

# #Alt Lookups
# table_name = 'altlookups'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('upc', char=90, primary_key=True)
# a.AddField('altlookup', text='')
                  
                  
# # Flexible Retail Program
# table_name = 'flexible_update'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('upc', char=90, primary_key=True)
# a.AddField('avg_cost', decimal=(10,3), defaults=0.000)
# a.AddField('max_margin', decimal=(10,3), defaults=0.000)
# a.AddField('last_update', date='')


# # Tax Holiday Table
# table_name = 'tax_holiday'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('id', integer=11)
# a.AddField('name', char=90)
# a.AddField('begin_date', date='')
# a.AddField('end_date', date='')
# a.AddField('upc', text='')
# a.AddField('active', bool=True)



# for i in range(1,7):
#     a.CreateTestItem('id',"'{}'".format(i)) 

# # Item Detailed2 table
# table_name = 'item_detailed2'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('upc', char=90, primary_key=True)
# a.AddField('do_not_discount', integer=11, defaults=0)
# a.AddField('lock_prices', integer=11, defaults=0)
# a.AddField('tax1', integer=11, defaults=0)
# a.AddField('tax2', integer=11, defaults=0)
# a.AddField('tax3', integer=11, defaults=0)
# a.AddField('tax4', integer=11, defaults=0)
# a.AddField('tax_never', integer=11, defaults=0)
# a.AddField('override_tax_rate', decimal=(5,4), defaults=0.0000)
# a.AddField('sale_begin', date='')
# a.AddField('sale_end', date='')
# a.AddField('sale_begin_time', time='')
# a.AddField('sale_end_time', time='')
# a.AddField('buyX', integer=11, defaults=0)
# a.AddField('getY', integer=11, defaults=0)
# a.AddField('credit_book_exempt', integer=11, defaults=0)
# a.AddField('delete_when_out', integer=11, defaults=0)
# a.AddField('case_break_num', char=90)
# a.AddField('substituteYN', integer=11, defaults=0)
# a.AddField('substitute_num', char=90)
# a.AddField('location', char=45)
# a.AddField('weight', decimal=(6,3), defaults=0.000)
# a.AddField('tare_weight', decimal=(6,3), defaults=0.000)
# a.AddField('image_loc', char=250)
# a.AddField('last_saledate', date='')
# a.AddField('last_returndate', date='')
# a.AddField('maintdate', date='')
# a.AddField('added_date', date='')
# a.AddField('override_commission', integer=11, defaults=0)
# a.AddField('over_commission', decimal=(6,4), defaults=0.0000)
# a.AddField('over_fixd_comm', decimal=(6,2), defaults=0.00)
# a.AddField('priceschema', char=2)
# a.AddField('orderctrl', text='')

# a.CreateTestItem('upc', "'0'")


# # Consignment Options - Consignment Page Options 
# table_name = 'consignments'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('upc', char=90, primary_key=True)
# a.AddField('vendor_num', char=90)
# a.AddField('override_fee', decimal=(6,3))


# # Item Options - info you gotta know to make sense of other things
# table_name = 'item_options'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('upc', char=90, primary_key=True)
# a.AddField('num_of_vendors', integer=11, defaults=0)
# a.AddField('department', char=15)
# a.AddField('category', char=15)
# a.AddField('subcategory', char=15)
# a.AddField('location', char=15)
# a.AddField('postacct', char=12)
# a.AddField('unit_type', char=10)
# a.AddField('item_type', char=15)
# a.AddField('agepopup', integer=11, defaults=0)
# a.AddField('posoptions', text='')
# a.AddField('consignment', integer=11, defaults=0)
# a.AddField('unitsinpackage', integer=11, defaults=1)
# a.AddField('foodstampexempt', integer=11, defaults=1)
# a.AddField('loyaltyexempt', integer=11, defaults=0)
# a.AddField('deactivated', integer=11, defaults=0)
# a.AddField('aisle_num', char=3)
# a.AddField('extra_places', char=30)
# a.AddField('section_num', char=15)
# a.AddField('closeout', bool=True,  defaults=0)

# a.CreateTestItem('upc', "'0'")

# # POSoptions via JSON
# #   Prompt for Quantity = Y/N
# #   Assume 1 Sold = Y/N
# #   Prompt for Price, Quantity Calculated = Y/N
# #   Prompt for scale = Y/N


# # Item Pricing Schemes table
# table_name = 'item_pricing_schemes'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('name', char=10, primary_key=True)
# a.AddField('scheme_list', text='')
# a.AddField('reduce_by', char=90, defaults="3")

# a.CreateTestItem('name, scheme_list, reduce_by', "'1-3-10','1-3-10', 2.50")

                  
# # Item Vendor Data
# table_name = 'item_vendor_data'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('upc', char=90, primary_key=True)
# a.AddField('vendor1_num', text='')
# a.AddField('vendor2_num', text='')
# a.AddField('vendor3_num', text='')
# a.AddField('vendor4_num', text='')
# a.AddField('vendor5_num', text='')
# a.AddField('vendor6_num', text='')

# # JSON in each field
# #
# #   - ordernum
# #   - prev_ordernum
# #   - lead_time
# #   - minimum_order
# #   - last_order
# #   - last_order_date
# #   - last_rec
# #   - last_rec_date
# #   - outstanding
# #   - units_in_order

# # Item Notes
# table_name = 'item_notes'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('upc', char=90, primary_key=True)
# a.AddField('notes', text='')

# a.CreateTestItem('upc', "'0'")

# # Item POS Sales Links
# table_name = 'item_sales_links'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('upc', char=90, primary_key=True)
# a.AddField('sales_links', text='')

# a.CreateTestItem('upc', "'0'")
# #JSON
# #   - item(#) infinite number of sales links associated with item
# #   - message


# # Item Customer Instructions
# table_name = 'item_cust_instructions'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('upc', char=90, primary_key=True)
# a.AddField('print_info_options', integer=11)
# a.AddField('print_return_options', integer=11)
# a.AddField('print_warranty_options', integer=11)
# a.AddField('info_dialog', char=45)
# a.AddField('return_dialog', char=45)
# a.AddField('warranty_dialog', char=45)
# a.AddField('info_box', text='')
# a.AddField('return_box', text='')
# a.AddField('warranty_box', text='')

# a.CreateTestItem('upc', "'0'")


# # Item History
# table_name = 'item_history'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('upc', char=90, primary_key=True)
# a.AddField('year', integer=11)
# a.AddField('January', decimal=(20,3))
# a.AddField('February', decimal=(20,3))
# a.AddField('March', decimal=(20,3))
# a.AddField('April', decimal=(20,3))
# a.AddField('May', decimal=(20,3))
# a.AddField('June', decimal=(20,3))
# a.AddField('July', decimal=(20,3))
# a.AddField('August', decimal=(20,3))
# a.AddField('September', decimal=(20,3))
# a.AddField('October', decimal=(20,3))
# a.AddField('November', decimal=(20,3))
# a.AddField('December', decimal=(20,3))

# a.CreateTestItem('upc', "'0'")


# ############# Transaction Related Tables #####################
# sql_file = '../db/TRANSACTIONS.sql'

# # Transaction Ctrl Number
# table_name = 'transaction_control'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('abuser', char=10, primary_key=True)
# a.AddField('trans_num', integer=11)

# a.CreateTestItem('abuser, trans_num', "'rhp', 1")
    

# # Transactions
# table_name = 'transactions'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('transaction_id', char=15)
# a.AddField('date', date='')
# a.AddField('salesperson', integer=11)
# a.AddField('time', time='')
# a.AddField('cust_num', char=30)
# a.AddField('address_acct_num', char=90)
# a.AddField('upc', char=90)
# a.AddField('description', char=120)
# a.AddField('quantity', decimal=(20,3))
# a.AddField('avg_cost', decimal=(20,3))
# a.AddField('unit_price', decimal=(20,2))
# a.AddField('total_price', decimal=(20,2))
# a.AddField('pricetree', text='')
# a.AddField('discount', varchar=20)
# a.AddField('type_of_transaction', char=15)
# a.AddField('tax1', integer=11, defaults=0)
# a.AddField('tax2', integer=11, defaults=0)
# a.AddField('tax3', integer=11, defaults=0)
# a.AddField('tax4', integer=11, defaults=0)
# a.AddField('tax_never', integer=11, defaults=0)
# a.AddField('tax_exempt', bool=True,  defaults=0)
# a.AddField('po_number', char=120)


# fieldnames = '''transaction_id, date, salesperson, time, cust_num, address_acct_num, 
# upc, description, quantity, avg_cost, unit_price, total_price, pricetree, discount, type_of_transaction,
# tax1, tax2, tax3, tax4, tax_never, tax_exempt, po_number'''
# values = """'00000000', '20201016', '1', '10:10:00', '37047734', '', 
# 'BEEFSTICK', 'Jack Links BeefStick',3, 0.65, 0.99, 2.97,'',0, 'SALE',
# 1, 1, 1, 1, 1, 1, ''"""
# a.CreateTestItem(fieldnames, values)

    
# #CreateTable(sql_file, table_name, column_info)
# # per item entry per row, no primary_key=True

# #Transaction Payments
# table_name = 'transaction_payments'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('transaction_id', char=15, primary_key=True)
# a.AddField('paid', decimal=(20,2), defaults=0.00)
# a.AddField('discount_taken', decimal=(20,2), defaults=0.00)
# a.AddField('subtotal_price', decimal=(20,2), defaults=0.00)
# a.AddField('tax', decimal=(20,2), defaults=0.00)
# a.AddField('total_price', decimal=(20,2), defaults=0.00)
# a.AddField('paid_date', date='')
# a.AddField('date', date='')
# a.AddField('time', time='')
# a.AddField('cust_num', char=30)
# a.AddField('address_acct_num', char=90)
# a.AddField('pay_method', char=15)
# a.AddField('change_back', decimal=(20,2))
# a.AddField('type_of_transaction', char=15)
# a.AddField('cash_payment', decimal=(20,2))
# a.AddField('check_payment', decimal=(20,2))
# a.AddField('check_num', char=30)
# a.AddField('dl_number', char=90)
# a.AddField('phone_num', char=15)
# a.AddField('dob', char=12)
# a.AddField('charge', decimal=(20,2), defaults=0.00)
# a.AddField('card1_payment', decimal=(20,2), defaults=0.00)
# a.AddField('auth1_num', char=60)
# a.AddField('card1_type', char=60)
# a.AddField('card1_numbers', char=36)
# a.AddField('card2_payment', decimal=(20,2), defaults=0.00)
# a.AddField('auth2_num', char=60)
# a.AddField('card2_numbers', char=36)
# a.AddField('card2_type', char=60)
# a.AddField('card3_payment', decimal=(20,2), defaults=0.00)
# a.AddField('auth3_num', char=60)
# a.AddField('card3_numbers', char=36)
# a.AddField('card3_type', char=60)
# a.AddField('card4_payment', decimal=(20,2), defaults=0.00)
# a.AddField('auth4_num', char=60)
# a.AddField('card4_numbers', char=36)
# a.AddField('card4_type', char=60)
# a.AddField('card5_payment', decimal=(20,2), defaults=0.00)
# a.AddField('auth5_num', char=60)
# a.AddField('card5_numbers', char=36)
# a.AddField('card5_type', char=60)
# a.AddField('debit_payment', decimal=(20,2), defaults=0.00)
# a.AddField('auth6_num', char=60)
# a.AddField('debit_numbers', char=36)
# a.AddField('debit_type', char=60)


# #Transaction Notes
# table_name = 'transaction_notes'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('station_num', char=3)
# a.AddField('transaction_id', char=15)
# a.AddField('line_position', char=15)
# a.AddField('note', text='')            

    
# ############## General Operations Related Tables ##############
# sql_file = '../db/CONFIG.sql'

# # Store info
# table_name = 'basic_store_info'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('store_num', integer=11, primary_key=True)
# a.AddField('name', char=90)
# a.AddField('address1', char=90)
# a.AddField('address2', char=90)
# a.AddField('city', char=30)
# a.AddField('state', char=3)
# a.AddField('zip', char=15)
# a.AddField('phone1', char=30)
# a.AddField('phone2', char=30)
# a.AddField('fax', char=30)
# a.AddField('email', char=150)
# a.AddField('print_on_forms', integer=11, defaults=0)
# a.AddField('late_charge', decimal=(3,2))
# a.AddField('cust_id_title', char=50)
# a.AddField('penny_tally', decimal=(12,2))
# a.AddField('website', text='')
# a.AddField('logo', text='')

# a.CreateTestItem("store_num, name, address1, city, state, zip","0,'ABC Hardware','111 Hill St','Ipsum City','OH','45632'")

# # POS Controls
# table_name = 'pos_controls'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('print_receipt_ondemand', integer=11, defaults=0)
# a.AddField('prompt_for_qty', integer=11, defaults=0)
# a.AddField('add_cust', integer=11, defaults=0)
# a.AddField('add_items', integer=11, defaults=0)
# a.AddField('payment_on_acct', integer=11, defaults=0)
# a.AddField('verify_assigned_discounts', integer=11, defaults=0)
# a.AddField('report_out_of_stock', integer=11, defaults=0)
# a.AddField('disable_credit_security', integer=11, defaults=0)
# a.AddField('print_signature_line', integer=11, defaults=0)
# a.AddField('skip_finished_question', integer=11, defaults=0)
# a.AddField('print_item_count', integer=11, defaults=0)
# a.AddField('track_salesperson', integer=11, defaults=0)
# a.AddField('mailing_list_capture', integer=11, defaults=0)
# a.AddField('disable_open_drawer', integer=11, defaults=0)
# a.AddField('dept_totals_by_drawer', integer=11, defaults=0)
# a.AddField('omit_cust_addr', integer=11, defaults=0)
# a.AddField('print_totals_on_logoff', integer=11, defaults=0)
# a.AddField('save_cleared_totals_to_reconcile', integer=11, defaults=0)
# a.AddField('verify_parts_explosion', integer=11, defaults=0)
# a.AddField('display_parts_explosion', integer=11, defaults=0)
# a.AddField('print_kit_parts', integer=11, defaults=0)
# a.AddField('print_kit_parts_price', integer=11, defaults=0)
# a.AddField('discount_omit_price', integer=11, defaults=0)
# a.AddField('trap_zips', integer=11, defaults=0)
# a.AddField('prompt_for_cost', integer=11, defaults=0)
# a.AddField('print_item_num', integer=11, defaults=0)
# a.AddField('support_eos_discount', integer=11, defaults=0)
# a.AddField('no_alt_tax', integer=11, defaults=0)
# a.AddField('notify_if_cost_gt_price', integer=11, defaults=0)
# a.AddField('omit_you_saved_line', integer=11, defaults=0)
# a.AddField('offer_on_hold_options', integer=11, defaults=0)
# a.AddField('print_void_trans', integer=11, defaults=0)
# a.AddField('exclude_layaways', integer=11, defaults=0)
# a.AddField('exclude_orders', integer=11, defaults=0)
# a.AddField('exclude_quotes', integer=11, defaults=0)
# a.AddField('exclude_hold', integer=11, defaults=0)


# # POS Messages
# table_name = 'pos_messages'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('abuser', char=10, primary_key=True)
# a.AddField('conditions', text='')
# a.AddField('return_policy', text='')
# a.AddField('warranty', text='')
# a.AddField('charge_agreement', text='')
# a.AddField('credit_card_agreement', text='')
# a.AddField('thanks', text='')
# a.AddField('check_policy', text='')
# a.AddField('layaway_policy', text='')
# a.AddField('gift_loyalty', text='')
# a.AddField('special_event', text='')

# return_policy='30 Day Return, Package unopened, item unused'
# charge_agree='You agree to pay in full every month before the 30th'
# cc_agree='The way of the future, Hooray for a cashless society'
# thanks='Thank you for your business'
# check_policy='Nope, no thanks, never, NO CHECKS!!!!'
# a.CreateTestItem('abuser, return_policy, charge_agreement, credit_card_agreement, thanks, check_policy', f"'rhp','{return_policy}','{charge_agree}','{cc_agree}','{thanks}','{check_policy}'")


# # Store Closing Options
# table_name = 'store_closing_options'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('combined_trans_detail', integer=11, defaults=0)
# a.AddField('trans_by_pay_type', integer=11, defaults=0)
# a.AddField('trans_by_salesperson', integer=11, defaults=0)
# a.AddField('trans_by_drawer', integer=11, defaults=0)
# a.AddField('tax_audit_report', integer=11, defaults=0)
# a.AddField('item_sales_by_deptcat', integer=11, defaults=0)
# a.AddField('deptcat_option', integer=11, defaults=0)
# a.AddField('exit_after_closing', integer=11, defaults=0)
# a.AddField('do_not_print_hardcopy', integer=11, defaults=0)


# table_name = 'reports_closing_daily'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('abuser', char=10, primary_key=True)
# a.AddField('all_transactions', bool=True,  defaults=1)
# a.AddField('cash_drawer_totals', bool=True,  defaults=1)
# a.AddField('customer_invoiced', bool=True,  defaults=0)

# a.CreateTestItem('abuser', "'rhp'")


# table_name = 'reports_closing_weekly'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('abuser', char=10, primary_key=True)
# a.AddField('sales_breakdown', bool=True,  defaults=1)
# a.AddField('inventory_top10', bool=True,  defaults=1)
# a.AddField('inventory_losers10', bool=True,  defaults=1)
# a.AddField('inventory_most_requested', bool=True,  defaults=1)                  


# a.CreateTestItem('abuser', "'rhp'")

# #
# # table_name = 'reports_closing_monthly'
# # a = TableAware(table_name, sql_file, dbtype='sqlite3')
# # a.AddField('abuser', char=10, primary_key=True)
# # a.AddField('sales_breakdown', bool=True,  defaults=1)
# # a.AddField('inventory_top50', bool=True,  defaults=1)
# # a.AddField('inventory_losers50', bool=True,  defaults=1)
# # a.AddField('inventory_most_requested', bool=True,  defaults=1)
# # a.AddField('tax_report', bool=True,  defaults=1)

# # a.CreateTestItem('abuser', "'rhp'")

# #
# table_name = 'reports_closing_quarterly'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('abuser', char=10, primary_key=True)
# a.AddField('sales_breakdown', bool=True,  defaults=1)
# a.AddField('inventory_top100', bool=True,  defaults=1)
# a.AddField('inventory_losers100', bool=True,  defaults=1)

# a.CreateTestItem('abuser', "'rhp'")

# #
# table_name = 'reports_closing_yearly'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('abuser', char=10, primary_key=True)
# a.AddField('sales_breakdown', bool=True,  defaults=1)
# a.AddField('inventory_top250', bool=True,  defaults=1)
# a.AddField('inventory_losers250', bool=True,  defaults=1)

# a.CreateTestItem('abuser', "'rhp'")

# #
# #Payment Methods
# table_name = 'payment_methods'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('cash', integer=11, defaults=0)
# a.AddField('checks', integer=11, defaults=0)
# a.AddField('house_charges', integer=11, defaults=0)
# a.AddField('credit_cards', integer=11, defaults=0)
# a.AddField('credit_book', integer=11, defaults=0)
# a.AddField('food_stamps', integer=11, defaults=0)
# a.AddField('foreign_cash', integer=11, defaults=0)
# a.AddField('loyalty_card', integer=11, defaults=0)
# a.AddField('check_setup_def_state', char=20)
# a.AddField('check_setup_def_guarrantor', char=20)


# table_name = 'tax_tables'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('tax_name', char=20, primary_key=True)
# a.AddField('GLsub', integer=11, defaults=000)
# a.AddField('RNDscheme', integer=11, defaults=0)
# a.AddField('APscheme', integer=11, defaults=0)
# a.AddField('no_pennies_rounding', integer=11, defaults=0)
# a.AddField('min_sale', decimal=(5,2), defaults=0.00)
# a.AddField('max_sale', decimal=(5,2), defaults=0.00)
# a.AddField('item_max', decimal=(5,2), defaults=0.00)
# a.AddField('from_amt0', decimal=(5,2), defaults=0.00)
# a.AddField('tax_rate0', decimal=(6,5), defaults=0.00000)
# a.AddField('from_amt1', decimal=(5,2), defaults=0.00)
# a.AddField('tax_rate1', decimal=(6,5), defaults=0.00000)
# a.AddField('from_amt2', decimal=(5,2), defaults=0.00)
# a.AddField('tax_rate2', decimal=(6,5), defaults=0.00000)



# # Passwords
# table_name = 'passwords'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('abuser', char=15, primary_key=True, defaults="'rhp'")
# a.AddField('admin_key', char=15)
# a.AddField('manager_key', char=15)
# a.AddField('clerk_key', char=15)
# a.AddField('acctreceivable', char=15)
# a.AddField('inventoryctrl', char=15)
# a.AddField('acctpayable', char=15)
# a.AddField('financials', char=15)
# a.AddField('employees', char=15)
# a.AddField('store_controls_maint', char=15)
# a.AddField('profit_pic', char=15)
# a.AddField('close_the_store', char=15)
# a.AddField('cash_drawer_display', char=15)
# a.AddField('restrict_data_access', char=15)
# a.AddField('exceed_credit', char=15)
# a.AddField('tools_menu', char=15)
# a.AddField('req_drawer_access', integer=11, defaults=0)
# a.AddField('req_cash_check', integer=11, defaults=0)
# a.AddField('req_cancel_trans', integer=11, defaults=0)
# a.AddField('req_coupons', integer=11, defaults=0)
# a.AddField('req_giftcard_override', integer=11, defaults=0)

# a.CreateTestItem('abuser, admin_key, manager_key, clerk_key', "'rhp', 'rhp', 'god', '123'")


# #Closeouts Options
# table_name = 'closeout_options'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('abuser', char=90, primary_key=True)
# a.AddField('autoadd', bool=True,  defaults=0)
# a.AddField('start_age', char=11, defaults='365')
# a.AddField('discount_percent', char=11, defaults='10')
# a.AddField('max_cost_percent', char=11, defaults='90')
# a.AddField('incremental_days', char=11, defaults='30')

# a.CreateTestItem('abuser', "'rhp'")


# # Misc Options
# table_name = 'misc_options'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('inventory_price_label_on', integer=11, defaults=0)
# a.AddField('inventory_shelf_label_spool', integer=11, defaults=0)
# a.AddField('inventory_omit_label_prices', integer=11, defaults=0)
# a.AddField('ap_canadian_cheques', integer=11, defaults=0)
# #a.AddField('export_to_quickbooks', integer=11, defaults=0)


# # Themes
# table_name = 'themes'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('theme_name', char=25, primary_key=True)
# a.AddField('bg', char=50, defaults="'#ffffff'")
# a.AddField('text', char=50, defaults="'#000000'")
# a.AddField('cell', char=50, defaults="'#d6fcd7'")
# a.AddField('info', char=50, defaults="'#f8fda9'")
# a.AddField('note', char=50, defaults="'#e8f4f0'")

# a.CreateTestItem('theme_name', "'INVENTORY'")
# a.CreateTestItem('theme_name', "'CUSTOMERS'", extra=True)
# a.CreateTestItem('theme_name', "'VENDORS'", extra=True)
# a.CreateTestItem('theme_name', "'POS'", extra=True)

                
# # Employees
# table_name = 'employees'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('employee_num', char=6, primary_key=True)
# a.AddField('employee_name', char=160)
# a.AddField('date_of_birth', date='')
# a.AddField('ssn', char=15)

# a.CreateTestItem("employee_num, employee_name, date_of_birth, ssn", "'0', 'Alvin Acres', 20121222, '234422341'")

# # Discount Class
# table_name = 'discount_class'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('class_name', char=90)
# a.AddField('scheme', text='')
# # scheme in JSON = {'Department':'','Category':'',
# #    'SubCatesgory':'','Price Level':'','Percentage':''}

# # Item Margin
# table_name = 'item_margin'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('abuser', char=15, primary_key=True, defaults="'rhp'")
# a.AddField('starting_margin_control', integer=11, defaults=0)
# a.AddField('general_margin', decimal=(6,3), defaults=50.0000)
# a.AddField('by_category', text='')


# # Margin By Category
# table_name = 'margin_by_category'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('department', char=15)
# a.AddField('category', char=15)
# a.AddField('subcategory', char=15)
# a.AddField('margin', decimal=(10,3))


# #Margin by Cost                  
# table_name = 'margin_by_cost'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('label', char=15)
# a.AddField('greater_than', decimal=(10,2))
# a.AddField('less_than', decimal=(10,2))
# a.AddField('margin', decimal=(10,2))


# # Discount Options
# table_name = 'discount_options'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('name', char=45, primary_key=True)
# a.AddField('percent', decimal=(3,2), defaults=0.00)


# # Hardware Configs
# table_name = 'hardware_config'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('abuser', char=15, primary_key=True, defaults="'rhp'")
# a.AddField('vendor_id', char=15) 
# a.AddField('product_id', char=15)
# a.AddField('interface_id', char=15)
# a.AddField('input_endpoint', char=15)
# a.AddField('output_endpoint', char=15)

# # ############## Table Support ######################


# # sql_file = '../db/SUPPORT.sql'
# # table_name = 'tableSupport'
# # a = TableAware(table_name, sql_file, dbtype='sqlite3')
# # a.AddField('sql_file', text='')
# # a.AddField('table_name', text='')

# # a.CreateTestItem('sql_file, table_name','CUSTOMERS.sql, customer_codes')
# # a.CreateTestItem('sql_file, table_name','CUSTOMERS.sql, customer_basic_info', extra=True)
# # a.CreateTestItem('sql_file, table_name','CUSTOMERS.sql, address_accounts')
# # a.CreateTestItem('sql_file, table_name','CUSTOMERS.sql, customer_sales_options')
# # a.CreateTestItem('sql_file, table_name','CUSTOMERS.sql, customer_accts_receivable')
# # a.CreateTestItem('sql_file, table_name','CUSTOMERS.sql, customer_shipto_info')
# # a.CreateTestItem('sql_file, table_name','CUSTOMERS.sql', 'customer_notes'),
# #                ('CUSTOMERS.sql', 'customer_security'),
# #                ('ACCOUNTING.sql', 'general_ledger'),
# #                ('ACCOUNTING.sql', 'ledger_post_accounts'),
# #                ('ACCOUNTING.sql', 'paidout_routing'),
# #                ('VENDORS.sql', 'vendor_basic_info'),
# #                ('VENDORS.sql', 'vendor_invoices'),
# #                ('VENDORS.sql', 'vendor_notes'),
# #                ('SUPPORT.sql', 'organizations'),
# #                ('SUPPORT.sql', 'department_list'),
# #                ('SUPPORT.sql', 'category_list'),
# #                ('SUPPORT.sql', 'subcategory_list'),
# #                ('SUPPORT.sql', 'location_list'),
# #                ('SUPPORT.sql', 'unittype_list'),
# #                ('SUPPORT.sql', 'shipping_methods'),
# #                ('SUPPORT.sql', 'account_types'),
# #                ('INVENTORY.sql', 'item_detailed'),
# #                ('INVENTORY.sql', 'item_detailed2'),
# #                ('INVENTORY.sql', 'item_options'),
# #                ('INVENTORY.sql', 'item_pricing_schemes'),
# #                ('INVENTORY.sql', 'item_vendor_data'),
# #                ('INVENTORY.sql', 'item_notes'),
# #                ('INVENTORY.sql', 'item_sales_links'),
# #                ('INVENTORY.sql', 'item_cust_instructions'),
# #                ('INVENTORY.sql', 'item_history'),
# #                ('TRANSACTIONS.sql', 'transactions'),
# #                ('TRANSACTIONS.sql', 'transaction_payments'),
# #                ('TRANSACTIONS.sql', 'transaction_notes'),
# #                ('CONFIG.sql', 'basic_store_info'),
# #                ('CONFIG.sql', 'pos_controls'),
# #                ('CONFIG.sql', 'pos_messages'),
# #                ('CONFIG.sql', 'store_closing_options'),
# #                ('CONFIG.sql', 'payment_methods'),
# #                ('CONFIG.sql', 'tax_tables'),
# #                ('CONFIG.sql', 'passwords'),
# #                ('CONFIG.sql', 'misc_options'),
# #                ('CONFIG.sql', 'employees'),
# #                ('CONFIG.sql', 'discount_class'),
# #                ('CONFIG.sql', 'item_margin'),
# #                ('CONFIG.sql', 'discount_options'),
# #                ('CONFIG.sql', 'themes')]


# # for sqlfile, tableName in do_list:
# #     query = 'SELECT COUNT(*) FROM tableSupport WHERE sql_file=(?) AND table_names=(?)'
# #     data = (sqlfile, tableName)
# #     cnt_returnd = HU.SQConnect(query, data, sql_file).ONE()
# #     cnt = HU.DeTupler(cnt_returnd)
# #     if cnt == 0:
# #         query = 'INSERT INTO tableSupport (sql_file, table_names) VALUES (?,?)'
# #         data = (sqlfile, tableName)
# #         HU.SQConnect(query, data, sql_file).ONE()
        
