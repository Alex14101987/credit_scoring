class MyDatabase:
    """
    Класс представляет собой соединение к базе данных, 
    через которое можно отрпавлять запросы и получать ответы

    :param db:  название БД.
    :type db: str
    :param user: имя пользователя БД.
    :type user: str
    :param host: хост для подключения к БД.
    :type host: str
    :param password: парль пользователя БД.
    :type password: str
    """

    def __init__(self, db="mydb", user="postgres", host="127.0.0.1", password="postgres"):
        self.conn = psycopg2.connect(dbname=db,
                                     user=user,
                                     host=host,
                                     password=password
                                     )
        self.cur = self.conn.cursor()

    def send_query(self, query):
        """
        Выполняет запрос к базе.

        :param query: строка с sql запросом.
        """
        try:
            self.cur.execute(query)
            self.conn.commit()
        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)

    def get_query(self, query):
        """
        Выполняет запрос к базе, который должен вернуть результат

        :param query: строка с sql запросом.

        :return: pandas.DataFrame
        """
        df = pd.read_sql(query, self.conn)
        return df

    def close(self):
        """
        Закрывает соединение с БД.
        """
        self.cur.close()
        self.conn.close()