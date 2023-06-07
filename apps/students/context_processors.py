from apps.students.models import Feedback

def feedback_count(request):
    if request.user.is_authenticated:
        feedback_count = Feedback.objects.filter(user=request.user, is_seen=False).count()
        return {'feedback_count': feedback_count}
    else:
        return {'feedback_count': 0}
