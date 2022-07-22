from rest_framework.views import exception_handler


def core_exception_handler(exc, context):
    responce = exception_handler(exc, context)
    handlers = {
        'ValidationError': _handle_generic_error
    }
    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, responce)

    return responce


def _handle_generic_error(exc, context, responce):
    responce.data = {
        'errors': responce.data
    }
    return responce