import streamlit as st
import os
import openai
from openai import OpenAI
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

# --- הגדרות ה-API ---
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

try:
    mongo_client = MongoClient(os.getenv("MONGO_URI"))
    db = mongo_client["iTest_DB"]
    collection = db["interactions"]
except Exception:
    pass  # We will just silently ignore DB errors for the MVP UI

# --- הגדרות עמוד ---
st.set_page_config(page_title="iTest", page_icon="🪄", layout="centered")

# --- CSS פרימיום מונפש (עיצוב בסגנון React/Next.js) ---
st.markdown("""
<style>
/* ייבוא פונטים מודרניים */
@import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;600;800;900&display=swap');

* {
    font-family: 'Heebo', sans-serif !important;
}

/* 1. רקע הגרדיאנט המונפש - משתלט על כל האפליקציה */
.stApp {
    background: linear-gradient(-45deg, #FF9A9E, #FECFEF, #A1C4FD, #C2E9FB);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    direction: rtl;
    text-align: right;
}

@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* 2. כרטיסייה ראשית - אפקט זכוכית יוקרתי (Glassmorphism) */
div.block-container {
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(25px);
    -webkit-backdrop-filter: blur(25px);
    border-radius: 40px;
    border: 1px solid rgba(255, 255, 255, 1);
    box-shadow: 0 40px 80px rgba(0,0,0,0.1) !important;
    padding: 4rem 3rem 5rem 3rem !important;
    max-width: 800px !important;
    margin-top: 5vh;
    margin-bottom: 5vh;
}

/* 3. כותרות האפליקציה */
h1 {
    font-weight: 900 !important;
    font-size: 4.5rem !important;
    background: -webkit-linear-gradient(45deg, #FF6B6B, #5X0CFF);
    background: linear-gradient(45deg, #ff416c, #ff4b2b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 0px !important;
    padding-bottom: 0px !important;
    text-shadow: 0px 10px 20px rgba(255,107,107,0.1);
}

h3.subtitle {
    text-align: center;
    color: #4A4A4A;
    font-weight: 400 !important;
    font-size: 1.5rem !important;
    margin-top: -10px !important;
    margin-bottom: 3rem !important;
    letter-spacing: -0.5px;
}

/* 4. רכיב ההקלטה (Audio Input) */
div[data-testid="stAudioInput"] {
    background: #ffffff !important;
    border: 2px dashed #a5b1c2 !important;
    border-radius: 30px !important;
    padding: 2.5rem !important;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    box-shadow: 0 10px 30px rgba(0,0,0,0.03) !important;
    display: flex;
    justify-content: center;
    margin-bottom: 2rem;
}

div[data-testid="stAudioInput"]:hover {
    border-color: #ff416c !important;
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 20px 40px rgba(255, 65, 108, 0.2) !important;
    background: #fffafa !important;
}

/* 5. תיבות צ'אט (פידבק המורה) */
div.stChatMessage {
    background: #ffffff !important;
    border-radius: 24px !important;
    padding: 1.5rem 2rem !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.06) !important;
    border: 1px solid rgba(0,0,0,0.03) !important;
    margin-bottom: 1.5rem;
    font-size: 1.2rem;
    color: #2f3542 !important;
}

/* אנימציות וריווח הודעות תצוגה */
.stAlert {
    border-radius: 20px !important;
    border: none !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
}

.ai-response-box {
    font-size: 1.4rem;
    color: #2d3436;
    background: #fdfbfb;
    padding: 20px 30px;
    border-radius: 20px;
    border-right: 5px solid #ff4b2b;
    box-shadow: 0 4px 10px rgba(0,0,0,0.03);
    margin: 10px 0 30px 0;
    font-weight: 500;
}

/* 6. אנימציית קפיצה והופעה לכל האלמנטים בעמוד */
.block-container, [data-testid="stAudioInput"], .stChatMessage, .stAlert, .ai-response-box {
    animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1.2) forwards;
    opacity: 0;
}

@keyframes fadeUp {
    0% { opacity: 0; transform: translateY(40px) scale(0.95); }
    100% { opacity: 1; transform: translateY(0) scale(1); }
}

/* Delay for different elements */
h1 { animation-delay: 0.1s; }
.subtitle { animation-delay: 0.2s; }
[data-testid="stAudioInput"] { animation-delay: 0.3s; }

/* 7. הסתרת אלמנטים מיותרים של Streamlit */
header, footer, #MainMenu {
    visibility: hidden !important;
    height: 0px !important;
}
</style>
""", unsafe_allow_html=True)

