var mysql = require('mysql');

// TODO make config file for login mysql server and select db
var pool = mysql.createPool({
    connectionLimit: 10,
    host: 'localhost',
    user: 'root',
    password: 'R2c20309_1234',
    database: "itp"
});

module.exports = {
    pool : pool,
}