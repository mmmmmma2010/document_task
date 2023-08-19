from rest_framework import  status
from rest_framework.viewsets import  generics,ViewSet
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import UploadedFile
from .serializers import FileUploadSerializer,CustomFileUploadSerializer
from PIL import Image
import fitz
from pdf2image import convert_from_path
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer


class FileUploadView(generics.CreateAPIView):
    
    queryset=UploadedFile.objects.all()
    serializer_class=FileUploadSerializer
    renderer_classes=[JSONRenderer]


class UploadedImageViewSet(ViewSet,generics.ListAPIView,generics.DestroyAPIView,generics.RetrieveAPIView):
    queryset = UploadedFile.objects.filter(file_type="image")
    serializer_class = CustomFileUploadSerializer
    renderer_classes=[JSONRenderer]

    def retrieve(self, request, *args, **kwargs):

        file=self.get_object().file
        img = Image.open(file)
        width=img.width
        height=img.height
        chanals=img.getbands()
        chanals=len(chanals)
        response={
            "location":file.url,
            "width":width,
            "height":height,
            "chanals":chanals
        }
        return Response(response,status=status.HTTP_200_OK)


class UploadedPDFViewSet(ViewSet,generics.ListAPIView,generics.DestroyAPIView,generics.RetrieveAPIView):
    queryset = UploadedFile.objects.filter(file_type="pdf")
    serializer_class = CustomFileUploadSerializer
    renderer_classes=[JSONRenderer]


    def retrieve(self, request, *args, **kwargs):

        file=self.get_object().file
        pdf = fitz.open(file)
        num_pages = pdf.page_count
        page = pdf.load_page(0)
        print("num_pages",num_pages)
        print("page",page.__dir__())
        page_width=page.rect.width
        page_height=page.rect.height
        response={
            "location":file.url,
            "page_width":page_width,
            "page_height":page_height,
            "num_pages":num_pages
        }
        return Response(response,status=status.HTTP_200_OK)

class RotateImageViewSet(APIView):
    def post(self, request):
        image_id = request.data.get('image_id')
        rotation_angle = request.data.get('rotation_angle')

        try:
            image = UploadedFile.objects.get(pk=image_id)
            img = Image.open(image.file.path)
            
            rotated_img = img.rotate(rotation_angle, expand=True)
            rotated_img.save(image.file.path)
            return Response({'rotated_image': image.file.path}, status=status.HTTP_200_OK)
        except UploadedFile.DoesNotExist:
            raise NotFound(detail='Image not found')
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ConvertPDFToImageViewSet(APIView):
    def post(self, request):
        pdf_id = request.data.get('pdf_id')

        try:
            pdf = UploadedFile.objects.get(pk=pdf_id)
            images = convert_from_path(pdf.file.path)

            for i, img in enumerate(images):
                img_path = pdf.file.path.replace('.pdf', f'_{i+1}.jpg')
                img.save(img_path, 'JPEG')

                new_image = UploadedFile.objects.create(
                    file=img_path,
                )

            return Response({'image': img_path}, status=status.HTTP_200_OK)
        except UploadedFile.DoesNotExist:
            raise NotFound(detail='PDF not found')
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
