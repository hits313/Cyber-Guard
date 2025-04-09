import streamlit as st
import ollama
import time
from datetime import datetime
import requests
import random
import re
import markdown
import html
import json
import os
import uuid

# Page configuration
st.set_page_config(
    page_title="CyberGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Larger, better ASCII Art Logo
ASCII_LOGO = """
 ██████╗██╗   ██╗██████╗ ███████╗██████╗  ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗ 
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║  ███╗██║   ██║███████║██████╔╝██║  ██║
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║
╚██████╗   ██║   ██████╔╝███████╗██║  ██║╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ██╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ 
                                                                                    
                    🛡️ ADVANCED DEVSECOPS & CYBERSECURITY AI 🛡️
"""

# Theme options
THEMES = {
    "midnight": {
        "name": "Midnight",
        "primary_color": "#7C3AED",
        "primary_light": "#8B5CF6",
        "primary_dark": "#6D28D9",
        "secondary_color": "#10B981",
        "bg_color": "#0F172A",
        "card_bg": "#1E293B",
        "sidebar_bg": "#1E293B",
        "text_color": "#E2E8F0",
        "text_muted": "#94A3B8",
        "border_color": "#334155",
        "hover_color": "#2D3748",
        "gradient_start": "rgba(124, 58, 237, 0.05)",
        "gradient_end": "rgba(16, 185, 129, 0.05)",
        "code_bg": "#111827"
    },
    "hacker": {
        "name": "Hacker",
        "primary_color": "#00FF41",
        "primary_light": "#00FF41",
        "primary_dark": "#00CC33",
        "secondary_color": "#00FFFF",
        "bg_color": "#0D0208",
        "card_bg": "#121212",
        "sidebar_bg": "#121212",
        "text_color": "#00FF41",
        "text_muted": "#008F11",
        "border_color": "#008F11",
        "hover_color": "#003B00",
        "gradient_start": "rgba(0, 255, 65, 0.05)",
        "gradient_end": "rgba(0, 255, 255, 0.05)",
        "code_bg": "#0D0208"
    },
    "cyberpunk": {
        "name": "Cyberpunk",
        "primary_color": "#FF00FF",
        "primary_light": "#FF5EFF",
        "primary_dark": "#CC00CC",
        "secondary_color": "#00FFFF",
        "bg_color": "#120458",
        "card_bg": "#1A0B6B",
        "sidebar_bg": "#1A0B6B",
        "text_color": "#F2F2F2",
        "text_muted": "#B8B8B8",
        "border_color": "#FF00FF",
        "hover_color": "#2D0B59",
        "gradient_start": "rgba(255, 0, 255, 0.1)",
        "gradient_end": "rgba(0, 255, 255, 0.1)",
        "code_bg": "#0D0221"
    },
    "nord": {
        "name": "Nord",
        "primary_color": "#88C0D0",
        "primary_light": "#8FBCBB",
        "primary_dark": "#81A1C1",
        "secondary_color": "#A3BE8C",
        "bg_color": "#2E3440",
        "card_bg": "#3B4252",
        "sidebar_bg": "#3B4252",
        "text_color": "#ECEFF4",
        "text_muted": "#D8DEE9",
        "border_color": "#4C566A",
        "hover_color": "#434C5E",
        "gradient_start": "rgba(136, 192, 208, 0.05)",
        "gradient_end": "rgba(163, 190, 140, 0.05)",
        "code_bg": "#2E3440"
    }
}

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm CyberGuard AI, your DevSecOps and cybersecurity assistant. I can help with pentesting, DevSecOps workflows, and coding in Python, Bash, and more. How can I assist you today?"}
    ]

if "user_name" not in st.session_state:
    st.session_state.user_name = "User"

if "typing" not in st.session_state:
    st.session_state.typing = False

if "input_key" not in st.session_state:
    st.session_state.input_key = 0

if "mode" not in st.session_state:
    st.session_state.mode = "standard"  # standard, deep_research, or code_focused

if "chat_history_count" not in st.session_state:
    st.session_state.chat_history_count = 1

if "vulnerability_scans" not in st.session_state:
    st.session_state.vulnerability_scans = 0

if "code_snippets" not in st.session_state:
    st.session_state.code_snippets = 0

if "security_tips" not in st.session_state:
    st.session_state.security_tips = 0

if "last_activity" not in st.session_state:
    st.session_state.last_activity = datetime.now().strftime("%Y-%m-%d %H:%M")

if "theme" not in st.session_state:
    st.session_state.theme = "midnight"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = str(uuid.uuid4())

if "chat_titles" not in st.session_state:
    st.session_state.chat_titles = {}

if "show_welcome_prompts" not in st.session_state:
    st.session_state.show_welcome_prompts = True

# Directory for saving chat history
HISTORY_DIR = "chat_history"
os.makedirs(HISTORY_DIR, exist_ok=True)

# Predefined questions
PREDEFINED_QUESTIONS = [
    "What are the OWASP Top 10 vulnerabilities?",
    "How do I set up a secure CI/CD pipeline?",
    "Explain the concept of DevSecOps",
    "Write a Python script to scan for open ports",
    "What are best practices for secure coding in JavaScript?",
    "How can I implement zero trust architecture?",
    "Explain the difference between penetration testing and vulnerability assessment",
    "What tools should I use for container security?"
]

# Welcome prompts that appear under the ASCII banner
WELCOME_PROMPTS = [
    {"title": "Secure Your Network", "prompt": "What are the essential steps to secure a corporate network?"},
    {"title": "Learn Penetration Testing", "prompt": "I want to learn penetration testing. Where should I start?"},
    {"title": "Secure Coding Practices", "prompt": "What are the most important secure coding practices for web applications?"},
    {"title": "DevSecOps Implementation", "prompt": "How can I implement DevSecOps in my organization's development workflow?"}
]

# Get current theme
current_theme = THEMES[st.session_state.theme]

