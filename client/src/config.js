const dotenv = require('dotenv');
dotenv.config();

module.exports = {
    db_host: process.env.DB_HOST,
    db_user: process.env.DB_USER,
    db_pass: process.env.DB_PASS,
}