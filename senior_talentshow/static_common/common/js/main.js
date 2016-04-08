function load_instagram(limit)
{
    if (!limit)
    {
        limit = 3;
    }
    $feed = $('.instagram-feed .feed');
    $.ajax({
        url: 'https://api.instagram.com/v1/users/1436010400/media/recent/?client_id=4d7350a23d64425682e91d87c37f50c0&callback=instagramCallback',
        crossDomain: true,
        type: 'GET',
        dataType: 'jsonp',
        success: function(data) {
            $('.instagram-feed .loading').remove();
            $.each(data.data, function(i, gram) {
                if (i < limit)
                {
                    $feed.append('<div class="embed-responsive embed-responsive-instagram"><iframe src="' + gram.link + 'embed/" frameborder="0" scrolling="no" allowtransparency="true"></iframe></div>');
                }
            });
        },
    });

}

$(function(){
    function build_error(field, msg)
    {
        return '<p class="alert alert-danger form-error"><strong>' + field + ':</strong> ' + msg;
    }

    function build_success(msg)
    {
        return '<p><i class="fa fa-check-square green"></i> ' + msg + '</p>';
    }

    $('.js-reminder-submit').on('click', function(e){
        e.preventDefault();
        var $formContainer = $('.reminder-form-container');
        var $form = $('#audition-reminder-form');
        var data = $form.serializeArray();
        $('.form-error').remove();
        $.ajax({
            url: '/set-reminder/',
            data: data,
            type: 'POST',
            success: function(response)
            {
                if (response.errors)
                {
                    $.each(response.errors, function(key, val){
                        $form.before(build_error(key, val));
                    });
                }
                else
                {
                    var success_response = '';
                    if (response.reminder_email)
                    {
                        success_response += build_success("We'll send you a reminder email the night before your audition.");
                    }

                    if (response.reminder_text)
                    {
                        success_response += build_success("We'll send you a reminder text an hour before your audition.");
                    }

                    if (!response.reminder_text && !response.reminder_email)
                    {
                        success_response += build_success("We won't send you any reminders.");
                    }

                    $formContainer.html(success_response);
                }
            },
            error: function(response)
            {
                $form.before(build_error('Error', 'Sorry, an error occurred.'));
            }
        });
    });
});