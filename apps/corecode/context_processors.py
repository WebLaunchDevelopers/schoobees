from .models import SiteConfig, AcademicSession, AcademicTerm
from apps.base.models import CustomUser, UserProfile

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

        try:
            user_profile = UserProfile.objects.get(user=custom_user)
            contexts['school_name'] = user_profile.school_name
        except UserProfile.DoesNotExist:
            # Handle the case where no matching UserProfile object is found
            contexts['school_name'] = 'My School'

    return contexts
