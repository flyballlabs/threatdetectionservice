function agentViewModel() {
    var self = this;

    /* observables */
    self.agentID = ko.observable("");
    self.macAddress = ko.observable(AGENT);
    self.ipAddress = ko.observable("");
    self.active = ko.observable("");
    self.companyID = ko.observable("");
    self.site = ko.observable("");
    self.mode = ko.observable("");
    self.cmd = ko.observable("");
    self.assetscanInterval = ko.observable("");
    self.timesyncInterval = ko.observable("");
    self.updateInterval = ko.observable("");
    self.startTime = ko.observable("");
    self.stopTime = ko.observable("");

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

    route = API_SERVER + "/api/agent/" + AGENT;
	$.ajax({ /* get agent info from api using passed in mac_address */
		url: route,
		dataType: 'json',
		contentType: "application/json, text/javascript",
		headers: {'Accept' : 'application/json'},
		success: function(data) {
			self.agentID(data["agent_id"]);
			self.ipAddress(data["ip_address"]);
			self.active(data["active"]);
			self.companyID(data["company_id"]);
			self.site(data["site"]);
			self.mode(data["mode"]);
			self.cmd(data["cmd"]);
			self.startTime(data["time_setting"]["start_stop"]["start"]);
			self.stopTime(data["time_setting"]["start_stop"]["stop"]);
			self.timesyncInterval(data["time_setting"]["interval"]["time_sync"]);
			self.updateInterval(data["time_setting"]["interval"]["update"]);
			self.assetscanInterval(data["time_setting"]["interval"]["discover_assets"]);
		},
		beforeSend: setHeader
	});

	// Call API, Update observable, and animate response
    self.onSubmit = function(data) {

    	/* Error checking for improper form submission (bug) */
		if (data["agentMode"] !== undefined || data["agentCmd"] !== undefined ||
			data["startTime"] !== undefined || data["stopTime"] !== undefined ||
			data["timesyncInterval"] !== undefined || data["updateInterval"] !== undefined ||
			data["assetscanInterval"] !== undefined || data["companyID"] !== undefined ||
			data["ipAddress"] !== undefined || data["active"] !== undefined) {/*   pass   */}
		else { return; }

    	var route = API_SERVER + "/api/agent/" + AGENT;
    	var payload = JSON.stringify(
        {
        	"agent_id" : data["agentID"](),
			"mac_address" : self.macAddress(),
			"ip_address" : data["ipAddress"](),
			"active" : data["active"](),
			"company_id" : data["companyID"](),
			"site" : data["site"](),
            "mode" : data["mode"](),
            "cmd" : data["cmd"](),
            "time_setting" : {"start_stop":{"start":data["startTime"](),"stop":data["stopTime"]()},"interval":{"time_sync":data["timesyncInterval"](),"update":data["updateInterval"](),"discover_assets":data["assetscanInterval"]()}}
        });

    	/* Error catching */
		if (payload == {}) {
			displayOnFail("Improper data input, try reformatting")
		}

		$.ajax({
			headers: {'Content-Type' : 'application/json',
					  		'Accept' : 'application/json'},
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
