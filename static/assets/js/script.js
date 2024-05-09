function navToggle() {
    document.getElementById('nav').classList.toggle('extend');
}

function urlRedirect(direction='index.html') {
    window.location.href = direction;
}


window.onload = function () {
    document.getElementById('toggle-icon').onclick = navToggle;
    // document.getElementById('signup-button').onclick = singUpRedirect;
}
