!/bin/python
#-*- coding: utf-8 -*-

#
#
#
import wxversion
wxversion.select('2.8')

import sqlite3
import HandyUtilities as HU



def CreateTable(sql_file, table_name, column_info):
    con = None
    exists = None
    con = sqlite3.connect(sql_file)
    print('----------------------------------------')
    with con:
        cur = con.cursor()

        cur.execute("SELECT name FROM sqlite_master WHERE \
                     type='table' AND name='{0}';".format(table_name))
        exists = cur.fetchone()
        print("Fetch Catch : ", exists)
        if not exists:
            print("Does Not Exist; Creating...")
            cur.execute("CREATE TABLE {0} {1};".format(table_name, column_info))
        else:
            print("Table {0} Exists".format(exists))


def CheckEntries(sql_file):
    query = 'SELECT COUNT(*) FROM {}'.format(table_name)
    data = ''
    returnd = HU.SQConnect(query, data, sql_file).ONE()
    return returnd
#
################## Customer Related Tables ##########################
# Customer Codes
sql_file = './db/CUSTOMERS.sql'
table_name = 'customer_codes'
column_info = '(customer_code varchar(30))'
CreateTable(sql_file, table_name, column_info)

# Customer basic details
table_name = 'customer_basic_info'
column_info = '''(cust_num varchar(30) PRIMARY KEY,
                first_name varchar(30),
                last_name varchar(30),
                middle_initial varchar(6),
                suffix varchar(6),
                prefix varchar(6),
                address_acct_num varchar(90),
                phone_numbers text,
                email_addr varchar(50),
                tax_exempt_number varchar(30),
                typecode varchar(12),
                rental_of text,
                statement_terms text,
                contact1 varchar(120),
                contact2 varchar(120),
                account_type varchar(20),
                alt_post_acct varchar(10),
                date_added integer,
                last_maintained integer,
                last_sale integer,
                last_layaway integer,
                birthday text,
                charge_priviledge_expiry integer,
                full_name varchar(130))'''

CreateTable(sql_file, table_name, column_info)

# Address Accounts
table_name = 'address_accounts'
column_info = '''(addr_acct_num varchar(90),
                street_num varchar(12),
                street_direction varchar(10),
                street_name varchar(30),
                street_type varchar(12),
                unit varchar(12),
                address0 varchar(120),
                address2 varchar(50),
                address3 varchar(50),
                city varchar(30),
                state varchar(3),
                zipcode varchar(15),
                transactions text)'''

CreateTable(sql_file, table_name, column_info)

# Customer Sales Options
table_name = 'customer_sales_options'
column_info = '''(cust_num varchar(20) PRIMARY KEY,
                tax1 integer DEFAULT 0,
                tax2 integer DEFAULT 0,
                tax3 integer DEFAULT 0,
                tax4 integer DEFAULT 0,
                tax_direct integer DEFAULT 0,
                no_checks integer DEFAULT 0,
                pos_clerk_message text,
                salesperson varchar(12),
                no_discount integer DEFAULT 1,
                fixed_discount integer DEFAULT 0,
                discount_amt decimal(4,2) DEFAULT 00.00)'''

CreateTable(sql_file, table_name, column_info)

# Customer Accounts Receivables
table_name = 'customer_accts_receivable'
column_info = '''(cust_num varchar(20) PRIMARY KEY,
                credit_limit decimal(10,2),
                freeze_charges integer DEFAULT 0,
                late_charge_exempt integer DEFAULT 0,
                print_invoice_detail_on_statement integer DEFAULT 0,
                last_statement_date integer,
                last_paid_date integer,
                last_paid_amt decimal(12,2) DEFAULT 0.00)'''

CreateTable(sql_file, table_name, column_info)

# Customer Ship To Info
table_name = 'customer_shipto_info'
column_info = '''(cust_num varchar(20) PRIMARY KEY,
                name varchar(160),
                phone varchar(30),
                ship_by varchar(12),
                address_acct_num varchar(90),
                comments text)'''

CreateTable(sql_file, table_name, column_info)


# Customer Notes
table_name = 'customer_notes'
column_info = '(cust_num varchar(20) PRIMARY KEY, notes text)'

CreateTable(sql_file, table_name, column_info)


