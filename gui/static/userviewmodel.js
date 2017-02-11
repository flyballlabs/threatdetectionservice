function userViewModel() {
    var self = this;

    /* observables */
    self.userName = ko.observable("");
    self.firstName = ko.observable("");
    self.lastName = ko.observable("");
    self.email = ko.observable("");
    self.phone = ko.observable("");
    self.alertLevel = ko.observable("");
    self.alertType = ko.observable("");
    self.companyID = ko.observable("");

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

	/* get user info from api */
    $.ajax({
	url: API_SERVER + "/api/user/mack@goflyball.com",
	dataType: 'json',
	success: function(data) {
			self.firstName(data["firstname"]);
			self.lastName(data["lastname"]);
			self.email(data["email"]);
			self.phone(data["phone_number"]);
			self.alertLevel(data["notification"]["alert_type"]);
    		self.alertType(data["notification"]["notification_type"]);
			self.companyID(data["company_id"]);
		},
	beforeSend: setHeader
    });

	// Call API, Update observable, and animate response
	// TODO: make user / agent object passable instead of hardcoded
    self.onSubmit = function(data, trigger)
    {
    	var route, payload;
    	// conditional data routing depending on trigger
		if (trigger == 'user-profile')
		{
			payload = JSON.stringify(
            {
                firstname : data["firstName"],
				lastname : data["lastName"],
				email : data["email"],
				phone_number : data["phone"]
            });
			route = API_SERVER + "/api/user/mack@goflyball.com"
		}
		else if (trigger == 'alert-settings')
		{
			payload = JSON.stringify(
            {
				notification : {"alert_type":data["alertLevel"],"notification_type":data["alertType"]}
			});
			route = API_SERVER + "/api/user/mack@goflyball.com"
		}
		else if (trigger == 'agent-settings')
		{
			payload = JSON.stringify(
            {
            	mode : data["agentMode"],
				cmd : data["agentCmd"],
				time_setting : {"start_stop":{"start":data["startTime"],"stop":data["stopTime"]},"interval":{"time_sync":data["timesyncInterval"],"update":data["updateInterval"],"discover_assets":data["assetscanInterval"]}}
			});
			route = API_SERVER + "/api/agent/D4:85:64:A3:9A:27"
		}

		$.ajax({
			headers: {'Content-Type' : 'application/json'},
			url: route,
			type: 'PUT',
			data: payload,
			success : function(response, textStatus,jqXhr) {
				self.responseJSON("Updated Successfully");
				var msgBox = document.getElementById("messagebox");
				msgBox.className="bg-primary";
			},
			error : function(response, textStatus,jqXhr) {
				self.responseJSON("Update Failed");
				var msgBox = document.getElementById("messagebox");
				msgBox.className="bg-danger";
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
    ko.applyBindings(new userViewModel());
});
