# HNG Stage 1 Backend Task – Profile Classification API

A RESTful API built with **Django** and **Django REST Framework** for the HNG Stage 1 Backend Task.

This API accepts a user’s name, integrates with three external public APIs, classifies the result, stores it in a database, and exposes endpoints for profile management.

---

## Live API URL

**Base URL:**
`https://your-live-url.up.railway.app`

Example:
`https://your-live-url.up.railway.app/api/profiles`

---

## GitHub Repository

`https://github.com/yourusername/hng-stage1-profile-api`

---

## Tech Stack

* **Backend Framework:** Django
* **API Framework:** Django REST Framework
* **Database:** PostgreSQL / SQLite (development)
* **Deployment:** Railway / Vercel
* **Language:** Python

---

##  External APIs Used

This project integrates with:

* **Genderize API**
  `https://api.genderize.io?name={name}`

* **Agify API**
  `https://api.agify.io?name={name}`

* **Nationalize API**
  `https://api.nationalize.io?name={name}`

---

## Features

* Create a profile from a name
* Fetch profile by ID
* Retrieve all profiles
* Filter profiles by:

  * gender
  * country_id
  * age_group
* Prevent duplicate profile creation
* Delete profile
* Handles external API validation errors
* Stores data persistently in a database

---

##  API Endpoints

---

### 1. Create Profile

**Endpoint:**
`POST /api/profiles`

**Request Body**

```json
{
  "name": "ella"
}
```

**Success Response (201 Created)**

```json
{
  "status": "success",
  "data": {
    "id": "uuid",
    "name": "ella",
    "gender": "female",
    "gender_probability": 0.99,
    "sample_size": 1234,
    "age": 46,
    "age_group": "adult",
    "country_id": "DRC",
    "country_probability": 0.85,
    "created_at": "2026-04-18T10:00:00Z"
  }
}
```

**Duplicate Response**

```json
{
  "status": "success",
  "message": "Profile already exists",
  "data": { }
}
```

---

### 2. Get All Profiles

**Endpoint:**
`GET /api/profiles`

**Optional Query Parameters**

* `gender`
* `country_id`
* `age_group`

Example:

```text
/api/profiles?gender=male&country_id=NG
```

**Success Response**

```json
{
  "status": "success",
  "count": 2,
  "data": []
}
```

---

### 3. Get Single Profile

**Endpoint:**
`GET /api/profiles/{id}`

Example:

```text
/api/profiles/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

**Success Response**

```json
{
  "status": "success",
  "data": {}
}
```

---

### 4. Delete Profile

**Endpoint:**
`DELETE /api/profiles/{id}`

````

**Success Response:**  
`204 No Content`

---

##  Error Responses

All errors follow this structure:

```json
{
  "status": "error",
  "message": "error message"
}
````

### Possible Errors

* `400` → Missing or empty name
* `422` → Invalid type
* `404` → Profile not found
* `502` → External API returned invalid response

Example:

```json
{
  "status": "error",
  "message": "Genderize returned an invalid response"
}
```

---

##  Classification Logic

### Age Group Rules

* `0–12` → child
* `13–19` → teenager
* `20–59` → adult
* `60+` → senior

### Nationality Rule

The country with the **highest probability** from the Nationalize API response is selected.

---

## Local Setup

Clone the repository:

```bash
git clone https://github.com/yourusername/hng-stage1-profile-api.git
cd hng-stage1-profile-api
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Start server:

```bash
python manage.py runserver
```

---

## 📝 Author

Built by **Your Name** for HNG Stage 1 Backend Task.
