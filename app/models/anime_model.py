from app.models import DatabaseConnector
from psycopg2 import sql

class Anime(DatabaseConnector):
    available_keys = ['anime', 'released_date', 'seasons']
    anime_keys = DatabaseConnector.get_column_names('animes')

    def __init__(self, *args, **kwargs):
        self.anime = kwargs['anime']
        self.released_date = kwargs['released_date']
        self.seasons = kwargs['seasons']

    @staticmethod
    def serialize_anime(data, keys=anime_keys):
        if type(data) is tuple:
            return dict(zip(keys, data))
        if type(data) is list:
            return [dict(zip(keys, anime)) for anime in data]

    @classmethod
    def read_animes(cls):
        cls.get_conn_cur()

        query = "SELECT * FROM animes ORDER BY id;"

        cls.cur.execute(query)

        animes = cls.cur.fetchall()

        cls.commit_and_close()

        return animes

    @classmethod
    def anime_by_id(cls, anime_id):
        cls.get_conn_cur_without_table_creation()

        query = "SELECT * FROM animes WHERE id = %s;"

        query_id = str(anime_id)

        cls.cur.execute(query, query_id)

        anime = cls.cur.fetchone()

        cls.commit_and_close()

        return anime

    def create_anime(self):
        self.get_conn_cur()

        query = """
                INSERT INTO
                    animes (anime, released_date, seasons)
                VALUES
                    (%s, %s, %s)
                RETURNING *
            """
        
        query_values = list(self.__dict__.values())

        self.cur.execute(query, query_values)

        inserted_anime = self.cur.fetchone()

        self.commit_and_close()

        return inserted_anime
    
    @classmethod
    def update_anime(cls, anime_id, data):
        cls.get_conn_cur()

        columns = [sql.Identifier(key) for key in data.keys()]
        values = [sql.Literal(value) for value in data.values()]

        query = sql.SQL(
            """
                UPDATE
                    animes
                SET
                    ({columns}) = ROW({values})
                WHERE
                    id = {id}
                RETURNING
                    *
                ;
            """
        ).format(
            id = sql.Literal(anime_id),
            columns = sql.SQL(",").join(columns),
            values = sql.SQL(",").join(values),
        )

        cls.cur.execute(query)

        updated_anime = cls.cur.fetchone()

        cls.commit_and_close()

        return updated_anime

    @classmethod
    def delete_anime(cls, anime_id):
        cls.get_conn_cur()

        query = sql.SQL(
            """
                DELETE FROM 
                    animes 
                WHERE 
                    id = {id} 
                RETURNING 
                    *
                ;
            """).format(id=sql.Literal(anime_id))

        cls.cur.execute(query)

        deleted_anime = cls.cur.fetchone()
        
        cls.commit_and_close()

        return deleted_anime