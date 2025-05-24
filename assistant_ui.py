import streamlit as st

# 🚨 Must be the first Streamlit call
st.set_page_config(
    page_title="Service First AI Assistant",
    layout="centered"
)

import sys
import pysqlite3
sys.modules["sqlite3"] = pysqlite3
import chromadb
import openai

# 🔐 OpenAI API Key (stored in Streamlit secrets)
client_openai = openai.OpenAI(api_key=st.secrets["openai_key"])

# 🔎 Chroma client and collection
client = chromadb.Client()
collection = client.get_or_create_collection(name="service_first_assistant")

# 🛠️ Branded UI
st.image("Service First Logo.png", use_column_width=True)
st.title("🛠️ Service First AI Assistant")

st.markdown(
    "This tool is designed to help our internal team — especially HR, admin, and marketing — "
    "get fast, helpful answers based on Service First’s knowledge base."
)

st.markdown("### 💬 Ask the Assistant a question:")

user_input = st.text_input(" ", label_visibility="collapsed")

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

# 🧭 Sidebar for internal links
with st.sidebar:
    st.markdown("### 🔗 Quick Links")
    st.markdown("📄 SOPs (coming soon)")
    st.markdown("🎓 Training Materials")
    st.markdown("💬 Contact Mark or Ashley")