import redis from 'redis';
import { promisify } from 'util';

const client = redis
  .createClient()
  .on('error', (err) => console.log(`Redis client not connected to the server: ${err}`));
client.on('ready', () => console.log('Redis client connected to the server'));

function setNewSchool(schoolName, value) {
  client.set(schoolName, value, redis.print);
  // redis.print
}

async function displaySchoolValue(schoolName) {
  const getFunc = promisify(client.get).bind(client);

  await getFunc(schoolName).then((res) => console.log(res));
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
displaySchoolValue('HolbertonSanF');
