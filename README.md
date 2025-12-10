# Chat Template for LLMs

This repository provides a **simple and customizable chat template** that allows you to interact with **any Large Language Model (LLM)** with minimal setup. You can easily switch between models, manage prompts, and extend functionality as needed.

---

## 🚀 Features

* Plug‑and‑play structure to chat with any Hugging Face LLM.
* Clean and minimal codebase.
* Fully customizable system, user, and assistant messages.
* Environment‑based configuration for API tokens.

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/sherrytelli/chat-template-for-LLM
cd chat-template-for-LLM
```

Install dependencies (recommended to do this inside a virtual environment):

```bash
pip install transformers streamlit
```

---

## 🔐 Environment Setup

Create a `.env` file in the project root:

```bash
HF_TOKEN=your_huggingface_token_here
```

This token will be used for model authentication.

---

## 🧠 Choosing Your Model

Inside the code, you will see a line where the model is loaded:

```python
model = "meta-llama/Llama-3.2-3B-Instruct"
```

Replace this string with **any** Hugging Face model you'd like to use, for example:

```python
model = "Qwen/Qwen2.5-7B-Instruct"
```

Or any other:

```python
model = "google/gemma-2-27b-it"
```

Make sure the model:

* Supports text generation.
* Is accessible with your HF token.

---

## ▶️ Running the Chat

Once everything is configured, run:

```bash
streamlit run app.py
```

You will be prompted for input and can chat with the LLM interactively.

---

## 📝 Notes

* Ensure your system meets the hardware/runtime requirements of the model you choose.
* Some large models may require GPU acceleration.
* You can customize the chat template and system prompts inside the code.

---

## 🤝 Contributing

Pull requests and improvements are welcome!

---

## 📄 License

MIT License
