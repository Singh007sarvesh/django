import http.server
import requests
from urllib.parse import unquote, parse_qs
import cgi
import MySQLdb
from http import cookies

memory = {}

form = '''<!DOCTYPE html>
<head>
    <title>Login</title>
</head>
<body>
<h1 style="margin-left:40%;margin-top:20px;">Login User</h1>
<form method="POST" style="margin-top:100px;margin-left:33%;">
    
        <input style="width: 300px;" type="text" name ="user"   placeholder="Enter User Name" maxlength="25" required>
   
    <br>
    <br>
    <br>
        <input  type="password" name ="pass"   placeholder="Enter Password" required style="width: 300px;">
   
    <br>
    <input style="color:red;margin-left:22%;font-size:25px;margin-top:20px;" type="submit" name="sub" value="Login">
</form>
</body>
'''

detail = '''<!DOCTYPE html>
<head>
    <title>User Details</title>
</head>
<body>
    <h1 style="margin-left:40%;margin-top:20px;">User Details</h1>
    <table style="margin-left:300px;">
        <tr style="margin-left:80px;">
            <th style="margin-left:80px;font-size:20px">Firstname</th>
            <th style="margin-left:80px;font-size:20px">LastName</th>
            <th style="margin-left:80px;font-size:20px">Aadhar ID</th>
            <th style="margin-left:80px;font-size:20px">Gender</th>
            <th style="margin-left:80px;font-size:20px">Email ID</th>
        </tr>
        {}
    </table>
</body>
'''
users = []
def readdata():
    conn = MySQLdb.connect("localhost","root","","test")
    sql = conn.cursor();
    sql.execute("SELECT * FROM emp_records ")
    for row in sql.fetchall():
        list=(row[0], row[1], row[3], row[4], row[5])
        users.append(list)
def logincheck(user):
    conn = MySQLdb.connect("localhost","root","","test" )
    sql=conn.cursor();
    sql.execute("SELECT * FROM emp_records where username='{}'".format(user))   
    for row in sql.fetchall():
        if row[6]:
            return True
    return False
def login(user, password):
    conn = MySQLdb.connect("localhost","root","","test" )
    sql=conn.cursor();
    sql.execute("SELECT * FROM emp_records where username='{}' and password='{}'".format(user,password))   
    for row in sql.fetchall():
        if row[6] and row[7]:
            return True
    return False


class Shortener(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-length', 0))
        body = self.rfile.read(length).decode()
        params = parse_qs(body)
        user = params["user"][0]
        password = params["pass"][0]
        check = login(user, password)
        if(check):
            #self.wfile.write("Login successful".encode())
            #self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.send_response(303)
            self.send_header('Location','/detail')
            c = cookies.SimpleCookie()
            c['_user'] = user
            c['_user']['domain'] = 'localhost'
            c['_user']['max-age'] = 10000
            self.send_header('Set-Cookie', c['_user'].OutputString())
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write('Enter valid user id and password'.encode())

    def do_GET(self):
        name = unquote(self.path[1:])
        #is_valid=False
        def validUser():
            cookie_header = self.headers.get('Cookie')
            is_valid = False
            if cookie_header:
                cookie=cookies.SimpleCookie()
                cookie.load(cookie_header)
                if cookie['_user']:
                    is_valid=logincheck(cookie['_user'].value)
            if is_valid:
                return True
            else:
                return False
                
        if name:
            if (name == "detail"):
                if validUser():
                    self.send_response(200)
                    self.send_header('Location', '/detail')
                    self.end_headers()
                    name = "\n".join("<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(row[0],row[1],row[2],row[3],row[4])
                                  for row in users)
                    self.wfile.write(detail.format(name).encode())
                    
                else:
                    self.send_response(404)
                    self.send_header('Content-type', 'text/plain; charset=utf-8')
                    self.end_headers()
                    self.wfile.write("Login plz".encode())
            elif (name == 'form'):
                
                self.send_response(200)
                self.send_header('Location', '/form')
                self.end_headers()
                self.wfile.write(form.encode())

            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write("I don't know '{}'.".format(name).encode())
        else:
            self.send_response(200)
            self.send_header('Location', '/')
            self.end_headers()
            known = "\n".join("{} : {}".format(key, memory[key])
                              for key in sorted(memory.keys()))
            self.wfile.write(form.format(known).encode())
            


if __name__ == '__main__':
    server_address = ('', 8092)
    readdata()
    httpd = http.server.HTTPServer(server_address, Shortener)
    httpd.serve_forever()
