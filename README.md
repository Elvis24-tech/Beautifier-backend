# Beautifier Full Stack E-Commerce Platform

Beautifier is a modern full-stack beauty e-commerce web application that allows users to browse, wishlist, and purchase beauty products, with admin product management and M-Pesa payment integration.

It is built using:

- React (Frontend)
- Tailwind CSS
- Django + Django REST Framework (Backend)
- PostgreSQL
- Firebase + JWT Authentication
- M-Pesa Daraja API

---

# Frontend Github link - https://github.com/Elvis24-tech/Beautifier
# Frontend Live link - https://beautifier-pi.vercel.app/

# Features

## Customer Features

- Browse beauty products
- Add/remove from cart
- Wishlist products
- Update quantity in cart
- Checkout flow
- Mobile responsive UI
- Smooth animations

---

## Admin Features

- Secure admin login
- Add / edit / delete products
- Admin-only dashboard
- Protected routes (JWT + Firebase)

---

## Payments

- M-Pesa STK Push integration
- Payment callback handling
- Order confirmation system

---

# Tech Stack

## Frontend

- React.js
- Tailwind CSS
- React Router DOM
- Context API
- Firebase Auth

---

## Backend

- Django
- Django REST Framework
- SimpleJWT Authentication
- PostgreSQL / SQLite
- CORS headers

---

# Project Structure

```bash
Beautifier/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── context/
│   │   └── App.jsx
│   │
│   └── package.json
│
├── backend/
│   ├── api/
│   ├── users/
│   ├── products/
│   ├── orders/
│   ├── payments/
│   ├── manage.py
│   └── requirements.txt
```

---

# Installation Guide

## 1. Clone Project

```bash id="c1q9xv"
git clone https://github.com/yourusername/beautifier.git
cd beautifier
```

---

# FRONTEND SETUP

## Install dependencies

```bash id="f8q2wp"
cd frontend
npm install
```

## Run frontend

```bash id="m1xk9p"
npm run dev
```

Frontend runs on:

```
http://localhost:5173
```

---

# BACKEND SETUP

## Create virtual environment

```bash id="v9xk2a"
cd backend
python -m venv venv
```

## Activate environment

### Windows
```bash id="w1k9qp"
venv\Scripts\activate
```

### Mac/Linux
```bash id="l3xk9z"
source venv/bin/activate
```

---

## Install dependencies

```bash id="p8xk2w"
pip install -r requirements.txt
```

---

## Run migrations

```bash id="z9xk2m"
python manage.py migrate
```

---

## Create superuser

```bash id="s2xk9p"
python manage.py createsuperuser
```

---

## Start server

```bash id="d8xk2q"
python manage.py runserver
```

Backend runs on:

```
http://127.0.0.1:8000
```

---

# Environment Variables

Create `.env` file inside backend:

```env id="e9xk2v"
SECRET_KEY=your_secret_key
DEBUG=True

DB_NAME=beautifier
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

MPESA_CONSUMER_KEY=your_key
MPESA_CONSUMER_SECRET=your_secret
MPESA_SHORTCODE=your_shortcode
MPESA_PASSKEY=your_passkey
MPESA_CALLBACK_URL=https://yourdomain.com/api/mpesa/callback/
```

---

# API ENDPOINTS

## Auth
```
POST /api/token/
POST /api/token/refresh/
```

## Products
```
GET    /api/products/
POST   /api/products/
PUT    /api/products/:id/
DELETE /api/products/:id/
```

## Cart
```
GET    /api/cart/
POST   /api/cart/
DELETE /api/cart/:id/
```
## Orders
```
GET  /api/orders/
POST /api/orders/
```

## Payments
```
POST /api/mpesa/stkpush/
POST /api/mpesa/callback/
```

---

# Responsive Design

Beautifier is fully responsive:

- Mobile phones
- Tablets
- Laptops
- Desktop screens

---

# Security

- JWT authentication
- Firebase login (admin protection)
- Protected API routes
- Environment variables
- CORS protection

---

# Deployment

## Frontend
- Vercel
- Netlify

## Backend
- Render
- Railway
- DigitalOcean

---

# Developer

Built by **Elvis Muasya Kariuki** @Elvis24-tech

Full Stack Developer:
- React
- Tailwind CSS
- Django
- Flask
- Firebase

---

# Beautifier

A modern luxury beauty shopping experience built for performance, elegance, and scalability.