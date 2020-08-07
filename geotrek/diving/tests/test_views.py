from django.urls import reverse
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

from geotrek.authent.models import Structure
from geotrek.common.tests import CommonLiveTest, CommonTest
from geotrek.diving.models import Dive
from geotrek.diving.factories import DiveFactory, DivingManagerFactory, PracticeFactory

from mapentity.factories import SuperUserFactory


class DiveViewsTests(CommonTest):
    model = Dive
    modelfactory = DiveFactory
    userfactory = DivingManagerFactory
    expected_json_geom = {
        'type': 'Point',
        'coordinates': [-1.3630812, -5.9838563],
    }

    def get_expected_json_attrs(self):
        return {
            'advice': '',
            'category': {
                'id': 'D{}'.format(self.obj.practice.id),
                'label': 'Practice',
                'order': None,
                'pictogram': '/media/upload/dummy_img.png',
                'slug': self.obj.practice.slug,
            },
            'departure': '',
            'depth': None,
            'description': '',
            'description_teaser': '',
            'difficulty': None,
            'disabled_sport': '',
            'dives': [],
            'eid': None,
            'facilities': '',
            'filelist_url': '/paperclip/get/diving/dive/{}/'.format(self.obj.pk),
            'files': [],
            'levels': [],
            'map_image_url': '/image/dive-{}-en.png'.format(self.obj.pk),
            'name': 'Dive',
            'owner': '',
            'pictures': [],
            'pois': [],
            'portal': [],
            'practice': {
                'id': self.obj.practice.pk,
                'label': 'Practice',
                'pictogram': '/media/upload/dummy_img.png'
            },
            'printable': '/api/en/dives/{}/dive.pdf'.format(self.obj.pk),
            'publication_date': '2020-03-17',
            'published': True,
            'published_status': [
                {'lang': 'en', 'language': 'English', 'status': True},
                {'lang': 'es', 'language': 'Spanish', 'status': False},
                {'lang': 'fr', 'language': 'French', 'status': False},
                {'lang': 'it', 'language': 'Italian', 'status': False}
            ],
            'slug': self.obj.slug,
            'source': [],
            'themes': [],
            'thumbnail': None,
            'touristic_contents': [],
            'touristic_events': [],
            'treks': [],
            'videos': [],
        }

    def setUp(self):
        super(DiveViewsTests, self).setUp()

    def get_bad_data(self):
        return {
            'geom': 'doh!'
        }, _('Invalid geometry value.')

    def get_good_data(self):
        return {
            'structure': Structure.objects.first().pk,
            'name_en': 'test',
            'practice': PracticeFactory.create().pk,
            'geom': '{"type": "Point", "coordinates":[0, 0]}',
        }

    def test_services_on_treks_do_not_exist(self):
        self.login()
        self.modelfactory.create()
        response = self.client.get(reverse('diving:dive_service_geojson', kwargs={'lang': translation.get_language(), 'pk': 0}))
        self.assertEqual(response.status_code, 404)

    def test_services_on_treks_not_public(self):
        self.login()
        dive = self.modelfactory.create(published=False)
        response = self.client.get(reverse('diving:dive_service_geojson', kwargs={'lang': translation.get_language(), 'pk': dive.pk}))
        self.assertEqual(response.status_code, 404)

    def test_pois_on_treks_do_not_exist(self):
        self.login()
        self.modelfactory.create()
        response = self.client.get(reverse('diving:dive_poi_geojson', kwargs={'lang': translation.get_language(), 'pk': 0}))
        self.assertEqual(response.status_code, 404)

    def test_pois_on_treks_not_public(self):
        self.login()
        dive = self.modelfactory.create(published=False)
        response = self.client.get(reverse('diving:dive_poi_geojson', kwargs={'lang': translation.get_language(), 'pk': dive.pk}))
        self.assertEqual(response.status_code, 404)

    def test_bbox_filter(self):
        class DiveGoodGeomFactory(DiveFactory):
            geom = 'Point(700000 6600000)'

        self.modelfactory = DiveGoodGeomFactory
        super(DiveViewsTests, self).test_bbox_filter()


class DiveViewsLiveTests(CommonLiveTest):
    model = Dive
    modelfactory = DiveFactory
    userfactory = SuperUserFactory
