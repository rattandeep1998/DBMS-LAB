
$(function() {
    $('button').click(function() {
        console.log('here');
        var user = $('#txtUsername').val();
        var pass = $('#txtPassword').val();
        $.ajax({
            type: 'POST',
            url: '/signUpUser',
            data: $('form').serialize(),
            dataType: 'json',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
