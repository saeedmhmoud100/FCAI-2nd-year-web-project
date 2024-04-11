function navToggle() {
  document.getElementById('nav').classList.toggle('extend');
}

window.onload = function() {
  document.getElementById('toggle-icon').onclick = navToggle;
}