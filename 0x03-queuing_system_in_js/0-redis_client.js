import redis from 'redis';

const redisCli = redis.createClient().on('error', (err) => console.log(`Redis client not connected to the server: ${err}`));
redisCli.on('ready', () => console.log('Redis client connected to the server'));
