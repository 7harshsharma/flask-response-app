from flask import Flask, request, jsonify
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# ===============================
# GOOGLE SHEET SETUP
# ===============================
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

sheet = client.open("hotel_responses").sheet1


# ===============================
# UPDATE DATA (REPLACES CSV LOGIC)
# ===============================
def update_data(booking_id, status):
    booking_id = str(booking_id)

    records = sheet.get_all_records()
    
    # Check if booking exists
    for idx, row in enumerate(records, start=2):  # start=2 because row 1 = header
        if str(row.get('booking_id')) == booking_id:
            sheet.update_cell(idx, 2, status)  # checked_in column
            sheet.update_cell(idx, 3, str(datetime.now()))  # timestamp
            return

    # If not exists → append
    sheet.append_row([
        booking_id,
        status,
        str(datetime.now())
    ])


# -------------------------------
# STEP 1 PAGE (OPEN FROM EMAIL)
# -------------------------------
@app.route('/confirm')
def confirm():
    booking_id = request.args.get('booking_id')
    guest_name = request.args.get('guest_name', 'Guest')

    return f"""
    <h2>Check-in Confirmation</h2>

    <p><b>Guest Name:</b> {guest_name}</p>
    <p><b>Booking ID:</b> {booking_id}</p>

    <br>

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
# DATA API (FOR YOUR PYTHON SCRIPT)
# -------------------------------
@app.route('/data')
def get_data():
    records = sheet.get_all_records()
    return jsonify(records)


@app.route('/')
def home():
    return "Server Running ✅"
