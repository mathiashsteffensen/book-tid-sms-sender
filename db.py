import psycopg2

class DB_Conn():
    def __init__(self, host, password, user = "postgres", port = "5432"):
        super().__init__()
        self.db = psycopg2.connect(host=host, port=port, user=user, password=password)
        self.query = self.db.cursor()

    def close(self):
        self.db.close()
        self.query.close()

    def commit(self):
        self.db.commit()
