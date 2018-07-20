from .models import User

def frontuser(request):
    user_id = request.session.get('user_id')
    request.session.set_expiry(0)
    if user_id:
        try:
            user = User.objects.get(pk=user_id)
            print('front_user',user)
            if user:
                return {'front_user':user}
            else:
                return {}
        except:
            return {}
    else:
        return {}