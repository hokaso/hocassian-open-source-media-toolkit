import json
import os


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
    if os.path.splitext(filename)[-1] in image_ext:
        return True


# 判断传入文件是否为视频
def is_match_video_ext(filename):
    image_ext = ['.mp4', '.avi', '.mpg', '.mov']
    if os.path.splitext(filename)[-1] in image_ext:
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


class Serializer(object):
    pass


if __name__ == "__main__":
    a = ["1", "2", "3"]
    serialize(a)
