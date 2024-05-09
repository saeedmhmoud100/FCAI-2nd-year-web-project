function createBooks() {
    if(localStorage.getItem('books')===null){
        localStorage.setItem('books', JSON.stringify([]));
    }
}

function addBook(book) {
    createBooks();

    let books = JSON.parse(localStorage.getItem('books'));
    books.push(book);
    localStorage.setItem('books', JSON.stringify(books));

}

function setAllBooks(books) {
    localStorage.setItem('books', JSON.stringify(books));
}

function getAllBooks() {
    createBooks();

    return JSON.parse(localStorage.getItem('books'));
}
function addCurrentBook(id) {
    localStorage.setItem('currentBook', id);
}

export {addBook,getAllBooks,addCurrentBook,setAllBooks};