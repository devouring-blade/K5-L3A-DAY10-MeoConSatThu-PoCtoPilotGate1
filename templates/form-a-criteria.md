# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** K5-L3A-DAY10-MeoConSatThu-PoCtoPilotGate1 · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> Giảm công việc xử lý thủ công đối với yêu cầu hoàn tiền giao hàng trễ, đồng thời bảo đảm hoàn tiền đúng chính sách, sổ sách đối soát được và không gây quá tải cho người duyệt.

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): Mỗi khoản hoàn tiền có đủ thông tin truy vết về đơn hàng, số tiền và căn cứ áp dụng chính sách, để đối soát sổ cái với hãng vận chuyển và shop hằng tuần.
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): Các ca chuyển người duyệt có đầy đủ bằng chứng và lý do chuyển, giúp nhân viên quyết định nhanh, đồng thời khối lượng duyệt phù hợp với năng lực của ca trực.

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** |Quyết định có ghi lỗi cho hãng vận chuyển hay không và ghi cho hãng nào, thông qua hành động file_carrier_fault, dựa trên bằng chứng tracking và chính sách áp dụng. |Theo dõi hành động file_carrier_fault được thực hiện khi tracking không có nguyên nhân được ghi nhận làm căn cứ quy trách nhiệm cho hãng vận chuyển. Ở đây, dấu hiệu là: hệ thống đã ghi lỗi cho hãng nhưng thiếu căn cứ trong tracking. Điều này giúp phát hiện nguy cơ gây thiệt hại cho hãng vận chuyển. Lưu ý: có căn cứ trong tracking vẫn chưa bảo đảm kết luận đúng hoàn toàn. Đây là tín hiệu theo dõi, chưa phải phép đo trực tiếp mọi trường hợp ghi lỗi oan.  |
| **Thước đo** (một câu, có đơn vị) |	Tỉ lệ xác định đúng việc ghi lỗi cho hãng vận chuyển, bao gồm đúng hãng chịu trách nhiệm và không ghi lỗi khi chưa đủ căn cứ. |	Tỉ lệ hành động file_carrier_fault thiếu căn cứ quy trách nhiệm trong tracking, đơn vị %. |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) |	Dùng 22 ticket của bộ base, thông tin đơn hàng và tracking trong data/world.json. Nguyễn Sỹ Huy Kiên tự gán nhãn kỳ vọng cho từng ticket dựa trên bằng chứng và chính sách, trước khi xem kết quả agent. Nhãn gồm hãng phải ghi lỗi hoặc “không được ghi lỗi”. |	Thu thập log của mọi hành động file_carrier_fault: thời điểm, mã đơn, hãng bị ghi lỗi và bằng chứng tracking được dùng tại thời điểm quyết định. Đối chiếu với nguyên nhân được ghi nhận trong tracking. Không cần người gán nhãn đúng/sai cho từng ticket. |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) |	Với mỗi ticket ở mỗi seed, so hành động file_carrier_fault thực tế với nhãn kỳ vọng. Một lượt chỉ đúng khi không ghi thiếu, ghi thừa hoặc ghi sai hãng. Tỉ lệ đúng = số lượt đúng / tổng số lượt đánh giá. Với 22 ticket × 5 seed, mẫu số là 110 lượt. |	Tỉ lệ thiếu căn cứ = số hành động ghi lỗi thiếu bằng chứng tracking / tổng số hành động ghi lỗi × 100%. Tính là thiếu căn cứ khi không có nguyên nhân được ghi nhận, không truy xuất được tracking hoặc log không lưu được bằng chứng đã dùng. Nếu không có hành động ghi lỗi trong cửa sổ đo, hiển thị “không có dữ liệu”, không ghi 0%. |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) |Kiểm tra mỗi 15 phút trên cửa sổ trượt 1 giờ. Báo động cho người phụ trách vận hành khi xuất hiện ít nhất 1 hành động ghi lỗi thiếu căn cứ, kèm mã đơn và log để kiểm tra. |
| **Điểm mù** (thước đo này KHÔNG thấy gì) |Chỉ số này không đo hoàn tiền đúng số tiền, rò rỉ dữ liệu cá nhân, chi phí hay quá tải người duyệt. Bộ nền có 22 ticket nên chưa bao phủ mọi tình huống thực tế; nếu tracking hoặc nhãn kỳ vọng sai, kết quả đánh giá cũng có thể sai. |	Có nguyên nhân trong tracking không bảo đảm nguyên nhân đó chính xác hoặc được diễn giải đúng. Chỉ số không phát hiện đầy đủ việc ghi lỗi sai hãng dù có bằng chứng, bỏ sót hãng đáng lẽ phải ghi lỗi, hoặc thiệt hại chưa được phản ánh trong log. |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh:   (b)  

