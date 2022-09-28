from utils.serializer import hump_to_underline, underline_hump
from schema_model import BaseModel


class Run(object):

    def __init__(self):

        # 此处请填入驼峰命名
        self.model_name = "sen_cookie"

        # self.

        with open("model_model.txt", 'r') as f0:
            self.model_model = f0.read()

    def run(self):

        column_name_map = BaseModel.execute("select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s'" % self.model_name).get()
        print(column_name_map)

        model_underline_column_list = ["\'" + i["COLUMN_NAME"] + "\'" for i in column_name_map]
        model_underline_column = ',\n        '.join(model_underline_column_list)

        model_hump_name = underline_hump(self.model_name)

        _sm = self.model_model
        sm = _sm.replace("{model_hump_name}", model_hump_name).replace("{model_underline_name}", self.model_name).replace("{model_underline_column}", model_underline_column)

        with open(self.model_name + "_model.py", 'w') as f0:
            f0.write(sm)

        print(sm)
        pass


if __name__ == "__main__":
    r = Run()
    r.run()
