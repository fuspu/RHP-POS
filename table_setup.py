
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
from db_related import TableAware, SQConnect, Tabling, DBConnect

################## Support Table ####################################
sql_file = '../db/SUPPORT.sql'
table_name = 'tableSupport'
cols = 'sql_file TEXT, table_name TEXT'
a = Tabling(table_name, cols, sql_file)
a.CreateTable()


################## Customer Related Tables ##########################
# Customer Codes
#################
sql_file = '../db/CUSTOMERS.sql'
table_name = 'customer_codes'
col_list = 'customer_code TEXT'
a = Tabling(table_name, col_list, sql_file)
a.CreateTable()


returnd = a.CheckEntries()
if returnd == 0:
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
data_list = f"'Test1', 'Alvin', 'Acres', '{ah}'"
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
a.CreateTable()


# # Customer Sales Options
table_name = 'customer_sales_options'
cols_list = '''cust_num text primary key,
               tax_exempt integer default 0,
               tax_direct integer default 0,
               no_checks integer default 0,
               pos_clerk_message text,
               salesperson text,
               no_discount integer default 1,
               fixed_discount integer default 0,
               discount_amt real default 00.00
               '''
a = Tabling(table_name, cols_list, sql_file)               
a.CreateTable()


# Customer Accounts Receivables
table_name = 'customer_accts_receivable'
cols_list = '''cust_num text primary key,
               credit_limit real,
               freeze_charges integer default 1,
               late_charge_exempt integer default 0,
               print_invoice_detail_on_statement integer default 0,
               last_statement_date text,
               last_paid_date text,
               last_paid_amt real default 0.00,
               partial_cash real default 0.00'''
a = Tabling(table_name, cols_list, sql_file)
a.CreateTable()


# Customer Ship To Info
table_name = 'customer_shipto_info'
cols_list = '''cust_num text primary key,
               name text,
               phone text,
               ship_by text,
               address_acct_num text,
               comments text'''
a = Tabling(table_name, cols_list, sql_file)
a.CreateTable()


# Customer Notes
table_name = 'customer_notes'
cols_list = '''cust_num text primary key,
               notes text'''
a = Tabling(table_name, cols_list, sql_file)
a.CreateTable()


# Customer Security Photos & Facial Recognition
table_name = 'customer_security'
cols_list = '''cust_num text primary key,
               security_loc text'''
a = Tabling(table_name, cols_list, sql_file)
# JSON security_loc = {[key] : '/path/to/images/'}
a.CreateTable()

# Customer Penalty & Info
table_name = 'customer_penalty_info'
cols_list = '''cust_num text primary key,
               date_added text,
               unpaid_invoice integer,
               last_unpaid_date text,
               last_avail_date text,
               last_avail_credit real,
               score text'''
a = Tabling(table_name, cols_list, sql_file)
a.CreateTable()
                  
# ############### Accounting Related Tables ###################
sql_file = '../db/ACCOUNTING.sql'

# General Ledger
table_name = 'general_ledger'
cols_list = '''transaction_num integer primary key,
               post_acct text,
               debit real,
               credit real,
               date text,
               memo text,
               account_desc text'''
a = Tabling(table_name, cols_list, sql_file)               
a.CreateTable()

# Accounts
table_name = 'ledger_post_accounts'
cols_list = '''account_major text,
               account_minor text,
               account_name text'''
a = Tabling(table_name, cols_list, sql_file)
a.CreateTable()
do_list = ["('100', '010', 'Cash Disbursements');",
            "('100', '010', 'Cash Receipts');",
            "('100', '010', 'Credit Cards');",
            "('300', '010', 'Gift Cards');",
            "('000', '000', 'Food Stamps');",
            "('100', '020', 'Foreign Cash 1');",
            "('100', '030', 'Foreign Cash 2');",
            "('100', '040', 'Foreign Cash 3');",
            "('300', '020', 'Credit Book');",
            "('120', '010', 'Accounts Receivable');",
            "('145', '000', 'Inventory');",
            "('146', '000', 'Layaway Inventory');",
            "('300', '010', 'Accounts Payable');",
            "('310', '010', 'Sales Tax Payable');",
            "('400', '000', 'Store Sales');",
            "('500', '000', 'Cost of Sales');",
            "('510', '000', 'Inventory Adjustment');",
            "('520', '010', 'A/R Adjustments');",
            "('400', '020', 'Late Charge Income');",
            "('399', '010', 'Retained Earnings');",
            "('350', '010', 'Layaway Liability');",
            "('110', '020', 'Late Charge Receivable');",
            "('110', '020', 'Transfer Receivable');",
            "('300', '020', 'Transfer Payable');",
            "('300', '020', 'A/P Paid w/ Credit Card');"]
