window.onload = _ => {
    const e = document.getElementById('love-icon')
    e.addEventListener('click', handle_click)
}

function handle_click(e) {
    e.preventDefault()

    const user_id = e.target.getAttribute('data-user')
    const book_id = e.target.getAttribute('data-book')

    const xhr = new XMLHttpRequest()
    const url = '/wishlist/toggle-book-in-wishlist-api/' + book_id + '/' + user_id
    xhr.open('GET', url, true)

    xhr.send()

    xhr.onreadystatechange = _ => {

        if (xhr.readyState == 4 && xhr.status == 200) {
            const data = JSON.parse(xhr.responseText)
            e = e.target
            if(data.status == 200){
                if (e.src.includes('/static/assets/icons/heart-regular.svg'))
                    e.src = '/static/assets/icons/heart-solid.svg'
                else
                    e.src = '/static/assets/icons/heart-regular.svg'
            }
        }
    }
}



