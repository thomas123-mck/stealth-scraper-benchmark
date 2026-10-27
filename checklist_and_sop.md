# SOP & CHECKLIST TRIỂN KHAI B2B SAAS AFFILIATE (ZENROWS & PROXYSCRAPE)

## BƯỚC 1: LẤY LINK AFFILIATE CHÍNH CHỦ (WALTER THỰC HIỆN)

### 1. ProxyScrape (Ưu tiên số 1 - Duyệt tự động tức thì)
- URL đăng ký: `https://affiliates.proxyscrape.com/`
- Cơ chế duyệt: TỰ ĐỘNG 100% (Auto approval) - Lấy link ngay sau khi bấm đăng ký.
- Chính sách: 50% hoa hồng định kỳ trọn đời (recurring lifetime).
- Thanh toán: Tối thiểu chỉ từ 10 USD qua Tremendous / PayPal.
- Link nhận về có dạng: `https://proxyscrape.com?ref=walter...`

### 2. ZenRows (Ưu tiên số 2 - Duyệt qua đối tác Rewardful)
- URL đăng ký: `https://www.zenrows.com/affiliate`
- Cơ chế duyệt: Xét duyệt thủ công trong 24-48h (Manual approval).
- Thông tin khai báo trong form:
  * Traffic Source / Promotion Channel: "Developer blog, GitHub open-source scraping tools & technical Reddit case studies."
  * Website: Link GitHub của bạn hoặc Portfolio.
- Chính sách: 35% hoa hồng định kỳ trong 12 tháng (tự động nâng lên 40% khi đạt mốc doanh số).
- Thanh toán: Tối thiểu 50 EUR hàng tháng.
- Link nhận về có dạng: `https://www.zenrows.com/?via=walter...`

---

## BƯỚC 2: CẬP NHẬT LINK VÀO BỘ VŨ KHÍ (REPLACE PLACEHOLDERS)

Mở 2 file sau trong thư mục `C:/Projects/b2b-saas-affiliate-engine`:
1. `README.md`
2. `articles/reddit_case_study.md`

Tìm và thay thế 2 cụm sau bằng link thật của Walter:
- `YOUR_PROXYSCRAPE_AFFILIATE_LINK` -> Thay bằng link ProxyScrape
- `YOUR_ZENROWS_AFFILIATE_LINK` -> Thay bằng link ZenRows

---

## BƯỚC 3: ĐẨY REPOSITORY LÊN GITHUB

Khởi tạo git và push lên GitHub cá nhân của Walter:
```bash
cd "C:/Projects/b2b-saas-affiliate-engine"
git init
git add .
git commit -m "feat: initial commit for stealth scraping benchmark suite"
git branch -M main
git remote add origin https://github.com/your-username/stealth-scraper-benchmark.git
git push -u origin main
```
*Lưu ý: Đặt tên repository chuẩn SEO để thu hút search traffic: `stealth-scraper-benchmark` hoặc `anti-bot-scraping-toolkit`.*

---

## BƯỚC 4: PHÂN PHỐI BÀI VIẾT KỸ THUẬT (DISTRIBUTION)

1. Đăng bài lên Dev.to / Hashnode / Medium:
   - Dùng nội dung trong `articles/reddit_case_study.md` hoặc chuyển thể từ `README.md`.
   - Gắn các tag: `#webscraping`, `#python`, `#datascience`, `#cloudflare`.

2. Đăng bài thảo luận trên Reddit:
   - Đăng vào `r/webscraping`, `r/Python`, `r/dataengineering`.
   - Bài viết tập trung 100% vào số liệu benchmark và code giải pháp (Zero spam). Người đọc quan tâm sẽ tự click link GitHub hoặc link tool ở cuối bài.
