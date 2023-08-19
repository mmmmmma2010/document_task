from rest_framework import serializers
from .utils import decode_base64
from .models import UploadedFile





class CustomFileUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = UploadedFile  # Use a generic UploadedFile model for both images and PDFs
        fields = "__all__"
    



class FileUploadSerializer(serializers.ModelSerializer):
    base64_data = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UploadedFile  # Use a generic UploadedFile model for both images and PDFs
        fields = ('base64_data',)

    def create(self, validated_data):
        base64_data = validated_data.pop('base64_data')
        ext,content=decode_base64(base64_data)

        image_ext=["JPEG","JPG","PNG","GIF"]
        pdf_ext=["pdf"]
        file_type="pdf"

        if  not ext in image_ext+pdf_ext:
            raise serializers.ValidationError({"Error":"not supported file"})
        
        if not ext in pdf_ext:
            file_type="image"
            
        uploaded_file = UploadedFile.objects.create(file_type=file_type,**validated_data )
        uploaded_file.file.save(f'file_{uploaded_file.pk}.{ext}', content, save=False)
        uploaded_file.save()

        return uploaded_file
    


