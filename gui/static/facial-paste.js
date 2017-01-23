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
            alert("Sucess! Upload completed");
        } else {
            alert("Error! Upload failed");
        }
    };

    xhr.onerror = function() {
        alert("Error! Upload failed. Can not connect to server.");
    };

    xhr.open("POSTileUploader", true);
    xhr.setRequestHeader("Content-Type", file.type);
    xhr.send(file);
}

