import requests

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbx8dqhtyZ_kfO3GGbkT8RDw1wyyOG9oTLm-bJFfL1JzTzXNG9BG_ECwrMR2Z7Fu8z1LlQ/exec"

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
