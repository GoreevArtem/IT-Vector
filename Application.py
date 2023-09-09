from tkinter import Tk, Text, Button, Scrollbar, Frame
from Recognition import Recognition
from VoiceActing import VoiceActing
from DataBase import DataBase
import threading

is_recording = [False, ]


class Application:

    def __init__(self):
        self.__language = "ru"

        self.__window_height = 250
        self.__window_width = 400
        self.__frame_txt_height = 300
        self.__frame_btn_height = self.__window_height - self.__frame_txt_height
        self.__btn_height = 2
        self.__font = "Arial 12"

        self.__window = Tk()
        self.__window.title("VoiceAssistant")
        self.__window.geometry(f"{self.__window_width}x{self.__window_height}")

        self.__frame_txt = Frame(master=self.__window, borderwidth=1, relief="solid", height=self.__frame_txt_height)
        self.__frame_txt.pack(anchor="n", fill="both", padx=5, pady=5, expand=True)

        self.__frame_btn = Frame(master=self.__window, borderwidth=1, relief="solid", height=self.__frame_btn_height)
        self.__frame_btn.pack(anchor="s", fill="both", padx=5, pady=5, expand=True)

        self.__txt = Text(self.__frame_txt, font=self.__font)
        self.__txt.pack(anchor="center", fill="both", expand=True, side="top")

        self.__scroll = Scrollbar(master=self.__txt, orient="vertical", command=self.__txt.yview)
        self.__scroll.pack(side="right", fill="y")

        self.__btn_record = Button(master=self.__frame_btn, text="Запись", command=self.__clicked_btn_record,
                                   height=self.__btn_height)
        self.__btn_record.pack(anchor="center", fill="x", expand=True, side="bottom", padx=5)

        self.__btn_stop_record = Button(master=self.__frame_btn, text="Стоп", command=self.__clicked_btn_stop_record,
                                        height=self.__btn_height, state="disabled")
        self.__btn_stop_record.pack(anchor="center", fill="x", expand=True, side="bottom", before=self.__btn_record,
                                    padx=5)

        self.__recognition = Recognition()
        self.__voice_actor = VoiceActing()
        self.__database = DataBase()
        self.__thread = threading.Thread()

    def __clicked_btn_record(self):
        self.__txt.delete(0.0, "end")
        self.__btn_record.config(state='disabled')
        self.__btn_stop_record.config(state='normal')
        global is_recording
        is_recording[0] = True
        self.__thread = threading.Thread(target=self.__recognition.record, args=(is_recording,))
        self.__thread.start()

    def __clicked_btn_stop_record(self):
        self.__txt.delete(0.0, "end")
        self.__btn_stop_record.config(state='disabled')
        self.__btn_record.config(state='normal')
        global is_recording
        is_recording[0] = False
        self.__thread.join()
        text = self.convert_speech_to_text()
        print(f"транскрибированный текст: {text}")
        relevant_text = self.get_relevant_text(text)
        print(relevant_text)
        t1 = threading.Thread(target=self.__txt.insert, args=(0.0, relevant_text,))
        t2 = threading.Thread(target=self.voice_acting, args=(relevant_text,))

        t1.start()
        t2.start()

        # self.voice_acting(relevant_text)

    def convert_speech_to_text(self) -> str:
        text = self.__recognition.recognize_speech(self.__language)
        return text

    def voice_acting(self, text: str):
        self.__voice_actor.talk(text)

    def get_relevant_text(self, text: str) -> str:
        return self.__database.find_relevant_info(text)

    def run(self):
        self.__window.mainloop()