a.CreateTestItem('account_major, account_minor, account_name', do_list)
    
## Paidout
table_name = 'paidout_routing'
cols_list = '''account_major text,
               account_minor text,
               account_name text'''
a = Tabling(table_name, cols_list, sql_file)
a.CreateTable()
test_list = ["'710', '020', 'GAS VAN'",
             "'720', '050', 'POSTAGE'",
             "'385', '010', 'DRAW'",
             "'710', '030', 'VEHICLE REPAIRS'",
             "'620', '010', 'CASUAL LABOR'",               
             "'145', '010', 'INVENTORY'"]
a.CreateTestItem('account_major, account_minor, account_name', test_list)

     

################ Vendor Related Tables #######################
sql_file = '../db/VENDORS.sql'

## Vendor Basic Info
table_name = 'vendor_basic_info'
cols_list = '''vend_num text primary key,
               name text,
               address1 text,
               address2 text,
               city text,
               state text,
               zip text,
               acct_num text,
               post_acct text,
               phone text,
               fax text,
               email text,
               terms_day integer default 10,
               discount_percent real default 0.0,
               contact text'''
a = Tabling(table_name, cols_list, sql_file)        
a.CreateTable()
a.CreateTestItem('vend_num, name', "'0', 'Test Account'")


# Vendor Invoices
table_name = 'vendor_invoices'
cols_list = '''vend_num text,
               acct_num text,
               date text,
               amount real,
               post_date text,
               terms_days integer default 0,
               discount_percent real default 00.0,
               invoice_num text,
               post_acct text,
               disc_ok, integer default 0,
               pay_after text,
               date_paid text,
               checknum integer,
               payment_type text,
               banknum integer,
               cleared integer default 0,
               paid_in_full integer default 0'''
a = Tabling(table_name, cols_list, sql_file)
a.CreateTable()


# Vendor Invoice Distributions Data
# JSON'd
# partials = {parts : {
#                      active : active_amt,
#                      post_acct : 100-001,
#                      partialAmt : 0.00,
#                      discOK : T or F,
#                      discAmt : 0.00,
#                     }
#             }
table_name = 'vendor_invoice_dist_partials'
cols_list = '''vend_num text,
               acct_num text,
               invoice text,
               parts text'''
a = Tabling(table_name, cols_list, sql_file)               
a.CreateTable()


# Vendor Invoice PayAllocation Data
# JSON'd
# partials = {parts : {
#                      active : True or False,
#                      pay_after : date,
#                      pay_amt : 0.00,
#                      date_paid : date,
#                      check_num : 0.00
#                      }
#             }

table_name = 'vendor_invoice_partials'
cols_list = '''vend_num text,
               acct_num text,
               invoice text,
               parts text'''
a = Tabling(table_name, cols_list, sql_file)               
a.CreateTable()


# Vendor Notes
table_name = 'vendor_notes'
cols_list = '''vend_num text primary key,
               notes text'''
a = Tabling(table_name, cols_list, sql_file)               
a.CreateTable()


# ######################## Support Tables ####################
# sql_file = '../db/SUPPORT.sql'


# Organizations
table_name = 'organizations'
cols_list = '''abuser text primary key,
               department text,
               category text,
               subcategory text,
               location text,
               material text,
               unittype text,
               num_of_aisles text default '0',
               extra_places text,
               num_of_sections text default '0',
               customer_codes text,
               account_types text,
               shipping_methods text'''
a = Tabling(table_name, cols_list, sql_file)
a.CreateTable()
a.CreateTestItem('abuser, department, category, subcategory', "'rhp', 'Hardware', 'Tools', 'Wrenches'")


# ############### Item Related Tables #########################
sql_file = '../db/INVENTORY.sql'

