from typing import Union
from fastapi import FastAPI
from sql_app.curd import DatabaseHandler

import os.path

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/search")
def query_item(q: Union[str, None] = None):
    if q is None:
        return {"q": "None"}
    # SQLite数据库文件路径
    SQLALCHEMY_DATABASE_URL = "sqlite:///{}".format(os.path.abspath(
        os.path.join(os.path.dirname(__file__), "./sql_app/dictionary.db")))
    # 创建DatabaseHandler实例
    db_handler = DatabaseHandler(SQLALCHEMY_DATABASE_URL)
    # 连接到数据库
    db_handler.connect()
    # 根据term_name进行查询
    term_name_result = db_handler.query_by_term_name(q)
    # 打印查询结果
    # print(term_name_result)
    # 不需要连接时调用关闭连接
    db_handler.disconnect()
    return {"res": str(term_name_result)}
