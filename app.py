from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)
app.secret_key = "raf_team_mod_secure_key"

# تخزين محلي آمن للأكواد
KEYS_DB = {
    "7391-RF-BSUW-XJSA": {
        "code": "7391-RF-BSUW-XJSA",
        "expiresAt": datetime.datetime.now().timestamp() * 1000 + (24 * 3600 * 1000),
        "status": "ACTIVE"
    }
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

# الواجهة كود HTML مباشر داخل البايثون لتجنب مشاكل المجلدات
HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>RAF MOD - Premium Gaming Portal</title>
<style>
:root{--accent:#ff3333;--accent-glow:rgba(255,51,51,0.35);--bg:#030305;--card-bg:rgba(10,10,14,0.95);--border:rgba(255,255,255,0.12);--text:#fff;--muted:#8888a0}
*{box-sizing:border-box;margin:0;padding:0;font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;-webkit-tap-highlight-color:transparent}
body{background-color:var(--bg);color:var(--text);min-height:100vh;display:flex;justify-content:center;align-items:center;padding:15px;overflow-x:hidden}
.container{width:100%;max-width:420px;position:relative}
.auth-wrapper{width:100%;display:flex;flex-direction:column;align-items:center}
.brand-logo-text{font-size:26px;font-weight:900;color:var(--accent);letter-spacing:3px;margin-bottom:25px;text-align:center;text-shadow:0 0 20px var(--accent-glow)}
.card{background:var(--card-bg);border:1px solid var(--border);border-radius:28px;padding:30px 22px;margin-bottom:15px;box-shadow:0 0 50px rgba(0,0,0,0.8);backdrop-filter:blur(20px);width:100%}
.section-header{display:flex;align-items:center;gap:12px;margin-bottom:8px}
.icon-box{width:36px;height:36px;background:rgba(255,51,51,0.1);border:1px solid rgba(255,51,51,0.3);border-radius:10px;display:flex;align-items:center;justify-content:center;color:var(--accent);font-size:16px}
.redeem-title{font-size:18px;font-weight:900;color:#fff;letter-spacing:1px}
.redeem-desc{font-size:12px;color:var(--muted);margin-bottom:22px;line-height:1.4}
.input-label-row{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;font-size:11px;font-weight:bold;color:var(--muted);letter-spacing:1.5px;text-transform:uppercase}
.paste-link{color:var(--accent);cursor:pointer;display:flex;align-items:center;gap:4px}
.full-key-input{width:100%;background:#040407;border:1px solid #1f1f2e;border-radius:16px;padding:16px;color:#fff;font-size:14px;font-family:monospace;letter-spacing:1px;outline:none;text-align:center;margin-bottom:20px;transition:0.3s}
.full-key-input:focus{border-color:var(--accent);background:#0a0a12;box-shadow:0 0 15px var(--accent-glow)}
.activate-btn{width:100%;background:linear-gradient(135deg, #ff3333, #cc0000);color:#fff;border:none;border-radius:16px;padding:16px;font-size:15px;font-weight:900;cursor:pointer;letter-spacing:2px;box-shadow:0 8px 25px var(--accent-glow);transition:0.3s}
.activate-btn:active{transform:scale(0.98)}
.top-bar{display:flex;justify-content:space-between;align-items:center;margin-bottom:15px}
.app-title{font-weight:900;font-size:16px;letter-spacing:1px}
.logout-btn{background:rgba(255,255,255,0.06);color:#fff;border:1px solid rgba(255,255,255,0.1);border-radius:8px;padding:6px 12px;font-size:11px;font-weight:bold;cursor:pointer}
.timer-circle-box{text-align:center;padding:15px 0;position:relative}
.circle-ring{width:210px;height:210px;border:2px dashed rgba(255,51,51,0.3);border-radius:50%;margin:0 auto;display:flex;flex-direction:column;align-items:center;justify-content:center;position:relative;background:radial-gradient(circle, rgba(255,51,51,0.03) 0%, transparent 70%);box-shadow:0 0 40px rgba(255,51,51,0.08)}
.client-name-txt{font-size:12px;letter-spacing:2px;color:var(--accent);font-weight:800;margin-bottom:6px}
.main-client-txt{font-size:16px;font-weight:900;letter-spacing:2px;margin-bottom:12px}
.countdown-txt{font-size:22px;font-weight:900;letter-spacing:1px;color:#fff}
.countdown-txt span{font-size:10px;color:var(--muted);margin:0 2px}
.info-grid{display:grid;grid-template-columns:repeat(3, 1fr);gap:8px;margin-top:15px}
.info-box{background:#040407;border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:10px 5px;text-align:center}
.info-label{font-size:9px;color:var(--muted);letter-spacing:1px;margin-bottom:4px}
.info-val{font-size:11px;font-weight:bold;color:#fff}
.key-row{background:#040407;border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:10px;display:flex;align-items:center;justify-content:space-between;margin-top:8px}
.key-txt{font-size:11px;color:var(--muted);letter-spacing:1px}
.icon-btn{background:#11111a;border:1px solid rgba(255,255,255,0.1);color:#fff;border-radius:8px;width:30px;height:30px;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:12px}
.sub-btn{width:100%;background:linear-gradient(135deg, #ff3333, #cc0000);color:#fff;border:none;border-radius:14px;padding:16px 20px;font-weight:900;font-size:14px;display:flex;justify-content:space-between;align-items:center;cursor:pointer;margin-top:12px;box-shadow:0 6px 20px var(--accent-glow)}
.sub-subtxt{font-size:10px;color:rgba(255,255,255,0.7);font-weight:normal;margin-top:2px}
.arrow-icon{background:rgba(255,255,255,0.2);width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:13px}
.hidden{display:none!important}
#toast { position: fixed; left: 50%; bottom: 30px; transform: translate(-50%, 20px); background: #07070e; border: 1px solid var(--accent); color: #fff; padding: 12px 26px; border-radius: 999px; font-weight: bold; font-size: 13px; opacity: 0; pointer-events: none; transition: 0.3s; z-index: 6000; box-shadow: 0 0 30px var(--accent-glow); }
#toast.show { opacity: 1; transform: translate(-50%, 0); }
</style>
</head>
<body>
<div id="toast">✓ Success!</div>
<div class="container">

<!-- LOGIN PAGE -->
<div id="loginPage" class="auth-wrapper">
    <div class="brand-logo-text">RAF MOD</div>
    <div class="card">
        <div class="section-header">
            <div class="icon-box">🔑</div>
            <div class="redeem-title">Redeem Key</div>
        </div>
        <div class="redeem-desc">Enter your license key to activate your access.</div>

        <div class="input-label-row">
            <span>License Key</span>
            <span class="paste-link" onclick="pasteKey()">📋 Paste</span>
        </div>

        <input type="text" id="codeIn" class="full-key-input" value="7391-RF-">

        <button class="activate-btn" onclick="verifyKey()">✓ ACTIVATE</button>
    </div>
</div>

<!-- DASHBOARD PAGE -->
<div id="homePage" class="hidden auth-wrapper" style="width:100%;">
<div class="card" style="width:100%;">
<div class="top-bar">
  <div class="app-title">RAF MOD CLIENT</div>
  <button class="logout-btn" onclick="doLogout()">LOGOUT</button>
</div>

<div class="timer-circle-box">
  <div class="circle-ring">
    <div class="client-name-txt">RAX TEAM DEV</div>
    <div class="main-client-txt">GAMING CLIENT</div>
    <div id="timerDisplay" class="countdown-txt">00<span>H</span> 00<span>M</span> 00<span>S</span></div>
  </div>
</div>

<div class="key-row">
  <div class="key-txt" id="activeKeyView">7391-RF-XXXX-XXXX</div>
  <div class="icon-btn" onclick="copyActiveKey()" title="Copy Key">📋</div>
</div>

<div class="info-grid">
  <div class="info-box"><div class="info-label">DEVICE</div><div class="info-val">1/1</div></div>
  <div class="info-box"><div class="info-label">STATUS</div><div class="info-val" style="color:#2ecc71;">ONLINE</div></div>
  <div class="info-box"><div class="info-label">EXPIRES</div><div class="info-val" id="expireDateText">-</div></div>
</div>

<button class="sub-btn" onclick="openHappVPN()">
  <div>
    <div>START RAX TEAM DEV</div>
    <div class="sub-subtxt">Launch Happ VPN Directly</div>
  </div>
  <div class="arrow-icon">→</div>
</button>
</div>
</div>

</div>

<script>
let activeConfigData = null;
let timerInterval = null;

function showToast(msg) {
    let t = document.getElementById('toast');
    t.innerText = msg;
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 3000);
}

function pasteKey() {
    navigator.clipboard.readText().then(text => {
        document.getElementById('codeIn').value = text.trim();
        showToast("✓ Pasted successfully!");
    }).catch(() => {
        showToast("❌ Paste failed.");
    });
}

async function verifyKey() {
    let code = document.getElementById('codeIn').value.trim();
    if(!code || code === "7391-RF-") {
        alert("Please enter a valid key!");
        return;
    }
    
    let res = await fetch('/api/verify', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({code: code})
    });
    let data = await res.json();
    
    if(data.success) {
        activeConfigData = data.config;
        document.getElementById('activeKeyView').innerText = data.code;
        document.getElementById('expireDateText').innerText = new Date(data.expiresAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        document.getElementById('loginPage').classList.add('hidden');
        document.getElementById('homePage').classList.remove('hidden');
        
        startTimer(data.expiresAt);
        openHappVPN();
    } else {
        alert(data.message);
    }
}

function openHappVPN() {
    if(!activeConfigData) {
        alert("Please activate your key first!");
        return;
    }
    let jsonString = JSON.stringify(activeConfigData, null, 4);
    navigator.clipboard.writeText(jsonString).then(() => {
        showToast("✓ Config loaded & opening Happ VPN...");
        setTimeout(() => {
            window.location.href = "happ://";
        }, 500);
    }).catch(() => {
        window.location.href = "happ://";
    });
}

function startTimer(expTime) {
    if(timerInterval) clearInterval(timerInterval);
    function update() {
        let diff = expTime - new Date().getTime();
        if(diff <= 0) {
            document.getElementById('timerDisplay').innerText = 'EXPIRED';
            clearInterval(timerInterval);
            alert("Subscription expired!");
            doLogout();
            return;
        }
        let h = Math.floor(diff / 3600000);
        let m = Math.floor((diff % 3600000) / 60000);
        let s = Math.floor((diff % 60000) / 1000);
        document.getElementById('timerDisplay').innerHTML = String(h).padStart(2,'0') + '<span>H</span> ' + String(m).padStart(2,'0') + '<span>M</span> ' + String(s).padStart(2,'0') + '<span>S</span>';
    }
    update();
    timerInterval = setInterval(update, 1000);
}

function copyActiveKey() {
    navigator.clipboard.writeText(document.getElementById('activeKeyView').innerText);
    showToast("✓ Key copied!");
}

function doLogout() {
    if(timerInterval) clearInterval(timerInterval);
    activeConfigData = null;
    document.getElementById('homePage').classList.add('hidden');
    document.getElementById('loginPage').classList.remove('hidden');
    document.getElementById('codeIn').value = "7391-RF-";
}
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return HTML_CONTENT

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
            "success": True, 
            "code": key_data['code'],
            "expiresAt": key_data['expiresAt'],
            "config": RAX_CONFIG
        })
    return jsonify({"success": False, "message": "Invalid license key!"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
