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
                alert(get_error_message(data));
            },
            'error': function (xhr, status, error) {
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
                    alert(get_error_message(data))
                    getFileList();
                }, 100);

            },
            'error': function (xhr, status, error) {
                $(".img-loading").addClass("d-none");
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
            var list = getList(data);
            list.forEach(x => addDropdownItem(x))
        },
        'error': function (xhr, status, error) {
            alert("errore");
        }
    });
}
function getFileList() {
    $.ajax({
        url: 'http://127.0.0.1:5000/list/',
        type: 'GET',
        success: function (ret) {
            $("#box-file").empty();
            getList(ret).forEach(function (el) {
                    addBoxFile(el, "");
            });
        },
        error: function (xhr, status, error) {
            alert("errore");
        }
    });
}
function change_dropdown_value(el) {
  var txt = el.textContent;
   document.querySelector(".client-files").innerHTML = txt;
}

function getList(ret) {
    return ret.replaceAll("[", "").replaceAll("]", "").replaceAll("'", "").replaceAll(" ", "").split(",");
}



function addBoxFile(filename, data) {
    if (filename != "") {
        let div = $(".hide-box").clone().removeClass("d-none hide-box");
        div.find(".card-text").html(filename);
        div.find(".text-muted").html(data);
        $("#box-file").append(div);
}
}

function addDropdownItem(filename) {
    let item = $(".hide-item-client").clone().removeClass("d-none hide-item-client");
    item.html(filename)
    $(".dropdown-menu-client").append(item);
}

function get_error_message(result){
    if(result == "0"){
        return "successful operation";
    }else{
        return "errore";
    }
}