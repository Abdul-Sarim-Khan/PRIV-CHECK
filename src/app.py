#app.py module

import streamlit as st
from streamlit_lottie import st_lottie
import json
from json import JSONDecodeError
import time
import plotly.graph_objects as go
from detector import detect_patterns, calculate_severity_and_tier
import os

# Set page config for better appearance
st.set_page_config(
    page_title="VULNERACHECK - Script Integrity Analysis",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load animations (you'll need to replace these with your own Lottie files or use URLs)
def load_lottie_file(filepath: str):
    """Load Lottie file with multiple fallback options."""
    paths_to_try = [
        filepath,  # Original path
        os.path.join("assets", filepath),  # Common alternative
        os.path.join(os.path.dirname(__file__), filepath)  # Absolute path
    ]
    
    for path in paths_to_try:
        try:
            with open(path, "r", encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, JSONDecodeError):
            continue
    
    print(f"Failed to load Lottie file after trying {len(paths_to_try)} paths")
    return None

# Custom CSS for animations and styling
def local_css(file_name):
    """Load and apply local CSS file."""
    try:
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        with open(file_path, encoding='utf-8') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Failed to load CSS: {str(e)}")

# Load custom CSS
local_css("styles.css")  # You'll need to create this file



# Create a gauge meter for severity
# Create a gauge meter for privilege risk
def create_gauge(severity):
    """Create a Plotly gauge chart for privilege risk"""
    # Define colors and labels
    colors = ["#00FF00", "#FFFF00", "#FFA500", "#FF0000"]  # Green, Yellow, Orange, Red
    labels = ["Low", "Medium", "High", "Critical"]
    background_color = "#2C2C2C"  # Dark gray background
    
    # Input validation
    try:
        severity = float(severity)
        severity = max(0, min(3, severity))  # Clamp between 0-3
        severity_level = int(round(severity))
    except (TypeError, ValueError):
        severity = 0
        severity_level = 0
    
    # Create gauge with colored labels
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=severity,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "PRIVILEGE RISK LEVEL", 'font': {'size': 24, 'color': 'white'}},
        number={'font': {'color': 'white'}},
        gauge={
            'axis': {
                'range': [0, 3],
                'tickvals': [0.5, 1.5, 2.5, 3],
                'ticktext': [f'<span style="color:{colors[i]}">{labels[i]}</span>' 
                            for i in range(4)],
                'tickwidth': 1,
                'tickcolor': "white",
                'tickfont': {'size': 12},
            },
            'bar': {'color': colors[severity_level]},
            'bgcolor': background_color,
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 1], 'color': background_color},
                {'range': [1, 2], 'color': background_color},
                {'range': [2, 3], 'color': background_color}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': severity
            }
        }
    ))
    
    # Add colored severity label annotation
    fig.add_annotation(
        x=0.5,
        y=0.5,
        text=f'<b style="color:{colors[severity_level]}"></br>{labels[severity_level]}</b>',
        showarrow=False,
        font=dict(size=20),
        xanchor='center'
    )
    
    # Update layout with dark theme
    fig.update_layout(
        height=350,
        paper_bgcolor=background_color,
        plot_bgcolor=background_color,
        margin=dict(l=50, r=50, b=50, t=80),
        font=dict(color="white", family="Arial")
    )
    
    return fig

# Animated header
def animated_header():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
        <div class="header-container">
            <h1 class="glow" style="text-align: left;">PRIVCHECK</h1>
            <p class="subheader" style="text-align: left;">Privileged Command Analysis Tool</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st_lottie(load_lottie_file("shield_animation.json"), height=150, key="shield")