# כותרת והסבר
st.markdown("<h1>iTest ✨</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='subtitle'>המורה הווירטואלי והחכם לעברית</h3>", unsafe_allow_html=True)

# --- פונקציות חכמות ותפיסת שגיאות API ---
def get_pedagogical_feedback(student_text):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "אתה מורה לספרות ולשון סבלני שאוהב ילדים. חזק את הילד (דובר ערבית) על משפטו בעברית. אם מצאת טעות, עזור לו לתקן בעדינות ובהתלהבות. השתמש באימוג'ים כדי לעשות את המשוב כיפי!"},
                {"role": "user", "content": f"הילד אמר: '{student_text}'"}
            ]
        )
        return response.choices[0].message.content
        
    except openai.RateLimitError:
        return "ERROR_QUOTA"
    except Exception as e:
        return f"אופס, משהו השתבש עם האינטליגנציה המלאכותית: {e}"

# אזור ההקלטה
recorded_audio = st.audio_input("👈 לחץ כאן והקלט משפט בעברית:")

if recorded_audio is not None:
    # וידוא שאין עומס/חריגת מכסה ב-OpenAI ממש על ההתחלה
    try:
        with st.spinner('המורה iTest מקשיב וחושב... 🤔'):
            
            # עבודה עם הקובץ הזמני
            with open("temp_audio.wav", "wb") as f:
                f.write(recorded_audio.getbuffer())
            
            with open("temp_audio.wav", "rb") as audio_file:
                # ניסיון תמלול
                transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file, language="he")
                user_text = transcript.text

            # ניסיון קבלת משוב מהמורה הווירטואלי
            ai_feedback = get_pedagogical_feedback(user_text)

            # טיפול במצב שבו נגמרה המכסה ל-GPT, אך רק התמלול עבד
            if ai_feedback == "ERROR_QUOTA":
                st.error("🚨 המכסה שלך ב-OpenAI ירדה לאפס (RateLimitError/Quota Exceeded). יש לעדכן את כרטיס האשראי או להוסיף יתרה בחשבון ה-API שלך ב-OpenAI.")
                st.markdown(f"**הצלחת להקליט:** {user_text}")
                st.stop()
            
            # שמירה נתונים חכמה, אם נכשל - מדלג מבלי להפיל את האפליקציה בגלל דאטה-בייס
            try:
                collection.insert_one({
                    "user_id": "ameed_student_v2",
                    "transcribed_text": user_text,
                    "ai_feedback": ai_feedback,
                    "timestamp": datetime.now()
                })
            except Exception:
                pass 

        # --- תצוגת התוצאה המושלמת ב-UI ---
        st.markdown(f"<div class='ai-response-box'>🎤 <b>הילד אמר:</b><br>{user_text}</div>", unsafe_allow_html=True)
        
        with st.chat_message("assistant"):
            st.markdown(f"<div style='line-height: 1.8; font-size: 1.25rem;'>{ai_feedback}</div>", unsafe_allow_html=True)
            
    except openai.RateLimitError:
         st.error("🚨 תקלה: המכסה שלך ב-OpenAI הסתיימה או שאתה ב-Rate Limit (שגיאה 429). אנא בדוק את החשבון המפתח שלך! 💳")
    except Exception as e:
         st.error(f"אופס! שגיאה מפתיעה קרתה: {e}")