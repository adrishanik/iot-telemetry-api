from flask import Flask, jsonify, request, render_template_string
from datetime import datetime

app = Flask(__name__)

# In-memory storage for sensor and device records
sensor_logs = [
    {"id": 1, "sensor": "soil_moisture", "value": 68.5, "unit": "%", "timestamp": "2026-08-25 06:30:00"},
    {"id": 2, "sensor": "temperature", "value": 29.4, "unit": "C", "timestamp": "2026-08-25 06:35:00"},
    {"id": 3, "sensor": "air_quality_pm25", "value": 42.1, "unit": "ug/m3", "timestamp": "2026-08-25 06:40:00"}
]

# --- 1. DOCS ENDPOINT (/docs) ---
@app.route("/docs", methods=["GET"])
def documentation():
    html_docs = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>IoT Telemetry API - Documentation</title>
        <style>
            body { font-family: monospace; padding: 24px; background: #0f172a; color: #f8fafc; }
            h1 { color: #38bdf8; }
            .badge-get { background: #0284c7; color: white; padding: 4px 8px; border-radius: 4px; }
            .badge-post { background: #16a34a; color: white; padding: 4px 8px; border-radius: 4px; }
            pre { background: #1e293b; padding: 12px; border-radius: 6px; }
            .card { border: 1px solid #334155; padding: 14px; margin-bottom: 16px; border-radius: 8px; }
        </style>
    </head>
    <body>
        <h1>📡 IoT Telemetry API Docs</h1>
        <p>Built for Hack Club RaspAPI submission.</p>

        <div class="card">
            <p><span class="badge-get">GET</span> <code>/api/health</code></p>
            <p>Returns system status and server uptime.</p>
        </div>

        <div class="card">
            <p><span class="badge-get">GET</span> <code>/api/sensors</code></p>
            <p>Lists all recorded sensor readings.</p>
        </div>

        <div class="card">
            <p><span class="badge-get">GET</span> <code>/api/sensors/&lt;sensor_name&gt;</code></p>
            <p>Filter data by sensor name (e.g. <code>soil_moisture</code>, <code>temperature</code>).</p>
        </div>

        <div class="card">
            <p><span class="badge-post">POST</span> <code>/api/sensors</code></p>
            <p>Submit a new sensor data point.</p>
            <pre>Payload: {"sensor": "soil_moisture", "value": 72.0, "unit": "%"}</pre>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_docs)


# --- 2. GET ENDPOINT #1: System Health ---
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "online",
        "service": "IoT Telemetry API",
        "total_records": len(sensor_logs),
        "timestamp": datetime.now().isoformat()
    }), 200


# --- 3. GET ENDPOINT #2: Get All Sensor Logs ---
@app.route("/api/sensors", methods=["GET"])
def get_all_sensors():
    return jsonify({
        "success": True,
        "count": len(sensor_logs),
        "data": sensor_logs
    }), 200


# --- 4. GET ENDPOINT #3: Get Readings by Specific Sensor ---
@app.route("/api/sensors/<string:sensor_name>", methods=["GET"])
def get_sensor_by_name(sensor_name):
    matched = [s for s in sensor_logs if s["sensor"].lower() == sensor_name.lower()]
    if not matched:
        return jsonify({"success": False, "message": f"No data found for sensor: {sensor_name}"}), 404
    return jsonify({"success": True, "count": len(matched), "data": matched}), 200


# --- 5. POST ENDPOINT: Add New Sensor Reading ---
@app.route("/api/sensors", methods=["POST"])
def add_sensor_reading():
    data = request.get_json()
    if not data or "sensor" not in data or "value" not in data or "unit" not in data:
        return jsonify({
            "success": False,
            "error": "Invalid payload. Required keys: 'sensor', 'value', 'unit'"
        }), 400

    new_entry = {
        "id": len(sensor_logs) + 1,
        "sensor": str(data["sensor"]).strip(),
        "value": float(data["value"]),
        "unit": str(data["unit"]).strip(),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    sensor_logs.append(new_entry)

    return jsonify({
        "success": True,
        "message": "Sensor data logged successfully",
        "entry": new_entry
    }), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
