from simpysql.DBModel import DBModel


class SenCookie(DBModel):
    __basepath__ = '../../'
    __tablename__ = 'sen_cookie'
    columns = [
        'cookie_id',
        'cookie_name',
        'cookie_keyword',
        'cookie_raw',
        'create_by',
        'create_time',
        'update_by',
        'update_time'
    ]
