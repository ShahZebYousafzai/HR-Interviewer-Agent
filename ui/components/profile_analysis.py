import streamlit as st

class ProfileAnalysisDisplay:
    """Profile analysis display component"""
    
    def render(self):
        """Render profile analysis section"""
        if st.session_state.state.get("profile_analysis"):
            with st.expander("📋 Candidate Profile Analysis", expanded=False):
                analysis = st.session_state.state["profile_analysis"]
                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"**Domain:** {analysis.get('domain', 'N/A')}")
                    st.write(f"**Experience Level:** {analysis.get('experience_level', 'N/A')}")
                    st.write(f"**Years of Experience:** {analysis.get('years_experience', 'N/A')}")

                with col2:
                    st.write(f"**Skills:** {', '.join(analysis.get('skills', []))}")
                    st.write(f"**Strengths:** {', '.join(analysis.get('strengths', []))}")
                    st.write(f"**Focus Areas:** {', '.join(analysis.get('focus_areas', []))}")