from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django import forms
from .models import Image


class ImageCreateForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {
            'url': forms.HiddenInput,
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        #由于教程上提供的地址被墙，这里提供一个不用翻墙的图片
        # 地址（是个小太阳，亲测可用）：http://1.su.bdimg.com/icon/weather/a0.jpg
        # 这里应该在搜索引擎中搜索图片外链网站，这样你就可用自己传图片到因特网上；
        # 地址二：http://p1.bqimg.com/1949/c2eeb87f73ae3d18.jpg
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not match valid image extensions.')
        return url


    def save(self, force_insert=False, force_update=False, commit=True):
        image = super(ImageCreateForm, self).save(commit=False)
        image_url = self.cleaned_data['url']
        image_name = '{}.{}'.format(slugify(image.title),
                                    image_url.rsplit('.', 1)[1].lower())

        # download image from the given URL
        response = request.urlopen(image_url)
        image.image.save(image_name,
                         ContentFile(response.read()),
                         save=False)

        if commit:
            image.save()
        return image