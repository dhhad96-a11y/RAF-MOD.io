from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import random
import string
import datetime

app = Flask(__name__)
app.secret_key = "raf_team_mod_super_secure_key_200"

# --- قواعد البيانات المحلية (يمكن ربطها بـ Firebase لاحقاً إذا رغبت) ---
# حساب الأدمن الرئيسي
RESELLERS_DB = {
    "admin": {
        "password": "RAF TEAM MOD 200",
        "role": "admin",
        "balance": 99999
    }
}

# تخزين الأكواد
KEYS_DB = {
    "7391-RF-BSUW-XJSA": {
        "code": "7391-RF-BSUW-XJSA",
        "expiresAt": datetime.datetime.now().timestamp() * 1000 + (24 * 3600 * 1000),
        "createdBy": "admin",
        "status": "ACTIVE"
    }
}

# حالة الموقع (وضع الصيانة)
SETTINGS = {
    "maintenance": False
}

# كونفيغ RAX TEAM DEV المطلوب
RAX_CONFIG = [
    {
        "remarks": "RAX TEAM DEV",
        "inbounds": [
            {"listen": "127.0.0.1", "port": 10808, "protocol": "socks", "settings": {"auth": "noauth", "udp": True}, "sniffing": {"destOverride": ["http", "tls", "quic"], "enabled": True, "routeOnly": False}, "tag": "socks"},
            {"listen": "127.0.0.1", "port": 10809, "protocol": "http", "sniffing": {"destOverride": ["http", "tls", "quic"], "enabled": True, "routeOnly": False}, "tag": "http"}
        ],
        "outbounds": [
            {
                "protocol": "hysteria",
                "settings": {"address": "proxy-eu.dripwire.cc", "port": 443, "version": 2},
                "streamSettings": {
                    "hysteriaSettings": {"auth": "7850232467:292dbda85d7383fa", "version": 2},
                    "network": "hysteria",
                    "security": "tls",
                    "tlsSettings": {"alpn": ["h3"], "serverName": "proxy-eu.dripwire.cc", "show": False},
                    "finalmask": {"quicParams": {"disableChromeParrot": True}}
                },
                "tag": "proxy"
            },
            {"protocol": "freedom", "tag": "direct"}
        ],
        "routing": {
            "domainStrategy": "AsIs",
            "rules": [
                {"network": "tcp", "outboundTag": "proxy", "port": "39000-39999"},
                {"network": "udp", "outboundTag": "proxy", "port": "10000-10999"},
                {"network": "tcp,udp", "outboundTag": "direct"}
            ]
        }
    }
]

@app.route('/')
def index():
    if SETTINGS["maintenance"] and session.get('role') != 'admin':
        return "<h1>Site is under maintenance. Please try again later.</h1>"
    return render_template('index.html')

# --- التحقق من الكود ---
@app.route('/api/verify', methods=['POST'])
def verify_key():
    data = request.get_json()
    code = data.get('code', '').strip().upper()
    
    if code in KEYS_DB:
        key_data = KEYS_DB[code]
        now = datetime.datetime.now().timestamp() * 1000
        if key_data['expiresAt'] < now:
            return jsonify({"success": False, "message": "Key has expired!"}), 400
        return jsonify({
            "success": "SUCCESS",
            "code": key_data['code'],
            "expiresAt": key_data['expiresAt'],
            "config": RAX_CONFIG
        })
    return jsonify({"success": False, "message": "Invalid license key!"}), 400

# --- تسجيل دخول الأدمن / الموزعين ---
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    if username in RESELLERS_DB and RESELLERS_DB[username]['password'] == password:
        session['user'] = username
        session['role'] = RESELLERS_DB[username]['role']
        return jsonify({"success": True, "role": session['role']})
    
    return jsonify({"success": False, "message": "Invalid credentials!"}), 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# --- لوحة التحكم وإدارة الموزعين والأكواد ---
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('index'))
    return render_template('admin.html', user=session['user'], role=session['role'], keys=KEYS_DB, resellers=RESELLERS_DB, maintenance=SETTINGS["maintenance"])

# --- توليد أكواد جديدة (بالساعات والأيام وثبات 7391-RF-) ---
@app.route('/api/generate', methods=['POST'])
def generate_key():
    if 'user' not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401
        
    data = request.get_json()
    val = int(data.get('val', 1))
    dtype = data.get('type', 'hours') # hours or days
    
    multiplier = 3600 * 1000 if dtype == 'hours' else 24 * 3600 * 1000
    expires_at = datetime.datetime.now().timestamp() * 1000 + (val * multiplier)
    
    p1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    p2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    new_code = f"7391-RF-{p1}-{p2}"
    
    KEYS_DB[new_code] = {
        "code": new_code,
        "expiresAt": expires_at,
        "createdBy": session['user'],
        "status": "ACTIVE"
    }
    
    return jsonify({"success": True, "code": new_code})

# --- إضافة موزح جديد ---
@app.route('/api/reseller/add', methods=['POST'])
def add_reseller():
    if session.get('role') != 'admin':
        return jsonify({"success": False, "message": "Access denied"}), 403
    data = request.get_json()
    username = data.get('username').strip()
    password = data.get('password').strip()
    balance = int(data.get('balance', 10))
    
    if username in RESELLERS_DB:
        return jsonify({"success": False, "message": "Reseller already exists!"}), 400
        
    RESELLERS_DB[username] = {"password": password, "role": "reseller", "balance": balance}
    return jsonify({"success": True})

# --- حذف موزع ---
@app.route('/api/reseller/delete', methods=['POST'])
def delete_reseller():
    if session.get('role') != 'admin':
        return jsonify({"success": False, "message": "Access denied"}), 403
    data = request.get_json()
    username = data.get('username')
    if username in RESELLERS_DB and username != 'admin':
        del RESELLERS_DB[username]
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Cannot delete this user"})

# --- تعديل رصيد الموزع ---
@app.route('/api/reseller/balance', methods=['POST'])
def update_balance():
    if session.get('role') != 'admin':
        return jsonify({"success": False, "message": "Access denied"}), 403
    data = request.get_json()
    username = data.get('username')
    balance = int(data.get('balance', 0))
    if username in RESELLERS_DB:
        RESELLERS_DB[username]['balance'] = balance
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "User not found"})

# --- تبديل وضع الصيانة ---
@app.route('/api/maintenance', methods=['POST'])
def toggle_maintenance():
    if session.get('role') != 'admin':
        return jsonify({"success": False, "message": "Access denied"}), 403
    SETTINGS["maintenance"] = not SETTINGS["maintenance"]
    return jsonify({"success": True, "status": SETTINGS["maintenance"]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
