import logging

from config import celery_app as app

# from pydub import AudioSegment

logger = logging.getLogger(__name__)


@app.task()
def reduce_audio_file_weight(file_path):
    # audio = AudioSegment.from_file(file_path)
    # logger.info(audio)
    # output_path = file_path.replace('.mp3', '_reduced.mp3')
    # audio.export(output_path, format='mp3', bitrate='128k')
    #
    # os.remove(file_path)
    # os.rename(output_path, file_path)

    return "Success reduced track weight"
