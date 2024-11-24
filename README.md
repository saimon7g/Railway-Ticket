# Railway E-Ticket Reservation System

A comprehensive online railway ticket booking system built with Django and Oracle Database, featuring real-time seat availability, multiple payment methods, and secure user authentication.

## Features

### User Authentication
- Secure signup/login system with password hashing
- Session management
- Profile management

### Ticket Booking System
- Real-time train search
- Station to station journey planning
- Date-wise booking
- Interactive seat selection
- Support for multiple passenger types (Adult/Child)
- Different seat classes (Snigdha, S-Chair, Shovan)

### Payment Integration
- Multiple payment methods:
  - bKash
  - Rocket
  - Card Payment
  - Nexus Pay
- Payment verification system
- Real-time transaction handling

### Ticket Management
- Digital ticket verification
- Journey details viewing
- Booking history
- Ticket status checking

## Technology Stack

### Backend
- Django 4.1
- Oracle Database
- Python cx_Oracle

### Frontend
- HTML/CSS
- JavaScript
- Django Templates

### Authentication
- Custom user authentication
- SHA-256 password hashing
- Session-based auth management

## Database Schema
- Accounts
- Train
- Station
- Reservation
- Booked_Seats
- Reserved_Seat
- Train_Timetable
- Cost

## Installation

1. Clone the repository
```bash
git clone <repository-url>
pip install -r requirements.txt
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'your_db_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '1521',
    }
}
python manage.py migrate
python manage.py runserver

## Database Design

### Database Configuration
- System: Oracle Database
- Port: 1521
- Character Set: UTF-8

### Schema Design

#### 1. ACCOUNTS Table
- USER_ID (Primary Key)
- FIRST_NAME
- LAST_NAME
- PASSWORD (SHA-256 hashed)
- EMAIL (Unique)
- PHONE
- NID_NUMBER (Unique)
- GENDER
- ADDRESS
- DOB (Date of Birth)

#### 2. TRAIN Table
- TRAIN_ID (Primary Key)
- TRAIN_NAME
- (Other train specifications)

#### 3. STATION Table
- STATION_ID (Primary Key)
- STATION_NAME
- (Location details)

#### 4. TRAIN_TIMETABLE Table
- TRAIN_ID (Foreign Key)
- STATION_ID (Foreign Key)
- DEPARTURE_TIME
- DIRECTION
- (Schedule details)

#### 5. COST Table
- FROM_STATION_ID (Foreign Key)
- TO_STATION_ID (Foreign Key)
- SEAT_CLASS
- FARE
- (Pricing details)

#### 6. RESERVATION Table
- RESERVATION_ID (Primary Key)
- DATE_OF_RESERVATION
- DATE_OF_JOURNEY
- NUMBER_OF_TICKETS
- SEAT_CLASS
- FROM_STATION
- TO_STATION
- USER_ID (Foreign Key)
- PAYMENT_STATUS
- TRAIN_ID (Foreign Key)

#### 7. RESERVED_SEAT Table
- SEAT_ID
- SEAT_CLASS
- TRAIN_ID (Foreign Key)
- TRAIN_COMPARTMENT
- DATE_OF_JOURNEY
- RESERVATION_ID (Foreign Key)
- SL_NO

#### 8. BOOKED_SEATS Table
- RESERVATION_ID (Foreign Key)
- SEAT_ID
- SEAT_CLASS
- TRAIN_ID (Foreign Key)
- COMPARTMENT
- DATE_OF_JOURNEY
- SL_NO

#### 9. PAYMENT Tables
- BKASH Table (Phone_num, PIN)
- (Other payment method tables)

### Key Features

1. **Seat Management**
   - 78 seats per class capacity
   - Real-time seat tracking
   - Different seat classes (SNIGDHA, S_CHAIR, SHOVAN)

2. **Pricing System**
   - Station-to-station based pricing
   - Different rates for different classes
   - Child ticket discount (50%)
   - VAT calculation (15%)

3. **Booking System**
   - Prevents double booking through transaction management
   - Automatic seat status updates
   - Reservation timeout system

4. **Data Integrity**
   - Foreign key constraints
   - Unique constraints on critical fields
   - Transaction management for booking process

### Database Triggers
```sql
CREATE TRIGGER deletereserve
    AFTER INSERT ON RESERVED_SEAT
    FOR EACH ROW
BEGIN
    DELETE FROM RESERVATION r 
    WHERE r.RESERVATION_ID IN 
    (SELECT RESERVATION_ID 
     FROM RESERVATION 
     WHERE EXTRACT(MINUTE FROM(sysdate-DATE_OF_RESERVATION)) > 10 
     AND PAYMENT_STATUS='pending');
END;