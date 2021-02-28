import pout
import re
import json
import pymysql
import time


class SQConnect(object):
    def __init__(self, query, data=None, sql_file=None, debug=False):
        
        self.query = None
        self.data = None
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
        con = pymysql.connect(host='localhost', user='rhp', passwd='password', db='rhp')
        try:
            with con.cursor() as cur:
                if len(self.data) > 0:
                    cur.execute(self.query, self.data)
                else:
                    cur.execute(self.query)
                    
                returnd = cur.fetchall()
                if re.search('(UPDATE|INSERT)', self.query, re.I):
                    con.commit()
        finally:
            con.close()

        return self.CheckJson(returnd)

    def ONE(self):
        con = pymysql.connect(host='localhost', user='rhp', passwd='password', db='rhp')
        try: 
            with con.cursor() as cur:
                #cur = con #. cursor()
                if len(self.data) > 0:
                    cur.execute(self.query, self.data)
                else:
                    cur.execute(self.query)
            
                returnd = cur.fetchone()
                if re.search('(UPDATE|INSERT)', self.query, re.I):
                    con.commit()
        finally:
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
    
     
    

class LookupDB(object):
    def __init__(self, table, debug=False):
        self.table = table
        
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
        returnd = SQConnect(query, data).ALL()
        return returnd
        
    def Specific(self, whereValue, whereField, selectFields, limit=None):
        limitd = self.Limit(limit)
        query = '''SELECT {}
                   FROM {}
                   WHERE {}=(?)
                   {}'''.format(selectFields, self.table, whereField, limitd)
        
        data = [whereValue,]
        returnd = SQConnect(query, data).ALL()
        
        pout.v('Specific : {} ; Query : {} ; Data : {}'.format(returnd, query, data))
        ty = self.Typed(returnd)
        pout.v(f'Typed : {ty}')
        return ty
       
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
        returnd = SQConnect(query, data).ONE()
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
        returnd = SQConnect(query, data).ALL()
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
        returnd = SQConnect(query, data).ALL()
        
        return returnd[0]

    def DescribeTable(self):
        # try:
        query = '''SELECT * FROM information_schema.COLUMNS 
                   WHERE TABLE_SCHEMA = 'rhp' 
                   AND TABLE_NAME = "{}"
                   AND COLUMN_NAME = "{}"'''.format(self.table)
        data = []
        returnd = SQConnect(query, data).ALL()
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
        try:
            returnd = SQConnect(query, data).ALL()
        except ProgrammingError as e:
            print('Table does not exist')
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
        returnd = SQConnect(query, data).ONE()
        pout.v(query)
        return returnd


class TableAware(object):
    def __init__(self, table_name, sql_file=None, dbtype='mysql'):
        self.table_name = table_name
        self.sql_file = sql_file
        self.dbtype = dbtype.lower()
        self.table_list = None
    
    def CheckTable(self):
        print(f'** Table Check : {self.table_name} : ')
        returnd = LookupDB(self.table_name).is_table()
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
            returnd = LookupDB(self.table_name).is_field(fieldname)
            addcolumn = False
            if returnd is None:
                addcolumn = True
            
            return addcolumn
    
    def CompareField(self, fieldname, defn):
        pout.b('Compare Field')
        self.table_list = LookupDB(self.table_name).DescribeTable()
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
        returnd = SQConnect(query, data).ONE()

    
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

    def AddField(self, fieldname, char=None, varchar=None, integer=None, text=None, date=None, bool=None, time=None, decimal=None, primary_key=False, defaults=None):
        addTable = self.CheckTable()
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
        
