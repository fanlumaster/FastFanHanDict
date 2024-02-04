from sqlalchemy import create_engine, select, MetaData, Table, Connection
import os.path


class DatabaseHandler:
    def __init__(self, database_url):
        # 创建数据库引擎
        self.engine = create_engine(database_url)
        # 创建元数据对象，用于存储数据库结构信息
        self.metadata = MetaData()
        # 连接对象，用于连接数据库
        self.connection: Connection
        # 数据库表对象，用于执行查询操作
        self.taiwan_chinese_dict: Table

    def connect(self):
        # 连接到数据库
        self.connection = self.engine.connect()
        # 通过autoload_with参数加载数据库表的结构信息
        self.taiwan_chinese_dict = Table(
            'taiwan_chinese_dict', self.metadata, autoload_with=self.engine)

    def disconnect(self):
        # 关闭数据库连接
        if self.connection:
            self.connection.close()

    def query_by_term_name(self, term_name):
        if not self.connection:
            # 如果连接未建立，抛出运行时错误
            raise RuntimeError(
                "Connection not established. Call connect() first.")
        # 构建查询对象
        query = select(
            self.taiwan_chinese_dict.columns.id,
            self.taiwan_chinese_dict.columns.term_name,
            self.taiwan_chinese_dict.columns.term_alias,
            self.taiwan_chinese_dict.columns.char_nums,
            self.taiwan_chinese_dict.columns.char_no,
            self.taiwan_chinese_dict.columns.radical_char,
            self.taiwan_chinese_dict.columns.stroke_nums,
            self.taiwan_chinese_dict.columns.stroke_nums_except_radical_char,
            self.taiwan_chinese_dict.columns.polyphonic_sorting,
            self.taiwan_chinese_dict.columns.zhuyin_yishi,
            self.taiwan_chinese_dict.columns.variant_type,
            self.taiwan_chinese_dict.columns.variant_zhuyin,
            self.taiwan_chinese_dict.columns.hanyu_pinyin,
            self.taiwan_chinese_dict.columns.variant_hanyu_pinyn,
            self.taiwan_chinese_dict.columns.similar_words,
            self.taiwan_chinese_dict.columns.opposite_words,
            self.taiwan_chinese_dict.columns.interpretation,
            self.taiwan_chinese_dict.columns.multi_phonetic_see_msg,
            self.taiwan_chinese_dict.columns.various_char
        ).where(
            self.taiwan_chinese_dict.columns.term_name == term_name
        )
        # 执行查询并获取结果
        result = self.connection.execute(query)
        rows = result.fetchall()
        return rows


if __name__ == "__main__":
    # SQLite数据库文件路径
    SQLALCHEMY_DATABASE_URL = "sqlite:///{}".format(os.path.abspath(
        os.path.join(os.path.dirname(__file__), "./dictionary.db")))
    # 创建DatabaseHandler实例
    db_handler = DatabaseHandler(SQLALCHEMY_DATABASE_URL)
    # 连接到数据库
    db_handler.connect()
    # 根据term_name进行查询
    term_name_result = db_handler.query_by_term_name('國')
    # 打印查询结果
    print(term_name_result)
    # 不需要连接时调用关闭连接
    db_handler.disconnect()
