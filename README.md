## SmartWaste – AI-Powered Food Waste Tracker 

**SmartWaste** is a mobile-friendly food waste tracking application that leverages AI-powered insights to help users manage groceries, minimize waste, and optimize purchasing habits.

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

*   **Grocery Inventory Management:** Comprehensive CRUD operations for tracking food items.
*   **Barcode Scanning:** Quickly add items using barcode recognition.
*   **Smart Reminders & Notifications:** Receive push notifications for expiring items.
*   **AI-Powered Waste Analysis:** Identify frequently wasted items through intelligent insights.
*   **Personalized Suggestions:** Get recommendations for optimized purchases to reduce waste.
*   **Secure Authentication:** Token-based authentication powered by Django Allauth.
*   **Cloud Availability:** Reliably deployed backend for seamless access.

---

## Tech Stack

*   **Backend:** Django, Django REST Framework, PostgreSQL
*   **AI Integration:** Google Gemini API
*   **Push Notifications:** FCM with `fcm-django`
*   **Deployment:** Render
*   **Mobile Frontend:** Flutter

---

## Installation

To get started with SmartWaste, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/KDaqrouq/smartwaste_backend.git
    cd smartwaste_backend
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up the database:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Add your Gemini API key:**
    Open `settings.py` and add your Google Gemini API key:
    ```python
    GEMINI_API_KEY = "YOUR_API_KEY_HERE"
    ```

---

## API Endpoints

### Inventory CRUD

*   **`GET /api/`**: List user’s inventory items.
*   **`POST /api/`**: Add a new item to the inventory.
*   **`PUT /api/<id>/`**: Update an existing item by ID.
*   **`DELETE /api/<id>/`**: Delete an item by ID.

### Notifications

*   **`GET /expiring/notify/`**: Trigger notifications for expiring items.

### Device Registration (FCM)

*   **`POST /fcm/token/`**: Register mobile devices for push notifications.

### AI Recommendations

*   **`POST /ai/recommendations/`**: Get personalized purchase and waste reduction suggestions.

---

## AI Insights

SmartWaste's AI integration with the Google Gemini API provides intelligent insights by:

*   Collecting a user’s inventory and waste history.
*   Sending structured data to the Google Gemini API for analysis.
*   Returning actionable recommendations.

**Example Response:**

```json
{
  "frequent_waste": ["Milk", "Bread"],
  "suggestions": ["Buy smaller milk cartons", "Consider frozen bread"],
  "purchase_habits": ["Buy fruits in smaller batches", "Track expiry dates carefully"]
}
```

---

## Deployment

The backend of SmartWaste is deployed on [Render](https://render.com/) for cloud hosting. Key deployment features include:

*   **Continuous Deployment:** Automatic updates are reflected from GitHub.
*   **Scalable Architecture:** Supports multiple users with reliable push notifications.

---

## Contributors

*   **Khaled Daqrouq** – Backend Development, AI Integration, API Development, Deployment.
*   **[Partner Name]** – Frontend Development, Mobile App Development, UI/UX Design.
