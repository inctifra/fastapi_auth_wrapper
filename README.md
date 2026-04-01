# fastapi-auth-wrapper

A lightweight, plug-and-play authentication wrapper for FastAPI applications that delegate authorization to an external service.

This package allows your FastAPI app to accept incoming requests with an `Authorization` header, forward the token to a remote authentication service (e.g., a Java backend), and inject a validated user object directly into your route handlers.

---

## ✨ Features

* 🔌 Simple dependency injection (`AuthorizedUserClient`)
* 🔐 External token validation (supports microservices architecture)
* ⚡ Minimal configuration via environment variables
* 🧩 Clean separation of concerns (FastAPI app vs auth service)
* 👤 Direct access to authenticated user (`client.user`)

---

## 📦 Installation

```bash
pip install fastapi-auth-wrapper
```

---

## ⚙️ Configuration

Set the following environment variables in your application:

```env
AUTH_SERVICE_URL=http://127.0.0.1:8002
AUTH_SERVICE_TOKEN_URL=/auth/user
```

### Explanation

| Variable                 | Description                                          |
| ------------------------ | ---------------------------------------------------- |
| `AUTH_SERVICE_URL`       | Base URL of your authentication service              |
| `AUTH_SERVICE_TOKEN_URL` | Endpoint path used to validate tokens (must be POST) |

> The final request URL will be: `AUTH_SERVICE_URL + AUTH_SERVICE_TOKEN_URL`

---

## 🚀 Quick Start

### 1. Import the client

```python
from fastapi import FastAPI
from fastapi_auth_wrapper import AuthorizedUserClient
```

### 2. Use in your route

```python
app = FastAPI()

@app.get("/check")
async def get_status(client: AuthorizedUserClient):
    print(client.user)
    return {"status": "ok"}
```

That’s it. The user will be automatically validated and injected.

---

## 🔄 How It Works

1. Incoming request contains:

   ```http
   Authorization: Bearer <token>
   ```

2. The wrapper:

   * Extracts the token
   * Sends a **POST** request to:

     ```
     AUTH_SERVICE_URL + AUTH_SERVICE_TOKEN_URL
     ```
   * Passes the token for validation

3. Auth service responds with user data

4. The wrapper:

   * Parses the response
   * Attaches it to `client.user`
   * Injects `AuthorizedUserClient` into your route

---

## 👤 Accessing the Authenticated User

Inside any route where `AuthorizedUserClient` is injected:

```python
@app.get("/profile")
async def profile(client: AuthorizedUserClient):
    user = client.user
    return {
        "user_id": user.get("id"),
        "email": user.get("email")
    }
```

> `client.user` contains the exact user object returned by your auth service.

---

## 🧪 Example Request

```http
GET http://127.0.0.1:8001/check
Content-Type: application/json
Accept: application/json
Authorization: Bearer <your-token>
```

---

## 🧾 Expected Auth Service Behavior

Your external auth service **must**:

* Accept a **POST** request
* Receive the token (typically via header or body)
* Validate the token
* Return a JSON response containing user information

### Example Response

```json
{
  "id": "1",
  "email": "user@example.com",
  "roles": ["user"]
}
```

---

## ⚠️ Error Handling

The wrapper will raise appropriate HTTP errors in cases such as:

* Missing `Authorization` header
* Invalid token format
* Auth service unavailable
* Token validation failure

You can customize error handling globally in your FastAPI app if needed.

---

## 🧩 Use Cases

* Microservices with centralized authentication
* FastAPI frontend backed by Java/Spring auth service
* API gateways needing token verification
* Multi-client architectures sharing auth

---

## 🛠 Advanced Usage

### Custom logic using user data

```python
@app.get("/admin")
async def admin_only(client: AuthorizedUserClient):
    if "admin" not in client.user.get("roles", []):
        raise HTTPException(status_code=403, detail="Forbidden")
    return {"message": "Welcome admin"}
```

---

## 🧠 Design Philosophy

* Keep FastAPI apps lightweight
* Delegate authentication responsibility
* Promote reusable infrastructure components

---

## 📄 License

[MIT License](LICENSE)

---

## 🙌 Contributing

Contributions, issues, and feature requests are welcome!

---

## 📬 Support

If you encounter any issues, feel free to open a GitHub issue or reach out.
