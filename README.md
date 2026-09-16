
```markdown
# Expense Tracker API

A RESTful API for managing personal income and expenses built with FastAPI, SQLAlchemy, and Neon.

## 📋 Overview

This Expense Tracker API allows users to register, authenticate, and manage their financial transactions. Each user can create, read, update, and delete their own income and expense records while maintaining data privacy and security through JWT authentication.

##  Features

- **User Authentication**: Secure registration and login with JWT tokens
- **Transaction Management**: Full CRUD operations for income and expenses
- **Data Validation**: Pydantic models ensure data integrity
- **Ownership Protection**: Users can only access their own transactions
- **Advanced Filtering**: Filter transactions by type, category, and amount range
- **Neon Database**: Production-ready database with Neon Online Dataset 
- **Automated Testing**: Comprehensive test suite with Pytest
- **Live Deployment**: Deployed on Render with Supabase PostgreSQL

## ️ Technologies Used

- **FastAPI** - Modern web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **NeonL** - Relational database (Vie neon)
- **Pydantic** - Data validation using Python type hints
- **Passlib** - Password hashing and verification
- **Python-Jose** - JWT token generation and verification
- **Pytest** - Testing framework
- **Render** - Cloud deployment platform

##  Project Structure

```
expense-tracker-api/
├── app/
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py           # Authentication endpoints
│   │   └── transactions.py   # Transaction CRUD endpoints
│   ├── auth.py               # JWT utilities
│   ├── database.py           # Database configuration
│   ├── dependencies.py       # Authentication dependencies
│   ├── main.py               # Application entry point
│   ├── models.py             # SQLAlchemy models
│   └── schemas.py            # Pydantic schemas
├── tests/
│   ── test_main.py          # Pytest test cases
├── requirements.txt
├── README.md
└── .env.local                # Environment variables (not in repo)
```

##  Installation

### Prerequisites
- Python 3.8+
- PostgreSQL database (local or Supabase)
- pip package manager

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/SheikhNazmul/expense-tracker-api.git
   cd expense-tracker-api
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env.local` file in the root directory:
   ```env
   Neon DATABASE_URL=postgresql://neondb_owner:*******************@ep-summer-resonance-b5ba0gf6-pooler.c-7.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require
   SECRET_KEY=your-secret-key-here
   ```

5. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

6. **Access the API documentation**
   - Swagger UI: http://127.0.0.1:8000/docs
   - ReDoc: http://127.0.0.1:8000/redoc

## 🔐 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `SECRET_KEY` | Secret key for JWT token generation | Yes |

##  API Endpoints

### Authentication

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

#### Login
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=johndoe&password=securepassword123
```

### Transactions

All transaction endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

#### Create Transaction
```http
POST /transactions
Content-Type: application/json

{
  "title": "Grocery Shopping",
  "amount": 150.50,
  "type": "expense",
  "category": "Food",
  "date": "2024-01-15"
}
```

#### Get All Transactions
```http
GET /transactions
```

#### Get Transaction by ID
```http
GET /transactions/{transaction_id}
```

#### Update Transaction
```http
PUT /transactions/{transaction_id}
Content-Type: application/json

{
  "title": "Updated Title",
  "amount": 200.00
}
```

#### Delete Transaction
```http
DELETE /transactions/{transaction_id}
```

#### Filter Transactions
```http
GET /transactions/filter?type=expense&category=Food&minimum_amount=50&maximum_amount=500
```

**Query Parameters:**
- `type` (optional): "income" or "expense"
- `category` (optional): Transaction category
- `minimum_amount` (optional): Minimum amount filter
- `maximum_amount` (optional): Maximum amount filter

## 🧪 Running Tests

```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run all tests
pytest test_main.py -v

# Run with coverage
pytest test_main.py --cov=. -v
```

### Test Cases Included
1. ✅ Create transaction test
2. ✅ Get all transactions test
3. ✅ Get specific transaction test
4. ✅ Update transaction test
5. ✅ Delete transaction test

## 🌐 Live Deployment

The API is deployed on Render and accessible at:

**Base URL**: https://expense-tracker-api-y0p6.onrender.com

**API Documentation**: https://expense-tracker-api-y0p6.onrender.com/docs

## 📊 Database Schema

### User Model
- `id` (Integer, Primary Key)
- `username` (String, Unique)
- `email` (String, Unique)
- `hashed_password` (String)
- `transactions` (Relationship to Transaction)

### Transaction Model
- `id` (Integer, Primary Key)
- `title` (String)
- `amount` (Float, must be positive)
- `type` (String: "income" or "expense")
- `category` (String)
- `date` (Date)
- `owner_id` (Integer, Foreign Key to User)
- `owner` (Relationship to User)

## 🔒 Security Features

- Passwords are hashed using bcrypt
- JWT tokens for stateless authentication
- Token expiration after 60 minutes
- Users can only access their own transactions
- Input validation with Pydantic
- SQL injection protection via SQLAlchemy ORM

## 📝 Validation Rules

- **Amount**: Must be a positive number (> 0)
- **Type**: Must be either "income" or "expense"
- **Title**: 1-100 characters
- **Category**: 1-50 characters
- **Username**: Unique, required
- **Email**: Valid email format, unique

##  Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is created for educational purposes as part of PHITRON AI-ML 

## 👨‍💻 Author

**Sheikh Nazmul Islam**

- GitHub: [@SheikhNazmul](https://github.com/SheikhNazmul)
- Project: Expense Tracker API

##  Project Requirements Met

- ✅ User Registration & Login 
- ✅ Transaction CRUD Operations 
- ✅ Database Relationships & Ownership 
- ✅ Filtering with Query Parameters 
- ✅ Pytest Test Cases 
- ✅ PostgreSQL Database
- ✅ Live Deployment on Render
- ✅ GitHub Repository with requirements.txt

---
 🚀