import streamlit as st
from transformers import pipeline
import torch
import re

# -----------------------------------
# Page Config
# -----------------------------------
st.set_page_config(page_title="Advanced Ethical Poem Generator", page_icon="📝")

st.title("📝 Advanced Ethical Poem Generator")
st.write("Generate high-quality English poems based on your topic ✨")
st.write("⚠️ Unethical topics are strictly restricted.")

# -----------------------------------
# Load Advanced Model
# -----------------------------------
@st.cache_resource
def load_model():
    return pipeline(
        "text2text-generation",
        model="google/flan-t5-large",
        device=0 if torch.cuda.is_available() else -1
    )

generator = load_model()

# -----------------------------------
# Advanced Ethical Filter
# -----------------------------------
UNETHICAL_PATTERNS = [
    r"violence", r"terror", r"hate", r"racism",
    r"sexism", r"drugs", r"weapon", r"murder",
    r"kill", r"bomb", r"crime", r"porn",
    r"explicit", r"abuse"
]

def is_unethical(text):
    text = text.lower()
    for pattern in UNETHICAL_PATTERNS:
        if re.search(pattern, text):
            return True
    return False

# -----------------------------------
# User Input
# -----------------------------------
topic = st.text_input("Topic :", placeholder="Enter a topic (e.g., Nature, Dreams, Success)")

if st.button("Generate Poem"):

    if topic.strip() == "":
        st.warning("Please enter a topic.")

    elif is_unethical(topic):
        st.error("⚠️ This topic violates ethical guidelines. Please enter a safe topic.")

    else:
        prompt = f"""
        Write a beautiful, emotionally rich, well-structured English poem about "{topic}".
        The poem must:
        - Be creative and expressive
        - Have rhythm and imagery
        - Contain 3–4 stanzas
        - Avoid repetition
        - Sound professional and literary
        """

        with st.spinner("Crafting your poem... ✨"):
            result = generator(
                prompt,
                max_length=300,
                temperature=0.9,
                top_p=0.95,
                do_sample=True
            )

        poem = result[0]["generated_text"]

        st.subheader("📜 Output :")
        st.write(poem)