import pyaudio
import wave
import nemo.collections.asr as nemo_asr


class Recognition:

    def __init__(self):
        self.__CHUNK = 1024
        self.__FORMAT = pyaudio.paInt16
        self.__CHANNELS = 1
        self.__RATE = 16000
        self.__OUTPUT_FILENAME = "processed_audio.wav"
        self.__AUDIO_PATH = f"./{self.__OUTPUT_FILENAME}"

        self.__sber_quartzNet = nemo_asr.models.EncDecCTCModel.restore_from("./ZMv")

    def record(self, is_recording):
        p = pyaudio.PyAudio()

        stream = p.open(format=self.__FORMAT,
                        channels=self.__CHANNELS,
                        rate=self.__RATE,
                        input=True,
                        frames_per_buffer=self.__CHUNK)

        print("* recording")

        frames = []

        while is_recording[0]:
            data = stream.read(self.__CHUNK)
            frames.append(data)

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(self.__OUTPUT_FILENAME, 'wb')
        wf.setnchannels(self.__CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.__FORMAT))
        wf.setframerate(self.__RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

    def __recognize(self, language: str) -> str:
        files = [self.__AUDIO_PATH]
        transcripts = self.__sber_quartzNet.transcribe(paths2audio_files=files)
        print("* done transcribing")
        return transcripts[0]

    def recognize_speech(self, language: str) -> str:
        transcript = self.__recognize(language)
        print("* done speech recognize")
        return transcript
