# Lecture 1. What the Web Is and Why We Need Django

## 1. How the web works

When you open a website, two sides talk to each other:

- **Client** — the one who asks. Usually a browser (Chrome, Safari) or a mobile app.
- **Server** — the one who answers. A computer that runs the website's program.

```
 Browser (client)                         Server
      │                                     │
      │ ──── Request: "give me page /" ───> │
      │                                     │  thinks, gets data from the DB
      │ <─── Response: HTML page ────────── │
      │                                     │
```

The whole web is one endless loop: **request → response**.

> **Café analogy:** you (the client) order from a waiter, the kitchen (the server) cooks, and the waiter brings your dish (the response). The menu is the list of addresses (URLs) the website can serve.

## 2. HTTP — the language they speak

The client and server follow the rules of the **HTTP** protocol.

A **request** has:

| Part | Example | Meaning |
|---|---|---|
| Method | `GET` | What we want to do |
| URL | `/clients/5/` | What we want it done to |
| Headers | `Accept: text/html` | Extra information |
| Body | `{"name": "Aliya"}` | Data (not always) |

**Main methods:**

| Method | Action | Example |
|---|---|---|
| `GET` | Read | Open the client list |
| `POST` | Create | Add a new client |
| `PUT` / `PATCH` | Update | Change a client's phone number |
| `DELETE` | Delete | Remove a client |

A **response** always has a **status code** — a short number that tells the result:

| Code | Meaning |
|---|---|
| `200` | All good |
| `201` | Created |
| `301` / `302` | Go to another address |
| `400` | You sent something wrong |
| `403` | Access denied |
| `404` | Not found |
| `500` | The server broke |

Easy to remember: **2xx — success, 3xx — redirect, 4xx — client error, 5xx — server error.**

## 3. What a URL is made of

```
https://mycrm.kz:443/clients/5/?tab=orders
└─┬─┘   └───┬──┘ └┬┘ └───┬───┘ └───┬────┘
protocol  domain  port   path    parameters
```

The server looks at the **path** (`/clients/5/`) and decides which code to run.

## 4. Frontend and Backend

- **Frontend** — what the user sees: HTML (structure), CSS (looks), JavaScript (behavior). Runs in the browser.
- **Backend** — what is hidden on the server: logic, checks, working with the database. **Django is backend.**
- **Database** — where the data lives (clients, orders, users).

## 5. Why we need a framework

You can write a server from scratch, but then you have to handle a lot yourself:

- parse HTTP requests;
- connect URLs to code;
- work with the database;
- build login and sign-up;
- protect against attacks;
- build an admin panel.

A **framework** is a ready-made skeleton where all of this is already done. We only write what is unique to our project.

## 6. What Django is

**Django** is a web framework for Python. Its motto is *"Batteries included"* — almost everything you need is already inside: database access (ORM), an admin panel, authentication, templates, and protection against attacks.

Instagram, Pinterest, Mozilla, and Disqus are built with Django.

### MVC — the classic approach

Most web frameworks split code into three parts using the **MVC** pattern:

| Part | Role | In the café |
|---|---|---|
| **Model** | Data and database work | The pantry |
| **View** | How data looks to the user | How the dish is served |
| **Controller** | Takes the request, decides what to do | The waiter |

The idea is simple: **each part does only its own job**. A designer can change the looks without breaking the logic, and a developer can change the logic without touching the database.

### MTV — Django's approach

Django uses the same idea but names the parts its own way — **MTV** (Model, Template, View):

| MVC | Django (MTV) | File |
|---|---|---|
| Model | **Model** | `models.py` |
| View | **Template** | `*.html` |
| Controller | **View** + `urls.py` | `views.py` |

```
 Request ──> urls.py ──> View ──> Model ──> Database
                          │
                          └──> Template ──> Response (HTML)
```

> ⚠️ **The main confusion:** a `View` in Django is **not** "how it looks" — it's the **logic** (what MVC calls the Controller). How it looks is the `Template`.

### Django pros

- **Fast development** — you can build a working prototype in a day.
- **Everything included** — no need to find and glue together dozens of libraries.
- **Secure by default** — protection against CSRF, SQL injection, and XSS is already on.
- **Built-in admin** — you can manage data right away, without a frontend.
- **Common structure** — any Django developer quickly understands someone else's project.
- **Big community** — great documentation and ready-made solutions for almost everything.

### Django cons

- **Heavyweight** — for a small API or microservice, Django is overkill. People often pick FastAPI or Flask there.
- **Tight coupling** — Django's parts are closely tied together. Replacing the built-in ORM or templates with something else is hard.
- **Confusing names** — a Django `View` is not an MVC `View`, and beginners often mix them up.
- **No place for business logic** — MTV doesn't say where to put it. As a result, `views.py` or `models.py` grow to thousands of lines ("fat" views and models).
- **The ORM hides SQL** — convenient, but it's easy to write slow code without noticing (for example, hundreds of database queries instead of one).
- **Synchronous at heart** — async support arrived recently and isn't everywhere yet.
- **Templates are dated for SPAs** — modern frontends (React, Vue) usually talk to the server through an API, and for that you need an extra tool — Django REST Framework.

> **Takeaway:** Django is a great fit for large projects with a database, an admin panel, and users — like a CRM. For tiny services, there are lighter tools.

---

📂 **Code for Lectures 1–3:** [crm-django / week-1-2-3](https://github.com/MaratulyTemirbolat/crm-django/tree/week-1-2-3)