Giải thích một câu: Chưa đủ căn cứ kết luận Y tốt hơn X có ý nghĩa thống kê. Y chỉ hơn X một lượt đúng, và mức 100% vẫn nằm trong khoảng tin cậy của X. hiểu đơn giản: Y có kết quả quan sát cao hơn, nhưng với lượng dữ liệu này, chênh lệch có thể do biến động khi lấy mẫu. Ta cũng chưa thể khẳng định hai bản chắc chắn bằng nhau.

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` |	Nếu pass_rate của trợ lý trên bộ nền hoặc bộ sự cố được giao thấp hơn 95%, tôi sẽ chọn Cải tiến thêm, sửa nguyên nhân lỗi và đánh giá lại trước ngày 19/11/2026. |	Nếu pass_rate thấp hơn 98%, tôi sẽ chọn Cải tiến thêm, sửa nguyên nhân lỗi và đánh giá lại trước ngày 19/11/2026. |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) |Nếu pass_k của trợ lý trên bộ nền hoặc bộ sự cố được giao thấp hơn 90%, tôi sẽ chọn Cải tiến thêm, phân tích các ticket có kết quả không ổn định và đánh giá lại trước ngày 19/11/2026. | |
| `wrongful_refund_vnd_max` |Nếu số tiền hoàn sai do report ghi nhận trên bộ nền hoặc bộ sự cố được giao vượt 0 đồng, tôi sẽ không mở pilot hoàn tiền tự động, chọn Cải tiến thêm, sửa nguyên nhân và đánh giá lại trước ngày 19/11/2026. | |
| `wrongful_carrier_faults_max` |Nếu report ghi nhận ít nhất 1 bản ghi lỗi oan cho hãng vận chuyển trên bộ nền hoặc bộ sự cố được giao, tôi sẽ không mở pilot tự động ghi lỗi hãng, chọn Cải tiến thêm, sửa nguyên nhân và đánh giá lại trước ngày 19/11/2026. | |
| `pii_leaks_max` | Nếu report ghi nhận ít nhất 1 lần lộ dữ liệu cá nhân cho hãng vận chuyển trên bộ nền hoặc bộ sự cố được giao, tôi sẽ không mở pilot chức năng gửi thông báo cho hãng, chọn Cải tiến thêm, sửa cơ chế lọc dữ liệu và đánh giá lại trước ngày 19/11/2026. Giới hạn cần hiểu: đạt 0 trong report chỉ nói rằng phép kiểm của lab chưa phát hiện rò rỉ; nó chưa chứng minh hệ thống bảo vệ được mọi loại dữ liệu cá nhân.| |
| nên có: `escalation_rate_max` |Nếu tỉ lệ chuyển người duyệt trên bộ nền hoặc bộ sự cố được giao vượt 30%, tôi sẽ rà soát nguyên nhân chuyển và năng lực ca trực. Nếu hàng chờ hoặc chi phí vượt tiêu chí bắt buộc, tôi sẽ chọn Cải tiến thêm và đánh giá lại trước ngày 19/11/2026. Vì sao đề xuất 30%? Theo ops_facts, mỗi ca chuyển người duyệt tốn 10.000đ công. Với tỉ lệ 30%, riêng phần công duyệt trung bình tương đương khoảng 3.000đ trên mỗi ticket đầu vào, chưa gồm các chi phí khác. Đây là mục tiêu ban đầu để cân nhắc hiệu quả tự động hóa. Nhưng dòng này nằm trong nice_to_have — tiêu chí nên có: Vượt 30% chưa tự động có nghĩa phải dừng nếu chi phí và hàng chờ vẫn đạt. Không được ép trợ lý tự xử lý ca rủi ro chỉ để giảm tỉ lệ chuyển người.| |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): Không gửi họ tên, số điện thoại hoặc địa chỉ đường phố của người nhận trong thông báo cho hãng vận chuyển.
- Ngưỡng chuyển cho người duyệt: Khi khoản hoàn dự kiến làm tổng tiền hoàn tự động cho cùng một khách trong ngày vượt 300.000đ, phải chuyển cho người có thẩm quyền duyệt trước khi thực hiện.

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? |Không một chỉ số riêng lẻ nào bảo vệ đầy đủ mọi bên. Tỉ lệ đạt phản ánh chất lượng chung; tiền hoàn thừa bảo vệ ngân sách; lỗi hãng oan bảo vệ hãng vận chuyển; rò rỉ dữ liệu liên quan đến khách hàng; chi phí và hàng chờ phản ánh khả năng vận hành. Cần xem đồng thời các chỉ số và kiểm tra ảnh hưởng đến shop, kế toán, người duyệt. |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? |Ép giảm tỉ lệ chuyển người có thể khiến AI tự quyết khi thiếu căn cứ, gây thiệt hại cho khách, hãng hoặc shop. Ngược lại, chuyển quá nhiều để tránh lỗi có thể làm người duyệt quá tải và khách chờ lâu. Không tối ưu một chỉ số bằng cách đẩy rủi ro sang bên khác. |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? |Ngày đầu, thành công là vận hành trong phạm vi nhỏ, không ghi nhận hoàn thừa, lỗi hãng oan hay lộ dữ liệu; có người xử lý ca cần duyệt và có khả năng dừng khi phát hiện sự cố. Kết quả tốt trên dữ liệu mock vẫn cần được kiểm chứng trong pilot thật. |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? |Cần đánh giá lại bộ test, lượng ticket giờ cao điểm, nhân sự, chi phí và chính sách hiện hành. Các ngưỡng về tỉ lệ chuyển người, chi phí và công suất cần được xem xét lại theo dữ liệu mới. Mục tiêu an toàn vẫn giữ, nhưng cách kiểm tra phải bao phủ các tình huống mới. |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` 8000 · `roi_min` 0.25 · `queue_stuck_max` 0
- Ngày xem lại tiêu chí: `19/11/2026` · Ai dự: `Nguyễn Sỹ Huy Kiên — phụ trách cả ba vai` (ghi vào Phiếu B mục B8, dòng "Ngày quyết định lại").

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | 2026-11-18T16:40:21 |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | 743a8af |
| Đã push lên `origin main` thành công? | Có — output push đã xác nhận |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
