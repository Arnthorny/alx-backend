import kue from 'kue';

const queue = kue.createQueue();

function createPushNotificationsJobs(jobs) {
  if (!Array.isArray(jobs)) throw Error('Jobs is not an array');

  jobs.forEach((jobObj) => {
    const job = queue.create('push_notification_code_3', jobObj).save((err) => {
      if (!err) console.log(`Notification job created: ${job.id}`);
    });

    job
      .on('complete', () => {
        console.log(`Notification job ${job.id} completed`);
      })
      .on('failed', (errorMessage) => {
        console.log(`Notification job ${job.id} failed: ${errorMessage}`);
      })
      .on('progress', (progress) => {
        console.log(`Notification job ${job.id} ${progress}% complete`);
      });
  });
}

export default createPushNotificationsJobs;
