const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
app.use(bodyParser.json());
app.use(cors());

const mongoUri = process.env.MONGO_URI || 'mongodb://localhost:27017/dealersdb';
mongoose.connect(mongoUri, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(()=> console.log('Mongo connected'))
  .catch(err => console.error('Mongo connection error', err));

const DealerSchema = new mongoose.Schema({
  id: Number,
  full_name: String,
  city: String,
  state: String,
  address: String,
});

const ReviewSchema = new mongoose.Schema({
  dealer_id: Number,
  name: String,
  review: String,
  rating: Number,
  created_at: { type: Date, default: Date.now }
});

const Dealer = mongoose.model('Dealer', DealerSchema);
const Review = mongoose.model('Review', ReviewSchema);

// Seed data
app.get('/seed', async (req, res) => {
  await Dealer.deleteMany({});
  await Review.deleteMany({});
  await Dealer.insertMany([
    { id: 1, full_name: 'Kansas Motors', city: 'Wichita', state: 'Kansas', address: '123 Main St' },
    { id: 2, full_name: 'Denver Auto', city: 'Denver', state: 'Colorado', address: '8th Ave' },
    { id: 3, full_name: 'NYC Cars', city: 'New York', state: 'New York', address: '5th Ave' },
  ]);
  await Review.insertMany([
    { dealer_id: 1, name: 'Alice', review: 'Great service', rating: 5 },
    { dealer_id: 1, name: 'Bob', review: 'Okay experience', rating: 3 },
    { dealer_id: 2, name: 'Cara', review: 'Loved the car', rating: 5 },
  ]);
  res.json({ ok: true });
});

// Endpoints
app.get('/dealers', async (req,res) => { res.json(await Dealer.find({})); });
app.get('/dealer/:id', async (req,res) => { res.json(await Dealer.findOne({id: parseInt(req.params.id)})); });
app.get('/dealer/details', async (req,res) => { res.json(await Dealer.find({})); });
app.get('/dealer/state/:state', async (req,res) => { res.json(await Dealer.find({state: new RegExp(req.params.state,'i')})); });
app.get('/dealer/reviews/:id', async (req,res) => { res.json(await Review.find({dealer_id: parseInt(req.params.id)})); });
app.post('/dealer/:id/add_review', async (req,res) => {
  const { name, review, rating } = req.body;
  const r = new Review({ dealer_id: parseInt(req.params.id), name, review, rating: rating || 5 });
  await r.save();
  res.status(201).json({ ok: true, review: r });
});

const port = process.env.PORT || 3030;
app.listen(port, () => console.log(`Server running on ${port}`));
