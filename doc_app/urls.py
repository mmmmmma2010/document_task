from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UploadedImageViewSet, UploadedPDFViewSet,FileUploadView,RotateImageViewSet,ConvertPDFToImageViewSet

router = DefaultRouter()
router.register(r'images', UploadedImageViewSet)
router.register(r'pdfs', UploadedPDFViewSet)


urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('rotate/', RotateImageViewSet.as_view(), name='file-rotate'),
    path('convert-pdf-to-image/', ConvertPDFToImageViewSet.as_view(), name='file-convert'),
    path('', include(router.urls)),
]
