import streamlit as st
from twilio.rest import Client

client = Client(
    st.secrets["TWILIO_ACCOUNT_SID"],
    st.secrets["TWILIO_AUTH_TOKEN"]
)

messages = client.messages.list(limit=10)

for message in messages:
    print("SID:", message.sid)
    print("From:", message.from_)
    print("To:", message.to)
    print("Body:", message.body)
    print("Status:", message.status)

    # Check whether Twilio returned a ContentSid
    print("ContentSid:", getattr(message, "content_sid", None))

    print("-" * 50)