import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

system_prompt = """You are a healthcare expert with 10+ years of experience. You only answer questions related to healthcare. 
If a question is not about healthcare, politely refuse with: "I can only answer healthcare-related questions. Please ask about health, diet, exercise, or medical topics."

Keep your responses:
- Short and practical
- In a friendly tone
- In Hinglish when possible
- Focused on actionable advice"""

def ask_healthcare_ai(question):
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt}, 
            {"role": "user", "content": question}, 
        ],
        model="llama3-70b-8192",
    )
    return chat_completion.choices[0].message.content

# Set page config
st.set_page_config(
    page_title="Health Buddy AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e3f2fd;
        margin-left: 20%;
    }
    .assistant-message {
        background-color: #ffffff;
        margin-right: 20%;
    }
    .stTextInput > div > div > input {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 1rem;
    }
    .stButton > button {
        background-color: #2196f3;
        color: white;
        border-radius: 10px;
        padding: 0.5rem 2rem;
    }
    .stButton > button:hover {
        background-color: #1976d2;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🏥 Health Buddy AI")
    st.markdown("---")
    st.markdown("""
    ### About
    Health Buddy AI is your personal healthcare assistant. Ask me anything about:
    - Diet and nutrition
    - Exercise and fitness
    - Mental health
    - General health tips
    - Medical advice
    """)
    st.markdown("---")
    st.markdown("Made with ❤️ for better health")

# Main content
st.title("💬 Chat with Health Buddy AI")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.container():
        if message["role"] == "user":
            st.markdown(f"""
                <div class="chat-message user-message">
                    <b>You:</b> {message["content"]}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="chat-message assistant-message">
                    <b>Health Buddy:</b> {message["content"]}
                </div>
            """, unsafe_allow_html=True)

# Chat input
with st.container():
    # Create a form for the chat input
    with st.form("chat_form"):
        user_input = st.text_input("Ask your health question here...", key="user_input")
        submit_button = st.form_submit_button("Send")
        
        if submit_button and user_input:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Get AI response
            response = ask_healthcare_ai(user_input)
            
            # Add AI response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Rerun to update chat display and clear input
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>© 2024 Health Buddy AI | Ask me anything about health!</p>
    </div>
""", unsafe_allow_html=True)

