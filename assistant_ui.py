import streamlit as st
import chromadb
import openai

# OpenAI API setup
client_openai = openai.OpenAI(api_key=st.secrets["openai_key"])

# Chroma setup
client = chromadb.Client()
collection = client.get_or_create_collection(name="service_first_assistant")

# UI
st.set_page_config(page_title="Service First AI Assistant", layout="centered")
st.title("🛠️ Service First AI Assistant")

user_input = st.text_input("Ask a question about Service First:")

if st.button("Submit") and user_input:
    with st.spinner("Thinking..."):
        results = collection.query(query_texts=[user_input], n_results=3)
        context = "\n\n".join(results["documents"][0])

        system_prompt = """
        You are the AI assistant for Service First Heating & Air Conditioning in Newtown, PA.
        Answer like a confident team member. Avoid em dashes and fluff. Be helpful, clear, and precise.
        """

        response = client_openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{user_input}"}
            ]
        )

        st.markdown("### 💡 Assistant's Response")
        st.write(response.choices[0].message.content)
