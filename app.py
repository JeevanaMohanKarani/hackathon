"""
app.py - Nova Voice-to-Task Assistant Dashboard.
Streamlit application featuring voice input, multi-agent execution pipeline, live critic feedback, and persistent memory.
"""

import streamlit as st
import json
import time
from datetime import datetime
import memory
import tools
from agents.orchestrator import run_pipeline
import voice

# Page configuration
st.set_page_config(
    page_title="VoxFlow | Voice-to-Task Autonomous Assistant",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern dark glassmorphic styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .main {
        background: radial-gradient(circle at 10% 20%, rgba(18, 24, 38, 1) 0%, rgba(10, 14, 23, 1) 90.2%);
    }

    .stApp {
        background-color: #0B0F19;
        color: #F3F4F6;
    }

    /* Glass card container */
    .glass-card {
        background: rgba(23, 32, 51, 0.65);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .glass-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
    }

    /* Agent badges */
    .agent-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .badge-planner {
        background: rgba(139, 92, 246, 0.2);
        color: #C4B5FD;
        border: 1px solid rgba(139, 92, 246, 0.4);
    }

    .badge-executor {
        background: rgba(59, 130, 246, 0.2);
        color: #93C5FD;
        border: 1px solid rgba(59, 130, 246, 0.4);
    }

    .badge-critic {
        background: rgba(245, 158, 11, 0.2);
        color: #FCD34D;
        border: 1px solid rgba(245, 158, 11, 0.4);
    }

    .badge-memory {
        background: rgba(16, 185, 129, 0.2);
        color: #6EE7B7;
        border: 1px solid rgba(16, 185, 129, 0.4);
    }

    .priority-high {
        background: rgba(239, 68, 68, 0.2);
        color: #FCA5A5;
        border: 1px solid rgba(239, 68, 68, 0.4);
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    .priority-medium {
        background: rgba(245, 158, 11, 0.2);
        color: #FDE68A;
        border: 1px solid rgba(245, 158, 11, 0.4);
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    .priority-low {
        background: rgba(107, 114, 128, 0.2);
        color: #D1D5DB;
        border: 1px solid rgba(107, 114, 128, 0.4);
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    .score-circle {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.8rem;
        font-weight: 800;
        color: #10B981;
    }

    .code-box {
        font-family: 'JetBrains Mono', monospace;
        background: #0D1117;
        border: 1px solid #30363D;
        border-radius: 8px;
        padding: 12px;
        font-size: 0.85rem;
        color: #58A6FF;
    }
</style>
""", unsafe_allow_html=True)

# Ensure DB initialized
memory.init_db()

# Session State Initialization
if "last_pipeline_result" not in st.session_state:
    st.session_state.last_pipeline_result = None
if "transcribed_text" not in st.session_state:
    st.session_state.transcribed_text = ""
if "voice_processed" not in st.session_state:
    st.session_state.voice_processed = False


# --- Sidebar: System Status & Persistent Memory ---
with st.sidebar:
    st.markdown("### 🎙️ **VoxFlow Control Center**")
    st.caption("Autonomous Voice-to-Task Multi-Agent System")
    
    st.markdown("---")
    st.markdown("#### ⚡ **Active Agents & Pipeline**")
    st.markdown("""
    - 🟣 **Planner**: Meta Llama-3.2 (NVIDIA NIM) / Gemini
    - 🔵 **Executor**: Multi-Tool Task Engine
    - 🟡 **Critic**: Reflection & Quality Scoring (1-10)
    - 🟢 **Memory**: SQLite Persistent Engine
    - 🎙️ **Voice**: Groq Whisper-large-v3
    """)
    
    st.markdown("---")
    st.markdown("#### 🧠 **Persistent User Profile**")
    user_facts = memory.get_all_facts()
    for f in user_facts:
        st.markdown(f"**{f['key']}**: `{f['value']}`")
    
    with st.expander("➕ Add New Memory / Fact"):
        with st.form("new_fact_form"):
            new_key = st.text_input("Key (e.g. 'work_hours', 'preferred_email')")
            new_val = st.text_input("Value")
            new_cat = st.selectbox("Category", ["profile", "schedule", "settings", "context"])
            fact_submit = st.form_submit_button("Save Memory")
            if fact_submit and new_key and new_val:
                memory.save_fact(new_key, new_val, new_cat)
                st.success(f"Remembered: {new_key}!")
                st.rerun()

    st.markdown("---")
    if st.button("🗑️ Reset Demo Tasks & DB", use_container_width=True):
        import os
        if os.path.exists(memory.DB_PATH):
            os.remove(memory.DB_PATH)
        memory.init_db()
        st.session_state.last_pipeline_result = None
        st.success("Database reset to defaults.")
        st.rerun()


# --- Main Dashboard Header ---
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
    <div>
        <h1 style="margin: 0; font-size: 2.2rem; font-weight: 800; background: linear-gradient(135deg, #6366F1 0%, #A855F7 50%, #EC4899 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            VoxFlow Voice-to-Task
        </h1>
        <p style="margin: 4px 0 0 0; color: #9CA3AF; font-size: 1rem;">
            Spoken requests $\\to$ Self-Reflecting Autonomous Agent Pipeline $\\to$ Persistent Task Engine
        </p>
    </div>
    <div style="text-align: right;">
        <span class="agent-badge badge-memory">● SYSTEM ACTIVE</span>
    </div>
</div>
""", unsafe_allow_html=True)


# --- Input Section: Voice & Text ---
tabs = st.tabs(["🎙️ Voice Input (Microphone)", "⌨️ Text Command & Quick Scenarios", "📋 Task Board & Kanban", "📊 Multi-Agent Execution History"])

with tabs[0]:
    col_mic, col_sample = st.columns([1.2, 1])
    
    with col_mic:
        st.markdown("#### 🎙️ **Speak to VoxFlow**")
        st.caption("Record voice command directly from your browser microphone:")
        
        # Audio input widget (Streamlit 1.40+)
        audio_value = st.audio_input("Record your voice command", key="mic_input")
        
        if audio_value is not None:
            audio_bytes = audio_value.read()
            if audio_bytes and len(audio_bytes) > 0:
                with st.spinner("🎧 Transcribing your voice in real-time..."):
                    transcription = voice.transcribe_audio_bytes(audio_bytes)
                    if transcription:
                        st.session_state.transcribed_text = transcription
                    elif not st.session_state.transcribed_text:
                        st.warning("⚠️ No clear speech detected from recording. Please speak closer to the mic or type below.")
        
        # Editable Transcribed Voice Input Box
        user_voice_prompt = st.text_area(
            "📝 Transcribed Voice Command (Live Editable):",
            value=st.session_state.transcribed_text,
            placeholder="Your spoken words will appear here. You can also edit or type directly...",
            height=100,
            key="voice_text_box"
        )
        
        if user_voice_prompt:
            st.session_state.transcribed_text = user_voice_prompt
            
        col_run, col_clear = st.columns([2, 1])
        with col_run:
            if st.button("🚀 Process with VoxFlow Multi-Agent Loop", type="primary", use_container_width=True, disabled=not bool(st.session_state.transcribed_text)):
                with st.spinner("🤖 Autonomous agents planning, executing, and critiquing..."):
                    res = run_pipeline(st.session_state.transcribed_text)
                    st.session_state.last_pipeline_result = res
                st.rerun()
        with col_clear:
            if st.button("🔄 Clear Input", use_container_width=True):
                st.session_state.transcribed_text = ""
                st.rerun()

    with col_sample:
        st.markdown("#### ⚡ **Quick Demo Voice Prompts**")
        st.caption("Click any real-world voice command to simulate:")
        
        prompts = [
            "Schedule an urgent team architecture review meeting for 3 PM today and mark it high priority.",
            "Remember that my daily gym workout is scheduled at 7:00 AM every weekday.",
            "Deconstruct a complete deployment checklist for our production release on Friday.",
            "Complete task number 1 and calculate 45 * 12 + 180 for server budget."
        ]
        
        for p in prompts:
            if st.button(f"🗣️ \"{p}\"", use_container_width=True):
                st.session_state.transcribed_text = p
                with st.spinner("Running agent loop..."):
                    res = run_pipeline(p)
                    st.session_state.last_pipeline_result = res
                st.rerun()

with tabs[1]:
    st.markdown("#### ⌨️ **Type Spoken Instruction**")
    custom_text = st.text_area("Enter command as if spoken:", placeholder="e.g. Schedule a 1-on-1 sync with Alex tomorrow at 11 AM regarding model evaluations")
    if st.button("Run Multi-Agent Pipeline", type="primary") and custom_text:
        with st.spinner("Orchestrating agents..."):
            res = run_pipeline(custom_text)
            st.session_state.last_pipeline_result = res
        st.rerun()


# --- Real-Time Agent Execution Pipeline Results ---
if st.session_state.last_pipeline_result:
    res = st.session_state.last_pipeline_result
    st.markdown("---")
    st.markdown(f"### 🚀 **Multi-Agent Pipeline Trace** (Attempts: `{res['attempts']}`)")

    # Spoken Confirmation Banner & TTS Trigger
    spoken_text = res.get("spoken_response", "")
    st.markdown(f"""
    <div class="glass-card" style="border-left: 4px solid #10B981;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <span class="agent-badge badge-memory">🔊 VOXFLOW SPOKEN REPLY</span>
                <h4 style="margin: 8px 0 0 0; color: #E5E7EB;">"{spoken_text}"</h4>
            </div>
            <div style="text-align: right;">
                <span style="font-size: 0.85rem; color: #10B981; font-weight: 600;">💾 Saved to SQLite DB (Log #{res.get('history_id', '-')})</span><br>
                <span style="font-size: 0.75rem; color: #9CA3AF;">👉 View under <b>'📋 Task Board'</b> tab above</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Auto-play browser TTS
    st.components.v1.html(voice.get_browser_tts_html(spoken_text), height=0)

    # Agent Breakdown Columns
    col_plan, col_exec, col_crit = st.columns(3)

    plan = res.get("final_plan", {})
    exec_res = res.get("final_execution", {})
    critic = res.get("final_critic", {})

    with col_plan:
        st.markdown("""
        <div class="glass-card">
            <span class="agent-badge badge-planner">🟣 1. PLANNER AGENT</span>
            <h4 style="margin-top: 10px;">Intent Decomposition</h4>
        """, unsafe_allow_html=True)
        st.markdown(f"**Intent**: {plan.get('intent', 'N/A')}")
        st.markdown(f"**Reasoning**: {plan.get('reasoning', 'N/A')}")
        st.markdown("**Planned Tools**:")
        st.json(plan.get("planned_tools", []))
        st.markdown("</div>", unsafe_allow_html=True)

    with col_exec:
        st.markdown("""
        <div class="glass-card">
            <span class="agent-badge badge-executor">🔵 2. EXECUTOR AGENT</span>
            <h4 style="margin-top: 10px;">Tool Execution</h4>
        """, unsafe_allow_html=True)
        st.markdown(f"**Tools Run**: `{exec_res.get('total_tools', 0)}` | **Success**: `{exec_res.get('success_count', 0)}`")
        st.markdown("**Execution Results**:")
        st.json(exec_res.get("results", []))
        st.markdown("</div>", unsafe_allow_html=True)

    with col_crit:
        score = critic.get("score", 0)
        passed = critic.get("passed", False)
        badge_color = "#10B981" if passed else "#EF4444"
        st.markdown(f"""
        <div class="glass-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="agent-badge badge-critic">🟡 3. CRITIC AGENT</span>
                <span class="score-circle" style="color: {badge_color};">{score}/10</span>
            </div>
            <h4 style="margin-top: 10px;">Self-Reflection & Quality</h4>
        """, unsafe_allow_html=True)
        st.markdown(f"**Strengths**: {critic.get('strengths', 'N/A')}")
        st.markdown(f"**Weaknesses**: {critic.get('weaknesses', 'None')}")
        st.markdown(f"**Retry Needed**: `{'Yes' if critic.get('retry_needed') else 'No (Approved)'}`")
        if critic.get("improved_instructions"):
            st.info(f"Feedback applied: {critic.get('improved_instructions')}")
        st.markdown("</div>", unsafe_allow_html=True)


# --- Task Board Tab ---
with tabs[2]:
    st.markdown("### 📋 **Persistent Task Board**")
    
    col_filter1, col_filter2, col_new = st.columns([1, 1, 1.2])
    with col_filter1:
        status_filter = st.selectbox("Status Filter", ["All", "Pending", "In Progress", "Completed"])
    with col_filter2:
        category_filter = st.selectbox("Category Filter", ["All", "Hackathon", "Work", "General", "Reminder", "Review"])
    with col_new:
        with st.expander("➕ Add Manual Task"):
            with st.form("manual_task_form"):
                t_title = st.text_input("Task Title")
                t_desc = st.text_area("Description")
                t_priority = st.selectbox("Priority", ["High", "Medium", "Low"])
                t_cat = st.text_input("Category", "General")
                t_due = st.text_input("Due Date", "Today")
                t_submit = st.form_submit_button("Create Task")
                if t_submit and t_title:
                    memory.create_task(t_title, t_desc, t_priority, t_cat, "Pending", t_due)
                    st.success("Task added!")
                    st.rerun()

    current_tasks = memory.get_tasks(
        status=status_filter if status_filter != "All" else None,
        category=category_filter if category_filter != "All" else None
    )

    if not current_tasks:
        st.info("No tasks found matching current filters.")
    else:
        for t in current_tasks:
            p_class = f"priority-{t['priority'].lower()}"
            status_emoji = "✅" if t["status"] == "Completed" else ("⏳" if t["status"] == "In Progress" else "📌")
            
            with st.container():
                st.markdown(f"""
                <div class="glass-card" style="padding: 16px; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <span style="font-size: 1.1rem; font-weight: 700;">{status_emoji} #{t['id']}: {t['title']}</span>
                            <span class="{p_class}" style="margin-left: 8px;">{t['priority']}</span>
                            <span style="background: rgba(255,255,255,0.1); padding: 2px 8px; border-radius: 6px; font-size: 0.75rem; margin-left: 4px;">{t['category']}</span>
                            {f'<span style="background: rgba(139,92,246,0.2); color: #C4B5FD; padding: 2px 8px; border-radius: 6px; font-size: 0.75rem; margin-left: 4px;">🔄 {t["recurrence"]}</span>' if t['recurrence'] != 'None' else ''}
                        </div>
                        <div>
                            <span style="color: #9CA3AF; font-size: 0.85rem;">🕒 Due: {t['due_date'] or 'No deadline'}</span>
                        </div>
                    </div>
                    <p style="margin: 8px 0 12px 0; color: #D1D5DB; font-size: 0.9rem;">{t['description'] or 'No description provided.'}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Action Buttons
                c1, c2, c3 = st.columns([1, 1, 4])
                with c1:
                    if t["status"] != "Completed":
                        if st.button("Mark Done", key=f"done_{t['id']}"):
                            memory.update_task_status(t["id"], "Completed")
                            st.rerun()
                    else:
                        if st.button("Re-open", key=f"reopen_{t['id']}"):
                            memory.update_task_status(t["id"], "Pending")
                            st.rerun()
                with c2:
                    if st.button("Delete", key=f"del_{t['id']}"):
                        memory.delete_task(t["id"])
                        st.rerun()


# --- Execution History Tab ---
with tabs[3]:
    st.markdown("### 📊 **Multi-Agent Run History & Memory Log**")
    history_logs = memory.get_execution_history(limit=15)
    
    if not history_logs:
        st.info("No execution runs logged yet.")
    else:
        for h in history_logs:
            score_col = "#10B981" if h["critic_score"] >= 7 else "#EF4444"
            with st.expander(f"Run #{h['id']} | \"{h['user_request'][:60]}...\" (Critic: {h['critic_score']}/10)"):
                st.markdown(f"**Timestamp**: `{h['timestamp']}` | **Retries**: `{h['retry_count']}`")
                st.markdown(f"**Spoken Reply**: *\"{h['final_output']}\"*")
                st.markdown(f"**Critic Feedback**: {h['critic_feedback']}")
                st.markdown("---")
                st.markdown("**Planner Raw Output**:")
                st.code(h["planner_output"], language="json")
                st.markdown("**Executor Raw Output**:")
                st.code(h["executor_output"], language="json")