## item retails table
table_name = 'item_retails'
cols_list = '''upc text primary key,
               standard_unit integer default 1,
               standard_price real default 0.00,
               level_a_unit integer default 1,
               level_a_price real default 0.00,
               level_b_unit integer default 1,
               level_b_price real default 0.00,
               level_c_unit integer default 1,
               level_c_price real default 0.00,
               level_d_unit integer default 1,
               level_d_price real default 0.00,
               level_e_unit integer default 1,
               level_e_price real default 0.00,
               level_f_unit integer default 1,
               level_f_price real default 0.00,
               level_g_unit integer default 1,
               level_g_price real default 0.00,
               level_h_unit integer default 1,
               level_h_price real default 0.00,
               level_i_unit integer default 1,
               level_i_price real default 0.00,
               compare_unit integer default 1,
               compare_price real default 0.00,
               on_sale_unit integer default 1,
               on_sale_price real default 0.00'''
a = Tabling(table_name, cols_list, sql_file)
a.CreateTable()
a.CreateTestItem('upc, standard_price',"'TESTITEM', 9.98")

# Item Detailed table
#   JSON'd Vendors
#   vendors = { '1' = 
#                   id : 0-9A-Z
#                   ordernum : ordernum
#                   last_cost : 0.00
#                   lead_time : 0 in days
#             }
#
table_name = 'item_detailed'
cols_list = '''upc text primary key,
               description text, 
               avg_cost real default 0.000,
               last_cost real default 0.000,
               size_a text,
               size_b text,
               altlookup text,
               qty_on_hand real default 0.000,
               qty_committed real default 0.000,
               qty_on_layaway real default 0.000,
               part_num text,
               oempart_num text,
               kit_num text,
               kit_pieces integer default 1,
               vendors text'''
a = Tabling(table_name, cols_list, sql_file)               
a.CreateTable()
a.CreateTestItem('upc, description, avg_cost, qty_on_hand',"'TESTITEM', 'Test Item', 5.34, 1")


# Closeouts
table_name = 'closeouts'
cols_list = '''upc text primary key,
               avg_cost real default 0.000,
               last_retail real default 0.000,
               closeout_date text'''
a = Tabling(table_name, cols_list, sql_file)               
a.CreateTable()

# #Alt Lookups
# table_name = 'altlookups'
# a = TableAware(table_name, sql_file, dbtype='sqlite3')
# a.AddField('upc', char=90, primary_key=True)
# a.AddField('altlookup', text='')
                  
                  
# Flexible Retail Program
table_name = 'flexible_update'
cols_list = '''upc text primary key,
               avg_cost real default 0.000,
               max_margin real default 0.000,
               last_update text'''
a = Tabling(table_name, cols_list, sql_file)               
a.CreateTable()


# Tax Holiday Table
table_name = 'tax_holiday'
cols_list = '''sheet_id integer,
               name text,
               begin_date text,
               end_date text,
               upc text,
               active integer default 1'''
a = Tabling(table_name, cols_list, sql_file)               
a.CreateTable()
for i in range(1,7):
    a.CreateTestItem('sheet_id',"'{}'".format(i)) 

# Item Detailed2 table
table_name = 'item_detailed2'
cols_list = '''upc text primary key,
               do_not_discount integer default 0,
               lock_prices integer default 0,
               tax1 integer default 0,
               tax2 integer default 0,
               tax3 integer default 0,
               tax4 integer default 0,
               tax_never integer default 0,
               override_tax_rate real default 0.000,
               sale_begin text,
               sale_end text,
               sale_begin_time text,
               sale_end_time text,
               buyX integer default 0,
               getY integer default 0,
               credit_book_exempt integer default 0,
               delete_when_out integer default 0,
               case_break_num text,
               substituteYN integer default 0,
               substitute_num text,
               location text,
               weight real default 0.000,
               tare_weight real default 0.000,
               image_loc text,
               last_saledate text,
               last_returndate text,
               maintdate text,
               added_date text,
               override_commission integer default 0,
               over_commission real default 0.000,
               over_fixed_comm real default 0.00,
               priceschema text,
               orderctrl text'''
a = Tabling(table_name, cols_list, sql_file)
a.CreateTable()
a.CreateTestItem('upc', "'TESTITEM'")


# Consignment Options - Consignment Page Options 
table_name = 'consignments'
cols_list = '''upc text primary key,
               vendor_num text,
               override_fee real'''
a = Tabling(table_name, cols_list, sql_file)
a.CreateTable()


