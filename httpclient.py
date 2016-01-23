#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib
from urlparse import urlparse

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPRequest(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'Socket created'

        #Connect to remote server
        s.connect((host , port))
        return s

    def get_code(self, data):
        return data.split()[1]

    def get_headers(self,data):
        return data.split("\r\n\r\n")[0]

    def get_body(self, data):
        return data.split("\r\n\r\n")[1]

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
        code = 500
        body = ""
        return HTTPRequest(code, body)

    def POST(self, url, args=None):
        # Get the host and port from url
        # https://docs.python.org/2/library/urlparse.html 2016-01-23
        host, port, path = self.parse_url(url);

        if args != None:
            data = urllib.urlencode(args)
            content_length = str(len(data))
        else:
            data = ""
            content_length = str(0)

        sock = self.connect(host, port)

        try:
            # print 'Sending HEADERS...'
            sock.sendall("POST " + path + " HTTP/1.1\r\n".encode("UTF8"))
            sock.sendall("Host: " + host+":"+str(port)+"\r\n".encode("UTF8"))
            sock.sendall("Content-Type: application/x-www-form-urlencoded\r\n".encode("UTF8"))
            sock.sendall("Content-Length: "+content_length+"\r\n".encode("UTF8"))
            sock.sendall("Connection: close\r\n\r\n".encode("UTF8"))

            if data != "":
                # print 'Sending BODY...'
                sock.sendall(data+"\r\n\r\n".encode("UTF8"))

        except socket.error:
            #Send failed
            print 'Send failed'
            return None

        #Now recieve data
        reply = self.recvall(sock)
        print(reply)

        sock.close()

        code = self.get_code(reply)
        body = self.get_body(reply)
        headers = self.get_headers(reply)
        # print "\nHTTP POST REQUEST RESULT:\n"
        # print reply.split("\r\n\r\n")
        # print "CODE: "+code
        # print "HEADERS: "+headers
        # print "BODY: "+body
        # print
        return HTTPRequest(code, body)


    def parse_url(self, url):
        # obtain following information: hostname, port, path
        url_parse = urlparse(url)
        host_name = url_parse.hostname
        path = url_parse.path
        port = url_parse.port

        if port == None:
            port = 8080

        return host_name, port, path

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[1], sys.argv[2] )
    else:
        print client.command( command, sys.argv[1] )    
