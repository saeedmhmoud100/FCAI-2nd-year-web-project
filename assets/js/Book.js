class Book {
    static id;
    _title;
    _author;
    _price;
    _category;
    _description;
    _available;
    _image_path;
    _is_borrowed;
    constructor(title, author, price, category, description, image_path) {
        this._title = title;
        this._author = author;
        this._price = price;
        this._category = category;
        this._description = description;
        this._available = true;
        this._image_path = image_path;
        this._is_borrowed = false;
        this.id = Book.id++;
    }
    get title() {
        return this._title;
    }
    set title(value) {
        this._title = value;
    }
    get author() {
        return this._author;
    }
    set author(value) {
        this._author = value;
    }
    get price() {
        return this._price;
    }
    set price(value) {
        this._price = value;
    }
    get category() {
        return this._category;
    }
    set category(value) {
        this._category = value;
    }
    get description() {
        return this._description;
    }
    set description(value) {
        this._description = value;
    }
    get available() {
        return this._available;
    }
    set available(value) {
        this._available = value;
    }
    get image_path() {
        return this._image_path;
    }
    set image_path(value) {
        this._image_path = value;
    }
    get is_borrowed() {
        return this._is_borrowed;
    }
    set is_borrowed(value) {
        this._is_borrowed = value;
    }
    toString() {
        return `Title: ${this.title} Author: ${this.author}`;
    }
}

Book.id = 0;

export { Book };
