from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
import random
import string
import datetime

app = Flask(__name__)
app.secret_key = "raf_team_mod_secure_admin_key_200"

# --- قواعد البيانات ---
RESELLERS_DB = {
    "RAX TEAM MOD 200": {
        "role": "admin",
        "balance": 99999
    },
    "dealer123": {
        "role": "reseller",
        "balance": 50
    }
}

# الأكواد مع دعم حد الأجهزة وحالة التفعيل (Active/Disabled)
KEYS_DB = {
    "RAF-9182-45A-89X": {
        "code": "RAF-9182-45A-89X",
        "expiresAt": datetime.datetime.now().timestamp() * 1000 + (24 * 3600 * 1000),
        "createdBy": "admin",
        "maxDevices": 1,
        "usedDevices": 0,
        "status": "ACTIVE"
    }
}

SETTINGS = {
    "maintenance": False
}

ENCRYPTED_SUBSCRIPTION_LINK = "happ://crypt5/fzvdLCFPPkolXTOUACtQwouK13ET9N6l96UaBoOYN8ptqH10oFWdbszJswnlLoCJPG2TkDRkE7yrl22hSZfib8+IPWmq4g1dBRAP+kW7Tc9M2faAGcL2x/vR31h8RmpGB96maWq2mBQH2J4EiWBO21qQmS36ZJpurgpbNB==6xcmpj3naGcw2BVZ1GbuZPpOrdIwywyYDQDnCVU+xwRQWES52JXaxdS31FC2eJKLtCnFBOk8cYbRNc5kgKYBX9uWhnxqhzgEgZ90SjYenldhKbZUPV+K/E4M9KlcI1FjJ3KiJbjCLSRDJXgGlGhfYrK91ygA9fa41X8beDUXFlBCSKtLjwPSxNWjNyrcfz54cgzp36V3c3z8IJMDKlthiyNQZ5R7K3KCEXuA0HcJrpuuKkwYgDnlDJlhKqC1W0aFJZILl2gcH6R/1radHmHNOcsPWNftTp/qdIesyByjw2c7+S50NGhFZOv0JkJe9ggd3cmaMg7rzy6QhxLfbPFAGCIX29wXr1LqzwB1l4jax/qM/w9pM8hyH+TgzCT1QuGHalX10NZUF5Bby1AdC6DAkavXUOkj61VepQU5Z8C9w73UB9DCZuHI0bF3qdfIaCegUwS0EC1Ld6Z6DMB8oFkJ5NyjCdj8G/WwS5OVpQnPXOTMEkJjtvlbmNE7PBcjKoz2keHgI6dFAHfjkkGszujOAPhMnWgxjsu47gIsDqiQpstDrPtN9A9nfynOOAN/XKsJLWCCFKRYbW7locsW10p+FHLpoqD8W2vANHp7JklkT5PkAwFRvMlva1jgwNaZs/R9sJZVUe5N9dDZr/gFiQ8K9G6k3On/h7BXYCXQbUWwfoI=ff"

