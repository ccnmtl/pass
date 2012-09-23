(function (jQuery) {

    var QUESTION_LIMIT = 3;
    var STAKEHOLDER_LIMIT = 4;

    var User = Backbone.Model.extend({
        urlRoot: '/_careerlocation/api/v1/user/'
    });

    var MapLayer = Backbone.Model.extend({
        urlRoot: '/_careerlocation/api/v1/map_layer/'
    });

    var MapLayerList = Backbone.Collection.extend({
        model: MapLayer,
        urlRoot: '/_careerlocation/api/v1/map_layer/',
        getByDataId: function(id) {
            var internalId = this.urlRoot + id + '/';
            return this.get(internalId);
        },
        removeByDataId: function(id) {
            var internalId = this.urlRoot + id + '/';
            this.remove(internalId);
        }
    });

    var ActorQuestion = Backbone.Model.extend({
        urlRoot: '/_careerlocation/api/v1/actor_question/'
    });

    var ActorQuestionList = Backbone.Collection.extend({
        model: ActorQuestion,
        urlRoot: '/_careerlocation/api/v1/actor_question/',
        getByDataId: function(id) {
            var internalId = this.urlRoot + id + '/';
            return this.get(internalId);
        }
    });

    var Actor = Backbone.Model.extend({
        urlRoot: '/_careerlocation/api/v1/actor/',
        defaults: {
            questions: new ActorQuestionList()
        },
        parse: function(response) {
            if (response) {
                response.questions = new ActorQuestionList(response.questions);
            }
            return response;
        },
        toJSON: function() {
            var json = _.clone(this.attributes);
            _.each(json, function(value, name) {
                if (value !== null && _.isFunction(value.toJSON)) {
                    json[name] = value.toJSON();
                }
            });
            return json;
        }
    });

    var ActorList = Backbone.Collection.extend({
        model: Actor,
        urlRoot: '/_careerlocation/api/v1/actor/',
        getByDataId: function(id) {
            var internalId = this.urlRoot + id + '/';
            return this.get(internalId);
        },
        parse: function(response) {
            return response.objects || response;
        }
    });

    var ActorResponse = Backbone.Model.extend({
        defaults: {
            actor: new Actor(),
            question: new ActorQuestion()
        },
        urlRoot: '/_careerlocation/api/v1/actor_response/',
        initialize: function(attrs) {
            if (attrs) {
                this.set("actor", new Actor(attrs.actor));
                this.set("question", new ActorQuestion(attrs.question));
            }
        },
        parse: function(response) {
            if (response) {
                response.actor = new Actor(response.actor);
                response.question = new ActorQuestion(response.question);
            }
            return response;
        }
    });

    var ActorResponseList = Backbone.Collection.extend({
        model: ActorResponse,
        urlRoot: '/_careerlocation/api/v1/actor_response/',
        getResponsesByActor: function(actor) {
            var responses = [];
            this.forEach(function(obj) {
                if (actor.get("id") === obj.get("actor").get("id")) {
                    responses.push(obj);
                }
            });
            return responses;
        },
        parse: function(response) {
            return response.objects || response;
        }
    });

    var UserState = Backbone.Model.extend({
        defaults: {
            layers: new MapLayerList(),
            actors: new ActorList(),
            responses: new ActorResponseList(),
            notes: ""
        },
        urlRoot: '/_careerlocation/api/v1/career_location_state/',
        parse: function(response) {
            if (response) {
                response.layers = new MapLayerList(response.layers);
                response.actors = new ActorList(response.actors);
                response.responses = new ActorResponseList(response.responses);
            }
            return response;
        },
        selectActor: function(actor) {
            this.get("actors").add(actor);
        },
        isActorSelected: function(actor) {
            var obj = this.get("actors").getByDataId(actor.get('id'));
            return typeof obj !== 'undefined' && obj !== null;
        },
        getActorState: function(actor) {
            if (!this.isActorSelected(actor)) {
                return "unselected";
            }

            var responses = this.get("responses").getResponsesByActor(actor);
            if (responses.length >= QUESTION_LIMIT) {
                return "complete";
            } else {
                return "inprogress";
            }
        },
        isQuestionAnswered: function(actor, question) {
            var answered = false;
            this.get("responses").forEach(function(response) {
                if (response.get("actor").get("id") === actor.get("id") &&
                    response.get("question").get("id") === question.get("id")) {
                    answered = true;
                }
            });
            return answered;
        },
        unlock: function() {
            if (this.get("actors").length < 4) {
                return false;
            }

            var unlock = true;
            var allResponses = this.get("responses");

            this.get("actors").forEach(function(actor) {
                var responses = allResponses.getResponsesByActor(actor);
                if (responses.length < 3) {
                    unlock = false;
                }
            });
            return unlock;
        }

    });

    window.CareerLocationView = Backbone.View.extend({
        events: {
            'click .select-layer': 'onSelectLayer',
            'keyup textarea.notepad': 'onChangeNotes',
            'click img.actor': 'onShowActorProfile',
            'click button.interview': 'onShowActorInterview',
            'click .cancel': 'onHideActorProfile',
            'click .ask': 'onAskQuestion',
            'click .done': 'onCloseResponse'
        },
        initialize: function(options) {
            _.bindAll(this,
                "initialRender",
                "render",
                "onSelectLayer",
                "onChangeNotes",
                "onShowActorProfile",
                "onShowActorInterview",
                "onHideActorProfile",
                "onAskQuestion");

            this.state = new UserState({id: options.current_state_id});
            this.state.on('change', this.initialRender);
            this.state.fetch();

            this.layers = new MapLayerList();
            this.layers.fetch();

            this.actors = new ActorList();
            this.actors.fetch();

            this.profile_template = _.template(jQuery("#profile-template").html());
        },
        initialRender: function() {
            this.state.off("change", this.initialRender);
            this.state.get("layers").on("add remove", this.render);
            this.state.get("actors").on("add", this.render);
            this.state.get("responses").on("add", this.render);

            jQuery("textarea.notepad").html(this.state.get("notes"));

            this.render();
            jQuery(this.el).fadeIn();
        },
        render: function() {
            var self = this;

            // toggle map layers on/off
            jQuery(".career_location_map_layer").each(function() {
                var dataId = jQuery(this).data("id");
                if (self.state.get("layers").getByDataId(dataId)) {
                    // Check layer box
                    jQuery("#select_layer_" + dataId).attr("checked", "checked");

                    // Display layer
                    jQuery("#map_layer_" + dataId).show();
                } else {
                    // Uncheck layer box
                    jQuery("#select_layer_" + dataId).removeAttr("checked");

                    // Hide layer
                    jQuery("#map_layer_" + dataId).hide();
                }
            });

            // update selected actor status
            this.state.get('actors').forEach(function (actor) {
                var slots = jQuery("#actor_state_" + actor.get("id"));

                // replace an empty actor_state state w/this actor
                if (slots.length < 1) {
                    slots = jQuery("div.actor_state.empty");
                    var markup = '<img src="' + actor.get("image") + '"></img>';
                    jQuery(slots[0])
                        .attr("id", "actor_state_" + actor.get("id"))
                        .html(markup)
                        .removeClass("empty");
                }

                // always update state
                jQuery(slots[0]).removeClass("inprogress").addClass(self.state.getActorState(actor));
            });

            jQuery("#selected_actor_count").html(this.state.get("actors").length);
            jQuery("#actors_remaining").html(STAKEHOLDER_LIMIT - this.state.get("actors").length);

            // if an actor is being interviewed, update the question state
            if (this.current_actor) {
                this._updateProfile();
            }


            // Enable the "next" links if
            // 1. selected_actor_count == 4
            // 2. each actor has 3 questions asked
            if (this.state.unlock()) {
                var anchor = jQuery("a#next");
                if (anchor.length < 1) {
                    // construct an anchor link
                    var label = jQuery("span#next").html();
                    var url = jQuery("#next_url").attr("value");
                    jQuery("span#next").replaceWith('<a id="next" href="' + url + '">' + label + '</a>');

                    // enable the subnav link too
                    var elts = jQuery('#secondary_navigation ul li div.disabled');
                    for (var i = 0; i < elts.length; i++) {
                        var text = jQuery(elts[i]).html().replace(/(\r\n|\n|\r)/gm,"").trim();
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
            this.state.save();

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
            var json = this.current_actor.toJSON();
            json.select_stakeholder = !this.state.isActorSelected(this.current_actor);
            json.remaining_stakeholders = STAKEHOLDER_LIMIT - this.state.get("actors").length;
            json.notes = this.state.get("notes");

            json.responses = this.state.get("responses").getResponsesByActor(this.current_actor);
            json.response_count = json.responses.length;
            json.remaining_questions = QUESTION_LIMIT - json.response_count;

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

            var offset = jQuery(srcElement).parent().position();
            jQuery("div.profile")
                .css({
                    left: offset.left + "px",
                    top: offset.top - 50 + "px"
                })
                .fadeIn("slow");

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
            jQuery("div.profile").fadeOut("slow", function() {
                jQuery(this).html("");
                self.current_actor = null;
                self.delegateEvents();
            });
        },
        onAskQuestion: function(evt) {
            var self = this;
            var srcElement = evt.srcElement || evt.target || evt.originalTarget;

            var thisAnswer = jQuery(srcElement).parent().next();
            jQuery(thisAnswer).show('fast');
            jQuery(".btn.ask").attr("disabled", "disabled");

            this.current_question = this.current_actor.get("questions").getByDataId(jQuery(srcElement).data("id"));

            if (!this.state.isQuestionAnswered(this.current_actor, this.current_question)) {
                var response = new ActorResponse();
                response.set("user", this.state.get("user"));
                response.set("actor", this.current_actor);
                response.set("question", this.current_question);

                response.save({}, {
                    success: function() {
                        self.state.get("responses").add(response);
                        self.state.save();
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
        }
    });
}(jQuery));