# Item Options - info you gotta know to make sense of other things
table_name = 'item_options'
cols_list = '''upc text primary key,
               num_of_vendors integer default 0,
               department text,
               category text,
               subcategory text,
               location text,
               material text,
               postacct text,
               unit_type text,
               item_type text,
               agepopup integer default 0,
               posoptions text,
               consignment integer default 0,
               unitsinpackage integer default 1,
               foodstampexempt integer default 0,
               loyaltyexempt integer default 0,
               deactivated integer default 0,
               aisle_num text,
               extra_places text,
               section_num text,
               closeout integer default 0'''
a = Tabling(table_name, cols_list, sql_file)               
a.CreateTable()
a.CreateTestItem('upc', "'TESTITEM'")

# POSoptions via JSON
#   Prompt for Quantity = Y/N
#   Assume 1 Sold = Y/N
#   Prompt for Price, Quantity Calculated = Y/N
#   Prompt for scale = Y/N


# Item Pricing Schemes table
table_name = 'item_pricing_schemes'
cols_list = '''name text primary key,
               scheme_list text,
               reduce_by text default "3"'''
a = Tabling(table_name, cols_list, sql_file)               
a.CreateTable()
a.CreateTestItem('name, scheme_list, reduce_by', "'1-3-10','1-3-10', '2.50'")

                  
# Item Vendor Data
table_name = 'item_vendor_data'
cols_list = '''upc text primary key,
               vendor1_num text,
               vendor2_num text,
               vendor3_num text,
               vendor4_num text,
               vendor5_num text,
               vendor6_num text'''
a = Tabling(table_name, cols_list, sql_file)
a.CreateTable()
# JSON in each field
#
#   - ordernum
#   - prev_ordernum
#   - lead_time
#   - minimum_order
#   - last_order
#   - last_order_date
#   - last_rec
#   - last_rec_date
#   - outstanding
#   - units_in_order

## Item Notes
table_name = 'item_notes'
cols_list = '''upc text primary key,
               notes text'''
a = Tabling(table_name, cols_list, sql_file)               
a.CreateTable()
a.CreateTestItem('upc, notes', "'TESTITEM','This here is a note for the Test Item'")

# Item POS Sales Links
table_name = 'item_sales_links'
cols_list = '''upc text primary key,
               sales_links text'''
a = Tabling(table_name, cols_list, sql_file)               
a.CreateTable()
a.CreateTestItem('upc', "'TESTITEM'")
#JSON
#   - item(#) large number of sales links associated with item
#   - message

# Item Customer Instructions
table_name = 'item_cust_instructions'
cols_list = '''upc text primary key,
               print_info_options integer default 0,
               print_return_options integer default 0,
               print_warranty_options integer default 0,
               info_dialog text, 
               return_dialog text,
               warranty_dialog text,
               info_box, text,
               return_box text,
               warranty_box text'''
a = Tabling(table_name, cols_list, sql_file)
a.CreateTable()
info_message = 'Hello there, I see you bought the TestItem, Good Luck with that'
return_message = "Dont even think of returning this now that ive managed to get rid of it"
warranty_message = "There isnt one, even if there was, i certainly wouldnt tell you about it"
a.CreateTestItem('upc, info_box, return_box, warranty_box', f"'TESTITEM','{info_message}', '{return_message}', '{warranty_message}'")               


# Item History
table_name = 'item_history'
cols_list = '''upc text primary key,
               year integer,
               january real,
               february real,
               march real,
               april real,
               may real,
               june real,
               july real,
               august real,
               september real,
               october real,
               november real,
               december real'''
a = Tabling(table_name, cols_list, sql_file)
a.CreateTable()
a.CreateTestItem('upc, year, january', "'TESTITEM', 2021, 1.5")               

############# Transaction Related Tables #####################
sql_file = '../db/TRANSACTIONS.sql'

# Transaction Ctrl Number
table_name = 'transaction_control'
cols_list = '''abuser text primary key,
               trans_num integer'''
a = Tabling(table_name, cols_list, sql_file)
a.CreateTable()
a.CreateTestItem('abuser, trans_num', "'rhp', 0")


# Transactions
table_name = 'transactions'
cols_list = '''transaction_id text,
               date text,
               salesperson integer,
               time text,
               cust_num text,
               address_acct_num text,
               upc text,
               description text,
               qty real,
               avg_cost real,
               unit_price real,
               total_price real,
               pricetree text,
               discount text,
               type_of_transaction text,
               tax1 integer default 0,
               tax2 integer default 0,
               tax3 integer default 0,
               tax4 integer default 0,
               tax_never integer default 0,
               tax_exempt integer default 0,
               po_number text'''
