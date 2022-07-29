$(document).ready(function () {
    getFileList();
})

$(document).on("click", ".btn-download",function () {
    var filename = $(this).closest(".card-body").find(".card-text").html();
    $.ajax({
        'url': 'http://127.0.0.1:5000/get?filename=' + filename,
        'type': 'GET',
        'success': function (data) {
            if (data == "0") {
                alert("download andato a buon fine")
            } else {
                alert("errore");
            }
        },
        'error': function (xhr, status, error) {
            var err = eval("(" + xhr.responseText + ")");
            alert("errore");
        }
    });
});

$(document).on("click", ".add-file",function () {
            $.ajax({
                'url': 'http://127.0.0.1:5000/put?filename='+document.getElementById("filePicker").files[0].name,
                'type': 'POST',
                'success': function (data) {
                    if (data == "0") {
                        alert("put andato a buon fine")
                    } else {
                        alert("errore");
                    }
                },
                'error': function (xhr, status, error) {
                    var err = eval("(" + xhr.responseText + ")");
                    alert("errore");
                }
            });
        })

function getFileList() {
    $.ajax({
        url: 'http://127.0.0.1:5000/list/',
        type: 'GET',
        success: function (ret) {
            $("#box-file").empty();
            var list = ret.replaceAll("[","").replaceAll("]","").replaceAll("'","").replaceAll(" ","").split(",");
            list.forEach(function (el) {
                addBoxFile(el, "");
            });
        },
        error: function (xhr, status, error) {
            var err = eval("(" + xhr.responseText + ")");
            alert("errore");
        }
    });
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