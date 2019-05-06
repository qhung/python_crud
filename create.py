from cgi import parse_qs, escape
from urllib.parse import urlparse
import mysql.connector
import sys

url = urlparse('mysql://root:@localhost:3306/test')

def insert_data(name, email, freetext):
    conn = mysql.connector.connect(
        host = url.hostname or 'localhost',
        port = url.port or 3306,
        user = url.username or 'root',
        password = url.password or '',
        database = url.path[1:],
    )
    sql_insert_query = """ INSERT INTO `indival`(`name`, `email`, `text`, `created`, `modified`) VALUES 
    ('%(name)s', '%(email)s', '%(text)s', now(), now()) """ % {'name': name, 'email': email, 'text': freetext}
    
    cursor = conn.cursor()
    result  = cursor.execute(sql_insert_query)
    conn.commit()

    print('INSERT SUCCESS')

def application(environ, start_response):
    status = '200 OK'
    response_headers = [
        ('Content-Type', 'text/html')
    ]
    start_response(status, response_headers)

    create_form = '''<html><head>
        <title>Create</title>
        </head>
        <body>
        <form method="POST">
            <p>Name<input type="text" name="name"></p>
            <p>E-Mail<input type="text" name="email"></p>
            <p>Free Text<input type="text" name="text"></p>
            <p><input type="submit" value="Insert"></p>
        </form>
        </body>
    </html>
    '''

    # FormView
    output = create_form

    # Save Process
    if environ['REQUEST_METHOD'] == 'POST':
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0

        request_body = environ['wsgi.input'].read(request_body_size)
        d = parse_qs(request_body.decode('ascii'))

        # Get POST data
        name = d.get('name', [''])[0]
        email = d.get('email', [''])[0]
        freetext = d.get('text', [''])[0]

        # Save data
        insert_data(name, email, freetext)
    bytes(output, encoding= 'utf-8')
    return [output]