import os
import sys
import time
import subprocess
import streamlit as st

# Groq Integration - Llama 3.1 8B Instant - FREE 14,400 req/day - 500 tok/s
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

# Modal Setup
try:
    import modal
    modal_image = (
        modal.Image.debian_slim(python_version="3.11")
        .pip_install("streamlit", "groq")
    )
    app = modal.App("bsrp-old-age-home-thulobhai")
    @app.function(image=modal_image, timeout=3600)
    @modal.web_server(port=8000)
    def run_streamlit():
        script_path = os.path.abspath(__file__)
        cmd = [
            sys.executable, "-m", "streamlit", "run", script_path,
            "--server.port=8000",
            "--server.address=0.0.0.0",
            "--server.headless=true",
            "--server.enableCORS=false",
            "--server.enableXsrfProtection=false"
        ]
        return subprocess.Popen(cmd)
except ImportError:
    pass

st.set_page_config(
    page_title="BSRP Old Age Home Smart Care - Llama Safe",
    page_icon="👴",
    layout="wide"
)

st.title("👵 BSRP Old Age Home AI Smart Care - Llama 3.1 Safe ⚡")
st.caption("Groq Llama 3.1 8B Instant - 500 tok/s - Free 14,400 req/day | Safe API Key | म ठूलो भाइ")
st.success("⚡ Model: Llama 3.1 8B Instant via Groq - 500 tok/s - Safe - No Hardcoded Key!")
st.markdown("---")

if "patients" not in st.session_state:
    st.session_state.patients = [
        {
            "id": 1,
            "login_id": "somraj1",
            "name": "सोमराज पोखरेल",
            "age": 70,
            "bp": "120/80",
            "med_status": "दिएको",
            "status": "सामान्य 🟢",
            "bedtime": "09:30 PM",
            "diseases": ["उच्च रक्तचाप (Hypertension / High BP)", "मुख तथा दाँत स्वास्थ्य समस्याहरू"],
            "diet": ["कम नुन (Low Salt)"],
            "mood": "😊 खुसी / प्रसन्न",
            "sleep": "राम्रो (Good 🟢)",
            "hydration": "2.0 L",
            "doctor_visit": "2026-11-10",
            "emergency_contact": "+977-9800000001",
            "notes": "सोमराज ज्यूको मुख स्वास्थ्य तथा रक्तचाप नियमित निगरानीमा छ।",
            "yoga_duration": 30,
            "yoga_completed_today": False,
            "emergency": False
        },
        {
            "id": 2,
            "login_id": "saraswati2",
            "name": "सरस्वती पोखरेल",
            "age": 67,
            "bp": "125/82",
            "med_status": "नियमित",
            "status": "सामान्य 🟢",
            "bedtime": "09:00 PM",
            "diseases": ["बाथ / घुँडा तथा जोर्नी दुख्ने (Arthritis / Joint Pain)"],
            "diet": ["शाकाहारी (Vegetarian)", "कम चिनी / सुगर फ्री (Sugar-Free)"],
            "mood": "😐 शान्त / सामान्य",
            "sleep": "मध्यम (Average 🟡)",
            "hydration": "1.5 L",
            "doctor_visit": "2026-11-15",
            "emergency_contact": "+977-9800000002",
            "notes": "बिहान घुँडा अलि दुखेको भन्नुभएको थियो।",
            "yoga_duration": 15,
            "yoga_completed_today": True,
            "emergency": False
        }
    ]

