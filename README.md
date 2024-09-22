# eAmbulance - Ambulance Booking System 🚑

**Live Demo:** [https://eambulance.aptechsfc.online/](https://eambulance.aptechsfc.online/)

---

## Overview
**eAmbulance** is a web-based ambulance booking system designed to streamline the process of requesting and dispatching ambulance services during medical emergencies. This system connects patients, drivers, and administrators on a unified platform to ensure quick and efficient medical response.

## Features

### User Features
- **Ambulance Booking:** Users can quickly request an ambulance by filling out essential information about their emergency.
- **Medical Profile Management:** Users can input and update their medical history, allergies, and emergency contact details.
- **Real-Time Ambulance Tracking:** Once an ambulance is dispatched, users can track its real-time location on the map.
- **Order Medicines:** Users can order medicines from the built-in shop, add items to the cart, and pay on delivery.
- **Feedback Submission:** After receiving service, users can submit feedback to help improve the platform.

### Admin Features
- **Ambulance Fleet Management:** Admins can add, edit, or remove ambulances and drivers. 
- **Booking Management:** Admins can view, manage, and assign ambulance requests to drivers.
- **Real-Time Monitoring:** Admins can monitor the real-time location of ambulances.
- **Order Management:** Admins can update the status of medicine orders placed by users.
- **Medical Profile Access:** Admins can view users' medical profiles and emergency contact details to assist in decision-making.

### Driver Features
- **Dispatch Management:** Drivers can accept ambulance dispatch requests and update their status.
- **Access to Medical Profiles:** Drivers/EMTs have access to patients' medical information to prepare for emergencies during transit.

---

## Tech Stack

- **Backend:** Python, Django, Django Channels (WebSockets for real-time tracking)
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Database:** MongoDB Atlas
- **Maps & Tracking:** OpenStreetMap for real-time ambulance tracking
- **Authentication:** User and admin authentication for secure access

---

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/eambulance.git
