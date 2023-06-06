function addPost() {
    $('#addpost').click(function() {
        document.getElementById('add_photo').show()
    })
}

function addText(){
    $('#select_photo').change(function() {
        var formData = new FormData();

        formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val());
        formData.append('file', document.getElementById('select_photo').files[0]);
        formData.append('formd', true);

        $.ajax('/addpost/', {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': formData,
            'processData': false,
            'contentType': false,
            'success': function(data) {
                document.getElementById('add_img').src = data;
            }
        })

        document.getElementById('add_photo').close()
        document.getElementById('add_text').show()
    })
}

function createPost(){
    $('.submit').click(function(){
      $.ajax('/', {
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            'title': $('#post_title').val(),
            'body': $('#post_text').val()
        },
        'success': function(data){
            window.location.reload();
        }
    })  
    })
}

$(document).ready(function() {
    addPost();
    addText();
    createPost();
})