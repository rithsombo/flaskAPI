import psycopg2;
from psycopg2.extras import DictCursor;

con=psycopg2.connect(database="lemonade", user="postgres",
                 password="123456", host="127.0.0.1", port="5433")

class PgConfig:
    @staticmethod
    def getCursor(self):
        return con.cursor(cursor_factory=DictCursor)

    @staticmethod
    def Commit(self):
        con.commit();



# cur=PgConfig.getCursor(PgConfig)
#
# cur.execute("select * from usr.tbluser")
# data=cur.fetchall();
# print(data)