# Customer Security Photos & Facial Recognition
table_name = 'customer_security'
column_info = '(cust_num varchar(20) PRIMARY KEY,security_loc text)'

CreateTable(sql_file, table_name, column_info)
    # JSON security_loc = {[key] : '/path/to/images/'}


############### Accounting Related Tables ###################
sql_file = './db/ACCOUNTING.sql'

# General Ledger
table_name = 'general_ledger'
column_info = '''(transaction_num integer PRIMARY KEY,
                post_acct varchar(10),
                debit decimal(15,2),
                credit decimal(15,2),
                date integer,
                memo varchar(90),
                account_desc varchar(90))'''

CreateTable(sql_file, table_name, column_info)

# Accounts
table_name = 'ledger_post_accounts'
column_info = '''(account_major varchar(5),
                account_minor varchar(5),
                account_name varchar(30))'''

CreateTable(sql_file, table_name, column_info)
returnd = CheckEntries(sql_file, table_name)
print('Ledger Post Accounts : {0}'.format(returnd[0]))
InsertInto = 'INSERT INTO ledger_post_accounts values '
if returnd[0] == 0:
    do_list = [InsertInto + "('100', '010', 'Cash Disbursements');",
               InsertInto + "('100', '010', 'Cash Receipts');",
               InsertInto + "('100', '010', 'Credit Cards');",
               InsertInto + "('300', '010', 'Gift Cards');",
               InsertInto + "('000', '000', 'Food Stamps');",
               InsertInto + "('100', '020', 'Foreign Cash 1');",
               InsertInto + "('100', '030', 'Foreign Cash 2');",
               InsertInto + "('100', '040', 'Foreign Cash 3');",
               InsertInto + "('300', '020', 'Credit Book');",
               InsertInto + "('120', '010', 'Accounts Receivable');",
               InsertInto + "('145', '000', 'Inventory');",
               InsertInto + "('146', '000', 'Layaway Inventory');",
               InsertInto + "('300', '010', 'Accounts Payable');",
               InsertInto + "('310', '010', 'Sales Tax Payable');",
               InsertInto + "('400', '000', 'Store Sales');",
               InsertInto + "('500', '000', 'Cost of Sales');",
               InsertInto + "('510', '000', 'Inventory Adjustment');",
               InsertInto + "('520', '010', 'A/R Adjustments');",
               InsertInto + "('400', '020', 'Late Charge Income');",
               InsertInto + "('399', '010', 'Retained Earnings');",
               InsertInto + "('350', '010', 'Layaway Liability');",
               InsertInto + "('110', '020', 'Late Charge Receivable');",
               InsertInto + "('110', '020', 'Transfer Receivable');",
               InsertInto + "('300', '020', 'Transfer Payable');",
               InsertInto + "('300', '020', 'A/P Paid w/ Credit Card');"]

    data = ''
    for query in do_list:
        HU.SQConnect(query, data, sql_file).ONE()

#Paidout
table_name = 'paidout_routing'
column_info = '''(account_major varchar(5),
                account_minor varchar(5),
                account_name varchar(30))'''

CreateTable(sql_file, table_name, column_info)

returnd = CheckEntries(sql_file, table_name)
InsertInto = 'INSERT INTO paidout_routing values '
if returnd[0] == 0:
    do_list = [InsertInto + "('710', '020', 'GAS VAN');",
               InsertInto + "('720', '050', 'POSTAGE');",
               InsertInto + "('385', '010', 'DRAW');",
               InsertInto + "('710', '030', 'VEHICLE REPAIRS');",
               InsertInto + "('620', '010', 'CASUAL LABOR');",
               InsertInto + "('145', '010', 'INVENTORY');"]

    data = ''
    for query in do_list:
        HU.SQConnect(query, data, sql_file).ONE()

################ Vendor Related Tables #######################
sql_file = './db/VENDORS.sql'

#Vendor Basic Info
table_name = 'vendor_basic_info'
column_info = '''(vend_num varchar(20) PRIMARY KEY,
                name varchar(60),
                address1 varchar(60),
                address2 varchar(60),
                city varchar(30),
                state varchar(3),
                zip varchar(15),
                account_num text,
                post_acct varchar(12),
                phone varchar(30),
                fax varchar(30),
                email varchar(50),
                terms_days integer DEFAULT 10,
                discount_percent decimal(3,1) DEFAULT 0.0,
                contact text)'''

