import pout
import re
import json
import sqlite3
import time
from pathlib import Path


class DBConnect(object):
    def __init__(self, query, data=None, sql_file=None):
        self.query = query
        self.data = data
        self.sql_file = sql_file
        if sql_file is None:
            tablename = re.sub('^.+FROM.([a-zA-Z]+)', '\\1', query)
            self.sql_file = GetSQLFile(tablename).Get()

        self.START()
        
    def START(self):
        self.con = sqlite3.connect(self.sql_file)        
        self.cur = self.con.cursor()
        if len(self.data) > 0:
            self.cur.execute(self.query, self.data)
        else:
            self.cur.execute(self.query)
    
    def END(self):
        if re.search('(UPDATE|INSERT)', self.query, re.I):
            self.con.commit()
    
        self.con.close()

    def ALL(self):
        item = self.cur.fetchall()
        self.END()
        return item
        
    def ONE(self):
        item = self.cur.fetchone()
        self.END()
        return item
        

class GetSQLFile(object):
    def __init__(self, tblname):
        self.tblname = tblname
        self.sqlfile = './db/SUPPORT.sql'
        
    def Get(self):
        q = 'SELECT sql_file FROM tableSupport WHERE table_name=?'
        d = (self.tblname,)
        r = DBConnect(q, d, self.sqlfile).ONE()
        
        if 'tuple' in str(type(r)):
            r = r[0]

        return r

class SQConnect(object):
    def __init__(self, query, data=None, sql_file=None, dbtype='sqlite3', debug=False):
        self.dbtype = dbtype
        self.query = None
        self.data = None
        self.sql_file = sql_file
        pout.v(self.sql_file)
        if sql_file is None:
            tablename = re.sub('^.+FROM.([a-zA-Z]+)', '\\1', query)
            self.sql_file = GetSQLFile(tablename).Get()

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
            con = fdb.connect(host='localhost', database=f'{self.sql_file}', user='rhp', password='password')
        if self.dbtype == 'sqlite3':
            con = sqlite3.connect(self.sql_file)
            # con.row_factory = sqlite3.Row
        
        cur = con.cursor()
        if len(self.data) > 0:
            cur.execute(self.query, self.data)
        else:
            cur.execute(self.query)
            
        returnd = cur.fetchall()
        # if self.dbtype == 'sqlite3':
        #     returnd = [{k: item[k] for k in item.keys()} for item in returnd]
        
        if re.search('(UPDATE|INSERT)', self.query, re.I):
            con.commit()

        con.close()

        return returnd

    def ONE(self):
        if self.dbtype == 'mysql':
            con = pymysql.connect(host='localhost', user='rhp', passwd='password', db='rhp')
        if self.dbtype == 'fdb':
            con = fdb.connect(host='localhost', database=f'{self.sql_file}', user='rhp', password='password')
        if self.dbtype == 'sqlite3':
            pout.v(self.sql_file)
            con = sqlite3.connect(self.sql_file)
            # con.row_factory = sqlite3.Row
        
        cur = con.cursor()
        if len(self.data) > 0:
            cur.execute(self.query, self.data)
        else:
            cur.execute(self.query)
    
        returnd = cur.fetchone()
        pout.v(returnd)
        print(returnd[0])
        pout.b('--')
        # if self.dbtype == 'sqlite3':
        #     returnd = [{k: item[k] for k in item.keys()} for item in returnd]
        
        if re.search('(UPDATE|INSERT)', self.query, re.I):
            con.commit()
        
        con.close()

        return returnd

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
        sql_file = './db/SUPPORT.sql'
        prefix = './db/'
        query = "SELECT sql_file FROM tableSupport WHERE table_names=(?)"
        data = (tableName,)
        returnd = SQConnect(query, data, sql_file).ONE()
        
        filed = prefix + returnd[0]
        if os.path.isfile(filed):
            return filed
        else:
            
            print(('--- table Name : {0} ---'.format(tableName)))


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
        pout.v(fromTable)
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
        
        #VarOps().GetTyped(fromTable)

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


class LookupDB(object):
    def __init__(self, table, sql_file=None, dbtype='sqlite3', debug=False):
        self.table = table
        self.dbtype = dbtype
        self.sql_file = self.GetSQLFile(sql_file)
        
    def GetSQLFile(self, sql_file):
        supportSQLFile = './db/SUPPORT.sql'
        item = sql_file
        if sql_file is None:
            query = '''SELECT sql_file 
                       FROM tableSupport 
                       WHERE table_name=?'''
            data = [self.table,]
            returnd = DBConnect(query, data, supportSQLFile).ONE()
            #pout.v(f'GetSQLFILE : {returnd}')
            item = returnd[0]
        return item

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
        returnd = DBConnect(query, data, self.sql_file).ALL()
        return returnd
        
    def Specific(self, whereValue, whereField, selectFields, limit=None):
        limitd = self.Limit(limit)
        query = '''SELECT {}
                   FROM {}
                   WHERE {}=(?)
                   {}'''.format(selectFields, self.table, whereField, limitd)
        
        data = [whereValue,]
        returnd = DBConnect(query, data, sql_file=self.sql_file).ALL()
        
        #pout.v('Specific : {} ; Query : {} ; Data : {}'.format(returnd, query, data))
        #ty = self.Typed(returnd)
        #pout.v(f'Typed : {ty}')
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
        #pout.v(f'Where : {query}\n Data : {data}')
        returnd = DBConnect(query, data, sql_file=self.sql_file).ONE()
        # if len(returnd) == 0:
        #     returnd = (None,)

        #pout.v(f'Count : {returnd}')
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
        returnd = DBConnect(query, data, sql_file=self.sql_file).ALL()
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
        returnd = DBConnect(query, data, sql_file=self.sql_file).ALL()
        
        return returnd[0]

    def DescribeTable(self):
        if self.dbtype == 'mysql':
            query = '''SELECT * FROM information_schema.COLUMNS 
                    WHERE TABLE_SCHEMA = 'rhp' 
                    AND TABLE_NAME = "{}"
                    AND COLUMN_NAME = "{}"'''.format(self.table)
        if self.dbtype == 'sqlite3':
            query = '.schema {}'.format(self.table)

        data = []
        returnd = DBConnect(query, data, sql_file=self.sql_file).ALL()
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
        pout.v(self.dbtype)
        if self.dbtype == 'mysql':
            query = '''SELECT * FROM information_schema.COLUMNS 
                    WHERE TABLE_SCHEMA = 'rhp' 
                    AND TABLE_NAME = "{}"
                    '''.format(self.table)
        
        if self.dbtype == 'sqlite3':
            query = '.schema {}'.format(self.table)

        data = []
        returnd = DBConnect(query, data, sql_file=self.sql_file).ALL()
        
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
        returnd = DBConnect(query, data, sql_file=self.sql_file).ONE()
        pout.v(query)
        return returnd

