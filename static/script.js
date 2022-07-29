function set_div_height() {
    $(".album").css("min-height", $(window).height() - $(".div-main").height() - 98);
}

$(document).ready(function () {
    getFileList();
    fill_dropdown_client();
     set_div_height();

    $(window).resize(function () {
        set_div_height();
    });

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

    $(document).on("click", ".add-file",function (e) {
        e.preventDefault();
        $(".img-loading").removeClass("d-none");
        $.ajax({
            'url': 'http://127.0.0.1:5000/put/?filename=' + document.querySelector(".client-files").innerHTML,
            'type': 'GET',
            'success': function (data) {
                $(".img-loading").addClass("d-none");
                setTimeout(function () {
                    if (data == "0") {
                        alert("put andato a buon fine")
                    } else {
                        alert("errore");
                    }
                    getFileList();
                }, 100);

            },
            'error': function (xhr, status, error) {
                $(".img-loading").addClass("d-none");
                var err = eval("(" + xhr.responseText + ")");
                alert("errore");
            }
        });
    })

})


function fill_dropdown_client(){
    $.ajax({
        'url': 'http://127.0.0.1:5000/getclient/',
        'type': 'GET',
        'success': function (data) {
            var list = data.replaceAll("[","").replaceAll("]","").replaceAll("'","").replaceAll(" ","").split(",");
            list.forEach(x => addDropdownItem(x))
        },
        'error': function (xhr, status, error) {
            var err = eval("(" + xhr.responseText + ")");
            alert("errore");
        }
    });
}

function change_dropdown_value(el) {
  var txt = el.textContent;
   document.querySelector(".client-files").innerHTML = txt;
}

function getFileList() {
    $.ajax({
        url: 'http://127.0.0.1:5000/list/',
        type: 'GET',
        success: function (ret) {
            $("#box-file").empty();
            var list = ret.replaceAll("[","").replaceAll("]","").replaceAll("'","").replaceAll(" ","").split(",");
            list.forEach(function (el) {
                if(el != "") {
                    addBoxFile(el, "");
                }
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

function addDropdownItem(filename) {
    let item = $(".hide-item-client").clone().removeClass("d-none hide-item-client");
    item.html(filename)
    $(".dropdown-menu-client").append(item);
}
function refreshPage(){
    window.location.reload();
}