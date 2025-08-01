const express = require('express');
const cors = require('cors');
const path = require('path');
const app = express();

const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));

const PORT = 3000;
const API_KEY = '1bd7c8923e7d8762fea40468';
const BASE_URL = `https://v6.exchangerate-api.com/v6/${API_KEY}`;

app.use(cors());
app.use(express.json());

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/currencies', async (req, res) => {
    try {
        const response = await fetch(`${BASE_URL}/codes`);
        const data = await response.json();

        console.log("Currency API response:", data);
        res.json(data.supported_codes || []);
    } catch (err) {
        console.error("Currency fetch error:", err);
        res.status(500).json({ error: 'Failed to fetch currencies' });
    }
});

app.post('/convert', async (req, res) => {
    const { currency1, currency2, amount } = req.body;

    try {
        const response = await fetch(`${BASE_URL}/pair/${currency1}/${currency2}`);
        const data = await response.json();

        console.log("Conversion API response:", data);

        if (data.result !== 'success') {
            return res.status(400).json({ error: 'Invalid currency pair' });
        }

        const rate = data.conversion_rate;
        const converted = (rate * parseFloat(amount)).toFixed(2);
        res.json({ rate, converted });
    } catch (err) {
        console.error("Conversion error:", err);
        res.status(500).json({ error: 'Conversion failed' });
    }
});

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
