function navToggle() {
    document.getElementById('nav').classList.toggle('extend');
}

function singUpRedirect(direction='home.html') {
    window.location.href = direction;
}


window.onload = function () {
    document.getElementById('toggle-icon').onclick = navToggle;
    // document.getElementById('signup-button').onclick = singUpRedirect;
}
