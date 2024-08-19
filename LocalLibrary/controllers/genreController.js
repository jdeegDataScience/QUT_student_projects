const mongoose = require("mongoose");

const Genre = require("../models/genre");
const Book = require("../models/book");

const { body, validationResult } = require("express-validator");
const asyncHandler = require("express-async-handler");

// Display list of all Genre.
exports.genre_list = asyncHandler(async (req, res, next) => {
  const allGenres = await Genre.find().sort({ name: 1 }).exec();
  res.json(allGenres);
});

// Display detail page for a specific Genre.
exports.genre_detail = asyncHandler(async (req, res, next) => {
  // Check if the provided ID is a valid ObjectId
  if (!mongoose.Types.ObjectId.isValid(req.params.id)) {
    return res.status(400).json({ error: "Invalid genre ID" });
  }
  
  // Get details of genre and all associated books (in parallel)
  const [genre, booksInGenre] = await Promise.all([
    Genre.findById(req.params.id).exec(),
    Book.find({ genre: req.params.id }, "title summary").exec(),
  ]);
  if (genre === null) {
    // No results.
    const err = new Error("Genre not found");
    err.status = 404;
    return next(err);
  }

  res.json({
    genre: genre,
    genre_books: booksInGenre,
  });
});

// Handle Genre create on POST.
exports.genre_create = [
  // Validate and sanitize the name field.
  body("name", "Genre name must contain at least 3 characters")
    .trim()
    .isLength({ min: 3 })
    .escape(),

  // Process request after validation and sanitization.
  asyncHandler(async (req, res, next) => {
    // Extract the validation errors from a request.
    const errors = validationResult(req);

    // Create a genre object with escaped and trimmed data.
    const genre = new Genre({ name: req.body.name });

    if (!errors.isEmpty()) {
      // There are errors. 
      res.status(400).json({
        genre: genre,
        errors: errors.array(),
      });
      return;
    } else {
      // Data from form is valid.
      // Check if Genre with same name (case insensitive) already exists.
      const genreExists = await Genre.findOne({ name: req.body.name })
        .collation({ locale: "en", strength: 2 })
        .exec();
        
      if (genreExists) {
        res.status(400).json({'error' : 'genre exists'});
      } else {
        await genre.save();
        res.status(200);
        res.json(genre);
      }
    }
  }),
];

// Handle Genre delete on POST.
exports.genre_delete = asyncHandler(async (req, res, next) => {
  // Get details of genre and all associated books (in parallel)

  // Check if the provided ID is a valid ObjectId
  if (!mongoose.Types.ObjectId.isValid(req.params.id)) {
    return res.status(400).json({ error: "Invalid genre ID" });
  }
  
  const [genre, booksInGenre] = await Promise.all([
    Genre.findById(req.params.id).exec(),
    Book.find({ genre: req.params.id }, "title summary").exec(),
  ]);

  if (genre == null) {
    // No book found
    return res.status(404).json({ error: 'Genre not found' });
  }

  if (booksInGenre.length > 0) {
    // Genre has books.
    res.status(405).json({
      genre: genre,
      genre_books: booksInGenre,
    });
    return;
  } else {
    // Genre has no books. Delete object and redirect to the list of genres.
    await Genre.findByIdAndDelete(req.params.id);
    return res.status(200).send();
  }
});

// Handle Genre update on POST.
exports.genre_update = [
  // Validate and sanitize the name field.
  body("name", "Genre name must contain at least 3 characters")
    .trim()
    .isLength({ min: 3 })
    .escape(),

  // Process request after validation and sanitization.
  asyncHandler(async (req, res, next) => {
    // Extract the validation errors from a request .
    const errors = validationResult(req);

    // Check if the provided ID is a valid ObjectId
    if (!mongoose.Types.ObjectId.isValid(req.params.id)) {
      return res.status(400).json({ error: "Invalid genre ID" });
    }

    // Check if the provided ID is a valid ObjectId
    const bookExists = await Genre.exists({ _id: req.params.id });
    if (!bookExists) {
      return res.status(404).json({ error: 'Genre not found' });
    }

    // Create a genre object with escaped and trimmed data (and the old id!)
    const genre = new Genre({
      name: req.body.name,
      _id: req.params.id,
    });

    if (!errors.isEmpty()) {
      // There are errors. Render the form again with sanitized values and error messages.
      res.status(400).json({
        genre: genre,
        errors: errors.array(),
      });
      return;
    } else {
      // Data from form is valid. Update the record.
      await Genre.findByIdAndUpdate(req.params.id, genre);
      const newgenre = await Genre.findById(req.params.id);
      res.status(200);
      res.json(newgenre);
    }
  }),
];
