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

export {addBook};