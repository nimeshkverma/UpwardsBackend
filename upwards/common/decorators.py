from functools import wraps
from rest_framework import status
from serializers import AuthenticationSerializer


def session_authorize(f):
    def abstract_customerId(request):
        if request.method == 'GET':
            customerId = request.args.get('customer_id')
        else:
            customerId = request.data.get('customer_id')
        return customerId

    def abstract_session_token(request):
        session_token_header_key = 'HTTP_SESSION_TOKEN'
        return request.META.get(session_token_header_key)

    @wraps(f)
    def decorated_function(*args, **kwargs):
        request = args[1]
        auth_data = {
            'customer_id': abstract_customerId(request),
            'session_token': abstract_session_token(request)
        }
        auth_serializer = AuthenticationSerializer(data=auth_data)
        auth_data['authorized'] = auth_serializer.is_valid(
        ) and auth_serializer.verify_and_update_session()
        return f(auth_data=auth_data, * args, **kwargs)
    return decorated_function
