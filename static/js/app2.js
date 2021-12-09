let project_name, nav

project_name = JSON.parse(document.getElementById('pn').textContent);
let attr = JSON.parse(document.getElementById('attr').textContent);
console.log(attr)

nav = document.querySelector('.tit')

nav.innerHTML = project_name
let title = document.querySelector('.title')
title.innerHTML = "Welcome to the " + project_name + " Annotation Tool"

document.querySelector('.upload').addEventListener('click',
    function () {
        if (attr === 1){
            document.querySelector('.popup').style.display = 'flex';
        }else {
            $('.errorX').css({'display': 'block'})
        }

    });

document.querySelector('.close').addEventListener('click',
    function () {
        document.querySelector('.popup').style.display = 'none';
    });

$(document).ready(function () {

    $("#sub").click(function () {
        $.ajaxSetup({
            headers: {
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
            }
        });
        let error = $('#upload-error')
        error.css({'display': 'none'})
        let file = $('#batch-file').get(0).files[0]
        // you need to upload a text file
        let filename = file.name
        // you can also check for the size of the file
        // let filesize = file.size
        if (filename.endsWith(".txt")){

            filename = filename.replace('.txt', '')
            let formData = new FormData();
            formData.append('filename', filename)
            formData.append('file', file)
            formData.append('action', 'batch-upload')

            $.ajax({
                method: 'POST',
                url: "",
                data: formData,
                processData: false,
                contentType : false,
                success: function (resp) {
                    document.querySelector('.popup').style.display = 'none';
                },
                error: function (error) {
                    error.css({'display': 'block'})
                    error.html("There was an issue, Please try again later")
                }
            });

        }else {
            error.css({'display': 'block'})
            error.html("You have to upload a text file")
        }

    });

});