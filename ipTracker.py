from flask import Flask, request, redirect
import datetime

app = Flask(__name__)

LOG_FILE = 'ip_logs.txt'

@app.route('/')
def home():
    return "Rastreador de IPs. Usa /generate para generar un nuevo enlace de registro."
@app.route('/generate')
def generate():
    unique_id = "track"
    tracking_link = f"http://127.0.0.1:5000/{unique_id}"
    return f"Tu enlace rastreable es : {tracking_link}"
@app.route('/track')
def track():
    ip_adress = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    timestamp = datetime.datetime.now().isoformat()

    with open(LOG_FILE, 'a') as f:
        f.write(f"{ip_adress},{user_agent},{timestamp}\n")
    return redirect('https://youtube.com')
if __name__ == '__main__':
    app.run(debug=True)