# AiTest
Spoken Hebrew – AI-Driven Language Practice Platform
### Helping Arabic Speakers & ORT Students

An interactive, AI-powered platform designed to help users practice and improve their spoken language skills through real-time conversation simulation, speech recognition, and instant feedback.

👉 **Try the Live App:** [ai--test.streamlit.app](https://ai--test.streamlit.app)

## 🚀 Features

* **Real-Time Spoken Interaction:** Integrates OpenAI Whisper for accurate speech-to-text transcription.
* **AI-Powered Evaluation:** Leverages advanced GPT models to analyze responses and provide instant feedback.
* **Interactive UI:** Built with Streamlit for a seamless, responsive user experience.
* **Tech Stack:** Python, Streamlit, MongoDB, OpenAI API (GPT models & Whisper).

## 🏗️ System Architecture

1. **Audio Capture & Transcription:** User audio is captured via Streamlit and processed using Whisper.
2. **LLM Processing:** Transcribed text is evaluated by GPT models configured for conversational scenarios.
3. **Data Persistence:** Session logs and metrics are stored in MongoDB.

## 🎓 Academic Context
Developed as an AI-driven spoken language practice platform for an academic project showcase under the supervision of Gadi.

## ⚙️ Getting Started

Run the following commands in your terminal:

```bash
# 1. Clone the repository
git clone [https://github.com/AmeedKe/AiTest_MVP.git](https://github.com/AmeedKe/AiTest_MVP.git)
cd AiTest_MVP

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables in a .env file:
# OPENAI_API_KEY=X
# MONGO_URI=X

# 4. Run the application
streamlit run src/app.py
