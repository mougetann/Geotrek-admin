import logging
import os
from urllib.parse import urljoin
from django.utils.translation import ugettext as _

from django.conf import settings
from django.db.models import Q
from django.contrib.gis.db.models.functions import Transform
from django.http import Http404
from django.views.generic import DetailView
from mapentity.views import (MapEntityCreate,
                             MapEntityUpdate, MapEntityLayer, MapEntityList, MapEntityJsonList,
                             MapEntityDetail, MapEntityDelete, MapEntityViewSet,
                             MapEntityFormat, MapEntityDocument)
from rest_framework import permissions as rest_permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from geotrek.authent.decorators import same_structure_required
from geotrek.common.models import RecordSource, TargetPortal
from geotrek.common.views import DocumentPublic, MarkupPublic
from django.shortcuts import get_object_or_404
from geotrek.trekking.models import Trek

from .filters import TouristicContentFilterSet, TouristicEventFilterSet, TouristicEventApiFilterSet
from .forms import TouristicContentForm, TouristicEventForm
from .models import (TouristicContent, TouristicEvent, TouristicContentCategory, InformationDesk)
from .serializers import (TouristicContentSerializer, TouristicEventSerializer,
                          TouristicContentGeojsonSerializer, TouristicEventGeojsonSerializer,
                          InformationDeskGeojsonSerializer)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

if 'geotrek.diving' in settings.INSTALLED_APPS:
    from geotrek.diving.models import Dive


logger = logging.getLogger(__name__)


class TouristicContentLayer(MapEntityLayer):
    queryset = TouristicContent.objects.existing()
    properties = ['name']
    geometry_field_db = 'geom'


class TouristicContentList(MapEntityList):
    queryset = TouristicContent.objects.existing()
    filterform = TouristicContentFilterSet
    columns = ['id', 'name', 'category']

    @property
    def categories_list(self):
        used = TouristicContent.objects.values_list('category__pk')
        return TouristicContentCategory.objects.filter(pk__in=used)


class TouristicContentJsonList(MapEntityJsonList, TouristicContentList):
    pass


class TouristicContentFormatList(MapEntityFormat, TouristicContentList):
    columns = [
        'id', 'structure', 'eid', 'name', 'category', 'type1', 'type2', 'description_teaser',
        'description', 'themes', 'contact', 'email', 'website', 'practical_info',
        'review', 'published', 'publication_date', 'source', 'portal', 'date_insert', 'date_update',
        'cities', 'districts', 'areas', 'approved'
    ]


class TouristicContentDetail(MapEntityDetail):
    queryset = TouristicContent.objects.existing()

    def get_context_data(self, *args, **kwargs):
        context = super(TouristicContentDetail, self).get_context_data(*args, **kwargs)
        context['can_edit'] = self.get_object().same_structure(self.request.user)
        return context


class TouristicContentCreate(MapEntityCreate):
    model = TouristicContent
    form_class = TouristicContentForm

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super(TouristicContentCreate, self).get_initial()
        try:
            category = int(self.request.GET.get('category'))
            initial['category'] = category
        except (TypeError, ValueError):
            pass
        return initial


class TouristicContentUpdate(MapEntityUpdate):
    queryset = TouristicContent.objects.existing()
    form_class = TouristicContentForm

    @same_structure_required('tourism:touristiccontent_detail')
    def dispatch(self, *args, **kwargs):
        return super(TouristicContentUpdate, self).dispatch(*args, **kwargs)


class TouristicContentDelete(MapEntityDelete):
    model = TouristicContent

    @same_structure_required('tourism:touristiccontent_detail')
    def dispatch(self, *args, **kwargs):
        return super(TouristicContentDelete, self).dispatch(*args, **kwargs)


class TouristicContentDocument(MapEntityDocument):
    queryset = TouristicContent.objects.existing()


