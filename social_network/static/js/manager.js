function getCookie(name) {
  let matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}

function setCookie(name, value){
    let updateCookie= encodeURIComponent(name)+ "="+ encodeURIComponent(value)
    document.cookie= `${updateCookie}; path=/`
}

function clearCookie(nameList){
    nameList.forEach(name => {     
        if (!getCookie(name)){
            return
        }
        document.cookie= `${encodeURIComponent(name)}=; max-age=0; path=/`
    });
}

function openModal(modalClass){
    $(`.${modalClass}`).removeClass('hidden');
    $(`.${modalClass}`).addClass('visible');
};

function closeModal(modalClass){
    $(`.${modalClass}`).addClass('hidden');
    $(`.${modalClass}`).removeClass('visible');
};

function openModalId(modalId){
    $(`#${modalId}`).removeClass('hidden');
    $(`#${modalId}`).addClass('visible');
};

function closeModalId(modalId){
    $(`#${modalId}`).addClass('hidden');
    $(`#${modalId}`).removeClass('visible');
};