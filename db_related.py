import pout
import re
import json
import pymysql
import sqlite3
import fdb
import time
from var_operations import VarOps


class SQConnect(object):
    def __init__(self, query, data=None, sql_file=None, dbtype='sqlite3', debug=False):
        self.dbtype = dbtype
        self.query = None
        self.data = None
        self.sql_file = sql_file
        self.debug = debug
        checkTypes = []
        if query is not None:
            query = query.replace("?","%s")
        
        checkTypes = [('query', self.query),
                      ('data', self.data)]    
    
        self.query = query
        self.data = self.MaskData(query,data)
        returnd = None
    
    def ALL(self):
        if self.dbtype == 'mysql':
            con = pymysql.connect(host='localhost', user='rhp', passwd='password', db='rhp')
        if self.dbtype == 'fdb':
            con = fdb.connect(host='localhost', database=f'../db/{self.sql_file}', user='rhp', password='password')
        if self.dbtype == 'sqlite3':
            con = sqlite3.connect(self.sql_file)
        
        cur = con.cursor()
        if len(self.data) > 0:
            cur.execute(self.query, self.data)
        else:
            cur.execute(self.query)
            
        returnd = cur.fetchall()
        if re.search('(UPDATE|INSERT)', self.query, re.I):
            con.commit()

        con.close()

        return self.CheckJson(returnd)

    def ONE(self):
        if self.dbtype == 'mysql':
            con = pymysql.connect(host='localhost', user='rhp', passwd='password', db='rhp')
        if self.dbtype == 'fdb':
            con = fdb.connect(host='localhost', database=f'../db/{self.sql_file}', user='rhp', password='password')
        if self.dbtype == 'sqlite3':
            con = sqlite3.connect(self.sql_file)
        
        cur = con.cursor()
        if len(self.data) > 0:
            cur.execute(self.query, self.data)
        else:
            cur.execute(self.query)
    
        returnd = cur.fetchone()
        if re.search('(UPDATE|INSERT)', self.query, re.I):
            con.commit()
        con.close()

        return self.CheckJson(returnd)

    def CHECK(self):
        if re.search('update', self.query, re.I):
            tab = re.search('update.(.*).set', self. query, re.I)
        elif re.search('select', self.query, re.I):
            tab = re.search('where.(.*).set', self.query, re.I)

        tabld = tab.group(1).strip()
        
        sql_file = FindSQLFile(tabld)
        newq = 'SELECT COUNT(*) FROM {0} WHERE upc=(?)'.format(tabld)
        newdata = self.data[len(self.data) - 1]
        
        newdatas = (newdata,)
        returnd = SQConnect(sql_file, newq, newdatas).ONE()
        
        if returnd[0] >= 1:
            print(f'Returnd : {returnd[0]}')
           
        return returnd[0]

    def UniqueList(self, seq, idfun=None):
    # order preserving
        if idfun is None:
            def idfun(x):
                return x
        seen = {}
        result = []
        for item in seq:
            marker = idfun(item)
            if marker in seen:
                continue
            seen[marker] = 1
            result.append(item)
        return result


    def MaskData(self, query, data, debug=False):
        if data is not None or data != '' or len(data) != 0:
            new_data = []
            fromquery = []
            if re.search('SELECT', query, re.I):
                if re.search('LIKE', query, re.I):
                    if re.search('(or|and)', query, re.I):
                        fromquery = re.split('(or|and)', query, flags=re.IGNORECASE)
                    else:
                        fromquery.append(query)
                        
                    idx = 0
                    for item in fromquery:
                        print(f'Item L : {len(fromquery)}')
                        dat = ''
                        if re.search('(\?|%s)', item):
                            if re.search('LIKE',item, re.I):
                                if len(data) != 0:
                                    dat = '%{}%'.format(data[idx])
                            else:
                                print(f'IDX : {idx} ; Data : {data}')
                                print(f'FROMQuery : {fromquery}\nItem : {item}')
                                dat = '{}'.format(data[idx])
                            new_data.append(dat)
                            idx += 1
                else:
                    new_data = data
            else:
                new_data = data

            typd = str(type(new_data))
            if 'list' in typd:
                
                new_data = tuple(new_data)
                
        else:
            pass    
        
        if len(data) == 0:
            new_data = ''
        
        return new_data

    def Typd(self, ret):
        return str(type(ret))
 
    def CheckType(self, ret):
        if ',' in self.query:
            ret = ret[0]
        else:
            while 'tuple' in self.Typd(ret):
                # if len(ret) == 0 and not 'tuple' in self.Typd(ret):
                #     pout.v('Len of ret : {}'.format(len(ret)))
                #     break
                try:
                    ret = ret[0]
                except IndexError as e:
                    print(f'Returnd : {ret} ; {e}')
                    break

        pout.v(f'CheckType : {ret}')   
        return ret
        
    def CheckJson(self, myjson):
        posttype = self.CheckType(myjson)
        pout.v(f'Check Type : {posttype}')
        try:
            json_object = json.loads(posttype)
        except:
            json_object = posttype
        
        pout.v(json_object)
        return json_object

    def FindSQLFile(self, tableName):
        sql_file = '../db/SUPPORT.sql'
        prefix = '../db/'
        query = "SELECT sql_file FROM tableSupport WHERE table_names=(?)"
        data = (tableName,)
        returnd = SQConnect(query, data, sql_file).ONE()
        
        filed = prefix + returnd[0]
        if os.path.isfile(filed):
            return filed
        else:
            
            print(('--- table Name : {0} ---'.format(tableName)))


     
    

