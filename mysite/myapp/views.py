from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from .models import Sentiment
from .serializers import SentimentSerializer
import myapp.screen as screen
import json


# Create your views here.
class SentimentViewSet(viewsets.ViewSet):
    """
    A viewset that provides `retrieve`, `create`, and `list` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """

    """
    demo sentiments:
    negative:
        The older interface was much simpler
    neutral: 
        I don't think there is anything I really dislike about the product
    positive:
        Text need to be analyzed
    """
    # def list(self, request):
    #     serializer = SentimentSerializer()
    #     return Response({}, status=HTTP_200_OK)

    def create(self, request):
        # check request format
        if request.content_type != "application/json":
            return Response({"error": "content-type should be application/json "}, status=HTTP_400_BAD_REQUEST)

        # check request is valid
        text = request.data.get('text', None)

        if not text or not isinstance(text, str) or len(request.data) != 1:
            context = {
                "text": "Enter the text"
            }
            return Response({"error": "invalid format",
                             "valid format": context}, status=HTTP_400_BAD_REQUEST)
        sentiment = None
        print("in post method")
        try:
            sentiment = screen.screen(text)
            print("sentiment: ", sentiment)
        except (TypeError, AttributeError, IOError, OSError) as err:
            return Response({"error": err}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": e}, status=HTTP_500_INTERNAL_SERVER_ERROR)


        context = {
            'text': text,
            'label': sentiment
        }
        serializer = SentimentSerializer(data=context)
        if serializer.is_valid():
            serializer.save()
            return Response({'sentiment': sentiment}, status=HTTP_200_OK)
        else:
            return Response({"error": serializer.errors}, status=HTTP_500_INTERNAL_SERVER_ERROR)