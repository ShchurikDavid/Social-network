const onlineCache = new Map()

if (isAuthenticated === 'True'){
    const onlineSocket = new WebSocket(`ws://${window.location.host}/chat/online/`);
    
    onlineSocket.onmessage = function (event) {
        const data = JSON.parse(event.data)
        onlineCache.set(data.user_id, data.status)
    
        setUserOnline(data.user_id, data.status)
    }
}

function setUserOnline(userId, status) {
    document.querySelectorAll(`.online-img-${userId}`).forEach((avatar) => {
        const statusWrapper = avatar.closest('.status-wrapper')
        let statusImg = statusWrapper?.querySelector('.status-img')

        if (!statusImg){
            statusImg = statusWrapper?.querySelector('.status-small-img')
        }
        
        if (!statusImg) return

        if (status === "offline") {
            statusImg.src = offlineImg
        } else if (status === "online") {
            statusImg.src = onlineImg
        }
    })
}

const observer = new MutationObserver(() => {
    requestAnimationFrame(() => {
        onlineCache.forEach((status, userId) => {
            setUserOnline(userId, status)
        })
    })
})

observer.observe(document.body, {
    childList: true,
    subtree: true
})