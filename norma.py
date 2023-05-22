import gradio as gr
import openai
import librosa
from pydub import AudioSegment
import pyttsx3
import requests
from urllib import parse

openai.api_key = "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"

chat_content = "The following is a conversation with an AI assistant. " \
               "The assistant is helpful, creative, clever, and very friendly.\n\n" \
               "Human: Hello, who are you?\n" \
               "AI: I am Norma, an AI created by OpenAI. How can I help you today?\n" \
               "Human: Use the language I used to relpy me.\n" \
               "AI: Ok."

sound_list = []
text = ""
stop_count = 0
history = ""

language_dict = {
    'af': 'Afrikaans',
    'sq': 'Shqip',
    'am': 'አማርኛ',
    'ar': 'العربية',
    'hy': 'Հայերեն',
    'az': 'Azərbaycan dili',
    'eu': 'Euskara',
    'be': 'Беларуская',
    'bn': 'বাংলা',
    'bs': 'Bosanski',
    'bg': 'Български',
    'ca': 'Català',
    'ceb': 'Cebuano',
    'ny': 'Chichewa',
    'zh': '简体中文',
    'co': 'Corsu',
    'hr': 'Hrvatski',
    'cs': 'Čeština',
    'da': 'Dansk',
    'nl': 'Nederlands',
    'en': 'English',
    'eo': 'Esperanto',
    'et': 'Eesti',
    'tl': 'Filipino',
    'fi': 'Suomi',
    'fr': 'Français',
    'fy': 'Frysk',
    'gl': 'Galego',
    'ka': 'ქართული',
    'de': 'Deutsch',
    'el': 'Ελληνικά',
    'gu': 'ગુજરાતી',
    'ht': 'Kreyòl Ayisyen',
    'ha': 'Hausa',
    'haw': 'ʻŌlelo Hawaiʻi',
    'iw': 'עברית',
    'hi': 'हिन्दी',
    'hmn': 'Hmong',
    'hu': 'Magyar',
    'is': 'Íslenska',
    'ig': 'Igbo',
    'id': 'Bahasa Indonesia',
    'ga': 'Gaeilge',
    'it': 'Italiano',
    'ja': '日本語',
    'jw': 'Basa Jawa',
    'kn': 'ಕನ್ನಡ',
    'kk': 'Қазақ тілі',
    'km': 'ភាសាខ្មែរ',
    'ko': '한국어',
    'ku': 'Kurdî',
    'ky': 'Кыргызча',
    'lo': 'ລາວ',
    'la': 'Latina',
    'lv': 'Latviešu',
    'lt': 'Lietuvių',
    'lb': 'Lëtzebuergesch',
    'mk': 'Македонски',
    'mg': 'Malagasy',
    'ms': 'Bahasa Melayu',
    'ml': 'മലയാളം',
    'mt': 'Malti',
    'mi': 'Māori',
    'mr': 'मराठी',
    'mn': '蒙古文',
    'my': 'မြန်မာ',
    'ne': 'नेपाली',
    'no': 'Norsk',
    'ps': 'پښتو',
    'fa': 'فارسی',
    'pl': 'Polski',
    'pt': 'Português',
    'pa': 'ਪੰਜਾਬੀ',
    'ro': 'Română',
    'ru': 'Русский',
    'sm': 'Gagana Samoa',
    'gd': 'Gàidhlig',
    'sr': 'Српски',
    'st': 'Sesotho',
    'sn': 'Shona',
    'sd': 'سنڌي',
    'si': 'සිංහල',
    'sk': 'Slovenčina',
    'sl': 'Slovenščina',
    'so': 'Soomaali',
    'es': 'Español',
    'su': 'Basa Sunda',
    'sw': 'Kiswahili',
    'sv': 'Svenska',
    'tg': 'Тоҷикӣ',
    'ta': 'தமிழ்',
    'tt': 'Татарча',
    'te': 'తెలుగు',
    'th': 'ไทย',
    'tr': 'Türkçe',
    'tk': 'Türkmen',
    'uk': 'Українська',
    'ur': 'اردو',
    'ug': 'ئۇيغۇرچە',
    'uz': 'Oʻzbek',
    'vi': 'Tiếng Việt',
    'cy': 'Cymraeg',
    'xh': 'isiXhosa',
    'yi': 'ייִדיש',
    'yo': 'Yorùbá',
    'zu': 'isiZulu'
    }
reversed_languages = {value: key for key, value in language_dict.items()}


