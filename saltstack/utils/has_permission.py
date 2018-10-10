import re

def has_permission(request):

    for i in request.session.get('url'):
        result = re.match(i, request.path_info)
        if result:
            return True