from flask import Flask, request
import requests

# ✅ STEP 1: CREATE APP FIRST
app = Flask(__name__)

# ✅ STEP 2: GOOGLE SCRIPT URL
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbx8dqhtyZ_kfO3GGbkT8RDw1wyyOG9oTLm-bJFfL1JzTzXNG9BG_ECwrMR2Z7Fu8z1LlQ/exec"


# -------------------------------
# HOME
# -------------------------------
@app.route('/')
def home():
    return "Server Running ✅"


# -------------------------------
# CONFIRM PAGE
# -------------------------------
@app.route('/confirm')
def confirm():
    booking_id = request.args.get('booking_id')
    guest_name = request.args.get('guest_name')

    return f"""
    <h2>Check-in Confirmation</h2>
    <p><b>Booking ID:</b> {booking_id}</p>
    <p><b>Guest Name:</b> {guest_name}</p>

    <a href="/submit?booking_id={booking_id}&status=YES" 
       style="background:green;color:white;padding:10px 15px;text-decoration:none;">
       YES
    </a>

    <a href="/submit?booking_id={booking_id}&status=NO" 
       style="background:red;color:white;padding:10px 15px;text-decoration:none;margin-left:10px;">
       NO
    </a>
    """


# -------------------------------
# SUBMIT RESPONSE
# -------------------------------
@app.route('/submit')
def submit():
    booking_id = request.args.get('booking_id')
    status = request.args.get('status')

    try:
        requests.get(GOOGLE_SCRIPT_URL, params={
            "booking_id": booking_id,
            "status": status
        }, timeout=10)
    except:
        pass

    return f"""
    <h2>✅ Response Recorded</h2>
    <p>Booking: {booking_id}</p>
    <p>Status: {status}</p>
    """
