import streamlit as st
from transformers import pipeline
import torch

# ------------------------------
# Page Config
# ------------------------------
st.set_page_config(page_title="Soft ChatGPT - Poem Generator", page_icon="📝")

st.title("📝 Soft Version of ChatGPT - Ethical Poem Generator")
st.write("Enter any topic and get a beautiful poem in English ✨")
st.write("Note: The model will not generate poems on unethical topics.")

# ------------------------------
# Load Model
# ------------------------------
@st.cache_resource
def load_model():
    generator = pipeline(
        "text-generation",
        model="gpt2",
        device=0 if torch.cuda.is_available() else -1
    )
    return generator

generator = load_model()

# ------------------------------
# Ethical Filter
# ------------------------------
UNETHICAL_KEYWORDS = [
    "violence", "terrorism", "drugs", "weapon", "hate",
    "racism", "sexism", "abuse", "crime", "murder",
    "kill", "blood", "bomb", "porn", "explicit"
]

def is_unethical(topic):
    topic = topic.lower()
    for word in UNETHICAL_KEYWORDS:
        if word in topic:
            return True
    return False

# ------------------------------
# User Input
# ------------------------------
topic = st.text_input("Topic :", placeholder="Enter your topic here...")

if st.button("Generate Poem"):

    if topic.strip() == "":
        st.warning("Please enter a topic.")
    
    elif is_unethical(topic):
        st.error("⚠️ This topic is unethical. Please enter a safe and ethical topic.")
    
    else:
        prompt = f"Write a beautiful English poem about {topic}:\n\n"
        
        with st.spinner("Generating poem..."):
            result = generator(
                prompt,
                max_length=150,
                num_return_sequences=1,
                temperature=0.8,
                top_p=0.9,
                do_sample=True
            )
        
        poem = result[0]["generated_text"].replace(prompt, "")
        
        st.subheader("Output :")
        st.write(poem)