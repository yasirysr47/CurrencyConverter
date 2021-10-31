#!/usr/bin/python3
import cgi
from io import BytesIO
import pdb
from CurrencyConverter import CurrencyConverter
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, unquote



hostName = "localhost"
serverPort = 8000

class WebServerHandle(BaseHTTPRequestHandler):
    def exchange_currency(self, data):
        currrent_symbol = data.get("current_currency",[''])[0].upper()
        target_symbol = data.get("target_currency",[''])[0].upper()
        value = float(data.get("value",[''])[0])
        exchange_value = CurrencyConverter().exchange_currency(currrent_symbol, target_symbol, value)
        print(exchange_value)
        output = "The amount of {} {} is {} {} as of today".format(value, currrent_symbol, exchange_value, target_symbol)
        self.wfile.write(bytes(output, "utf-8"))

    def do_GET(self):
        try:
            if self.path.startswith("/convert?"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                query = urlparse(self.path).query
                multipart_data = dict()
                for k, v in [qc.split("=") for qc in query.split("&")]:
                    multipart_data[k] = [v]
                print(self.path)
                self.exchange_currency(multipart_data)

            elif self.path.startswith("/convert"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><head><style>body {font-family: Helvetica, Arial; color: #333}</style></head>"
                output += "<body><h2>Welcome to Exchange Rate Conversion</h2>"
                output += """<form method="POST" enctype="multipart/form-data" action="/convert">
                <h4> Please enter the Data below</h4>
                <label for="cars">Currrent Currency : </label>
                <select name="current_currency" id="current_currency">
                    <option value="USD">USD</option>
                    <option value="EUR">EUR</option>
                    <option value="JPY">JPY</option>
                </select>
                <br><br>
                <label for="cars">Target Currency : </label>
                <select name="target_currency" id="target_currency">
                    <option value="USD">USD</option>
                    <option value="EUR">EUR</option>
                    <option value="JPY">JPY</option>
                </select>
                <br><br>
                Amount : <input name="value" type="text" id="value" /><br>
                <input type="submit" value="Submit" />"""
                output += "</form></html></body>"
                self.wfile.write(bytes(output, "utf-8"))
                return
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><head><style>body {font-family: Helvetica, Arial; color: #333}</style></head>"
                output += "<body><h3>Welcome to currency converter</h3>"
                output += "Click the below link for currency exchange <br>"
                output += "<a href='http://localhost:8000/convert' > Start Converting </a>"
                output += "</html></body>"
                self.wfile.write(bytes(output, "utf-8"))
                return
        except IOError:
            self.send_error(404, 'Invalid Input!! Please enter correct data: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.startswith("/convert"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                ctype, pdict = cgi.parse_header(self.headers['content-type'])
                pdict['CONTENT-LENGTH'] = int(self.headers['Content-Length'])
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                multipart_data = cgi.parse_multipart(self.rfile, pdict)
                print(multipart_data)
                self.exchange_currency(multipart_data)

        except:
            self.send_error(404, 'Invalid Input!! Please enter correct data')

def main():
    try:
        server = HTTPServer((hostName, serverPort), WebServerHandle)
        print("Starting web server on the port 8000..")
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C entered. Shutting down the server..')
        server.socket.close()

if __name__ == '__main__':
    main()