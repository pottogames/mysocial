# Create a new file middleware.py in your app directory
from django.http import HttpResponseForbidden
from .models import BanIP

class BanIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = request.META.get('REMOTE_ADDR')
        if BanIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden('You are banned from accessing this site.')
        return self.get_response(request)