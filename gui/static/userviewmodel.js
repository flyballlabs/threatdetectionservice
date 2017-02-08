function userViewModel() {
    var self = this;

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

    /* $.getJSON(API_SERVER + "/api/user/mack@goflyball.com",
            function(data) {
		console.log(data);
                //var parsed = JSON.parse(data);
		//console.log(parsed);
		self.firstName(data["firstname"]);
		self.lastName(data["lastname"]);
		self.email(data["email"]);
                
		//self.firstName(parsed.firstName);
            }
       );
   */

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
			self.companyID = data["company_id"];
		},
	beforeSend: setHeader
    });

    function setHeader(xhr) {
        xhr.setRequestHeader('X-AUTH-TOKEN', AUTH_TOKEN);
      }

    self.responseJSON = ko.observable(null);
    self.onSubmit = function(trigger)
    {
    	var data, route;
    	// conditional data routing depending on trigger
		if (trigger == 'user-profile')
		{
			data = JSON.stringify(
            {
                firstname : self.firstName(),
				lastname : self.lastName(),
				email : self.email(),
				phone : self.phone()
            });
			route = API_SERVER + "/api/user/mack@goflyball.com"
		}
		else if (trigger == 'alert-settings')
		{
			data = JSON.stringify(
            {
				notification : {"alert_type":self.alertLevel,"notification_type":self.alertType}
			});
			route = API_SERVER + "/api/user/mack@goflyball.com"
		}
		else if (trigger == 'agent-settings')
		{
			data = JSON.stringify(
            {
            	agentMode : self.agentMode,
				agentCmd : self.agentCmd,
				time_setting : {"start_stop":{"start":self.startTime,"stop":self.stopTime},"interval":{"time_sync":self.timesyncInterval,"update":self.updateInterval,"discover_assets":self.assetscanInterval}}
			});
			route = API_SERVER + "/api/agent/D4:85:64:A3:9A:27"
		}

         // prepare request data
        //$.patch("http://10.10.10.97:7777/api/user/mack@goflyball.com", data, function(response) // sends 'post' request
       //{
           // on success callback
        //    self.responseJSON = "Updated";
        // })

		$.ajax({ headers : { 'Content-Type' : 'application/json'},
			 url: route,
			 type: 'PUT',
			 data: data,
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
    }
}

$(document).ready(function () {
    ko.applyBindings(new userViewModel());
});