CreateTable(sql_file, table_name, column_info)


# Vendor Invoices
table_name = 'vendor_invoices'
column_info = '''(vend_num varchar(20),
                date integer,
                amount decimal(10,2),
                post_date varchar(8),
                terms_days integer DEFAULT 10,
                discount_percent decimal(3,1) DEFAULT 00.0,
                invoice_num varchar(45),
                post_acct text,
                disc_ok integer DEFAULT 0,
                pay_after integer,
                date_paid integer,
                checknum integer,
                payment_type varchar(12),
                banknum integer,
                cleared integer DEFAULT 0,
                breakdown text)'''

CreateTable(sql_file, table_name, column_info)


# Vendor Notes
table_name = 'vendor_notes'
column_info = '(vend_num varchar(20) PRIMARY KEY, notes text)'

CreateTable(sql_file, table_name, column_info)

######################## Support Tables ####################

sql_file = './db/SUPPORT.sql'


# Organizations
table_name = 'organizations'
column_info = '''(abuser varchar(10) PRIMARY KEY,
                department text, category text,
                subcategory text,location text,
                unittype text,
                num_of_aisles integer DEFAULT 0,
                extra_places text,
                num_of_sections integer integer DEFAULT 0,
                customer_codes text,
                account_types text)'''

CreateTable(sql_file, table_name, column_info)

returnd = CheckEntries(sql_file, table_name)
if returnd[0] == 0:
    query = 'INSERT INTO organizations (abuser) VALUES ("rhp");'
    data = ''
    HU.SQConnect(query, data, sql_file).ONE()

# Listing of Departments for Items
table_name = 'department_list'
column_info = '(department text)'
CreateTable(sql_file, table_name, column_info)


# Listing of Categories for Items
table_name = 'category_list'
column_info = '(category text)'
CreateTable(sql_file, table_name, column_info)


# Listing of SubCategory for Items
table_name = 'subcategory_list'
column_info = '(subcategory text)'
CreateTable(sql_file, table_name, column_info)


# Listing of Location/Materials for Items
table_name = 'location_list'
column_info = '(location text)'
CreateTable(sql_file, table_name, column_info)


# Listing of Unit Types
table_name = 'unittype_list'
column_info = '(unittype varchar(5))'
CreateTable(sql_file, table_name, column_info)


# Listing of Shipping Methods
table_name = 'shipping_methods'
column_info = '(method varchar(50))'
CreateTable(sql_file, table_name, column_info)


# Listing of Account Types
table_name = 'account_types'
column_info = '(account_type varchar(90))'
CreateTable(sql_file, table_name, column_info)

############### Item Related Tables #########################
sql_file = './db/INVENTORY.sql'


# Item Detailed table
table_name = 'item_detailed'
column_info = '''(upc varchar(90) PRIMARY KEY,
                description varchar(150),
                avg_cost decimal(10,3) DEFAULT 0.000,
                retails text,
                last_cost decimal(10,3) DEFAULT 0.000,
                size_A varchar(30),
                size_B varchar(30),
                altlookup text,
                quantity_on_hand decimal(12,3) DEFAULT 0.000,
                quantity_committed decimal(12,3) DEFAULT 0.000,
                quantity_on_layaway decimal(12,3) DEFAULT 0.000,
                part_num varchar(90),
                oempart_num varchar(90),
                kit_num varchar(90),
                kit_pieces integer DEFAULT 1,
                vendor_info text)'''

CreateTable(sql_file, table_name, column_info)

returnd = CheckEntries(sql_file, table_name)
if returnd[0] == 0:
    print("Creating Test Item Record")
    query = "INSERT INTO item_detailed (upc,description) VALUES \
             ('0', 'Test Item');"
    data = ''
    HU.SQConnect(query, data, sql_file).ONE()


