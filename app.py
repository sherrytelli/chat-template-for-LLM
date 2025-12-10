import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import streamlit as st
from huggingface_hub import login
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Llama-3.2-3B-Instruct Chat",
    page_icon="🦙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add CSS for wave animation and centered title
st.markdown("""
<style>
    @keyframes wave {
        0%, 60%, 100% {
            transform: initial;
        }
        30% {
            transform: translateY(-0.2rem);
        }
    }
    .wave-ellipsis span {
        display: inline-block;
        animation: wave 1.5s infinite;
        line-height: 1.5rem;
    }
    .wave-ellipsis span:nth-child(2) {
        animation-delay: 0.2s;
    }
    .wave-ellipsis span:nth-child(3) {
        animation-delay: 0.4s;
    }
    .centered-title {
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

if os.getenv("HF_TOKEN"):
    try:
        login(os.getenv("HF_TOKEN"))
        print("Logged into Hugging Face")
    except Exception as e:
        print(f"Login failed: {e}")
        st.error("Failed to setup services.")
        st.stop()
else:
    print("No Hugging Face token found")
    st.error("Failed to setup services.")
    st.stop()

@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-3B-Instruct", cache_dir="/home/extra/vllm/model weights/")
    model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-3B-Instruct", cache_dir="/home/extra/vllm/model weights/", device_map="auto")
    return model, tokenizer

st.markdown('<h1 class="centered-title">Llama-3.2-3B-Instruct Chat Interface</h1>', unsafe_allow_html=True)
model, tokenizer = load_model()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown(
            '<div class="wave-ellipsis"><span>.</span><span>.</span><span>.</span></div>',
            unsafe_allow_html=True
        )
    
    chat = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    inputs = tokenizer.apply_chat_template(
        chat,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt",
        return_dict=True
    ).to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=1024,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )
    
    response = tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
    del inputs, outputs
    
    response = response.split(tokenizer.eos_token)[0].strip()
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    message_placeholder.markdown(response)