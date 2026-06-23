async function loadChats() {
    const container = document.getElementById('chats_container')
    const response = await fetch (
        '/home_loder?selection=chats', {
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        }
    )

    const objectRespone = await response.json()

    if (objectRespone.chats_html){
        container.insertAdjacentHTML("afterbegin", objectRespone.chats_html)
        $(document.getElementById('followers_container')).remove()
    }
}

async function loadRequests() {
    const container = document.getElementById('requests_container')
    const response = await fetch (
        '/home_loder?selection=requests', {
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        }
    )

    const objectRespone = await response.json()

    if (objectRespone.chats_html){
        container.insertAdjacentHTML("afterbegin", objectRespone.chats_html)
        $(document.getElementById('followers_container')).remove()
    }
}

loadRequests()
loadChats()

$(document).on('click', '.user-profile-request', function(){
    window.location.href = `/friends/profile/${this.dataset.profileId}/requests`
})

$(document).on('click', '.open-chat-with', function(){
    setCookie("chatId", this.dataset.chatId)
    window.location.href = `/chats/chat`
})