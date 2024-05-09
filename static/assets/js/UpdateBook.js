import {addBook, getAllBooks, setAllBooks} from "./myLocalStorage.js";


window.addEventListener('load', function () {

    load_data();
    document.getElementById('update-book-button').addEventListener('click', handle_update_book);
    document.getElementById('bookImage').onchange = handle_change_image;
});


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


function handle_update_book() {

    const title = document.getElementById('bookTitle');
    const author = document.getElementById('bookAuthor');
    const price = document.getElementById('bookPrice');
    const category = document.getElementById('bookCategory');
    const description = document.getElementById('bookDescription');
    const status = document.getElementById('bookStatus');
    const imgData = document.getElementById('bookImage');

    if (title.value !== '' && author.value !== '' && price.value !== '' && category.value !== '' && description.value !== '' && imgData.nextElementSibling.src !== '') {
        setAllBooks(getAllBooks().map(book => {
            if (book._id == localStorage.getItem('currentBook')) {
                return {
                    ...book,
                    _title: title.value,
                    _author: author.value,
                    _price: price.value,
                    _category: category.value,
                    _description: description.value,
                    _available: status.value == 0 ? true : false,
                    _image_path: imgData.nextElementSibling.src
                }
            }
                return book
        }));
    }

    urlRedirect('book_list.html');
}


function load_data() {
    const book = getAllBooks().find(book => book._id == localStorage.getItem('currentBook'));
    document.getElementById('bookImage').nextElementSibling.src = book._image_path;
    document.getElementById('bookTitle').value = book._title;
    document.getElementById('bookAuthor').value = book._author;
    document.getElementById('bookCategory').value = book._category;
    document.getElementById('bookPrice').value = book._price;
    document.getElementById('bookDescription').value = book._description;
    if(book._available == true) {
        document.getElementById('bookStatus').firstElementChild.selected = true;
    }else{
        document.getElementById('bookStatus').lastElementChild.selected = true;
    }
}


