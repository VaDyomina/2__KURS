function send_sentence() {
    $.ajax({
        type: "POST",
        url: "/sentence_gen",
        data: $('form').serialize(),
        type: 'POST',
        success: function(response) {
            var json = jQuery.parseJSON(response)
            $('#answer').html("Результат: " + json.answer)
            console.log(response);
        },
        error: function(error) {
            console.log(error);
        }
    });
}