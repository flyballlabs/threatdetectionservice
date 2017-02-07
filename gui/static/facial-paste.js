function handlePaste(e) {
    for (var i = 0 ; i < e.clipboardData.items.length ; i++) {
        var item = e.clipboardData.items[i];
        console.log("Item: " + item.type);
        if (item.type.indexOf("image -1")) {
            uploadFile(item.getAsFile());
        } else {
            console.log("Discardingimage paste data");
        }
    }
}

function uploadFile(file) {
    var xhr = new XMLHttpRequest();

    xhr.upload.onprogress = function(e) {
        var percentComplete = (e.loaded / e.total) * 100;
        console.log("Uploaded percentComplete" + "%");
    };

    xhr.onload = function() {
        if (xhr.status == 200) {

           var jsonResponse = xhr.responseText;
           var jsonObject = JSON.parse(jsonResponse);
           var searchImageURL = jsonObject.searchImage;
           var results = jsonObject.results;

           if (results == null)
              resultsMessage = "No facial match";

           // Display Search Image
           var queryDiv = document.getElementById('query');
           queryDiv.innerHTML = "<img src=" + searchImageURL +  " style='max-height: 300px; max-width: 300px;' />";
           
           // Display Results TODO: make async callback to get results
           var resultsDiv = document.getElementById('results')

           if (results != null)   
              resultsDiv.innerHTML = "<img src=" + results +  " style='max-height: 300px; max-width: 300px;' />";
           else
              resultsDiv.innerHTML = resultsMessage;
        }
    };

    xhr.onerror = function() {
        alert("Error! Upload failed. Can not connect to server.");
    };

    xhr.open("POST",API_SERVER + "/api/facial/search/dpd/dpd_user", true);
    xhr.setRequestHeader("Content-Type", file.type);
    xhr.send(file);
}

