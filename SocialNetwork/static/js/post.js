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
            }
        })
    })
}

$(function(){
    $(document).click(function(event) {
        let btn = $(event.target);
        if (btn.attr('class') == 'comment_like') {
            $.ajax(btn.data('url'), {
                'type': 'POST',
                'async': true,
                'dataType': 'json',
                'data': {
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                    'id_comment': btn.data('id')
                },
                'success': function(data){
                    document.getElementById('likes').innerHTML = data['like_amount'];
            })
        }
    }

    }
    }
    }

$(document).ready(function(){
    addComment();
    addLike();

    $.ajax($('#like').data('url'), {
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            'is_like': 1
        },
        'success': function(data){
            if (data['like'] == 1){
                document.getElementById('img').src = '/static/a_like.png';
            }else{
                 document.getElementById('img').src = '/static/like.png';
            }
        }
    })


})
