from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)

DB_PATH = "ledger.db"

def get_ledger_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, card_uid, amount, status, hmac_sig FROM ilp_stream_ledger ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_summary():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), SUM(amount), COUNT(DISTINCT card_uid) FROM ilp_stream_ledger")
    total_packets, total_cash, unique_cards = cursor.fetchone()
    
    cursor.execute("SELECT card_uid, COUNT(*), SUM(amount) FROM ilp_stream_ledger GROUP BY card_uid")
    breakdown = cursor.fetchall()
    conn.close()
    return {
        "total_packets": total_packets or 0,
        "total_cash": total_cash or 0.0,
        "unique_cards": unique_cards or 0,
        "breakdown": breakdown
    }

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Octopus 2.0 Audit Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: monospace; background: #121212; color: #00ffcc; padding: 20px; }
        h1, h2 { color: #fff; border-bottom: 1px solid #333; padding-bottom: 10px; }
        .card { background: #1e1e1e; padding: 15px; margin-bottom: 15px; border-radius: 5px; border-left: 4px solid #00ffcc; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; background: #1e1e1e; }
        th, td { border: 1px solid #333; padding: 8px; text-align: left; font-size: 12px; }
        th { background: #262626; color: #fff; }
        tr:nth-child(even) { background: #161616; }
        .metric { font-size: 24px; font-weight: bold; color: #fff; }
    </style>
</head>
<body>
    <h1>🐙 OCTOPUS 2.0 AUDIT DASHBOARD</h1>
    <p>Status: <span style="color: #00ffcc;">ONLINE & SECURED</span></p>

    <div class="card">
        <h2>System Overview</h2>
        <p>Total Settled Cash: <span class="metric">${{ "%.2f"|format(summary.total_cash) }}</span></p>
        <p>Total Stream Packets: <strong>{{ summary.total_packets }}</strong> | Active Cards: <strong>{{ summary.unique_cards }}</strong></p>
    </div>

    <div class="card">
        <h2>Card Breakdown</h2>
        <table>
            <tr><th>Card UID</th><th>Packets</th><th>Subtotal</th></tr>
            {% for row in summary.breakdown %}
            <tr><td>{{ row[0] }}</td><td>{{ row[1] }}</td><td>${{ "%.2f"|format(row[2]) }}</td></tr>
            {% endfor %}
        </table>
    </div>

    <div class="card">
        <h2>Live Transaction Ledger</h2>
        <table>
            <tr><th>Timestamp</th><th>Card UID</th><th>Amount</th><th>Status</th><th>HMAC Anchor</th></tr>
            {% for tx in transactions %}
            <tr>
                <td>{{ tx[0] }}</td>
                <td>{{ tx[1] }}</td>
                <td>${{ "%.2f"|format(tx[2]) }}</td>
                <td>{{ tx[3] }}</td>
                <td style="font-size: 10px; color: #888;">{{ tx[4][:16] }}...</td>
            </tr>
            {% endfor %}
        </table>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, summary=get_summary(), transactions=get_ledger_data())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
