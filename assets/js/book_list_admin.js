import {getAllBooks,addCurrentBook} from "./myLocalStorage.js";

function handle_delete_button_click(bookId) {
    addCurrentBook(bookId);
    urlRedirect('delete_book.html');
}
function handle_update_button_click(bookId) {
    addCurrentBook(bookId);
    urlRedirect('update_book.html');
}



function book_list_admin() {
    const n = document.getElementById('book_list_admin');

    let books = getAllBooks()

    books.forEach(book => {
        const template = `
              <div class="col-xs-12 col-sm-6 col-md-4 col-lg-3">
                <div class="card">
                    <img src=${book._image_path} alt="book image">
                    <div class="card-body">
                         <span class="id" style="display: none;">${book._id}</span>
                        <h2 class="card-title">Random Data: ${book._title}</h2>
                        <span>author:  ${book._author}</span>
                        <span>category:  ${book._category}</span>
                        <span>available:  ${book._available}</span>
                        <div class="row w-100">
                            <div class="col-12 text-center">
                                <button class="btn-6 btn-dark">Update</button>
                                <button class="btn-6 btn-dark">Delete</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        const div = document.createElement('div');
        div.innerHTML = template.trim();
        n.appendChild(div.firstChild);
        n.lastElementChild.lastElementChild.lastElementChild.lastElementChild.lastElementChild.lastElementChild.addEventListener('click', () => handle_delete_button_click(book._id));
        n.lastElementChild.lastElementChild.lastElementChild.lastElementChild.lastElementChild.firstElementChild.addEventListener('click', () => handle_update_button_click(book._id));
    });
}

window.addEventListener('load', book_list_admin)