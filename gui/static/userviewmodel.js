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

	/* Call API, Update observable, and animate response */
	// TODO: make user / agent object passable instead of hardcoded
    self.onSubmit = function(data, event) {

    	/* Error checking for improper form submission (bug) */
		if (data["firstName"] !== "" || data["lastName"] !== "" ||
			data["email"] !== "" || data["phone"] !== "") { // grab calling elem and get id
			var elem = (event.currentTarget) ? event.currentTarget : event.srcElement;
            var trigger = elem.id;
		} else {return;}

        var payload = {};
        var route = API_SERVER + "/api/user/mack@goflyball.com";

		/* If user-profile submitted form */
		if (trigger == "user-profile") {
			payload = JSON.stringify(
			{
				"firstname" : data["firstName"](),
				"lastname" : data["lastName"](),
				"email" : data["email"](),
				"phone_number" : data["phone"]()
			});
		}

		/* If alert-settings submitted form */
		else if (trigger == "alert-settings") {
			payload = JSON.stringify(
			{
				"notification" : {
					"alert_type" : data["alertLevel"](),
					"notification_type" : data["alertType"]()
				}
			});
		}

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
	var vm = new userViewModel();
    ko.applyBindings(vm);
});
