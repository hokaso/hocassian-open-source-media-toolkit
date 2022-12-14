import os
import shutil

from scenedetect.video_manager import VideoManager
from utils.vision_algorithm.dynamic_interval import find_scenes, clip_render
from utils.serializer import is_match_video_ext, get_folder_files
from utils.id_generator import timestamp_gen
from concurrent.futures import ThreadPoolExecutor


class SelectionSegment(object):

    def __init__(self):
        path = input(r"请输入需要处理的视频文件夹（例如「M:\data\互动派\正佳极地公园\手机」）：")

        self.raw_clip_folder = path + r"/"
        self.clip_list = get_folder_files(self.raw_clip_folder, is_match_video_ext)

        # 新建文件夹
        self.fin_clip_path = self.raw_clip_folder + "selection/"
        if not os.path.exists(self.fin_clip_path):
            os.makedirs(self.fin_clip_path)

        self.threshold_default = 20
        self.crf_default = "20"
        self.acceptable_shortest_interval = 5

        # 线程池相关
        self.pool = ThreadPoolExecutor(max_workers=2)

    def render(self, key):
        print(key)

        video = VideoManager([key])
        scenes = find_scenes(video, self.threshold_default)

        if not scenes:
            shutil.copy(key, self.fin_clip_path + str(timestamp_gen()) + os.path.splitext(key)[-1])
            return

        new_scenes = []

        for ikey in scenes:
            dur = ikey[1].get_seconds() - ikey[0].get_seconds()
            if dur >= self.acceptable_shortest_interval:
                new_scenes.append(ikey)

        clip_render(key, new_scenes, self.crf_default, self.fin_clip_path)

    def run(self):
        for key in self.clip_list:
            self.pool.submit(self.render, key)


if __name__ == "__main__":
    ss = SelectionSegment()
    ss.run()
