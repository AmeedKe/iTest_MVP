import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["iTest_DB"]
questions_col = db["questions"]

QUESTION_BANK = {
    "general": [
        "שימוש בטכנולוגיה בחיי היומיום",
        "רשתות חברתיות והשפעתן",
        "לחץ בלימודים",
        "עבודה מול לימודים",
        "חשיבות הספורט",
        "קשרים עם חברים ומשפחה",
        "השפעת הטלפון על בני נוער",
        "הצלחה – מה זה אומר?"
    ],
    "opinion": [
        "מה דעתך על שימוש בטלפונים בבית הספר?",
        "האם רשתות חברתיות עוזרות או פוגעות?",
        "האם חשוב לעבוד בזמן הלימודים?",
        "האם לדעתך צריך להגביל זמן מסך?",
        "מה יותר חשוב – ציונים או כישורים?",
        "האם בית הספר מכין לחיים האמיתיים?"
    ],
    "personal": [
        "ספר על חוויה משמעותית שהייתה לך",
        "מה התחביבים שלך ולמה אתה אוהב אותם?",
        "מי האדם שמשפיע עליך ולמה?",
        "איך נראה יום רגיל שלך?",
        "מה אתה רוצה לעשות בעתיד?"
    ],
    "comparison": [
        "השווה בין לימודים בבית ללימודים בבית ספר",
        "מה ההבדל בין חיים עם טכנולוגיה לחיים בלי?",
        "השווה בין עבודה כשכיר לעצמאי",
        "יתרונות וחסרונות של למידה מרחוק"
    ]
}

# Assign levels: personal -> 1, general -> 2, opinion -> 3, comparison -> 4
LEVEL_MAPPING = {
    "personal": 1,
    "general": 2,
    "opinion": 3,
    "comparison": 4
}

def seed():
    # Clear existing questions
    questions_col.delete_many({})
    
    docs = []
    for category, qs in QUESTION_BANK.items():
        level = LEVEL_MAPPING.get(category, 1)
        for q in qs:
            docs.append({
                "text": q,
                "category": category,
                "level": level
            })
            
    if docs:
        questions_col.insert_many(docs)
        print(f"Inserted {len(docs)} questions successfully!")

if __name__ == "__main__":
    seed()
