$(() => {
    $(document).on('click', '.msg-btn', function(){
        window.location.href = CHAT_URL
    })

    document.getElementById('all_requests').addEventListener('click', function(){
        setCookie("selection", "requests")
        window.location.href = REQUEST_HTTP
    })

    const registrationModal = $('#registration_modal');
    
    if (first_registration === "True"){
        openModal("modal-registration-bg");
    };

    $('#openModal').on('click', function(){
        openModal('modal-registration-bg');
    });

    registrationModal.on('submit', function(event){
        event.preventDefault()

        $.ajax({
            url: registrationModal.attr('action'),
            method: 'POST',
            data: registrationModal.serialize(),
            success: function(response){
                document.getElementById('username_text').textContent = response.username;
                document.getElementById('pseudonym_text').textContent = response.pseudonym;

                $('.modal-registration-bg').removeClass('visible')
                $('.modal-registration-bg').addClass('hidden');              
            },
            error: function(response){
                const errorText = $('.modal-error-text');

                if (data?.error) {
                    const errors = data.error;

                    const firstKey = Object.keys(errors)[0];
                    const message = errors[firstKey][0];

                    errorText.text(message);
                } else {
                    errorText.text('Помилка серверу');
                };

                errorText.removeClass('hidden');
                errorText.addClass('visible');
            }
        })
    })
})
