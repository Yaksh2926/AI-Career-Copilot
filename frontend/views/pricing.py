import streamlit as st
import textwrap

def show_pricing():
    """
    Renders a premium 3-tier SaaS pricing grid with glassmorphic cards and hover lifts.
    """
    pricing_header = """
    <div style="text-align: center; margin-bottom: 3rem;">
        <h1 class="hero-title" style="font-size: 3rem; font-weight: 800; letter-spacing: -1.5px; margin-bottom: 0.5rem;">SaaS Pricing Plans</h1>
        <p style="color: #94A3B8; font-size: 1rem; max-width: 500px; margin: 0 auto; line-height: 1.6;">
            Choose the plan that fits your career aspirations. Unlock advanced ATS scoring and unlimited mock interview packs.
        </p>
    </div>
    """
    st.markdown(textwrap.dedent(pricing_header), unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        # Starter Tier
        starter_html = """
        <div class="glass-card glass-card-hover" style="padding: 2.5rem 2rem; border-radius: 16px; height: 100%; display: flex; flex-direction: column; justify-content: space-between; border-top: 3px solid #94A3B8;">
            <div>
                <span style="font-size: 0.75rem; text-transform: uppercase; color: #94A3B8; font-weight: 700; letter-spacing: 1px;">Starter</span>
                <div style="font-family: 'Outfit', sans-serif; font-size: 2.5rem; font-weight: 800; color: #FFFFFF; margin-top: 0.5rem; margin-bottom: 0.5rem;">
                    $0 <span style="font-size: 1rem; color: #94A3B8; font-weight: 400;">/ mo</span>
                </div>
                <p style="color: #94A3B8; font-size: 0.85rem; line-height: 1.5; margin-bottom: 1.5rem;">For individuals testing their resume quality indices.</p>
                <div style="width: 100%; height: 1px; background: rgba(255,255,255,0.06); margin-bottom: 1.5rem;"></div>
                <ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 10px;">
                    <li style="font-size: 0.85rem; color: #E2E8F0; display: flex; align-items: center; gap: 8px;">
                        <span style="color: #22C55E;">✓</span> 3 Resume Uploads / mo
                    </li>
                    <li style="font-size: 0.85rem; color: #E2E8F0; display: flex; align-items: center; gap: 8px;">
                        <span style="color: #22C55E;">✓</span> Basic Skill Extraction
                    </li>
                    <li style="font-size: 0.85rem; color: #E2E8F0; display: flex; align-items: center; gap: 8px;">
                        <span style="color: #22C55E;">✓</span> Public Q&A Board
                    </li>
                    <li style="font-size: 0.85rem; color: #64748B; display: flex; align-items: center; gap: 8px; text-decoration: line-through;">
                        ✗ Unlimited ATS Checks
                    </li>
                    <li style="font-size: 0.85rem; color: #64748B; display: flex; align-items: center; gap: 8px; text-decoration: line-through;">
                        ✗ Interactive Roadmaps
                    </li>
                </ul>
            </div>
            <div style="margin-top: 2rem;">
                <a href="/?page=dashboard" target="_self" class="sidebar-upgrade-btn" style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08); box-shadow: none; display: block; text-align: center;">Get Started Free</a>
            </div>
        </div>
        """
        st.markdown(textwrap.dedent(starter_html), unsafe_allow_html=True)
        
    with col2:
        # Professional Tier (Highlighted)
        pro_html = """
        <div class="glass-card glass-card-hover" style="
            padding: 2.5rem 2rem; 
            border-radius: 16px; 
            height: 100%; 
            display: flex; 
            flex-direction: column; 
            justify-content: space-between; 
            border: 1px solid rgba(124, 58, 237, 0.4);
            border-top: 4px solid #7C3AED;
            box-shadow: 0 10px 30px rgba(124, 58, 237, 0.15);
            background: rgba(124, 58, 237, 0.02);
        ">
            <div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 0.75rem; text-transform: uppercase; color: #A855F7; font-weight: 700; letter-spacing: 1px;">Professional</span>
                    <span class="chip chip-primary" style="margin: 0; font-size: 0.65rem; padding: 2px 8px;">Popular</span>
                </div>
                <div style="font-family: 'Outfit', sans-serif; font-size: 2.5rem; font-weight: 800; color: #FFFFFF; margin-top: 0.5rem; margin-bottom: 0.5rem;">
                    $19 <span style="font-size: 1rem; color: #94A3B8; font-weight: 400;">/ mo</span>
                </div>
                <p style="color: #94A3B8; font-size: 0.85rem; line-height: 1.5; margin-bottom: 1.5rem;">For active job seekers optimizing match rates.</p>
                <div style="width: 100%; height: 1px; background: rgba(124, 58, 237, 0.15); margin-bottom: 1.5rem;"></div>
                <ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 10px;">
                    <li style="font-size: 0.85rem; color: #E2E8F0; display: flex; align-items: center; gap: 8px;">
                        <span style="color: #22C55E;">✓</span> Unlimited Resume Review
                    </li>
                    <li style="font-size: 0.85rem; color: #E2E8F0; display: flex; align-items: center; gap: 8px;">
                        <span style="color: #22C55E;">✓</span> Unlimited ATS Keyword Checks
                    </li>
                    <li style="font-size: 0.85rem; color: #E2E8F0; display: flex; align-items: center; gap: 8px;">
                        <span style="color: #22C55E;">✓</span> Month-by-month roadmaps
                    </li>
                    <li style="font-size: 0.85rem; color: #E2E8F0; display: flex; align-items: center; gap: 8px;">
                        <span style="color: #22C55E;">✓</span> Full Interview Prep Accordions
                    </li>
                    <li style="font-size: 0.85rem; color: #E2E8F0; display: flex; align-items: center; gap: 8px;">
                        <span style="color: #22C55E;">✓</span> Cover Letter & LinkedIn Optimizer
                    </li>
                </ul>
            </div>
            <div style="margin-top: 2rem;">
                <button onclick="alert('Subscription simulated successfully! Pro tier features are active.');" class="gradient-btn" style="display: block; width: 100%; text-align: center; border-radius: 8px;">Upgrade to Pro ➔</button>
            </div>
        </div>
        """
        st.markdown(textwrap.dedent(pro_html), unsafe_allow_html=True)
        
    with col3:
        # Enterprise Tier
        enterprise_html = """
        <div class="glass-card glass-card-hover" style="padding: 2.5rem 2rem; border-radius: 16px; height: 100%; display: flex; flex-direction: column; justify-content: space-between; border-top: 3px solid #3B82F6;">
            <div>
                <span style="font-size: 0.75rem; text-transform: uppercase; color: #3B82F6; font-weight: 700; letter-spacing: 1px;">Enterprise</span>
                <div style="font-family: 'Outfit', sans-serif; font-size: 2.5rem; font-weight: 800; color: #FFFFFF; margin-top: 0.5rem; margin-bottom: 0.5rem;">
                    $49 <span style="font-size: 1rem; color: #94A3B8; font-weight: 400;">/ mo</span>
                </div>
                <p style="color: #94A3B8; font-size: 0.85rem; line-height: 1.5; margin-bottom: 1.5rem;">For agencies and career counselling institutions.</p>
                <div style="width: 100%; height: 1px; background: rgba(255,255,255,0.06); margin-bottom: 1.5rem;"></div>
                <ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 10px;">
                    <li style="font-size: 0.85rem; color: #E2E8F0; display: flex; align-items: center; gap: 8px;">
                        <span style="color: #22C55E;">✓</span> Everything in Pro Plan
                    </li>
                    <li style="font-size: 0.85rem; color: #E2E8F0; display: flex; align-items: center; gap: 8px;">
                        <span style="color: #22C55E;">✓</span> Multi-candidate Dashboard
                    </li>
                    <li style="font-size: 0.85rem; color: #E2E8F0; display: flex; align-items: center; gap: 8px;">
                        <span style="color: #22C55E;">✓</span> Collaborative Saved Records
                    </li>
                    <li style="font-size: 0.85rem; color: #E2E8F0; display: flex; align-items: center; gap: 8px;">
                        <span style="color: #22C55E;">✓</span> Dedicated API Endpoint Keys
                    </li>
                    <li style="font-size: 0.85rem; color: #E2E8F0; display: flex; align-items: center; gap: 8px;">
                        <span style="color: #22C55E;">✓</span> SLA Support SLAs
                    </li>
                </ul>
            </div>
            <div style="margin-top: 2rem;">
                <button onclick="alert('Contacting sales department... request queued.');" style="
                    background: rgba(255, 255, 255, 0.05);
                    color: #FFFFFF;
                    border: 1px solid rgba(255, 255, 255, 0.08);
                    padding: 8px 0;
                    font-weight: 600;
                    font-size: 0.85rem;
                    border-radius: 8px;
                    width: 100%;
                    cursor: pointer;
                ">Contact Sales</button>
            </div>
        </div>
        """
        st.markdown(textwrap.dedent(enterprise_html), unsafe_allow_html=True)
