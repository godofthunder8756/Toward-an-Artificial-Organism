import http.server,urllib.parse,os
SEND='/workspace/astra_serve37/send'; OUT='/workspace/astra_consult37_response.txt'
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(s):
        p=s.path.strip('/')
        if p=='' or p=='index':
            n=len(os.listdir(SEND)); b=''.join('<p><a href="/c37_%d.txt">part %d</a></p>'%(i,i) for i in range(1,n+1))+'<p><a href="/save">save reply</a></p>'
            s._r(b,'text/html')
        elif p=='save':
            s._r('<form method=post action=/save><textarea name=t rows=30 cols=100></textarea><br><button type=submit>Save</button></form>','text/html')
        elif os.path.exists(os.path.join(SEND,p)):
            s._r(open(os.path.join(SEND,p)).read(),'text/plain; charset=utf-8')
        else: s.send_response(404); s.end_headers()
    def do_POST(s):
        l=int(s.headers['Content-Length']); d=urllib.parse.parse_qs(s.rfile.read(l).decode())
        t=d.get('t',[''])[0]; open(OUT,'w').write(t)
        s._r('SAVED %d chars'%len(t),'text/plain')
    def _r(s,b,ct):
        b=b.encode(); s.send_response(200); s.send_header('Content-Type',ct); s.send_header('Content-Length',str(len(b))); s.end_headers(); s.wfile.write(b)
http.server.ThreadingHTTPServer(('127.0.0.1',8837),H).serve_forever()
