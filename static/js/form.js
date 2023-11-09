const signupForm = document.getElementById('signup-form');
const signinForm = document.getElementById('signin-form');
const showSignupLink = document.getElementById('show-signup-link');
const showSigninLink = document.getElementById('show-signin-link');

showSignupLink.addEventListener('click', function (e) {
    e.preventDefault();
    signupForm.style.display = 'block';
    signinForm.style.display = 'none';
});

showSigninLink.addEventListener('click', function (e) {
    e.preventDefault();
    signinForm.style.display = 'block';
    signupForm.style.display = 'none';
});