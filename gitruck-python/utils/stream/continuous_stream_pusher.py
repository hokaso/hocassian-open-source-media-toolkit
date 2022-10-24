import ffmpeg
import os
import time
import random
import multiprocessing
from utils.serializer import is_match_video_ext
from utils.vision_algorithm.obtain_media_meta import video_meta_info
from utils.vision_algorithm.time_convert import sec2ts


class StreamServer(object):

    def __init__(self, clip_pool_path, server_url):
        self.clip_pool_path = clip_pool_path
        self.server_url = server_url

        self.limited_dur = 30

    def pusher(self):

        ffmpeg.input(
            self.clip_pool_path + 'list1.txt',
            safe=0,
            f='concat',
            re=None
        ).output(
            self.server_url,
            codec="copy",
            f='flv'
        ).run()

    def pusher_sp(self, filename):

        _, _, origin_duration, _ = video_meta_info(filename)

        if self.limited_dur - origin_duration >= 1:
            _ss = round(origin_duration)
        else:
            _ss = random.randint(0, round(origin_duration - self.limited_dur))

        ffmpeg.input(
            filename,
            ss=str(_ss),
            re=None
        ).output(
            self.server_url,
            codec="copy",
            f='flv'
        ).run()


class ContinuousStreamPusher(object):

    def __init__(self, clip_pool_path):
        self.clip_pool_path = clip_pool_path
        # self.clip_list = [self.clip_pool_path + "/" + i for i in os.listdir(self.clip_pool_path)]

        self.clip_list = [i for i in os.listdir(self.clip_pool_path) if is_match_video_ext(i)]
        self.clip_reading_times = 0
        self.clip_list_length = len(self.clip_list)

        # 直播画面持续时间基准值
        self.scene_dur = 120

        # 直播画面持续时间±值
        self.scene_pm = 30

    def get_clip(self):
        # 顺序播放
        clip_reading_index = self.clip_reading_times % self.clip_list_length
        self.clip_reading_times += 1

        # 乱序播放
        # clip_reading_index = random.randint(0, self.clip_list_length)

        _, _, origin_duration, _ = video_meta_info(self.clip_pool_path + self.clip_list[clip_reading_index])

        return self.clip_list[clip_reading_index], origin_duration

    def random_dur(self, origin_duration):

        # 确定偏移量
        cur_pm = random.randint(0, self.scene_pm)

        # 如果素材长度甚至短于预设间隔+偏移量，那就直接返回原始长度就行
        if self.scene_dur + cur_pm - origin_duration >= 1:
            return "00:00.00", sec2ts(origin_duration), round(origin_duration)

        # 确定开始点
        start_sec = random.randint(0, round(origin_duration - self.scene_dur))
        start_ts = sec2ts(start_sec)

        # 确定结束点
        end_sec = start_sec + self.scene_dur + cur_pm
        end_ts = sec2ts(end_sec)

        return start_ts, end_ts, self.scene_dur + cur_pm

    def change_list_1(self):
        filepath, duration = self.get_clip()
        start_ts, end_ts, cur_dur = self.random_dur(duration)

        with open("utils/stream/list1_model.txt", 'r') as f0:
            list1_model = f0.read()

        with open(self.clip_pool_path + "list1.txt", 'w') as f0:
            f0.write(
                list1_model.
                replace("{filename1}", "\'" + filepath + "\'").
                replace("{ts1}", start_ts).
                replace("{ts2}", end_ts)
            )

        return cur_dur

    def change_list_2(self):
        filepath, duration = self.get_clip()
        start_ts, end_ts, cur_dur = self.random_dur(duration)

        with open("utils/stream/list2_model.txt", 'r') as f0:
            list1_model = f0.read()

        with open(self.clip_pool_path + "list2.txt", 'w') as f0:
            f0.write(
                list1_model.
                replace("{filename2}", "\'" + filepath + "\'").
                replace("{ts1}", start_ts).
                replace("{ts2}", end_ts)
            )

        return cur_dur

    def start(self):
        d_1 = self.change_list_1()
        d_2 = self.change_list_2()

        wait_time = d_1 + d_2 - 2
        self.cycle(wait_time)

    def cycle(self, wait_time):
        time.sleep(wait_time)
        while True:
            time.sleep(1)
            d_1 = self.change_list_1()
            time.sleep(d_1 - 1)
            d_2 = self.change_list_2()
            time.sleep(d_2)


if __name__ == "__main__":
    clip_pool_path = ""
    server_url = "rtmp://127.0.0.1:1935/live/dy"

    ss = StreamServer(clip_pool_path, server_url)
    csp = ContinuousStreamPusher(clip_pool_path)

    p2 = multiprocessing.Process(target=csp.start)
    p2.start()

    time.sleep(1)

    p1 = multiprocessing.Process(target=ss.pusher)
    p1.daemon = True
    p1.start()
