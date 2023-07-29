from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import cgi

class FileUploadHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = """
            <html>
            <head>
                <title>File Upload</title>
            </head>
            <body>
                <h1>File Upload</h1>
                <form action="/upload" method="post" enctype="multipart/form-data">
                    <input type="file" name="file" />
                    <input type="submit" value="Upload" />
                </form>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write("Not Found".encode('utf-8'))

    def do_POST(self):
        if self.path == '/upload':
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type']}
            )

            if 'file' not in form:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("Bad Request: File data missing.".encode('utf-8'))
                return

            file_item = form['file']
            if not file_item.file:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("Bad Request: File data missing.".encode('utf-8'))
                return

            filename = os.path.basename(file_item.filename)
            with open(filename, 'wb') as f:
                while True:
                    chunk = file_item.file.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("File uploaded successfully.".encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write("Not Found".encode('utf-8'))


def run_server(server_class=HTTPServer, handler_class=FileUploadHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {port}...")
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