a = Tabling(table_name, cols_list, sql_file)               
a.CreateTable()

fieldnames = '''transaction_id, date, salesperson, time, cust_num, address_acct_num, 
                upc, description, qty, avg_cost, unit_price, total_price, pricetree, discount, type_of_transaction,
                tax1, tax2, tax3, tax4, tax_never, tax_exempt, po_number'''
values = """'0', '20201016', '1', '10:10:00', '37047734', '', 
            'BEEFSTICK', 'Jack Links BeefStick',3, 0.65, 0.99, 2.97,'',0, 'SALE',
            1, 1, 1, 1, 1, 1, 'Test PO'"""
a.CreateTestItem(fieldnames, values)

    
#Transaction Payments
table_name = 'transaction_payments'
cols_list = '''transaction_id text primary key,
               paid real default 0.00,
               discount_taken real default 0.00,
               subtotal_price real default 0.00,
               tax real default 0.00,
               total_price real default 0.00,
               paid_date text,
               date text,
               time text,
               cust_num text,
               address_acct_num text,
               pay_method text,
               change_back text,
               type_of_transaction text,
               cash_payment real,
               check_payment real,
               check_num text,
               dl_number text,
               phone_num text,
               dob text,
               charge real default 0.00,
               card1_payment real default 0.00,
               auth1_num text,
               card1_type text,
               card1_numbers text,
               card2_payment real default 0.00,
               auth2_num text,
               card2_type text,
               card2_numbers text,
               card3_payment real default 0.00,
               auth3_num text,
               card3_type text,
               card3_numbers text,
               card4_payment real default 0.00,
               auth4_num text,
               card4_type text,
               card4_numbers text,
               card5_payment real default 0.00,
               auth5_num text,
               card5_type text,
               card5_numbers text,
               debit_payment real default 0.00,
               auth6_num text,
               debit_type text,
               debit_numbers text'''
a = Tabling(table_name, cols_list, sql_file)
a.CreateTable()

#Transaction Notes
table_name = 'transaction_notes'
cols_list = '''station_num integer,
               transaction_id text,
               line_position text,
               note text'''
a = Tabling(table_name, cols_list, sql_file)
a.CreateTable()

    
############## General Operations Related Tables ##############
sql_file = '../db/CONFIG.sql'

# Store info
table_name = 'basic_store_info'
cols_list = '''store_num integer primary key,
               name text,
               address1 text,
               address2 text,
               city text,
               state text,
               zip text,
               phone1 text,
               phone2 text,
               fax text,
               email text,
               print_on_forms integer default 0,
               late_charge real,
               cust_id_title text,
               penny_tally real,
               website text,
               logo text'''
a = Tabling(table_name, cols_list, sql_file)
a.CreateTable()
a.CreateTestItem("store_num, name, address1, city, state, zip","0,'ABC Hardware','111 Hill St','Ipsum City','OH','45632'")

# POS Controls
table_name = 'pos_controls'
cols_list = '''store_num text primary key,
               print_receipt_ondemand integer default 0,
               prompt_for_qty integer default 0,
               add_cust integer default 1,
               add_items integer default 1,
               payment_on_acct integer default 0,
               verify_assigned_discounts integer default 0,
               report_out_of_stock integer default 0,
               print_signature_line integer default 1, 
               print_item_count integer default 1,
               track_salesperson integer default 0,
               mailing_list_capture integer default 0,
               omit_discount_price integer default 0,
               disable_open_drawer integer default 1,
               omit_you_saved_line integer default 0,
               no_alt_tax integer default 1,
               notify_if_cost_gt_price integer default 1,
               offer_on_hold_options integer default 1,
               exclude_quotes integer default 0,
               print_void_transactions integer default 0,
               print_totals_on_logoff integer default 1,
               prompt_for_cost integer default 0,
               print_item_number integer default 0
               '''

a = Tabling(table_name, cols_list, sql_file)               
a.CreateTable()
a.CreateTestItem('store_num',"0")


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


# POS Messages
table_name = 'pos_messages'
cols_list = '''abuser text primary key,
               conditions text,
               return_policy text,
               warranty text,
               charge_agreement text,
               credit_card_agreement text,
               thanks text,
               check_policy text,
               layaway_policy text,
               gift_loyalty text,
               special_event text'''