def transcribe(audio, language, request: gr.Request):
    url = parse.urlparse(request.headers['referer'])

    global history
    global chat_content
    global sound_list
    global text
    global stop_count

    my_token = parse.parse_qs(url.query)["token"][0]

    y, sr = librosa.load(audio)

    # 计算RMS能量
    rms = librosa.feature.rms(y=y)

    # 判断RMS能量是否超过阈值
    threshold = 0.1

    hint = 'Try to speak something'

    vip = requests.get("http://192.168.18.2:5000/api/user/limitation?token=%s" % my_token).json()["data"]["vip"]

    if rms.max() > threshold:
        print('------------Detect somebody is speaking now------------')

        sound_list.append(AudioSegment.from_wav(audio))
        stop_count = 0
        return hint, text, requests.get("http://192.168.18.2:5000/api/user/limitation?token=%s" % my_token).json()["data"]["left_times"]

    else:
        stop_count = stop_count + 1
        if sound_list:
            if stop_count > 5:
                if not vip:
                    limitation = requests.get("http://192.168.18.2:5000/api/user/limitation?token=%s" % my_token).json()["data"]["left_times"]
                    if limitation <= 0:
                        return "You have reached the limitation today, welcome to upgrade your account.", text, limitation
                combined_sound = None
                for sound in sound_list:
                    if combined_sound:
                        combined_sound = combined_sound + sound
                    else:
                        combined_sound = sound
                combined_sound.export("combined_audio.wav", format="wav")
                sound_list = []

                with open("combined_audio.wav", "rb") as audio_file:
                    language = reversed_languages[language]
                    transcript = str(openai.Audio.transcribe("whisper-1", file=audio_file, language=language)["text"])
                    print(transcript)
                if transcript != "":
                    chat_content = chat_content + "Human: %s\nAI:" % transcript

                    response = openai.Completion.create(
                        model="text-davinci-003",
                        prompt=chat_content,
                        temperature=0.9,
                        max_tokens=150,
                        top_p=1,
                        frequency_penalty=0.0,
                        presence_penalty=0.6,
                        stop=[" Human:", " AI:"]
                    )

                    chat_content = chat_content + response["choices"][0]["text"] + "\n"

                    text = response["choices"][0]["text"]
                    print(text)
                    pyttsx3.speak(text)
                    data1 = {
                               "content": transcript,
                               "token": my_token
                    }
                    data2 = {
                        "content": text,
                        "token": my_token
                    }
                    requests.post("http://192.168.18.2:5000/api/record/add", data=data1)
                    requests.post("http://192.168.18.2:5000/api/record/add", data=data2)
                    requests.put("http://192.168.18.2:5000/api/user/limitation?token=%s" % my_token)
                    stop_count = 0
                    if stop_count > 20:
                        hint = 'Are you still here? Or maybe you are muted.'

                    if requests.get("http://192.168.18.2:5000/api/user/limitation?token=%s" % my_token).json()["data"]["left_times"]:
                        return hint, text, requests.get("http://192.168.18.2:5000/api/user/limitation?token=%s" % my_token).json()["data"]["left_times"]
                    else:
                        return hint, text, "You are VIP, there is no limitation."
            else:
                sound_list.append(AudioSegment.from_wav(audio))
                if stop_count > 20:
                    hint = 'Are you still here? Or maybe you are muted.'
                if requests.get("http://192.168.18.2:5000/api/user/limitation?token=%s" % my_token).json()["data"][
                    "left_times"]:
                    return hint, text, \
                           requests.get("http://192.168.18.2:5000/api/user/limitation?token=%s" % my_token).json()[
                               "data"]["left_times"]
                else:
                    return hint, text, "You are VIP, there is no limitation."
        if stop_count > 20:
            hint = 'Are you still here? Or maybe you are muted.'

        if requests.get("http://192.168.18.2:5000/api/user/limitation?token=%s" % my_token).json()["data"][
            "left_times"]:
            return hint, text, \
                   requests.get("http://192.168.18.2:5000/api/user/limitation?token=%s" % my_token).json()["data"][
                       "left_times"]
        else:
            return hint, text, "You are VIP, there is no limitation."


app = gr.Interface(
    fn=transcribe,
    inputs=[
        gr.Audio(source="microphone", type="filepath", streaming=True),
        gr.Dropdown(choices=[key for key in reversed_languages.keys()], value='English', label='language')
    ],
    outputs=[
        gr.Textbox(label='Hint', value='Try to speak something'),
        gr.Textbox(label='Reply'),
        gr.Textbox(label='limitation'),
    ],
    live=True,
)

app.launch()
