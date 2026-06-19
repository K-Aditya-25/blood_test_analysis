import { chromium } from "@playwright/test";

const BASE = "http://localhost:3000";

async function main() {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

  // Light mode — full dashboard
  await page.goto(BASE, { waitUntil: "networkidle" });
  await page.waitForTimeout(1500);
  await page.screenshot({
    path: "screenshots/dashboard-light.png",
    fullPage: true,
  });

  // Dark mode
  await page.getByRole("button", { name: /theme|toggle|sun|moon/i }).click();
  await page.waitForTimeout(800);
  await page.screenshot({
    path: "screenshots/dashboard-dark.png",
    fullPage: true,
  });

  // Hero / wellness ring close-up (light)
  await page.getByRole("button", { name: /theme|toggle|sun|moon/i }).click();
  await page.waitForTimeout(500);
  const hero = page.locator("main").first();
  await hero.screenshot({ path: "screenshots/hero.png" });

  // Section card detail
  const firstSection = page.locator('[class*="section"], [data-section]').first();
  if (await firstSection.isVisible().catch(() => false)) {
    await firstSection.screenshot({ path: "screenshots/section-detail.png" });
  } else {
    // Fallback: screenshot the top portion of the page
    await page.screenshot({
      path: "screenshots/section-detail.png",
      clip: { x: 0, y: 400, width: 1440, height: 500 },
    });
  }

  await browser.close();
  console.log("Screenshots saved to screenshots/");
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
