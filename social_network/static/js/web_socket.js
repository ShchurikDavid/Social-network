const authToken = localStorage.getItem('authToken');

const socket = io("http://192.168.0.145:8020", {
    auth: {
        token: `Bearer ${authToken}`
    },
    transports: ["websocket"],
    autoConnect: true
});

async function joinToChat(chatId) {
    socket.emit("joinChat", { chatId: chatId }, (response) => {
        console.log("connected", response.status)
        startListeningMessages()
    })
}

async function leaveFromChat(chatId) {
    socket.emit("leaveChat", { chatId: chatId }, (response) => {
        console.log("leave")
    })
}

async function subscribeOnOnlineChatsUsers(ids) {
    socket.emit("subscribeAndGetInitialStatuses", ids, (response) => {
        console.log("subscribeAndGetIntialStatuses", response.userIds)
        startListeningOnlineStatus() 
    })
}

async function startListeningOnlineStatus() {
    socket.off("userStatusUpdated");
    socket.on("userStatusUpdated", (response) => {
        setUserOnline(response.userId, response.status)
    });
    
    console.log("Прослушивание новых статусов");
}

function startListeningMessages() {
    socket.off("newChatMessage", newMessage);
    socket.on("newChatMessage", newMessage);
    console.log("Прослушивание новых сообщений успешно запущено.");
}
  
function newMessage(data) {
    console.log("got message:", data);

    if (data.sender.id == Number(myId)) return

    let chatDiv = document.getElementById('chat_message_container')

    if (data.text){
        chatDiv.innerHTML += `
            <div class="msg-container">
                <img class="message-image msg-image online-img-${data.senderId}" src="${offlineImg}" alt="indicator">
    
                <div class="msg-info content-border-container">
                    <div class="msg-info-text">
                        <p class="msg-username-text">${ data.sender.profile.pseudonym }</p>
                        <div class="msg-text">${ data.text }</div>
                    </div>
                    <div class="msg-info-date">
                        <p class="msg-date-text">${ formatMessageTime(data.createdAt) }</p>
                        <img class="msg-img" src="{% static 'images/msg/open.svg' %}" alt="open" >
                    </div>
                </div>
            </div>
        `
    }

    let imageHtml = ''
    for (let image of data.messageImages){
        if (LOCAL === "True"){
            imageHtml += `<img class="send-message-image-other load-message-image" src="{% if LOCAL == 'False' %}http://192.168.0.145:8020/media/{% else %}/media/{% endif %}${ image.image }" alt="img"></img>`
        } else {
            imageHtml += `<img class="send-message-image-other load-message-image" src="{% if LOCAL == 'False' %}http://192.168.0.145:8020/media/{% else %}/media/{% endif %}${ image.image }" alt="img"></img>`
        }
    }

    chatDiv.innerHTML += imageHtml

    chatDiv.scrollTo({
        top: chatDiv.scrollHeight,
        behavior: 'smooth'
    });
}
 const timeFormatter = new Intl.DateTimeFormat("uk-UA", {
    hour: "2-digit",
    minute: "2-digit",
});

function formatMessageTime(createdAt) {
    return timeFormatter.format(new Date(createdAt));
}

async function getOnlineUsers(friends_ids){
    let ids = friends_ids.map((obj, index) => {
        console.log(obj, 'obj', '=============')
        return obj
    })

    setOnlineUsers(ids)
}

async function setOnlineUsers(ids){
    console.log(ids, typeof ids)
    socket.emit("getOnlineUsers", ids, (response) => {
        console.log("getOnlineUsers", response.userIds, response)
        for (let id of response.userIds){
            setUserOnline(id, "online")
        }
    })
}