INDEX_HTML = """<!DOCTYPE html>
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
.paste-link{color:var(--accent);cursor:pointer;display:flex;align-items:center;gap:4px;background:rgba(255,51,51,0.1);padding:4px 10px;border-radius:8px;border:1px solid rgba(255,51,51,0.2)}
.full-key-input{width:100%;background:#040407;border:1px solid #1f1f2e;border-radius:16px;padding:16px;color:#fff;font-size:14px;font-family:monospace;letter-spacing:1px;outline:none;text-align:center;margin-bottom:20px;transition:0.3s}
.full-key-input:focus{border-color:var(--accent);background:#0a0a12;box-shadow:0 0 15px var(--accent-glow)}
.activate-btn{width:100%;background:linear-gradient(135deg, #ff3333, #cc0000);color:#fff;border:none;border-radius:16px;padding:16px;font-size:15px;font-weight:900;cursor:pointer;letter-spacing:2px;box-shadow:0 8px 25px var(--accent-glow);transition:0.3s}
.activate-btn:active{transform:scale(0.98)}
.admin-link-btn{text-align:center;margin-top:15px;font-size:12px;color:var(--muted);cursor:pointer}
.admin-link-btn span{color:var(--accent);font-weight:bold}
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
            <span class="paste-link" onclick="pasteKey()">📋 PASTE</span>
        </div>

        <input type="text" id="codeIn" class="full-key-input" placeholder="RAF-####-###-###">

        <button class="activate-btn" onclick="verifyKey()">✓ ACTIVATE</button>

        <div class="admin-link-btn" onclick="openAdminLogin()">Admin & Reseller Access</div>
    </div>
</div>

<!-- PASSWORD LOGIN MODAL -->
<div id="adminLoginModal" class="hidden auth-wrapper">
    <div class="brand-logo-text">ACCESS PORTAL</div>
    <div class="card">
        <div class="section-header">
            <div class="icon-box">🛡️</div>
            <div class="redeem-title">Password Login</div>
        </div>
        <div class="redeem-desc">Enter your secure access password.</div>
        
        <input type="password" id="adminPass" class="full-key-input" placeholder="Enter Password">

        <button class="activate-btn" onclick="submitAdminLogin()">LOGIN</button>
        <div class="admin-link-btn" onclick="closeAdminLogin()">Back to Key Login</div>
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
  <div class="key-txt" id="activeKeyView">RAF-####-###-###</div>
  <div class="icon-btn" onclick="copyActiveKey()" title="Copy Key">📋</div>
</div>

<div class="info-grid">
  <div class="info-box"><div class="info-label">DEVICE</div><div class="info-val" id="deviceLimitView">1/1</div></div>
  <div class="info-box"><div class="info-label">STATUS</div><div class="info-val" style="color:#2ecc71;">ONLINE</div></div>
  <div class="info-box"><div class="info-label">EXPIRES</div><div class="info-val" id="expireDateText">-</div></div>
</div>

<button class="sub-btn" onclick="openHappVPN()">
  <div>
    <div>START RAX TEAM DEV</div>
    <div class="sub-subtxt">Launch Happ VPN Subscription</div>
  </div>
  <div class="arrow-icon">→</div>
</button>
</div>
</div>

</div>

<script>
let activeSubLink = null;
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

function openAdminLogin() {
    document.getElementById('loginPage').classList.add('hidden');
    document.getElementById('adminLoginModal').classList.remove('hidden');
}

function closeAdminLogin() {
    document.getElementById('adminLoginModal').classList.add('hidden');
    document.getElementById('loginPage').classList.remove('hidden');
}

async function submitAdminLogin() {
    let p = document.getElementById('adminPass').value;
    let res = await fetch('/api/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({password: p})
    });
    let data = await res.json();
    if(data.success) {
        window.location.href = '/dashboard';
    } else {
        alert(data.message);
    }
}

async function verifyKey() {
    let code = document.getElementById('codeIn').value.trim();
    if(!code) {
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
        activeSubLink = data.config;
        document.getElementById('activeKeyView').innerText = data.code;
        document.getElementById('deviceLimitView').innerText = data.usedDevices + "/" + data.maxDevices;
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
    if(!activeSubLink) {
        alert("Please activate your key first!");
        return;
    }
    navigator.clipboard.writeText(activeSubLink).then(() => {
        showToast("✓ Subscription Copied & Opening Happ VPN...");
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
    activeSubLink = null;
    document.getElementById('homePage').classList.add('hidden');
    document.getElementById('loginPage').classList.remove('hidden');
    document.getElementById('codeIn').value = "";
}
</script>
</body>
</html>
"""

