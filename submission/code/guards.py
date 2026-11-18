"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


def pre_guard(ctx):
    # G1: dates, not a stale search-index flag, determine the active policy.
    try:
        policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    except (KeyError, ValueError, TypeError):
        policy = None
    if policy is None:
        return Verdict.escalate("Không xác định được chính sách còn hiệu lực; cần người duyệt")
    ctx.log("policy_by_date", policy_id=policy["policy_id"], as_of=ctx.as_of)
    return Verdict.allow(policy_id=policy["policy_id"])


def write_gate(ctx, action):
    # G2: independently authorize money against DB facts before any write.
    if action.get("tool") == "issue_refund":
        order = ctx.tools.lookup_order(action.get("order_id"))
        if not order or order.get("customer_id") != ctx.ticket.get("customer_id"):
            return Verdict.escalate("Không xác minh được chủ đơn")
        if action.get("order_id") != ctx.ticket.get("order_id"):
            return Verdict.escalate("Lệnh hoàn tiền không thuộc đơn trong ticket")
        try:
            policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
            parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
            delay = H.db_delay_days(parcel, ctx.as_of)
            if policy is None:
                return Verdict.escalate("Không có chính sách còn hiệu lực")
            # Missing attribution is not a reason to reject an otherwise eligible refund.
            # G3 separately requires recorded carrier responsibility before writing a fault.
            entitled = H.entitlement_vnd(policy, order, delay, parcel.get("delay_cause"))
        except (KeyError, ValueError, TypeError):
            return Verdict.escalate("Dữ liệu tracking/chính sách không đủ để cấp quyền ghi tiền")
        amount = action.get("amount_vnd")
        if type(amount) is not int or amount <= 0:
            return Verdict.deny("Số tiền hoàn phải là số nguyên dương")
        if action.get("payer", "LOGIX") != "LOGIX":
            return Verdict.escalate("Không có thẩm quyền tự trừ tiền shop")
        if amount > entitled:
            ctx.log("refund_fact_mismatch", proposed=amount, entitled=entitled, db_delay=delay)
            return Verdict.escalate("Đề xuất vượt quyền lợi tính từ tracking DB; cần người xử lý")
        paid = sum(r["amount_vnd"] for r in ctx.tools.ledger_rows(order_id=order["order_id"]))
        if paid + amount > entitled:
            return Verdict.deny("Sổ cái đã ghi tiền: không ghi lặp/vượt quyền lợi của đơn")
        approval_id = action.get("approval_id")
        if approval_id:
            approvals = ctx.tools.lookup_approvals(approval_id=approval_id)
            expected = (ctx.gates or {}).get("operations", {}).get("approver_id")
            valid = any(a.get("status") == "valid" and a.get("expires_at", "") >= ctx.as_of
                        and a.get("ticket_id") == ctx.ticket.get("ticket_id")
                        and a.get("order_id") == order["order_id"]
                        and a.get("customer_id") == order["customer_id"]
                        and a.get("max_vnd", 0) >= amount
                        and (not expected or a.get("approver_id") == expected)
                        for a in approvals)
            if not valid:
                return Verdict.escalate("Phê duyệt sai đối tượng, hết hạn hoặc không đủ thẩm quyền")
        elif amount > policy["auto_limit_vnd"]:
            return Verdict.escalate("Vượt hạn mức tự động của chính sách, cần phê duyệt hợp lệ")
        if not approval_id:
            limits = ctx.tools.ops_limits()
            # The simulator keeps a scenario's ledger/faults in its working world.
            # Count pre-existing rows conservatively when no dated history is available.
            auto_customer = sum(r["amount_vnd"] for r in ctx.tools.ledger_rows(customer_id=order["customer_id"])
                                if not r.get("approval_id"))
            customer_cap = limits.get("max_auto_refund_per_customer_per_day_vnd")
            if customer_cap is not None and auto_customer + amount > customer_cap:
                return Verdict.escalate("Tổng hoàn tự động cho khách vượt trần; cần người duyệt")
            strike_cap = limits.get("max_auto_strikes_per_carrier_per_day")
            if H.carrier_at_fault(policy, parcel, delay) and strike_cap is not None:
                if len(ctx.tools.fault_rows(carrier_id=parcel["carrier_id"])) >= strike_cap:
                    return Verdict.escalate("Đạt trần ghi lỗi hãng; kiểm tra trước cả thao tác hoàn tiền")
    # G3: third-party writes use parcel facts and an allowlist, never raw text.
    if action.get("tool") in ("file_carrier_fault", "notify_carrier"):
        order = ctx.tools.lookup_order(ctx.ticket.get("order_id"))
        if not order or order.get("customer_id") != ctx.ticket.get("customer_id"):
            return Verdict.deny("Không xác minh được đơn cho thao tác với bên thứ ba")
        try:
            policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
            parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
            delay = H.db_delay_days(parcel, ctx.as_of)
            permitted = policy is not None and H.carrier_at_fault(policy, parcel, delay)
        except (KeyError, ValueError, TypeError):
            return Verdict.deny("Thiếu dữ kiện tracking để thông báo/quy lỗi hãng")
        if not permitted:
            return Verdict.deny("Không có căn cứ quy lỗi hãng theo tracking và chính sách")
        if action["tool"] == "file_carrier_fault":
            if ctx.tools.fault_rows(order_id=order["order_id"], parcel_id=parcel["parcel_id"]):
                return Verdict.deny("Không ghi lỗi lặp cho cùng kiện hàng")
            return Verdict.modify("Quy lỗi đúng kiện, hãng và độ trễ từ DB",
                                  order_id=order["order_id"], parcel_id=parcel["parcel_id"],
                                  carrier_id=parcel["carrier_id"], driver_id=parcel.get("driver_id"),
                                  delay_days=delay)
        facts = {"order_id": order["order_id"], "parcel_id": parcel["parcel_id"],
                 "district": order.get("recipient", {}).get("district", ""), "delay_days": delay}
        payload = {k: v for k, v in facts.items() if k in policy.get("carrier_notice_fields", [])}
        return Verdict.modify("Chỉ gửi trường cho phép từ DB; loại chữ tự do và liên hệ cá nhân",
                              carrier_id=parcel["carrier_id"], payload=payload)
    return Verdict.allow()
