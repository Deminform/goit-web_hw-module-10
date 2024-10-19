from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings


def previous_url(request):
    prev_url = request.META.get('HTTP_REFERER')
    if prev_url and url_has_allowed_host_and_scheme(url=prev_url, allowed_hosts={request.get_host()}):
        return {'previous_url': prev_url}
    else:
        return {'previous_url': None}
