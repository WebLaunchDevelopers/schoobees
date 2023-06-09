from .models import  AcademicSession, AcademicTerm
from apps.base.models import UserProfile
from apps.staffs.models import Staff

def site_defaults(request):
    contexts = {}
    if request.user.is_authenticated:
        finaluser = request.user
        if finaluser.is_faculty:
            staffrecord = Staff.objects.get(email=finaluser.username)
            finaluser = staffrecord.user
        try:
            current_session = AcademicSession.objects.get(user=finaluser, current=True)
            contexts['current_session'] = current_session.name
        except AcademicSession.DoesNotExist:
            pass

        try:
            current_term = AcademicTerm.objects.get(user=finaluser, current=True)
            contexts['current_term'] = current_term.name
        except AcademicTerm.DoesNotExist:
            pass

        try:
            user_profile = UserProfile.objects.get(user=finaluser)
            contexts['school_name'] = user_profile.school_name
        except UserProfile.DoesNotExist:
            # Handle the case where no matching UserProfile object is found
            contexts['school_name'] = 'My School'

    return contexts
