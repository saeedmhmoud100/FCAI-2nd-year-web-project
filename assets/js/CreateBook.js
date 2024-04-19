import {addBook} from "./myLocalStorage.js";
import {Book} from "./Book.js";

function addNewBook() {
    const title = document.getElementById('bookTitle');
    const author = document.getElementById('bookAuthor');
    const price = document.getElementById('bookPrice');
    const category = document.getElementById('bookCategory');
    const description = document.getElementById('bookDescription');
    const imgData = document.getElementById('bookImage');

    if (title.value !== '' && author.value !== '' && price.value !== '' && category.value !== '' && description.value !== '' && imgData.value !== '') {
        {
            const new_book = new Book(title.value, author.value, price.value, category.value, description.value, imgData.nextElementSibling.src);
            addBook(new_book);
            title.value = '';
            author.value = '';
            price.value = '';
            category.value = '';
            description.value = '';
            imgData.nextElementSibling.src = '';
            imgData.value = '';
        }


    }
}
document.getElementById('add-book-button').onclick = addNewBook;

const handle_change_image = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    // async function
    reader.onload = function(e) {
        document.getElementById('bookImage').nextElementSibling.src = e.target.result;
    }
    // onload function waiting this to complete
    reader.readAsDataURL(file);
}

window.onload = function() {
document.getElementById('bookImage').onchange = handle_change_image;

}