# Item Detailed2 table
table_name = 'item_detailed2'
column_info = '''(upc varchar(90) PRIMARY KEY,
                do_not_discount integer DEFAULT 0,
                lock_prices integer DEFAULT 0,
                tax1 integer DEFAULT 0,
                tax2 integer DEFAULT 0,
                tax3 integer DEFAULT 0,
                tax4 integer DEFAULT 0,
                tax_never integer DEFAULT 0,
                override_tax_rate decimal(5,4) DEFAULT 0.0000,
                sale_begin integer,
                sale_end integer,
                sale_begin_time text,
                sale_end_time text,
                buyX integer DEFAULT 0,
                getY integer DEFAULT 0,
                credit_book_exempt integer DEFAULT 0,
                delete_when_out integer DEFAULT 0,
                case_break_num varchar(90),
                substituteYN integer DEFAULT 0,
                substitute_num varchar(90),
                location varchar(45),
                weight decimal(6,3) DEFAULT 0.000,
                tare_weight decimal(6,3) DEFAULT 0.000,
                image_loc varchar(90),
                last_saledate integer,
                last_returndate integer,
                maintdate integer, added_date integer,
                override_commission integer DEFAULT 0,
                over_commission decimal(6,4) DEFAULT 0.0000,
                over_fixd_comm decimal(6,2) DEFAULT 0.00,
                priceschema varchar(2),orderctrl text)'''

CreateTable(sql_file, table_name, column_info)

returnd = CheckEntries(sql_file, table_name)
if returnd[0] == 0:
    print("Creating Test Item Record")
    query = "INSERT INTO item_detailed2 (upc) VALUES ('0');"
    data = ''
    HU.SQConnect(query, data, sql_file).ONE()


# Item Options - info you gotta know to make sense of other things
table_name = 'item_options'
column_info = '''(upc varchar(90) PRIMARY KEY,
                num_of_vendors integer DEFAULT 0,
                department varchar(15),
                category varchar(15),
                subcategory varchar(15),
                location varchar(15),
                postacct varchar(12),
                unit_type varchar(10),
                item_type varchar(15),
                agepopup integer DEFAULT 0,
                posoptions text,
                consignment integer DEFAULT 0,
                unitsinpackage integer DEFAULT 1,
                foodstampexempt integer DEFAULT 1,
                loyaltyexempt integer DEFAULT 0,
                deactivated integer DEFAULT 0,
                aisle_num varchar(3),
                extra_places varchar(30),
                section_num varchar(15))'''

CreateTable(sql_file, table_name, column_info)

returnd = CheckEntries(sql_file, table_name)
if returnd[0] == 0:
    print("Creating Test Item Record")
    query = "INSERT INTO item_options (upc) VALUES ('0');"
    data = ''
    HU.SQConnect(query, data, sql_file).ONE()

# POSoptions via JSON
#   Prompt for Quantity = Y/N
#   Assume 1 Sold = Y/N
#   Prompt for Price, Quantity Calculated = Y/N
#   Prompt for scale = Y/N


# Item Pricing Schemes table
table_name = 'item_pricing_schemes'
column_info = '''(name varchar(10) PRIMARY KEY,
                scheme_list text,
                reduce_by varchar(90) DEFAULT "3")'''
CreateTable(sql_file, table_name, column_info)

returnd = CheckEntries(sql_file, table_name)

if returnd[0] == 0:
    print("Creating Test Item Record")
    query = """INSERT INTO item_pricing_schemes
             (name,scheme_list, reduce_by) VALUES('1-3-10','1-3-10',2.50);"""
    data = ''
    HU.SQConnect(query, data, sql_file).ONE()

                  
# Item Vendor Data
table_name = 'item_vendor_data'
column_info = '''(upc varchar(90) PRIMARY KEY,
                vendor1_num text,
                vendor2_num text,
                vendor3_num text,
                vendor4_num text,
                vendor5_num text,
                vendor6_num text)'''

CreateTable(sql_file, table_name, column_info)

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

# Item Notes
table_name = 'item_notes'
column_info = '''(upc varchar(90) PRIMARY KEY,
                  notes text)'''
CreateTable(sql_file, table_name, column_info)

returnd = CheckEntries(sql_file, table_name)
if returnd[0] == 0:
    print("Creating Test Item Record")
    query = "INSERT INTO item_notes (upc) VALUES ('0');"
    data = ''
    HU.SQConnect(query, data, sql_file).ONE()

# Item POS Sales Links
table_name = 'item_sales_links'
column_info = '''(upc varchar(90) PRIMARY KEY,
                  sales_links text)'''
CreateTable(sql_file, table_name, column_info)

