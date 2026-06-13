from flask import Flask, render_template_string, jsonify
import subprocess
import json

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>KernelMind - Monitor IA</title>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
        }
        .metric-value {
            font-size: 48px;
            font-weight: bold;
            margin: 10px 0;
        }
        .suggestions {
            background: #f5f5f5;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
        button {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin: 5px;
        }
        button:hover {
            background: #45a049;
        }
        .status {
            position: fixed;
            bottom: 10px;
            right: 10px;
            background: #333;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 KernelMind - Monitoramento Ético do Sistema</h1>
        
        <div class="metrics" id="metrics">
            <div class="metric-card">
                <h3>CPU</h3>
                <div class="metric-value" id="cpu">-</div>
                <div id="cpu_detail">Carregando...</div>
            </div>
            <div class="metric-card">
                <h3>RAM</h3>
                <div class="metric-value" id="ram">-</div>
                <div id="ram_detail">Carregando...</div>
            </div>
            <div class="metric-card">
                <h3>DISCO</h3>
                <div class="metric-value" id="disk">-</div>
                <div id="disk_detail">Carregando...</div>
            </div>
        </div>
        
        <div class="suggestions">
            <h3>💡 Sugestões da IA</h3>
            <div id="suggestions">Aguardando dados...</div>
        </div>
        
        <div style="text-align: center; margin-top: 20px;">
            <button onclick="refresh()">🔄 Atualizar Agora</button>
            <button onclick="optimizeRAM()">⚡ Otimizar RAM</button>
            <button onclick="showEthics()">📜 Ver Log Ético</button>
        </div>
    </div>
    <div class="status" id="status">✅ EthicsLock: ATIVO</div>
    
    <script>
        async function refresh() {
            const response = await fetch('/api/snapshot');
            const data = await response.json();
            
            document.getElementById('cpu').innerHTML = data.cpu.percent + '%';
            document.getElementById('cpu_detail').innerHTML = `Núcleos: ${data.cpu.count}`;
            
            document.getElementById('ram').innerHTML = data.memory.percent + '%';
            document.getElementById('ram_detail').innerHTML = `${data.memory.used_gb}GB / ${data.memory.total_gb}GB`;
            
            document.getElementById('disk').innerHTML = data.disk.percent + '%';
            document.getElementById('disk_detail').innerHTML = `Livre: ${data.disk.free_gb}GB`;
            
            const suggestions = await fetch('/api/suggestions');
            const suggestions_text = await suggestions.text();
            document.getElementById('suggestions').innerHTML = suggestions_text.replace(/\n/g, '<br>');
        }
        
        async function optimizeRAM() {
            if(confirm('EthicsLock: Permitir otimização de RAM?')) {
                const response = await fetch('/api/optimize_ram', {method: 'POST'});
                const result = await response.text();
                alert(result);
                refresh();
            }
        }
        
        async function showEthics() {
            const response = await fetch('/api/ethics_log');
            const log = await response.text();
            alert('Log Ético:\n\n' + log);
        }
        
        setInterval(refresh, 5000);
        refresh();
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/snapshot')
def snapshot():
    cmd = "cd ~/kernelmind && km snapshot --json"
    result = subprocess.run(['wsl', 'bash', '-c', cmd], 
                          capture_output=True, text=True)
    if result.stdout:
        return jsonify(json.loads(result.stdout))
    return jsonify({'error': 'Erro ao obter dados'})

@app.route('/api/suggestions')
def suggestions():
    cmd = "cd ~/kernelmind && km memory"
    result = subprocess.run(['wsl', 'bash', '-c', cmd], 
                          capture_output=True, text=True)
    return result.stdout

@app.route('/api/optimize_ram', methods=['POST'])
def optimize_ram():
    cmd = "cd ~/kernelmind && km memory --optimize"
    result = subprocess.run(['wsl', 'bash', '-c', cmd], 
                          capture_output=True, text=True)
    return result.stdout

@app.route('/api/ethics_log')
def ethics_log():
    cmd = "cd ~/kernelmind && km ethics --log"
    result = subprocess.run(['wsl', 'bash', '-c', cmd], 
                          capture_output=True, text=True)
    return result.stdout

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
