import streamlit as st
import time
from frontend.utils.auth import signup_user, validate_email, calculate_password_strength

def show_signup_page():
    """
    Renders a premium, centered glassmorphic signup card.
    Integrates password strength indicators, email validation, and confirm matches.
    """
    empty_col_left, signup_col, empty_col_right = st.columns([3.5, 5, 3.5])
    
    with signup_col:
        st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)
        
        # Logo header
        logo_html = """
        <div style="text-align: center; margin-bottom: 1.5rem;">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="display: inline-block;">
                <path d="M12 2L2 22H22L12 2Z" fill="url(#signup-logo-grad)" stroke="#A855F7" stroke-width="2" stroke-linejoin="round"/>
                <defs>
                    <linearGradient id="signup-logo-grad" x1="2" y1="22" x2="22" y2="2" gradientUnits="userSpaceOnUse">
                        <stop offset="0" stop-color="#7C3AED"/>
                        <stop offset="1" stop-color="#3B82F6"/>
                    </linearGradient>
                </defs>
            </svg>
            <h2 style="font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 2rem; background: linear-gradient(135deg, #FFF 30%, #A855F7 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-top: 0.5rem; margin-bottom: 0.25rem; letter-spacing: -0.5px;">Create Your Account</h2>
            <p style="color: #94A3B8; font-size: 0.9rem;">Join AI Career Copilot sandbox today</p>
        </div>
        """
        st.html(logo_html)
        
        st.markdown("<div class='glass-card' style='padding: 2.5rem 2.25rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.06);'>", unsafe_allow_html=True)
        
        # Form fields
        fullname = st.text_input("Full Name", placeholder="Yaksh Jindal", key="signup_name")
        email = st.text_input("Work Email Address", placeholder="name@company.com", key="signup_email")
        
        # Password
        show_pw = st.checkbox("Show Passwords", key="signup_show_pw")
        pw_type = "default" if show_pw else "password"
        
        password = st.text_input("Password", type=pw_type, placeholder="••••••••", key="signup_password")
        
        # Render Password Strength Indicator
        score, label, color = calculate_password_strength(password)
        bar_width = f"{(score/4)*100}%" if password else "0%"
        
        strength_html = f"""
        <div style="margin-top: -8px; margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                <span style="font-size: 0.75rem; color: #94A3B8;">Password Strength:</span>
                <span style="font-size: 0.75rem; color: {color}; font-weight: 600;">{label}</span>
            </div>
            <div style="width: 100%; height: 4px; background: rgba(255,255,255,0.06); border-radius: 2px; overflow: hidden;">
                <div style="width: {bar_width}; height: 100%; background: {color}; transition: all 0.3s ease;"></div>
            </div>
        </div>
        """
        st.html(strength_html)
        
        confirm_password = st.text_input("Confirm Password", type=pw_type, placeholder="••••••••", key="signup_confirm_password")
        
        st.markdown("<div style='margin-top: 1.25rem;'></div>", unsafe_allow_html=True)
        
        # Submit Button
        if st.button("Create Account ➔", key="signup_submit_btn", use_container_width=True):
            if not fullname.strip():
                st.error("Please enter your full name.")
            elif not email.strip():
                st.error("Please enter your email address.")
            elif not validate_email(email):
                st.error("Please enter a valid email address.")
            elif not password.strip():
                st.error("Please set a password.")
            elif score < 2:
                st.error("Password is too weak. Please ensure it has at least 8 characters, numbers, and special symbols.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            else:
                # Execute Register
                with st.spinner("Provisioning candidate workspace..."):
                    time.sleep(1.5)
                res = signup_user(fullname, email, password)
                if res["success"]:
                    st.toast("Account created successfully!", icon="🎉")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error(res["message"])
                    
        # Separator line
        sep_html = """
        <div style="display: flex; align-items: center; margin: 1.25rem 0;">
            <div style="flex: 1; height: 1px; background: rgba(255,255,255,0.08);</div>
            <span style="font-size: 0.75rem; color: #64748B; padding: 0 10px; text-transform: uppercase; letter-spacing: 1px;">Or sign up with</span>
            <div style="flex: 1; height: 1px; background: rgba(255,255,255,0.08);</div>
        </div>
        """
        # Note: Fixed minor unclosed div markup in separator
        sep_html_fixed = """
        <div style="display: flex; align-items: center; margin: 1.25rem 0;">
            <div style="flex: 1; height: 1px; background: rgba(255,255,255,0.08);"></div>
            <span style="font-size: 0.75rem; color: #64748B; padding: 0 10px; text-transform: uppercase; letter-spacing: 1px;">Or sign up with</span>
            <div style="flex: 1; height: 1px; background: rgba(255,255,255,0.08);"></div>
        </div>
        """
        st.html(sep_html_fixed)
        
        # SSO Grid
        sso_html = """
        <div style="display: flex; gap: 12px; margin-bottom: 1.5rem;">
            <a href="/?sso=google" target="_self" class="sso-btn">
                <svg width="16" height="16" viewBox="0 0 18 18">
                    <path d="M17.64 9.2c0-.63-.06-1.25-.16-1.84H9v3.47h4.84c-.21 1.12-.84 2.07-1.79 2.7v2.24h2.9c1.7-1.57 2.69-3.88 2.69-6.57z" fill="#4285F4"/>
                    <path d="M9 18c2.43 0 4.47-.8 5.96-2.18l-2.9-2.24c-.8.54-1.84.87-3.06.87-2.35 0-4.33-1.59-5.04-3.73H.95v2.3C2.43 15.93 5.48 18 9 18z" fill="#34A853"/>
                    <path d="M3.96 10.72c-.18-.54-.28-1.12-.28-1.72s.1-1.18.28-1.72V5H.95C.34 6.2.0 7.56.0 9s.34 2.8.95 4v-2.28z" fill="#FBBC05"/>
                    <path d="M9 3.58c1.32 0 2.5.45 3.44 1.35L15 2.4C13.46.97 11.43 0 9 0 5.48 0 2.43 2.07.95 5.07l3.01 2.33c.71-2.14 2.69-3.72 5.04-3.72z" fill="#EA4335"/>
                </svg>
                Google
            </a>
            <a href="/?sso=microsoft" target="_self" class="sso-btn">
                <svg width="16" height="16" viewBox="0 0 23 23">
                    <rect x="0" y="0" width="11" height="11" fill="#F25022"/>
                    <rect x="12" y="0" width="11" height="11" fill="#7FBA00"/>
                    <rect x="0" y="12" width="11" height="11" fill="#00A4EF"/>
                    <rect x="12" y="12" width="11" height="11" fill="#FFB900"/>
                </svg>
                Microsoft
            </a>
        </div>
        """
        st.html(sso_html)
        
        # Link to login page
        login_link_html = """
        <div style="text-align: center; font-size: 0.85rem; color: #94A3B8;">
            Already have an account? <a href="/?page=login" target="_self" style="color: #3B82F6; text-decoration: none; font-weight: 600;">Sign In</a>
        </div>
        """
        st.html(login_link_html)
        
        st.markdown("</div>", unsafe_allow_html=True)