class LookupDB(object):
    def __init__(self, table, sql_file, debug=False):
        self.table = table
        self.sql_file = sql_file
    
    def General(self, selectFields, limit=None):
        """Lookup in the database for a non-specific search.

        Arguments:
          selectFields -- Which fields that you will be searching for. (Mandatory)
          limit        -- Limit the search to a specific number of records. (Optional)
        """

        limitd = self.Limit(limit)
        query = '''SELECT {}
                   FROM {}
                   {}'''.format(selectFields, self.table, limitd)
        
        data = ''
        returnd = SQConnect(query, data, self.sql_file).ALL()
        return returnd
        
    def Specific(self, whereValue, whereField, selectFields, limit=None):
        limitd = self.Limit(limit)
        query = '''SELECT {}
                   FROM {}
                   WHERE {}=(?)
                   {}'''.format(selectFields, self.table, whereField, limitd)
        
        data = [whereValue,]
        returnd = SQConnect(query, data, sql_file=self.sql_file).ALL()
        
        pout.v('Specific : {} ; Query : {} ; Data : {}'.format(returnd, query, data))
        #ty = self.Typed(returnd)
        pout.v(f'Typed : {ty}')
        return returnd
       
    def Typed(self, its):
        a = str(type(its))
        new_its = its
        if 'tuple' in a:
            if len(a) == 0:
                new_its = None
        
        return new_its

    
    def Count(self, whereValue=None, whereField=None, limit=None):
        limitd = self.Limit(limit)
        where_Stmt = 'WHERE {}=(?)'.format(whereField)
        if whereField is None:
            where_Stmt = ''
        query = '''SELECT count(*)
                   FROM {}
                   {}
                   {}'''.format(self.table, where_Stmt, limitd)
        data = [whereValue,]
        if not whereValue:
            data = []
        pout.v(f'Where : {query}\n Data : {data}')
        returnd = SQConnect(query, data, sql_file=self.sql_file).ONE()
        # if len(returnd) == 0:
        #     returnd = (None,)

        pout.v(f'Count : {returnd}')
        return returnd


    def Limit(self, limit):
        
        if limit is not None:
            limitd = 'LIMIT {}'.format(limit)
        else:
            limitd = ''
        return limitd            

    def UpdateSingle(self, setField, setValue, whereField, whereValue):
        if setValue is None:
            setValue = "NULL"            
        else:
            setValue = f"'{setValue}'"

        query = '''UPDATE {}
                   SET {}={}
                   WHERE {}=(?)'''.format(self.table, setField, setValue, whereField)
        data = [whereValue,]
        returnd = SQConnect(query, data, sql_file=self.sql_file).ALL()
        # print(f"Update Single Returnd : {returnd}")
        # print('Type of Returnd : {}'.format(str(type(returnd))))
        a = str(type(returnd))
        obret = VarOps().CheckNone(returnd)
        
        return obret    

    def UpdateGroup(self, setWhatNto, whereField, whereValue):
        query = '''UPDATE {}
                   SET {}
                   WHERE {}=(?)'''.format(self.table, setWhatNto, WhereField)
        data = WhereValue
        returnd = SQConnect(query, data, sql_file=self.sql_file).ALL()
        
        return returnd[0]

    def DescribeTable(self):
        # try:
        query = '''SELECT * FROM information_schema.COLUMNS 
                   WHERE TABLE_SCHEMA = 'rhp' 
                   AND TABLE_NAME = "{}"
                   AND COLUMN_NAME = "{}"'''.format(self.table)
        data = []
        returnd = SQConnect(query, data, sql_file=self.sql_file).ALL()
        pout.b(f'DescribeTable : {query} \nReturnd : {returnd}')
        info = {}
        tb = len(returnd)
        for cnt in range(0, tb):
            for val in returnd:
                pout.v(f'Val : {val}')
                info[cnt] = {'field': val[2],
                        'type': val[7],
                        'null': val[6],
                        'key': val[16],
                        'default': val[5],
                        'extra': val[17]}
            returnd = info
        pout.v(returnd)
        time.sleep(3)
    # except:
            # returnd = None
        
        return returnd

    def is_table(self):
        query = '''SELECT * FROM information_schema.COLUMNS 
                   WHERE TABLE_SCHEMA = 'rhp' 
                   AND TABLE_NAME = "{}"
                '''.format(self.table)
        data = []
        returnd = SQConnect(query, data, sql_file=self.sql_file).ALL()
        
        return returnd
    
    def is_field(self, fieldname):
        query = '''   
        SELECT * 
        FROM information_schema.COLUMNS 
        WHERE 
            TABLE_SCHEMA = 'rhp' 
        AND TABLE_NAME = '{}' 
        AND COLUMN_NAME = '{}'; '''.format(self.table, fieldname)
        data = []
        returnd = SQConnect(query, data, sql_file=self.sql_file).ONE()
        pout.v(query)
        return returnd


