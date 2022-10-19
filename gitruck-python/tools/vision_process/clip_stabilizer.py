import os

from vidgear.gears.stabilizer import Stabilizer
from vidgear.gears import CamGear
from vidgear.gears import WriteGear
from utils.serializer import is_match_video_ext
from utils.vision_algorithm.obtain_media_meta import video_meta, video_rate_info, video_is_ten_bit, video_is_bt2020


class ClipStabilizer(object):

    def __init__(self):
        self.unstable_clip_folder = r"C:/Users/Administrator/Desktop/test/"
        self.clip_list = [self.unstable_clip_folder + i for i in os.listdir(self.unstable_clip_folder) if is_match_video_ext(i)]

        # 新建文件夹
        self.stable_clip_path = self.unstable_clip_folder + "stable/"
        if not os.path.exists(self.stable_clip_path):
            os.makedirs(self.stable_clip_path)

    def run(self):

        for ikey in self.clip_list:

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
                "-preset": "medium",
                "-clones": []
            }

            # 获取文件meta_info
            origin_info = video_meta(ikey)
            clip_rate = video_rate_info(origin_info)

            # 确定帧率
            output_params["-input_framerate"] = clip_rate
            output_params["-r"] = clip_rate

            # 预设渲染质量
            output_params["-crf"] = 18

            # 确定色彩深度
            if video_is_ten_bit(origin_info):

                output_params["-clones"].append("-pix_fmt")
                output_params["-clones"].append("yuv422p10le")

                output_params["-crf"] = 0

            # 确定色彩范围
            if video_is_bt2020(origin_info):

                # color-primaries 输入内容的色彩格式：bt709, unspecified, bt601, bt470m, bt470bg, smpte240, film, bt2020, xyz, smpte431, smpte432, ebu3213
                # transfer-characteristics 输入内容的传输特性（CICP）:unspecified, bt709, bt470m, bt470bg, bt601, smpte240, lin, log100, log100sq10, iec61966, bt1361, srgb, bt2020-10bit, bt2020-12bit, smpte2084, hlg, smpte428
                # matrix-coefficients 输入内容的矩阵系数:identity, bt709, unspecified, fcc73, bt470bg, bt601, smpte240, ycgco, bt2020ncl, bt2020cl, smpte2085, chromncl, chromcl, ictcp

                output_params["-clones"].append("-color_primaries")
                output_params["-clones"].append("bt2020")

                output_params["-clones"].append("-bsf:v")
                output_params["-clones"].append("h264_metadata=colour_primaries=9:transfer_characteristics=18:matrix_coefficients=9")

                output_params["-crf"] = 0

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


if __name__ == "__main__":
    cs = ClipStabilizer()
    cs.run()
