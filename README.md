# SmartWaste – AI-Powered Food Waste Tracker

**SmartWaste** is a mobile-friendly food waste tracking application that helps users manage their groceries, reduce waste, and optimize purchases using AI-powered insights.

[GitHub Repository](https://github.com/KDaqrouq/smartwaste_backend)

---

## Table of Contents

- [Features](#features)  
- [Tech Stack](#tech-stack)  
- [Installation](#installation)  
- [Usage](#usage)  
- [API Endpoints](#api-endpoints)  
- [AI Insights](#ai-insights)  
- [Deployment](#deployment)  
- [Contributors](#contributors)  

---

## Features

- Track grocery inventory with CRUD operations  
- Barcode scanning for quick item addition  
- Smart reminders and push notifications for expiring items  
- AI-powered insights to identify frequently wasted items  
- Personalized purchase suggestions to reduce waste  
- Token-based authentication using Django Allauth  
- Deployed backend for reliable cloud availability  

---

## Tech Stack

- **Backend:** Django, Django REST Framework, PostgreSQL  
- **AI Integration:** Google Gemini API  
- **Push Notifications:** FCM with `fcm-django`  
- **Deployment:** Render  
- **Mobile Frontend:** Flutter  

---

## Installation

1. Clone the repository:

- git clone https://github.com/KDaqrouq/smartwaste_backend.git
- cd smartwaste_backend
  
2. Create a virtual environment:

- python -m venv venv
- source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:

- pip install -r requirements.txt

4. Set up the database:

- python manage.py makemigrations
- python manage.py migrate

5. Create a superuser:

- python manage.py createsuperuser

6. Add your Gemini API key in settings.py:

- GEMINI_API_KEY = "YOUR_API_KEY_HERE"

---

## API Endpoints
Inventory CRUD:

GET /api/ – List user’s items

POST /api/ – Add a new item

PUT /api/<id>/ – Update an item

DELETE /api/<id>/ – Delete an item

Notifications:

GET /expiring/notify/ – Notify users of expiring items

Device Registration (FCM):

POST /fcm/token/ – Register mobile device for push notifications

AI Recommendations:

POST /ai/recommendations/ – Get personalized purchase and waste reduction suggestions

---

## AI Insights

Collects a user’s inventory and waste history

Sends structured data to Google Gemini API

Returns:

Most frequently wasted items

Recommendations for smaller portions or alternatives

Optimized purchase habits

Example Response:

{
  "frequent_waste": ["Milk", "Bread"],
  "suggestions": ["Buy smaller milk cartons", "Consider frozen bread"],
  "purchase_habits": ["Buy fruits in smaller batches", "Track expiry dates"]
}

---

## Deployment
Deployed backend on Render for cloud hosting

Continuous deployment ensures updates from GitHub are reflected automatically

Scalable architecture supports multiple users with reliable push notifications

---

## Contributors
Khaled Daqrouq – Backend, AI Integration, API Development, Deployment

Partner Name – Frontend, Mobile App Development, UI/UX Design
