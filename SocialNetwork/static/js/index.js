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

$(document).ready(function() {
    addPost();
    addText();
})