const handle_change_image = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    // async function
    reader.onload = function(e) {
        document.getElementById('id_image').nextElementSibling.src = e.target.result;
    }
    // onload function waiting this to complete
    reader.readAsDataURL(file);
}

window.onload = function() {
document.getElementById('id_image').onchange = handle_change_image;

}
