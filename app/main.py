"""Dadly Streamlit application."""

import streamlit as st
import requests
import json
from datetime import datetime
from typing import List, Optional

# Page config
st.set_page_config(
    page_title="Dadly - Where dad's love becomes memory",
    page_icon="👨‍👩‍👧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .stButton > button {
        width: 100%;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None

# API configuration
API_BASE_URL = "http://localhost:8000"

def send_chat_message(message: str, conversation_id: Optional[str] = None) -> dict:
    """Send chat message to API."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/chat/",
            json={
                "message": message,
                "conversation_id": conversation_id
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API 요청 오류: {str(e)}")
        return None

def main():
    """Main application."""
    # Header
    st.markdown('<h1 class="main-header">👨‍👩‍👧 Dadly</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Where dad\'s love becomes memory</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("💬 채팅 설정")
        
        # New conversation button
        if st.button("🆕 새 대화 시작"):
            st.session_state.messages = []
            st.session_state.conversation_id = None
            st.rerun()
        
        st.divider()
        
        # Conversation info
        if st.session_state.conversation_id:
            st.info(f"대화 ID: {st.session_state.conversation_id[:8]}...")
        
        st.divider()
        
        # About
        st.header("ℹ️ About Dadly")
        st.markdown("""
        Dadly는 아빠가 남긴 기록과 이야기를 가족과 함께 나누고, 
        시간이 흘러도 잊히지 않도록 보존하는 서비스입니다.
        
        AI 어시스턴트와 대화하며 가족의 소중한 추억을 정리하고 
        보존하는 방법을 찾아보세요.
        """)
    
    # Main chat area
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("메시지를 입력하세요..."):
            # Add user message to chat history
            st.session_state.messages.append({
                "role": "user",
                "content": prompt,
                "timestamp": datetime.now().isoformat()
            })
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("AI가 응답을 생성하고 있습니다..."):
                    response = send_chat_message(
                        prompt, 
                        st.session_state.conversation_id
                    )
                    
                    if response:
                        # Update conversation ID
                        if not st.session_state.conversation_id:
                            st.session_state.conversation_id = response["conversation_id"]
                        
                        # Add assistant message to chat history
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response["message"],
                            "timestamp": response["timestamp"]
                        })
                        
                        # Display assistant response
                        st.markdown(response["message"])
                    else:
                        st.error("응답을 받지 못했습니다. 다시 시도해주세요.")

if __name__ == "__main__":
    main()