returnd = CheckEntries(sql_file, table_name)
if returnd[0] == 0:
    print("Creating Test Item Record")
    query = "INSERT INTO item_sales_links (upc) VALUES ('0');"
    data = ''
    HU.SQConnect(query, data, sql_file).ONE()

    #JSON
    #   - item(#) infinite number of sales links associated with item
    #   - message


# Item Customer Instructions
table_name = 'item_cust_instructions'
column_info = '''(upc varchar(90) PRIMARY KEY,
                  print_options text,
                  dialog varchar(45),
                  info_box text)'''
CreateTable(sql_file, table_name, column_info)

returnd = CheckEntries(sql_file, table_name)
if returnd[0] == 0:
    print("Creating Test Item Record")
    query = "INSERT INTO item_cust_instructions (upc) VALUES ('0');"
    data = ''
    HU.SQConnect(query, data, sql_file).ONE()

# Item History
table_name = 'item_history'
column_info = '''(upc varchar(90) PRIMARY KEY,
                  year integer,
                  January decimal(20,3),
                  February decimal(20,3),
                  March decimal(20,3),
                  April decimal(20,3),
                  May decimal(20,3),
                  June decimal(20,3),
                  July decimal(20,3),
                  August decimal(20,3),
                  September decimal(20,3),
                  October decimal(20,3),
                  November decimal(20,3),
                  December decimal(20,3))'''

CreateTable(sql_file, table_name, column_info)

returnd = CheckEntries(sql_file, table_name)
if returnd[0] == 0:
    print("Creating Test Item Record")
    query = "INSERT INTO item_history (upc) VALUES ('0');"
    data = ''
    HU.SQConnect(query, data, sql_file).ONE()

############# Transaction Related Tables #####################
sql_file = './db/TRANSACTIONS.sql'

# Transactions
table_name = 'transactions'
column_info = '''(transaction_id varchar(15),
                  date integer,
                  salesperson integer,
                  time text,
                  cust_num varchar(30),
                  address_acct_num varchar(90),
                  upc varchar(90),
                  description varchar(120),
                  quantity decimal(20,3),
                  avg_cost decimal(20,3),
                  unit_price decimal(20,2),
                  total_price decimal(20,2),
                  discount decimal(20,3),
                  type_of_transaction varchar(15),
                  tax1 integer DEFAULT 0,
                  tax2 integer DEFAULT 0,
                  tax3 integer DEFAULT 0,
                  tax4 integer DEFAULT 0,
                  tax_never integer DEFAULT 0,
                  po_number varchar(120))'''

CreateTable(sql_file, table_name, column_info)
# per item entry per row, no primary key

#Transaction Payments
table_name = 'transaction_payments'
column_info = '''(transaction_id varchar(15),
                  paid decimal(20,3) DEFAULT 0.00,
                  total_price decimal(20,3) DEFAULT 0.00,
                  date integer,
                  time text,
                  cust_num varchar(30),
                  address_acct_num varchar(90),
                  pay_method varchar(15),
                  type_of_transaction varchar(15),
                  cash_payment decimal(20,2),
                  check_payment decimal(20,2),
                  check_num varchar(30),
                  dl_number varchar(90),
                  phone_num varchar(15),
                  dob integer,
                  card1_payment decimal(20,2) DEFAULT 0.00,
                  auth1_num varchar(60),
                  card1_type varchar(60),
                  card1_numbers varchar(36),
                  card2_payment decimal(20,2) DEFAULT 0.00,
                  auth2_num varchar(60),
                  card2_numbers varchar(36),
                  card2_type varchar(60),
                  card3_payment decimal(20,2) DEFAULT 0.00,
                  auth3_num varchar(60),
                  card3_numbers varchar(36),
                  card3_type varchar(60),
                  card4_payment decimal(20,2) DEFAULT 0.00,
                  auth4_num varchar(60),
                  card4_numbers varchar(36),
                  card4_type varchar(60),
                  card5_payment decimal(20,2) DEFAULT 0.00,
                  auth5_num varchar(60),
                  card5_numbers varchar(36),
                  card5_type varchar(60),
                  debit_payment decimal(20,2) DEFAULT 0.00,
                  auth6_num varchar(60),
                  debit_numbers varchar(36),
                  debit_type varchars(60))'''