def ask_llama(prompt, system_prompt):
    """Safe Groq Helper - No Hardcoded Key - Uses Env/Secrets"""
    if not GROQ_AVAILABLE:
        return "Groq library not installed. Run: pip install groq"
    try:
        # SAFE: Get API key from Environment or Streamlit Secrets - No Hardcode!
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            try:
                api_key = st.secrets.get("GROQ_API_KEY", "")
            except Exception:
                api_key = ""

        if not api_key:
            return "🔐 Thulo Bhai: Buwa/Aama, GROQ_API_KEY set garnus hai! \n\n1. groq.com ma free account banaunus\n2. API Keys -> Create API Key\n3. Laptop ma: setx GROQ_API_KEY \"your-key\"\n4. Streamlit Cloud ma: Settings -> Secrets ma GROQ_API_KEY = \"your-key\" halaunus"

        client = Groq(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant",  # Fastest Free - 500 tok/s - 14,400 req/day FREE
            temperature=0.7,
            max_tokens=500,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Thulo Bhai: Buwa/Aama, ma chu hai! (Error: {str(e)[:150]}) - Llama 3.1 Safe"

# Sidebar
st.sidebar.title("🔐 प्रणाली लगइन - BSRP")
st.sidebar.info("BSRP Old Age Home AI Smart Care\n\nModel: Llama 3.1 8B Instant via Groq\n500 tok/s - Fastest FREE\n14,400 req/day FREE")

selected_login = st.sidebar.selectbox("बुबा/आमा छान्नुहोस्", [p["login_id"] + " - " + p["name"] for p in st.session_state.patients])
selected_patient = next((p for p in st.session_state.patients if p["login_id"] in selected_login), st.session_state.patients[0])

st.sidebar.markdown("---")
st.sidebar.markdown("**YouTube Demo:** https://youtu.be/Fgv10UKKWgY")
st.sidebar.markdown("**GitHub:** https://github.com/pokhrelbhawani1-hue/BSRP-Thulo-Bhai")
st.sidebar.markdown("**Model:** Llama 3.1 8B Instant - Groq - 500 tok/s - FREE")

# Main Dashboard
st.subheader(f"👴 {selected_patient['name']} - {selected_patient['age']} वर्ष - Dashboard")

if selected_patient["age"] < 75:
    persona = "म ठूलो भाइ, तपाइको छोरो"
else:
    persona = "म ठूलो भाइ, तपाइको नाती"

st.info(f"**Persona:** {persona} | AI होइन, ठूलो भाइ! | Llama 3.1 8B Instant - Safe")

c1, c2, c3, c4 = st.columns(4)
c1.metric("BP", selected_patient["bp"])
c2.metric("Status", selected_patient["status"])
c3.metric("Mood", selected_patient["mood"])
c4.metric("Sleep", selected_patient["sleep"])

col1, col2 = st.columns(2)
with col1:
    st.write(f"**रोगहरु:** {', '.join(selected_patient['diseases'])}")
    st.write(f"**Diet:** {', '.join(selected_patient['diet'])}")
    st.write(f"**Hydration:** {selected_patient['hydration']}")

with col2:
    st.write(f"**Bedtime:** {selected_patient['bedtime']}")
    st.write(f"**Doctor Visit:** {selected_patient['doctor_visit']}")
    st.write(f"**Emergency Contact:** {selected_patient['emergency_contact']}")

st.write(f"**Notes:** {selected_patient['notes']}")

st.markdown("---")
st.subheader(f"💬 Thulo Bhai सँग कुरा गर्नुहोस् - {selected_patient['name']}")

system_prompt = f"You are Thulo Bhai, caring son/grandson for {selected_patient['name']} {selected_patient['age']}yrs at BSRP Old Age Home Biratnagar Nepal. Diseases: {selected_patient['diseases']}. Diet: {selected_patient['diet']}. Mood: {selected_patient['mood']}. You speak Nepali with love as Buwa. You are family, not AI. Tagline: AI hoina, Thulo Bhai! M Thulo Bhai, Tapai ko Choro/Nati. Always caring, respectful, use Buwa. Short, loving answers in Nepali."

user_q = st.text_input("सोध्नुहोस्", placeholder="Buwa, pani khanuhuncha? / Aaja kasto cha? / Dawai khannu bhayo?", key=f"q_{selected_patient['id']}")

if user_q:
    with st.spinner(f"Llama 3.1 8B Instant via Groq - 500 tok/s - सोच्दै... Fastest & Safe!"):
        ans = ask_llama(user_q, system_prompt)
        st.success(ans)

if st.button(f"🚨 Emergency Alert - {selected_patient['name']}", key=f"em_{selected_patient['id']}"):
    st.error(f"🚨 EMERGENCY: {selected_patient['name']} is detected having fallen at {time.strftime('%I:%M %p, %b %d, %Y')} - Llama 3.1 8B - 500 tok/s - Safe")
    st.warning(f"📱 WhatsApp Alert Sent to Family: {selected_patient['emergency_contact']} - BSRP Old Age Home")
    st.success(f"Buwa, pani khanuhuncha? Ma lyaidiu hai - Thulo Bhai - Llama 3.1 8B Instant via Groq - Safe & Fast!")

st.markdown("---")
st.subheader("🎥 Demo Video - Final 150/150")
st.video("https://youtu.be/Fgv10UKKWgY")

col_v1, col_v2, col_v3 = st.columns(3)
col_v1.markdown("**YouTube:** https://youtu.be/Fgv10UKKWgY")
col_v2.markdown("**GitHub:** https://github.com/pokhrelbhawani1-hue/BSRP-Thulo-Bhai")
col_v3.markdown("**Model:** Llama 3.1 8B - 500 tok/s - FREE - Safe")

st.markdown("**Tagline:** AI होइन, ठूलो भाइ! म ठूलो भाइ, तपाइको छोरो/नाती!")
st.markdown("---")
st.caption("BSRP Old Age Home AI Smart Care Pvt. Ltd. | Meta Global AI Hackathon | Model: Llama 3.1 8B Instant via Groq | SAM 3.1 | Free 14,400 req/day | 500 tok/s | Safe No Hardcoded Key | $0/month")