a = Tabling(table_name, cols_list, sql_file)
a.CreateTable()
return_policy='30 Day Return, Package unopened, item unused'
charge_agree='You agree to pay in full every month before the 30th'
cc_agree='The way of the future, Hooray for a cashless society'
thanks='Thank you for your business'
check_policy='Nope, no thanks, never, NO CHECKS!!!!'
a.CreateTestItem('abuser, return_policy, charge_agreement, credit_card_agreement, thanks, check_policy', f"'rhp','{return_policy}','{charge_agree}','{cc_agree}','{thanks}','{check_policy}'")


# Store Closing Options
table_name = 'store_closing_options'
cols_list = '''store_num integer,
               combined_trans_detail integer default 0,
               trans_by_pay_type integer default 0,
               trans_by_salesperson integer default 0,
               trans_by_drawer integer default 1,
               tax_audit_report integer default 0,
               item_sales_by_deptcat integer default 0,
               deptcat_option integer default 0,
               exit_after_closing integer default 0,
               do_not_print_hardcopy integer default 0'''
a = Tabling(table_name, cols_list, sql_file)               
a.CreateTable()
a.CreateTestItem('store_num','0')


table_name = 'reports_closing_daily'
cols_list = '''store_num integer primary key,
               all_transactions integer default 1,
               cash_drawer_totals integer default 1,
               customer_invoiced integer default 1'''
a = Tabling(table_name, cols_list, sql_file)               
a.CreateTable()
a.CreateTestItem('store_num', "0")

table_name = 'reports_closing_weekly'
cols_list = '''store_num integer primary key,
               sales_breakdown integer default 1,
               inventory_top10 integer default 1,
               inventory_loser10 integer default 1,
               inventory_most_requested integer default 1'''
a = Tabling(table_name, cols_list, sql_file)
a.CreateTable()
a.CreateTestItem('store_num', "0")

table_name = 'reports_closing_monthly'
cols_list = '''store_num integer primary key,
               sales_breakdown integer default 1,
               inventory_top50 integer default 1,
               inventory_losers50 integer default 1,
               inventory_most_requested integer default 1,
               tax_report integer default 1'''
a = Tabling(table_name, cols_list, sql_file)               
a.CreateTable()
a.CreateTestItem('store_num', "0")

table_name = 'reports_closing_quarterly'
cols_list = '''store_num integer primary key,
               sales_breakdown integer default 1,
               inventory_top100 integer default 1,
               inventory_losers100 integer default 1'''
a = Tabling(table_name, cols_list, sql_file)
a.CreateTable()
a.CreateTestItem('store_num', "0")

table_name = 'reports_closing_yearly'
cols_list = '''store_num integer primary key,
               sales_breakdown integer default 1,
               inventory_top250 integer default 1,
               inventory_losers250 integer default 1'''
a = Tabling(table_name, cols_list, sql_file)
a.CreateTable()
a.CreateTestItem('store_num', "0")


## Payment Methods
table_name = 'payment_methods'
cols_list = '''store_num integer primary key,
               cash integer default 1,
               checks integer default 1, 
               charge integer default 0,
               credit_card integer default 1,
               debit_card integer default 1,
               food_stamps integer default 0,
               foreign_stamps integer default 0,
               loyalty_card integer default 0
               '''
a = Tabling(table_name, cols_list, sql_file)               
a.CreateTable()
a.CreateTestItem('store_num', "0")
            

table_name = 'tax_tables'
cols_list = '''tax_name text primary key,
               GLsub integer default 000,
               RNDscheme integer default 0,
               APscheme integer default 0,
               no_pennies_rounding integer default 0,
               min_sale real default 0.00,
               max_sale real default 0.00,
               item_max real default 0.00,
               from_amt0 real default 0.00,
               tax_rate0 real default 0.00000,
               from_amt1 real default 0.00,
               tax_rate1 real default 0.00000,
               from_amt2 real default 0.00,
               tax_rate2 real default 0.00000'''
a = Tabling(table_name, cols_list, sql_file)
a.CreateTable()


## Passwords
table_name = 'passwords'
cols_list = '''store_num integer primary key,
               admin_key text,
               manager_key text,
               clerk_key text,
               acctreceivable text,
               inventoryctrl text,
               acctpayable text,
               financials text,
               employees text,
               store_control_maint text,
               profit_pic text,
               close_the_store text,
               cash_drawer_display text,
               restrict_data_access text,
               exceed_credit text,
               tools_menu text,
               req_drawer_access integer default 0,
               req_cash_check integer default 0,
               req_cancel_trans integer default 0,
               req_coupons integer default 0,
               req_giftcard_override integer default 0'''
