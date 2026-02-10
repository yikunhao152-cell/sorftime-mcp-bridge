from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Sorftime MCP配置
MCP_URL = "https://mcp.sorftime.com"

# 【修改点1】这里替换成了你图片里最新的 Key (zvjwuezgq1dbl1fvm0zxrjhqz3ljut09)
ACCOUNT_SK = os.environ.get("ACCOUNT_SK", "zvjwuezgq1dbl1fvm0zxrjhqz3ljut09") 

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
        
        # 【修改点2】注意看这里！原本是 key=account-sk (这是错的)，
        # 现在改成了 key={ACCOUNT_SK}，这样才能把你上面的真 Key 传进去。
        response = requests.post(
            f"{MCP_URL}?key={ACCOUNT_SK}", 
            json=mcp_request,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        try:
            return jsonify({
                "success": True,
                "data": response.json()
            })
        except:
            return jsonify({
                "success": True,
                "data": response.text
            })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
