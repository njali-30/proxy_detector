# Attendance Check-in System

A simple Flask-based web application for student attendance check-in with proxy detection using statistical methods.

## Features

- Fetches student roll numbers and names from a MySQL database.
- Students enter their check-in time in decimal format (e.g., 9.00 for 9:00 AM).
- Detects proxy attendance using Z-score and Interquartile Range (IQR) outlier detection.
- Marks students as Present, Absent, or Proxy based on their check-in times.
- Displays attendance results dynamically after form submission.

## Technologies Used

- Python 3.x
- Flask web framework
- MySQL database
- Pandas and NumPy for data processing

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/attendance-flask-app.git
cd attendance-flask-app
