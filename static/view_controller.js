
$(document).ready(function () {
    getFileList();
    fill_dropdown_client();
    set_div_height();

    $(window).resize(function () {
        set_div_height();
    });

    /*
    * this method takes care of the file download
    * when the download button is pressed, the relevant file is downloaded
    * */
    $(document).on("click", ".btn-download",function () {
        $(".img-loading").removeClass("d-none");
        var filename = $(this).closest(".card-body").find(".card-text").html();
        $.ajax({
            'url': 'http://127.0.0.1:5000/get?filename=' + filename,
            'type': 'GET',
            'success': function (data) {
                $(".img-loading").addClass("d-none");
                    setTimeout(function () {
                    alert(get_error_message(data));
                    reload();
                }, 100);

            },
            'error': function (xhr, status, error) {
                alert("errore");
            }
        });
    });

    /*
    * this method takes care of the file upload, after the upload is done the files on the server are displayed
    * */
    $(document).on("click", ".add-file",function (e) {
        $(".img-loading").removeClass("d-none");
        $.ajax({
            'url': 'http://127.0.0.1:5000/put/?filename=' + document.querySelector(".client-files").innerHTML,
            'type': 'GET',
            'success': function (data) {
                $(".img-loading").addClass("d-none");
                    setTimeout(function () {
                    alert(get_error_message(data));
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

/* this method calculates the height of the main div */
function set_div_height() {
    $(".album").css("min-height", $(window).height() - $(".div-main").height() - 98);
}
/* this method fills the dropdown menu with the list of file names on the client */
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
//this method displays the files on the server
function getFileList() {
    $.ajax({
        url: 'http://127.0.0.1:5000/list/',
        type: 'GET',
        success: function (ret) {
            $("#box-file").empty();
            getList(ret).forEach(el =>  addBoxFile(el, ""));
        },
        error: function (xhr, status, error) {
            alert("errore");
        }
    });
}
// this method keeps the selection on the selected file in the dropdown-menu
function change_dropdown_value(el) {
   document.querySelector(".client-files").innerHTML = el.textContent;
}

//converts a string-formatted array, to a real array
function getList(ret) {
    return ret.replaceAll("[", "").replaceAll("]", "").replaceAll("'", "").replaceAll(" ", "").split(",");
}

//this method is used to create a box given a name.
//The box represents a file in the server
function addBoxFile(filename, data) {
    if (filename != "") {
        let div = $(".hide-box").clone().removeClass("d-none hide-box");
        div.find(".card-text").html(filename);
        div.find(".text-muted").html(data);
        $("#box-file").append(div);
}
}

//this method is used to add an item (a file in the client) in the dropdown menu
function addDropdownItem(filename) {
    let item = $(".hide-item-client").clone().removeClass("d-none hide-item-client");
    item.html(filename)
    $(".dropdown-menu-client").append(item);
}

//this method is used to display an message from status code
function get_error_message(result){
    if(result == "0"){
        return "successful operation";
    }else{
        return "errore";
    }
}
//this method is used to reload the page
function reload(){
    window.location.reload();
}