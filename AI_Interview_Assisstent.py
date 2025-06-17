import openai
import speech_recognition as sr
import pyttsx3

# Replace with your actual API key
client = openai.OpenAI(api_key="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")

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
mic = sr.Microphone()
tts = pyttsx3.init()

# Optional: Configure TTS voice (you can skip this or tweak)
tts.setProperty('rate', 180)

def transcribe_audio():
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("\n🟢 Listening for a question...")
        audio = recognizer.listen(source)
    try:
        question = recognizer.recognize_google(audio)
        print(f"🗣 Interviewer asked: {question}")
        return question
    except sr.UnknownValueError:
        print("❌ Couldn't understand. Ask again.")
        return None
    except sr.RequestError as e:
        print(f"⚠️ API error: {e}")
        return None

def get_chatgpt_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


print("🎙️ AI Interview Assistant is now active. Say 'stop' to quit.")

try:
    while True:
        question = transcribe_audio()
        if question is None:
            continue
        if question.lower() in ["stop", "exit", "quit"]:
            print("👋 Session ended.")
            break

        answer = get_chatgpt_response(question)
        print(f"🤖 Suggested Answer: {answer}")

except KeyboardInterrupt:
    print("\n👋 Manually stopped.")
