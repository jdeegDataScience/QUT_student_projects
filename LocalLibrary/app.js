const createError = require("http-errors");
const express = require("express");
const cookieParser = require("cookie-parser");
const cors = require("cors");

const indexRouter = require("./routes/index");
const usersRouter = require("./routes/users");
const catalogRouter = require("./routes/catalog"); // Import routes for "catalog" area of site

const app = express();

const RateLimit = require("express-rate-limit");
const limiter = RateLimit({
  windowMs: 1 * 10 * 1000, // 10 seconds
  max: 10,
});

// Apply rate limiter to all requests
app.use(limiter);

// Allow requests from any origin
app.use(cors());

// Set up mongoose connection
const mongoose = require("mongoose");

mongoose.set("strictQuery", false);

const mongoDB = process.env.MONGODB_URI;

main().catch((err) => console.log(err));
async function main() {
  await mongoose.connect(mongoDB);
}

app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());

app.use("/", indexRouter);
app.use("/users", usersRouter);
app.use("/catalog", catalogRouter); // Add catalog routes to middleware chain.

// catch 404 and forward to error handler
app.use(function (req, res, next) {
  next(createError(404, 'Endpoint not found'));
});

app.use(function (err, req, res, next) {
  // Log 500 Internal Server Errors
  if (err.status === 500 || !err.status) {
    console.error("Internal Server Error:", err);
  }

  // If the error doesn't have a status, default to 500
  const status = err.status || 500;

  // Send the error response
  res.status(status).json({
    error: {
      status: status,
      message: err.message,
    },
  });
});

// error handler
app.use(function (err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get("env") === "development" ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.json(err);
});

module.exports = app;
