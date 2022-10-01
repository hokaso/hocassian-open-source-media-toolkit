# import cv2
import ffmpeg
import os
import copy

from PIL import Image, ImageFilter

from utils.serializer import is_match_video_ext, is_match_pic_ext
from utils.vision_algorithm.obtain_media_meta import video_meta_info, image_meta_info
from utils.vision_algorithm.suitable_layout import fill, adapt, adapt_extra
from utils.id_generator import timestamp_gen

"""
@Author: Hocassian
@Date: 2022-09-15
@Update: 2022-09-29
@Info: 能用就行，不要试图搞懂该算法的原理；虽然写的是横转竖，但实际上竖转横也可以用
"""


class Horizontal2Vertical(object):

    def __init__(self):

        # 0正常处理 1四比三 2一比一
        self.video_frame_type = 0
        self.image_frame_type = 0

        # 竖转横
        # self.standard_1k_w = 1920
        # self.standard_1k_h = 1080

        # 横转竖
        self.standard_1k_w = 1080
        self.standard_1k_h = 1920

        self.source_path = "temp_input/"  # 视频来源路径
        self.save_path = "temp_output/"  # 视频修改后的保存路径

        self.cur_video_name = ""
        self.cur_image_name = ""

    def cal_param(
            self,
            origin_width,
            origin_height,
    ):

        # 计算前景和背景尺寸
        tw1, th1, cw1, ch1, cw2, ch2 = fill(origin_width, origin_height, self.standard_1k_w, self.standard_1k_h)
        tw2, th2, lw, lh = adapt(origin_width, origin_height, self.standard_1k_w, self.standard_1k_h)

        # 去除一些不必要的处理
        if all([
            origin_width == tw1,
            origin_height == th1,
        ]):
            raise

        return tw1, th1, cw1, ch1, cw2, ch2, tw2, th2, lw, lh

    def process_image(self, file):

        # 采集原始素材信息
        origin_width, origin_height, _, img = image_meta_info(self.source_path + file)

        self.cur_image_name = file

        try:
            tw1, th1, cw1, ch1, cw2, ch2, tw2, th2, lw, lh = self.cal_param(origin_width, origin_height)
        except Exception as e:
            print(e)
            return

        self._image_synthesize(
            origin_width,
            origin_height,
            img,
            tw1,
            th1,
            cw1,
            ch1,
            tw2,
            th2,
            lw,
            lh,
        )

    def _image_synthesize(
            self,
            origin_width,
            origin_height,
            img,
            tw1,
            th1,
            cw1,
            ch1,
            tw2,
            th2,
            lw,
            lh,
    ):

        # 如果image_frame_type有变动，就调整一下再传回来
        if self.image_frame_type != 0:
            tw2, th2, lw, lh, cx, cy, fw, fh = adapt_extra(
                origin_width,
                origin_height,
                self.standard_1k_w,
                self.standard_1k_h,
                self.image_frame_type,
            )

            self.sp_image_synthesize(
                copy.deepcopy(img),
                tw1,
                th1,
                cw1,
                ch1,
                fw,
                fh,
                cx,
                cy,
                tw2,
                th2,
                lw,
                lh,
            )

        else:
            self.image_synthesize(
                copy.deepcopy(img),
                tw1,
                th1,
                cw1,
                ch1,
                tw2,
                th2,
                lw,
                lh,
            )

    def sp_image_synthesize(
            self,
            img,
            tw1,
            th1,
            cw1,
            ch1,
            fw,
            fh,
            cx,
            cy,
            tw2,
            th2,
            lw,
            lh,
    ):

        back_img = self.image_synthesize_bg(
            copy.deepcopy(img),
            tw1,
            th1,
            cw1,
            ch1,
        )

        # 把原图处理成前景图——裁剪，仅此处有差异
        front_img = img.crop(
            (
                cx,
                cy,
                cx + fw,
                cy + fh
            )
        )

        self.image_synthesize_fin(
            back_img,
            front_img,
            tw2,
            th2,
            lw,
            lh,
        )

    def image_synthesize(
            self,
            img,
            tw1,
            th1,
            cw1,
            ch1,
            tw2,
            th2,
            lw,
            lh,
    ):

        back_img = self.image_synthesize_bg(
            copy.deepcopy(img),
            tw1,
            th1,
            cw1,
            ch1,
        )

        self.image_synthesize_fin(
            back_img,
            copy.deepcopy(img),
            tw2,
            th2,
            lw,
            lh,
        )

    def image_synthesize_bg(
            self,
            img,
            tw1,
            th1,
            cw1,
            ch1,
    ):

        # 把原图放大为背景图
        _back_img_tmp = img.resize((tw1, th1), Image.Resampling.LANCZOS)

        # 裁切背景图
        back_img_tmp = _back_img_tmp.crop(
            (
                cw1,
                ch1,
                cw1 + self.standard_1k_w,
                ch1 + self.standard_1k_h
            )
        )

        # 模糊背景图
        back_img = back_img_tmp.filter(ImageFilter.GaussianBlur(radius=18))
        return back_img

    def image_synthesize_fin(
            self,
            back_img,
            front_img,
            tw2,
            th2,
            lw,
            lh,
    ):

        # 把原图处理成前景图——缩放
        front_img_tmp = front_img.resize((tw2, th2), Image.Resampling.LANCZOS)

        # 拼合
        back_img.paste(front_img_tmp, (lw, lh, lw + tw2, lh + th2))

        # 这两步是用来转换的
        bg = Image.new("RGB", back_img.size, (255, 255, 255))
        bg.paste(back_img)
        bg.save(os.path.join(self.save_path, self.cur_image_name), quality=100)
        # bg.save(os.path.join(self.save_path, str(timestamp_gen()) + '.jpg'), quality=100)

    def process_video(self, file):

        # 采集原始素材信息
        origin_info, after_rate, origin_width, origin_height = video_meta_info(self.source_path + file)

        try:
            tw1, th1, cw1, ch1, cw2, ch2, tw2, th2, lw, lh = self.cal_param(origin_width, origin_height)
        except Exception as e:
            print(e)
            return

        self._video_synthesize(
            origin_width,
            origin_height,
            file,
            tw1,
            th1,
            cw1,
            ch1,
            tw2,
            th2,
            lw,
            lh,
        )

    def _video_synthesize(
            self,
            origin_width,
            origin_height,
            file,
            tw1,
            th1,
            cw1,
            ch1,
            tw2,
            th2,
            lw,
            lh,
    ):

        # 如果frame_type有变动，就调整一下再传回来
        if self.video_frame_type != 0:
            tw2, th2, lw, lh, cx, cy, fw, fh = adapt_extra(
                origin_width,
                origin_height,
                self.standard_1k_w,
                self.standard_1k_h,
                self.video_frame_type,
            )

            self.sp_video_synthesize(
                file,
                tw1,
                th1,
                cw1,
                ch1,
                fw,
                fh,
                cx,
                cy,
                tw2,
                th2,
                lw,
                lh,
            )

        else:
            self.video_synthesize(
                file,
                tw1,
                th1,
                cw1,
                ch1,
                tw2,
                th2,
                lw,
                lh,
            )

    def sp_video_synthesize(
            self,
            file,
            tw1,
            th1,
            cw1,
            ch1,
            fw,
            fh,
            cx,
            cy,
            tw2,
            th2,
            lw,
            lh,
    ):

        cur_file = ffmpeg.input(self.source_path + file)
        fv1 = self.video_synthesize_fv1(
            cur_file,
            tw1,
            th1,
            cw1,
            ch1
        )
        fa = cur_file.audio

        # 仅此处有差异
        fv2 = cur_file.video.filter(
            "crop",
            fw,
            fh,
            cx,
            cy,
        ).filter("scale", tw2, th2)

        self.video_synthesize_fin(
            fv1,
            fv2,
            fa,
            lw,
            lh,
        )

    def video_synthesize(
            self,
            file,
            tw1,
            th1,
            cw1,
            ch1,
            tw2,
            th2,
            lw,
            lh,
    ):

        cur_file = ffmpeg.input(self.source_path + file)
        fv1 = self.video_synthesize_fv1(
            cur_file,
            tw1,
            th1,
            cw1,
            ch1
        )
        fa = cur_file.audio

        # 仅此处有差异
        fv2 = cur_file.video.filter("scale", tw2, th2)

        self.video_synthesize_fin(
            fv1,
            fv2,
            fa,
            lw,
            lh,
        )

    def video_synthesize_fv1(
            self,
            cur_file,
            tw1,
            th1,
            cw1,
            ch1
    ):

        fv1 = cur_file.video.filter("scale", tw1, th1).filter(
            "crop",
            self.standard_1k_w,
            self.standard_1k_h,
            cw1,
            ch1,
        ).filter("gblur", sigma=20)

        return fv1

    def video_synthesize_fin(
            self,
            fv1,
            fv2,
            fa,
            lw,
            lh,
    ):

        fv3 = ffmpeg.filter([fv1, fv2], 'overlay', lw, lh)
        out = ffmpeg.output(fv3, fa, self.save_path + str(timestamp_gen()) + ".mp4")
        out.run()

    def run(self):
        for file in os.listdir(self.source_path):

            # 根据实际情况决定要转什么
            if is_match_video_ext(file):
                self.process_video(file)
            # elif is_match_pic_ext(file):
            #     self.process_image(file)

            # if is_match_pic_ext(file):
            #     self.process_image(file)


if __name__ == "__main__":
    hv = Horizontal2Vertical()
    hv.run()
