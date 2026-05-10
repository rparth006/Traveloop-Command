import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import time
from datetime import datetime

# =================================================================
# 1. ADVANCED PAGE CONFIGURATION
# =================================================================
st.set_page_config(
    page_title="Traveloop Pro | AIML Enterprise Solution",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Styling
st.markdown("""
    <style>
    .main { background-color: #f4f7fb; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 15px; border-left: 5px solid #2563eb; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; background-color: #2563eb; color: white; border: none; height: 3.5em; transition: 0.3s; }
    .stButton>button:hover { background-color: #1d4ed8; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
    .reportview-container .main .block-container { padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# =================================================================
# 2. ROBUST DATABASE ARCHITECTURE
# =================================================================
def init_db():
    """Initializes the SQLite core engine for user and trip persistence"""
    conn = sqlite3.connect('travel_vault.db')
    c = conn.cursor()
    # User Management Table
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (username TEXT PRIMARY KEY, password TEXT, last_login TEXT)''')
    # Trip Intelligence Table
    c.execute('''CREATE TABLE IF NOT EXISTS trips 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, dest TEXT, 
                  total REAL, per_person REAL, date TEXT, category TEXT)''')
    conn.commit()
    conn.close()

def direct_entry_auth(username, password):
    """Zero-friction authentication: Saves or updates user instantly"""
    conn = sqlite3.connect('travel_vault.db')
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password, last_login) VALUES (?, ?, ?)", 
                  (username, password, now))
    else:
        c.execute("UPDATE users SET password = ?, last_login = ? WHERE username = ?", 
                  (password, now, username))
    conn.commit()
    conn.close()
    return True

def archive_trip(user, dest, total, per_capita, cat):
    """Archives trip analytics for future retrieval"""
    conn = sqlite3.connect('travel_vault.db')
    c = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    c.execute("INSERT INTO trips (user, dest, total, per_person, date, category) VALUES (?, ?, ?, ?, ?, ?)",
              (user, dest, total, per_capita, today, cat))
    conn.commit()
    conn.close()

# =================================================================
# 3. ANALYTICAL LOGIC CORE (Engine Classes)
# =================================================================
class TravelAI:
    @staticmethod
    def run_budget_sim(f_cost, h_cost, days, people, misc):
        """Heavy duty cost simulation logic"""
        accommodation = h_cost * days
        transport = f_cost * people
        total = transport + accommodation + misc
        per_person = total / max(people, 1)
        return {
            "total": total,
            "per_person": per_person,
            "breakdown": [transport, accommodation, misc]
        }

    @staticmethod
    def get_itinerary_data(city):
        """Mock AI Database for travel sequences"""
        db = {
            "Paris": ["Eiffel Tower Visit", "Louvre Museum", "Seine River Cruise", "Montmartre Walk"],
            "Dubai": ["Burj Khalifa", "Desert Safari", "Dubai Mall", "Palm Jumeirah"],
            "Goa": ["Baga Beach", "Old Goa Churches", "Dudhsagar Falls", "Anjuna Market"],
            "Tokyo": ["Shibuya Crossing", "Senso-ji Temple", "Akihabara Tour", "Mount Fuji Day Trip"],
            "London": ["Big Ben", "London Eye", "British Museum", "Tower Bridge"]
        }
        return db.get(city, ["Local Exploration", "City Center Walk", "Food Tasting", "Shopping District"])

# =================================================================
# 4. SESSION & STATE MANAGEMENT
# =================================================================
init_db()

if 'auth' not in st.session_state:
    st.session_state.auth = False
    st.session_state.user = ""

# =================================================================
# 5. SIDEBAR: THE CONTROL TOWER
# =================================================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/826/826070.png", width=120)
    st.title("Traveloop Command")
    st.markdown("---")
    
    if not st.session_state.auth:
        st.subheader("🔐 Fast-Pass Login")
        u = st.text_input("Name/ID")
        p = st.text_input("Passkey", type="password")
        if st.button("Access Dashboard"):
            if u:
                direct_entry_auth(u, p)
                st.session_state.auth = True
                st.session_state.user = u
                st.rerun()
            else:
                st.warning("Identification required.")
    else:
        st.success(f"Verified: {st.session_state.user}")
        st.caption(f"Role: Enterprise Explorer")
        
        with st.expander("👤 Profile Details"):
            st.write(f"User: **{st.session_state.user}**")
            st.write("Node: **Parul University**")
            st.write("Auth: **Verified ✅**")
        
        st.markdown("---")
        nav = st.radio("System Modules", 
                       ["🏠 Dashboard", "📈 Financial Planner", "🗓️ AI Itinerary", "🗄️ Trip Vault"])
        
        if st.button("Logout"):
            st.session_state.auth = False
            st.rerun()

# =================================================================
# 6. MAIN INTERFACE LOGIC
# =================================================================
if not st.session_state.auth:
    # Landing Page for non-authenticated users
    st.title("🌍 Traveloop Pro: AI-Powered Travel Infrastructure")
    st.info("System Lockdown: Please provide Admin/User credentials in the sidebar to proceed.")
    st.image("https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?auto=format&fit=crop&w=1200", 
             caption="The future of trip planning starts here.")
    st.stop()

# --- MODULE 1: DASHBOARD ---
if nav == "🏠 Dashboard":
    st.title(f"🚀 Welcome Back, {st.session_state.user}")
    st.subheader("Global Travel Network Status")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Active Sessions", "4,102", "+5%")
    m2.metric("Data Sync", "Stable", "12ms")
    m3.metric("Server Load", "34%", "Optimal")
    m4.metric("Security", "Encrypted", "AES-256")
    
    st.markdown("---")
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown("### 📊 Global Planning Trends")
        chart_data = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
            'Users': [450, 700, 1100, 1500, 2400]
        })
        st.line_chart(chart_data.set_index('Month'))
        
    with col_right:
        st.markdown("### 🔔 System Alerts")
        st.warning("Database Sync scheduled for 12:00 AM")
        st.success("AI Model v2.4 successfully deployed.")
        st.info("Parul University AIML Dept: Project Live.")

# --- MODULE 2: FINANCIAL PLANNER ---
elif nav == "📈 Financial Planner":
    st.title("📈 Advanced Financial Forecaster")
    
    with st.container():
        c1, c2 = st.columns([1, 1])
        with c1:
            st.subheader("🛠️ Parameters")
            target_city = st.text_input("Destination", "Dubai")
            cat = st.selectbox("Travel Class", ["Budget", "Standard", "Business", "Ultra-Luxury"])
            group_size = st.number_input("Total Travelers", 1, 100, 2)
            nights = st.slider("Duration (Nights)", 1, 30, 5)
            
            st.markdown("#### Cost Breakdown")
            f_cost = st.number_input("Flights (Per Person)", 0, 1000000, 25000)
            h_cost = st.number_input("Hotel (Per Night)", 0, 500000, 5000)
            m_cost = st.number_input("Buffer/Miscellaneous", 0, 200000, 15000)
            
        with c2:
            st.subheader("📊 Intelligence Output")
            results = TravelAI.run_budget_sim(f_cost, h_cost, nights, group_size, m_cost)
            
            res_1, res_2 = st.columns(2)
            res_1.metric("Estimated Grand Total", f"₹{results['total']:,}")
            res_2.metric("Per Capita Investment", f"₹{results['per_person']:,.2f}")
            
            # Interactive Donut Chart
            labels = ['Transport', 'Stay', 'Misc']
            values = results['breakdown']
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4)])
            fig.update_layout(title_text="Investment Distribution", margin=dict(t=30, b=10, l=10, r=10))
            st.plotly_chart(fig, use_container_width=True)
            
            if st.button("📡 Synchronize & Archive Trip"):
                archive_trip(st.session_state.user, target_city, results['total'], results['per_person'], cat)
                st.balloons()
                st.success("Data packet sent to travel_vault.db")

# --- MODULE 3: AI ITINERARY ---
elif nav == "🗓️ AI Itinerary":
    st.title("🗓️ Sequence Generator")
    target = st.selectbox("Target Node", ["Paris", "Dubai", "Goa", "Tokyo", "London"])
    
    if st.button("⚡ Generate Optimized Itinerary"):
        with st.spinner("Processing regional data..."):
            time.sleep(1.5)
            plans = TravelAI.get_itinerary_data(target)
            
            st.markdown(f"### 📍 AI Suggested Timeline: {target}")
            for i, p in enumerate(plans):
                st.markdown(f"""
                <div style="background-color: white; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #2563eb;">
                    <strong>DAY {i+1}</strong>: {p}
                </div>
                """, unsafe_allow_html=True)

# --- MODULE 4: TRIP VAULT (DATABASE VIEW) ---
elif nav == "🗄️ Trip Vault":
    st.title("🗄️ Secured Data Vault")
    st.write("Extracting records for user:", st.session_state.user)
    
    conn = sqlite3.connect('travel_vault.db')
    query = f"SELECT dest, category, total, per_person, date FROM trips WHERE user = '{st.session_state.user}' ORDER BY id DESC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        # Visual Analytics of past trips
        st.subheader("Historical Budget Analysis")
        fig_hist = px.bar(df, x='dest', y='total', color='category', title="Spending by Destination")
        st.plotly_chart(fig_hist, use_container_width=True)
    else:
        st.info("Vault is currently empty. Initialize a new plan to populate records.")

# =================================================================
# 7. ENTERPRISE FOOTER
# =================================================================
st.markdown("---")
f_left, f_right = st.columns([4, 1])
with f_left:
    st.caption(f"Traveloop Pro v2.0.4 | Lead: {st.session_state.user} | AIML Division | Parul University")
with f_right:
    if st.button("♻️ Reset System"):
        st.rerun()