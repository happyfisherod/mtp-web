# Python packages

import threading

# Django Packages
from django.contrib.gis.geos import Point, LineString
from django.http import Http404, JsonResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import MapillaryUser
# Custom Libs ##
from lib.functions import *
from lib.mapillary import Mapillary
from sequence.models import CameraMake
from sequence.models import Sequence, TransType
from sequence.views import get_images_by_sequence
from sys_setting.models import Tag as SeqTag
# Project packages
from tour.models import TourSequence


# App packages
# That includes from .models import *


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class SequenceCreate(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = [IsAuthenticated]

    def post(self, request, version='v1'):
        sequence_name = request.POST.get('name')
        if not sequence_name or sequence_name is None:
            return Response({'error': 'Sequence Name is missing', 'status': False})

        transport_type = request.POST.get('transport_type')
        if transport_type is None:
            return Response({'error': 'Transport type is missing', 'status': False})
        trans_types = TransType.objects.filter(name__iexact=transport_type.lower())[:1]
        if trans_types.count() == 0:
            return Response({'error': 'Transport type is invalid', 'status': False})
        else:
            trans_type = trans_types[0]

        sequence = Sequence()

        sequence.user = request.user

        sequence.name = sequence_name
        if not request.POST.get('description') is None:
            sequence.description = request.POST.get('description')
        sequence.transport_type_id = trans_type.pk
        sequence.is_published = False
        sequence.is_mapillary = False
        sequence.save()

        if not request.POST.get('tag') is None:
            tags = request.POST.get('tag')
            tag_ary = tags.split(',')
            if len(tag_ary) > 0:
                for t in tag_ary:
                    tag = SeqTag.objects.filter(name__iexact=t.lower())[:1]
                    if tag.count() > 0:
                        seq_tag = tag[0]
                    else:
                        seq_tag = SeqTag()
                        seq_tag.name = t
                        seq_tag.save()
                    sequence.tag.add(seq_tag)

                for tag in sequence.tag.all():
                    if not tag.name in tag_ary:
                        sequence.tag.remove(tag)

        return JsonResponse({
            'status': 'success',
            'message': 'Sequence successfully was created.',
            'unique_id': str(sequence.unique_id)
        })


class SequenceImport(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = [IsAuthenticated]

    def put(self, request, unique_id, version='v1'):
        sequence = Sequence.objects.get(unique_id=unique_id)
        if not sequence or sequence is None:
            return Response({'error': 'Sequence id is invalid', 'status': False})

        data = request.data

        print(data)

        message = ''

        if 'google_street_view' in data.keys():
            google_street_view = data['google_street_view']
            print(google_street_view)
            sequence.google_street_view = google_street_view
            message += 'Google Street View is updated \n'
            sequence.save()

        if 'strava' in data.keys():
            strava = data['strava']
            print(strava)
            sequence.strava = strava
            message += 'Strava is updated \n'
            sequence.save()



        if not 'mapillary_user_token' in data.keys():
            if message != '':
                return Response({'message': message, 'status': True})
            else:
                return Response({'error': 'Mapillary token is missing', 'status': False})

        token = data['mapillary_user_token']

        mapillary = Mapillary(token, source='mtpdu')
        map_user_data = mapillary.get_mapillary_user()
        if not map_user_data:
            return Response({'error': 'Mapillary token is invalid', 'status': False})


        if not 'mapillary_sequence_key' in data.keys():
            if message != '':
                return Response({'message': message, 'status': True})
            else:
                return Response({'error': 'Sequence key is missing', 'status': False})

        seq_key = data['mapillary_sequence_key']

        sequence_json = mapillary.get_sequence_by_key(seq_key)
        print('sequence_json')
        if not sequence_json:
            return Response({'error': 'Sequence is empty', 'status': False})
        properties = sequence_json['properties']
        geometry = sequence_json['geometry']
        seq_key = properties['key']

        if properties['username'] != map_user_data['username']:
            return Response({'error': 'You are not owner of this sequence', 'status': False})

        sequences = Sequence.objects.filter(seq_key=seq_key)[:1]
        if sequences.count() > 0:
            for seq in sequences:
                if seq.unique_id == unique_id:
                    continue
                tour_seqs = TourSequence.objects.filter(sequence=seq)
                if tour_seqs.count() > 0:
                    for t_s in tour_seqs:
                        t_s.delete()
                seq.delete()

        sequence.user = request.user
        if 'camera_make' in properties:
            camera_makes = CameraMake.objects.filter(name=properties['camera_make'])
            if camera_makes.count() > 0:
                c = camera_makes[0]
            else:
                c = CameraMake()
                c.name = properties['camera_make']
                c.save()
            sequence.camera_make = c
        sequence.captured_at = properties['captured_at']
        if 'created_at' in properties:
            sequence.created_at = properties['created_at']
        sequence.seq_key = properties['key']
        if 'pano' in properties:
            sequence.pano = properties['pano']
        if 'user_key' in properties:
            sequence.user_key = properties['user_key']
        if 'username' in properties:
            sequence.username = properties['username']
        sequence.geometry_coordinates_ary = geometry['coordinates']
        sequence.image_count = len(geometry['coordinates'])
        sequence.coordinates_cas = properties['coordinateProperties']['cas']
        sequence.coordinates_image = properties['coordinateProperties']['image_keys']
        if 'private' in properties:
            sequence.is_private = properties['private']

        lineString = LineString()
        firstPoint = None
        if sequence.image_count == 0:
            firstPoint = Point(sequence.geometry_coordinates_ary[0][0], sequence.geometry_coordinates_ary[0][1])
            lineString = LineString(firstPoint.coords, firstPoint.coords)
        else:
            for i in range(len(sequence.geometry_coordinates_ary)):
                coor = sequence.geometry_coordinates_ary[i]
                if i == 0:
                    firstPoint = Point(coor[0], coor[1])
                    continue
                point = Point(coor[0], coor[1])
                if i == 1:
                    lineString = LineString(firstPoint.coords, point.coords)
                else:
                    lineString.append(point.coords)

        sequence.geometry_coordinates = lineString


        sequence.is_published = True
        sequence.save()

        sequence.distance = sequence.get_distance()
        sequence.save()

        print('1')
        p = threading.Thread(target=get_images_by_sequence, args=(sequence, 'mtpdu',))
        p.start()
        print('2')

        return JsonResponse({
            'status': 'success',
            'message': 'Sequence successfully was imported. Sequence will be published in about 10 minutes.',
            'unique_id': str(sequence.unique_id)
        })


class MapillaryTokenVerify(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated]

    def post(self, request, version='v1'):
        mapillary_access_token = request.POST.get('mapillary_token')
        if mapillary_access_token is None or mapillary_access_token == '':
            return Response({'error': 'Mapillary token is invalid', 'status': False})
        user = request.user
        user.mapillary_access_token = mapillary_access_token
        user.save()

        map_user_data = check_mapillary_token(user)

        if not map_user_data:
            return Response({'error': 'Mapillary token is invalid', 'status': False})

        data = MapillaryUser.objects.filter(key=map_user_data['key'], user=request.user)
        if 0 == data.count():
            map_user = MapillaryUser()
        else:
            map_user = data[0]

        if 'about' in map_user_data:
            map_user.about = map_user_data['about']
        if 'avatar' in map_user_data:
            map_user.avatar = map_user_data['avatar']
        if 'created_at' in map_user_data:
            map_user.created_at = map_user_data['created_at']
        if 'email' in map_user_data:
            map_user.email = map_user_data['email']
        if 'key' in map_user_data:
            map_user.key = map_user_data['key']
        if 'username' in map_user_data:
            map_user.username = map_user_data['username']

        map_user.user = request.user
        map_user.save()
        return Response({'status': True, 'map_user_data': map_user_data})
