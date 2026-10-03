import streamlit as st
from twilio.rest import Client

client = Client(
    st.secrets["TWILIO_ACCOUNT_SID"],
    st.secrets["TWILIO_AUTH_TOKEN"]
)

message = client.messages.create(
    from_=st.secrets["TWILIO_WHATSAPP_NUMBER"],
    to="whatsapp:+918252028036",
    body="Hello from Snap & Study! 🎓"
)

print("Message sent!")
print("SID:", message.sid)
print("Status:", message.status)