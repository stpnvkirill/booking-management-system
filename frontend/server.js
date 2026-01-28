import express from 'express';
import cors from 'cors';
import pg from 'pg'; // Use require if not using ES modules
import dotenv from 'dotenv';
dotenv.config();
const app = express();
// Allow all origins (for development/testing)
app.use(cors());

// Or specify your React app's exact origin for production
// app.use(cors({ origin: 'https://www.your-react-app-domain.com' }));

const { Pool } = pg;
const pool = new Pool({
  user: process.env.VITE_POSTGRES_USER, //'bms_user',
  host: process.env.VITE_POSTGRES_HOST, //'localhost',
  database: process.env.VITE_POSTGRES_DB, //'bms_db',
  password: process.env.VITE_POSTGRES_PASSWORD, //'bms_pwd',
  port: process.env.VITE_POSTGRES_PORT, //6432,
});
// Or using async/await:
app.get('/', (req, res) => {
  res.send('fine!');
});
app.get('/api/bookings/all', (req, response) => {
  (async () => {
    try {
      const res = await pool.query('SELECT * FROM bookings');
      console.log('Current time from pool (async):', res.rows[0]);
      response.send(res.rows);
    } catch (err) {
      console.error(err);
      response.send(err);
    }
  })();
});

app.listen(88, () => {
  console.log('Server running on http://localhost:88/');
});
// node script.js
