import logging

from apps.albums.models import Album
from apps.core.services import generate_color_from_image
from config import celery_app as app

logger = logging.getLogger(__name__)


@app.task()
def generate_album_color(album_id):
    album = Album.objects.get(id=album_id)
    logger.info(f"Album: {album}")
    if album.image:
        logger.info("in album image")
        album.color = generate_color_from_image(album.image)
        logger.info(f"color: {album.color}")
        logger.info(f"generated color: {generate_color_from_image(album.image)}")
        album.save(update_fields=["color"], generate_color=False)
    return "OK"
