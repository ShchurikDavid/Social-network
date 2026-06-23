function getEmailCode(){
    let emailCode = '';

    $('.code-letter').each(function() {
        emailCode += $(this).val() || '';
    });

    return emailCode;
}

function getErrorText(form) {
    return $(form).closest('.auth-form').find('.error-text')[0];
}

const inputs = document.querySelectorAll('.code-letter');

inputs[0].addEventListener('paste', (e) => {
    let data = e.clipboardData.getData('text');
    let chars = data.split('');

    inputs.forEach((input, i) => {
        input.value = chars[i] || '';
    });
});

inputs.forEach((input, index) => {
    input.addEventListener('input', (e) => {
        if (e.target.value && index < inputs.length - 1) {
            inputs[index + 1].focus();
        }
    });

    input.addEventListener('keydown', (e) => {
        if (e.key === "Backspace" && !e.target.value && index > 0) {
            inputs[index - 1].focus();
        }
    });
});