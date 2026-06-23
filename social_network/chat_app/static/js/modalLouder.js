let modalCurrentPage = 0;
let modalLoading = false;

const modalSentinel = document.getElementById('modal_loader')

const modalObeserve = new IntersectionObserver(async (entries)=>{
    if (entries[0].isIntersecting && modalLoading === false){
        modalLoading = true
        modalCurrentPage += 1
        
        const response = await fetch (
            `/chats/chat_modal/?page=${modalCurrentPage}`, {
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            }
        )

        const objectRespone = await response.json()

        if (objectRespone.html){
            let selectionDiv = document.getElementById('users_array')
            if (!selectionDiv) return

            selectionDiv.insertAdjacentHTML("beforeend", objectRespone.html)
        }

        if (!objectRespone.has_next){
            modalObeserve.disconnect()
        }

        modalLoading = false
    }
}, {rootMargin: "50px"})

modalObeserve.observe(modalSentinel)


let editModalCurrentPage = 0;
let editModalLoading = false;

const editModalSentinel = document.getElementById('edit_modal_loader')

const editModalObeserve = new IntersectionObserver(async (entries)=>{
    if (entries[0].isIntersecting && editModalLoading === false){
        editModalLoading = true
        editModalCurrentPage += 1
        
        const response = await fetch (
            `/chats/chat_modal/?page=${editModalCurrentPage}&edit_modal=true`, {
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            }
        )

        const objectRespone = await response.json()

        if (objectRespone.html){
            let selectionDiv = document.getElementById('edit_users_array')
            if (!selectionDiv) return

            selectionDiv.insertAdjacentHTML("beforeend", objectRespone.html)
        }

        if (!objectRespone.has_next){
            editModalObeserve.disconnect()
        }

        editModalLoading = false
    }
}, {rootMargin: "50px"})

editModalObeserve.observe(editModalSentinel)

$(document).on('input', '#edit_filter_input, #create_filter_input', async function(){
    let filterText = $(this).val()
    let currentPage = 1
    let hasNextPage = true
    let fetchUrl = `/chats/chat_modal/?page=${currentPage}&filter_text=${filterText}`
    
    let selectionDiv
    
    if (this.id === 'create_filter_input') {
        selectionDiv = document.getElementById('users_array')
    } else if (this.id === 'edit_filter_input') {
        selectionDiv = document.getElementById('edit_users_array')
    }
    
    if (!selectionDiv) return

    const isEmptyText = filterText === ''
    
    if (!selectionDiv){
        return
    }
        
    try {
        const response = await fetch(fetchUrl, {
            headers: { "X-Requested-With": "XMLHttpRequest" }
        });
    
        const data = await response.json();
        
        filterData = data.html.trim()
        if (lastFilterDiv === filterData && !isEmptyText){
            return
        }
    
        selectionDiv.innerHTML = ''
        lastFilterDiv = filterData
    
        if (filterData !== '') {
            selectionDiv.insertAdjacentHTML("beforeend", filterData);
            reapplySelectedUsers()
        } else {
            selectionDiv.innerHTML = '<p class="empty-text">Нет результату по этому запросу</p>'
        }
    
    } catch (error){
        console.log(error)
        selectionDiv.innerHTML = '<p class="empty-text">Ошибка закрузки</p>'
    }
})

function reapplySelectedUsers() {
    selectedUsers.forEach(id => {
        let checkbox = document.querySelector(`.checkbox[data-profile-id="${id}"]`)

        if (checkbox) {
            checkbox.dataset.checkbox = 'true'
            checkbox.src = trueCheckbox
        }
    })

    setCountUsersSpan(selectedUsers.length, 'count_select_users')
}