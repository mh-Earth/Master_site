from functools import wraps
import json
from django.http import JsonResponse, HttpResponse
from django.conf import settings
import logging
from .models import RedditAdmin

def add_cors_headers(view_func):
    """
    Decorator to add CORS headers to the response.
    NOTE: The recommended way to handle CORS in Django is by using the
    `django-cors-headers` package. This decorator is a direct conversion
    of the original Flask logic.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        if isinstance(response, JsonResponse) or isinstance(response, HttpResponse):
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Methods'] = 'GET, DELETE, HEAD, OPTIONS'
            response['Access-Control-Allow-Headers'] = 'Content-Type'
            response['Access-Control-Max-Age'] = '3600'
        return response

    return wrapper

def require_api_key(view_func):
    """
    Decorator to check for a valid API key in the request headers or body.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        api_key = request.GET.get('api_key')
        if not api_key:
            try:
                data = json.loads(request.body)
                api_key = data.get('api_key')
            except (json.JSONDecodeError, KeyError):
                pass
        
        # NOTE: Replace 'your-api-key' with your actual API key or fetch it from settings.
        if not api_key or api_key != "4EJzNg7UAV1vRisJCcW4rYQfOqPRIOpoQsG63BBkIFYPFdTCdatrLSm6jXpPYYiAzaKoLO02FZSPn7F5CguNKo51jfGxHpaoLjq0RhXdq5pFR7VTSxAv3kSbOUixV0X7":
            logging.warning('{"Message": "Invalid API Key"}')
            return JsonResponse({"Message": "Invalid API Key"}, status=401)
            
        return view_func(request, *args, **kwargs)

    return wrapper

def require_password(view_func):
    """
    Decorator to check for a password exsits in the request JSON body.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.method in ['POST', 'DELETE', 'PUT']:
            try:
                data = json.loads(request.body)
                password = data.get('password')

                if not password:
                    logging.error('{"Message":"Password cannot be empty"} ,401')
                    return JsonResponse({"Message": "Password cannot be empty"}, status=401)
                
                # Check password against the stored admin password
                admin_user = RedditAdmin.objects.first()
                if not admin_user or password != admin_user.password:
                    logging.error('{"Message":"Password required"} ,401')
                    return JsonResponse({"Message": "Password required"}, status=401)

            except json.JSONDecodeError:
                logging.error('{"Message":"Invalid JSON format"} ,400')
                return JsonResponse({"Message": "Invalid JSON format"}, status=400)
            except Exception as e:
                logging.error(e)
                return JsonResponse({"Message": "Server Error"}, status=500)

        return view_func(request, *args, **kwargs)

    return wrapper

def admin_user_require(view_func):
    """
    Decorator to ensure that admin user exsits.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # A simple check to see if the user is authenticated and is a superuser.
        if RedditAdmin.objects.exists():
            return view_func(request, *args, **kwargs)
        else:
            logging.warning('{"Message":"Access denied. User is not an admin."}')
            return JsonResponse({"Message": "Access denied. User is not an admin."}, status=403)
    return wrapper

def password_auth(view_func):
    """
    Decorator to check the password provided in the request body.
    As only one user can be create in app's life time (admin user) this will 
    only check for admin's passowrd
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.method in ['POST', 'DELETE', 'PUT']:
            try:
                data = json.loads(request.body)
                password = data.get('password')

                user = RedditAdmin.objects.first()
                if user and user.password == password:
                    return view_func(request, *args, **kwargs)

                else:
                    logging.warning('{"Message":"Invalid credentials or not an admin."}')
                    return JsonResponse({"Message": "Invalid credentials or not an admin."}, status=401)

            except json.JSONDecodeError:
                return JsonResponse({"Message": "Invalid JSON format."}, status=400)
            except Exception as e:
                logging.error(e)
                return JsonResponse({"Message": "Server Error"}, status=500)
        else:
            return view_func(request, *args, **kwargs)
    return wrapper

def validate_json_request(view_func):
    """
    Decorator to validate if the request body contains valid JSON data.
    If the request body is not valid JSON, it returns a 400 Bad Request error.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # We only care about methods that can have a body
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                # Attempt to parse the JSON body
                json.loads(request.body)
            except json.JSONDecodeError as e:
                logging.error(f"Invalid JSON in request body: {e}")
                return JsonResponse({"error": "Invalid JSON format"}, status=400)
            
        # If the JSON is valid or if the method doesn't have a body,
        # proceed to the original view function
        return view_func(request, *args, **kwargs)
    
    return wrapper