# Ruby on Rails API Mode, ActiveJob, and Sidekiq Concurrency

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Rails API mode ek restaurant ke **Express Drive-Thru Window** jaisa hai: Dining room aur plates (HTML Views, Sprockets) ko hata diya gaya hai, sirf fast JSON deliver hota hai.
**Sidekiq** ek **Dedicated Delivery Boy** ki tarah hai: Customer ne pizza order kiya, counter executive ne receipt print karke kitchen hook (Redis Queue) par latka di aur customer ko 2 second mein receipt pakda di. Delivery boy (Sidekiq worker) background mein pizza pack karke delivery karta rehta hai.

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Rails API Only Mode (`--api`)**: Strips out session management, cookies, asset pipelines, and view rendering for ultra-lean JSON APIs.
2. **Sidekiq Architecture**: Multi-threaded background job processor powered by Redis for reliable job persistence.
3. **Idempotency**: Background jobs must be idempotent because Sidekiq guarantees **at-least-once** job execution.

---

## 💻 3. Line-by-Line Commented Code Snippets

```ruby
# app/jobs/process_monthly_invoice_job.rb
class ProcessMonthlyInvoiceJob < ApplicationJob
  # Line 3: Route this job to the high-priority Sidekiq queue in Redis
  queue_as :critical

  # Line 6: Automatically retry up to 5 times with exponential backoff
  sidekiq_options retry: 5

  def perform(account_id, billing_cycle)
    # Line 10: Find account safely
    account = Account.find(account_id)
    
    # Line 13: Idempotency check to prevent double charging
    return if account.invoices.where(billing_cycle: billing_cycle).exists?

    # Line 16: Generate invoice and charge card
    invoice = account.generate_invoice!(billing_cycle)
    PaymentService.charge!(invoice)
  end
end
```
