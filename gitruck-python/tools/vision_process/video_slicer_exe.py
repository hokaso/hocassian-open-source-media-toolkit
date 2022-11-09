import os
import shutil

from scenedetect.video_manager import VideoManager
from utils.vision_algorithm.dynamic_interval import find_scenes, clip_render
from utils.serializer import is_match_video_ext, get_folder_files
from utils.id_generator import timestamp_gen
from concurrent.futures import ThreadPoolExecutor


class SelectionSegment(object):

    def __init__(self):
        self.threshold_default = 27.5
        self.crf_default = "20"
        self.worker_default = 2

        path = input(r"请输入需要处理的视频文件夹（例如「M:\data\待处理\海洋公园\手机」）：")
        crf = input(r"请输入crf值（选择区间[1, 51]，如无输入则默认20）：")
        threshold = input(r"请输入画面阈值（选择区间[10, 90]，如无输入则默认27.5）：")
        max_workers = input(r"请输入并行工作的线程数（选择区间[1, 4]，如无输入则默认2）：")

        if crf:
            self.crf_default = crf

        if threshold:
            self.threshold_default = float(threshold)

        if max_workers:
            self.worker_default = int(max_workers)

        self.raw_clip_folder = path + r"/"
        # self.clip_list = [self.raw_clip_folder + i for i in os.listdir(self.raw_clip_folder) if is_match_video_ext(i)]
        self.clip_list = get_folder_files(self.raw_clip_folder, is_match_video_ext)

        # 新建文件夹
        self.fin_clip_path = self.raw_clip_folder + "selection/"
        if not os.path.exists(self.fin_clip_path):
            os.makedirs(self.fin_clip_path)

        # 线程池相关
        self.pool = ThreadPoolExecutor(max_workers=self.worker_default)

    def render(self, key):

        video = VideoManager([key])
        scenes = find_scenes(video, self.threshold_default)

        if not scenes:
            shutil.copy(key, self.fin_clip_path + str(timestamp_gen()) + os.path.splitext(key)[-1])
            return

        clip_render(key, scenes, self.crf_default, self.fin_clip_path)

    def run(self):
        for key in self.clip_list:
            self.pool.submit(self.render, key)


if __name__ == "__main__":
    ss = SelectionSegment()
    ss.run()
