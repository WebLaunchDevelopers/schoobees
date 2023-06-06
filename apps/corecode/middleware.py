from .models import AcademicSession, AcademicTerm
from apps.staffs.models import Staff

class SiteWideConfigs:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_session = None
        current_term = None

        if request.user.is_authenticated:
            finaluser = request.user
            if finaluser.is_faculty:
                staffrecord = Staff.objects.get(email=finaluser.username)
                finaluser = staffrecord.user            
            try:
                current_session = AcademicSession.objects.get(user=finaluser, current=True)
            except AcademicSession.DoesNotExist:
                pass
            try:
                current_term = AcademicTerm.objects.get(user=finaluser, current=True)
            except AcademicTerm.DoesNotExist:
                pass

        request.current_session = current_session
        request.current_term = current_term

        response = self.get_response(request)

        return response
