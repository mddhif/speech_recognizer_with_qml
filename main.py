# This Python file uses the following encoding: utf-8
import sys, os, time, pygame
import speech_recognition as sr


from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, QEventLoop, Signal

recognizer = sr.Recognizer()

def recognizeSpeech():

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            # connect to google api
            track_name = recognizer.recognize_google(audio, language="en-US", show_all=True)
            if "alternative" in track_name:
                alt_text = track_name["alternative"][0]["transcript"]
            else:

                alt_text = ""

            return alt_text

        except sr.UnknownValueError:
            print("Could not understand command")

        except sr.RequestError as e:
            print("Error fetching results (or track); {0}".format(e))


def stop(_):

    print("exiting recognition .....")
    sys.exit(0)



class Controller(QObject):

    updateLabel = Signal(str)

    def __init__(self):
           super().__init__()
           self.COMMANDS = {
                       "play track": self.play_track,
                       "stop": stop,

            }


    def playTrack(self, track_name):

        pygame.init()
        pygame.mixer.music.load(track_name)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        pygame.mixer.music.stop()
        pygame.quit()



    def play_track(self):

            time.sleep(3)

            self.updateLabel.emit("You entered this command : Play Track")
            print("Speak the track name!")
            alt_text = recognizeSpeech()
            if alt_text.lower() == 'exit':
                print("exiting track player...")

            else:
                self.playTrack(alt_text)
                #print(f"Playing track: {alt_text}")
                # time.sleep(30)



    def triggerPlayTrack(self, text):
            print("triggering play track...", text)

            self.updateLabel.emit(text)

            command_found = False
            for keyword, action in self.COMMANDS.items():
                print("checking commands ....")
                if keyword in text.lower():
                    #action(text.lower().replace(keyword, "").strip())
                    action()
                    command_found = True


            if not command_found:
                print("Command not recognized")

    @Slot()
    def command(self):
           prev_text = ""
           #while True:
           with sr.Microphone() as source:
                   print("Enter command ...")

                   alt_text = recognizeSpeech()


                   if prev_text:

                       text = prev_text + " " + alt_text
                   else:

                       text = alt_text


                   prev_text = alt_text
                   print("TEXT :",text)
                   self.triggerPlayTrack(text)
                   # self.updateLabel.emit(text)


    def startSignalThread(self,text):
          print("before emitting.....")
          self.updateLabel.emit(text)
          print("after emitting ...")
          loop = QEventLoop()
          self.updateLabel.connect(loop.quit)
          loop.exec_()




if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    controller = Controller()
    engine.rootContext().setContextProperty("controller", controller)
    engine.load(os.fspath(Path(__file__).resolve().parent / "main.qml"))
    # qml_file = Path(__file__).resolve().parent / "main.qml"

    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
