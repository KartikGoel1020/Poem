import streamlit as st
from openai import OpenAI

# -----------------------------------
# Page Setup
# -----------------------------------
st.set_page_config(page_title="Premium Ethical Poem Generator", page_icon="📝")

st.title("📝 Premium Ethical Poem Generator")
st.write("High-quality English poetry powered by AI ✨")
st.write("⚠️ Unethical topics are automatically filtered.")

# -----------------------------------
# Load OpenAI Client
# -----------------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -----------------------------------
# Moderation Function
# -----------------------------------
def is_unethical(text):
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=text
    )
    return response.results[0].flagged

# -----------------------------------
# Input
# -----------------------------------
topic = st.text_input("Topic :", placeholder="Enter any topic...")

if st.button("Generate Poem"):

    if topic.strip() == "":
        st.warning("Please enter a topic.")

    elif is_unethical(topic):
        st.error("⚠️ This topic violates ethical guidelines. Please enter a safe topic.")

    else:

        with st.spinner("Crafting your poem... ✨"):

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional English poet. "
                                   "Write beautiful, structured, emotionally rich poems. "
                                   "Never write about harmful or unethical content."
                    },
                    {
                        "role": "user",
                        "content": f"Write a 3-4 stanza poetic masterpiece about '{topic}'. "
                                   "Use vivid imagery, rhythm, and literary devices."
                    }
                ],
                temperature=0.9
            )

            poem = response.choices[0].message.content

        # Double-check output moderation
        if is_unethical(poem):
            st.error("⚠️ Generated content violated ethical guidelines.")
        else:
            st.subheader("📜 Output :")
            st.write(poem)