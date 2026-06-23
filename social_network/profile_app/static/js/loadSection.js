async function getFriendsArray(type, selectionDiv){
    let filterText = ''
    let currentPage = 1
    let limit = type === 'requests' ? 3 : 6

    let fetchUrl = `/friends/all_friends/${type}?page=${currentPage}&filter_text=${filterText}&limit=${limit}`

    try {
        const response = await fetch(fetchUrl, {
            headers: { "X-Requested-With": "XMLHttpRequest" }
        });
    
        const data = await response.json(); 

        if (data.html){
            selectionDiv.innerHTML = data.html
        }
    }
    catch (error){
        console.log(error)
        selectionDiv.innerHTML = '<p class="empty-text">Ошибка закрузки</p>'
    }
}

getFriendsArray('requests', document.getElementById('requests'))
getFriendsArray('recommendations', document.getElementById('recommendations'))
getFriendsArray('friend', document.getElementById('friend'))