(function (jQuery) {

    window.CareerLocationView = Backbone.View.extend({
        events: {
            'click .select-layer': 'onSelectLayer',
            'keyup textarea.notepad': 'onChangeNotes',
            'keyup div.answer_content textarea': 'onChangeAnswer',
            'click img.actor': 'onShowActorProfile',
            'click button.interview': 'onShowActorInterview',
            'click .cancel': 'onHideActorProfile',
            'click .ask': 'onAskQuestion',
            'click .done': 'onCloseResponse',
            'click #toggle_help': 'onToggleHelp',
            'click #toggle_map_layers': 'onToggleMapLayers',
            'click #toggle_map': 'onToggleMap',
            'click #toggle_notepad': 'onToggleNotepad',
            'click div.popover-close a.btn.notepad': 'onCloseNotepad',
            'click div.popover-close a.btn': 'onTogglePopover',
            'click div.popover-done button.btn': 'onSubmitBoardQuestion',
            'click div.actor_state.inprogress': 'onShowActorProfile',
            'click div.actor_state.complete': 'onShowActorProfile',
            'click table.location_grid.LC tr td': 'onSelectLocation',
            'mouseover table.location_grid.LC tr td': 'onMouseOverLocation',
            'mouseout table.location_grid.LC tr td': 'onMouseOutLocation'
        },
        initialize: function(options) {
            _.bindAll(this,
                "initialRender",
                "render",
                "renderStakeholderInterview",
                "renderSelectLocation",
                "renderBoardView",
                "onSelectLayer",
                "onChangeNotes",
                "onChangeAnswer",
                "onShowActorProfile",
                "onShowActorInterview",
                "onHideActorProfile",
                "onAskQuestion",
                "onCloseResponse",
                "onToggleHelp",
                "onToggleMapLayers",
                "onToggleMap",
                "onToggleNotepad",
                "onTogglePopover",
                "onSubmitBoardQuestion",
                "onSelectLocation",
                "onMouseOverLocation",
                "onMouseOutLocation");

            this.layers = new MapLayerList(options.layers);            
            
            this.state = new UserState({id: options.current_state_id});
            this.state.set("view_type", jQuery("#view_type").html());
            this.state.on('change', this.initialRender);
            this.state.fetch();

            this.actors = new ActorList(options.actors);
            this.actors.fetch();

            this.profile_template = _.template(jQuery("#profile-template").html());
            this.actor_state_template = _.template(jQuery("#actor-state-template").html());
            this.actor_map_template = _.template(jQuery("#actor-map-template").html());
            this.boardmember_template = _.template(jQuery("#boardmember-template").html());
        },
        initialRender: function() {
            this.state.off("change", this.initialRender);
            this.state.get("layers").on("add remove", this.render);
            this.state.get("actors").on("add", this.render);
            this.state.get("responses").on("add", this.render);
            this.state.on("change:practice_location_row", this.render);
            this.state.on("change:practice_location_column", this.render);

            jQuery("textarea.notepad").html(this.state.get("notes"));

            this.render();

            jQuery(this.el).fadeIn();
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

            if (this.state.get("view_type") === "IV" || this.state.get("view_type") === "LC") {
                this.renderStakeholderInterview();
            }
            if (this.state.get("view_type") === "LC" || this.state.get("view_type") === "BD") {
                this.renderSelectLocation();
            }
            if (this.state.get("view_type") === "BD") {
                this.renderBoardView();
            }
        },
        renderStakeholderInterview: function() {
            var self = this;

            // update selected actor status
            this.state.get('actors').forEach(function (actor) {
                if (actor.get("type") == "IV") {
                    var slots = jQuery("#actor_state_" + actor.get("id"));

                    // replace an empty actor_state state w/this actor
                    var slot;
                    if (slots.length < 1) {
                        slot = jQuery("div.actor_state.empty")[0];
                    } else {
                        slot = slots[0];
                    }

                    var json = actor.toTemplate();
                    json.state = self.state.getActorState(actor);
                    json.asked = self.state.get("responses").getResponsesByActor(actor).length;

                    // update the actor state div on top
                    var markup = self.actor_state_template(json);
                    jQuery(slot).replaceWith(markup);

                    // update the actor state div within the map
                    json.asked = self.state.get("responses").getResponsesByActor(actor).length;
                    markup = self.actor_map_template(json);
                    jQuery("#actor_map_" + actor.get("id")).html(markup);
                }
            });

            jQuery("#selected_actor_count").html(this.state.get("actors").length);
            jQuery("#actors_remaining").html(STAKEHOLDER_LIMIT - this.state.get("actors").length);

            // if an actor is being interviewed, update the question state
            if (this.current_actor) {
                this._updateProfile();
            }
            this.maybeUnlock();
        },
        renderSelectLocation: function() {
            jQuery("table.location_grid tr td").removeClass("selected");
            if (this.state.get("practice_location_row") !== undefined) {
                var selector = "table.location_grid tr:eq(" + this.state.get("practice_location_row") +
                    ") td:eq(" + this.state.get("practice_location_column") + ")";
                jQuery(selector).addClass("selected");
            }
            this.maybeUnlock();
        },
        renderBoardView: function() {
            var boardmembers = jQuery('div.boardmember').sort(function (a, b) {
                var contentA = parseInt(jQuery(a).attr('data-sort'), 10);
                var contentB = parseInt(jQuery(b).attr('data-sort'), 10);
                return (contentA < contentB) ? -1 : (contentA > contentB) ? 1 : 0;
            });

            var complete = 0;

            for (var i = 0; i < boardmembers.length; i++) {
                var b = boardmembers[i];
                var actor = this.actors.getByDataId(jQuery(b).data("id"));
                if (actor !== undefined) {
                    var response = this.state.get("responses").getResponsesByActor(actor);
                    if (response.length > 0) {
                        jQuery(b).removeClass("selected", "fast", function() {
                            jQuery(this).addClass("complete disabled");
                        });
                        complete++;
                    } else {
                        jQuery(b).addClass("selected", "fast", function() {
                            jQuery(this).removeClass("disabled");
                        });

                        var json = actor.toTemplate();
                        var markup = this.boardmember_template(json);
                        jQuery("#boardmember_question").html(markup);

                        setTimeout(function() {
                            var left = jQuery(b).position().left + jQuery(b).width() / 2 - 35;
                            jQuery("#boardmember_question b.notch").css("left", left + "px");

                            jQuery("#boardmember_question .answer_content textarea").focus();

                            jQuery("div.popover-done button.btn").button();
                        }, 100);
                        break;
                    }
                }
            }

            if (complete === BOARDMEMBER_LIMIT) {
                jQuery("#boardmember_question").fadeOut(function() {
                    jQuery("#boardmember_question").html("");
                });
            }

            this.maybeUnlock();
        },
        maybeUnlock: function() {
            // Enable the "next" links if
            // 1. selected_actor_count == STAKEHOLDER_LIMIT
            // 2. each actor has QUESTION_LIMIT questions asked
            if (this.state.unlock()) {
                jQuery("div.basic_instructions").hide();
                jQuery("div.unlock_instructions").show();

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
        onChangeNotes: function(evt) {
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;
            var notes = jQuery(srcElement).val();
            this.state.set("notes", notes);

            // update any other notepads
            jQuery("textarea.notepad").not(srcElement).val(notes);
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
        _updateProfile: function() {
            var json = this.current_actor.toTemplate();
            json.select_stakeholder = !this.state.isActorSelected(this.current_actor);
            json.remaining_stakeholders = STAKEHOLDER_LIMIT - this.state.get("actors").length;
            json.notes = this.state.get("notes");

            json.responses = this.state.get("responses").getResponsesByActor(this.current_actor);
            json.response_count = json.responses.length;
            json.remaining_questions = QUESTION_LIMIT - json.response_count;

            json.asked = this.state.get("responses").getResponsesByActor(this.current_actor).length;

            json.current_question = this.current_question;


            var markup = this.profile_template(json);
            jQuery("div.profile").html(markup);

            this.delegateEvents();
        },
        onShowActorProfile: function(evt) {
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;
            var actorId = jQuery(srcElement).data("id");
            this.current_actor = this.actors.getByDataId(actorId);

            this.render();

            this.toggleOverlay();
            var offset = jQuery("div.interview_state").position();
            jQuery("div.profile").fadeIn("slow");

            this.delegateEvents();
        },
        onShowActorInterview: function(evt) {
            if (!this.state.isActorSelected(this.current_actor)) {
                this.state.selectActor(this.current_actor);
                this.state.save();
            }
        },
        onHideActorProfile: function(evt) {
            var self = this;
            this.state.save();
            this.toggleOverlay();
            this.current_actor = null;
            this.current_question = null;
            jQuery("div.profile").fadeOut("slow", function() {
                jQuery(this).html("");
                self.delegateEvents();
            });
        },
        onAskQuestion: function(evt) {
            var self = this;
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;

            var thisAnswer = jQuery(srcElement).parent().next();
            jQuery(thisAnswer).show('fast');

            this.current_question = this.current_actor.get("questions").getByDataId(jQuery(srcElement).data("id"));

            if (!this.state.isQuestionAnswered(this.current_actor, this.current_question)) {
                jQuery(".btn.ask").attr("disabled", "disabled");
                jQuery(".btn.done").button('loading');
                var response = new ActorResponse();
                response.set("user", this.state.get("user"));
                response.set("actor", this.current_actor);
                response.set("question", this.current_question);

                response.save({}, {
                    success: function(model, response) {
                        self.state.get("responses").add(model);
                        self.state.save();
                        jQuery(".btn.done").removeAttr("disabled");
                    }
                });
            }
        },
        onCloseResponse: function(evt) {
            var self = this;
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;

            this.current_question = null;

            jQuery(srcElement).parents("div.accordion-body").hide('fast');
            jQuery(".btn.ask").removeAttr("disabled");
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
        onToggleNotepad: function(evt) {
            this.toggleOverlay();
            jQuery('div.notepad_content').toggle();
        },
        onCloseNotepad: function(evt) {
            this.state.save();
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
        onMouseOverLocation: function(evt) {
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;
            jQuery(srcElement).addClass("hovered");
        },
        onMouseOutLocation: function(evt) {
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;
            jQuery(srcElement).removeClass("hovered");
        },
        onSelectLocation: function(evt) {
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;
            var row_index = jQuery(srcElement).parent().index('tr');
            var col_index = jQuery(srcElement).index('tr:eq('+row_index+') td');

            // Do this immediately. The whole save state trigger is slow in IE.
            jQuery("table.location_grid tr td").removeClass("selected");
            var selector = "table.location_grid tr:eq(" + row_index +
                ") td:eq(" + col_index + ")";
            jQuery(selector).addClass("selected");

            this.state.set({
                "practice_location_row": row_index,
                "practice_location_column": col_index
            });
            this.state.save();
        },
        onChangeAnswer: function(evt) {
            var answer = jQuery("#boardmember_question").find("div.answer_content textarea").val();
            if (answer.length > 0) {
                jQuery("#boardmember_question div.popover-done .btn").removeClass("disabled");
            } else {
                jQuery("#boardmember_question div.popover-done .btn").addClass("disabled");
            }
        },
        onSubmitBoardQuestion: function(evt) {
            var self = this;
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;
            jQuery(srcElement).button('loading');

            var answer = jQuery("#boardmember_question").find("div.answer_content textarea").val();
            if (answer.length > 0) {
                var actor = this.actors.getByDataId(jQuery(srcElement).data("id"));
                var questionId = jQuery("#boardmember_question").find("div.question_content").data("id");
                var question = actor.get("questions").getByDataId(questionId);

                var response = new ActorResponse();
                response.set("user", this.state.get("user"));
                response.set("actor", actor);
                response.set("question", question);
                response.set("long_response", answer);

                response.save({}, {
                    success: function() {
                        self.state.get("responses").add(response);
                        self.state.selectActor(actor);
                        self.state.save();
                    }
                });
            }
        }
    });
}(jQuery));
