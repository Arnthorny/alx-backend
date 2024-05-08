import redis from 'redis';

const client = redis
  .createClient()
  .on('error', (err) => console.log(`Redis client not connected to the server: ${err}`));
client.on('ready', () => console.log('Redis client connected to the server'));
// client.hSet('HolbertonSchools', 'Portland', 50, redis.print)
// client.hSet('HolbertonSchools', 'Seattle', 80, redis.print)
// client.hSet('HolbertonSchools', 'New York', 20, redis.print)
// client.hSet('HolbertonSchools', 'Bogota', 50, redis.print)
// client.hSet('HolbertonSchools', 'Cali', 40, redis.print)
// client.hSet('HolbertonSchools', 'Paris', 2, redis.print)

const arr = [
  ['Portland', '50'],
  ['Seattle', '80'],
  ['New York', '20'],
  ['Bogota', '20'],
  ['Cali', '40'],
  ['Paris', '2'],
];
// client.HSET('HolbertonSchools', ...arr, redis.print);

arr.forEach((val) => client.HSET('HolbertonSchools', ...val, redis.print));
client.HGETALL('HolbertonSchools', (_, res) => console.log(res));