class TouristicContentDocumentPublicMixin(object):
    queryset = TouristicContent.objects.existing()

    def get_context_data(self, **kwargs):
        context = super(TouristicContentDocumentPublicMixin, self).get_context_data(**kwargs)
        content = self.get_object()

        context['headerimage_ratio'] = settings.EXPORT_HEADER_IMAGE_SIZE['touristiccontent']

        context['object'] = context['content'] = content
        source = self.request.GET.get('source')
        if source:
            try:
                context['source'] = RecordSource.objects.get(name=source)
            except RecordSource.DoesNotExist:
                pass
        portal = self.request.GET.get('portal', None)

        if portal:
            try:
                context['portal'] = TargetPortal.objects.get(name=portal)
            except TargetPortal.DoesNotExist:
                pass

        return context


class TouristicContentDocumentPublic(TouristicContentDocumentPublicMixin, DocumentPublic):
    pass


class TouristicContentMarkupPublic(TouristicContentDocumentPublicMixin, MarkupPublic):
    pass


class TouristicContentMeta(DetailView):
    model = TouristicContent
    template_name = 'tourism/touristiccontent_meta.html'

    def get_context_data(self, **kwargs):
        context = super(TouristicContentMeta, self).get_context_data(**kwargs)
        context['FACEBOOK_APP_ID'] = settings.FACEBOOK_APP_ID
        context['facebook_image'] = urljoin(self.request.GET['rando_url'], settings.FACEBOOK_IMAGE)
        context['FACEBOOK_IMAGE_WIDTH'] = settings.FACEBOOK_IMAGE_WIDTH
        context['FACEBOOK_IMAGE_HEIGHT'] = settings.FACEBOOK_IMAGE_HEIGHT
        return context


class TouristicEventLayer(MapEntityLayer):
    queryset = TouristicEvent.objects.existing()
    properties = ['name']
    geometry_field_db = 'geom'


class TouristicEventList(MapEntityList):
    queryset = TouristicEvent.objects.existing()
    filterform = TouristicEventFilterSet
    columns = ['id', 'name', 'type', 'begin_date', 'end_date']


class TouristicEventJsonList(MapEntityJsonList, TouristicEventList):
    pass


class TouristicEventFormatList(MapEntityFormat, TouristicEventList):
    columns = [
        'id', 'structure', 'eid', 'name', 'type', 'description_teaser', 'description', 'themes',
        'begin_date', 'end_date', 'duration', 'meeting_point', 'meeting_time',
        'contact', 'email', 'website', 'organizer', 'speaker', 'accessibility',
        'participant_number', 'booking', 'target_audience', 'practical_info',
        'date_insert', 'date_update', 'source', 'portal',
        'review', 'published', 'publication_date',
        'cities', 'districts', 'areas', 'approved'
    ]


class TouristicEventDetail(MapEntityDetail):
    queryset = TouristicEvent.objects.existing()

    def get_context_data(self, *args, **kwargs):
        context = super(TouristicEventDetail, self).get_context_data(*args, **kwargs)
        context['can_edit'] = self.get_object().same_structure(self.request.user)
        return context


class TouristicEventCreate(MapEntityCreate):
    model = TouristicEvent
    form_class = TouristicEventForm


class TouristicEventUpdate(MapEntityUpdate):
    queryset = TouristicEvent.objects.existing()
    form_class = TouristicEventForm

    @same_structure_required('tourism:touristicevent_detail')
    def dispatch(self, *args, **kwargs):
        return super(TouristicEventUpdate, self).dispatch(*args, **kwargs)


class TouristicEventDelete(MapEntityDelete):
    model = TouristicEvent

    @same_structure_required('tourism:touristicevent_detail')
    def dispatch(self, *args, **kwargs):
        return super(TouristicEventDelete, self).dispatch(*args, **kwargs)


class TouristicEventDocument(MapEntityDocument):
    queryset = TouristicEvent.objects.existing()


class TouristicEventDocumentPublicMixin(object):
    queryset = TouristicEvent.objects.existing()

    def get_context_data(self, **kwargs):
        context = super(TouristicEventDocumentPublicMixin, self).get_context_data(**kwargs)
        event = self.get_object()

        context['headerimage_ratio'] = settings.EXPORT_HEADER_IMAGE_SIZE['touristicevent']
        context['object'] = context['event'] = event
        source = self.request.GET.get('source')
        if source:
            try:
                context['source'] = RecordSource.objects.get(name=source)
            except RecordSource.DoesNotExist:
                pass

        portal = self.request.GET.get('portal')
        if portal:
            try:
                context['portal'] = TargetPortal.objects.get(name=portal)
            except TargetPortal.DoesNotExist:
                pass

        return context


