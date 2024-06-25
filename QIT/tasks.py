from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from QIT.models import QitVisitorinout 

@shared_task
def update_checkin_status():
    now = timezone.now()
    eight_hours_ago = now - timedelta(hours=8)
    visitors_to_update = QitVisitorinout.objects.filter(
        entrydate__lt=eight_hours_ago,
        status='A',
        checkinstatus='I'
    )
    if visitors_to_update.exists():
        visitors_to_update.update(checkinstatus='O')
        print("Successfully updated CheckInStatus for", visitors_to_update.count(), "visitors.")
    else:
        print("No visitors found matching the update criteria.")
