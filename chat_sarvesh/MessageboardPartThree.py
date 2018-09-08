#!/usr/bin/env python3
#
# An HTTP server that's a message board.

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

memory = []

form = '''<!DOCTYPE html>
  <title>User Board</title>
    <p style="color:black; font-size:40px;color:red;margin-left:20%;">
    Welcome User &nbsp; let's do chat (lass uns chatten) ? </p>
        <form method="POST" style="margin-left:35%;margin-top:30px;">
            <textarea name="message" style="color:green;font-size:40px;"></textarea>
            <br>
            <button type="submit" style="color:red;margin-left:200px;margin-top:15px;font-size:20px;">Click It</button>
  </form>
  <pre style="margin-left:100px;">
 
{}
  </pre>
'''


class MessageHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-length', 0))
        data = self.rfile.read(length).decode()
        message = parse_qs(data)["message"][0]
        message = message.replace("Karthik", "Sarvesh")
        memory.append(message)
        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        mesg = form.format("\n".join(memory))
        self.wfile.write(mesg.encode())


if __name__ == '__main__':
    server_address = ('', 8081)
    httpd = HTTPServer(server_address, MessageHandler)
    httpd.serve_forever()
