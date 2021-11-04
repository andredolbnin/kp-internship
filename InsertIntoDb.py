import psycopg2


host1 = '127.0.0.1'
user1 = 'postgres'
password1 = 'u1eqHONP0Jlj8AaZYXfK33Plx'
dbname1 = 'test'
port1 = '5433'


def DbInsert(records):
    try:    
        connection = psycopg2.connect(dbname = dbname1, user = user1, 
                                  password = password1, host = host1, port = port1)
    
        connection.autocommit = True
    
        cursor = connection.cursor()
    
        query = """INSERT INTO maintable (number, demand, solution, category1, category2, acts, count_inst)
                VALUES (%s, %s, %s, %s, %s, %s, %s);"""
     
        for record in records:
            cursor.execute(query, record)
    
    except Exception as ex:
        print('Error: ', ex)
    
    finally:
        if connection:
            cursor.close()
            connection.close()
 
    
    return None