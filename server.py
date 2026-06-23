import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

DB_FILE = os.path.join(os.path.dirname(__file__), 'db.json')

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE) as f:
            return json.load(f)
    return {'bets': [], 'txns': []}

def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/betting-tracker.html'
        if self.path == '/api/data':
            body = json.dumps(load_db()).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', len(body))
            self.end_headers()
            self.wfile.write(body)
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/api/data':
            length = int(self.headers.get('Content-Length', 0))
            data = json.loads(self.rfile.read(length))
            save_db(data)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"ok":true}')

    def log_message(self, format, *args):
        pass  # silence request logs

if __name__ == '__main__':
    port = 8080
    print(f'Betting tracker → http://localhost:{port}')
    HTTPServer(('localhost', port), Handler).serve_forever()
