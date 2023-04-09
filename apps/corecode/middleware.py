from .models import AcademicSession, AcademicTerm

class SiteWideConfigs:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_session = None
        current_term = None

        if request.user.is_authenticated:
            try:
                current_session = AcademicSession.objects.get(user=request.user, current=True)
                current_term = AcademicTerm.objects.get(user=request.user, current=True)
            except AcademicSession.DoesNotExist or AcademicTerm.DoesNotExist:
                pass

        request.current_session = current_session
        request.current_term = current_term

        response = self.get_response(request)

        return response
