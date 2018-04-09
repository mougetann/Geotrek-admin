from django import forms
from django.conf import settings
from geotrek.common.forms import CommonForm
from geotrek.core.forms import TopologyForm

from leaflet.forms.widgets import LeafletWidget

from .models import Infrastructure
from django.utils.translation import ugettext_lazy as _

if settings.TREKKING_TOPOLOGY_ENABLED:
    class BaseInfrastructureForm(TopologyForm):
        implantation_year = forms.IntegerField(label=_("Implantation year"), required=False)

        class Meta(TopologyForm.Meta):
            fields = TopologyForm.Meta.fields + \
                ['structure', 'name', 'description', 'type', 'condition', 'implantation_year', 'published']
else:
    class BaseInfrastructureForm(CommonForm):
        implantation_year = forms.IntegerField(label=_("Implantation year"), required=False)
        geomfields = ['geom']

        def __init__(self, *args, **kwargs):
            super(BaseInfrastructureForm, self).__init__(*args, **kwargs)
            modifiable = self.fields['geom'].widget.modifiable
            self.fields['geom'].widget = LeafletWidget(attrs={'geom_type': 'POINT'})
            self.fields['geom'].widget.modifiable = modifiable

        class Meta(CommonForm.Meta):
            model = Infrastructure
            fields = CommonForm.Meta.fields + ['geom', 'structure', 'name', 'description', 'type', 'condition',
                                               'implantation_year', 'published']


class InfrastructureForm(BaseInfrastructureForm):
    class Meta(BaseInfrastructureForm.Meta):
        model = Infrastructure
