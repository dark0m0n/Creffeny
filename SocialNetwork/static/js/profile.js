function addPost() {
    $('#addpost').click(function(){
        document.getElementById('add_photo').showModal();
    })
}

function addText(){
    $('#select_photo').change(function(){
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
            'success': function(data){
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

function closeDialogs(){
    $('.close').click(function(){
        document.getElementById('add_photo').close();
        document.getElementById('add_text').close();
        document.getElementById('change_profile_img_1').close();
        document.getElementById('change_profile_img_2').close();
    })
}

function changeProfileImage1(){
    $('#change_img').click(function(){
        document.getElementById('change_profile_img_1').showModal();
    })
}

function changeProfileImage2(){
    $('#change_profile').change(function(){
        var formData = new FormData();

        formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val());
        formData.append('file', document.getElementById('change_profile').files[0]);
        formData.append('change_img', true);

        $.ajax('/change/', {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': formData,
            'processData': false,
            'contentType': false,
            'success': function(data){
                document.getElementById('changed_profile_img').src = `/${data}`;
            }
        })

        document.getElementById('change_profile_img_1').close();
        document.getElementById('change_profile_img_2').showModal();
    })
}

function change_profile_img_3(){
    $('.submit_img').click(function(){
      $.ajax('/change/', {
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': {
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
            'changed': 1
        },
        'success': function(data){
            window.location.reload();
        }
    })  
    })
}

function follow(){
    $('#follow').click(function(){
        let btn = $(this);
        $.ajax(btn.data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'follow': 1
            },
            'success': function(data){
                document.getElementById('followers').innerHTML = 'Followers: ' + data['followers_len'];
                if (data['is_follow'] == 1){
                    document.getElementById('follow').innerHTML = 'Followed';
                }else{
                    document.getElementById('follow').innerHTML = 'Follow';
                }
            }
        })
    })
}

$(document).ready(function() {
    addPost();
    addText();
    createPost();
    closeDialogs();
    changeProfileImage1();
    changeProfileImage2();
    change_profile_img_3();
    follow();

    $.ajax($('#follow').data('url'), {
        'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'is_follow': 1
            },
            'success': function(data){
                if (data['is_follow'] == 1){
                    document.getElementById('follow').innerHTML = 'Followed';
                }else{
                    document.getElementById('follow').innerHTML = 'Follow';
                }
            }
    })
})