import streamlit as st


def inject_theme():
    st.markdown(
        """
    <style>
      .main { background-color: #0f1116; color: #e5e7eb; }
      .block-container { padding-top: 1rem; padding-bottom: 2rem; }
      .stTextArea textarea { background-color:#1c1f2b !important; color:#e5e7eb !important; }
      .stFileUploader { background:#1c1f2b; border-radius:12px; padding:8px 10px; }
      .ev-card { background:#1c1f2b; border-radius:14px; padding:16px; }
      .ev-primary button { background:#7c3aed !important; color:white !important; border-radius:10px; height:44px; width:100%; font-weight:600; }
      .ev-history { background:#1c1f2b; border-radius:14px; padding:16px; height:420px; overflow-y:auto; }
      audio { width: 100%; }
      hr { border: none; border-top: 1px solid #2a2f3d; margin: 10px 0 16px; }
    </style>
    """,
        unsafe_allow_html=True,
    )
