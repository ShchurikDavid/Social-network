$(document).on('click', '.profile-interaction-image', function(event){
    event.stopPropagation()

    const menu =  $(this).siblings('.interaction-menu')
    $('.interaction-menu').not(menu).removeClass('visible').addClass('hidden')
    menu.toggleClass('hidden visible')
})

$(document).on('click', '.interaction-img', function(event){
    const csrfToken = document.getElementById('meta_csrf_token').dataset.csrfToken

    fetch(this.dataset.action, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Ошибка")
        }

        return response.json()
    })
    .then(data => {
        const interactCount = document.getElementById(`post_${this.dataset.postId}_${this.dataset.interact}`)
        
        if (data.do) {
            interactCount.textContent = Number(interactCount.textContent) + 1
        } else {
            interactCount.textContent = Number(interactCount.textContent) - 1
        }

    })
    .catch(error => {
        console.log("Ошибки", error)
    })
})

$(document).on('click', '.delete-post-button', function(event){
    event.preventDefault();

    const button = $(this)
    const deletePostForm = button.closest('form')
    const post = button.closest('.post-conteiner')
    const menu = button.closest('.interaction-menu')

    $.ajax({
        url: deletePostForm.attr('action'),
        method: 'POST',
        data: deletePostForm.serialize(),
        success: function(response){
            menu.removeClass('visible').addClass('hidden')
            post.remove()
        },
        error: function(response){
            console.log('400', response);
        }
    });
})