CreateTable(sql_file, table_name, column_info)

#Transaction Notes
table_name = 'transaction_notes'
column_info = '''(station_num varchar(3), 
                  transaction_id varchar(15),
                  line_position varchar(15),
                  note text)'''            

CreateTable(sql_file, table_name, column_info)
    
############## General Operations Related Tables ##############
sql_file = './db/CONFIG.sql'

# Store info
table_name = 'basic_store_info'
column_info = '''(store_num integer PRIMARY KEY,
                  name varchar(90),
                  address1 varchar(90),
                  address2 varchar(90),
                  city varchar(30),
                  state varchar(3),
                  zip varchar(15),
                  phone1 varchar(15),
                  phone2 varchar(15),
                  fax varchar(15),
                  email varchar(50),
                  print_on_forms integer DEFAULT 0,
                  late_charge decimal(3,2),
                  Cust_id_title varchar(50),
                  penny_tally decimal(12,2),
                  website text,
                  logo text)'''

CreateTable(sql_file, table_name, column_info)

# POS Controls
table_name = 'pos_controls'
column_info = '''(print_receipt_ondemand integer DEFAULT 0,
                  prompt_for_qty integer DEFAULT 0,
                  add_cust integer DEFAULT 0,
                  add_items integer DEFAULT 0,
                  payment_on_acct integer DEFAULT 0,
                  verify_assigned_discounts integer DEFAULT 0,
                  report_out_of_stock integer DEFAULT 0,
                  disable_credit_security integer DEFAULT 0,
                  print_signature_line integer DEFAULT 0,
                  skip_finished_question integer DEFAULT 0,
                  print_item_count integer DEFAULT 0,
                  track_salesperson integer DEFAULT 0,
                  mailing_list_capture integer DEFAULT 0,
                  disable_open_drawer integer DEFAULT 0,
                  dept_totals_by_drawer integer DEFAULT 0,
                  omit_cust_addr integer DEFAULT 0,
                  print_totals_on_logoff integer DEFAULT 0,
                  save_cleared_totals_to_reconcile integer DEFAULT 0,
                  verify_parts_explosion integer DEFAULT 0,
                  display_parts_explosion integer DEFAULT 0,
                  print_kit_parts integer DEFAULT 0,
                  print_kit_parts_price integer DEFAULT 0,
                  discount_omit_price integer DEFAULT 0,
                  trap_zips integer DEFAULT 0,
                  prompt_for_cost integer DEFAULT 0,
                  print_item_num integer DEFAULT 0,
                  support_eos_discount integer DEFAULT 0,
                  no_alt_tax integer DEFAULT 0,
                  notify_if_cost_gt_price integer DEFAULT 0,
                  omit_you_saved_line integer DEFAULT 0,
                  offer_on_hold_options integer DEFAULT 0,
                  print_void_trans integer DEFAULT 0,
                  exclude_layaways integer DEFAULT 0,
                  exclude_orders integer DEFAULT 0,
                  exclude_quotes integer DEFAULT 0,
                  exclude_hold integer DEFAULT 0)'''

CreateTable(sql_file, table_name, column_info)


# POS Messages
table_name = 'pos_messages'
column_info = '''(abuser varchar(10) PRIMARY KEY,
                conditions text,
                return_policy text,
                warranty text,
                charge_agreement text,
                credit_card_agreement text,
                thanks text,
                check_policy text,
                layaway_policy text,
                gift_loyalty text,
                special_event text)'''

CreateTable(sql_file, table_name, column_info)

# Store Closing Options
table_name = 'store_closing_options'
column_info = '''(combined_trans_detail integer DEFAULT 0,
                trans_by_pay_type integer DEFAULT 0,
                trans_by_salesperson integer DEFAULT 0,
                trans_by_drawer integer DEFAULT 0,
                tax_audit_report integer DEFAULT 0,
                item_sales_by_deptcat integer DEFAULT 0,
                deptcat_option integer DEFAULT 0,
                exit_after_closing integer DEFAULT 0,
                do_not_print_hardcopy integer DEFAULT 0)'''

CreateTable(sql_file, table_name, column_info)

