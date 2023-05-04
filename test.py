SCOPES = ["https://www.googleapis.com/auth/homegraph"]

import jwt
import requests
from datetime import datetime

epoch_time = datetime(1970, 1, 1)
iat = int((datetime.utcnow() - epoch_time).total_seconds())

credentials = {
  "iss": "firebase-adminsdk-xlrev@retropixel-8f415.iam.gserviceaccount.com",
  "scope": "https://www.googleapis.com/auth/homegraph",
  "aud": "https://oauth2.googleapis.com/token",
  "exp": iat + 3600,
  "iat": iat
}

secret = b"-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC1qo5sjFhVSRcj\nASQxX5KOcv73yCKQvjV1LPCWyyyxKXksMvH+MKfgDpHaztFDx4BB+yU1Db+jR6Yn\nT8vhsC1pj+51QoHvtQJ5Th+tPUpLIbd4jfGhuIE/zCG96G0xQcpRvJLET0vqitto\n/5emkAmlSoUodDHPNZE92fUw+DMRYkGBr4eQeESc9EVSDKWtpPaX9LlzbaRMbEGe\noYpYu4N7noZ6XLam0mzw/t2410cRrfJHnpY0kumLF6zF+OZ0gTTTNOTzeEkMekCC\n3r0jWqWlGHlyveWnNBEWVzWctTg27W+yDztTenbTSiMmU3/30LwiY3syXoH65Vi2\nQVOfU2qlAgMBAAECggEAWijW/YVbs5wOOQewfDaICF2HL9cqXHaiFlDi6JvWRuij\n5C02j6Z7MoZYmeUJ0584BscLbLyxjuoYyqreL1id+SV/Pb/vt9U4cJa2vuZLsGT/\n5vtfYBkvQEfhuRwY0RjrPcyedII8VZ9rjD1JeNdEij2lP3IHZGSb/DvnZdHQmn+3\nYhfVA2t3TMLYhgUEL4OAtg5y6JP0cQJhyffR9u11hhMqcICbo3Sh0peG0yU9/2UO\nIIajPapqhX9neSNvoizN1dyYNdiolesCbKi6hc9yVitLfRHb0LQiLSEzXpjTxoyu\nf75Q98PTAOYO4nubJIlDbNPnZz7MWy8qpTIhjtp/8wKBgQDwI1kiS5TCqwrzHRcr\n/WEzzc2G57VC8R5fb32La+NCktKbYz/oSgT7ZBf/1g7LLiS8X+B3aKKH/Z2Jcjfn\nqGEy3GDKkcfm+8LhvvprnmbvkWVvOda4QsF4Tt0pR4C8sHUxuUdaAYWMsEvBp3/F\nb2k52XasUGyewJxHLCCT16EqFwKBgQDBqngzGVYJfD4aQjuLBgvmgrWGQkN83Hv4\n53wF1G4m/qHoeNDQG/waZFRNYau+JsyJacn3tUciiUNNf5AswvvQX4uh8KByAcPa\nu2nzU2vvjVtCmv5Rdqk0eexd6itOZTdT5HXATT1k6ieS+Ho3s0DgK5ydfhNHSOGs\n/+1e70ASowKBgQCPaGy4oG5sev0FBuBpst2ztDoDUKjdG2XKFKji9EE55rjDd1gY\n/utOvg3fCRS4ngvuO0uvw9scX4cPKBjezZ2OZDGhh8Hb3YoaipS+ZFCQzUHIVMA4\nNhWYJXDKUBs/lBnI4h8MT1BUHox/T+psHAa5N3c5nKXhgKFTl7S01dc3bQKBgQCf\nmNQliCOW/YRQL3TSRNFZzS26zrC/HRQtMtbKFx4PlJfo9GdgmS9QsI2ol2zo7yBv\nvXZrZECS/XsxSoaN3MGYHqT7d0lBqqK0hu3xUDYK2/rxELm0eI1IaZGYc3nsyQyn\nXgaLyxtlJnImdA6ECHzWQBp4z4UjobQY1W/QZGnw8QKBgD9YxwB9Qk34YULTHIj6\nMpg/tsKxJl2SPB6sP8vA6IyI6tyb5lOSHQt2dyCTjJUliXJD9DyrxAj0OH49GmYZ\n4NjHMYrvVGEc9l+soAXH/BrhhYma7Hui2emvFWa3otb2V6D+A4KrxYfgLm8mcwTv\nw04nxddRWwPPLsOK9t3C3PVe\n-----END PRIVATE KEY-----\n"

code = jwt.encode(credentials, secret, 'RS256')

response = requests.post(
    'https://oauth2.googleapis.com/token',
    json={
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": code
    }
)

token = response.json()

print(token)