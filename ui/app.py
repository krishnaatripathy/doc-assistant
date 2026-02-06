import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Doc Assistant",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Doc Assistant")
st.caption("An AI powered system for querying uploaded documents using semantic retrieval and controlled answer generation.")
#Upload
st.header("Upload a document")

uploaded_file = st.file_uploader(
    "Choose a PDF or TXT file",
    type=["pdf", "txt"]
)

if uploaded_file:
    files = {
        "file": (uploaded_file.name, uploaded_file, uploaded_file.type)
    }
    response = requests.post(f"{API_URL}/upload", files=files)

    if response.ok:
        st.success("Document uploaded and indexed successfully")
    else:
        st.error("Upload failed. Please check file format.")
#Ask
st.header("Ask a question")

question = st.text_input("Enter your question")

strict_mode = st.checkbox(
    "Strict mode (refuse answers if confidence is low)",
    value=True
)

if st.button("Ask") and question:
    params = {
        "question": question,
        "strict": strict_mode
    }

    response = requests.post(f"{API_URL}/ask", params=params)

    if response.ok:
        data = response.json()

        st.subheader("Answer")
        st.write(data["answer"])

        st.caption(f"Mode: {data.get('mode', 'unknown')}")

        with st.expander("Retrieved context"):
            for i, src in enumerate(data.get("sources", []), 1):
                st.markdown(f"**Chunk {i}:**")
                st.write(src)
    else:
        st.error("Failed to generate answer")
#Summary
st.header("Document Summary")

if st.button("Generate Summary"):
    response = requests.get(f"{API_URL}/summary")

    if response.ok:
        data = response.json()
        st.subheader("Summary")
        st.write(data["summary"])
    else:
        st.error("Summary unavailable. Upload a document first.")
