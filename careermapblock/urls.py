from django.conf.urls.defaults import patterns

urlpatterns = patterns('careermapblock.views',
                       (r'^edit_questions/(?P<id>\d+)/$','edit_questions',{},'edit-careermap-questions'),
                       (r'^edit_questions/(?P<id>\d+)/add_question/$','add_question',{},'edit-careermap-add-question'),
                       (r'^edit_question/(?P<id>\d+)/$','edit_question',{},'edit-careermap-question'),
                       (r'^delete_question/(?P<id>\d+)/$','delete_question',{},'delete-careermap-question'),
                       (r'^reorder_questions/(?P<id>\d+)/$','reorder_questions',{},'reorder-careermap-questions'),

                       (r'^edit_layers/(?P<id>\d+)/$','edit_layers',{},'edit-careermap-layers'),
                       (r'^edit_layers/(?P<id>\d+)/add_layer/$','add_layer',{},'edit-careermap-add-layer'),
                       (r'^edit_layer/(?P<id>\d+)/$','edit_layer',{},'edit-careermap-layer'),
                       (r'^delete_layer/(?P<id>\d+)/$','delete_layer',{},'delete-careermap-layer'),
                       (r'^reorder_layers/(?P<id>\d+)/$','reorder_layers',{},'reorder-careermap-layers'),

                       (r'^edit_basemaps/(?P<id>\d+)/$','edit_basemaps',{},'edit-careermap-basemaps'),
                       (r'^edit_basemaps/(?P<id>\d+)/add_basemap/$','add_basemap',{},'edit-careermap-add-basemap'),
                       (r'^edit_basemap/(?P<id>\d+)/$','edit_basemap',{},'edit-careermap-basemap'),
                       (r'^delete_basemap/(?P<id>\d+)/$','delete_basemap',{},'delete-careermap-basemap'),
                       (r'^reorder_basemaps/(?P<id>\d+)/$','reorder_basemaps',{},'reorder-careermap-basemaps'),

)
