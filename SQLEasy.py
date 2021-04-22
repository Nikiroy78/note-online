import sqlite3


class SQLiteEasyException(Exception):
    pass


def compareKey(DBlist, key, type_of_key=lambda x: x, hideIndex=True):
    if not(type(DBlist) is list):
        raise SQLiteEasyException(f"function compareKey need List object, unsupported type: {type(DBlist)}")
    
    if len(DBlist) > 0:
        if key not in DBlist[0]:
            raise SQLiteEasyException(f"key '{key}' not founded.")
    DB_Dictonary = dict()
    for BD in sorted(DBlist, key=lambda List: List[key]):
        comparedBD = dict()
        for Key in BD:
            if not(Key == key) and hideIndex:
                comparedBD[Key] = BD[Key]
            elif not hideIndex:
                comparedBD[Key] = BD[Key]
        DB_Dictonary[type_of_key(BD[key])] = comparedBD
    
    return DB_Dictonary


def autoselectID_fromNew_item(DATABASE, TABLE, ID_KEY):
    TABLE_DATA = DATABASE.getBase(TABLE)
    TABLE_DATA = compareKey(TABLE_DATA, ID_KEY)
    TABLE_DATA = [ID for ID in TABLE_DATA]
    INDEX = 0
    for DATA_INDEX in TABLE_DATA:
        if INDEX == DATA_INDEX:
            INDEX += 1
        else:
            return INDEX
    return INDEX