class TableAware(object):
    def __init__(self, table_name, sql_file=None, dbtype='sqlite3'):
        self.table_name = table_name
        self.sql_file = sql_file
        self.dbtype = dbtype.lower()
        self.table_list = None
    
    def CheckTable(self):
        print(f'** Table Check : {self.table_name} : ')
        returnd = LookupDB(self.table_name, sql_file=self.sql_file).is_table()
        addTable = False
        try:
            if len(returnd) == 0:
                addTable = True
        except:
            print('Not an Empty Tuple')

        
        if returnd is None:
            print('\r Adding...')
            addTable = True
        return addTable 

    def CheckFieldName(self, fieldname):
        print(f'\t Field Name Check : {fieldname}')
        self.CheckTable()
        if self.dbtype == 'mysql':
            returnd = LookupDB(self.table_name, sql_file=self.sql_file).is_field(fieldname)
            addcolumn = False
            if returnd is None:
                addcolumn = True
            
            return addcolumn
    
    def CompareField(self, fieldname, defn):
        pout.b('Compare Field')
        self.table_list = LookupDB(self.table_name, sql_file=self.sql_file).DescribeTable()
        pout.v(self.table_name, self.table_list)
        time.sleep(3)
        if self.table_list is not None:
            tb = len(self.table_list)
            pout.v(f'tb : {tb}')
            for cnt in range(0, tb):
                if self.table_list[cnt]['field'] == fieldname:
                    print(f"{self.table_list[cnt]['field']} == {fieldname}")
                    if self.table_list[cnt]['type'] != defn:
                        print('Drop Field : {}'.format(fieldname))
                        # self.DropField(fieldname)
            time.sleep(3)        

    def CreateTable(self, fieldname, defn):
        query = 'CREATE TABLE {} ({} {})'.format(self.table_name, fieldname, defn) 
        print(f' ** Create Table : query : {query}')
        data = []
        returnd = SQConnect(query, data, sql_file=self.sql_file).ONE()
        self.AddSupport()
    
    def CheckDBType(self):
        pass

    def SortDefn(self, defn):
        primary_key = defn['primary_key']
        defaults = defn['defaults']
        del defn['primary_key']
        del defn['defaults']
        coldefn = ''
        for key, value in defn.items():
            if value is not None:
                if key in ['date', 'bool', 'text', 'time']:
                    coldefn = '{}'.format(key)
                elif key in ['decimal']:
                    coldefn = '{}'.format(key)
                else:
                    coldefn = '{}({})'.format(key, value)
        typed = coldefn        
        if primary_key is not False:
            coldefn += ' PRIMARY KEY'
        if defaults is not None:
            coldefn += ' DEFAULT {}'.format(defaults)
        
        return coldefn, typed

    def AddSupport(self):
        support_sql = '../db/SUPPORT.sql'
        query = f'INSERT INTO {self.table_name} (sql_name, table_name) VALUES (?, ?)'
        data = (self.sql_file, self.table_name)
        returnd = SQConnect(query, data, support_sql).ONE()

    def AddField(self, fieldname, char=None, varchar=None, integer=None, text=None, date=None, bool=None, time=None, decimal=None, primary_key=False, defaults=None):
        addTable = self.CheckTable()
        if self.dbtype == 'sqlite3':
            defn = {'char':char, 'varchar':varchar, 'int':integer, 'text':text, 'date':date, 'bool':bool, 'time':time, 'decimal':decimal, 'primary_key':primary_key, 'defaults':defaults}    
        if self.dbtype == 'mysql':
            defn = {'char':char, 'varchar':varchar, 'int':integer, 'text':text, 'date':date, 'bool':bool, 'time':time, 'decimal':decimal, 'primary_key':primary_key, 'defaults':defaults}
        
        orig_defn = defn
        col_defn, justtypd = self.SortDefn(defn)
        print(f'Column Definitions : {col_defn}, {justtypd}')
        self.CompareField(fieldname, justtypd)
        if addTable is True:
            self.CreateTable(fieldname, col_defn)
        chkfield = self.CheckFieldName(fieldname)
        if chkfield is True:
            query = 'ALTER TABLE {} ADD COLUMN {} {}'.format(self.table_name, fieldname, col_defn)
            print(f'++ ALTER TABLE : ADD COLUMN : {query}')
            data = []
            returnd = SQConnect(query, data).ONE()

    def DropField(self, fieldname):
        addTable = self.CheckTable()
        if addTable is True:
            print('Table does not Exist')
        else:
            query = 'ALTER TABLE {} DROP {}'.format(self.table_name, fieldname)
            print(f'-- ALTER TABLE : DROP COLUMN : {query}')
            data = []
            returnd = SQConnect(query, data).ONE()

    def CheckEntries(self):
        query = 'SELECT COUNT(*) FROM {}'.format(self.table_name)
        data = ''
        return SQConnect(query, data).ONE()
        
    def CreateTestItem(self, fieldnames, values, extra=None):
        returnd = self.CheckEntries()
        pout.v(returnd)
        if returnd == 0 or extra is not None:
            fn = fieldnames.split(",")
            val = values.split(",")
            pout.v(f'FieldNames : {fn} ; Values : {val}')
            chkexist = LookupDB(self.table_name).Count(val[0].strip("'"), fn[0].strip("'"))
            if chkexist == 0:
                print(f'Creating Test Item for {self.table_name}')
                query = f"INSERT INTO {self.table_name} ({fieldnames}) VALUES ({values});"
                print(f'$$ -- Create Test Item : query : {query}')
                data = ''
                SQConnect(query,data).ONE()    
        

