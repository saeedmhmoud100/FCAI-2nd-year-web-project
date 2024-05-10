import { getAllBooks,setAllBooks } from "./myLocalStorage.js";

function borrow_book() {
    setAllBooks(getAllBooks().map(book => {
        if (book._id == localStorage.getItem('currentBook')) {
            return {...book, _available : false, _is_borrowed :true}
        }
        return book
    }));
    urlRedirect('book_detail.html');

}

window.onload = function () {
    document.getElementById("BookName").innerHTML = getAllBooks().filter(book => book._id == localStorage.getItem('currentBook'))[0]._title;
    document.getElementById('borrow_book_button').addEventListener('click', borrow_book);
}

