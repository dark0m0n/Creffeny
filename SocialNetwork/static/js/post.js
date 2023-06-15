function addComment(){
    $('#add').click(function(){
        let btn = $(this);
        $.ajax(btn.data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'text': $('#id_body').val()
            },
            'success': function(data){
                document.getElementById('comments').innerHTML += data;
            }
        })
    })
}

function addLike(){
    $('#like').click(function(){
        let btn = $(this);
        $.ajax(btn.data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'like': 1
            },
            'success': function(data){
                document.getElementById('likes').innerHTML = data['like_amount'];
                document.getElementById('dislikes').innerHTML = data['dislike_amount'];
                if (data['is_like'] == 1){
                    document.getElementById('like_img').src = '/static/icons/like_on.png';
                }else{
                    document.getElementById('like_img').src = '/static/icons/like_off.png';
                }
                if (data['is_dislike'] == 1){
                    document.getElementById('dislike_img').src = '/static/icons/dislike_on.png';
                }else{
                    document.getElementById('dislike_img').src = '/static/icons/dislike_off.png';
                }
            }
        })
    })
}

function addDisike(){
    $('#dislike').click(function(){
        let btn = $(this);
        $.ajax(btn.data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'dislike': 1
            },
            'success': function(data){
                document.getElementById('likes').innerHTML = data['like_amount'];
                document.getElementById('dislikes').innerHTML = data['dislike_amount'];
                if (data['is_dislike'] == 1){
                    document.getElementById('dislike_img').src = '/static/icons/dislike_on.png';
                }else{
                    document.getElementById('dislike_img').src = '/static/icons/dislike_off.png';
                }
                if (data['is_like'] == 1){
                    document.getElementById('like_img').src = '/static/icons/like_on.png';
                }else{
                    document.getElementById('like_img').src = '/static/icons/like_off.png';
                }
            }
        })
    })
}

function addPost() {
    $('#addpost').click(function() {
        document.getElementById('add_photo').showModal()
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
                document.getElementById('add_img').src = `/${data}`;
            }
        })

        document.getElementById('add_photo').close();
        document.getElementById('add_text').showModal();
    })
}

function createPost(){
    $('.submit').click(function(){
      $.ajax('/addpost/', {
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

function addCommentLike(){
    $('.comment_like').click(function(){
        let btn = $(this);
        $.ajax(btn.data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'comment_like': 1,
                'comment_id': btn.data('id')
            },
            'success': function(data){
                $('.comment_likes').innerHTML = data['comment_like_amount'];
                if (data['is_comment_like'] == 1){
                    $('.comment_like').src = '/static/icons/like_on.png';
                }else{
                    $('.comment_like').src = '/static/icons/like_off.png';
                }
            }
        })
    })
}

function closeDialogs(){
    $('.close').click(function(){
        document.getElementById('add_photo').close()
        document.getElementById('add_text').close()
    })
}

$(document).ready(function(){
    addComment();
    addLike();
    addDisike();
    addPost();
    addText();
    createPost();
    closeDialogs();
    
    $.ajax($('#like').data('url'), {
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            'is_like': 1,
        },
        'success': function(data){
            if (data['is_like'] == 1){
                document.getElementById('like_img').src = '/static/icons/like_on.png';
            }else{
                document.getElementById('like_img').src = '/static/icons/like_off.png';
            }
        }
    })

    $.ajax($('#dislike').data('url'), {
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            'is_dislike': 1
        },
        'success': function(data){
            if (data['is_dislike'] == 1){
                document.getElementById('dislike_img').src = '/static/icons/dislike_on.png';
            }else{
                document.getElementById('dislike_img').src = '/static/icons/dislike_off.png';
            }
        }
    })

    $.ajax($('.comment_like').data('url'), {
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            'is_comment_like': 1,
            'comment_id': $('.comment_like').data('id')
        },
        'success': function(data){
            if (data['is_comment_like'] == 1){
                $('.comment_like').src = '/static/icons/like_on.png';
            }else{
                $('.comment_like').src = '/static/icons/like_off.png';
            }
        }
    })
})
