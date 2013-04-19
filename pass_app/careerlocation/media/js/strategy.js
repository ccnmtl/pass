(function (jQuery) {

    window.StrategyView = Backbone.View.extend({
        events: {
            'click .select-layer': 'onSelectLayer',
            'click #toggle_help': 'onToggleHelp',
            'click #toggle_map_layers': 'onToggleMapLayers',
            'click #toggle_map': 'onToggleMap',
            'click div.popover-close a.btn': 'onTogglePopover',
            'click div.strategy-state': 'onShowStrategy',
            'click .cancel': 'onHideStrategy'
        },
        initialize: function(options) {
            _.bindAll(this,
                "initialRender",
                "render",
                "onSelectLayer",
                "onToggleHelp",
                "onToggleMapLayers",
                "onToggleMap",
                "onTogglePopover");
            
            this.strategyTemplate = _.template(jQuery("#strategy-template").html());

            this.layers = new MapLayerList();
            this.layers.fetch();
            
            this.strategies = new StrategyList();
            this.strategies.fetch();
            
            this.state = new UserState({id: options.current_state_id});
            this.state.set("view_type", jQuery("#view_type").html());
            this.state.on('change', this.initialRender);
            this.state.fetch();
        },
        initialRender: function() {
            this.state.off("change", this.initialRender);
            this.state.get("layers").on("add remove", this.render);
            this.render();

            jQuery(this.el).fadeIn();
            
            var strategies = this.state.get('strategies_viewed'); 
            if (strategies.length < 1) {
                jQuery(this.el).find("div.help_content div.popover-close a.btn").html("I got it!");
                this.onToggleHelp();
            }
        },
        toggleOverlay: function() {
            var height = jQuery("div.career_location").outerHeight();
            jQuery("div.career_location_overlay").css("height", height + "px").toggle();
        },
        render: function() {
            var self = this;

            // toggle map layers on/off
            jQuery(".career_location_map_layer").each(function() {
                var dataId = jQuery(this).data("id");
                if (self.state.get("layers").getByDataId(dataId) || self.state.get("view_type") === "BD") {
                    // Check layer box
                    jQuery("#select_layer_" + dataId).attr("checked", "checked");

                    // Display layer & legend
                    jQuery("#map_layer_" + dataId).show();
                    jQuery("#map_legend_" + dataId).show();
                } else {
                    // Uncheck layer box
                    jQuery("#select_layer_" + dataId).removeAttr("checked");

                    // Hide layer
                    jQuery("#map_layer_" + dataId).hide();
                    jQuery("#map_legend_" + dataId).hide();
                }
            });

            var selectedLayers = self.state.get("layers");
            if (selectedLayers.length > 0) {
                jQuery("div.map_legend_container h3").show();
            } else {
                jQuery("div.map_legend_container h3").hide();
            }
            
            if (this.currentStrategy) {
                this.renderStrategy();
            }
            
            var strategies = this.state.get('strategies_viewed');            
            strategies.forEach(function (strategy) {
                var selector = "div.strategy-state[data-id='" + strategy.get('id') + "']";
                jQuery(selector).addClass("viewed");
            });
            
            jQuery(this.el).find("div.help_content a.btn.close").html("Close");
            
            this.maybeUnlock();
        },
        renderStrategy: function() {
            var json = this.currentStrategy.toJSON();

            var markup = this.strategyTemplate(json);
            jQuery("div.strategy").html(markup);

            this.toggleOverlay();
            jQuery("div.strategy").fadeIn("slow");

            this.delegateEvents();
        },
        maybeUnlock: function() {
            // Enable the "next" links if
            // 1. VIEW == "VP" && strategies_viewed == available strategies
            if (this.state.unlockStrategy(this.strategies.length)) {

                var anchor = jQuery("a#next");
                if (anchor.length < 1) {
                    // construct an anchor link
                    var label = jQuery("#next").html();
                    var url = jQuery("#next_url").attr("value");
                    jQuery("#next").replaceWith('<a id="next" class="pager_button" href="' + url + '">' + label + '</a>');

                    // enable the subnav link too
                    var elts = jQuery('#secondary_navigation ul li div.disabled');
                    for (var i = 0; i < elts.length; i++) {
                        var text = jQuery(elts[i]).html().replace(/(\r\n|\n|\r)/gm,"");
                        if (text.trim !== undefined) {
                            text = text.trim();
                        }
                        if (label.search(text) === 0) {
                            jQuery(elts[i]).replaceWith('<div class="regular"><a href="' + url + '">' + text + '</a></div>');
                        }
                    }
                }

                jQuery("#next").show();
            }
        },
        onSelectLayer: function(evt) {
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;
            var layerId = jQuery(srcElement).data("id");

            var isChecked = jQuery(srcElement).attr("checked");

            if (typeof isChecked !== 'undefined' && isChecked !== false) {
                // add to selected layers
                var layer = this.layers.getByDataId(layerId);
                this.state.get("layers").add(layer);
            } else {
                // remove from selected layers
                this.state.get("layers").removeByDataId(layerId);
            }
            this.state.save();
        },
        onToggleHelp: function(evt) {
            this.toggleOverlay();
            jQuery('div.help_content').toggle();
        },
        onToggleMapLayers: function(evt) {
            this.toggleOverlay();
            jQuery('div.map_layer_content').toggle();
        },
        onToggleMap: function(evt) {
            this.toggleOverlay();
            jQuery('div.career_location_map_container').toggle();
        },
        onTogglePopover: function(evt) {
            this.toggleOverlay();

            var srcElement = evt.srcElement || evt.target || evt.originalTarget;
            if (jQuery(srcElement).parents('div.popover-parent').length) {
                jQuery(srcElement).parents('div.popover-parent').toggle();
            } else {
                jQuery(srcElement).parents('div.popover').toggle();
            }
        },
        onShowStrategy: function(evt) {
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;
            var strategyId = jQuery(srcElement).data("id");
            this.currentStrategy = this.strategies.getByDataId(strategyId);
            
            if (!this.state.isStrategySelected(this.currentStrategy)) {
                this.state.selectStrategy(this.currentStrategy);
                this.state.save();
            }

            this.render();
        },
        onHideStrategy: function(evt) {
            var self = this;
            this.toggleOverlay();
            this.currentStrategy = null;
            jQuery("div.strategy").fadeOut("slow", function() {
                jQuery(this).html("");
                self.delegateEvents();
            });
        }
    });
}(jQuery));    