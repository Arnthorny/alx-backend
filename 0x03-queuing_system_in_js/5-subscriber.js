import redis from 'redis';

const subscriber = redis
  .createClient()
  .on('error', (err) => console.log(`Redis client not connected to the server: ${err}`));
subscriber.on('ready', () => console.log('Redis client connected to the server'));

subscriber.subscribe('holberton school channel');

function listener(channel, message) {
  console.log(message);
  if (message === 'KILL_SERVER') {
    subscriber.unsubscribe('holberton school channel');
    process.exit();
  }
}

subscriber.on('message', listener);
