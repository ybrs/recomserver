from django.http import Http404
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from models import ObjectWithInterest


class ObjectWithInterestSerializer(serializers.ModelSerializer):

    class Meta:
        model = ObjectWithInterest
        fields = ('id', 'object_id', 'object_type', 'similarity')

class ObjectWithInterestWithMatchCountSerializer(serializers.ModelSerializer):

    class Meta:
        model = ObjectWithInterest
        fields = ('id', 'object_id', 'object_type', 'similarity', 'match_count')


class ObjectWithInterestWithInterestsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ObjectWithInterest
        fields = ('id', 'object_id', 'object_type', 'similarity', 'interests')

class Similar(APIView):

    def get_object(self, pk):
        try:
            return ObjectWithInterest.objects.get(pk=pk)
        except ObjectWithInterest.DoesNotExist:
            raise Http404

    def get(self, request, object_id):
        limit = int(request.query_params.get('limit', 5))
        object_with_interest = self.get_object(object_id)

        matches = object_with_interest.best_matches(limit=limit)

        serializer = ObjectWithInterestSerializer(matches, many=True)
        resp = Response(serializer.data)

        return resp


class SimilarWithInterests(APIView):

    def get_object(self, pk):
        try:
            return ObjectWithInterest.objects.get(pk=pk)
        except ObjectWithInterest.DoesNotExist:
            raise Http404

    def get(self, request, object_id):
        limit = int(request.query_params.get('limit', 5))
        object_with_interest = self.get_object(object_id)

        matches = object_with_interest.best_matches(limit=limit)

        serializer = ObjectWithInterestWithInterestsSerializer(matches, many=True)
        resp = Response(serializer.data)

        return resp

class SimilarWithMatchCount(APIView):

    def get_object(self, pk):
        try:
            return ObjectWithInterest.objects.get(pk=pk)
        except ObjectWithInterest.DoesNotExist:
            raise Http404

    def get(self, request, object_id):
        limit = int(request.query_params.get('limit', 5))
        object_with_interest = self.get_object(object_id)

        matches = object_with_interest.best_matches_with_match_count(limit=limit)

        serializer = ObjectWithInterestWithMatchCountSerializer(matches, many=True)
        resp = Response(serializer.data)

        return resp
