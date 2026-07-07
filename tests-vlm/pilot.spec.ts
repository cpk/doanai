import { test } from './fixture';

// Pilot GĐ1: xác nhận Midscene + model đã cấu hình hoạt động end-to-end.
// Yêu cầu: app dev server đang chạy (cd ../app && npm run dev) và .env đã có API key.
test('pilot: VLM thao tác được trang Vite mặc định', async ({ page, ai, aiAssert }) => {
  await page.goto('http://localhost:5173');
  await page.waitForLoadState('networkidle');

  await ai('Click the button that shows a count');
  await aiAssert('The button label now shows "count is 1"');

  await ai('Click the same count button two more times');
  await aiAssert('The button label now shows "count is 3"');
});