def user_input():
    with st.expander("", expanded=True):  # Empty string will remove the default title
        # Custom header for "Upload or Paste Script"
        st.markdown("""
        <div class="fade-in">
            <h2 style="font-size: 28px; color: #FFFFFF;">📁 Upload or Paste Script</h2>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            uploaded_file = st.file_uploader(
                "Choose a file", 
                type=["txt", "js", "sql", "sh"],
                key="file_uploader",
                help="Upload your script file for analysis"
            )
        with col2:
            if uploaded_file:
                script = uploaded_file.read().decode("utf-8")
                st.success("File uploaded successfully!")
                return script
            else:
                script = st.text_area(
                    "Or paste your script here", 
                    height=200,
                    placeholder="Paste your script content here...",
                    help="Directly paste your script for analysis"
                )
                return script if script else None

        # Format this to be consistent with Detection Results
        st.markdown("""
        <div class="fade-in">
            <h2 style="font-size: 28px; color: #FFFFFF;">📁 Upload or Paste Script</h2>
        </div>
        """, unsafe_allow_html=True)

def display_results(matches, severity, tier):
    with st.spinner("Analyzing privilege levels..."):
        time.sleep(1)
    
    st.markdown("---")
    st.plotly_chart(create_gauge(severity), use_container_width=True)

    with st.container():
        st.markdown("""
        <div class="fade-in">
            <h2 style="font-size: 28px; color: #FFFFFF;">🔍 Privileged Command Analysis</h2>
        </div>
        """, unsafe_allow_html=True)
        
        if matches:
            st.markdown(f"<div class='bounce' style='color:red;font-size:22px; font-weight: bold;'>⚠️ Detected {len(matches)} privileged commands</div>", unsafe_allow_html=True)
            
            # Display context-aware explanations
            with st.expander("View Command Details", expanded=True):
                for i, (category, command) in enumerate(matches):
                    # Add contextual information based on command type
                    context = get_command_context(category, command)
                    
                    st.markdown(f"""
                    <div class="slide-in" style="animation-delay:{i*0.1}s">
                        <div class="pattern-card" style="background-color:#2C2C2C; padding: 15px; margin-bottom: 10px; border-radius: 8px;">
                            <span class="pattern-type" style="font-weight: bold; color: #FFA07A;">{category}</span>
                            <div class="command-content" style="margin: 5px 0; font-family: monospace; font-size: 14px;">{command}</div>
                            <div class="context-info" style="font-size: 14px; color: #ADD8E6;">
                                {context}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="fade-in">
                <div class="success-card">
                    <h3>✅ No privileged commands detected</h3>
                    <p>This script contains no elevated-privilege operations</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Severity explanation with color coding
    severity_colors = {0: "#00FF00", 1: "#FFFF00", 2: "#FFA500", 3: "#FF0000"}
    severity_labels = {0: "Low Risk", 1: "Medium Risk", 2: "High Risk", 3: "Critical Risk"}
    
    st.markdown(f"""
    <div class="severity-box" style="border-left: 5px solid {severity_colors[severity]}; padding: 15px; margin-top: 20px; background-color: #2C2C2C; border-radius: 8px;">
        <h3>Risk Assessment</h3>
        <p><strong>Level:</strong> <span style="color:{severity_colors[severity]}">{severity} - {severity_labels[severity]}</span></p>
        <p><strong>Summary:</strong> {tier}</p>
    </div>
    """, unsafe_allow_html=True)


def get_command_context(category, command):
    """Provide contextual information for detected commands"""
    context_info = {
        'Privilege Escalation': "Elevates user privileges, potentially granting admin/root access",
        'User Management': "Modifies user accounts or group memberships",
        'File Permission': "Changes file/directory permissions or ownership",
        'System Config': "Alters system configuration or service states",
        'Destructive Command': "Can cause data loss or system instability if misused",
        'Sensitive Info Access': "Accesses security-sensitive files or credentials",
        'Network Admin': "Modifies network configuration or firewall rules"
    }
    
    specific_advice = {
        'sudo': "Ensure sudo usage is limited to authorized operations",
        'chmod': "Avoid setting 777 permissions; use least privilege principle",
        'rm -rf': "Double-check target paths before execution",
        'passwd': "Password changes should follow security policies",
        'systemctl': "Verify service changes are intentional and authorized"
    }
    
    base_info = context_info.get(category, "Requires elevated privileges to execute")
    
    # Add command-specific advice
    for cmd, advice in specific_advice.items():
        if cmd in command:
            base_info += f"<br><strong>Note:</strong> {advice}"
    
    return base_info

def main():
    animated_header()
    
    script = user_input()
    if script:
        matches, found_types = detect_patterns(script)
        severity, tier = calculate_severity_and_tier(found_types)
        display_results(matches, severity, tier)
        
        # Add a confetti animation for clean scripts
        if severity == 0:
            st.balloons()

if __name__ == "__main__":
    main()

#streamlit run "D:\sarim\University\Semester 8 ( Spring 2025 )\Theory of Automata\CCP\VulneraCheck\vulneracheck\src\app.py"