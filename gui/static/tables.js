/* Define view models */
function agentViewModel(agent) {
    self = this;

    self.agentID = ko.observable(agent.agent_id);
    self.macAddress = ko.observable(agent.mac_address);
    self.ipAddress = ko.observable(agent.ip_address);
    self.active = ko.observable(agent.active);
    self.companyID = ko.observable(agent.company_id);
    self.site = ko.observable(agent.site);
    self.mode = ko.observable(agent.mode);
    self.cmd = ko.observable(agent.cmd);
    self.assetscanInterval = ko.observable(agent.time_setting['interval']['discover_assets']);
    self.timesyncInterval = ko.observable(agent.time_setting['interval']['time_sync']);
    self.updateInterval = ko.observable(agent.time_setting['interval']['update']);
    self.startTime = ko.observable(agent.time_setting['start_stop']['start']);
    self.stopTime = ko.observable(agent.time_setting['start_stop']['stop']);
}

function agentTableViewModel() {
    var self = this;

    /* observables */
    self.userName = ko.observable(USER_NAME);
    self.companyAgents = ko.observableArray();

    self.addAgent = function(agent) {
        self.companyAgents.push(new agentViewModel(agent));
    };

    // create agent viewmodels and add them to this root viewmodel
    for (var i = 0; i < COMPANY_AGENTS.length; i++) {
        self.addAgent(COMPANY_AGENTS[i]);
    }

    self.removeAgent = function(agentId) {
        self.companyAgents.push(new agentViewModel(agent));
    };

    self.responseJSON = ko.observable(null);

    /* function for setting auth headers */
    function setHeader(xhr) {
        xhr.setRequestHeader('X-AUTH-TOKEN', AUTH_TOKEN);
    }

    /* functions for displaying info
     *  msg : optional msg to be displayed */
    function displayOnSuccess(msg) {
        if (msg === undefined) {
            msg = "Updated Successfully";
        }
        self.responseJSON(msg);
        var msgBox = document.getElementById("messagebox");
        msgBox.className = "bg-primary";
    }

    function displayOnFail(msg) {
        if (msg === undefined) {
            msg = "Update Failed";
        }
        self.responseJSON(msg);
        var msgBox = document.getElementById("messagebox");
        msgBox.className = "bg-danger";
    }

    /* Route to agent-settings page by id of click */
    self.editAgent = function (data, event) {
        /* grab calling elem and get id */
        var elem = (event.currentTarget) ? event.currentTarget : event.srcElement;
        if (elem.id == null || undefined) {/*   error handling   */
            displayOnFail("There was a problem resolving the agent");
            return;
        } var agentToEdit = elem.id;
        /* find agent in observable array */
        for (agent in self.companyAgents) {
            console.log(agent); // debug
            if (agent["agent_id"]() == agentToEdit) {
                agentToEdit = agent;
            }
        }

    	/*                   Error checking                     */
		if (data["agentMode"]() !== "" || data["agentCmd"]() !== "" ||
			data["startTime"]() !== "" || data["stopTime"]() !== "" ||
			data["timesyncInterval"]() !== "" || data["updateInterval"]() !== "" ||
			data["assetscanInterval"]() !== "" ) {/*   pass   */}
		else { displayOnFail();  return; }

    	var route = "http://0.0.0.0:8888/agent-settings";
    	var payload = JSON.stringify(
        {
            "mode" : data["agentMode"](),
            "cmd" : data["agentCmd"](),
            "time_setting" : {"start_stop":{"start":data["startTime"](),"stop":data["stopTime"]()},"interval":{"time_sync":data["timesyncInterval"](),"update":data["updateInterval"](),"discover_assets":data["assetscanInterval"]()}}
        });

		if (payload == {}) { /*         Error handling          */
			displayOnFail("Improper data input, try reformatting")
		}

        $.ajax({
            headers: {"Content-Type": "application/json"},
            url: route,
            type: "POST",
            data: payload,
            contentType: "application/json, text/javascript",
            success: function(response, textStatus, jqXhr) {
                document.write(response);
                window.location = "/agent-settings";
            },
            error: function(response, textStatus, jqXhr) {
                displayOnFail();
            },
            beforeSend: setHeader
        });
    };// end of onSubmit function

    self.onClickDelete = function(data, event) {
        /* grab calling elem and get id */
        var elem = (event.currentTarget) ? event.currentTarget : event.srcElement;
        if (elem.id == null || undefined) {/*   error handling   */
            displayOnFail("There was a problem resolving the agent");
            return;
        } var agentToDelete = elem.id.replace("agent-edit-button-", "");

        /* find agent in observable array */
        for (agent in COMPANY_AGENTS) {
            console.log(agent);
            if (agent.agent_id == agentToEdit) {
                agentToEdit = agent;
            }
        }
        var route = API_SERVER + "/api/agent/" + agentToDelete.mac_address;

        /* call api and delete agent */
        $.ajax({
            headers: {'Content-Type': 'application/json', 'Accept': 'application/json'},
            url: route,
            type: "DELETE",
            contentType: "application/json, text/javascript",
            success: function(response, textStatus, jqXhr) {
                displayOnSuccess("Successfully deleted Agent.");
            },
            error: function(response, textStatus, jqXhr) {
                displayOnFail();
            },
            beforeSend: setHeader
        });
    }
}

$(document).ready(function() {
    /* minor click handlers */
    $('.sub > a').click(function() {
        $('.sub').find('.current').removeClass('current');
        $(this).addClass('current');
    });
    $('aside > a').click(function() {
        $('aside').find('.current').removeClass('current');
        $(this).addClass('current');
    });
    $('.ntfy i').click(function() {
        $(this).parent().toggleClass('gt').toggleClass('active');
    });

    /* non-stick buttons :) */
    $(".non-stick").mouseup(function() {
        $(this).blur();
    });

    /* disable unusable links */
    $(".non-click").click(function(e) {
        e.preventDefault();
    });

    /* responsive window resizing */
    var x = $('aside').width();
    var margin = '50px 0 0 ' + x + 'px';
    var width = $(window).width() - x;
    $('#main').css({
        margin: margin,
        width: width
    });

    $(window).resize(function() {
        var x = $('aside').width();
        var margin = '50px 0 0 ' + x + 'px';
        var width = $(window).width() - x;
        $('#main').css({
            margin: margin,
            width: width
        });
    }); // end of doc ready function

    /*   delete button click handling   */
    $("button").click(function() {
        if($(this).hasClass("confirm")) {

            $(this).addClass("done");
            $("span").text("Deleted");
        }
        else {
            $(this).addClass("confirm");
            $("span").text("Are you sure?");
        }
    });

    $("button").on('mouseout', function() {
        if($(this).hasClass("confirm") || $(this).hasClass("done")) {
            setTimeout(function(){
                $("button").removeClass("confirm").removeClass("done");
                $("span").text("Delete");
            }, 3000);
        }
    });

    /* register view model */
    var vm = new agentTableViewModel();
    ko.applyBindings(vm);
});
