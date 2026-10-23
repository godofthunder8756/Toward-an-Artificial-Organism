import http.server,urllib.parse,sys
PAGE=b"""<html><body><h3>Save Astra response</h3><form method=POST action=/save><textarea name=t rows=30 cols=120></textarea><br><button type=submit>Save</button></form></body></html>"""
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(s):
        s.send_response(200);s.send_header('Content-Type','text/html');s.end_headers();s.wfile.write(PAGE)
    def do_POST(s):
        n=int(s.headers['Content-Length']);d=urllib.parse.parse_qs(s.rfile.read(n).decode())
        t=d.get('t',[''])[0]
        open(sys.argv[1],'w').write(t)
        s.send_response(200);s.end_headers();s.wfile.write(f"SAVED {len(t)} chars".encode())
http.server.HTTPServer(('127.0.0.1',int(sys.argv[2])),H).serve_forever()