#Payment Methods
table_name = 'payment_methods'
column_info = '''(cash integer DEFAULT 0,
                checks integer DEFAULT 0,
                house_charges integer DEFAULT 0,
                credit_cards integer DEFAULT 0,
                credit_book integer DEFAULT 0,
                food_stamps integer DEFAULT 0,
                foreign_cash integer DEFAULT 0,
                loyalty_card integer DEFAULT 0,
                check_setup_def_state varchar(20),
                check_setup_def_guarrantor varchar(20))'''

CreateTable(sql_file, table_name, column_info)

table_name = 'tax_tables'
column_info = '''(tax_name varchar(20) DEFAULT 'TAX',
                 GLsub integer DEFAULT 000,
                 RNDscheme integer DEFAULT 0,
                 APscheme integer DEFAULT 0,
                 no_pennies_rounding integer DEFAULT 0,
                 min_sale decimal(5,2) DEFAULT 0.00,
                 max_sale decimal(5,2) DEFAULT 0.00,
                 item_max decimal(5,2) DEFAULT 0.00,
                 from_amt0 decimal(5,2) DEFAULT 0.00,
                 tax_rate0 decimal(6,5) DEFAULT 0.00000,
                 from_amt1 decimal(5,2) DEFAULT 0.00,
                 tax_rate1 decimal(6,5) DEFAULT 0.00000,
                 from_amt2 decimal(5,2) DEFAULT 0.00,
                 tax_rate2 decimal(6,5) DEFAULT 0.00000)'''

CreateTable(sql_file, table_name, column_info)

returnd = CheckEntries(sql_file,table_name)
if returnd[0] == 0:
    query = 'INSERT INTO tax_tables (tax_name) VALUES (?)'
    data = ('TAX',)
    HU.SQConnect(query, data, sql_file).ONE()


# Passwords
table_name = 'passwords'
column_info = '''(abuser varchar(15) DEFAULT 'rhp',
                admin_key varchar(15),
                manager_key varchar(15),
                clerk_key varchar(15),
                acctreceivable varchar(15),
                inventoryctrl varchar(15),
                acctpayable varchar(15),
                financials varchar(15),
                employees varchar(15),
                store_controls_maint varchar(15),
                profit_pic varchar(15),
                close_the_store varchar(15),
                cash_drawer_display varchar(15),
                restrict_data_access varchar(15),
                exceed_credit varchar(15),
                tools_menu varchar(15),
                req_drawer_access integer DEFAULT 0,
                req_cash_check integer DEFAULT 0,
                req_cancel_trans integer DEFAULT 0,
                req_coupons integer DEFAULT 0,
                req_giftcard_override integer DEFAULT 0)'''

CreateTable(sql_file, table_name, column_info)
returnd = CheckEntries(sql_file,table_name)
if returnd[0] == 0:
    query = 'INSERT INTO passwords (abuser, admin_key) VALUES (?,?)'
    data = ('rhp','123',)
    HU.SQConnect(query, data,sql_file).ONE()

query = "SELECT admin_key FROM passwords WHERE abuser='rhp'"
data = ''
returnd = HU.SQConnect(query, data, sql_file).ONE()
if returnd == None:
    query = "UPDATE TABLE passwords SET admin_key='123' WHERE abuser='rhp'"
    data = ''
    HU.SQConnect(query, data, sql_file).ONE()
    
# Misc Options
table_name = 'misc_options'
column_info = '''(inventory_price_label_on integer DEFAULT 0,
                inventory_shelf_label_spool integer DEFAULT 0,
                inventory_omit_label_prices integer DEFAULT 0,
                ap_canadian_cheques integer DEFAULT 0,
                export_to_quickbooks integer DEFAULT 0)'''

CreateTable(sql_file, table_name, column_info)

# Themes
table_name = 'themes'
column_info = '''(theme_name varchar(25) PRIMARY KEY,
                  bg varchar(50),
                  text varchar(50),
                  cell varchar(50))'''

CreateTable(sql_file, table_name, column_info)                  
                
# Employees
table_name = 'employees'
column_info = '''(employee_num varchar(6) PRIMARY KEY,
                employee_name varchar(160),
                date_of_birth integer,
                ssn varchar(15))'''

CreateTable(sql_file, table_name, column_info)


# Discount Class
table_name = 'discount_class'
column_info = '''(class_name varchar(90),
                schema text)'''
