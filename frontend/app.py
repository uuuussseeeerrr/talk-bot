# frontend/app.py
import streamlit as st
import requests

st.header("📅 Upcoming Appointments")

try:
    resp = requests.get("http://127.0.0.1:8000/appointments")
    data = resp.json()
    events = data.get("events", [])
    if events:
        for event in events:
            start = event["start"].replace("T", " ").replace("Z", "")
            st.write(f"- {start} — {event['summary']}")
    else:
        st.write("No upcoming appointments.")
except Exception as e:
    st.error("Couldn't load appointments.")


st.set_page_config(page_title="TailorTalk Chatbot 💬")

st.title("🤖 TailorTalk - Appointment Bot")

name = st.text_input("Your Name")
email = st.text_input("Your Email")
date = st.date_input("Select Date")
time = st.time_input("Select Time")

if st.button("Book Appointment"):
    try:
        response = requests.post("http://127.0.0.1:8000/book", json={
            "name": name,
            "email": email,
            "date": str(date),
            "time": time.strftime("%H:%M")
        })
        st.success(response.json()["message"])
    except:
        st.error("Booking failed.")
        
st.markdown("---")
st.header("💬 Chat with TailorTalk")

user_input = st.text_input("Ask something like: 'Book a slot for 'Name' DD//MM/YYYY at 2 PM'")

if st.button("Send") and user_input.strip():
    with st.spinner("💬 Talking to TailorTalk..."):
        try:
            chat_resp = requests.get("http://127.0.0.1:8000/chat", params={"query": user_input})
            response_data = chat_resp.json()
            st.success(response_data.get("response", "✅ Done"))
        except Exception as e:
            st.error(f"Agent failed to respond. ❌ {e}")

