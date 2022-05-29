var express = require('express');
var bodyParser = require('body-parser');

var db = require("../utli/db");


var router = express.Router();
router.use(bodyParser.urlencoded({ extended: false }));
router.use(bodyParser.json());

// TODO remap apis

/* GET get all book */
router.get('/book', function (req, res, next) {
  // console.log(req.query)
  db.pool.getConnection((err, conn) => {
    conn.query(`SELECT * FROM Books`, function (err, rows) {
      if (err) throw err;
      res.json({data:rows});
      conn.release();
    });
  });
});

/* GET get specific book */
router.get('/book/:id', function (req, res, next) {
  db.pool.getConnection((err, conn) => {
    conn.query(`SELECT * FROM Books WHERE callnum = '${req.params.id}'`, function (err, rows) {
      if (err) throw err;
      res.json({data:rows});
      conn.release();
    });
  });
});

/* GET get all bookshelf */
router.get('/bookshelf', function (req, res, next) {
  db.pool.getConnection((err, conn) => {
    conn.query('SELECT bs.bsid, bs.tagsn, g.name FROM `Bookshelves` as bs INNER JOIN Genres as g on bs.gid = g.gid;', function (err, rows) {
      if (err) throw err;
      res.json({data:rows});
      conn.release();
    });
  });
});

/* GET get a specific bookshelf by bsid*/
router.get('/bookshelf/bsid/:id', function (req, res, next) {
  db.pool.getConnection((err, conn) => {
    conn.query(`SELECT bs.bsid, bs.tagsn, g.name FROM Bookshelves as bs INNER JOIN Genres as g on bs.gid = g.gid where bs.bsid = '${req.params.id}';`, function (err, rows) {
      if (err) throw err;
      res.json({data:rows});
      conn.release();
    });
  });
});

/* GET get a specific bookshelf */
router.get('/bookshelf/tagsn/:id', function (req, res, next) {
  db.pool.getConnection((err, conn) => {
    conn.query(`SELECT bs.bsid, bs.tagsn, g.name FROM Bookshelves as bs INNER JOIN Genres as g on bs.gid = g.gid where bs.tagsn = '${req.params.id}';`, function (err, rows) {
      if (err) throw err;
      res.json({data:rows});
      conn.release();
    });
  });
});

/* POST upload tag s/n  */
router.post('/checkBook',(req,res) => {
  // console.log(`[${utli.currentTime}] INFO: `,req.body);
  // console.log(`[${utli.currentTime}] INFO: tag info received`);
  // res.json({msg:"done"});
  console.log(req.body.data)
  // console.log(req.body.data.shelfsn)
  let sql = `SELECT tb.tbid, b.callnum, b.name, g.name, b.publisher, b.language, b.qty 
  FROM TagBook as tb 
  INNER JOIN Books as b ON tb.callnum = b.callnum 
  INNER JOIN Genres as g ON g.gid = b.genre 
  INNER JOIN Bookshelves as bs ON tb.bsid = bs.bsid
  where tb.tagsn = '${req.body.data.booksn}' AND bs.tagsn = '${req.body.data.shelfsn}'`
  db.pool.getConnection((err, conn) => {
    conn.query(sql, function (err, rows) {
      if (err) throw err;
      console.log(rows.length);
      if (rows.length >= 1){
        res.json({
          code:101,
          msg:'located in right bookshelf'
        })
      }else{
        res.json({
          code:100,
          msg:'located in wrong bookshelf'
        });
      }
      
      conn.release();
    });
  });
  
  // res.json({msg:"done"});
})

// get book location => bookshlef genre name
router.get('/getBSLocal/:callnum',(req,res)=>{
  let sql = `SELECT g.name , b.callnum, b.name from Books as b 
  INNER JOIN Genres as g ON g.gid = b.genre 
  INNER JOIN Bookshelves as bs ON bs.gid = g.gid 
  WHERE b.callnum = '${req.params.callnum}'`
  console.log(req.params.callnum)

  db.pool.getConnection((err, conn) => {
    conn.query(sql, function (err, rows) {
      if (err) throw err;
      res.json({data:rows});
      conn.release();
    });
  });
})

router.get('/test',(req,res) => {
  res.json({msg:fuck})
})

router.post('/submitStat', (req, res) => {
 let sql = `INSERT INTO Sessions (totoalBook, scannedBook) VALUES (${req.body.data.totalBook}, ${req.body.data.scannedBook})`
 db.pool.getConnection((err, conn) => {
  conn.query(sql, function (err, rows) {
    if (err) throw err;
    // console.log(rows.length);
    // if (rows.length >= 1){
    //   res.json({
    //     code:101,
    //     msg:'located in right bookshelf'
    //   })
    // }else{
    //   res.json({
    //     code:100,
    //     msg:'located in wrong bookshelf'
    //   });
    // }
    res.json({
      msg:'statistic submitted'
    })
    
    conn.release();
  });
});
})



module.exports = router;