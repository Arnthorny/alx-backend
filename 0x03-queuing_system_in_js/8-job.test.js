import { createQueue, Queue } from "kue";
import { expect } from "chai";
import sinon from "sinon";

import createPushNotificationsJobs from "./8-job.js";
import Sinon from "sinon";

const listOfJobs = [
  {
    phoneNumber: "4153518780",
    message: "This is the code 1234 to verify your account",
  },
  {
    phoneNumber: "4153511790",
    message: "This is the code 4123 to verify your account",
  },
];

describe("createPushNotificationsJobs", function () {
  /**
   * @type {Sinon.SinonSpy}
   */
  let spyConsole;

  /** @type {Queue} queue_obj*/
  const queue_obj = createQueue();

  beforeEach(function () {
    spyConsole = sinon.spy(console, "log");
  });

  afterEach(() => {
    spyConsole.restore();
  });

  before(function () {
    queue_obj.testMode.enter(false);
  });

  afterEach(function () {
    queue_obj.testMode.clear();
  });

  after(function () {
    queue_obj.testMode.exit();
  });

  it("display a error message if jobs is not an array", function () {
    expect(createPushNotificationsJobs.bind({}, "jobs", queue_obj)).to.throw(
      "Jobs is not an array"
    );
  });

  it("create two new jobs to the queue", function (done) {
    createPushNotificationsJobs(listOfJobs, queue_obj);
    expect(queue_obj.testMode.jobs.length).to.equal(2);

    expect(queue_obj.testMode.jobs[0].data.message).to.equal(
      listOfJobs[0].message
    );
    expect(queue_obj.testMode.jobs[1].data.phoneNumber).to.eql(
      listOfJobs[1].phoneNumber
    );
    done();
  });
});
