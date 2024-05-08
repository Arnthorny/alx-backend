import express from 'express';
import redis from 'redis';
import kue from 'kue';
import { promisify } from 'util';

let queue;
const client = redis
  .createClient()
  .on('error', (err) => console.log(`Redis client not connected to the server: ${err}`));
client.on('ready', () => {
  console.log('Redis client connected to the server')
  queue = kue.createQueue();
});

const app = express();
let reservationEnabled = true;


function reserveSeat(number) {
  client.set('available_seats', number, redis.print);
}
reserveSeat(50);

async function getCurrentAvailableSeats() {
  const getFunc = promisify(client.get).bind(client);

  const seats = await getFunc('available_seats');
  return seats;
}

app.get('/available_seats', async (req, res) => {
  await getCurrentAvailableSeats().then((seatCount) => {
    res.json({ numberOfAvailableSeats: seatCount });
  });
});

app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) res.json({ status: 'Reservation are blocked' });
  else {
    const jobObj = { reserve_date: new Date().toISOString() };
    const job = queue.create('reserve_seat', jobObj).save((err) => {
      if (!err) res.json({ status: 'Reservation in process' });
      else res.json({ status: 'Reservation failed' });
    });

    job
      .on('complete', () => {
        console.log(`Seat reservation job JOB_ID ${job.id} completed`);
      })
      .on('failed', (errorMessage) => {
        console.log(`Seat reservation job ${job.id} failed: ${errorMessage}`);
      });
  }
});

app.get('/process', (req, res) => {
  res.json({ status: 'Queue processing' });
  queue.process('reserve_seat', async (job, done) => {
    const seats = await getCurrentAvailableSeats();
    if (seats - 1 === 0) reservationEnabled = false;
    if (seats >= 1) {
      reserveSeat(seats - 1);
      done();
    } else done(Error('Not enough seats available'));
  });
});

const port = 1245;
const host = '0.0.0.0';

app.listen(port, host, () => {
  console.log(`Server is running on port ${port} on ${host}`);
});
