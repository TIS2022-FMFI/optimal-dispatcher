import psycopg2 as db

conn = None
cur = None

try:
    conn = db.connect(
            host = '',
            dbname = '',
            user = '',
            password = '',
            port = 5432
        )
        
    cur = conn.cursor() 
    delete_old_trasportations = '''
        DELETE FROM transport_management_transportations WHERE departure_time < NOW() - INTERVAL '14 DAY';
    '''
    cur.execute(delete_old_trasportations)
    conn.commit()
except db.OperationalError as error_msg:
    print(error_msg)
finally:
    if cur is not None: cur.close()
    if conn is not None: conn.close()
