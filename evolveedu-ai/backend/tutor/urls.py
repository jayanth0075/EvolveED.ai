# urls.py for tutor
from rest_framework.routers import DefaultRouter
from tutor.views import TutorViewSet, SessionViewSet, StudyNoteViewSet

router = DefaultRouter()
router.register(r"tutors", TutorViewSet, basename="tutor")
router.register(r"sessions", SessionViewSet, basename="session")
router.register(r"notes", StudyNoteViewSet, basename="studynote")

urlpatterns = router.urls
