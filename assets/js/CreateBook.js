import {addBook} from "./myLocalStorage.js";
import {Book} from "./Book.js";

function addNewBook() {
    const title = document.getElementById('bookTitle');
    const author = document.getElementById('bookAuthor');
    const price = document.getElementById('bookPrice');
    const category = document.getElementById('bookCategory');
    const description = document.getElementById('bookDescription');
    const new_book = new Book(title.value, author.value, price.value, category.value, description.value, 'assets/images/alchemist.jpg');
    addBook(new_book);
    title.value = '';
    author.value = '';
    price.value = '';
    category.value = '';
    description.value = '';

}

document.getElementById('add-book-button').onclick = addNewBook;