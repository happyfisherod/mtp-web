## Django Packages
## Python Packages
import uuid
from datetime import datetime

from django.contrib.auth import (
    get_user_model, )
from django.contrib.gis.db import models
from django.urls import reverse

from lib.mvtManager import CustomMVTManager
from lib.functions import get_current_timestamp
from sys_setting.models import Tag
from sequence.models import Sequence

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

UserModel = get_user_model()





def image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    current_time = get_current_timestamp()
    return 'guidebook/{0}/cover_image/{1}.jpg'.format(instance.unique_id, current_time)


def scene_image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    current_time = get_current_timestamp()
    path = 'guidebook/{}/scene/{}_{}.jpg'.format(instance.guidebook.unique_id, instance.unique_id, current_time)
    print(path)
    return path


def poi_image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    current_time = get_current_timestamp()
    return 'guidebook/{}/scene/{}/poi/{}_{}.jpg'.format(instance.scene.guidebook.unique_id, instance.scene.unique_id, instance.pk, current_time)



# class Tag(models.Model):
#     alphanumeric = RegexValidator(r'^[0-9a-zA-Z-]*$', 'Only alphanumeric characters are allowed for Username.')
#     name = models.CharField(max_length=50, unique=True, null=True, validators=[alphanumeric])
#     description = models.TextField(default=None, blank=True, null=True)
#     is_actived = models.BooleanField(default=True)
#
#     def __str__(self):
#         return self.name


def getAllTags():
    items = Tag.objects.filter(is_actived=True)
    itemsTuple = ()
    for item in items:
        itemsTuple = itemsTuple + ((item.pk, item.name),)
    return itemsTuple


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(default=None, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Guidebook(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    cover_image = models.ImageField(upload_to=image_directory_path, null=True)
    tag = models.ManyToManyField(Tag)
    is_published = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    like_count = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('guidebook.guidebook_detail', kwargs={'unique_id': str(self.unique_id)})

    def getScenes(self):
        scenes = Scene.objects.filter(guidebook=self).order_by('sort')
        return scenes

    def getScenePositions(self):
        scenes = Scene.objects.filter(guidebook=self)
        positions = []
        if scenes and scenes.count() > 0:
            for scene in scenes:
                position = [scene.lat, scene.lng]
                positions.append(position)
        return positions

    def getFirstScene(self):
        scenes = Scene.objects.filter(guidebook=self).order_by('sort')
        if scenes and scenes.count() > 0:
            firstScene = scenes[0]
            return firstScene
        else:
            return ''

    def getSceneCount(self):
        scenes = Scene.objects.filter(guidebook=self)
        return scenes.count()

    def get_like_count(self):
        liked_guidebook = GuidebookLike.objects.filter(guidebook=self)
        if not liked_guidebook:
            return 0
        else:
            return liked_guidebook.count()

    def get_short_description(self):
        description = self.description
        if len(description) > 100:
            return description[0:100] + '...'
        else:
            return description

    def get_tag_str(self):
        tags = []
        if self.tag is None:
            return ''
        for tag in self.tag.all():
            if tag and tag.is_actived:
                tags.append(tag.name)

        if len(tags) > 0:
            return ', '.join(tags)
        else:
            return ''

    def get_tags(self):
        tags = []
        if self.tag is None:
            return []
        for tag in self.tag.all():
            if tag and tag.is_actived:
                tags.append(tag.name)
        return tags

    def get_cover_image(self):
        scenes = Scene.objects.filter(guidebook=self)
        if scenes.count() > 0:
            return scenes[0].image_key
        else:
            return None

    def get_cover_imageUserOnMapillary(self):
        scenes = Scene.objects.filter(guidebook=self)
        if scenes.count() > 0:
            return scenes[0].username
        else:
            return ''


class GuidebookLike(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    guidebook = models.ForeignKey(Guidebook, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)


class POICategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(default=None, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'POI Categories'


class CustomSceneMVTManager(CustomMVTManager):
    def get_additional_where(self, additional_filters={}, request=None):
        from tour.models import Tour
        additional_where = ""
        page_name = ''
        if 'page_name' in additional_filters.keys() and additional_filters['page_name'] != '':
            page_name = additional_filters['page_name']
        else:
            return ''

        if page_name == 'guidebook_detail' and request.session['guidebooks_query'] is not None:
            additional_where = ' AND guidebook_id in ( SELECT t.id as id FROM (' + request.session['guidebooks_query'] + ') as t )'

        return additional_where


class SceneExternalURL(models.Model):
    external_url = models.TextField(default='')

    class Meta:
        ordering = ['external_url']

    def __str__(self):
        return self.external_url

    def short_external_url(self):
        external_url = self.external_url
        if len(external_url) > 30:
            return external_url[0:30] + '...'
        else:
            return external_url


class Scene(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    guidebook = models.ForeignKey(Guidebook, on_delete=models.CASCADE)
    image_key = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    lat = models.FloatField(default=0)
    lng = models.FloatField(default=0)
    point = models.PointField(null=True, blank=True)
    start_x = models.FloatField(default=0.5)
    start_y = models.FloatField(default=0.5)
    sort = models.IntegerField(default=1, null=True)
    image_url = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, default='', null=True, blank=True, verbose_name="Mapillary Username", )

    video_url = models.TextField(default='', blank=True)
    image = models.ImageField(upload_to=scene_image_directory_path, max_length=255, null=True, blank=True, storage=S3Boto3Storage(bucket=settings.AWS_STORAGE_BUCKET_NAME))

    external_url = models.ManyToManyField(SceneExternalURL, blank=True)

    objects = models.Manager()
    vector_tiles = CustomSceneMVTManager(
        geo_col='point',
        select_columns=['image_key', 'unique_id'],
        is_show_id=False,
        source_layer='mtp-scenes'
    )

    def get_poi_count(self):
        points_of_interest = PointOfInterest.objects.filter(scene=self)
        return points_of_interest.count()

    def get_poi_categories(self):
        points_of_interest = PointOfInterest.objects.filter(scene=self)
        categories = []
        if points_of_interest.count() > 0:
            for poi in points_of_interest:
                if poi.category.name not in categories:
                    categories.append(poi.category.name)
        if len(categories) > 0:
            return ', '.join(categories)
        else:
            return ''

    def get_sequence(self):
        sequences = Sequence.objects.filter(coordinates_image__contains=[self.image_key])
        if sequences.count() == 0:
            return None
        else:
            return sequences[0]

    def get_external_urls(self):
        external_urls = self.external_url.all()
        return external_urls


class POIExternalURL(models.Model):
    external_url = models.TextField(default='')

    class Meta:
        ordering = ['external_url']

    def __str__(self):
        return self.external_url

    def short_external_url(self):
        external_url = self.external_url
        if len(external_url) > 30:
            return external_url[0:30] + '...'
        else:
            return external_url


class PointOfInterest(models.Model):
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default='')
    description = models.TextField(default='')
    position_x = models.FloatField(default=0)
    position_y = models.FloatField(default=0)
    category = models.ForeignKey(POICategory, on_delete=models.CASCADE, default=1)
    video_url = models.TextField(default='')
    image = models.ImageField(upload_to=poi_image_directory_path, max_length=255, null=True, blank=True, storage=S3Boto3Storage(bucket=settings.AWS_STORAGE_BUCKET_NAME))

    external_url = models.ManyToManyField(POIExternalURL)


    def __str__(self):
        return self.title

    def get_external_urls(self):
        external_urls = self.external_url.all()
        return external_urls

    def is_exist_image(self):
        return bool(self.image)





