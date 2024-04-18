import {getAllBooks} from "./myLocalStorage.js";
function book_list_admin() {
    const n = document.getElementById('book_list_admin');

    let books = getAllBooks()

    books.forEach(book => {
        const template = `
              <div class="col-xs-12 col-sm-6 col-md-4 col-lg-3">
                <div class="card">
                    <img src="assets/images/book1.jpg" alt="book image">
                    <div class="card-body">
                        <h2 class="card-title">Random Data: ${book._title}</h2>
                        <span>author:  ${book._author}</span>
                        <span>category:  ${book._category}</span>
                        <span>available:  ${book._available}</span>

                        <div class="row w-100">
                            <div class="col-12 text-center">
                                <button class="btn-6 btn-dark" onclick="urlRedirect('update_book.html')">Update</button>

                                <button class="btn-6 btn-dark" onclick="urlRedirect('delete_book.html')">Delete</button>
                            </div>
                        </div>


                    </div>

                </div>
            </div>
        `;
        const div = document.createElement('div');
        div.innerHTML = template.trim();
        n.appendChild(div.firstChild);
    });
}

window.addEventListener('load', book_list_admin)