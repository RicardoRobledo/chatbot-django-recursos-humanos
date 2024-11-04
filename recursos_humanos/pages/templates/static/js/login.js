$(document).ready(function() {
    $('body').fadeIn(1000);
});

$('#login').on('click', async function(event){
    event.preventDefault();

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const url = 'http://127.0.0.1:8000/';
    //const url = 'https://demognp.nextwaveai.ai/';

    const response = await fetch(url, {
        method: 'POST',
        mode: 'same-origin',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            username: $('#username').val(),
            password: $('#password').val()
        })
    }).then(async (response) => {

        if (response.status === 302) {
            return response.json();
        }else{
            $('#message').show().delay(3000).fadeOut();
            throw new Error('Request failed with status');
        }
    
    }).then(async (data) => {

        window.location.href = data['redirect_url'];
        return data;
    
    }).catch(error => {
        console.error('Error:', error);
    });

})
