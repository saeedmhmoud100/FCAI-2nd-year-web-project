import { getAllBooks,setAllBooks } from "./myLocalStorage.js";

function borrow_book() {
    setAllBooks(getAllBooks().map(book => {
        if (book._id == localStorage.getItem('currentBook')) {
            return {...book, _available : false, _is_borrowed :true}
        }
        return book
    }));
    urlRedirect('details.html');

}

window.onload = function () {
    document.getElementById('borrow_book_button').addEventListener('click', borrow_book);
}

