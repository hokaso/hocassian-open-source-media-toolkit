import json
import os


# import sys

# sys.path.append(os.getcwd())


# from pymysql.converters import escape_string


# 普通序列化json文件
def serialize(obj):
    obj_temp = json.dumps(obj, ensure_ascii=False)

    # about why replace: https://github.com/PyMySQL/PyMySQL/issues/859
    # return escape_str(obj_temp).replace("\\", "")

    return obj_temp


# 将cookies字符串转为dict
def cookies_to_dict(cookies):
    if not cookies:
        return None

    cookie_dict = {}
    for i in cookies.split('; '):
        cookie_dict[i.split('=')[0]] = i.split('=')[1]
    return cookie_dict


# 适配自动化chrome浏览器的cookies格式，调用处可以这样使用：[self.driver.add_cookie(i) for i in cookie_list]
def cookies_suit_chrome(cookies):
    cookie_dict = cookies_to_dict(cookies)
    cookie_list = []
    for cookie_name, cookie_value in cookie_dict.items():
        cookie_list.append(
            {
                'name': cookie_name,
                'value': cookie_value
            }
        )
    return cookie_list


# 判断传入文件是否为图片
def is_match_pic_ext(filename):
    image_ext = ['.jpg', '.png', '.jpeg', '.bmp']
    if os.path.splitext(filename)[-1].lower() in image_ext:
        return True


# 判断传入文件是否为视频
def is_match_video_ext(filename):
    video_ext = [
        '.mp4', '.avi', '.mpg', '.mov',
        '.flv', ".mxf", ".mpeg", ".mkv",
        ".ogg", ".3gp", ".wmv", ".h264",
        ".m4v", ".webm"
    ]
    if os.path.splitext(filename)[-1].lower() in video_ext:
        return True


# 判断传入文件是否为音频
def is_match_audio_ext(filename):
    audio_ext = [
        '.wav', '.mp3', '.m4a', '.ape'
    ]
    if os.path.splitext(filename)[-1].lower() in audio_ext:
        return True


# 驼峰转下划线
def hump_to_underline(text):
    res = []
    for index, char in enumerate(text):
        if char.isupper() and index != 0:
            res.append("_")
        res.append(char)
    return ''.join(res).lower()


# 下划线转驼峰
def underline_hump(text):
    arr = text.lower().split('_')
    res = []
    for i in arr:
        res.append(i[0].upper() + i[1:])
    return ''.join(res)


# 获取工作区目录
def get_script_dir():
    return r"{0:}".format(os.getcwd())


def default_ext(i):
    return True


# 文件路径组合
def get_folder_files(folder_path, ext_func=default_ext):
    # return [folder_path + i for i in os.listdir(folder_path)]
    temp_list = []
    for i in os.listdir(folder_path):
        if ext_func(i):
            temp_list.append(folder_path + i)
    return temp_list


class Serializer(object):
    pass


