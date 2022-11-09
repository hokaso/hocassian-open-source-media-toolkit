from threading import Event, Thread
import random
import pyaudio
import wave

# 定义数据流块
CHUNK = 1024


class BasePlayerThread(Thread):

    def __init__(
            self
    ):
        super().__init__()
        self.player = pyaudio.PyAudio()

        # 用于暂停线程的标识
        self.__flag = Event()
        self.__flag.set()

        self.ifdo = True

    def base_player(self, file):
        cur_wf = wave.open(file, 'rb')

        # 打开数据流
        stream = self.player.open(
            format=self.player.get_format_from_width(cur_wf.getsampwidth()),
            channels=cur_wf.getnchannels(),
            rate=cur_wf.getframerate(),
            output=True
        )

        data = cur_wf.readframes(CHUNK)
        while len(data) > 5:
            self.__flag.wait()
            stream.write(data)
            data = cur_wf.readframes(CHUNK)

        return stream

    def pause(self):
        self.__flag.clear()  # 设置为False, 让线程阻塞
        print("pause")

    def resume(self):
        self.__flag.set()  # 设置为True, 让线程停止阻塞
        print("resume")

    # def stop(self):
    #     print('I am stopping it...')
    #     self.ifdo = False


# 该方法需要做到轮播一组音频，并且实时暂停实时恢复
class CyclePlayerThread(BasePlayerThread):

    def __init__(self, file_list):
        super().__init__()
        self.file_list = file_list

    def run(self):

        while self.ifdo:
            random.shuffle(self.file_list)
            for file in self.file_list:
                _ = self.base_player(file)


class OneTimePlayerThread(BasePlayerThread):

    def __init__(self, file):
        super().__init__()
        self.file = file

    def run(self):
        stream = self.base_player(self.file)

        # 停止数据流
        stream.stop_stream()
        stream.close()

        # 关闭 PyAudio
        self.player.terminate()


if __name__ == "__main__":
    a = ["感谢点赞_01(总).wav", "感谢点赞_02.wav", "感谢点赞_03.wav"]
    pt_1 = CyclePlayerThread(a)
    pt_1.start()

    b = "感谢点赞_02.wav"
    pt_2 = OneTimePlayerThread(b)
    pt_2.start()
