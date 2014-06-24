(function (jQuery) {

    User = Backbone.Model.extend({
        urlRoot: '/_supportservices/api/v1/user/'
    });

    SupportService = Backbone.Model.extend({
        urlRoot: '/_supportservices/api/v1/service/',
        toJSON: function() {
            return this.get('resource_uri');
        },
        toTemplate: function() {
            return _(this.attributes).clone();
        }
    });

    SupportServiceList = Backbone.Collection.extend({
        model: SupportService,
        urlRoot: '/_supportservices/api/v1/service/',
        initialize: function (lst) {
            if (lst !== undefined && lst instanceof Array) {
                for (var i = 0; i < lst.length; i++) {
                    var x = new MapLayer(lst[i]);
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
        }
    });

    UserState = Backbone.Model.extend({
        defaults: {
            services: new SupportServiceList()
        },
        urlRoot: '/_supportservices/api/v1/user_state/',
        parse: function(response) {
            if (response) {
                response.services = new SupportServiceList(response.services);
            }
            return response;
        }
    });
    
    window.SupportServicesView = Backbone.View.extend({
        events: {
            'click .support-service': 'onSelectService'                
        },
        initialize: function(options) {
            _.bindAll(this, 'render');
            
            this.servicesTemplate =
                _.template(jQuery("#services-template").html());
            this.services = new SupportServiceList();
            this.services.on('reset', this.render);
            this.services.fetch({reset: true, processData: true});
            
            /**this.state = new UserState({id: options.user_state_id});
            this.state.on('change', this.render);
            this.state.fetch();**/
        },
        render: function() {
            var context = {
                'services': this.services.toTemplate()
            }
            var markup = this.servicesTemplate(context);
            console.log(markup);
            jQuery(this.el).html(markup);
            this.delegateEvents();
        },
        maybeUnlock: function() {
            var unlock = false;
            
            if (unlock) {
                jQuery("#next").show();
            }
        },
        onSelectService: function(evt) {
        }
    });
    
}(jQuery));