# Custom CSS for a modern AI bot UI inspired by ChatGPT
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    :root {{
        --primary-color: {current_theme["primary_color"]};
        --primary-light: {current_theme["primary_light"]};
        --primary-dark: {current_theme["primary_dark"]};
        --secondary-color: {current_theme["secondary_color"]};
        --bg-color: {current_theme["bg_color"]};
        --card-bg: {current_theme["card_bg"]};
        --sidebar-bg: {current_theme["sidebar_bg"]};
        --text-color: {current_theme["text_color"]};
        --text-muted: {current_theme["text_muted"]};
        --border-color: {current_theme["border_color"]};
        --hover-color: {current_theme["hover_color"]};
        --gradient-start: {current_theme["gradient_start"]};
        --gradient-end: {current_theme["gradient_end"]};
        --code-bg: {current_theme["code_bg"]};
    }}

    /* Global styles */
    .stApp {{
        background-color: var(--bg-color);
        color: var(--text-color);
        font-family: 'Inter', sans-serif;
        background-image: 
            radial-gradient(circle at 25% 25%, var(--gradient-start) 0%, transparent 50%),
            radial-gradient(circle at 75% 75%, var(--gradient-end) 0%, transparent 50%);
        background-size: 100% 100%;
        background-attachment: fixed;
    }}
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header {{
        visibility: hidden;
    }}
    
    /* Sidebar styling */
    .sidebar .sidebar-content {{
        background-color: var(--sidebar-bg);
    }}
    
    section[data-testid="stSidebar"] {{
        background-color: var(--sidebar-bg);
        border-right: 1px solid var(--border-color);
    }}
    
    section[data-testid="stSidebar"] .block-container {{
        padding-top: 2rem;
    }}
    
    /* Headings */
    h1, h2, h3, h4, h5, h6 {{
        font-weight: 600;
        color: var(--text-color);
    }}
    
    /* ASCII Logo */
    .ascii-logo {{
        font-family: 'JetBrains Mono', monospace;
        white-space: pre;
        font-size: 0.7rem;
        line-height: 1;
        color: var(--primary-light);
        text-align: center;
        margin-bottom: 1rem;
        animation: glow 2s infinite alternate;
    }}
    
    @keyframes glow {{
        from {{ text-shadow: 0 0 5px var(--primary-color); }}
        to {{ text-shadow: 0 0 15px var(--secondary-color); }}
    }}
    
    /* Welcome section */
    .welcome-container {{
        text-align: center;
        margin-bottom: 1.5rem;
        padding: 1.5rem;
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.1), rgba(16, 185, 129, 0.1));
        border: 1px solid rgba(124, 58, 237, 0.2);
        animation: pulse 2s infinite ease-in-out;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }}
    
    @keyframes pulse {{
        0% {{ box-shadow: 0 0 0 0 rgba(124, 58, 237, 0.4); }}
        70% {{ box-shadow: 0 0 0 10px rgba(124, 58, 237, 0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(124, 58, 237, 0); }}
    }}
    
    .welcome-title {{
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        margin-bottom: 0.5rem;
    }}
    
    .welcome-subtitle {{
        font-size: 1.1rem;
        color: var(--text-muted);
        margin-bottom: 1rem;
    }}
    
    /* Main layout */
    .main-layout {{
        display: flex;
        flex-direction: column;
        height: 85vh;
    }}
    
    /* Dashboard layout */
    .dashboard-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-bottom: 1.5rem;
    }}
    
    @media (max-width: 992px) {{
        .dashboard-grid {{
            grid-template-columns: repeat(2, 1fr);
        }}
    }}
    
    @media (max-width: 768px) {{
        .dashboard-grid {{
            grid-template-columns: 1fr;
        }}
    }}
    
    .dashboard-card {{
        background-color: var(--card-bg);
        border-radius: 12px;
        border: 1px solid var(--border-color);
        padding: 1.25rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }}
    
    .dashboard-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        border-color: var(--primary-color);
    }}
    
    .dashboard-card-header {{
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
    }}
    
    .dashboard-card-icon {{
        width: 40px;
        height: 40px;
        border-radius: 10px;
        background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 1rem;
        font-size: 1.25rem;
        color: white;
    }}
    
    .dashboard-card-title {{
        font-weight: 600;
        font-size: 1.1rem;
        color: var(--text-color);
    }}
    
    .dashboard-card-content {{
        flex-grow: 1;
        color: var(--text-muted);
        font-size: 0.9rem;
        line-height: 1.5;
    }}
    
    .dashboard-card-footer {{
        margin-top: 1rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    
    .dashboard-card-stat {{
        font-size: 0.85rem;
        color: var(--text-muted);
    }}
    
    .dashboard-card-action {{
        font-size: 0.85rem;
        color: var(--primary-light);
        text-decoration: none;
        display: flex;
        align-items: center;
        cursor: pointer;
    }}
    
    .dashboard-card-action:hover {{
        color: var(--secondary-color);
    }}
    
    /* Chat container */
    .chat-container {{
        background-color: var(--card-bg);
        border-radius: 16px;
        border: 1px solid var(--border-color);
        padding: 1rem;
        flex-grow: 1;
        overflow-y: auto;
        margin-bottom: 1rem;
        scrollbar-width: thin;
        scrollbar-color: var(--primary-light) var(--card-bg);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }}
    
    .chat-container::-webkit-scrollbar {{
        width: 6px;
    }}
    
    .chat-container::-webkit-scrollbar-track {{
        background: var(--card-bg);
    }}
    
    .chat-container::-webkit-scrollbar-thumb {{
        background-color: var(--primary-light);
        border-radius: 3px;
    }}
    
    /* Message bubbles */
    .message {{
        display: flex;
        margin-bottom: 1.5rem;
        animation: fadeIn 0.3s ease-in-out;
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .message-content {{
        padding: 1rem;
        border-radius: 16px;
        max-width: 80%;
        line-height: 1.5;
    }}
    
    .user-message {{
        margin-left: auto;
        background-color: var(--primary-color);
        color: white;
        border-top-right-radius: 4px;
    }}
    
    .assistant-message {{
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        color: var(--text-color);
        border-top-left-radius: 4px;
    }}
    
    .avatar {{
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 1rem;
        margin: 0 0.75rem;
        flex-shrink: 0;
    }}
    
    .user-avatar {{
        background-color: var(--primary-dark);
        color: white;
    }}
    
    .assistant-avatar {{
        background-color: var(--secondary-color);
        color: white;
    }}
    
    /* Input area */
    .input-container {{
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 0.5rem;
        display: flex;
        align-items: center;
        margin-top: 1rem;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        position: relative;
    }}
    
    .input-container:focus-within {{
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.2);
    }}
    
    .stTextInput > div > div {{
        background-color: transparent;
        color: var(--text-color);
    }}
    
    .stTextInput > div > div > input {{
        color: var(--text-color);
    }}
    
    /* Buttons */
    .stButton > button {{
        background: linear-gradient(90deg, var(--primary-color), var(--primary-light));
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
    }}
    
    /* Status indicators */
    .status-indicator {{
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }}
    
    .status-online {{
        background-color: var(--secondary-color);
        box-shadow: 0 0 5px var(--secondary-color);
    }}
    
    .status-offline {{
        background-color: #EF4444;
        box-shadow: 0 0 5px #EF4444;
    }}
    
    /* Expanders */
    .streamlit-expanderHeader {{
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        color: var(--text-color);
        font-weight: 500;
    }}
    
    .streamlit-expanderContent {{
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-top: none;
        border-bottom-left-radius: 8px;
        border-bottom-right-radius: 8px;
        padding: 1rem;
    }}
    
    /* Enhanced Markdown styling */
    .enhanced-markdown h1 {{
        font-size: 1.8rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        padding-bottom: 0.3rem;
        border-bottom: 1px solid var(--border-color);
    }}
    
    .enhanced-markdown h2 {{
        font-size: 1.5rem;
        margin-top: 1.2rem;
        margin-bottom: 0.8rem;
        color: var(--text-color);
    }}
    
    .enhanced-markdown h3 {{
        font-size: 1.2rem;
        margin-top: 1rem;
        margin-bottom: 0.6rem;
        color: var(--text-color);
    }}
    
    .enhanced-markdown p {{
        margin-bottom: 1rem;
        line-height: 1.6;
    }}
    
    .enhanced-markdown ul, .enhanced-markdown ol {{
        margin-bottom: 1rem;
        margin-left: 1.5rem;
    }}
    
    .enhanced-markdown li {{
        margin-bottom: 0.5rem;
    }}
    
    .enhanced-markdown a {{
        color: var(--primary-light);
        text-decoration: none;
        border-bottom: 1px dashed var(--primary-light);
        transition: all 0.2s ease;
    }}
    
    .enhanced-markdown a:hover {{
        color: var(--secondary-color);
        border-bottom: 1px solid var(--secondary-color);
    }}
    
    .enhanced-markdown blockquote {{
        border-left: 4px solid var(--primary-light);
        padding-left: 1rem;
        margin-left: 0;
        margin-right: 0;
        font-style: italic;
        color: var(--text-muted);
    }}
    
    .enhanced-markdown table {{
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 1rem;
    }}
    
    .enhanced-markdown th, .enhanced-markdown td {{
        padding: 0.5rem;
        border: 1px solid var(--border-color);
    }}
    
    .enhanced-markdown th {{
        background-color: rgba(124, 58, 237, 0.1);
    }}
    
    .enhanced-markdown tr:nth-child(even) {{
        background-color: rgba(255, 255, 255, 0.05);
    }}
    
    /* Code blocks */
    .enhanced-markdown code {{
        font-family: 'JetBrains Mono', monospace;
        background-color: var(--code-bg);
        color: #A5B4FC;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-size: 0.9rem;
    }}
    
    .enhanced-markdown pre {{
        background-color: var(--code-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 1rem;
        overflow-x: auto;
        margin-bottom: 1rem;
    }}
    
    .enhanced-markdown pre code {{
        background-color: transparent;
        padding: 0;
        font-size: 0.9rem;
        color: var(--text-color);
        display: block;
        line-height: 1.6;
    }}
    
    /* Syntax highlighting */
    .enhanced-markdown .keyword {{ color: #FF79C6; }}
    .enhanced-markdown .function {{ color: #50FA7B; }}
    .enhanced-markdown .string {{ color: #F1FA8C; }}
    .enhanced-markdown .number {{ color: #BD93F9; }}
    .enhanced-markdown .comment {{ color: #6272A4; }}
    
    /* Typing indicator */
    .typing-indicator {{
        display: flex;
        align-items: center;
        margin-left: 1rem;
    }}
    
    .typing-dot {{
        width: 8px;
        height: 8px;
        background-color: var(--text-muted);
        border-radius: 50%;
        margin: 0 2px;
        animation: typingAnimation 1.4s infinite ease-in-out;
    }}
    
    .typing-dot:nth-child(1) {{ animation-delay: 0s; }}
    .typing-dot:nth-child(2) {{ animation-delay: 0.2s; }}
    .typing-dot:nth-child(3) {{ animation-delay: 0.4s; }}
    
    @keyframes typingAnimation {{
        0%, 60%, 100% {{ transform: translateY(0); }}
        30% {{ transform: translateY(-5px); }}
    }}
    
    /* Selectbox */
    .stSelectbox > div > div {{
        background-color: var(--card-bg);
        color: var(--text-color);
        border: 1px solid var(--border-color);
        border-radius: 8px;
    }}
    
    /* Checkbox */
    .stCheckbox > label {{
        color: var(--text-color);
    }}
    
    /* Links */
    a {{
        color: var(--primary-light);
        text-decoration: none;
        transition: color 0.2s ease;
    }}
    
    a:hover {{
        color: var(--secondary-color);
        text-decoration: underline;
    }}
    
    /* Feature cards */
    .feature-card {{
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    
    .feature-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    }}
    
    .feature-icon {{
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
        color: var(--primary-color);
    }}
    
    /* Mode selector */
    .mode-selector {{
        display: flex;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }}
    
    .mode-option {{
        flex: 1;
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 0.75rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s ease;
    }}
    
    .mode-option:hover {{
        border-color: var(--primary-light);
    }}
    
    .mode-option.active {{
        background-color: rgba(124, 58, 237, 0.2);
        border-color: var(--primary-color);
    }}
    
    .mode-icon {{
        font-size: 1.25rem;
        margin-bottom: 0.5rem;
    }}
    
    .mode-label {{
        font-size: 0.9rem;
        font-weight: 500;
    }}
    
    /* Stats card */
    .stats-card {{
        display: flex;
        align-items: center;
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        transition: transform 0.2s ease;
    }}
    
    .stats-card:hover {{
        transform: translateY(-3px);
        border-color: var(--primary-light);
    }}
    
    .stats-icon {{
        width: 48px;
        height: 48px;
        border-radius: 12px;
        background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        color: white;
        margin-right: 1rem;
    }}
    
    .stats-content {{
        flex-grow: 1;
    }}
    
    .stats-value {{
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-color);
    }}
    
    .stats-label {{
        font-size: 0.9rem;
        color: var(--text-muted);
    }}
    
    /* Progress bar */
    .progress-container {{
        margin-top: 0.5rem;
    }}
    
    .progress-bar {{
        height: 6px;
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 3px;
        overflow: hidden;
    }}
    
    .progress-fill {{
        height: 100%;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        border-radius: 3px;
        transition: width 0.5s ease;
    }}
    
    /* Tooltip */
    .tooltip {{
        position: relative;
        display: inline-block;
        cursor: pointer;
    }}
    
    .tooltip .tooltiptext {{
        visibility: hidden;
        width: 200px;
        background-color: var(--card-bg);
        color: var(--text-color);
        text-align: center;
        border-radius: 8px;
        padding: 0.5rem;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
        border: 1px solid var(--border-color);
        font-size: 0.9rem;
    }}
    
    .tooltip:hover .tooltiptext {{
        visibility: visible;
        opacity: 1;
    }}
    
    /* Tags */
    .tag {{
        display: inline-block;
        background-color: rgba(124, 58, 237, 0.2);
        color: var(--primary-light);
        border-radius: 4px;
        padding: 0.2rem 0.5rem;
        font-size: 0.8rem;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }}
    
    /* Footer */
    .footer {{
        text-align: center;
        margin-top: 1rem;
        padding: 1rem;
        color: var(--text-muted);
        font-size: 0.8rem;
        border-top: 1px solid var(--border-color);
    }}
    
    /* Mode badge */
    .mode-badge {{
        display: inline-flex;
        align-items: center;
        background-color: rgba(124, 58, 237, 0.2);
        color: var(--primary-light);
        border-radius: 9999px;
        padding: 0.25rem 0.75rem;
        font-size: 0.8rem;
        font-weight: 500;
        margin-left: 0.5rem;
    }}
    
    .mode-badge-icon {{
        margin-right: 0.25rem;
    }}
    
    /* Glow effect */
    .glow-effect {{
        position: relative;
    }}
    
    .glow-effect::after {{
        content: "";
        position: absolute;
        top: -10px;
        left: -10px;
        right: -10px;
        bottom: -10px;
        z-index: -1;
        background: radial-gradient(circle, var(--primary-color) 0%, transparent 70%);
        opacity: 0.15;
        border-radius: 16px;
        animation: glow-pulse 3s infinite alternate;
    }}
    
    @keyframes glow-pulse {{
        0% {{ opacity: 0.1; }}
        100% {{ opacity: 0.2; }}
    }}
    
    /* Chat history sidebar */
    .chat-history-item {{
        display: flex;
        align-items: center;
        padding: 0.75rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        cursor: pointer;
        transition: all 0.2s ease;
        border: 1px solid transparent;
    }}
    
    .chat-history-item:hover {{
        background-color: var(--hover-color);
        border-color: var(--border-color);
    }}
    
    .chat-history-item.active {{
        background-color: rgba(124, 58, 237, 0.2);
        border-color: var(--primary-color);
    }}
    
    .chat-history-icon {{
        width: 32px;
        height: 32px;
        border-radius: 8px;
        background-color: var(--primary-dark);
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 0.75rem;
        font-size: 1rem;
        color: white;
    }}
    
    .chat-history-content {{
        flex-grow: 1;
        overflow: hidden;
    }}
    
    .chat-history-title {{
        font-size: 0.9rem;
        font-weight: 500;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        color: var(--text-color);
    }}
    
    .chat-history-date {{
        font-size: 0.75rem;
        color: var(--text-muted);
    }}
    
    /* Predefined questions */
    .predefined-questions {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 1rem;
    }}
    
    .predefined-question {{
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 0.5rem 1rem;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.2s ease;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 100%;
    }}
    
    .predefined-question:hover {{
        background-color: var(--hover-color);
        border-color: var(--primary-color);
        transform: translateY(-2px);
    }}
    
    /* Cursor animation */
    .cursor {{
        display: inline-block;
        width: 2px;
        height: 1em;
        background-color: var(--primary-light);
        margin-left: 2px;
        animation: cursor-blink 1s infinite;
        vertical-align: text-bottom;
    }}
    
    @keyframes cursor-blink {{
        0%, 49% {{ opacity: 1; }}
        50%, 100% {{ opacity: 0; }}
    }}
    
    /* Theme selector */
    .theme-selector {{
        display: flex;
        gap: 0.5rem;
        margin-bottom: 1rem;
        flex-wrap: wrap;
    }}
    
    .theme-option {{
        width: 32px;
        height: 32px;
        border-radius: 50%;
        cursor: pointer;
        transition: all 0.2s ease;
        border: 2px solid var(--border-color);
        position: relative;
    }}
    
    .theme-option:hover {{
        transform: scale(1.1);
    }}
    
    .theme-option.active {{
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px var(--primary-color);
    }}
    
    .theme-option.active::after {{
        content: "✓";
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: white;
        font-size: 0.8rem;
        font-weight: bold;
    }}
    
    /* New chat button */
    .new-chat-btn {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        background-color: var(--primary-color);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        width: 100%;
        margin-bottom: 1rem;
    }}
    
    .new-chat-btn:hover {{
        background-color: var(--primary-dark);
        transform: translateY(-2px);
    }}
    
    /* Welcome prompts */
    .welcome-prompts-grid {{
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        margin: 1.5rem 0;
    }}
    
    @media (max-width: 768px) {{
        .welcome-prompts-grid {{
            grid-template-columns: 1fr;
        }}
    }}
    
    .welcome-prompt-card {{
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.25rem;
        cursor: pointer;
        transition: all 0.2s ease;
        height: 100%;
    }}
    
    .welcome-prompt-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        border-color: var(--primary-color);
    }}
    
    .welcome-prompt-title {{
        font-weight: 600;
        font-size: 1.1rem;
        color: var(--text-color);
        margin-bottom: 0.5rem;
    }}
    
    .welcome-prompt-text {{
        color: var(--text-muted);
        font-size: 0.9rem;
    }}
    
    /* Footer */
    .footer {{
        text-align: center;
        margin-top: 1rem;
        padding: 1rem;
        color: var(--text-muted);
        font-size: 0.8rem;
        border-top: 1px solid var(--border-color);
    }}
    </style>
""", unsafe_allow_html=True)

# Enhanced markdown rendering with better syntax highlighting
def render_markdown(text):
    # Process code blocks with syntax highlighting
    code_pattern = r'\`\`\`(\w+)?\n(.*?)\n\`\`\`'
    
    def code_replace(match):
        lang = match.group(1) or ''
        code = match.group(2)
        
        # Apply syntax highlighting based on language
        if lang.lower() in ['python', 'py']:
            # Python syntax highlighting
            code = re.sub(r'\b(def|class|import|from|return|if|else|elif|for|while|try|except|with|as|in|and|or|not|True|False|None)\b', r'<span class="keyword">\1</span>', code)
            code = re.sub(r'(\'.*?\'|\".*?\")', r'<span class="string">\1</span>', code)
            code = re.sub(r'\b(\d+)\b', r'<span class="number">\1</span>', code)
            code = re.sub(r'(#.*)', r'<span class="comment">\1</span>', code, flags=re.MULTILINE)
            code = re.sub(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\(', r'<span class="function">\1</span>(', code)
        elif lang.lower() in ['bash', 'sh']:
            # Bash syntax highlighting
            code = re.sub(r'\b(if|then|else|fi|for|do|done|while|case|esac|function|in|echo|exit|return|set)\b', r'<span class="keyword">\1</span>', code)
            code = re.sub(r'(\'.*?\'|\".*?\")', r'<span class="string">\1</span>', code)
            code = re.sub(r'\b(\d+)\b', r'<span class="number">\1</span>', code)
            code = re.sub(r'(#.*)', r'<span class="comment">\1</span>', code, flags=re.MULTILINE)
            code = re.sub(r'\$\{?([a-zA-Z0-9_]+)\}?', r'<span class="function">\$\1</span>', code)
        elif lang.lower() in ['javascript', 'js']:
            # JavaScript syntax highlighting
            code = re.sub(r'\b(var|let|const|function|return|if|else|for|while|try|catch|class|import|export|from|default|async|await)\b', r'<span class="keyword">\1</span>', code)
            code = re.sub(r'(\'.*?\'|\".*?\"|\`.*?\`)', r'<span class="string">\1</span>', code)
            code = re.sub(r'\b(\d+)\b', r'<span class="number">\1</span>', code)
            code = re.sub(r'(\/\/.*)', r'<span class="comment">\1</span>', code, flags=re.MULTILINE)
            code = re.sub(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\(', r'<span class="function">\1</span>(', code)
        
        return f'<pre><code class="{lang}">{code}</code></pre>'
    
    # Replace code blocks
    text = re.sub(code_pattern, code_replace, text, flags=re.DOTALL)
    
    # Convert markdown to HTML
    html_content = markdown.markdown(
        text,
        extensions=['tables', 'fenced_code', 'codehilite', 'nl2br']
    )
    
    return f'<div class="enhanced-markdown">{html_content}</div>'

# Animated typing indicator
def typing_indicator():
    return """
    <div class="typing-indicator">
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
    </div>
    """

# Welcome section with time-based greeting
def display_welcome():
    current_hour = datetime.now().hour
    if current_hour < 12:
        greeting = "Good morning"
    elif current_hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    
    name = st.session_state.user_name
    
    # Display ASCII logo
    st.markdown(f'<div class="ascii-logo">{ASCII_LOGO}</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="welcome-container">
        <div class="welcome-title">{greeting}, {name}</div>
        <div class="welcome-subtitle">Your AI-powered DevSecOps and Cybersecurity Companion</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display welcome prompts if this is a new chat
    if st.session_state.show_welcome_prompts and len(st.session_state.messages) <= 1:
        st.markdown('<div class="welcome-prompts-grid">', unsafe_allow_html=True)
        
        for i, prompt in enumerate(WELCOME_PROMPTS):
            prompt_id = f"welcome_prompt_{i}"
            st.markdown(f"""
            <div class="welcome-prompt-card" id="{prompt_id}">
                <div class="welcome-prompt-title">{prompt['title']}</div>
                <div class="welcome-prompt-text">{prompt['prompt']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Add a hidden button to handle the click
            if st.button(prompt['title'], key=prompt_id):
                # Add user message to chat
                st.session_state.messages.append({"role": "user", "content": prompt['prompt']})
                
                # Hide welcome prompts after selection
                st.session_state.show_welcome_prompts = False
                
                # Generate and display response
                response = generate_response(prompt['prompt'], "llama3", mode=st.session_state.mode)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Save chat to history
                save_chat_to_history()
                
                # Increment the input key to create a fresh input field
                st.session_state.input_key += 1
                
                # Rerun to update UI
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# Check Ollama server status
def check_ollama_server():
    try:
        response = requests.get("http://127.0.0.1:11434", timeout=3)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Display chat messages with enhanced markdown
def display_messages():
    for idx, message in enumerate(st.session_state.messages):
        if message["role"] == "user":
            st.markdown(f"""
            <div class="message">
                <div style="flex-grow: 1;"></div>
                <div class="message-content user-message">{message["content"]}</div>
                <div class="avatar user-avatar">{st.session_state.user_name[0].upper()}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Apply enhanced markdown to assistant messages
            formatted_content = render_markdown(message["content"])
            
            # Add mode badge for assistant messages
            mode_badges = {
                "standard": "",
                "deep_research": '<span class="mode-badge"><span class="mode-badge-icon">🔍</span>Deep Research</span>',
                "code_focused": '<span class="mode-badge"><span class="mode-badge-icon">💻</span>Code-Focused</span>'
            }
            
            # Only add badge if it's not the first welcome message
            mode_badge = mode_badges[st.session_state.mode] if idx > 0 else ""
            
            st.markdown(f"""
            <div class="message">
                <div class="avatar assistant-avatar">AI</div>
                <div class="message-content assistant-message">{formatted_content}{mode_badge}</div>
                <div style="flex-grow: 1;"></div>
            </div>
            """, unsafe_allow_html=True)
    
    # Show typing indicator if active
    if st.session_state.typing:
        st.markdown(f"""
        <div class="message">
            <div class="avatar assistant-avatar">AI</div>
            {typing_indicator()}
            <div style="flex-grow: 1;"></div>
        </div>
        """, unsafe_allow_html=True)

# Generate response with streaming effect
def generate_response(prompt, selected_model, mode="standard"):
    st.session_state.typing = True
    
    # Increment stats based on prompt content
    if any(term in prompt.lower() for term in ["vulnerability", "scan", "security", "pentest"]):
        st.session_state.vulnerability_scans += 1
    if "\`\`\`" in prompt or any(term in prompt.lower() for term in ["code", "script", "function", "class"]):
        st.session_state.code_snippets += 1
    if any(term in prompt.lower() for term in ["best practice", "secure", "protect", "defense"]):
        st.session_state.security_tips += 1
    
    # Update last activity timestamp
    st.session_state.last_activity = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Different system prompts based on mode
    if mode == "deep_research":
        system_prompt = """
        You are CyberGuard AI in Deep Research mode. Provide comprehensive, well-researched answers with academic depth.
        Include relevant technical details, methodologies, tools, and best practices. Cite sources where appropriate.
        Structure your responses with clear headings, bullet points, and code examples when relevant.
        Focus on providing thorough explanations that would satisfy security professionals and researchers.
        Use markdown formatting to organize your response with sections, subsections, and proper formatting.
        """
    elif mode == "code_focused":
        system_prompt = """
        You are CyberGuard AI in Code-Focused mode. Prioritize providing working, production-ready code examples.
        Include detailed comments, error handling, and security best practices in all code.
        Explain the code's functionality and potential security implications.
        Format code with proper syntax highlighting and follow language-specific conventions.
        Provide complete, executable code snippets that can be copied and used directly.
        Always include usage examples and expected outputs where appropriate.
        """
    else:  # standard mode
        system_prompt = """
        You are CyberGuard AI, an advanced assistant for cybersecurity, penetration testing, and DevSecOps. 
        Provide detailed, practical, and professional answers on pentesting tools, techniques, and methodologies.
        For DevSecOps, assist with secure coding, CI/CD pipeline security, infrastructure as code (IaC), and automation scripts.
        Include examples, commands, and best practices. Format code in Markdown code blocks.
        Use a professional tone with a modern, tech-savvy flair.
        """

    message_placeholder = st.empty()
    full_response = ""
    
    try:
        # Simulate typing delay for a more natural feel
        time.sleep(0.5)
        
        response = ollama.chat(
            model=selected_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            stream=True
        )
        
        for chunk in response:
            if 'message' in chunk and 'content' in chunk['message']:
                content = chunk['message']['content']
                full_response += content
                
                # Add a slight random delay to simulate natural typing
                time.sleep(random.uniform(0.01, 0.03))
                
                # Update with cursor effect and enhanced markdown
                formatted_response = render_markdown(full_response)
                
                # Add mode badge
                mode_badges = {
                    "standard": "",
                    "deep_research": '<span class="mode-badge"><span class="mode-badge-icon">🔍</span>Deep Research</span>',
                    "code_focused": '<span class="mode-badge"><span class="mode-badge-icon">💻</span>Code-Focused</span>'
                }
                
                message_placeholder.markdown(f"""
                <div class="message">
                    <div class="avatar assistant-avatar">AI</div>
                    <div class="message-content assistant-message">{formatted_response}{mode_badges[mode]}<span class="cursor"></span></div>
                    <div style="flex-grow: 1;"></div>
                </div>
                """, unsafe_allow_html=True)
        
        # Final update without cursor
        formatted_response = render_markdown(full_response)
        message_placeholder.markdown(f"""
        <div class="message">
            <div class="avatar assistant-avatar">AI</div>
            <div class="message-content assistant-message">{formatted_response}{mode_badges[mode]}</div>
            <div style="flex-grow: 1;"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Update chat title if this is the first message
        if len(st.session_state.messages) == 1:  # Only welcome message exists
            # Extract a title from the prompt
            title = prompt[:30] + "..." if len(prompt) > 30 else prompt
            st.session_state.chat_titles[st.session_state.current_chat_id] = title
            
            # Save chat to history
            save_chat_to_history()
        
    except Exception as e:
        error_message = f"""
        ⚠️ **Connection Error**
        
        Failed to connect to the Ollama server: {str(e)}
        
        Please ensure:
        1. Ollama server is running (`ollama serve`)
        2. The model '{selected_model}' is available (`ollama pull {selected_model}`)
        3. Port 11434 is accessible
        """
        full_response = error_message
        formatted_response = render_markdown(full_response)
        message_placeholder.markdown(f"""
        <div class="message">
            <div class="avatar assistant-avatar">AI</div>
            <div class="message-content assistant-message">{formatted_response}</div>
            <div style="flex-grow: 1;"></div>
        </div>
        """, unsafe_allow_html=True)
    
    st.session_state.typing = False
    st.session_state.chat_history_count += 1
    return full_response

# Save chat to history
def save_chat_to_history():
    chat_data = {
        "id": st.session_state.current_chat_id,
        "title": st.session_state.chat_titles.get(st.session_state.current_chat_id, "New Chat"),
        "messages": st.session_state.messages,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "mode": st.session_state.mode
    }
    
    # Save to file
    file_path = os.path.join(HISTORY_DIR, f"{st.session_state.current_chat_id}.json")
    with open(file_path, 'w') as f:
        json.dump(chat_data, f)
    
    # Update chat history list if not already there
    if st.session_state.current_chat_id not in [chat["id"] for chat in st.session_state.chat_history]:
        st.session_state.chat_history.append({
            "id": st.session_state.current_chat_id,
            "title": chat_data["title"],
            "timestamp": chat_data["timestamp"]
        })

# Load chat from history
def load_chat_from_history(chat_id):
    file_path = os.path.join(HISTORY_DIR, f"{chat_id}.json")
    try:
        with open(file_path, 'r') as f:
            chat_data = json.load(f)
            
        st.session_state.current_chat_id = chat_id
        st.session_state.messages = chat_data["messages"]
        st.session_state.mode = chat_data.get("mode", "standard")
        st.session_state.show_welcome_prompts = False
        
        return True
    except Exception as e:
        st.error(f"Failed to load chat: {str(e)}")
        return False

# Create new chat
def create_new_chat():
    st.session_state.current_chat_id = str(uuid.uuid4())
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm CyberGuard AI, your DevSecOps and cybersecurity assistant. I can help with pentesting, DevSecOps workflows, and coding in Python, Bash, and more. How can I assist you today?"}
    ]
    st.session_state.chat_titles[st.session_state.current_chat_id] = "New Chat"
    st.session_state.input_key += 1
    st.session_state.show_welcome_prompts = True

# Load chat history
def load_chat_history():
    try:
        # Get all JSON files in the history directory
        history_files = [f for f in os.listdir(HISTORY_DIR) if f.endswith('.json')]
        
        chat_history = []
        for file_name in history_files:
            file_path = os.path.join(HISTORY_DIR, file_name)
            with open(file_path, 'r') as f:
                chat_data = json.load(f)
                
            chat_history.append({
                "id": chat_data["id"],
                "title": chat_data["title"],
                "timestamp": chat_data["timestamp"]
            })
        
        # Sort by timestamp (newest first)
        chat_history.sort(key=lambda x: datetime.strptime(x["timestamp"], "%Y-%m-%d %H:%M"), reverse=True)
        
        return chat_history
    except Exception as e:
        st.error(f"Failed to load chat history: {str(e)}")
        return []

# Initialize chat history if empty
if not st.session_state.chat_history:
    st.session_state.chat_history = load_chat_history()

# Sidebar with modern styling
with st.sidebar:
    st.markdown("""
    <h1 style="display: flex; align-items: center; margin-bottom: 1.5rem;">
        <span style="font-size: 2rem; margin-right: 0.5rem;">🛡️</span> CyberGuard AI
    </h1>
    """, unsafe_allow_html=True)
    
    # New chat button
    if st.button("+ New Chat", key="new_chat_btn"):
        create_new_chat()
        st.rerun()
    
    # Chat history
    st.subheader("💬 Chat History")
    
    if not st.session_state.chat_history:
        st.info("No chat history yet. Start a new conversation!")
    else:
        for chat in st.session_state.chat_history:
            # Create a unique key for each chat
            chat_key = f"chat_{chat['id']}"
            
            # Check if this is the active chat
            is_active = chat["id"] == st.session_state.current_chat_id
            active_class = "active" if is_active else ""
            
            # Display chat history item
            st.markdown(f"""
            <div class="chat-history-item {active_class}" id="{chat_key}">
                <div class="chat-history-icon">💬</div>
                <div class="chat-history-content">
                    <div class="chat-history-title">{chat["title"]}</div>
                    <div class="chat-history-date">{chat["timestamp"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Add a hidden button to handle the click
            if st.button("Load", key=chat_key, help=f"Load chat: {chat['title']}"):
                load_chat_from_history(chat["id"])
                st.rerun()
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Server status with indicator
    server_status = check_ollama_server()
    status_color = "status-online" if server_status else "status-offline"
    status_text = "Online" if server_status else "Offline"
    
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
        <span class="status-indicator {status_color}"></span>
        <span>Ollama Server: <strong>{status_text}</strong></span>
    </div>
    """, unsafe_allow_html=True)
    
    if not server_status:
        st.error("Please launch 'ollama serve' in a terminal to connect.")
    
    # User settings
    with st.expander("👤 User Settings", expanded=False):
        name_input = st.text_input("Your Name", value=st.session_state.user_name)
        if st.button("Save Name"):
            st.session_state.user_name = name_input if name_input else "User"
            st.success(f"Name updated to {st.session_state.user_name}!")
    
    # Theme selector
    st.subheader("🎨 Theme")
    
    # Create theme selector
    theme_cols = st.columns(4)
    for i, (theme_id, theme) in enumerate(THEMES.items()):
        with theme_cols[i % 4]:
            # Create a colored circle for each theme
            active_class = "active" if st.session_state.theme == theme_id else ""
            st.markdown(f"""
            <div class="theme-option {active_class}" 
                 style="background: linear-gradient(135deg, {theme['primary_color']}, {theme['secondary_color']});"
                 id="theme_{theme_id}">
            </div>
            """, unsafe_allow_html=True)
            
            # Add a hidden button to handle the click
            if st.button(theme["name"], key=f"theme_btn_{theme_id}", help=f"Switch to {theme['name']} theme"):
                st.session_state.theme = theme_id
                st.rerun()
    
    # Model selection
    st.subheader("🤖 Model Settings")
    
    # Get available models or use default
    default_model = "llama3"
    try:
        if server_status:
            response = ollama.list()
            available_models = [m['name'] for m in response.get('models', [])]
            if not available_models:
                available_models = ["llama3"]
                st.warning("No models found. Defaulting to 'llama3'.")
        else:
            available_models = ["llama3"]
    except Exception:
        available_models = ["llama3"]
        st.warning("Failed to fetch models. Defaulting to 'llama3'.")
    
    # Ensure default model is in the list
    if default_model not in available_models:
        available_models.append(default_model)
    
    model = st.selectbox(
        "Select AI Model",
        available_models,
        index=available_models.index(default_model) if default_model in available_models else 0
    )
    
    # AI Mode Selection
    st.subheader("🧠 AI Mode")
    
    # Create radio buttons for mode selection that actually work
    mode_selected = st.radio(
        "Select Mode",
        ["standard", "deep_research", "code_focused"],
        index=["standard", "deep_research", "code_focused"].index(st.session_state.mode),
        format_func=lambda x: {
            "standard": "Standard",
            "deep_research": "Deep Research",
            "code_focused": "Code-Focused"
        }[x]
    )
    
    # Update session state if mode changed
    if mode_selected != st.session_state.mode:
        st.session_state.mode = mode_selected
    
    # Mode descriptions
    mode_descriptions = {
        "standard": "Balanced responses for general cybersecurity questions",
        "deep_research": "Comprehensive, well-researched answers with academic depth",
        "code_focused": "Prioritizes code examples and implementation details"
    }
    
    # Display current mode description
    st.markdown(f"""
    <div style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 1.5rem;">
        {mode_descriptions[st.session_state.mode]}
    </div>
    """, unsafe_allow_html=True)
    
    # Resources section
    st.markdown("""
    <h3 style="margin-top: 1rem; margin-bottom: 1rem;">📚 Quick Resources</h3>
    """, unsafe_allow_html=True)
    
    resources = [
        {"name": "Nmap Guide", "url": "https://nmap.org/docs.html", "icon": "🔍"},
        {"name": "OWASP Top 10", "url": "https://owasp.org/www-project-top-ten/", "icon": "🔒"},
        {"name": "DevSecOps Practices", "url": "https://www.redhat.com/en/topics/devops/what-is-devsecops", "icon": "🔄"},
        {"name": "Metasploit Basics", "url": "https://www.metasploit.com/", "icon": "🛠️"}
    ]
    
    for resource in resources:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">{resource["icon"]}</div>
            <a href="{resource["url"]}" target="_blank">{resource["name"]}</a>
        </div>
        """, unsafe_allow_html=True)

# Main chat interface - restructured to use space above
main_container = st.container()
if st.button("📄 Download Chat Log"):
    chat_log = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.messages])
    st.download_button("📥 Save Chat as TXT", data=chat_log, file_name="chat_log.txt")

with main_container:
    # Welcome message with ASCII art logo
    display_welcome()
    
    # Dashboard cards to utilize empty space
    st.markdown('<div class="dashboard-grid">', unsafe_allow_html=True)
    
    # Card 1: Chat Statistics
    st.markdown(f"""
    <div class="dashboard-card glow-effect">
        <div class="dashboard-card-header">
            <div class="dashboard-card-icon">📊</div>
            <div class="dashboard-card-title">Chat Statistics</div>
        </div>
        <div class="dashboard-card-content">
            Track your interaction history and engagement with CyberGuard AI.
            <div style="margin-top: 0.75rem;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span>Total Messages</span>
                    <span>{st.session_state.chat_history_count}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span>Last Activity</span>
                    <span>{st.session_state.last_activity}</span>
                </div>
            </div>
        </div>
        <div class="dashboard-card-footer">
            <div class="dashboard-card-stat">Active Mode: {st.session_state.mode.replace("_", " ").title()}</div>
            <div class="dashboard-card-action">View History →</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Card 2: Security Tools
    st.markdown("""
    <div class="dashboard-card glow-effect">
        <div class="dashboard-card-header">
            <div class="dashboard-card-icon">🛠️</div>
            <div class="dashboard-card-title">Security Toolkit</div>
        </div>
        <div class="dashboard-card-content">
            Access common security tools and get guidance on using them effectively.
            <div style="margin-top: 0.75rem;">
                <span class="tag">Nmap</span>
                <span class="tag">Metasploit</span>
                <span class="tag">OWASP ZAP</span>
                <span class="tag">Burp Suite</span>
                <span class="tag">Wireshark</span>
                <span class="tag">Kali Linux</span>
            </div>
        </div>
        <div class="dashboard-card-footer">
            <div class="dashboard-card-stat">Tools: 15+</div>
            <div class="dashboard-card-action">Explore Tools →</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Card 3: Learning Resources
    st.markdown(f"""
    <div class="dashboard-card glow-effect">
        <div class="dashboard-card-header">
            <div class="dashboard-card-icon">📚</div>
            <div class="dashboard-card-title">Learning Path</div>
        </div>
        <div class="dashboard-card-content">
            Follow structured learning paths to master cybersecurity and DevSecOps skills.
            <div class="progress-container" style="margin-top: 0.75rem;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                    <span style="font-size: 0.8rem;">DevSecOps Fundamentals</span>
                    <span style="font-size: 0.8rem;">45%</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: 45%;"></div>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 0.5rem; margin-bottom: 0.25rem;">
                    <span style="font-size: 0.8rem;">Penetration Testing</span>
                    <span style="font-size: 0.8rem;">30%</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: 30%;"></div>
                </div>
            </div>
        </div>
        <div class="dashboard-card-footer">
            <div class="dashboard-card-stat">Paths: 5</div>
            <div class="dashboard-card-action">Continue Learning →</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Stats cards row
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-icon">🔍</div>
            <div class="stats-content">
                <div class="stats-value">{st.session_state.vulnerability_scans}</div>
                <div class="stats-label">Vulnerability Scans</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-icon">💻</div>
            <div class="stats-content">
                <div class="stats-value">{st.session_state.code_snippets}</div>
                <div class="stats-label">Code Snippets</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-icon">🔐</div>
            <div class="stats-content">
                <div class="stats-value">{st.session_state.security_tips}</div>
                <div class="stats-label">Security Tips</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Create a layout with proper spacing
    st.markdown('<div class="main-layout">', unsafe_allow_html=True)
    
    # Chat container - now takes most of the vertical space
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    display_messages()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Predefined questions
    st.markdown('<div class="predefined-questions">', unsafe_allow_html=True)
    
    # Only show predefined questions if there are no messages yet or just the welcome message
    if len(st.session_state.messages) <= 1:
        for i, question in enumerate(PREDEFINED_QUESTIONS):
            # Create a unique key for each question
            question_key = f"q_{i}"
            
            # Display predefined question
            st.markdown(f"""
            <div class="predefined-question" id="{question_key}">
                {question}
            </div>
            """, unsafe_allow_html=True)
            
            # Add a hidden button to handle the click
            if st.button(question, key=question_key):
                # Add user message to chat
                st.session_state.messages.append({"role": "user", "content": question})
                
                # Hide welcome prompts after selection
                st.session_state.show_welcome_prompts = False
                
                # Generate and display response
                response = generate_response(question, model, mode=st.session_state.mode)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Save chat to history
                save_chat_to_history()
                
                # Increment the input key to create a fresh input field
                st.session_state.input_key += 1
                
                # Rerun to update UI
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Custom chat input at the bottom
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    # Two-column layout for input and button
    col1, col2 = st.columns([6, 1])
    
    with col1:
        # Use a unique key each time to prevent the experimental_rerun error
        user_input = st.text_input(
            "Ask about cybersecurity, DevSecOps, or request code...",
            key=f"user_input_{st.session_state.input_key}"
        )
    
    with col2:
        send_button = st.button("💬 Ask CyberGuard AI", key="send", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)  # Close main-layout
    
    # Process user input
    if user_input and send_button:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Hide welcome prompts after user input
        st.session_state.show_welcome_prompts = False
        
        # Generate and display response
        response = generate_response(user_input, model, mode=st.session_state.mode)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Save chat to history
        save_chat_to_history()
        
        # Increment the input key to create a fresh input field
        st.session_state.input_key += 1
        
        # Use st.rerun() instead of experimental_rerun
        st.rerun()

# Footer
st.markdown("""
<div class="footer">
    CyberGuard AI • Powered by Ollama • v3.0.0 Created By Hits • Ms Cyclone • Cypher Raven 
</div>
""", unsafe_allow_html=True)

# Run the app with: streamlit run cyberguard_ai.py
print("CyberGuard AI is running! Access it in your browser.")