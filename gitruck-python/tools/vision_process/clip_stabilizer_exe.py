import os

from vidgear.gears.stabilizer import Stabilizer
from vidgear.gears import CamGear
from vidgear.gears import WriteGear
from utils.serializer import is_match_video_ext
from utils.vision_algorithm.obtain_media_meta import video_meta, video_rate_info, video_is_ten_bit, video_is_bt2020, video_origin_rate_info
from concurrent.futures import ThreadPoolExecutor

'''
    color-primaries 输入内容的色彩格式
                  
    0 - reserved,
    1 - ITU-R BT.709,
    2 - unspecified,
    3 - reserved,
    4 - ITU-R BT.470M,
    5 - ITU-R BT.470BG - BT.601 625,
    6 - ITU-R BT.601 525 - SMPTE 170M,
    7 - SMPTE 240M,
    8 - FILM,
    9 - ITU-R BT.2020,
    10 - SMPTE ST 428-1,
    11 - SMPTE RP 432-2,
    12 - SMPTE EG 432-2,
    22 - EBU Tech. 3213-E - JEDEC P22 phosphors
    
    transfer-characteristics 输入内容的传输特性（CICP）
    
    0 - reserved,
    1 - ITU-R BT.709,
    2 - unspecified,
    3 - reserved,
    4 - Gamma 2.2 curve - BT.470M,
    5 - Gamma 2.8 curve - BT.470BG,
    6 - SMPTE 170M,
    7 - SMPTE 240M,
    8 - Linear,
    9 - Log,
    10 - Log Sqrt,
    11 - IEC 61966-2-4,
    12 - ITU-R BT.1361 Extended Colour Gamut,
    13 - IEC 61966-2-1,
    14 - ITU-R BT.2020 10 bit,
    15 - ITU-R BT.2020 12 bit,
    16 - ITU-R BT.2100 Perceptual Quantization (ST-2084),
    17 - SMPTE ST 428-1,
    18 - ARIB STD-B67 (HLG)
    
    matrix-coefficients 输入内容的矩阵系数
    
    0 - Identity,
    1 - ITU-R BT.709,
    2 - unspecified,
    3 - reserved,
    4 - US FCC 73.682,
    5 - ITU-R BT.470BG,
    6 - SMPTE 170M,
    7 - SMPTE 240M,
    8 - YCoCg,
    9 - BT2020 Non-constant Luminance,
    10 - BT2020 Constant Luminance,
    11 - SMPTE ST 2085,
    12 - Chroma-derived Non-constant Luminance,
    13 - Chroma-derived Constant Luminance,
    14 - ITU-R BT.2100-0
    
'''


class ClipStabilizer(object):

    def __init__(self):
        path = input(r"请输入需要处理的视频文件夹（例如「M:\data\互动派\正佳极地公园\手机」）：")
        self.unstable_clip_folder = path + r"/"
        self.clip_list = [self.unstable_clip_folder + i for i in os.listdir(self.unstable_clip_folder) if is_match_video_ext(i)]

        # 新建文件夹
        self.stable_clip_path = self.unstable_clip_folder + "stable/"
        if not os.path.exists(self.stable_clip_path):
            os.makedirs(self.stable_clip_path)

        # self.clip_model = True
        self.clip_model = False

        self.pool = ThreadPoolExecutor(2)

    def render(self, ikey):

        # border_type: 'black', 'reflect', 'reflect_101', 'replicate' and 'wrap'
        # initiate stabilizer object with defined parameters
        stab = Stabilizer(
            smoothing_radius=35,
            crop_n_zoom=True,
            border_size=0,
            border_type="wrap",
            logging=True,
        )

        stream = CamGear(source=ikey).start()

        output_params = {
            "-preset": "fast",
            "-clones": []
        }

        # 获取文件meta_info
        origin_info = video_meta(ikey)

        # 确定帧率
        output_params["-input_framerate"] = video_rate_info(origin_info)
        # output_params["-input_framerate"] = video_origin_rate_info(origin_info)
        # output_params["-r"] = video_rate_info(origin_info)

        # 预设渲染质量
        output_params["-crf"] = 20

        # 确定色彩深度
        if video_is_ten_bit(origin_info):
            output_params["-clones"].append("-pix_fmt")
            output_params["-clones"].append("yuv422p10le")

            output_params["-crf"] = 0

        # 确定色彩范围
        if video_is_bt2020(origin_info) and self.clip_model:

            output_params["-clones"].append("-color_primaries")
            output_params["-clones"].append("bt2020")

            output_params["-clones"].append("-bsf:v")
            output_params["-clones"].append(
                "h264_metadata=colour_primaries=9:transfer_characteristics=18:matrix_coefficients=9")

            output_params["-crf"] = 0
            output_params["-preset"] = "medium"

        else:
            output_params["-clones"].append("-bsf:v")
            output_params["-clones"].append(
                "h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1")
            output_params["-preset"] = "ultrafast"

        # 开始渲染
        _, clip_name = os.path.split(ikey)

        writer = WriteGear(
            output_filename=self.stable_clip_path + clip_name,
            logging=True,
            **output_params,
        )

        while True:

            frame = stream.read()
            if frame is None:
                break

            stabilized_frame = stab.stabilize(frame)
            if stabilized_frame is None:
                continue

            writer.write(stabilized_frame)

        stream.stop()
        writer.close()
        stab.clean()

    def run(self):
        for ikey in self.clip_list:
            self.pool.submit(self.render, ikey)


if __name__ == "__main__":
    cs = ClipStabilizer()
    cs.run()
