import json, os


# from pymysql.converters import escape_string


def serialize(obj):
    obj_temp = json.dumps(obj, ensure_ascii=False)

    # about why replace: https://github.com/PyMySQL/PyMySQL/issues/859
    # return escape_str(obj_temp).replace("\\", "")

    return obj_temp


def cookies_to_dict(cookies):
    if not cookies:
        return None

    cookie_dict = {}
    for i in cookies.split('; '):
        cookie_dict[i.split('=')[0]] = i.split('=')[1]
    return cookie_dict


# [self.driver.add_cookie(i) for i in cookie_list]
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


def is_match_pic_ext(filename):
    image_ext = ['.jpg', '.png', '.jpeg', '.bmp']
    if os.path.splitext(filename)[-1] in image_ext:
        return True


def is_match_video_ext(filename):
    image_ext = ['.mp4', '.avi', '.mpg', '.mov']
    if os.path.splitext(filename)[-1] in image_ext:
        return True


class Serializer(object):
    pass


if __name__ == "__main__":
    a = ["1", "2", "3"]
    serialize(a)