# schema in JSON = {'Department':'','Category':'',
#    'SubCatesgory':'','Price Level':'','Percentage':''}

# Item Margin
table_name = 'item_margin'
column_info = '''(starting_margin_control integer DEFAULT 0,
                general_margin decimal(6,3) DEFAULT 50.0000,
                by_category text,
                by_price text)'''

CreateTable(sql_file, table_name, column_info)

# Discount Options
table_name = 'discount_options'
column_info = '''(name varchar(45) PRIMARY KEY,
                  percent decimal(3,2) DEFAULT 0.00)'''

CreateTable(sql_file, table_name, column_info)


########### TableName LOOKUP REFERENCE ###############
sql_file = './db/SUPPORT.sql'
table_name = 'tableSupport'
column_info = '(sql_file text, table_names text)'
CreateTable(sql_file, table_name, column_info)
returnd = CheckEntries(sql_file,table_name)
do_list = [('CUSTOMERS.sql', 'customer_codes'),
           ('CUSTOMERS.sql', 'customer_basic_info'),
               ('CUSTOMERS.sql', 'address_accounts'),
               ('CUSTOMERS.sql', 'customer_sales_options'),
               ('CUSTOMERS.sql', 'customer_accts_receivable'),
               ('CUSTOMERS.sql', 'customer_shipto_info'),
               ('CUSTOMERS.sql', 'customer_notes'),
               ('CUSTOMERS.sql', 'customer_security'),
               ('ACCOUNTING.sql', 'general_ledger'),
               ('ACCOUNTING.sql', 'ledger_post_accounts'),
               ('ACCOUNTING.sql', 'paidout_routing'),
               ('VENDORS.sql', 'vendor_basic_info'),
               ('VENDORS.sql', 'vendor_invoices'),
               ('VENDORS.sql', 'vendor_notes'),
               ('SUPPORT.sql', 'organizations'),
               ('SUPPORT.sql', 'department_list'),
               ('SUPPORT.sql', 'category_list'),
               ('SUPPORT.sql', 'subcategory_list'),
               ('SUPPORT.sql', 'location_list'),
               ('SUPPORT.sql', 'unittype_list'),
               ('SUPPORT.sql', 'shipping_methods'),
               ('SUPPORT.sql', 'account_types'),
               ('INVENTORY.sql', 'item_detailed'),
               ('INVENTORY.sql', 'item_detailed2'),
               ('INVENTORY.sql', 'item_options'),
               ('INVENTORY.sql', 'item_pricing_schemes'),
               ('INVENTORY.sql', 'item_vendor_data'),
               ('INVENTORY.sql', 'item_notes'),
               ('INVENTORY.sql', 'item_sales_links'),
               ('INVENTORY.sql', 'item_cust_instructions'),
               ('INVENTORY.sql', 'item_history'),
               ('TRANSACTIONS.sql', 'transactions'),
               ('TRANSACTIONS.sql', 'transaction_payments'),
               ('TRANSACTIONS.sql', 'transaction_notes'),
               ('CONFIG.sql', 'basic_store_info'),
               ('CONFIG.sql', 'pos_controls'),
               ('CONFIG.sql', 'pos_messages'),
               ('CONFIG.sql', 'store_closing_options'),
               ('CONFIG.sql', 'payment_methods'),
               ('CONFIG.sql', 'tax_tables'),
               ('CONFIG.sql', 'passwords'),
               ('CONFIG.sql', 'misc_options'),
               ('CONFIG.sql', 'employees'),
               ('CONFIG.sql', 'discount_class'),
               ('CONFIG.sql', 'item_margin'),
               ('CONFIG.sql', 'discount_options'),
               ('CONFIG.sql', 'themes')]


for sqlfile, tableName in do_list:
    query = 'SELECT COUNT(*) FROM tableSupport WHERE sql_file=(?) AND table_names=(?)'
    data = (sqlfile, tableName)
    cnt_returnd = HU.SQConnect(query, data, sql_file).ONE()
    cnt = HU.DeTupler(cnt_returnd)
    if cnt == 0:
        query = 'INSERT INTO tableSupport (sql_file, table_names) VALUES (?,?)'
        data = (sqlfile, tableName)
        HU.SQConnect(query, data, sql_file).ONE()
        
