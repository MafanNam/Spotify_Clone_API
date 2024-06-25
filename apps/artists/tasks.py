import logging
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone

from apps.artists.models import ArtistVerificationRequest
from config import celery_app as app

User = get_user_model()

logger = logging.getLogger(__name__)


@app.task(bind=True)
def send_verification_emails(self):
    # found all unprocessed verification requests in 24 hours
    time_threshold = timezone.now() - timedelta(days=1)
    logger.info(f"Found time threshold: {time_threshold}")

    requests = ArtistVerificationRequest.objects.filter(created_at__lte=time_threshold, is_processed=False)

    # Log the number of requests found
    logger.info(f"Found {requests.count()} verification requests")

    # If no request found, return a message indicating so
    if not requests.exists():
        logger.warning("No requests activation found")
        return "No requests activation found"

    # Create a list of email messages
    for request in requests:
        artist = request.artist
        send_mail(
            f"Verify your profile {artist.display_name}",
            f"Please verify your profile by clicking the following link.",
            settings.EMAIL_HOST_USER,
            [artist.user.email],
            fail_silently=False,
        )

        artist.is_verify = True
        artist.save()

        request.is_processed = True
        request.save()

        logger.info("Emails sent successfully")
        return "Emails sent successfully"
