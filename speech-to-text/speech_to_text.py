import speech_recognition as sr

r = sr.Recognizer()

sr.Microphone.list_microphone_names()

micro = sr.Microphone(device_index=2)

with micro as source:
    print("Speak!")
    audio_data = r.listen(source)
    print("End!")
result = r.recognize_google(audio_data, language="fr-FR")
print (result)