$(document).on('click', '.friends-btn', function(){
    const dataAction = this.dataset.action
    const csrf =  document.getElementById('meta_csrf_token').dataset.csrfToken

    if (this.dataset.actionType === 'msg'){
        window.location.href = CHAT_URL

        return
    }

    if (dataAction === undefined) return

    fetch(`/friends/friends_action/${dataAction}/${this.dataset.userId}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrf 
        }
    })
    .then(response =>{
        if (!response.ok){
            throw new Error("Error")
        }
        return response.json()
    })
    .then(data =>{
        window.location.href = ALL_FRIENDS_URL
    })
    .catch(error =>{
        console.log(error.message)
    })
})
