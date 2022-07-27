
            function submitForm() {
              const enc = new TextDecoder("utf-8");
              const fileList = document.getElementById("filePicker").files;
              const fileReader = new FileReader();
              if (fileReader && fileList && fileList.length) {
                    fileReader.readAsArrayBuffer(fileList[0]);
                    fileReader.onload = function () {
                        const imageData = fileReader.result;

                        $.ajax({

                            'url' : 'http://127.0.0.1:5000/upload-image/',
                            'type' : 'POST',
                            'data' : {
                                nomefile : document.getElementById("filePicker").files[0].name,
                                contenuto: arrayBufferToBase64(imageData)
                            },
                            'success' : function(data) {
                                if (data == "0") {
                                    alert("OK")
                                } else {
                                    alert("errore")
                                }
                            },
                            'error' : function(xhr, status, error)
                            {
                                var err = eval("(" + xhr.responseText + ")");

                                alert("errore");
                            }
                        });

                        };
                   }
                }



function arrayBufferToBase64( buffer ) {
	var binary = '';
	var bytes = new Uint8Array( buffer );
	var len = bytes.byteLength;
	for (var i = 0; i < len; i++) {
		binary += String.fromCharCode( bytes[ i ] );
	}
	return window.btoa( binary );
}


            function addFile(){

                const filePiecker = document.getElementById("filePicker");
                const name = filePiecker.files.item(0).name
               document.getElementById('row').innerHTML+=
                   "            <div class=\"col-md-4\">\n" +
                   "              <div class=\"card mb-4 box-shadow\">\n" +
                   "                <div class=\"card-body\">\n" +
                   "                  <p class=\"card-text\">"+name+".</p>\n" +
                   "                  <div class=\"d-flex justify-content-between align-items-center\">\n" +
                   "                    <div class=\"btn-group\">\n" +
                   "                        <!-- Button trigger modal -->\n" +
                   "                        <button type=\"button\" class=\"btn btn-outline-secondary\" data-toggle=\"modal\" data-target=\"#exampleModal\">\n" +
                   "                          Info\n" +
                   "                        </button>\n" +
                   "            <!-- Modal -->\n" +
                   "                    <div class=\"modal fade\" id=\"exampleModal\" tabindex=\"-1\" role=\"dialog\" aria-labelledby=\"exampleModalLabel\" aria-hidden=\"true\">\n" +
                   "                      <div class=\"modal-dialog\" role=\"document\">\n" +
                   "                        <div class=\"modal-content\">\n" +
                   "                          <div class=\"modal-header\">\n" +
                   "                            <h5 class=\"modal-title\" id=\"exampleModalLabel\">Modal title</h5>\n" +
                   "                            <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\">\n" +
                   "                              <span aria-hidden=\"true\">&times;</span>\n" +
                   "                            </button>\n" +
                   "                          </div>\n" +
                   "                          <div class=\"modal-body\">\n" +
                   "                            info\n" +
                   "                          </div>\n" +
                   "                          <div class=\"modal-footer\">\n" +
                   "                            <button type=\"button\" class=\"btn btn-secondary\" data-dismiss=\"modal\">Close</button>\n" +
                   "                          </div>\n" +
                   "                        </div>\n" +
                   "                      </div>\n" +
                   "                    </div>\n" +
                   "                        <button type=\"button\" class=\"btn btn-outline-secondary\">Download</button>\n" +
                   "                    </div>\n" +
                   "                    <small class=\"text-muted\">9 mins</small>\n" +
                   "                  </div>\n" +
                   "                </div>\n" +
                   "            </div>\n" +
                   "            </div>"
           }