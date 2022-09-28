import re


def remove_duplicate(enter_list):
    return list(set(enter_list))


def check_phone_num(enter):
    raw_regex = r'((|\+)(([0-9\(\)\-\s]){6,}))'
    regex = re.compile(raw_regex)
    _phone_nums = re.findall(regex, str(enter))

    phone_nums = []
    if _phone_nums:
        for _phone_num in _phone_nums:
            # 应该没有什么电话号码+区号会超过15个字符了……
            if len(_phone_num[0]) <= 15:
                phone_nums.append(_phone_num[0])

    return remove_duplicate(phone_nums)


def remove_round_bracket(enter):
    regex = u"\\(.*?\\)"
    return re.sub(regex, "", str(enter))


def remove_angle_bracket(enter):
    regex = u"\\<.*?\\>"
    return re.sub(regex, "", str(enter))


def check_email(enter):
    raw_regex = r'(([\w-]+)@[\w-]+\.([\w-]){1,})'
    regex = re.compile(raw_regex)
    _emails = re.findall(regex, str(enter))
    emails = []
    if _emails:
        for _email in _emails:
            if len(_email) < 30:
                emails.append(_email[0])

    return remove_duplicate(emails)


def check_url(enter):
    raw_regex = r'((http)(\w|[:/.;/=&#?:%\-,\\.?#\*])*)|(www[.]\w+[.][a-z]+)'
    regex = re.compile(raw_regex)
    _urls = re.findall(regex, str(enter))
    urls = []
    if _urls:
        for _url in _urls:
            urls.append(_url[0])

    return remove_duplicate(urls)


def extract_url_infix(enter):
    enter_str = str(enter)
    raw_regex = r'(((?<=(^https:\/\/)).*?(?=[/])|((?<=(^http:\/\/))).*?(?=[/])|((?<=(^www))).*?(?=[/])))'
    regex = re.compile(raw_regex)
    url_index = re.search(regex, enter_str)

    if not url_index:
        cur_url_index = enter_str
    else:
        cur_url_index = url_index.group()

    url_index_list = cur_url_index.split(".")
    url_infix = ""
    url_index_list_len = len(url_index_list)
    if url_index_list_len > 2:
        url_infix = url_index_list[1]
        return url_infix
    elif url_index_list_len == 2 or url_index_list_len == 1:
        url_infix = url_index_list[0]
        return url_infix
    else:
        return url_infix


def is_anchor(enter):
    raw_regex = r'^#'
    regex = re.compile(raw_regex)
    return re.search(regex, str(enter))


def is_uri(enter):
    raw_regex = r'(^\/)'
    regex = re.compile(raw_regex)
    rsg = re.search(regex, str(enter))
    if not rsg:
        return None

    return rsg.group()


def extract_chinese_words(enter):

    new_str = ""
    for i in str(enter):
        if (i >= u'\u4e00') and (i <= u'\u9fa5'):
            new_str += i
    return new_str


def extract_common_words(enter):

    regex = u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])"
    return re.sub(regex, "", str(enter))


class Regex(object):

    def __init__(self):
        pass


if __name__ == "__main__":
    # r = Regex()
    test = "ertyhrthtr"
    a = is_uri(test)
    print(a)