class EmbedTransport(object):

    def __init__(self):

        from utils.regex import IsEnglishWord
        self.ie = IsEnglishWord()

        self.bold_alphabet = {
            'a': '𝗮', 'b': '𝗯', 'c': '𝗰', 'd': '𝗱', 'e': '𝗲', 'f': '𝗳', 'g': '𝗴', 'h': '𝗵', 'i': '𝗶',
            'j': '𝗷', 'k': '𝗸', 'l': '𝗹', 'm': '𝗺', 'n': '𝗻', 'o': '𝗼', 'p': '𝗽', 'q': '𝗾', 'r': '𝗿',
            's': '𝘀', 't': '𝘁', 'u': '𝘂', 'v': '𝘃', 'w': '𝘄', 'x': '𝘅', 'y': '𝘆', 'z': '𝘇', 'A': '𝗔',
            'B': '𝗕', 'C': '𝗖', 'D': '𝗗', 'E': '𝗘', 'F': '𝗙', 'G': '𝗚', 'H': '𝗛', 'I': '𝗜', 'J': '𝗝',
            'K': '𝗞', 'L': '𝗟', 'M': '𝗠', 'N': '𝗡', 'O': '𝗢', 'P': '𝗣', 'Q': '𝗤', 'R': '𝗥', 'S': '𝗦',
            'T': '𝗧', 'U': '𝗨', 'V': '𝗩', 'W': '𝗪', 'X': '𝗫', 'Y': '𝗬', 'Z': '𝗭'
        }
        self.italic_bold_alphabet = {
            'a': '𝙖', 'b': '𝙗', 'c': '𝙘', 'd': '𝙙', 'e': '𝙚', 'f': '𝙛', 'g': '𝙜', 'h': '𝙝',
            'i': '𝙞', 'j': '𝙟', 'k': '𝙠', 'l': '𝙡', 'm': '𝙢', 'n': '𝙣', 'o': '𝙤', 'p': '𝙥',
            'q': '𝙦', 'r': '𝙧', 's': '𝙨', 't': '𝙩', 'u': '𝙪', 'v': '𝙫', 'w': '𝙬', 'x': '𝙭',
            'y': '𝙮', 'z': '𝙯', 'A': '𝘼', 'B': '𝘽', 'C': '𝘾', 'D': '𝘿', 'E': '𝙀', 'F': '𝙁',
            'G': '𝙂', 'H': '𝙃', 'I': '𝙄', 'J': '𝙅', 'K': '𝙆', 'L': '𝙇', 'M': '𝙈', 'N': '𝙉',
            'O': '𝙊', 'P': '𝙋', 'Q': '𝙌', 'R': '𝙍', 'S': '𝙎', 'T': '𝙏', 'U': '𝙐', 'V': '𝙑',
            'W': '𝙒', 'X': '𝙓', 'Y': '𝙔', 'Z': '𝙕'
        }
        self.italic_alphabet = {
            'a': '𝘢', 'b': '𝘣', 'c': '𝘤', 'd': '𝘥', 'e': '𝘦', 'f': '𝘧', 'g': '𝘨', 'h': '𝘩',
            'i': '𝘪', 'j': '𝘫', 'k': '𝘬', 'l': '𝘭', 'm': '𝘮', 'n': '𝘯', 'o': '𝘰', 'p': '𝘱',
            'q': '𝘲', 'r': '𝘳', 's': '𝘴', 't': '𝘵', 'u': '𝘶', 'v': '𝘷', 'w': '𝘸', 'x': '𝘹',
            'y': '𝘺', 'z': '𝘻', 'A': '𝘈', 'B': '𝘉', 'C': '𝘊', 'D': '𝘋', 'E': '𝘌', 'F': '𝘍',
            'G': '𝘎', 'H': '𝘏', 'I': '𝘐', 'J': '𝘑', 'K': '𝘒', 'L': '𝘓', 'M': '𝘔', 'N': '𝘕',
            'O': '𝘖', 'P': '𝘗', 'Q': '𝘘', 'R': '𝘙', 'S': '𝘚', 'T': '𝘛', 'U': '𝘜', 'V': '𝘝',
            'W': '𝘞', 'X': '𝘟', 'Y': '𝘠', 'Z': '𝘡'
        }

    def bold(self, text):
        parsed_text = ""

        for char in text:

            if self.ie.judgement(char):
                parsed_text += self.bold_alphabet[char]
            else:
                parsed_text += char

        return parsed_text

    def italic(self, text):
        parsed_text = ""

        for char in text:

            if self.ie.judgement(char):
                parsed_text += self.italic_alphabet[char]
            else:
                parsed_text += char

        return parsed_text

    def bold_italic(self, text):
        parsed_text = ""

        for char in text:

            if self.ie.judgement(char):
                parsed_text += self.italic_bold_alphabet[char]
            else:
                parsed_text += char

        return parsed_text


class JsonCombinator(object):

    """
    # 使用例：
    # from utils.serializer import JsonCombinator
    #
    #
    # def default_info(data):
    #     return data["data"]["records"]
    #
    #
    # js = JsonCombinator(
    #     input_path="data",
    #     output_path="output.json",
    #     info_floor=default_info,
    # )
    # js.run()
    """

    @staticmethod
    def default_info(info):
        return info["data"]

    def __init__(
            self,
            input_path="input",
            output_path="output.json",
            info_floor=default_info,
    ):

        self.path_input = input_path
        self.path_output = output_path
        self.info_floor = info_floor

    def run(self):

        all_info = []

        for root, dirs, files in os.walk(self.path_input):
            # 遍历所有文件
            for file in files:
                if os.path.splitext(file)[-1] == '.json':

                    with open(root + "/" + file, 'r', encoding='utf-8', errors='ignore') as f0:
                        info = json.load(f0)

                    for ikey in self.info_floor(info):
                        all_info.append(ikey)

        with open(self.path_output, 'w', encoding='utf-8') as fp:
            json.dump(all_info, fp, ensure_ascii=False)


if __name__ == "__main__":
    a = ["1", "2", "3"]
    serialize(a)
