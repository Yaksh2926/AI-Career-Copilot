import streamlit as st
import time
from frontend.utils.auth import forgot_password_request, reset_user_password, validate_email

def show_forgot_password():
    """
    Renders the Forgot Password recovery flow and simulated reset password entry.
    """
    empty_col_left, forgot_col, empty_col_right = st.columns([3.5, 5, 3.5])
    
    with forgot_col:
        st.markdown("<div style='margin-top: 5rem;'></div>", unsafe_allow_html=True)
        
        # Checking if user is in reset mode (after clicking "link")
        if st.session_state.get("reset_email_target"):
            render_reset_password_form()
            return
            
        # Header
        forgot_header = """
        <div style="text-align: center; margin-bottom: 2rem;">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="display: inline-block;">
                <path d="M12 2L2 22H22L12 2Z" fill="url(#forgot-logo-grad)" stroke="#A855F7" stroke-width="2" stroke-linejoin="round"/>
                <defs>
                    <linearGradient id="forgot-logo-grad" x1="2" y1="22" x2="22" y2="2" gradientUnits="userSpaceOnUse">
                        <stop offset="0" stop-color="#7C3AED"/>
                        <stop offset="1" stop-color="#3B82F6"/>
                    </linearGradient>
                </defs>
            </svg>
            <h2 style="font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 2rem; background: linear-gradient(135deg, #FFF 30%, #A855F7 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-top: 0.5rem; margin-bottom: 0.25rem; letter-spacing: -0.5px;">Recover Password</h2>
            <p style="color: #94A3B8; font-size: 0.9rem;">We'll send you instructions to reset your password</p>
        </div>
        """
        st.html(forgot_header)
        
        st.markdown("<div class='glass-card' style='padding: 2.5rem 2.25rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.06);'>", unsafe_allow_html=True)
        
        email = st.text_input("Work Email Address", placeholder="name@company.com", key="recovery_email")
        
        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
        
        if st.button("Send Reset Instructions ➔", key="forgot_submit_btn", use_container_width=True):
            if not email.strip():
                st.error("Please enter your email address.")
            elif not validate_email(email):
                st.error("Please enter a valid email address.")
            else:
                with st.spinner("Validating account record..."):
                    time.sleep(1.0)
                
                res = forgot_password_request(email)
                if res["success"]:
                    st.success("Instructions sent! check your inbox (including spam).")
                    
                    # For demo sandbox purposes, let's render a quick direct link to mock the click on the reset link!
                    st.session_state["reset_email_target"] = email.strip()
                    quick_link_html = f"""
                    <div style="background: rgba(124, 58, 237, 0.08); border: 1px solid rgba(124, 58, 237, 0.2); border-radius: 8px; padding: 12px; margin-top: 1.5rem; text-align: center;">
                        <span style="font-size: 0.8rem; color: #E2E8F0; display: block; margin-bottom: 6px;">💡 Sandbox Quick-Link:</span>
                        <a href="/?page=forgot_password" target="_self" style="font-size: 0.85rem; color: #A855F7; text-decoration: underline; font-weight: 600;">Mock Reset Email Click ➔</a>
                    </div>
                    """
                    st.html(quick_link_html)
                else:
                    st.error("Email not found. Try signing up or using candidate@copilot.ai")
                    
        # Link to login page
        back_link_html = """
        <div style="text-align: center; font-size: 0.85rem; color: #94A3B8; margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.06);">
            Remembered your password? <a href="/?page=login" target="_self" style="color: #3B82F6; text-decoration: none; font-weight: 600;">Sign In</a>
        </div>
        """
        st.html(back_link_html)
        
        st.markdown("</div>", unsafe_allow_html=True)

def render_reset_password_form():
    """
    Renders the password reset form when a simulated token click is active.
    """
    target_email = st.session_state.get("reset_email_target")
    
    reset_header_html = f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 2rem; background: linear-gradient(135deg, #FFF 30%, #A855F7 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.25rem; letter-spacing: -0.5px;">Reset Password</h2>
        <p style="color: #94A3B8; font-size: 0.9rem;">Resetting password for: <b>{target_email}</b></p>
    </div>
    """
    st.html(reset_header_html)
    
    st.markdown("<div class='glass-card' style='padding: 2.25rem 2.25rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.06);'>", unsafe_allow_html=True)
    
    new_pw = st.text_input("New Password", type="password", placeholder="••••••••", key="reset_new_password")
    confirm_pw = st.text_input("Confirm New Password", type="password", placeholder="••••••••", key="reset_confirm_password")
    
    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
    
    if st.button("Update Password ➔", key="reset_submit_btn", use_container_width=True):
        if not new_pw.strip():
            st.error("Please enter a new password.")
        elif len(new_pw.strip()) < 6:
            st.error("Password must be at least 6 characters.")
        elif new_pw != confirm_pw:
            st.error("Passwords do not match.")
        else:
            with st.spinner("Updating password record..."):
                time.sleep(1.0)
            res = reset_user_password(target_email, new_pw)
            if res["success"]:
                st.session_state["reset_email_target"] = None
                st.toast("Password reset successfully!", icon="🔑")
                time.sleep(0.5)
                st.query_params["page"] = "login"
                st.rerun()
            else:
                st.error("Failed to reset password.")
                
    st.markdown("</div>", unsafe_allow_html=True)
