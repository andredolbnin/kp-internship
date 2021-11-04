import psycopg2


host1 = '127.0.0.1'
user1 = 'postgres'
password1 = 'u1eqHONP0Jlj8AaZYXfK33Plx'
dbname1 = 'test'
port1 = '5433'


def start():
    try:    
        connection = psycopg2.connect(dbname = dbname1, user = user1, 
                                  password = password1, host = host1, port = port1)
    
        connection.autocommit = True
    
        cursor = connection.cursor()
    
        cursor.execute(
            """DELETE FROM smalltable"""    
        )
        
        cursor.execute(
            """INSERT INTO smalltable (number, solution, demand, category1, category2, acts, solution_id, cat1_id, cat2_id, count_inst)
            SELECT number, solution, demand, category1, category2, acts, NULL, NULL, NULL, count_inst
            FROM maintable
            WHERE NOT demand = 'Не определено'"""
        )
    
    except Exception as ex:
        print('Error: ', ex)
    
    finally:
        if connection:
            cursor.close()
            connection.close()
            
    return None


def get_solution(n):  
    try:    
        connection = psycopg2.connect(dbname = dbname1, user = user1, 
                                  password = password1, host = host1, port = port1)
    
        #connection.autocommit = True
    
        cursor = connection.cursor()
    
        query = """SELECT solution FROM smalltable WHERE number = %s;"""    
        
        cursor.execute(query, [n])
        
        r = cursor.fetchall()
    
    except Exception as ex:
        print('Error: ', ex)
    
    finally:
        if connection:
            cursor.close()
            connection.close()
            
    return r[0][0]


def get_cat_1():
    r = []
    
    try:    
        connection = psycopg2.connect(dbname = dbname1, user = user1, 
                                  password = password1, host = host1, port = port1)
    
        #connection.autocommit = True
    
        cursor = connection.cursor()
    
        cursor.execute(
            """SELECT category1 FROM smalltable"""    
        )
        
        f = cursor.fetchall()
        for item in f:
            r.append(item[0])
    
    except Exception as ex:
        print('Error: ', ex)
    
    finally:
        if connection:
            cursor.close()
            connection.close()
            
    return set(r)


def get_cat_2(cat_1):
    r = []
    
    try:    
        connection = psycopg2.connect(dbname = dbname1, user = user1, 
                                  password = password1, host = host1, port = port1)
    
        cursor = connection.cursor()
        
        query = """SELECT category2 FROM smalltable WHERE category1 = %s;"""
    
        cursor.execute(query, [cat_1])
        
        f = cursor.fetchall()
        for item in f:
            r.append(item[0])
    
    except Exception as ex:
        print('Error: ', ex)
    
    finally:
        if connection:
            cursor.close()
            connection.close()
            
    return set(r)


def get_cat_3(cat_2):
    r = []
    
    try:    
        connection = psycopg2.connect(dbname = dbname1, user = user1, 
                                  password = password1, host = host1, port = port1)
    
        cursor = connection.cursor()
        
        query = """SELECT demand FROM smalltable WHERE category2 = %s;"""
    
        cursor.execute(query, [cat_2])
        
        f = cursor.fetchall()
        for item in f:
            r.append(item[0])
    
    except Exception as ex:
        print('Error: ', ex)
    
    finally:
        if connection:
            cursor.close()
            connection.close()
            
    return set(r)


def get_numbers(d):
    r = []
    
    try:    
        connection = psycopg2.connect(dbname = dbname1, user = user1, 
                                  password = password1, host = host1, port = port1)
    
        cursor = connection.cursor()
        
        query = """SELECT number FROM smalltable WHERE demand = %s;"""
    
        cursor.execute(query, [d])   
        
        f = cursor.fetchall()
        for item in f:
            r.append(item[0])
    
    except Exception as ex:
        print('Error: ', ex)
    
    finally:
        if connection:
            cursor.close()
            connection.close()
            
    return r


def get_acts(n):
    
    try:    
        connection = psycopg2.connect(dbname = dbname1, user = user1, 
                                  password = password1, host = host1, port = port1)
    
        cursor = connection.cursor()
        
        query = """SELECT acts FROM smalltable WHERE number = %s;"""
    
        cursor.execute(query, [n]) 
        
        r = cursor.fetchall()
    
    except Exception as ex:
        print('Error: ', ex)
    
    finally:
        if connection:
            cursor.close()
            connection.close()
            
    return r[0][0]