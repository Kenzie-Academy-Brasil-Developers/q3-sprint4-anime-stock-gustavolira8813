 
from app.controllers import animes_controller
from flask import Blueprint

bp = Blueprint("animes", __name__, url_prefix='/animes')

bp.get('')(animes_controller.animes)
bp.get('/<int:anime_id>')(animes_controller.select_by_id)

bp.post('')(animes_controller.create)

bp.patch('/<int:anime_id>')(animes_controller.update)

bp.delete('/<int:anime_id>')(animes_controller.delete)