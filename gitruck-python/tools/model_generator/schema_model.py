from simpysql.DBModel import DBModel


class BaseModel(DBModel):
    __basepath__ = '../../'
    __database__ = 'base'
    __tablename__ = 'COLUMNS'
    columns = [
        'TABLE_NAME',
    ]
