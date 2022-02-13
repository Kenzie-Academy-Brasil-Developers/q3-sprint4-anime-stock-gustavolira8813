from psycopg2 import sql
import psycopg2
import os
configs = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

class DatabaseConnector:
    @classmethod
    def get_conn_cur(cls):
        cls.conn = psycopg2.connect(**configs)
        cls.cur = cls.conn.cursor()
        cls.cur.execute("""
            CREATE TABLE IF NOT EXISTS animes (
                id              BIGSERIAL       PRIMARY KEY,
                anime           VARCHAR(100)    NOT NULL        UNIQUE,
                released_date   DATE            NOT NULL,
                seasons         INTEGER         NOT NULL
            );"""
        )

    @classmethod
    def get_conn_cur_without_table_creation(cls):
        cls.conn = psycopg2.connect(**configs)
        cls.cur = cls.conn.cursor()

    @classmethod
    def commit_and_close(cls):
        cls.conn.commit()
        cls.cur.close()
        cls.conn.close()
    
    @classmethod
    def get_column_names(cls, table_name: str):
        cls.get_conn_cur()

        query = sql.SQL(
            """
            SELECT
                column_name
            FROM
                information_schema.COLUMNS
            WHERE table_name = {table_name}
            ORDER BY ordinal_position;
            """
        ).format(table_name=sql.Literal(table_name))

        cls.cur.execute(query)

        column_names = cls.cur.fetchall()

        cls.commit_and_close()

        return [row[0] for row in column_names]