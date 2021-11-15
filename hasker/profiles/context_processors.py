from .models import Profile


def profile_pic(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(login=request.user)
        return {'avatar_picture': profile.avatar}
    return {}
