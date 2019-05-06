# -*- coding: utf-8 -*-
from urllib.parse import urlparse
import mysql.connector
import sys
import urllib
#import requests

url = urlparse('mysql://root:@localhost:3306/test')

def get_data():
    conn = mysql.connector.connect(
        host = url.hostname or 'localhost',
        port = url.port or 3306,
        user = url.username or 'root',
        password = url.password or '',
        database = url.path[1:],
    )
    cur = conn.cursor()
    cur.execute('SELECT * FROM indival')
    return cur.fetchall()

def get_detail(id):
    conn = mysql.connector.connect(
        host = url.hostname or 'localhost',
        port = url.port or 3306,
        user = url.username or 'root',
        password = url.password or '',
        database = url.path[1:],
    )
    cur = conn.cursor()
    cur.execute('SELECT * FROM indival where id = ' + id)

    return cur.fetchall()


def application(environ, start_response):
    targetid = urllib.parse.parse_qs(environ.get('QUERY_STRING'))['id']
    status = '200 OK'
    print(targetid[0])
    resources = get_detail(targetid[0])

    print(resources)    
    header = ('ID', '名前', 'email', '自由入力欄', '作成日', '変更日')

    output = ""
    output += "<html lang='ja'>"
    output += "<meta http-equiv='X-UA-Compatible' content='IE=edge'>"
    output += "<head>"
    output += "<meta charset='utf-8'>"
    output += "</head>"
    output += "<body>"
    output += "<a href='/'>TOP</a>"
    output += "<form action='update.py' method='post'>"
    output += "<table border=1>"
    output += "<tr>"
    for menu in header:
        output += "<th>" + str(menu) + "</th>"

    output += "</tr>"
    for data in resources:
        output += "<tr>"
        output += "<td>" + str(data[0]) + "</td>"
        output += "<td>" + str(data[1]) + "</td>"
        output += "<td>" + str(data[2]) + "</td>"
        output += "<td><input type='text' name='free' value='" + str(data[3]) + "' /></td>"
        output += "<td>" + str(data[4]) + "</td>"
        output += "<td>" + str(data[5]) + "</td>"
        output += "</tr>"

    output += "</table>"
    output += "<input type='submit' value='UPDATE'>"
    output += "</form>"
    output += "asssssss"
    output += "</body>"

    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(output)))]

    start_response(status, response_headers)

    output = bytes(output, encoding= 'utf-8')
    return [output, "asdf"]

