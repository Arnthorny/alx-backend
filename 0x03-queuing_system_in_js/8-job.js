import { Queue } from "kue";

/**
 *
 * @param {Array<Object>} jobs
 * @param {Queue} queue
 * @description - Create Push Notification Jobs
 */
function createPushNotificationsJobs(jobs, queue) {
  if (!Array.isArray(jobs)) throw Error("Jobs is not an array");

  jobs.forEach((jobObj) => {
    const job = queue.create("push_notification_code_3", jobObj);

    job
      .on("complete", () => {
        console.log(`Notification job ${job.id} completed`);
      })
      .on("failed", (errorMessage) => {
        console.log(`Notification job ${job.id} failed: ${errorMessage}`);
      })
      .on("progress", (progress) => {
        console.log(`Notification job ${job.id} ${progress}% complete`);
      })
      .on("enqueue", () => {
        console.log(`Notification job created: ${job.id}`);
      });
    job.save();
  });
}

export default createPushNotificationsJobs;