class QueryOps(object):
    def __init__(self, debug=False):
        pass    

    def GetQuery(self, fields, tableName, whereField, whereValue):
        query = '''SELECT {}
                   FROM {}
                   WHERE {}=(?)'''.format(fields, tableName, whereField)
        data = [whereValue]
        returnd = SQConnect(query, data).ONE()
        return returnd

    def QueryCheck(self, fromTable, queryWhere=None, queryData=None, debug=False):
        if queryWhere == '' or queryWhere is None:
            
            query = 'SELECT count(*) FROM {0}'.format(fromTable)
            data = ''
            
        elif not re.search('(=|LIKE)', queryWhere) and queryWhere.count('?') == 0:
            query = '''SELECT count(*)
                       FROM {0}
                       WHERE {1}=(?)'''.format(fromTable, queryWhere)
            data = queryData
        else:
            
            query = '''SELECT count(*)
                    FROM {0}
                    WHERE {1}'''.format(fromTable, queryWhere)
            data = queryData
        
        VarOps().GetTyped(fromTable)
        returnd = SQConnect(query, data).ONE()
        
        if re.search('(list|tuple)', str(type(returnd)), re.I):
            returnd = VarOps().DeTupler(returnd)    
        
        return returnd

    def ANDSearch(self, whatField, items):

        cnt = items.count(' ')
        text = ''

        if cnt > 0:
            sp1 = items.split()
            if 'list' in str(type(whatField)):
                xx = 0
                longList = len(whatField) - 1
                for field in whatField:
                    if xx > 0:
                        text += ' OR '

                    for i in range(len(sp1)):
                        text += "{0} LIKE '%{1}%'".format(field, sp1[i])
                        if i < len(sp1) - 1:
                            text += ' AND '
                    xx += 1
            else:
                for i in range(len(sp1)):
                    text += "{0} LIKE '%{1}%'".format(whatField, sp1[i])
                    if i < len(sp1) - 1:
                        text += ' AND '

        else:
            if 'list' in str(type(whatField)):
                xx = 0
                for field in whatField:
                    if xx > 0:
                        text += ' OR '

                    text += "{0} LIKE '%{1}%'".format(field, items)
                    xx += 1
            else:
                text = "{0} LIKE '%{1}%'".format(whatField, items)
        print(("And Search Text : ",text))
        return text

    def CheckEntryExist(self, controlfield, ItemNumberd, table_list, debug=False):
        for table in table_list:
            queryWhere = "{0}".format(controlfield)
            queryData = (ItemNumberd,)
            countreturn = QueryOps().QueryCheck(table, queryWhere, queryData)
            
            added = False
            if countreturn == 0:
                added = True
                
                query = "INSERT INTO {0} ({1}) VALUES (?)".format(table,
                                                                controlfield)
                
                data = (ItemNumberd,)
                SQConnect(query, data).ONE()
            else:
                pass      

        return added



    def Commaize(self, list_of_tuples, typd='names'):
        idx = 0
        fieldSet = ''
        dataSet = []
        
        print(('CommaIze : {} : {}'.format(list_of_tuples, typd)))
        for name,table,field in list_of_tuples:
            if typd == 'names':
                value = wx.FindWindowByName(name).GetCtrl()
            if typd == 'vari':  
                value = name
            if value is None or value == '':
                value = None #continue
            if idx > 0:
                fieldSet += ', '
                
            fieldSet += '{}=(?)'.format(field)
            dataSet.append(value)
                
            idx += 1
            table = table
                
        # pout.v('Field Set : ',fieldSet)
        # pout.v('data Set : ',dataSet)
        # pout.v('table : ',table)
        return fieldSet, dataSet, table

    def CreditCheck(self, custNum=None, credit=False):
        print(('CheckCredit : {} \ {}'.format(custNum, credit)))
        if custNum is not None:
            query = 'SELECT freeze_charges FROM customer_accts_receivable WHERE cust_num=(?)'
            data = [custNum,]
            returnd = SQConnect(query,data).ONE()
        
            #print(('check Credit returnd : ',returnd))
        
            if returnd[0] == 1:
                credit = True
        
        return credit

    def CustPenaltyCheck(self, custNum):
        query = 'SELECT last_avail_credit FROM customer_penalty_info WHERE cust_num=(?)'
        data = [custNum,]
        returnd = SQConnect(query, data).ONE()
        limit = 0
        if returnd is not None and returnd > 0:
            limit = returnd[0]
            
        
        return limit
            
    def CheckCredit(self, custNum):
        query = 'SELECT credit_limit FROM customer_accts_receivable WHERE cust_num=(?)'
        data = [custNum,]
        returnd = SQConnect(query,data).ONE()
        climit = 0
        if returnd[0] is not None and returnd[0] > 0:
            climit = returnd[0]
        
        penalty_limit = CustPenaltyCheck(custNum)
        
        if penalty_limit is not None and penalty_limit > 0:
            climit = penalty_limit
        
        return climit    


    def DisplayLookupItemsinGrid(self, queryWhere, queryData, queryTable, debug=False):
            fields = 'upc,description,retails,quantity_on_hand'
            
            if not 'item_detailed' in queryTable:
                
                returnd = []
                query = '''SELECT upc
                        FROM {0}
                        WHERE {1}'''.format(queryTable, queryWhere)

                data = queryData
                returnd1 = SQConnect(query, data).ALL()
                
                for upcd in returnd1:
                    query = '''SELECT {0}
                            FROM {1}
                            WHERE upc=(?)'''.format(fields, 'item_detailed')
                    data = (upcd,)
                    returnd2 = SQConnect(query, data).ALL()

                    returnd.append(returnd2)
                    
            else:
                query = '''SELECT {0}
                        FROM {1}
                        WHERE {2}'''.format(fields, queryTable, queryWhere)
                data = queryData
                returnd = SQConnect(query, data).ALL()

            if len(returnd) > 0:
                grid = wx.FindWindowByName('itemLookup_display_grid')
                ClearCtrl(grid.GetName())
                AlterGrid(grid.GetName(), returnd)

                
                xx = 0
                
                for upc, description, retails, qoh in returnd:
                    for yy in range(grid.GetNumberCols()):
                        header = grid.GetColLabelValue(yy)
                        
                        if 'Item Number' in header:
                            grid.SetCellValue(xx, yy, str(upc))
                        if 'Item Description' in header:
                            grid.SetCellValue(xx, yy, str(description))
                        if 'Price' in header:
                            try:
                                retail_now = retails
                                retailPrice = retail_now['standard_price']['price']
                             
                                moneyd = RoundIt(retailPrice, '1.00')
                                
                                grid.SetCellValue(xx, yy, str(moneyd))
                            except:
                                grid.SetCellValue(xx, yy, '')
                        if 'OnHand' in header:
                            grid.SetCellValue(xx, yy, str(qoh))

                    xx += 1

                GridOps(grid.GetName()).GridAlternateColor(len(returnd))
                grid.Refresh()


    def GetItemLine(self, gridname,row):
        getList = ['Item Number','Description','Price','Quantity','Total','Disc','Tx']
        got = []
        for item in getList:
            x = GridOps(gridname).GetCell(item, row)
            got.append(x)
        
        return got
