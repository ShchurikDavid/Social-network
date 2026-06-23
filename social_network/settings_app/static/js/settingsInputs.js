$(document).on('click', '.checkbox', function(){
    if (this.dataset.checkbox === 'true'){
        this.dataset.checkbox = false
        this.src = checkboxFalse
    } else if (this.dataset.checkbox){
        this.dataset.checkbox = true
        this.src = checkboxTrue
    }
})

$(document).on('click', '#avatar_img_div', function(){
    let input = document.getElementById('avatar_img_input')
    input.click()
})

$(document).on('click', '#my_password_eye', function(){
    let input = document.getElementById('my_password')

    if (input.type === 'text') {
        input.type = 'password'
        this.src = closeEye
    } else if (input.type === 'password') {
        input.type = 'text'
        this.src = openEye
    }
})

$(document).on('click', '#new_password_eye', function(){
    let input = document.getElementById('new_password')

    if (input.type === 'text') {
        input.type = 'password'
        this.src = closeEye
    } else if (input.type === 'password') {
        input.type = 'text'
        this.src = openEye
    }
})

$(document).on('click', '#check_password_eye', function(){
    let input = document.getElementById('check_password')

    if (input.type === 'text') {
        input.type = 'password'
        this.src = closeEye
    } else if (input.type === 'password') {
        input.type = 'text'
        this.src = openEye
    }
})

$(document).on('click', '#email_input_eye', function(){
    let input = document.getElementById('email_input')

    if (input.type === 'email') {
        input.type = 'password'
        this.src = closeEye
    } else if (input.type === 'password') {
        input.type = 'email'
        this.src = openEye
    }
})

$(document).on('click', '#birth_date_input_eye', function(){
    let input = document.getElementById('birth_date_input')

    if (!input.dataset.real) {
        input.dataset.real = input.value;
        input.value = 'дд.мм.гггг';
        this.src = closeEye
    } else {
        input.value = input.dataset.real;
        delete input.dataset.real;
        this.src = openEye
    }
})

$(document).on('click', '#user_sign_board', function(){
    console.log('')
})