$(document).on('click', '#edit_cansle_create_group_modal', function(){
    deleteUsersContainer = document.getElementById('delete_users_container').innerHTML = ''

    openModal('modal-add-group-bg')
    closeModal('modal-edit-create-group-bg')
})

$(document).on('click', '#edit_create_group_btn', async function(){
    createGroup(edit=true)
})

$(document).on('click', '#edit_cansle_add_group_modal', function(){
    clearCheckbox()
    closeModal('modal-edit-add-group-bg')
})

$(document).on('click', '#edit_next_add_group_modal', function(event){
    event.preventDefault()
    openModal('modal-edit-create-group-bg')
    closeModal('modal-edit-add-group-bg')

    
    deleteUsersContainer = document.getElementById('edit_delete_users_container')

    let userModalImg
    if (LOCAL === 'False') {
        userModalImg = `<img class="followers-image online-img-${checkbox.dataset.profileId} avatar-img" src="http://192.168.0.145:8020/media/${indicatorImg} alt="">`
    } else {
        userModalImg = `<img class="followers-image online-img-${checkbox.dataset.profileId} avatar-img" src=${indicatorImg} alt="">`
    }

    deleteUsersContainer.innerHTML = ''
    activeCheckBox().forEach(checkbox => {
        deleteUsersContainer.innerHTML += `
            <div class="followers-user-block" id=user_${checkbox.dataset.profileId}>
                <div class="followers-container-image-container">
                    <div class="status-wrapper">
                        <img class="followers-image online-img-${checkbox.dataset.profileId} avatar-img" src=${indicatorImg} alt="">
                        <img class="status-small-img" src=${offlineImg} alt="off">
                    </div>
                </div>
                <div class="user-block-info">
                    <p class="user-block-username">${checkbox.dataset.username}</p>
                    <img src=${deleteImg} alt="del" class="del-img del-user" data-del-user=${checkbox.dataset.profileId}>
                </div>
            </div>
        `
    })
})


$(document).on('click', '#edit_group_btn', function(){
    closeModalId('context_menu_admin')
    openModal('modal-edit-add-group-bg')

    let createNameInput = document.getElementById('edit_group_name_input')

    if (createNameInput){
        createNameInput.value = document.getElementById('group_name').textContent.trim()
    }

    document.querySelectorAll(".get-group-id").forEach((user)=>{
        let id = user.dataset.getId

        if (id != ""){
            let checkbox = document.getElementById(`edit_checkbox_${id}`)

            if (checkbox) {
                checkbox.dataset.checkbox = 'true'
                checkbox.src = trueCheckbox
    
                if (!selectedUsers.includes(id)) {
                    selectedUsers.push(id)
                }
            }
        }
    })
})

$(document).on('click', '.clear-chat', clearChat)

$(document).on('click', '.close-context-menu', ()=>{
    closeModalId('context_menu_admin')
    closeModalId('context_menu_user')
})

$(document).on('click', function(event) {
    if (!$(event.target).closest('.context-menu-admin').length) {
        closeModalId('context_menu_admin')
    }

    if (!$(event.target).closest('.context-menu-user').length) {
        closeModalId('context_menu_user')
    } 
})

$(document).on('click', '.context-menu-admin-interactive', function(event){
    event.stopPropagation();

    openModalId('context_menu_admin')
    
    const contextMenu = $('#context_menu_admin');
    contextMenu.css({
        top: event.pageY + 20 + 'px',
        left: event.pageX - ( contextMenu.width() / 2 ) + 'px'
    })
})

$(document).on('click', '.context-menu-interactive ', function(event){
    event.stopPropagation();

    openModalId('context_menu_user')

    const contextMenu = $('#context_menu_user');
    contextMenu.css({
        top: event.pageY + 20 + 'px',
        left: event.pageX - ( contextMenu.width() / 2 ) + 'px'
    })
})

function clearChat(){
    clearCookie(["chatId"])

    document.getElementById('chat_container').innerHTML = `
        <div class="empty-chat-conteiner" id="empty_chat_conteiner">
            <p class="empty-chat-title">Почніть нове спілкування</p>
            <p class="empty-chat-text">Оберіть контакт зі списку ліворуч або створіть групу, щоб почати спілкування</p>
        </div>
    `
}