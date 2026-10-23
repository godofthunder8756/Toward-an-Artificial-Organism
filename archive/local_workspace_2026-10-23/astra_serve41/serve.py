import http.server,urllib.parse,os,threading
SEND='/workspace/astra_serve41/send'; OUT='/workspace/astra_consult41_response.txt'
N=len(os.listdir(SEND))
class P(http.server.BaseHTTPRequestHandler):
    def do_GET(s):
        p=s.path.strip('/')
        if p in('','index'):
            s._r(''.join('<p><a href="/c41_%d.txt">part %d</a></p>'%(i,i) for i in range(1,N+1))+'<p>Save page: http://127.0.0.1:8841/save</p>','text/html')
        elif p.startswith('c41_') and os.path.exists(os.path.join(SEND,p)): s._r(open(os.path.join(SEND,p)).read(),'text/plain; charset=utf-8')
        else: s.send_response(404); s.end_headers()
    def _r(s,b,ct):
        b=b.encode(); s.send_response(200); s.send_header('Content-Type',ct); s.send_header('Content-Length',str(len(b))); s.end_headers(); s.wfile.write(b)
class S(P):
    def do_GET(s):
        s._r('<form method=post action=/save><textarea name=t rows=30 cols=100></textarea><br><button type=submit>Save</button></form>','text/html')
    def do_POST(s):
        l=int(s.headers['Content-Length']); d=urllib.parse.parse_qs(s.rfile.read(l).decode())
        t=d.get('t',[''])[0]; open(OUT,'w').write(t)
        s._r('SAVED %d chars'%len(t),'text/plain')
a=http.server.ThreadingHTTPServer(('127.0.0.1',8840),P); b=http.server.ThreadingHTTPServer(('127.0.0.1',8841),S)
threading.Thread(target=b.serve_forever,daemon=True).start(); a.serve_forever()
