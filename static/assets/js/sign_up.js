

window.onload = function() {

    document.getElementById('sign_up_form').addEventListener('submit', function(event) {
        event.preventDefault();
        var form = document.getElementById('sign_up_form');
        var formData = new FormData(form);
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/sign_up', true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4 && xhr.status == 200) {
                var response = JSON.parse(xhr.responseText);
                if (response['status'] == 'success') {
                    window.location.href = '/login';
                } else {
                    alert(response['message']);
                }
            }
        };
        xhr.send(formData);
    });


}