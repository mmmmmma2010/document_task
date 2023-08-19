from rest_framework import serializers
import base64
from django.core.files.base import ContentFile

def decode_base64(base64_data):
    try:
        format, data = base64_data.split(';base64,')
    except Exception as e:
        print("error",e)
        raise serializers.ValidationError({"Error":"not supported file"})
    ext = format.split('/')[-1]
    content=ContentFile(base64.b64decode(data))
    return (ext,content)
