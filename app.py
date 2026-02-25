import streamlit as st
from transformers import pipeline
import re

# -----------------------------------
# Page Config
# -----------------------------------
st.set_page_config(page_title="Advanced Ethical Poem Generator", page_icon="📝")

st.title("📝 Advanced Ethical Poem Generator")
st.write("Generate high-quality English poems based on your topic ✨")
st.write("⚠️ Unethical topics are restricted.")

# -----------------------------------
# Load Model (Cloud Safe)
# -----------------------------------
@st.cache_resource
def load_model():
    generator = pipeline(
        task="text2text-generation",
        model="google/flan-t5-base"   # base version works better on cloud memory
    )
    return generator

generator = load_model()

# -----------------------------------
# Ethical Filter
# -----------------------------------
UNETHICAL_KEYWORDS = [
    "violence", "terror", "hate", "racism",
    "sexism", "drugs", "weapon", "murder",
    "kill", "bomb", "crime", "porn",
    "explicit", "abuse"
]

def is_unethical(text):
    text = text.lower()
    for word in UNETHICAL_KEYWORDS:
        if word in text:
            return True
    return False

# -----------------------------------
# Input
# -----------------------------------
topic = st.text_input("Topic :", placeholder="Enter a topic (e.g., Hope, Nature, Success)")

if st.button("Generate Poem"):

    if topic.strip() == "":
        st.warning("Please enter a topic.")

    elif is_unethical(topic):
        st.error("⚠️ This topic violates ethical guidelines. Please enter a safe topic.")

    else:
        prompt = f"""
        Write a beautiful, expressive English poem about "{topic}".
        Use vivid imagery.
        Make it 3 stanzas.
        Make it emotional and rhythmic.
        """

        with st.spinner("Crafting your poem... ✨"):
            result = generator(
                prompt,
                max_length=256,
                do_sample=True,
                temperature=0.9
            )

        poem = result[0]["generated_text"]

        st.subheader("📜 Output :")
        st.write(poem)