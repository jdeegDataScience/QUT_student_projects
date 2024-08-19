const express = require("express");
const router = express.Router();

// Require our controllers.
const bookController = require("../controllers/bookController");
const authorController = require("../controllers/authorController");
const genreController = require("../controllers/genreController");
const bookInstanceController = require("../controllers/bookinstanceController");

/// BOOK ROUTES ///

// GET catalog home page.
router.get("/", bookController.index);

router.route("/books")
    .get(bookController.book_list) // GET list of all Books
    .post(bookController.book_create); // POST create a new Book

router.route("/books/:id")
    .get(bookController.book_detail) // GET one Book
    .put(bookController.book_update) // PUT update a Book
    .delete(bookController.book_delete); // DELETE a Book

/// AUTHOR ROUTES ///

router.route("/authors")
    .get(authorController.author_list) // GET list of all Authors
    .post(authorController.author_create); // POST create a new Author

router.route("/authors/:id")
    .get(authorController.author_detail) // GET one Author
    .put(authorController.author_update) // PUT update an Author
    .delete(authorController.author_delete); // DELETE an Author

/// GENRE ROUTES ///

router.route("/genres")
    .get(genreController.genre_list) // GET list of all Genres
    .post(genreController.genre_create); // POST create a new Genre

router.route("/genres/:id")
    .get(genreController.genre_detail) // GET one Genre
    .put(genreController.genre_update) // PUT update a Genre
    .delete(genreController.genre_delete); // DELETE a Genre

/// BOOKINSTANCE ROUTES ///

// CRUD operations for BookInstances
router.route("/bookinstances")
    .get(bookInstanceController.bookinstance_list) // GET list of all BookInstances
    .post(bookInstanceController.bookinstance_create); // POST create a new BookInstance

router.route("/bookinstances/:id")
    .get(bookInstanceController.bookinstance_detail) // GET one BookInstance
    .put(bookInstanceController.bookinstance_update) // PUT update a BookInstance
    .delete(bookInstanceController.bookinstance_delete); // DELETE a BookInstance

module.exports = router;
