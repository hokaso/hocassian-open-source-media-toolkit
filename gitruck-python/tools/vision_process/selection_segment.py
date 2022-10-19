import os

from scenedetect.video_manager import VideoManager
from utils.vision_algorithm.dynamic_interval import find_scenes, clip_render
from utils.serializer import is_match_video_ext


class SelectionSegment(object):

    def __init__(self):
        self.raw_clip_folder = r"F:/影视/2022下/20221009/test/"
        self.clip_list = [self.raw_clip_folder + i for i in os.listdir(self.raw_clip_folder) if is_match_video_ext(i)]

        # 新建文件夹
        self.fin_clip_path = self.raw_clip_folder + "selection/"
        if not os.path.exists(self.fin_clip_path):
            os.makedirs(self.fin_clip_path)

        self.threshold_default = 12.5
        self.crf_default = 20
        self.acceptable_shortest_interval = 5

    def run(self):

        for key in self.clip_list:

            video = VideoManager([key])
            scenes = find_scenes(video, self.threshold_default)

            new_scenes = []

            for ikey in scenes:
                dur = ikey[1].get_seconds() - ikey[0].get_seconds()
                if dur >= self.acceptable_shortest_interval:
                    new_scenes.append(ikey)

            clip_render(key, new_scenes, self.crf_default, self.fin_clip_path)


if __name__ == "__main__":
    ss = SelectionSegment()
    ss.run()
