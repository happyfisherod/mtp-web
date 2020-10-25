from django import forms

from .models import *


def capture_type():
    objs = CaptureType.objects.all()
    results = []
    for obj in objs:
        results.append([obj.name, obj.name])
    return results


def capture_method():
    objs = CaptureMethod.objects.all()
    results = []
    for obj in objs:
        results.append([obj.name, obj.name])
    return results


def image_quality():
    objs = ImageQuality.objects.all()
    results = []
    for obj in objs:
        results.append([obj.name, obj.name])
    return results


class PhotographerForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'data-validation': 'required'}),
                           required=False)

    business_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'data-validation': 'required'}), required=False)
    business_website = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'data-validation': 'url'}), required=False)
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'data-validation': 'required'}),
        required=False)
    capture_type = None
    capture_method = None
    image_quality = None
    geometry = forms.CharField(widget=forms.Textarea(attrs={'class': 'd-none'}), label='', required=False)
    zoom = forms.CharField(widget=forms.TextInput(attrs={'class': 'd-none'}), label='', required=False)

    is_published = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={'class': 'd-none', 'disabled': 'disabled'}),
        choices=(('True', 'Published'), ('False', 'Unpublished'))
        , required=False, label='')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['capture_type'] = forms.ModelMultipleChoiceField(
            required=False,
            widget=forms.SelectMultiple(
                attrs={'class': 'form-control'}
            ),
            queryset=CaptureType.objects.all()
        )

        self.fields['capture_method'] = forms.ModelMultipleChoiceField(
            required=False,
            widget=forms.SelectMultiple(
                attrs={'class': 'form-control'}
            ),
            queryset=CaptureMethod.objects.all()
        )

        self.fields['image_quality'] = forms.ModelMultipleChoiceField(
            required=False,
            widget=forms.SelectMultiple(
                attrs={'class': 'form-control'}
            ),
            queryset=ImageQuality.objects.all()
        )

    class Meta:
        model = Photographer
        fields = (
            # 'user_id',
            'name',
            'business_name',
            'business_website',
            'geometry',
            'description',
            'capture_type',
            'capture_method',
            'image_quality',
            'zoom',
            'is_published'
        )


class PhotographerSearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['capture_type'] = forms.MultipleChoiceField(
            required=False,
            widget=forms.SelectMultiple(
                attrs={'class': 'form-control'}
            ),
            choices=capture_type()
        )

        self.fields['capture_method'] = forms.MultipleChoiceField(
            required=False,
            widget=forms.SelectMultiple(
                attrs={'class': 'form-control'}
            ),
            choices=capture_method()
        )

        self.fields['image_quality'] = forms.MultipleChoiceField(
            required=False,
            widget=forms.SelectMultiple(
                attrs={'class': 'form-control'}
            ),
            choices=image_quality()
        )


class PhotographerEnquireForm(forms.ModelForm):
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'data-validation': 'required'}),
                              required=False)
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'data-validation': 'required'}),
        required=False)

    class Meta:
        model = PhotographerEnquire
        fields = (
            'subject',
            'description',
        )
