import { getAllBooks,setAllBooks } from "./myLocalStorage.js";

function delete_book() {
    setAllBooks(getAllBooks().filter(book => {
        if (book._id != localStorage.getItem('currentBook')) {
            return book
        }
    }));
    urlRedirect('book_list.html');

}

window.onload = function () {
    document.getElementById("BookName").innerHTML = getAllBooks().filter(book => book._id == localStorage.getItem('currentBook'))[0]._title;


    document.getElementById('delete_book_button').addEventListener('click', delete_book);
}
