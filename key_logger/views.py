from django.shortcuts import render,HttpResponse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import uuid


from .models import Keystroke
# Create your views here.

def generate_session_id():
    """
    Generates a unique session ID using the UUID library.
    This can be called from the client-side to create a new session
    identifier for a series of keystrokes.
    """
    return uuid.uuid4().hex


@csrf_exempt
def save_keystroke(request):
    """
    A view function to receive and save keystrokes sent via a POST request.

    This function uses @csrf_exempt for simplicity, which is NOT
    recommended for production environments without additional security measures.
    """
    if request.method == 'POST':
        try:
            # Decode the JSON data from the request body
            data = json.loads(request.body)
            keystroke = data.get('keystroke')
            session_id = data.get('session_id')
            username = data.get("username")
            if bool(session_id) == False:
                session_id = generate_session_id()
                if keystroke:
                    # Create and save a new Keystroke object
                    Keystroke.objects.create(
                        keystroke=keystroke,
                        session_id=session_id,
                        username = username
                    )
                    return JsonResponse({'status': 'success', 'message': 'Keystroke saved successfully.','session_id':session_id},status=201)
                else:
                    return JsonResponse({'session_id':session_id},stauts=201)
                    
            # Ensure both keystroke and session_id are present
            if keystroke and session_id and username:
                # Create and save a new Keystroke object
                Keystroke.objects.create(
                    keystroke=keystroke,
                    session_id=session_id,
                    username=username
                )
                return JsonResponse({'status': 'success', 'message': 'Keystroke saved successfully.'},status=200)
            else:
                return JsonResponse({},status=400)
        except json.JSONDecodeError:
            return JsonResponse({},status=400)
    else:
        # Return an error for any request method other than POST
        return JsonResponse({},status=405)
