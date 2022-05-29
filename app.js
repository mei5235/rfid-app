var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');

var logger = require('morgan');

var cors = require('cors');

// var indexRouter = require('./routes/index');
// var usersRouter = require('./routes/users');
var apiRouter = require('./routes/resource_api.js');

var app = express();
app.use('/api',apiRouter);

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use(cors());

app.get('/',(req,res) => {
  res.render('index', { title: 'Express' });
})

app.get('/stat', (req,res) => {
  res.render('statistics');
});

app.get('/mobile', (req,res) => {
  res.render('mobile_client');
})

//depleted
app.get('/mobile_demo', (req,res) => {
  res.render('mobile_demo');
})

app.get('/inventory',(req,res)=>{
  res.render('inventory');
});

app.get('/session_man',(req, res) => {
  res.render('session_management');
})

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
