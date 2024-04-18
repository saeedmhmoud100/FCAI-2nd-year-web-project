import {getAllBooks,addCurrentBook} from "./myLocalStorage.js";


function delete_button(bookId) {
    addCurrentBook(bookId);
    urlRedirect('details.html');
}

function book_list_user() {
    const n = document.getElementById('book_list_user');

    let books = getAllBooks()

    books.forEach(book => {
        const template = `
              <div class="col-xs-12 col-sm-6 col-md-4 col-lg-3">
                <div class="card">
                <img src="assets/images/book1.jpg" alt="book image">
                <div class="card-body">
                <span class="id" style="display: none;">${book.id}</span>
                <h2 class="card-title">${book._title}</h2>
                <span>author: ${book._author}</span>
                <span>category: ${book._category}</span>
                <span>available: ${book._available}</span>

                <div class="row w-100">
                    <div class="col-12 text-center">
                        <button class="btn-6 btn-dark">details</button>
                    </div>
                </div>


                </div>

            </div>
        </div>
        `;
        const div = document.createElement('div');
        div.innerHTML = template.trim();
        n.appendChild(div.firstChild);
        n.lastElementChild.lastElementChild.lastElementChild.lastElementChild.lastElementChild.lastElementChild.addEventListener('click', () => delete_button(book._id));
    });
}

window.addEventListener('load', book_list_user)