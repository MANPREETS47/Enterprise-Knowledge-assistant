import httpx

r = httpx.post(
    "https://enterprise-knowledge-assistant-5.onrender.com/ask",
    json={"message": "hello"},
    timeout=300
)

print(r.text)
