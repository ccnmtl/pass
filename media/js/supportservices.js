(function (jQuery) {

    User = Backbone.Model.extend({
        urlRoot: '/api/v1/user/'
    });

    SupportService = Backbone.Model.extend({
        urlRoot: '/api/v1/service/',
        toJSON: function() {
            return this.get('resource_uri');
        },
        toTemplate: function() {
            return _(this.attributes).clone();
        }
    });

    SupportServiceList = Backbone.Collection.extend({
        model: SupportService,
        urlRoot: '/api/v1/service/',
        initialize: function (lst) {
            if (lst !== undefined && lst instanceof Array) {
                for (var i = 0; i < lst.length; i++) {
                    var x = new SupportService(lst[i]);
                    this.add(x);
                }
            }
        },   
        getByDataId: function(id) {
            var internalId = this.urlRoot + id + '/';
            return this.get(internalId);
        },
        toTemplate: function() {
            var a = [];
            this.forEach(function (item) {
                a.push(item.toTemplate());
            });
            return a;
        },
        comparator: function(service) {
            return [service.get('category').name, service.get('title')]
        }
    });

    UserState = Backbone.Model.extend({
        defaults: {
            services: new SupportServiceList()
        },
        urlRoot: '/api/v1/support_service_state/',
        parse: function(response) {
            if (response) {
                response.services = new SupportServiceList(response.services);
            }
            return response;
        },
        url: function() {
            return this.urlRoot + this.get('id') + '/';
        }
    });
    
    window.SupportServicesView = Backbone.View.extend({
        events: {
            'click .support-service': 'onSelectService',
            'click div.service-description-list button.close': 'onCloseDescription'
        },
        initialize: function(options) {
            _.bindAll(this, 'initialRender', 'render',
                    'onSelectService', 'onCloseDescription');
            
            this.servicesTemplate =
                _.template(jQuery("#services-template").html());
            this.services = new SupportServiceList();
            this.services.on('reset', this.initialRender);
            this.services.fetch({reset: true, processData: true});
            
            this.state = new UserState({id: options.state_id});
            this.state.on('change', this.render);
            
            this.on('render', this.render);
        },
        initialRender: function() {
            var context = {'services': this.services.toTemplate()};
            
            var markup = this.servicesTemplate(context);
            jQuery(this.el).html(markup);
            this.delegateEvents();
            
            this.state.fetch();
        },
        render: function() {
            var selected = this.state.get('services').length;
            var elts = jQuery("ul.support-service-progress li");
            for (var i=0; i < selected; i++) {
                jQuery(elts[i]).addClass("selected");
            }

            this.state.get('services').forEach(function (service) {
                jQuery('[data-service-id="' + service.get('id') + '"]').addClass("selected");
            });
            
            var unlock = this.state.get('services').length === this.services.length;
            
            if (unlock) {
                jQuery("#next").removeClass("disabled");
            } else {
                jQuery("#next").addClass("disabled");
            }
        },
        onCloseDescription: function(evt) {
            jQuery("div.service-description-list div.description").hide();
            jQuery("div.service-description-list").hide();
        },
        onSelectService: function(evt) {
            var self = this;
            var serviceId = jQuery(evt.currentTarget).data('service-id');
            
            if (this.state.get('services').getByDataId(serviceId) === undefined) {
                var service = this.services.getByDataId(serviceId);
                this.state.get('services').add(service, {merge: true});
                this.state.save({}, {
                    success: function() {
                        self.trigger("render");
                }});
            }
            
            self.onCloseDescription();
            jQuery("[data-service-description='" + serviceId + "']").show();
            jQuery("div.service-description-list").show();
        }
    });
    
}(jQuery));