from flask import jsonify, request
from http import HTTPStatus
from app.models.anime_model import Anime
from psycopg2.errors import UniqueViolation, UndefinedTable

def animes():
    animes = Anime.read_animes()

    animes_list = Anime.serialize_anime(animes)

    return {"data": animes_list}, HTTPStatus.OK

def select_by_id(anime_id):
    try:
        existing_ids = []
        for anms in animes()[0].get("data"):
            existing_ids.append(anms.get("id"))
        if anime_id not in existing_ids:
            raise TypeError
            
        anime = Anime.anime_by_id(anime_id)

        anime = Anime.serialize_anime(anime)

        return {"data": anime}, HTTPStatus.OK

    except (TypeError, UndefinedTable):
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND

def create():
    data = request.get_json()
    wrong_keys_sent = list(set(data.keys() - Anime.available_keys))

    try:
        data_to_post = {}
        data_to_post['anime'] = data['anime'].title()
        data_to_post['released_date'] = data['released_date']
        data_to_post['seasons'] = data['seasons']

        anime = Anime(**data_to_post)

        inserted_anime = anime.create_anime()
    
    except UniqueViolation:
        return jsonify({'error': 'anime already exists'}), HTTPStatus.CONFLICT
    
    except KeyError as k:
        return {
            "available_keys": Anime.available_keys,
            "wrong_keys_sent": wrong_keys_sent
        }, HTTPStatus.UNPROCESSABLE_ENTITY

    inserted_anime = Anime.serialize_anime(inserted_anime)

    return jsonify(inserted_anime), HTTPStatus.CREATED

def update(anime_id):
    try:
        existing_ids = []
        for anms in animes()[0].get("data"):
            existing_ids.append(anms.get("id"))
        if anime_id not in existing_ids:
            raise TypeError

        data = request.get_json()

        wrong_keys_sent = list(set(data.keys() - Anime.available_keys))

        data['anime'] = data['anime'].title()

        updated_anime = Anime.update_anime(anime_id, data)

    except KeyError as k:
        return {
            "available_keys": Anime.available_keys,
            "wrong_keys_sent": wrong_keys_sent
        }, HTTPStatus.UNPROCESSABLE_ENTITY
    
    except (TypeError, UndefinedTable):
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND
    
    except UniqueViolation:
        return jsonify({'error': 'anime already exists'}), HTTPStatus.CONFLICT
    
    patched_anime = Anime.serialize_anime(updated_anime)

    return jsonify(patched_anime), HTTPStatus.OK

def delete(anime_id):
    try:
        existing_ids = []
        for anms in animes()[0].get("data"):
            existing_ids.append(anms.get("id"))

        if anime_id not in existing_ids:
            print('anime_id not in existing_ids')
            raise TypeError

        Anime.delete_anime(anime_id)

        return {}, HTTPStatus.NO_CONTENT
    
    except (TypeError, UndefinedTable):
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND