import streamlit as st
import sys
import pysqlite3
sys.modules["sqlite3"] = pysqlite3
import chromadb
import openai

# --- Service First Branding ---
st.set_page_config(page_title="Service First AI Assistant", page_icon="🛠️", layout="centered")
st.markdown(
    "<h1 style='text-align: center;'>🛠️ Service First AI Assistant</h1>",
    unsafe_allow_html=True
)

st.markdown("This tool is designed to help our internal team — especially HR, admin, and marketing — get fast, helpful answers based on Service First's knowledge base.")

# --- OpenAI + Chroma Setup ---
client_openai = openai.OpenAI(api_key=st.secrets["openai_key"])
client = chromadb.Client()
collection = client.get_or_create_collection(name="service_first_assistant")

# --- Assistant Input UI ---
user_input = st.text_input("📥 Ask the Assistant a question:")

if st.button("💬 Submit") and user_input:
    with st.spinner("Thinking like a pro..."):
        results = collection.query(query_texts=[user_input], n_results=3)
        context = "\n\n".join(results["documents"][0])

        system_prompt = """
        You are the AI assistant for Service First Heating & Air Conditioning in Newtown, PA.
        You sound like a smart and confident employee. Avoid em dashes and fluff. Keep it helpful, clear, and real.
        """

        response = client_openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{user_input}"}
            ]
        )

        st.markdown("### 💡 Assistant's Response")
        st.success(response.choices[0].message.content)