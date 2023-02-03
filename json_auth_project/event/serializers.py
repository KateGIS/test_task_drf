import datetime

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth.models import Group  # , User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.fields import Field, empty
from rest_framework.relations import MANY_RELATION_KWARGS
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import User
from .models import Tag, Event


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title']


class HiddenField(serializers.Field):
    def __init__(self, **kwargs):
        assert 'default' in kwargs, 'default is a required argument.'
        kwargs['write_only'] = False
        super().__init__(**kwargs)

    def get_value(self, dictionary):
        return empty

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        if not value:
            return None
        return value.email


class ManyTagRelatedField(serializers.ManyRelatedField):
    def to_internal_value(self, data):
        if isinstance(data, str) or not hasattr(data, '__iter__'):
            self.fail('not_a_list', input_type=type(data).__name__)
        valid_data = []
        for item in data:
            if isinstance(item, str) and "," in item:
                valid_data.extend(item.split(","))
            else:
                valid_data.append(item)

        if len(valid_data) == 0:
            self.fail('empty')

        return [
            self.child_relation.to_internal_value(item)
            for item in valid_data
        ]


class TagSlugRelatedField(serializers.SlugRelatedField):
    @classmethod
    def many_init(cls, *args, **kwargs):
        list_kwargs = {'child_relation': cls(*args, **kwargs)}
        for key in kwargs:
            if key in MANY_RELATION_KWARGS:
                list_kwargs[key] = kwargs[key]
        return ManyTagRelatedField(**list_kwargs)


class EventSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(required=False, allow_null=True,
                                           format='%Y-%m-%d %H:%M:%S', )
    # input_formats=['%Y-%m-%d %H:%M:%S',])
    detail = serializers.url = serializers.HyperlinkedIdentityField(view_name='event:event_detail', read_only=True)
    # owner = serializers.SerializerMethodField(method_name="_user")
    owner = HiddenField(default=User.objects.get(email="nikajey.80@gmail.com"))  # serializers.CurrentUserDefault())
    tags = TagSlugRelatedField(many=True, read_only=False, slug_field='title', queryset=Tag.objects.all())

    # tags = TagSerializer(many=True)
    class Meta:
        model = Event
        fields = ['id', 'title', 'owner', 'type_event', 'tags', 'category_event', 'created_at', 'detail']


class EventSerializerDetail(EventSerializer):
    class Meta(EventSerializer.Meta):
        model = EventSerializer.Meta.model
        fields = EventSerializer.Meta.fields[:-1] + ['description']


class EventSerializerUpdate(EventSerializerDetail):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = EventSerializer.Meta.model
        fields = EventSerializerDetail.Meta.fields
