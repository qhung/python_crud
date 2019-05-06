# -*- coding: utf-8 -*-
from urllib.parse import urlparse
import mysql.connector
import sys

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

def application(environ, start_response):
    status = '200 OK'
    resources = get_data()
    
    header = ('ID', '名前', 'email', '自由入力欄', '作成日', '変更日', '操作')

    output = "";
    output += "<html lang='ja'>"
    output += "<meta http-equiv='X-UA-Compatible' content='IE=edge'>"
    output += "<head>"
    output += "<meta charset='utf-8'>"
    output += "</head>"
    output += "<body>"
    output += "<a href='create.py'>作成</a>"
    output += "<table border=1>"
    output += "<tr>"
    for menu in header:
        output = output + "<th>" + str(menu) + "</th>"

    output += "</tr>"
    
    for data in resources:
        output += "<tr>"
        output += "<td><a href='edit.py?id=" + str(data[0]) + "'>" + str(data[0]) + "</a></td>"
        output += "<td>" + str(data[1]) + "</td>"
        output += "<td>" + str(data[2]) + "</td>"
        output += "<td>" + str(data[3]) + "</td>"
        output += "<td>" + str(data[4]) + "</td>"
        output += "<td>" + str(data[5]) + "</td>"
        output += "<td><a href='delete.py?id=" + str(data[0]) + "'>削除</a></td>"
        output += "</tr>"

    output += "</body>"
    output += '</table>'

    response_headers = [('Content-type', 'text/html')]
    # ('Content-Length', str(len(output)))]

    start_response(status, response_headers)

    output = bytes(output, encoding= 'utf-8')
    return [output]

