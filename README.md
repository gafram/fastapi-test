## Install
```bash
pip install fastapi uvicorn
uvicorn src.main:app --reload
```

## Examples

Negative:
```bash
❯ curl -X POST "http://localhost:8000/reviews" \
     -H "Content-Type: application/json" \
     -d '{"text": "Ненавижу, всё падает!"}'
{"text":"Ненавижу, всё падает!","id":1,"sentiment":"negative","created_at":"2025-08-04T10:40:22.477895"}
```
```bash
❯ curl -X POST "http://localhost:8000/reviews" \
     -H "Content-Type: application/json" \
     -d '{"text": "Работает плохо:("}'
{"text":"Работает плохо:(","id":2,"sentiment":"negative","created_at":"2025-08-04T10:41:28.139254"}
```

Neutral:
```bash
curl -X POST "http://localhost:8000/reviews" \
     -H "Content-Type: application/json" \
     -d '{"text": "Работает и ладно"}'
{"text":"Работает и ладно","id":3,"sentiment":"neutral","created_at":"2025-08-04T10:42:44.784239"}
```

Positive:
```bash
❯ curl -X POST "http://localhost:8000/reviews" \
     -H "Content-Type: application/json" \
     -d '{"text": "Хорошо, все хорошо"}'
{"text":"Хорошо, все хорошо","id":5,"sentiment":"positive","created_at":"2025-08-04T10:44:33.166518"}
```

Get negative reviews:
```bash
❯ curl -X GET "http://localhost:8000/reviews?sentiment=negative"
[{"text":"Ненавижу, всё падает!","id":1,"sentiment":"negative","created_at":"2025-08-04T10:40:22.477895"},{"text":"Работает плохо:(","id":2,"sentiment":"negative","created_at":"2025-08-04T10:41:28.139254"}]
```