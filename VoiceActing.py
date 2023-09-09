import pyttsx3


class VoiceActing:
    def __init__(self):
        self.__tts = pyttsx3.init()
        self.__rate = self.__tts.getProperty('rate')
        self.__tts.setProperty('rate', self.__rate - 40)
        self.__volume = self.__tts.getProperty('volume')
        self.__tts.setProperty('volume', self.__volume + 0.9)
        self.__voices = self.__tts.getProperty('voices')
        self.__tts.setProperty('voice', 'ru')
        for voice in self.__voices:
            if voice.name == 'Microsoft Irina Desktop - Russian':
                self.__tts.setProperty('voice', voice.id)

    def talk(self, text: str):
        self.__tts.say(text)
        self.__tts.runAndWait()
