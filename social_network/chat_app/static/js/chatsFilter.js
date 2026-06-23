let lastFilterDiv = ''

$(document).on('input', '#filter_friends', async function(){
    let selectionDiv = document.getElementById('friends_container')

    filterText = $(this).val()
    currentPage = 1
    hasNextPage = true

    const isEmptyText = filterText === ''

    if (!selectionDiv){
        return
    }
    
    try {
        const response = await fetch(`${window.location.pathname}?page=${chatsCurrentPage}&selection=${this.dataset.selection}&filter_text=${filterText}`, {
            headers: { "X-Requested-With": "XMLHttpRequest" }
        });

        const data = await response.json();
        
        filterData = data.friends_html.trim()
        if (lastFilterDiv === filterData && !isEmptyText){
            return
        }

        selectionDiv.innerHTML = ''
        lastFilterDiv = filterData

        if (filterData !== '') {
            selectionDiv.insertAdjacentHTML("beforeend", filterData);
        } else {
            selectionDiv.innerHTML = '<p class="empty-text">Нет результату по этому запросу</p>'
        }

    } catch (error){
        selectionDiv.innerHTML = '<p class="empty-text">Ошибка закрузки</p>'
    }
})