a = Tabling(table_name, cols_list, sql_file)               
a.CreateTable()
a.CreateTestItem('store_num, admin_key, manager_key, clerk_key', "0, 'rhp', 'god', '123'")


#Closeouts Options
table_name = 'closeout_options'
cols_list = '''store_num integer primary key,
               autoadd integer default 0,
               start_age text default 365,
               discount_percent integer default 10,
               max_cost_percent integer default 90,
               incremental_days integer default 30'''
a = Tabling(table_name, cols_list, sql_file)
a.CreateTable()
a.CreateTestItem('store_num',"0")               

# Misc Options
table_name = 'misc_options'
cols_list = '''store_num integer primary key,
               inv_price_label_on integer default 0,
               inv_shelf_label_spool integer default 0,
               inv_omit_label_prices integer default 0,
               ap_canadian_cheques integer default 0,
               export_to_quickbooks integer default 0'''
a = Tabling(table_name, cols_list, sql_file)               
a.CreateTable()
a.CreateTestItem('store_num', "0")

# Themes
table_name = 'themes'
cols_list = '''theme_name text primary key,
               bg text default '#ffffff',
               text text default '#000000',
               cell text default '#d6fcd7',
               info text default '#f8fda9',
               note text default '#e8f4f0'
               '''
a = Tabling(table_name, cols_list, sql_file)
a.CreateTable()
a.CreateTestItem('theme_name', "'INVENTORY'")               
a.CreateTestItem('theme_name', "'CUSTOMERS'", extra=True)
a.CreateTestItem('theme_name', "'VENDORS'", extra=True)
a.CreateTestItem('theme_name', "'POS'", extra=True)

                
## Employees
table_name = 'employees'
cols_list = '''employee_num integer primary key,
               employee_name text,
               date_of_birth text,
               ssn text'''
a = Tabling(table_name, cols_list, sql_file)
a.CreateTable()
a.CreateTestItem("employee_num, employee_name, date_of_birth, ssn", "0, 'Alvin Acres', '20121222', '234422341'")

## Discount Class
table_name = 'discount_class'
cols_list = '''class_name text primary key,
               scheme text'''
a = Tabling(table_name, cols_list, sql_file)
a.CreateTable()
# scheme in JSON = {'Department':'','Category':'',
#    'SubCatesgory':'','Price Level':'','Percentage':''}

## Item Margin
table_name = 'item_margin'
cols_list = '''store_num integer primary key,
               starting_margin_ctrl integer default 0,
               general_margin real default 50.0000,
               by_category text'''
a = Tabling(table_name, cols_list, sql_file)
a.CreateTable()


## Margin By Category
table_name = 'margin_by_category'
cols_list = '''department text,
               category text,
               subcategory text,
               margin real'''
a = Tabling(table_name, cols_list, sql_file)
a.CreateTable()


## Margin by Cost                  
table_name = 'margin_by_cost'
cols_list = '''label text,
               greater_than real,
               less_than real,
               margin real'''
a = Tabling(table_name, cols_list, sql_file)
a.CreateTable()               


## Discount Options
table_name = 'discount_options'
cols_list = '''name text primary key,
               percent real default 0.00'''
a = Tabling(table_name, cols_list, sql_file)               
a.CreateTable()


## Hardware Configs
table_name = 'hardware_config'
cols_list = '''store_num integer primary key,
               vendor_id text,
               product_id text,
               interface_id text,
               input_endpoint text,
               output_endpoint text'''
a = Tabling(table_name, cols_list, sql_file)               
a.CreateTable()

# # ############## Table Support ######################


# sql_file = '../db/SUPPORT.sql'
# table_name = 'tableSupport'
# cols_list = '''sql_file text, 
#                table_name text'''
# a = Tabling(table_name, cols_list, sql_file)               
# a.CreateTable()
# a.CreateTestItem('sql_file, table_name', 'CUSTOMERS.sql, customer_codes', sql_file)
# a.CreateTestItem('sql_file, table_name', 'CUSTOMERS.sql, customer_basic_infocodes', sql_file, extra=True)

# a.AddField('sql_file', text='')
# a.AddField('table_name', text='')

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
        
