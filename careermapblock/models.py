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
                "<a href=\"" + reverse("edit-careermap-counties",args=[self.id]) + "\">counties</a><br />" + \
                "<a href=\"" + reverse("edit-careermap-county_stat_types",args=[self.id]) + "\">county stat types</a><br />" + \
                "<a href=\"" + reverse("edit-careermap-questions",args=[self.id]) + "\">questions</a>" 
        return EditForm()

    def edit(self,vals,files=None):
        self.description = vals.get('description','')
        self.save()

    def dir(self):
        return dir(self)

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

    def add_county_form(self,request=None):
        return CountyForm(request)

    def update_counties_order(self,county_ids):
        self.set_county_order(county_ids)


    def add_county_stat_type_form(self,request=None):
        return CountyStatTypeForm(request)

    def update_county_stat_type_order(self,county_stat_type_ids):
        self.set_county_order(county_stat_type_ids)

    def default_base_map(self):
        return self.basemap_set.all()[0]
        
        

class CountyStatType(models.Model):
    """County_stat_type
        e.g.
            White person %, Black person %, Foreign Born %, etc.
            many-to-many: basemap.
    """
    cmap = models.ForeignKey(CareerMap)
    name = models.TextField(default="",blank=True,null=True)
    
    class Meta:
        order_with_respect_to = 'cmap'

    def __unicode__(self):
        return self.name or "County ID %d" % self.id

    def dir(self):
        return dir(self)
    
    def edit_form(self,request=None):
      return CountyStatTypeForm(request, instance=self)



        

class BaseMap(models.Model):
    cmap = models.ForeignKey(CareerMap)
        
    name = models.CharField(max_length=256,default="")
    
    #The columns of stats that need to be shown when this base map is selected:
    county_stat_types = models.ManyToManyField ('CountyStatType', blank=True)
   
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


    def dir(self):
        return dir(self)

    def __unicode__(self):
        return self.name or "BaseMap ID %d" % self.id

    def table_of_per_county_stat_types (self):
        """ Return all the stats associated with this basemap """
        return None

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


    def edit_form(self,request=None, files=None):
        the_form =  BaseMapForm(request, files, instance=self)
        the_form.fields['name']   = forms.CharField(initial=self.name)
        the_form.fields['image']  = forms.FileField(label="replace image")
        the_form.fields['county_stat_types'] = forms.ModelMultipleChoiceField(
            queryset=CountyStatType.objects.all(),
            initial = [c.pk for c in CountyStatType.objects.all() if c in  self.county_stat_types.all()]
        )
        return the_form
        
        
class BaseMapForm(forms.ModelForm):   
    class Meta:
        model = BaseMap
        fields = ('name', 'image', 'county_stat_types',)


class Layer(models.Model):
    cmap = models.ForeignKey(CareerMap)
    name = models.CharField(max_length=256,default="")
    color = models.CharField(max_length=16,default="#ff0000")
    
    
    def __unicode__(self):
        return self.name or "Layer ID %d" % self.id

    def dir(self):
        return dir(self)
    
    #The columns of stats that need to be shown when this layer is selected:
    county_stat_types = models.ManyToManyField ('CountyStatType', blank=True)
    
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

    def edit_form(self,request=None, files=None):
        the_form =  LayerForm(request, files, instance=self)
        the_form.fields['name']   = forms.CharField(initial=self.name)
        the_form.fields['image']  = forms.FileField(label="replace image")
        the_form.fields['county_stat_types'] = forms.ModelMultipleChoiceField(
            queryset=CountyStatType.objects.all(),
            initial = [c.pk for c in CountyStatType.objects.all() if c in  self.county_stat_types.all()]
        )
        return the_form


class LayerForm(forms.ModelForm):
    class Meta:
        model = Layer
        fields = ('name', 'color', 'image', 'county_stat_types')


class County(models.Model):
    """County
        e.g. Northwest County. There are 4.   
    """
    
    cmap = models.ForeignKey(CareerMap)
    name = models.TextField(default="",blank=True,null=True)

    class Meta:
        order_with_respect_to = 'cmap'
        verbose_name_plural = "counties"

    def __unicode__(self):
        return self.name or "County ID %d" % self.id

    def dir(self):
        return dir(self)

    def edit_form(self,request=None):
      return CountyForm(request, instance=self)
      
class CountyForm(forms.ModelForm):
    class Meta:
        model = County
        exclude = ("cmap",)
        fields = ('name', )




class CountyStatValue(models.Model):
    """County_stat_value
    currently contained in a simple csv.
    displayed in a table under the map
    foreign_key: county
    foreign_key: county_stat_type
    no need for a real interface for these - it's just a wrapper for a single value. 
    """
    
    def dir(self):
        return dir(self)

    cmap = models.ForeignKey(CareerMap)
    stat_type = models.ForeignKey(CountyStatType)
    county = models.ForeignKey(County)
    value = models.FloatField()
    


                            
                            
class Question(models.Model):
    """ These are just "did you know" questions"""
    
    cmap = models.ForeignKey(CareerMap)
    text = models.TextField(default="",blank=True,null=True)

    layer = models.ForeignKey(Layer, blank=True,null=True)
    basemap = models.ForeignKey(BaseMap, blank=True,null=True)

    class Meta:
        order_with_respect_to = 'cmap'

    def dir(self):
        return dir(self)

    def edit_form(self,request=None):
      return QuestionForm(request, instance=self)

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ("cmap",)
        fields = ('text', 'layer', 'basemap')
        
class CountyStatTypeForm(forms.ModelForm):
    class Meta:
        model = CountyStatType
        exclude = ("cmap",)
        fields = ('name',)
        


