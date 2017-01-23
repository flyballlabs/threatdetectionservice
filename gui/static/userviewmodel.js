function userViewModel() {
    var self = this;
    
    self.firstName = ko.observable("");
    self.lastName = ko.observable("");
    self.email = ko.observable("");
    
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
		},
	beforeSend: setHeader
    });

    function setHeader(xhr) {
        xhr.setRequestHeader('X-AUTH-TOKEN', AUTH_TOKEN);
      }

    self.responseJSON = ko.observable(null);
    self.onSubmit = function() 
    {
        var data = JSON.stringify(
            {
                firstname : self.firstName(),
		lastname : self.lastName(),
		email : self.email()    
            }); // prepare request data
        //$.patch("http://10.10.10.97:7777/api/user/mack@goflyball.com", data, function(response) // sends 'post' request
       //{
           // on success callback
        //    self.responseJSON = "Updated";
        // })

	$.ajax({ headers : { 'Content-Type' : 'application/json'},
		 url: API_SERVER + "/api/user/mack@goflyball.com",
		 type: 'PATCH',
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
		}
	       });
    }
}

$(document).ready(function () {
    ko.applyBindings(new userViewModel());
});
