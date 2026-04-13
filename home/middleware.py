from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from .models import PageVisit

class TrackUserMiddleware:
    """Logs each request to the PageVisit model."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip admin pages if you like
        if not request.path.startswith('/admin/'):
            ip = request.META.get('REMOTE_ADDR', '')
            path = request.path
            referer = request.META.get('HTTP_REFERER', '')
            user_agent = request.META.get('HTTP_USER_AGENT', '')

            PageVisit.objects.create(
                ip_address=ip,
                path=path,
                referer=referer,
                user_agent=user_agent
            )

        response = self.get_response(request)
        return response