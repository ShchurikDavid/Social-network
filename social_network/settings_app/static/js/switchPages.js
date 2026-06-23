const mainContainer = document.getElementById('main_container')
const navigationsTexts = document.querySelectorAll('.nav-text')

$(document).on('click', '.info-navigations-text', async function(){
    resetText(this)
})

function resetText(clickedText) {
    for (let text of navigationsTexts){
        if (text.classList.contains('info-navigations-text')) {
            text.classList.remove('info-navigations-text')
            text.classList.add('info-navigations-active-test')

            mainContainerChange(text.dataset.id)
        } else if (text.classList.contains('info-navigations-active-test')) {
            text.classList.remove('info-navigations-active-test')
            text.classList.add('info-navigations-text')
        }
    }
}

function mainContainerChange(id){
    if (id === 'set_settings_container') {
        openModalId('set_settings_container')
        closeModalId('set_albums_container')
    } else if (id === 'set_albums_container') {
        openModalId('set_albums_container')
        closeModalId('set_settings_container')
    }
}
