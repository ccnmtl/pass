from django.db import models
from pagetree.models import PageBlock
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django import forms
from datetime import datetime
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.conf import settings
from sorl.thumbnail.fields import ImageWithThumbnailsField
import os

class CareerMap(models.Model):
    pageblocks = generic.GenericRelation(PageBlock)
    description = models.TextField(blank=True)
    template_file = "careermapblock/careermapblock.html"
    js_template_file = "careermapblock/careermapblock_js.html"
    css_template_file = "careermapblock/careermapblock_css.html"

    display_name = "Career Map"

    def pageblock(self):
        return self.pageblocks.all()[0]

    def __unicode__(self):
        return unicode(self.pageblock())

    def edit_form(self):
        class EditForm(forms.Form):
            description = forms.CharField(initial=self.description,
                                          widget=forms.widgets.Textarea())
            alt_text = "<a href=\"" + reverse("edit-careermap-basemaps",args=[self.id]) + "\">base maps</a><br />" + \
                "<a href=\"" + reverse("edit-careermap-layers",args=[self.id]) + "\">layers</a><br />" + \
                "<a href=\"" + reverse("edit-careermap-questions",args=[self.id]) + "\">questions</a>" 
        return EditForm()

    def edit(self,vals,files=None):
        self.description = vals.get('description','')
        self.save()

    @classmethod
    def add_form(self):
        class AddForm(forms.Form):
            description = forms.CharField(widget=forms.widgets.Textarea())
        return AddForm()

    @classmethod
    def create(self,request):
        return CareerMap.objects.create(description=request.POST.get('description', ''))

    def needs_submit(self):
        return True

    def submit(self,user,data):
        pass

    def redirect_to_self_on_submit(self):
        return True

    def unlocked(self,user):
        return False

    def add_question_form(self,request=None):
        return QuestionForm(request)

    def update_questions_order(self,question_ids):
        self.set_question_order(question_ids)


    def add_layer_form(self,request=None,files=None):
        return LayerForm(request,files)

    def update_layers_order(self,layer_ids):
        self.set_layer_order(layer_ids)

    def add_basemap_form(self,request=None,files=None):
        return BaseMapForm(request,files)

    def update_basemaps_order(self,basemap_ids):
        self.set_basemap_order(basemap_ids)

    def default_base_map(self):
        return self.basemap_set.all()[0]

class BaseMap(models.Model):
    cmap = models.ForeignKey(CareerMap)
    name = models.CharField(max_length=256,default="")
    image = ImageWithThumbnailsField(upload_to="images/careermapblock/base_maps/%Y/%m/%d",
                                     thumbnail = {
            'size' : (65,65)
            },
                                     extra_thumbnails={
            'admin': {
                'size': (70, 50),
                'options': ('sharpen',),
                }
            })
    class Meta:
        order_with_respect_to = 'cmap'

    def edit_form(self):
        class EditForm(forms.Form):
            image = forms.FileField(label="replace image")
            name = forms.CharField(initial=self.name)
        return EditForm()

    def edit(self,vals,files):
        self.name = vals.get('name','')
        if 'image' in files:
            self.save_image(files['image'])
        self.save()

    def save_image(self,f):
        ext = f.name.split(".")[-1].lower()
        basename = slugify(f.name.split(".")[-2].lower())[:20]
        if ext not in ['jpg','jpeg','gif','png']:
            # unsupported image format
            return None
        now = datetime.now()
        path = "images/careermapblock/base_map/%04d/%02d/%02d/" % (now.year,now.month,now.day)
        try:
            os.makedirs(settings.MEDIA_ROOT + "/" + path)
        except:
            pass
        full_filename = path + "%s.%s" % (basename,ext)
        fd = open(settings.MEDIA_ROOT + "/" + full_filename,'wb')
        for chunk in f.chunks():
            fd.write(chunk)
        fd.close()
        self.image = full_filename
        self.save()


class Layer(models.Model):
    cmap = models.ForeignKey(CareerMap)
    name = models.CharField(max_length=256,default="")
    color = models.CharField(max_length=16,default="#ff0000")
    image = ImageWithThumbnailsField(upload_to="images/careermapblock/layers/%Y/%m/%d",
                                     thumbnail = {
            'size' : (65,65)
            },
                                     extra_thumbnails={
            'admin': {
                'size': (70, 50),
                'options': ('sharpen',),
                }
            })
    class Meta:
        order_with_respect_to = 'cmap'

    def edit_form(self):
        class EditForm(forms.Form):
            image = forms.FileField(label="replace image")
            name = forms.CharField(initial=self.name)
            color = forms.CharField(initial=self.color)
        return EditForm()

    def edit(self,vals,files):
        self.name = vals.get('name','')
        if 'image' in files:
            self.save_image(files['image'])
        self.save()

    def save_image(self,f):
        ext = f.name.split(".")[-1].lower()
        basename = slugify(f.name.split(".")[-2].lower())[:20]
        if ext not in ['jpg','jpeg','gif','png']:
            # unsupported image format
            return None
        now = datetime.now()
        path = "images/careermapblock/layers/%04d/%02d/%02d/" % (now.year,now.month,now.day)
        try:
            os.makedirs(settings.MEDIA_ROOT + "/" + path)
        except:
            pass
        full_filename = path + "%s.%s" % (basename,ext)
        fd = open(settings.MEDIA_ROOT + "/" + full_filename,'wb')
        for chunk in f.chunks():
            fd.write(chunk)
        fd.close()
        self.image = full_filename
        self.save()


class Question(models.Model):
    cmap = models.ForeignKey(CareerMap)
    text = models.TextField(default="",blank=True,null=True)

    class Meta:
        order_with_respect_to = 'cmap'

    def edit_form(self,request=None):
      return QuestionForm(request, instance=self)


class Response:
    question = models.ForeignKey('Question')
    user = models.ForeignKey(User)
    text = models.TextField(default="",blank=True,null=True)

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ("cmap",)
        fields = ('text', )

class LayerForm(forms.ModelForm):
    class Meta:
        model = Layer
        exclude = ("cmap",)
        fields = ('name', 'color', 'image')

class BaseMapForm(forms.ModelForm):
    class Meta:
        model = BaseMap
        exclude = ("cmap",)
        fields = ('name', 'image')
