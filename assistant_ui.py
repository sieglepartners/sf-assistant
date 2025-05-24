import streamlit as st
import sys
import pysqlite3
import chromadb
import openai

sys.modules["sqlite3"] = pysqlite3

# App styling for Service First
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f9f9f9;
    }
    h1 {
        color: #002f6c;
    }
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
        border: 1px solid #002f6c;
    }
    .stButton > button {
        background-color: #002f6c;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar for internal navigation
with st.sidebar:
    st.image("https://servicefirsthvac.com/wp-content/uploads/2023/05/ServiceFirst-Logo-Color.png", width=180)
    st.markdown("### Quick Links")
    st.write("📄 SOPs (coming soon)")
    st.write("🧠 Training Materials")
    st.write("💬 Contact Mark or Ashley")

# OpenAI API setup
client_openai = openai.OpenAI(api_key=st.secrets["openai_key"])

# Chroma setup
client = chromadb.Client()
collection = client.get_or_create_collection(name="service_first_assistant")

# App layout
st.set_page_config(page_title="Service First AI Assistant", layout="centered")
st.title("🛠️ Service First AI Assistant")

st.write(
    "This tool is designed to help our internal team — especially HR, admin, and marketing — get fast, helpful answers based on Service First's knowledge base."
)

question_type = st.selectbox(
    "What’s this about?",
    ["General", "HR Policy", "Marketing", "Office Operations"]
)

user_input = st.text_input("📩 Ask the Assistant a question:")

uploaded_file = st.file_uploader("Upload file for assistant context (PDF or TXT)", type=["pdf", "txt"])
if uploaded_file:
    st.session_state.uploaded_content = uploaded_file.read().decode("utf-8")

if st.button("💬 Submit") and user_input:
    with st.spinner("Thinking..."):
        results = collection.query(query_texts=[user_input], n_results=3)
        context = "\n\n".join(results["documents"][0])

        if "uploaded_content" in st.session_state:
            context += f"\n\nUploaded Content:\n{st.session_state.uploaded_content}"

        system_prompt = f"""
        You are the AI assistant for Service First Heating & Air Conditioning in Newtown, PA.
        You are helping with {question_type.lower()} tasks.
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