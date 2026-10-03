import streamlit as st
import time
from google import genai
from google.genai import types
from prompts import SYSTEM_PROMPT, SUMMARY_PROMPT


st.set_page_config(
    page_title="Snap & Study",
    page_icon="🎓"
)


# Gemini API
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)


# Conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Title
st.title("🎓 Snap & Study")
st.write("Your AI-powered study assistant")


# Show previous conversation
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# Image upload
uploaded_image = st.file_uploader(
    "📷 Upload a study image",
    type=["jpg", "jpeg", "png", "webp"]
)


# Question box
question = st.chat_input("Ask a study question...")


if question:

    # Save student's question
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })


    # Show student's question
    with st.chat_message("user"):
        st.write(question)


    # Prepare conversation
    conversation = []

    for message in st.session_state.messages:

        conversation.append(
            f"{message['role']}: {message['content']}"
        )

    conversation_text = "\n".join(conversation)


    # Prepare Gemini input
    if uploaded_image:

        image_bytes = uploaded_image.getvalue()

        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=uploaded_image.type
        )

        contents = [
            image_part,
            f"""
Conversation so far:

{conversation_text}

Answer the student's latest question using the
uploaded study image and the conversation context.

Explain concepts simply and clearly.
Use examples when helpful.
"""
        ]

    else:

        contents = f"""
Conversation so far:

{conversation_text}

Answer the student's latest question.

Explain concepts simply and clearly.
Use examples when helpful.
"""


    # Ask Gemini
    with st.chat_message("assistant"):

        response = None

        for attempt in range(3):

            try:

                with st.spinner(
                    f"Thinking... (attempt {attempt + 1}/3)"
                ):

                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=contents,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_PROMPT
                        )
                    )

                break

            except Exception:

                if attempt < 2:
                    time.sleep(3)


        # Check whether Gemini responded
        if response is not None:

            st.write(response.text)

            # Save Gemini response
            st.session_state.messages.append({
                "role": "assistant",
                "content": response.text
            })

        else:

            st.warning(
                "⚠️ Gemini is temporarily busy. "
                "Please try again in a moment."
            )


# Study Summary
st.divider()

st.subheader("📝 Study Summary")


if st.button("Generate Study Summary"):

    if not st.session_state.messages:

        st.warning(
            "Please ask a study question first."
        )

    else:

        # Prepare conversation
        conversation = []

        for message in st.session_state.messages:

            conversation.append(
                f"{message['role']}: {message['content']}"
            )

        conversation_text = "\n".join(conversation)


        # Summary prompt
        summary_prompt = f"""
Create a short revision summary from this conversation.

Conversation:

{conversation_text}
"""


        # Generate summary
        with st.spinner("Creating your study summary..."):

            summary_response = None

            for attempt in range(3):

                try:

                    summary_response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=summary_prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=SUMMARY_PROMPT
                        )
                    )

                    break

                except Exception:

                    if attempt < 2:
                        time.sleep(3)


            # Check summary response
            if summary_response is not None:

                st.session_state.study_summary = (
                    summary_response.text
                )

                st.success(
                    "Study summary created!"
                )

            else:

                st.warning(
                    "⚠️ Gemini is temporarily busy. "
                    "Please try generating the summary again."
                )


# Display summary
if "study_summary" in st.session_state:

    st.markdown("### 📚 Your Study Summary")

    st.write(
        st.session_state.study_summary
    )