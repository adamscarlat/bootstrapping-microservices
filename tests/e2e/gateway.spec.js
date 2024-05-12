// @ts-check
const { test, expect } = require('@playwright/test');
const { describe } = test;

//
// An example of running ab end-to-end test against our microservices application using Playwright.
//
describe("flixtube front end", () => {
  test("can list videos", async ({ page }) => {
    // Visit the Flixtube web page (NOTE: The base URL is set in the Playwright configuration file).
    await page.goto(`/`);

    // Check that we have two items in the video list.
    const videos = page.locator("#video-list>div");
    await expect(videos).toHaveCount(2);

    const firstVideo = videos.nth(0).locator("a"); // Check the first item in the video list.
    await expect(firstVideo).toHaveText("SampleVideo_1280x720_5mb.mp4"); // Make sure file name is correct.
    await expect(firstVideo).toHaveAttribute("href", "/video?id=1"); // Make sure link is correct.

    const secondVideo = videos.nth(1).locator("a"); // Check the second item in the video list.
    await expect(secondVideo).toHaveText("SampleVideo_1280x720_5mb.mp4"); // Make sure file name is correct.
    await expect(secondVideo).toHaveAttribute("href", "/video?id=2"); // Make sure link is correct.
  });
});