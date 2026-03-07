
1-Task (Build a Log Analyzer)
script path -> apps/common/scripts/log_analyzer.py

2-Task (REST API for Currency Conversion)
api/v1/currency/convert?amount=100&from_currency=USD&to_currency=UZS
"data": {
    "convert_amount": 1219766.52,
    "from_currency": "USD",
    "to_currency": "UZS"
  }

3-Task (JSON Data Validator and Transformer)
script path -> apps/common/utils/validate_and_export_to_csv.py
result:
<img width="1179" height="438" alt="image" src="https://github.com/user-attachments/assets/77ae88ae-199a-41c2-b7b3-1e118bf23bad" />

4-Task(Asynchronous Web Scraper)
script path -> apps/common/scripts/async_web_scaper.py

5-Task(Transactional Order Processor)
<img width="1173" height="136" alt="image" src="https://github.com/user-attachments/assets/7c0710bc-7607-4da3-a9be-a7f054ecc02f" />

6-Task(Celery Task Queue Challenge)
<img width="1181" height="257" alt="image" src="https://github.com/user-attachments/assets/1c364dcf-a988-489f-84a5-72fd1477f18a" />

7-Task(Performance Optimization – N+1 Killer)

select_related va prefetch_related dan foydalanmagan casedagi db ga yuborilayotgan querylar
queryset = Post.objects.all()
<img width="1126" height="687" alt="image" src="https://github.com/user-attachments/assets/9d157e72-a47c-4a1a-b039-14f297f0e394" />

select_related va prefetchdan foydalangan holatdagisi
queryset = Post.objects.select_related("category").prefetch_related("comments")
<img width="1146" height="672" alt="image" src="https://github.com/user-attachments/assets/34511b3b-17b7-4f13-bf8e-f89cce6e45bd" />

8-Task(File Upload Service with Chunking)

9-Task(HMAC-Signed Webhook Receiver)

payload='{"event_id":"evt_001","type":"payment_success","order_id":123}'
signature=$(echo -n $payload | openssl dgst -sha256 -hmac "SuperSecretKey" | sed 's/^.* //')

curl -X POST http://localhost:8000/api/v1/webhooks/payment/ \
     -H "X-Signature: $signature" \
     -H "Content-Type: application/json" \
     -d "$payload"

10-Task(Complex SQL Reporting Task)
script path -> apps/orders/scripts.py 
  customer_monthly_stats - Customer oylik statistikasi
  monthly_stats - Oylik buyurtmalar bo'yicha statistika
