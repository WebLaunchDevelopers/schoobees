from apps.students.models import Feedback

def feedback_count(request):
    feedback_count = Feedback.objects.filter(user=request.user, is_seen=False).count()
    return {'feedback_count': feedback_count}
