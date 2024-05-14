window.onload = function () {
    Array.from(document.getElementsByClassName('click_submit_action')).forEach(element => {
        element.addEventListener('submit', handle_submit)
    })
}

function handle_submit(e) {
    e.preventDefault()
    let url = '/books/list_api?'
    // append all form data to the url
    Array.from(document.getElementsByClassName('click_submit_action')).forEach(element => {
        const formData = new FormData(element)
        for (var pair of formData.entries()) {
            if(pair[0] == 'price_from' && pair[1] == ''){
                url += pair[0] + '=' + '0' + '&'
            }else
                url += pair[0] + '=' + pair[1] + '&'
        }

    })

    if (url.endsWith('&')) {
        url = url.slice(0, -1)
    }

    const xhr = new XMLHttpRequest()
    xhr.open('GET', url, true)
    xhr.send()

    xhr.onreadystatechange = _ => handle_response(xhr)

}


function handle_response(xhr) {
    if (xhr.readyState == 4 && xhr.status == 200) {
        const data = JSON.parse(xhr.responseText)
        const cards_container = document.getElementById('book_list_user')
        cards_container.innerHTML = ''

        for (const book of data) {
            let html_card = `
        <div class="col-12 col-sm-6 col-md-4">
                <div class="card">
                    <img src=${book.image_url} alt="book image">
                    <div class="card-body">
                        <span class="id" style="display: none;">${book.id}</span>
                        <h2 class="card-title">${book.title}</h2>
                        <span>author: ${book.author}</span>
                        <span>category: ${book.category}</span>
                        <span>available: ${String(book.available)}</span>
                        <span>rating: ${book.rating}</span>
                        <span>price: ${book.price}</span>
                        <div class="row w-100">
                            <div class="col-12 text-center">
                                <button class="btn-6 btn-dark" >
                                    details
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>           
            `

            const div = document.createElement('div')
            div.innerHTML = html_card
            const button = div.getElementsByTagName('button')
            button[0].addEventListener('click', _ => {
                    window.location.href = book.details_url
            })
            if(book.is_admin){
                button[0].parentElement.innerHTML += `<button class="btn-6 btn-success">Update</button><button class="btn-6 btn-danger">Delete</button>`
                button[1].addEventListener('click', _ => {
                        window.location.href = book.update_url
                })
                button[2].addEventListener('click', _ => {
                        window.location.href = book.delete_url
                })
            }

            cards_container.appendChild(div.children[0])
        }


    }
}