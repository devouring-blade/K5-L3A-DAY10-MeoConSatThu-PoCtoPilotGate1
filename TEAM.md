# Team

## Thông tin nhóm

- Tên nhóm: `MeoConSatThu`
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-MeoConSatThu-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): S3

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 |Nguyễn Sỹ Huy Kiên| 2A202603641| kỹ sư cổng, sản phẩm và kinh doanh, vận hành và pháp lý     | có            |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## NguyenSyHuyKien-2A202603641

### Phần việc phụ trách

Một mình phụ trách cả ba vai: Phiếu A, Phiếu B B0–B8; lab10/guards.py và config/operating_gates.json. Đã thực hiện CP4 với S3; Phiếu C C0–C12, lab10/monitors.py và cấu hình vòng 2.

### Đóng góp cụ thể

Đã điền và tìm hiểu tiêu chí Phiếu A, cấu hình Git và ký/push tiêu chí. Sử dụng ChatGPT để giải thích đề, soát phiếu, đề xuất ngưỡng; sau đó giao ChatGPT đọc code, viết ba họ cổng, chạy baseline/regression/behavioral test và soạn Phiếu B/runbook trên bản sao repo. Code và lập luận CP3 có AI hỗ trợ trực tiếp; không nhận là đã tự viết toàn bộ. Cần tự đọc, kiểm tra và giải thích được trước demo.

### Bằng chứng

Commit ký: 743a8af. Hash tiêu chí: 2d271a64dac34f52e14495fafc76f9167dd7c7cac5097e6999b781129543afd5.

Baseline: R-base-before-20261118-164423-bde05c.
Prepared: R-base-prepared-20261118-164857-29a8f5.
Hash chốt vòng 1: 5c5bf8ae.
Chi tiết các lần đo và trace: Phiếu B B0, B2, B7.3, runs/journal.jsonl và runs/cp3-evidence/.

### Exit ticket

Chưa viết exit ticket cuối buổi; bổ sung sau CP4/CP5 bằng điều bản thân đã học và điều còn chưa chắc.

### Bổ sung đóng góp CP4 (AI hỗ trợ trực tiếp)

Kiên nhận thẻ S3 và chạy grade trước sửa trên repo E (8417c32). ChatGPT đọc report đã gửi, phân tích guard quá rộng khi thiếu attribution; sửa G2, mở phạm vi thử all, thêm unknown_delay_cause_rate, chạy S3/base/public tests và soạn Phiếu C, submission.json. Chưa sửa evaluator/MANIFEST hoặc lấy thẻ khác; kết quả tổng còn FAIL do bộ kiểm đòi thẻ nhóm khác. Giữ v2 Cải tiến thêm.

Grade cuối: `R-S3-grade-20261118-173134-fc580c`; code hash fc580cb9e10e; S3 60/60, base110/110, monitor mới sáng; criteria/snapshot giữ nguyên. Nội dung cần được Kiên đọc và giải thích trước demo.

### Exit ticket — bản nháp để Kiên tự xác nhận

Điều đã được giải thích và thực hành trong bài: tỷ lệ đạt tổng thể không thay thế ngưỡng an toàn, chi phí bình quân phải tính cả người duyệt, và thiếu căn cứ quy lỗi hãng không đồng nghĩa khách mất quyền hoàn phí. Điều còn chưa chắc: khả năng chịu burst/race và chất lượng tracking thật; cần đo lại trước Gate 2.
