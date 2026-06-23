from configapp.models import UserProfile


def user_profile(request):
    ctx = {}
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            ctx['user_profile'] = profile
            ctx['theme_color'] = profile.theme_primary_color
        except UserProfile.DoesNotExist:
            ctx['theme_color'] = '#6750A4'
    else:
        ctx['theme_color'] = '#6750A4'
    return ctx
