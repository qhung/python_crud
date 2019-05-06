from cgi import parse_qs, escape
from urllib.parse import urlparse
import mysql.connector
import sys

url = urlparse('mysql://root:@localhost:3306/test')

def delete_data(id):
    conn = mysql.connector.connect(
        host = url.hostname or 'localhost',
        port = url.port or 3306,
        user = url.username or 'root',
        password = url.password or '',
        database = url.path[1:],
    )

    sql_insert_query = """ DELETE FROM `indival` WHERE id = '%(id)s'""" %{'id': id}

    cursor = conn.cursor()
    result  = cursor.execute(sql_insert_query)
    conn.commit()
    
    print('DELETED SUCCESS')

def application(environ, start_response):
    status = '200 OK'
    response_headers = [
        ('Content-Type', 'text/html')
    ]
    start_response(status, response_headers)
    
    if environ['REQUEST_METHOD'] == 'GET':
        d = parse_qs(environ['QUERY_STRING'])

        userid = d.get('id',[''])[0]
        
        delete_data(userid)

    output = """<p>DELETED SUCCESS</p>"""
    bytes(output, encoding= 'utf-8')
    return [output]
        
