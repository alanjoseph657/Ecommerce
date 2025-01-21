from functools import wraps
from django.http import HttpResponseForbidden

from Ecommerce.dataaccess.ecommerce_access.user_da import UserDA

def admin_required(f):
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        user_id = request.user.id
        if UserDA().is_admin(user_id):
            return f(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You do not have permission to access this")
    return decorated_function