ADMIN_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RAF MOD - Dashboard</title>
<style>
:root{--accent:#ff3333;--bg:#030305;--card-bg:#0a0a0e;--border:rgba(255,255,255,0.12);--text:#fff;--muted:#8888a0}
*{box-sizing:border-box;margin:0;padding:0;font-family:'Segoe UI', sans-serif}
body{background-color:var(--bg);color:var(--text);padding:20px;min-height:100vh}
.container{max-width:800px;margin:0 auto}
h1{color:var(--accent);margin-bottom:20px;text-align:center;letter-spacing:2px}
.card{background:var(--card-bg);border:1px solid var(--border);border-radius:16px;padding:20px;margin-bottom:20px}
.form-group{margin-bottom:15px}
label{display:block;font-size:12px;color:var(--muted);margin-bottom:6px;text-transform:uppercase}
input, select{width:100%;background:#040407;border:1px solid #1f1f2e;border-radius:10px;padding:12px;color:#fff;font-size:14px;outline:none}
button{background:linear-gradient(135deg, #ff3333, #cc0000);color:#fff;border:none;border-radius:10px;padding:12px 20px;font-weight:bold;cursor:pointer;width:100%;margin-top:5px}
table{width:100%;border-collapse:collapse;margin-top:15px}
th, td{padding:10px;text-align:left;border-bottom:1px solid rgba(255,255,255,0.08);font-size:13px}
th{color:var(--muted)}
.back-link{display:inline-block;margin-bottom:15px;color:var(--accent);text-decoration:none;font-weight:bold}
.generated-key-box { display: flex; align-items: center; justify-content: space-between; background: #040407; border: 1px solid var(--accent); border-radius: 12px; padding: 12px; margin-top: 15px; }
.generated-key-text { font-family: monospace; color: #fff; font-size: 15px; letter-spacing: 1px; }
.copy-btn-gen { background: rgba(255,51,51,0.2); border: 1px solid var(--accent); color: #fff; padding: 6px 14px; border-radius: 8px; font-size: 12px; cursor: pointer; width: auto; margin-top: 0; }
</style>
</head>
<body>
<div class="container">
    <a href="/" class="back-link">← Back to Portal</a>
    <h1>PORTAL DASHBOARD</h1>
    
    <div class="card">
        <h3>Generate New Key (RAF-####-###-###)</h3>
        <div class="form-group" style="margin-top:10px;">
            <label>Duration Value</label>
            <input type="number" id="durVal" value="24" min="1">
        </div>
        <div class="form-group">
            <label>Duration Type</label>
            <select id="durType">
                <option value="hours">Hours</option>
                <option value="days">Days</option>
            </select>
        </div>
        <div class="form-group">
            <label>Max Devices Allowed</label>
            <input type="number" id="maxDev" value="1" min="1">
        </div>
        <button onclick="generateKey()">Generate Key</button>
        
        <div id="resultCard" class="generated-key-box hidden">
            <span id="resultKey" class="generated-key-text">RAF-####-###-###</span>
            <button class="copy-btn-gen" onclick="copyGeneratedKey()">📋 COPY</button>
        </div>
    </div>

    {% if role == 'admin' %}
    <div class="card">
        <h3>Manage Reseller Passwords</h3>
        <div class="form-group" style="margin-top:10px;">
            <label>New Reseller Password</label>
            <input type="text" id="newResellerPass" placeholder="Enter password for new reseller">
        </div>
        <button onclick="addReseller()">Add Reseller Password</button>
        
        <table>
            <thead>
                <tr>
                    <th>Reseller Password</th>
                    <th>Role</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                {% for pwd, info in resellers.items() %}
                <tr>
                    <td><code>{{ pwd }}</code></td>
                    <td>{{ info.role }}</td>
                    <td>
                        {% if pwd != 'RAX TEAM MOD 200' %}
                        <button style="background:#333; padding:5px 10px; width:auto;" onclick="deleteReseller('{{ pwd }}')">Delete</button>
                        {% else %}
                        <span>Main Admin</span>
                        {% endif %}
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    {% endif %}

    <div class="card">
        <h3>Active Keys Overview & Control</h3>
        <table>
            <thead>
                <tr>
                    <th>Key</th>
                    <th>Devices</th>
                    <th>Status</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                {% for k, v in keys.items() %}
                <tr>
                    <td><code>{{ v.code }}</code></td>
                    <td>{{ v.usedDevices }}/{{ v.maxDevices }}</td>
                    <td style="color: {% if v.status == 'ACTIVE' %}#2ecc71{% else %}#ff3333{% endif %};">{{ v.status }}</td>
                    <td>
                        <button style="background:{% if v.status == 'ACTIVE' %}#cc0000{% else %}#2ecc71{% endif %}; padding:5px 10px; width:auto; font-size:11px;" onclick="toggleKeyStatus('{{ v.code }}')">
                            {% if v.status == 'ACTIVE' %}Disable{% else %}Enable{% endif %}
                        </button>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <div class="card">
        <a href="/logout" style="color:#ff3333; text-decoration:none; font-weight:bold; display:block; text-align:center;">LOGOUT</a>
    </div>
</div>

<script>
async function generateKey() {
    let val = document.getElementById('durVal').value;
    let type = document.getElementById('durType').value;
    let maxDev = document.getElementById('maxDev').value;
    let res = await fetch('/api/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({val: val, type: type, maxDevices: maxDev})
    });
    let data = await res.json();
    if(data.success) {
        document.getElementById('resultKey').innerText = data.code;
        document.getElementById('resultCard').classList.remove('hidden');
    } else {
        alert("Error");
    }
}

async function toggleKeyStatus(code) {
    let res = await fetch('/api/key/toggle', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({code: code})
    });
    let data = await res.json();
    if(data.success) {
        location.reload();
    } else {
        alert("Error updating status");
    }
}

function copyGeneratedKey() {
    let codeText = document.getElementById('resultKey').innerText;
    navigator.clipboard.writeText(codeText).then(() => {
        alert("✓ Key copied to clipboard!");
    });
}

async function addReseller() {
    let p = document.getElementById('newResellerPass').value.trim();
    if(!p) return alert("Enter password");
    let res = await fetch('/api/reseller/add', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({password: p})
    });
    let data = await res.json();
    if(data.success) {
        location.reload();
    } else {
        alert(data.message);
    }
}

async function deleteReseller(p) {
    let res = await fetch('/api/reseller/delete', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({password: p})
    });
    let data = await res.json();
    if(data.success) {
        location.reload();
    } else {
        alert(data.message);
    }
}
</script>
</body>
</html>
"""

@app.route('/')
def index():
    if SETTINGS["maintenance"] and session.get('role') != 'admin':
        return "<h1>Site under maintenance.</h1>"
    return render_template_string(INDEX_HTML)

@app.route('/api/verify', methods=['POST'])
def verify_key():
    data = request.get_json()
    code = data.get('code', '').strip().upper()
    if code in KEYS_DB:
        key_data = KEYS_DB[code]
        if key_data['status'] != 'ACTIVE':
            return jsonify({"success": False, "message": "Key is disabled by admin!"}), 400
        
        now = datetime.datetime.now().timestamp() * 1000
        if key_data['expiresAt'] < now:
            return jsonify({"success": False, "message": "Key has expired!"}), 400
        
        if key_data['usedDevices'] >= key_data['maxDevices']:
            return jsonify({"success": False, "message": "Device limit reached for this key!"}), 400
        
        # زيادة عداد الأجهزة المستخدمة عند التفعيل الناجح
        key_data['usedDevices'] += 1

        return jsonify({
            "success": True,
            "code": key_data['code'],
            "expiresAt": key_data['expiresAt'],
            "maxDevices": key_data['maxDevices'],
            "usedDevices": key_data['usedDevices'],
            "config": ENCRYPTED_SUBSCRIPTION_LINK
        })
    return jsonify({"success": False, "message": "Invalid license key!"}), 400

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    p = data.get('password', '').strip()
    if p in RESELLERS_DB:
        session['user_pass'] = p
        session['role'] = RESELLERS_DB[p]['role']
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Invalid password!"}), 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_pass' not in session:
        return redirect(url_for('index'))
    return render_template_string(ADMIN_HTML, keys=KEYS_DB, resellers=RESELLERS_DB, role=session.get('role'))

@app.route('/api/generate', methods=['POST'])
def generate_key():
    if 'user_pass' not in session:
        return jsonify({"success": False}), 401
    data = request.get_json()
    val = int(data.get('val', 1))
    dtype = data.get('type', 'hours')
    max_devices = int(data.get('maxDevices', 1))
    
    multiplier = 3600 * 1000 if dtype == 'hours' else 24 * 3600 * 1000
    expires_at = datetime.datetime.now().timestamp() * 1000 + (val * multiplier)
    
    p1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    p2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    p3 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    new_code = f"RAF-{p1}-{p2}-{p3}"
    
    KEYS_DB[new_code] = {
        "code": new_code,
        "expiresAt": expires_at,
        "createdBy": session.get('user_pass'),
        "maxDevices": max_devices,
        "usedDevices": 0,
        "status": "ACTIVE"
    }
    return jsonify({"success": True, "code": new_code})

@app.route('/api/key/toggle', methods=['POST'])
def toggle_key():
    if 'user_pass' not in session:
        return jsonify({"success": False}), 401
    data = request.get_json()
    code = data.get('code', '').strip().upper()
    if code in KEYS_DB:
        current_status = KEYS_DB[code]['status']
        KEYS_DB[code]['status'] = 'DISABLED' if current_status == 'ACTIVE' else 'ACTIVE'
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Key not found"})

@app.route('/api/reseller/add', methods=['POST'])
def add_reseller():
    if session.get('role') != 'admin':
        return jsonify({"success": False, "message": "Unauthorized"}), 403
    data = request.get_json()
    p = data.get('password', '').strip()
    if not p:
        return jsonify({"success": False, "message": "Password required"}), 400
    if p in RESELLERS_DB:
        return jsonify({"success": False, "message": "Password already exists"}), 400
    RESELLERS_DB[p] = {"role": "reseller", "balance": 50}
    return jsonify({"success": True})

@app.route('/api/reseller/delete', methods=['POST'])
def delete_reseller():
    if session.get('role') != 'admin':
        return jsonify({"success": False, "message": "Unauthorized"}), 403
    data = request.get_json()
    p = data.get('password', '').strip()
    if p == "RAX TEAM MOD 200":
        return jsonify({"success": False, "message": "Cannot delete main admin"})
    if p in RESELLERS_DB:
        del RESELLERS_DB[p]
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Not found"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
