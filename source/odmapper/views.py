# Copyright (C) 2024 A*STAR

# ODmapper (Omics Data Mapping and Harmonizer) is an effort by the
# Data Management Platform in the Bioinformatics Institute (BII),
# Agency of Science, Technology and Research (A*STAR), Singapore.

# This file is part of ODmapper.

# ODmapper is an open-source tool.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0 you can redistribute it and/or modify
# it under the terms of the https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# You should have received a copy of the Apache License, Version 2.0
# along with this program.  If not, see <https://www.apache.org/licenses/LICENSE-2.0>

from rest_framework import status, mixins, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser

from django.http import Http404
from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import get_object_or_404

from odmapper.models import Concept, ConceptSynonym
from odmapper.serializers import ConceptSerializer, ConceptSynonymSerializer
from odmapper.forms import ConceptForm

# authentication and permission purpose
from django.contrib.auth.models import User
from rest_framework import permissions

### Mixin for filtering queryset based on lookup_fields
class MultipleFieldLookupMixin:
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs.get(field): # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj

### Retrieve concept id detail
class ConceptDetail(MultipleFieldLookupMixin, generics.RetrieveAPIView):
    """
    Retrieve a concept id detail.
    """
    #authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = Concept.objects.all()
    serializer_class = ConceptSerializer
    lookup_fields = ['concept_id']

### Retrieve concept ids based on string contains within "concept_id", "concept_code" and "concept_name"
class ConceptSeekList(generics.ListAPIView):
    """
    Retrieve a list of concepts based on query_string contains within concept_id, concept_code and concept_name.
    """
    #authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = ConceptSerializer

    def get_queryset (self):
        self.query_text = self.kwargs['query_text']
        queryset =  Concept.objects.all().filter(Q(concept_id__contains=self.query_text) | Q(concept_name__contains=self.query_text) | Q(concept_code__contains=self.query_text)).distinct()
        return queryset

    def get_object (self):
        return get_object_or_404 (self.get_queryset(), id=self.query_text)


### Retrieve concept ids based on concept_synonym_name
class ConceptSynonymList(generics.ListAPIView):
    """
    Retrieve a list of concepts based on concept_synonym_name.
    """
    #authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = ConceptSynonymSerializer

    def get_queryset (self):
        self.synonym = self.kwargs['synonym']
        queryset = ConceptSynonym.objects.filter(concept_synonym_name=self.synonym).select_related('concept_id')
        return queryset

    def get_object (self):
        return get_object_or_404 (self.get_queryset(), id=self.synonym)

### Query Concept according to "Concept ID", "Synonym" and "Default (Concept_Name, Concept_Code, Synonym, Concept ID)"
class ConceptQuery(APIView):

    #authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query_text = request.query_params.get("query_text", None)
        searchtype = request.query_params.get("type", None)

        try:
            if searchtype == 'default':
                concepts = Concept.objects.all().filter(Q(concept_id__contains=query_text) | Q(concept_name__contains=query_text) | Q(concept_code__contains=query_text)).distinct()
                synonyms = ConceptSynonym.objects.all().filter(concept_synonym_name__contains=query_text)
                if not concepts and not synonyms:
                   return Response(status=status.HTTP_404_NOT_FOUND)
                elif not concepts:
                   serializer = ConceptSynonymSerializer(synonyms, many=True)
                   return Response(serializer.data)
                elif not synonyms:
                   serializer = ConceptSerializer(concepts, many=True)
                   return Response(serializer.data)
                else:
                    serializer_synonyms = ConceptSynonymSerializer(synonyms, many=True)
                    serializer_concepts = ConceptSerializer(concepts, many=True)
                    return Response({
                        "Concepts": serializer_concepts.data,
                        "Synonyms": serializer_synonyms.data
                    })
            elif searchtype == 'concept_id':
                concepts = Concept.objects.get(pk=query_text)
                serializer = ConceptSerializer(concepts)
                return Response(serializer.data)
            elif searchtype == 'concept_synonym':
                #concepts = ConceptSynonym.objects.all().filter(concept_synonym_name=query_text)
                concepts = ConceptSynonym.objects.filter(concept_synonym_name__contains=query_text).select_related('concept_id')
                if not concepts:
                   return Response(status=status.HTTP_404_NOT_FOUND)
                else:
                   serializer = ConceptSynonymSerializer(concepts, many=True)
                return Response(serializer.data)
            else:
                return render(request, "concept.html")
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
