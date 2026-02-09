from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Sorftime MCP配置
MCP_URL = "https://mcp.sorftime.com"
ACCOUNT_SK = "q1nqb0nlm3zzt1rsy1joqlvzovzyut09"

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "service": "Sorftime MCP Bridge",
        "status": "running"
    })

@app.route('/call-mcp', methods=['POST'])
def call_mcp():
    try:
        data = request.json or {}
        action = data.get('action', 'query')
        params = data.get('params', {})
        
        mcp_request = {
            "key": ACCOUNT_SK,
            "action": action,
            "params": params
        }
        
        response = requests.post(
            f"{MCP_URL}?key=account-sk",
            json=mcp_request,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        return jsonify({
            "success": True,
            "data": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
