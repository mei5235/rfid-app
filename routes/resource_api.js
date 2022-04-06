var express = require('express');
var bodyParser = require('body-parser');

var utli = require('../utli/utli');
var db = require("../utli/db");


var router = express.Router();
router.use(bodyParser.urlencoded({ extended: false }));
router.use(bodyParser.json());

// TODO remap apis

/* GET get book */
router.get('/', function (req, res, next) {
  // console.log(req.query)
  db.pool.getConnection((err, conn) => {
    conn.query('SELECT * FROM Books', function (err, rows) {
      if (err) throw err;
      res.json({data:rows});
      conn.release();
    });
  });
});

router.post('/scan',(req,res) => {
  console.log(`[${utli.currentTime}] INFO: `,req.body);
  console.log(`[${utli.currentTime}] INFO: tag info received`);
  res.json({msg:"done"});
})



module.exports = router;