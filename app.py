import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import re

# -----------------------------------
# Page Config
# -----------------------------------
st.set_page_config(page_title="Advanced Ethical Poem Generator", page_icon="📝")

st.title("📝 Advanced Ethical Poem Generator")
st.write("Generate high-quality English poems based on your topic ✨")
st.write("⚠️ Unethical topics are restricted.")

# -----------------------------------
# Load Model Safely (NO PIPELINE)
# -----------------------------------
@st.cache_resource
def load_model():
    model_name = "google/flan-t5-base"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_model()

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
# User Input
# -----------------------------------
topic = st.text_input("Topic :", placeholder="Enter a topic (e.g., Hope, Nature, Success)")

if st.button("Generate Poem"):

    if topic.strip() == "":
        st.warning("Please enter a topic.")

    elif is_unethical(topic):
        st.error("⚠️ This topic violates ethical guidelines. Please enter a safe topic.")

    else:
        prompt = f"""
        Write a beautiful, emotional English poem about "{topic}".
        Make it 3 stanzas.
        Use vivid imagery and expressive language.
        """

        with st.spinner("Crafting your poem... ✨"):

            inputs = tokenizer(prompt, return_tensors="pt")

            outputs = model.generate(
                **inputs,
                max_length=256,
                temperature=0.9,
                do_sample=True,
                top_p=0.95
            )

            poem = tokenizer.decode(outputs[0], skip_special_tokens=True)

        st.subheader("📜 Output :")
        st.write(poem)