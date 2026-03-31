#!/usr/bin/env python
# coding: utf-8

# In[3]:


from flask import Flask, request
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


@app.route('/response')
def capture():
    booking_id = request.args.get('booking_id')
    status = request.args.get('status')

    update_data(booking_id, status)

    return f"✅ Response Recorded<br>Booking: {booking_id}<br>Status: {status}"


@app.route('/')
def home():
    return "Server Running ✅"

