// ------ Login eye Show Password
const passwordField = document.querySelector('.password-field input[type="password"]');
const showPasswordField = document.querySelector('.password-field .eye-icon');

showPasswordField.addEventListener('click', function () {
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        showPasswordField.innerHTML = '<i class="fa fa-eye-slash"></i>';
    } else {
        passwordField.type = 'password';
        showPasswordField.innerHTML = '<i class="fa fa-eye"></i>';
    }
});
// ------ end Login eye Show Password



