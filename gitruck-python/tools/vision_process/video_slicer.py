import os

from scenedetect.video_manager import VideoManager
from utils.vision_algorithm.dynamic_interval import find_scenes, clip_render
from utils.serializer import is_match_video_ext


class VideoSlicer(object):

    def __init__(self):
        self.input_dir = 'temp_input/'
        self.output_dir = 'temp_output/'

        self.input_clip_list = [self.input_dir + i for i in os.listdir(self.input_dir) if is_match_video_ext(i)]

        self.threshold_default = 27.5
        self.crf_default = "20"

    def run(self):
        for key in self.input_clip_list:

            video = VideoManager([key])
            scenes = find_scenes(video, self.threshold_default)
            clip_render(key, scenes, self.crf_default, self.output_dir)


if __name__ == '__main__':
    VideoSlicer().run()
