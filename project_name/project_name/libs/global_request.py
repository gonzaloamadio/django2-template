"""
This file contains a middleware and functions that makes possible to access
requests globally. This is very usefull when you need to check the current user
or some request headers in model's save() method, for example.
The middleware will store the current request in the _REQUESTS dictionary, so
you can use it later calling the get_current_requet or get_current_user
functions.
You just have to add the middleware to the MIDDLEWARE list (at the bottom is
ok), and the use the provided functions to access the request data.
"""

from threading import current_thread

_REQUESTS = {}


def get_current_request():
    """
    Returns the current request (or None)
    """
    thread_id = current_thread().ident
    return _REQUESTS.get(thread_id, None)


def get_current_user():
    """
    Returns the current user (or None) extracted from the current request.
    """
    current_request = get_current_request()
    if current_request and current_request.user.is_authenticated:
        return current_request.user
    return None


class GlobalRequestMiddleware(object):
    """
    Middleware that stores the current request to be used from any part of the
    code.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # store request related to this thread id
        thread_id = current_thread().ident
        _REQUESTS[thread_id] = request

        # call the next middleware/view
        response = self.get_response(request)

        # clenaup
        del _REQUESTS[thread_id]

        return response


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
