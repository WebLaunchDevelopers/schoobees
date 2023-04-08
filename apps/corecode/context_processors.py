from .models import SiteConfig, AcademicSession, AcademicTerm
from apps.base.models import CustomUser

def site_defaults(request):
    contexts = {}
    if request.user.is_authenticated:
        try:
            current_session = AcademicSession.objects.get(user=request.user, current=True)
            contexts['current_session'] = current_session.name
        except AcademicSession.DoesNotExist:
            pass

        try:
            current_term = AcademicTerm.objects.get(user=request.user, current=True)
            contexts['current_term'] = current_term.name
        except AcademicTerm.DoesNotExist:
            pass

        custom_user = CustomUser.objects.get(username=request.user.username)
        contexts['school_name'] = custom_user.school_name

    return contexts
