var templateViewModel = {
    templates: ko.observableArray([
        { name: "info", active: ko.observable(true) },
        { name: "alert", active: ko.observable(false) },
        { name: "agent", active: ko.observable(false) }
    ]),

    activeTemplate: function(templates) {
        return templates.active() ? "active" : "inactive";
    },

    editBasicInfo: function() {
        templateViewModel.templates()[0].active(true);
        templateViewModel.templates()[1].active(false);
        templateViewModel.templates()[2].active(false);

        $("#user-settings li.active".removeClass("active"));
        $("#user-settings #info".addClass("active"));
    },

    editAlerts: function() {
        templateViewModel.templates()[0].active(false);
        templateViewModel.templates()[1].active(true);
        templateViewModel.templates()[2].active(false);

        $("#user-settings li.active".removeClass("active"));
        $("#user-settings #alert".addClass("active"));
    },

    editAgents: function() {
        templateViewModel.templates()[0].active(false);
        templateViewModel.templates()[1].active(false);
        templateViewModel.templates()[2].active(true);

        $("#user-settings li.active".removeClass("active"));
        $("#user-settings #agent".addClass("active"));
    }
};

$(document).ready(function() {
    ko.applyBindings(templateViewModel);
});