let project_name, cat, nav

project_name = JSON.parse(document.getElementById('pn').textContent);
cat = JSON.parse(document.getElementById('cat').textContent);
nav = document.querySelector('.tit')

nav.innerHTML = project_name
let title = document.querySelector('.title')
title.innerHTML = "Welcome to the " + project_name + " Annotation Tool"

categoryList(cat);

document.getElementById('team').addEventListener('click',
    function () {
       let error = document.getElementById('team-error')
        error.style.display = 'none'
        if(project_name === "[ Your Project Name ]"){
            error.style.display = 'flex'
            error.innerHTML = 'Please first provide your project name'
        }else if (cat.length === 0){
           error.style.display = 'flex'
           error.innerHTML = 'Please first provide at least one category'
       }else {
           document.querySelector('.popup').style.display = 'flex';
       }

    });

document.querySelector('.close').addEventListener('click',
    function () {
        document.querySelector('.popup').style.display = 'none';
    });

$(document).ready(function () {

    $("#name-submit").click(function () {
        $.ajaxSetup({
            headers: {
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
            }
        });

        let name = document.getElementById('name').value
        let error = document.getElementById('name-empty')
        error.style.display = 'none'
        let len = name.split(' ').length;
        if (containsNumbers(name)){
            error.style.display = 'block'
            error.innerHTML = 'Your Project name contains a digit'
        }else {
            if (name.length === 0){
                error.style.display = 'block'
                error.innerHTML = 'Please provide a project name'
            }else if (len >= 4){
                error.style.display = 'block'
                error.innerHTML = 'Your project name should have less than 4 words'
            }else {
                let formData = new FormData();
                formData.append('name', name)
                formData.append('action', 'project_name')

                $.ajax({
                    method: 'POST',
                    url: "",
                    data: formData,
                    processData: false,
                    contentType : false,
                    success: function (resp) {
                        project_name = resp.upload
                        nav.innerHTML = project_name
                        title.innerHTML = "Welcome to the " + project_name + " Annotation Tool"
                    },
                    error: function (error) {
                        error.style.display = 'block'
                        error.innerHTML = 'There was an issue, Please try again later'
                    }
                });
            }
        }

    });

});

function containsNumbers(str){
    let regexp = /\d/g;
    return regexp.test(str);
};

$(document).ready(function () {

    $("#cat-submit").click(function () {
        $.ajaxSetup({
            headers: {
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
            }
        });

        let category = document.getElementById('category').value
        let error = document.getElementById('cat-error')
        error.style.display = 'none'
        if (category.length === 0) {
            error.style.display = 'block'
            error.innerHTML = 'Please provide a category'
        }else {
            let formData = new FormData();
            formData.append('category', category)
            formData.append('action', 'category_name')

            $.ajax({
                method: 'POST',
                url: "",
                data: formData,
                processData: false,
                contentType : false,
                success: function (resp) {
                    cat = resp.upload
                    categoryList(cat)
                },
                error: function (error) {
                    error.style.display = 'block'
                    error.innerHTML = 'There was an issue, Please try again later'
                }
            });
        }

    });

});

function categoryList(data) {
    let div = document.querySelector('.list')
    div.innerHTML = ""
    let ul = document.createElement('ul')
    ul.style = `list-style-type: none;
                margin: 0;
                padding: 0;
                overflow: hidden;`
    let numberOfListItems = data.length
    div.appendChild(ul)
    for (let i = 0; i < numberOfListItems; i++){
        let listItem = document.createElement('li');
        listItem.style = `float: left;
                            margin-right: 5px;
                            margin-top: 5px;
                            background-color: #e7eef1 !important;
                            border-radius: 10px;
                            padding: 5px;
                            font-size: 12px;`
        listItem.innerHTML = data[i];
        ul.appendChild(listItem);
    }
}