class database:
    def dict_factory(self, cursor, row):
        dictDB = {}
        for idx, col in enumerate(cursor.description):
            dictDB[col[0]] = row[idx]
        return dictDB
    
    def encodeSQLiteType(self, objectum, all_as_str=False):
        if type(objectum) is str:
            return "'%s'" % objectum.replace("'", "[SQLEasy_symbol:&#39;]")
        elif objectum is None and all_as_str:
            return "''"
        elif objectum is None:
            return 'NULL'
        elif type(objectum) is bool and objectum and all_as_str:
            return "'TRUE'"
        elif type(objectum) is bool and objectum:
            return 'TRUE'
        elif type(objectum) is bool and not(objectum) and all_as_str:
            return "'FALSE'"
        elif type(objectum) is bool and not(objectum):
            return 'FALSE'
        elif all_as_str and True in [type(objectum) is int, type(objectum) is float]:
            return "'%s'" % objectum
        elif not(all_as_str) and True in [type(objectum) is int, type(objectum) is float]:
            return objectum
        else:
            raise SQLiteEasyException(f"Unsupported type: {type(objectum)}")
    
    def __init__(self, PATH, DatabaseName=None):
        self.ConnectedFile = sqlite3.connect(PATH, check_same_thread=False)
        self.databaseChoosed = DatabaseName
        self.ConnectedFile.row_factory = self.dict_factory
        self.act_commit = True
    
    def toggleCommit(self, value=None):
        if value in (False, True):
            self.act_commit = value
        else:
            if self.act_commit:
                self.act_commit = False
            else:
                self.act_commit = True
    
    def commit(self):
        self.ConnectedFile.commit()

    def getBase(self, DatabaseName=None, elementsFromDB='*'):
        elementsFromDB = str(elementsFromDB)
        if DatabaseName is None and self.databaseChoosed is None:
            raise SQLiteEasyException("Database is not choosed")
        elif DatabaseName is None and not(self.databaseChoosed is None):
            dbCursore = self.ConnectedFile.cursor()
            dbCursore.execute(f"select {elementsFromDB} from {self.databaseChoosed}")
            result = dbCursore.fetchall()
        else:
            dbCursore = self.ConnectedFile.cursor()
            dbCursore.execute(f"select {elementsFromDB} from {DatabaseName}")
            self.databaseChoosed = DatabaseName
            result = dbCursore.fetchall()
        
        for rowID in range(len(result)):
            row = result[rowID]
            for cellKey in row:
                if type(row[cellKey]) is str:
                    result[rowID][cellKey] = row[cellKey].replace('[SQLEasy_symbol:&#39;]', "'")
        return result

    def pop(self, key, value, DatabaseName=None):
        if type(value) is str:
            # value = f"'%s'" % value.replace('\'', '\\\'')
            value = f"'%s'" % value.replace("'", '[SQLEasy_symbol:&#39;]')
        if DatabaseName is None and not(self.databaseChoosed is None):
            DatabaseName = self.databaseChoosed
        elif DatabaseName is None:
            raise SQLiteEasyException("Database is not choosed")
        dbCursore = self.ConnectedFile.cursor()
        dbCursore.execute('DELETE FROM %s\n\nWHERE %s == %s;' % (DatabaseName, key, value))
        if self.act_commit:
            self.ConnectedFile.commit()

    def setItem(self, key, newValue, indexKey, value, DatabaseName=None):
        newValue = self.encodeSQLiteType(newValue)
        value = self.encodeSQLiteType(value)
        if DatabaseName is None and not(self.databaseChoosed is None):
            DatabaseName = self.databaseChoosed
        elif DatabaseName is None:
            raise SQLiteEasyException("Database is not choosed")
        dbCursore = self.ConnectedFile.cursor()
        if value is None:
            dbCursore.execute('UPDATE %s SET %s = %s WHERE %s is NULL;' % (DatabaseName, key, newValue, indexKey))
        else:
            dbCursore.execute('UPDATE %s SET %s = %s WHERE %s = %s;' % (DatabaseName, key, newValue, indexKey, value))
        if self.act_commit:
            self.ConnectedFile.commit()
    
    def add(self, values, DatabaseName=None):
        if DatabaseName is None and not(self.databaseChoosed is None):
            DatabaseName = self.databaseChoosed
        elif DatabaseName is None:
            raise SQLiteEasyException("Database is not choosed")
        if DatabaseName is None and not(self.databaseChoosed is None):
            DatabaseName = self.databaseChoosed
        elif DatabaseName is None:
            raise SQLiteEasyException("Database is not choosed")
        
        keys = [str(key) for key in values]
        values = [self.encodeSQLiteType(values[key], all_as_str=True) for key in values]
        
        dbCursore = self.ConnectedFile.cursor()
        try:
            dbCursore.execute('INSERT INTO %s (%s) VALUES (%s)' % (DatabaseName, ', '.join(keys), ', '.join(values)))
        except:
            dbCursore.execute('INSERT OR IGNORE INTO %s (%s) VALUES (%s)' % (DatabaseName, ', '.join(keys), ', '.join(values)))
        if self.act_commit:
            self.ConnectedFile.commit()
    
    def uploadFiles(self, binary, DatabaseName=None):  # Uwaga! Может работать с ошибками.
        if not(type(binary) is bytes or type(binary) is bytearray):
            raise SQLiteEasyException('You can upload only byte or bytearray types!!')
        dbCursore = self.ConnectedFile.cursor()
        binary = sqlite3.Binary(binary)
        
        if DatabaseName is None and not(self.databaseChoosed is None):
            DatabaseName = self.databaseChoosed
        elif DatabaseName is None:
            raise SQLiteEasyException("Database is not choosed")
        if DatabaseName is None and not(self.databaseChoosed is None):
            DatabaseName = self.databaseChoosed
        elif DatabaseName is None:
            raise SQLiteEasyException("Database is not choosed")
        # (!) Дописать
        
    def chooseDataBase(self, DatabaseName):
        self.getBase(DatabaseName)
        self.databaseChoosed = DatabaseName

    def currentIndex(self, key, value, DatabaseName=None):
        if DatabaseName is None and not(self.databaseChoosed is None):
            DatabaseName = self.databaseChoosed
        elif DatabaseName is None:
            raise SQLiteEasyException("Database is not choosed")
        
        DB = self.getBase(DatabaseName)
        
        ID = 0
        for Dictonary in sorted(DB, key=lambda dictonary: dictonary[key]):
            if Dictonary[key] == value:
                return ID
            ID += 1
    
    def currentValue(self, key, value, DatabaseName=None):
        if DatabaseName is None and not(self.databaseChoosed is None):
            DatabaseName = self.databaseChoosed
        elif DatabaseName is None:
            raise SQLiteEasyException("Database is not choosed")
        
        DB = self.getBase(DatabaseName)
        
        for Dictonary in sorted(DB, key=lambda dictonary: dictonary[key]):
            if Dictonary[key] == value:
                return Dictonary
    
    def createColumn(self, columnName, tableName, DatabaseName=None):
        return  # (!) Не реализовано!!
    
    def getTables(self):
        dbCursore = self.ConnectedFile.cursor()
        dbCursore.execute('SELECT name from sqlite_master where type= "table"')
        return [item['name'] for item in dbCursore.fetchall()]
    
    def getDict(self):
        dictonary = dict()
        tables = self.getTables()
        for table in tables:
            dictonary[table] = self.getBase(table)
        return dictonary
    
    def execute(self, req):
        dbCursore = self.ConnectedFile.cursor()
        dbCursore.execute(req)
        if self.act_commit:
            self.ConnectedFile.commit()
        return dbCursore.fetchall()


def formingTable(dictonary, path):
    pass  # В разработке