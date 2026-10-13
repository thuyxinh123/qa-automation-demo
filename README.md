# QA Automation Demo – UI & API Testing

Dự án tự học automation test gồm 2 phần:

- **UI test** bằng **Playwright + Pytest** trên trang demo [saucedemo.com](https://www.saucedemo.com), áp dụng mô hình **Page Object Model**.
- **API test** bằng **requests + jsonschema** trên API demo [restful-booker](https://restful-booker.herokuapp.com/apidoc/index.html).

Báo cáo kết quả xuất ra file HTML bằng **pytest-html**, và tự chạy trên **GitHub Actions** mỗi lần push code.

## Phạm vi test (16 test case)

| Nhóm | Test case | Kỹ thuật |
| --- | --- | --- |
| UI – Đăng nhập | Đăng nhập thành công; user bị khóa; sai mật khẩu; bỏ trống username; bỏ trống password | Data-driven (`parametrize`), negative test |
| UI – Giỏ hàng | Thêm/xóa sản phẩm, số trên icon giỏ hàng cập nhật đúng | Kiểm tra trạng thái |
| UI – Sắp xếp | Sắp xếp giá thấp → cao | So sánh danh sách |
| UI – Thanh toán | Subtotal = tổng giá sản phẩm, Total = Subtotal + Tax; đặt hàng thành công | Kiểm tra tính đúng của số tiền, E2E |
| UI – Validate | Bỏ trống mã bưu chính thì báo lỗi | Negative test |
| API – CRUD | Tạo, đọc, sửa, xóa booking | Status code, so sánh dữ liệu |
| API – Phân quyền | Sửa booking không có token → 403; sai mật khẩu → không trả token | Security cơ bản |
| API – Schema | Response đúng cấu trúc JSON | JSON Schema validation |

## Cấu trúc thư mục

```
qa-automation-demo/
├── pages/                  # Page Object: mỗi màn hình 1 class
│   ├── login_page.py
│   ├── inventory_page.py
│   └── checkout_page.py
├── tests/
│   ├── ui/                 # Test giao diện (Playwright)
│   └── api/                # Test API (requests)
├── .github/workflows/      # Tự chạy test trên GitHub Actions
├── requirements.txt        # Thư viện cần cài
└── pytest.ini              # Cấu hình pytest
```

## Cách chạy

```bash
# 1. Tạo môi trường ảo và cài thư viện
python -m venv .venv
.venv\Scripts\activate          # Windows (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
playwright install chromium

# 2. Chạy toàn bộ test
pytest

# Chỉ chạy UI hoặc API
pytest -m ui
pytest -m api

# Xem trình duyệt chạy (không ẩn)
pytest -m ui --headed --slowmo 500

# Xuất báo cáo HTML
pytest --html=report.html --self-contained-html
```

## Công cụ

Python · Pytest · Playwright · requests · jsonschema · pytest-html · Git · GitHub Actions
