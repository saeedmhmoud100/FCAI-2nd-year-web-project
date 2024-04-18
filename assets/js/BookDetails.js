import {getAllBooks} from "./myLocalStorage.js";

window.addEventListener('load', get_book_details)


function get_book_details() {
    if (localStorage.getItem('currentBook') != null) {
        const book = getAllBooks().find(book => book._id == localStorage.getItem('currentBook'));
        if (book) {
            document.getElementById('bookID').innerHTML = book._id;
            document.getElementById('bookTitle').innerHTML = book._title;
            document.getElementById('bookAuthor').innerHTML = book._author;
            document.getElementById('bookCategory').innerHTML = book._category;
            document.getElementById('bookAvailable').innerHTML = book._available;
            document.getElementById('bookDescription').innerHTML = book._description;

            if (book._available === false) {
                document.getElementById('bookAvailable').parentNode.parentNode.lastElementChild.style.display = 'none';
            }
        }
    }
}