class TouristicEventDocumentPublic(TouristicEventDocumentPublicMixin, DocumentPublic):
    pass


class TouristicEventMarkupPublic(TouristicEventDocumentPublicMixin, MarkupPublic):
    pass


class TouristicEventMeta(DetailView):
    model = TouristicEvent
    template_name = 'tourism/touristicevent_meta.html'

    def get_context_data(self, **kwargs):
        context = super(TouristicEventMeta, self).get_context_data(**kwargs)
        context['FACEBOOK_APP_ID'] = settings.FACEBOOK_APP_ID
        context['facebook_image'] = urljoin(self.request.GET['rando_url'], settings.FACEBOOK_IMAGE)
        context['FACEBOOK_IMAGE_WIDTH'] = settings.FACEBOOK_IMAGE_WIDTH
        context['FACEBOOK_IMAGE_HEIGHT'] = settings.FACEBOOK_IMAGE_HEIGHT
        return context


class TouristicContentViewSet(MapEntityViewSet):
    model = TouristicContent
    serializer_class = TouristicContentSerializer
    geojson_serializer_class = TouristicContentGeojsonSerializer
    permission_classes = [rest_permissions.DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        qs = TouristicContent.objects.existing()
        qs = qs.filter(published=True)

        if 'source' in self.request.GET:
            qs = qs.filter(source__name__in=self.request.GET['source'].split(','))

        if 'portal' in self.request.GET:
            qs = qs.filter(Q(portal__name__in=self.request.GET['portal'].split(',')) | Q(portal=None))

        qs = qs.annotate(api_geom=Transform("geom", settings.API_SRID))
        return qs


class TouristicEventViewSet(MapEntityViewSet):
    model = TouristicEvent
    serializer_class = TouristicEventSerializer
    geojson_serializer_class = TouristicEventGeojsonSerializer
    permission_classes = [rest_permissions.DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = TouristicEventApiFilterSet

    def get_queryset(self):
        qs = TouristicEvent.objects.existing()
        qs = qs.filter(published=True)

        if 'source' in self.request.GET:
            qs = qs.filter(source__name__in=self.request.GET['source'].split(','))

        if 'portal' in self.request.GET:
            qs = qs.filter(Q(portal__name__in=self.request.GET['portal'].split(',')) | Q(portal=None))

        qs = qs.annotate(api_geom=Transform("geom", settings.API_SRID))
        return qs


class InformationDeskViewSet(viewsets.ModelViewSet):
    model = InformationDesk
    queryset = InformationDesk.objects.all()
    serializer_class = InformationDeskGeojsonSerializer
    permission_classes = [rest_permissions.DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        qs = super(InformationDeskViewSet, self).get_queryset()
        if self.kwargs.get('type'):
            qs = qs.filter(type_id=self.kwargs['type'])
        qs = qs.annotate(api_geom=Transform("geom", settings.API_SRID))
        return qs


class TrekInformationDeskViewSet(viewsets.ModelViewSet):
    model = InformationDesk
    serializer_class = InformationDeskGeojsonSerializer
    permission_classes = [rest_permissions.DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        pk = self.kwargs['pk']
        trek = get_object_or_404(Trek.objects.existing(), pk=pk)
        return trek.information_desks.all().annotate(api_geom=Transform("geom", settings.API_SRID))


class TrekTouristicContentViewSet(viewsets.ModelViewSet):
    model = TouristicContent
    serializer_class = TouristicContentGeojsonSerializer
    permission_classes = [rest_permissions.DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        trek = get_object_or_404(Trek.objects.existing(), pk=self.kwargs['pk'])
        if not trek.is_public():
            raise Http404
        queryset = trek.touristic_contents.filter(published=True)

        if 'categories' in self.request.GET:
            queryset = queryset.filter(category__pk__in=self.request.GET['categories'].split(','))

        if 'source' in self.request.GET:
            queryset = queryset.filter(source__name__in=self.request.GET['source'].split(','))

        if 'portal' in self.request.GET:
            queryset = queryset.filter(portal__name__in=self.request.GET['portal'].split(','))

        return queryset.annotate(api_geom=Transform("geom", settings.API_SRID))


class TrekTouristicEventViewSet(viewsets.ModelViewSet):
    model = TouristicEvent
    serializer_class = TouristicEventGeojsonSerializer
    permission_classes = [rest_permissions.DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        trek = get_object_or_404(Trek.objects.existing(), pk=self.kwargs['pk'])
        if not trek.is_public():
            raise Http404
        queryset = trek.touristic_events.filter(published=True)

        if 'source' in self.request.GET:
            queryset = queryset.filter(source__name__in=self.request.GET['source'].split(','))

        if 'portal' in self.request.GET:
            queryset = queryset.filter(portal__name__in=self.request.GET['portal'].split(','))

        return queryset.annotate(api_geom=Transform("geom", settings.API_SRID))


if 'geotrek.diving' in settings.INSTALLED_APPS:
    class DiveTouristicContentViewSet(viewsets.ModelViewSet):
        model = TouristicContent
        permission_classes = [rest_permissions.DjangoModelPermissionsOrAnonReadOnly]

        def get_serializer_class(self):
            renderer, media_type = self.perform_content_negotiation(self.request)
            if getattr(renderer, 'format') == 'geojson':
                return TouristicContentGeojsonSerializer
            else:
                return TouristicContentSerializer

        def get_queryset(self):
            dive = get_object_or_404(Dive.objects.existing(), pk=self.kwargs['pk'])
            queryset = dive.touristic_contents.filter(published=True)

            if 'categories' in self.request.GET:
                queryset = queryset.filter(category__pk__in=self.request.GET['categories'].split(','))

            if 'source' in self.request.GET:
                queryset = queryset.filter(source__name__in=self.request.GET['source'].split(','))

            if 'portal' in self.request.GET:
                queryset = queryset.filter(portal__name__in=self.request.GET['portal'].split(','))

            return queryset.annotate(api_geom=Transform("geom", settings.API_SRID))

    class DiveTouristicEventViewSet(viewsets.ModelViewSet):
        model = TouristicEvent
        permission_classes = [rest_permissions.DjangoModelPermissionsOrAnonReadOnly]

        def get_serializer_class(self):
            renderer, media_type = self.perform_content_negotiation(self.request)
            if getattr(renderer, 'format') == 'geojson':
                return TouristicEventGeojsonSerializer
            else:
                return TouristicEventSerializer

        def get_queryset(self):
            dive = get_object_or_404(Dive.objects.existing(), pk=self.kwargs['pk'])

            queryset = dive.touristic_events.filter(published=True)
            if 'source' in self.request.GET:
                queryset = queryset.filter(source__name__in=self.request.GET['source'].split(','))
            if 'portal' in self.request.GET:
                queryset = queryset.filter(portal__name__in=self.request.GET['portal'].split(','))
            return queryset.annotate(api_geom=Transform("geom", settings.API_SRID))


class TouristicCategoryView(APIView):
    """
    touristiccategories.json generation for API
    """
    renderer_classes = (JSONRenderer,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None, lang=None):
        response = []
        content_categories = TouristicContentCategory.objects.all()

        if request.GET.get('categories', False):
            categories = request.GET['categories'].split(',')
            content_categories.filter(pk__in=categories)

        for cont_cat in content_categories:
            response.append({'id': cont_cat.prefixed_id,
                             'label': cont_cat.label,
                             'type1_label': cont_cat.type1_label,
                             'type2_label': cont_cat.type2_label,
                             'pictogram': os.path.join(settings.MEDIA_URL, cont_cat.pictogram.url),
                             'order': cont_cat.order,
                             'slug': 'touristic-content'})

        if request.GET.get('events', False):
            response.append({'id': 'E',
                             'label': _("Touristic events"),
                             'type1_label': "",
                             'type2_label': "",
                             'pictogram': os.path.join(settings.STATIC_URL, 'tourism', 'touristicevent.svg'),
                             'order': None,
                             'slug': 'touristic-event'})

        return Response(response)
