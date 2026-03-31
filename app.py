from flask import Flask, request, jsonify
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

FILE_PATH = "responses.csv"

def update_data(booking_id, status):
    booking_id = str(booking_id)

    if os.path.exists(FILE_PATH):
        df = pd.read_csv(FILE_PATH)
    else:
        df = pd.DataFrame(columns=['booking_id', 'checked_in', 'timestamp'])

    if booking_id in df['booking_id'].values:
        df.loc[df['booking_id'] == booking_id, 'checked_in'] = status
        df.loc[df['booking_id'] == booking_id, 'timestamp'] = datetime.now()
    else:
        df = pd.concat([df, pd.DataFrame([{
            "booking_id": booking_id,
            "checked_in": status,
            "timestamp": datetime.now()
        }])])

    df.to_csv(FILE_PATH, index=False)


# -------------------------------
# STEP 1 PAGE (OPEN FROM EMAIL)
# -------------------------------
@app.route('/confirm')
def confirm():
    booking_id = request.args.get('booking_id')

    return f"""
    <h2>Check-in Confirmation</h2>
    <p><b>Booking ID:</b> {booking_id}</p>

    <a href="/submit?booking_id={booking_id}&status=YES" 
       style="background:green;color:white;padding:10px 15px;text-decoration:none;">YES</a>

    <a href="/submit?booking_id={booking_id}&status=NO" 
       style="background:red;color:white;padding:10px 15px;text-decoration:none;margin-left:10px;">NO</a>
    """


# -------------------------------
# STEP 2 (SAVE RESPONSE)
# -------------------------------
@app.route('/submit')
def submit():
    booking_id = request.args.get('booking_id')
    status = request.args.get('status')

    update_data(booking_id, status)

    return f"""
    <h2>✅ Response Recorded</h2>
    <p>Booking: {booking_id}</p>
    <p>Status: {status}</p>
    """


# -------------------------------
# DATA API
# -------------------------------
@app.route('/data')
def get_data():
    if os.path.exists(FILE_PATH):
        df = pd.read_csv(FILE_PATH)
        return df.to_json(orient='records')
    return jsonify([])


@app.route('/')
def home():
    return "Server Running ✅"
