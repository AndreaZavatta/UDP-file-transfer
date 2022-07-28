$(document).ready(function () {
    getFileList();
})

function submitForm() {
    const enc = new TextDecoder("utf-8");
    const fileList = document.getElementById("filePicker").files;
    const fileReader = new FileReader();
    if (fileReader && fileList && fileList.length) {
        fileReader.readAsArrayBuffer(fileList[0]);
        fileReader.onload = function () {
            const imageData = fileReader.result;

            $.ajax({

                'url': 'http://127.0.0.1:5000/upload-file/',
                'type': 'POST',
                'data': {
                    nomefile: document.getElementById("filePicker").files[0].name,
                    contenuto: arrayBufferToBase64(imageData)
                },
                'success': function (data) {
                    if (data == "0") {
                        getFileList();
                    } else {
                        alert("errore");
                    }
                },
                'error': function (xhr, status, error) {
                    var err = eval("(" + xhr.responseText + ")");

                    alert("errore");
                }
            });

        };
    }
}

function getFileList() {
    $.ajax({
        'url': 'http://127.0.0.1:5000/getFileList/',
        'type': 'GET',
        'success': function (list) {
            var obj = JSON.parse(list);
            $("#box-file").empty();
            obj.forEach(function (el) {
                addBoxFile(el.name, el.data);
            });
        },
        'error': function (xhr, status, error) {
            var err = eval("(" + xhr.responseText + ")");
            alert("errore");
        }
    });
}

function arrayBufferToBase64(buffer) {
    var binary = '';
    var bytes = new Uint8Array(buffer);
    var len = bytes.byteLength;
    for ( var i = 0; i < len; i++ ) {
        binary += String.fromCharCode(bytes[i]);
    }
    return window.btoa(binary);
}


function addFile() {
    const filePiecker = document.getElementById("filePicker");
    const name = filePiecker.files.item(0).name;
    $("#file-container").innerHTML += $("#box-file").clone();
}


function addBoxFile(filename, data) {
    let div = $(".hide-box").clone().removeClass("d-none hide-box");
    div.find(".card-text").html(filename);
    div.find(".text-muted").html(data);
    $("#box-file").append(div);

}