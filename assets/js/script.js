function navToggle() {
    document.getElementById('nav').classList.toggle('extend');
}

function singUpRedirect() {
    window.location.href = 'home.html';
}


window.onload = function () {
    document.getElementById('toggle-icon').onclick = navToggle;
    document.getElementById('signup-button').onclick = singUpRedirect;
}
