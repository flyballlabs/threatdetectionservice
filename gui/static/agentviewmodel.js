function agentViewModel() {
    var self = this;

    /* observables */
    self.companyID = ko.observable("");
    self.agentID = ko.observable("");
    self.agentMode = ko.observable("");
	self.agentCmd =	ko.observable("");
	self.startTime = ko.observable("");
	self.stopTime = ko.observable("");
	self.timesyncInterval = ko.observable("");
	self.updateInterval = ko.observable("");
	self.assetscanInterval = ko.observable("");

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
		msgBox.className="bg-primary";
	}

	function displayOnFail(msg) {
		if (msg === undefined) {
			msg = "Update Failed";
		}
		self.responseJSON(msg);
		var msgBox = document.getElementById("messagebox");
		msgBox.className="bg-danger";
    }

	/* get agent info from api */
    $.ajax({
		url: API_SERVER + "/api/agent/D4:85:64:A3:9A:27",
		dataType: 'json',
		success: function(data) {
			self.agentID(data["agent_id"]);
			self.companyID(data["company_id"]);
            self.agentMode(data["mode"]);
            self.agentCmd(data["cmd"]);
            self.startTime(data["time_setting"]["start_stop"]["start"]);
            self.stopTime(data["time_setting"]["start_stop"]["stop"]);
            self.timesyncInterval(data["time_setting"]["interval"]["time_sync"]);
            self.updateInterval(data["time_setting"]["interval"]["update"]);
            self.assetscanInterval(data["time_setting"]["interval"]["discover_assets"]);
		},
		beforeSend: setHeader
    });

	// Call API, Update observable, and animate response
	// TODO: make user / agent object passable instead of hardcoded
    self.onSubmit = function(data) {

    	/* Error checking for improper form submission (bug) */
		if (data["agentMode"] !== "" || data["agentCmd"] !== "" ||
			data["startTime"] !== "" || data["stopTime"] !== "" ||
			data["timesyncInterval"] !== "" || data["updateInterval"] !== "" ||
			data["assetscanInterval"] !== "" ) {/*   pass   */}
		else {return;}

    	var route = API_SERVER + "/api/agent/D4:85:64:A3:9A:27";
    	var payload = JSON.stringify(
        {
            "mode" : data["agentMode"](),
            "cmd" : data["agentCmd"](),
            "time_setting" : {"start_stop":{"start":data["startTime"](),"stop":data["stopTime"]()},"interval":{"time_sync":data["timesyncInterval"](),"update":data["updateInterval"](),"discover_assets":data["assetscanInterval"]()}}
        });

    	/* Error catching */
		if (payload == {}) {
			displayOnFail("Improper data input, try reformatting")
		}

		$.ajax({
			headers: {'Content-Type' : 'application/json'},
			url: route,
			type: 'PUT',
			data: payload,
			contentType: "application/json, text/javascript",
			success : function(response, textStatus,jqXhr) {
				displayOnSuccess();
			},
			error : function(response, textStatus,jqXhr) {
				displayOnFail();
			},
			beforeSend: setHeader
		});
    };// end of onSubmit function
}

/* custom binding function for animations */
// ko.bindingHandlers.fadeInOut = {
//     update: function (element) {
// 		$(element).fadeIn(700);
// 		$(element).fadeOut(700);
//     }
// };

$(document).ready(function() {
	var vm = new agentViewModel();
    ko.applyBindings(vm);
});
