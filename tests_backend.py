import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000"
USERNAME = "Adiiii"
PASSWORD = "itsokay"
EMAIL = "aditya89505@gmail.com"

def test_endpoint(method, endpoint, data=None, token=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        response = requests.post(url, headers=headers, data=json.dumps(data))
    elif method == "PUT":
        response = requests.put(url, headers=headers, data=json.dumps(data))
    elif method == "DELETE":
        response = requests.delete(url, headers=headers)
    
    print(f"{method} {endpoint}: {response.status_code}")
    print(response.json())
    print("---")
    return response.json()

def run_tests():
    # 1. Authentication
    print("Testing Authentication")
    register_data = {"username": USERNAME, "email": EMAIL, "password": PASSWORD}
    test_endpoint("POST", "/auth/register/", register_data)
    
    token_data = {"username": USERNAME, "password": PASSWORD}
    token_response = test_endpoint("POST", "/auth/token/", token_data)
    token = token_response.get('access')
    
    test_endpoint("POST", "/auth/token/refresh/", {"refresh": token_response.get('refresh')})
    test_endpoint("POST", "/auth/password_reset/", {"email": EMAIL})

    # 2. Salon Operations
    print("Testing Salon Operations")
    salon_data = {
        "name": "Test Salon",
        "address": "123 Test St",
        "city": "Test City",
        "phone": "+1234567890",
        "email": "testsalon@example.com"
    }
    salon_response = test_endpoint("POST", "/api/salons/", salon_data, token)
    salon_id = salon_response.get('id')
    test_endpoint("GET", f"/api/salons/{salon_id}/", token=token)
    test_endpoint("GET", "/api/salons/top-rated/", token=token)
    # Commenting out location-based test
    # test_endpoint("GET", "/api/salons/nearby/?lat=40.7128&lon=-74.0060", token=token)

    # 3. Stylist Operations
    print("Testing Stylist Operations")
    stylist_data = {
        "name": "Test Stylist",
        "email": "teststylist@example.com",
        "phone": "+1234567890",
        "specialties": "Haircut, Coloring",
        "years_of_experience": 5,
        "salon": salon_id
    }
    stylist_response = test_endpoint("POST", "/api/stylists/", stylist_data, token)
    stylist_id = stylist_response.get('id')
    test_endpoint("GET", f"/api/stylists/{stylist_id}/", token=token)
    test_endpoint("GET", f"/api/stylists/{stylist_id}/available_slots/?date=2024-08-15", token=token)

    # 4. Service Operations
    print("Testing Service Operations")
    service_data = {
        "name": "Haircut",
        "description": "Basic haircut",
        "price": 30.00,
        "duration": 30,
        "salon": salon_id
    }
    service_response = test_endpoint("POST", "/api/services/", service_data, token)
    service_id = service_response.get('id')
    test_endpoint("GET", f"/api/services/{service_id}/", token=token)

    # 5. Appointment Operations
    print("Testing Appointment Operations")
    appointment_data = {
        "customer": 1,  # Assuming the first user has id 1
        "stylist": stylist_id,
        "salon": salon_id,
        "service": "Haircut",
        "date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "start_time": "14:00:00",
        "end_time": "15:00:00",
        "status": "booked",
        "total_price": 30.00
    }
    appointment_response = test_endpoint("POST", "/api/appointments/", appointment_data, token)
    appointment_id = appointment_response.get('id')
    test_endpoint("GET", f"/api/appointments/{appointment_id}/", token=token)
    test_endpoint("POST", f"/api/appointments/{appointment_id}/confirm/", token=token)
    test_endpoint("POST", f"/api/appointments/{appointment_id}/cancel/", token=token)

    # 6. Review Operations
    print("Testing Review Operations")
    review_data = {
        "appointment": appointment_id,
        "rating": 5,
        "comment": "Great service!"
    }
    review_response = test_endpoint("POST", "/api/reviews/", review_data, token)
    review_id = review_response.get('id')
    test_endpoint("GET", f"/api/reviews/{review_id}/", token=token)

    # 7. Blog Operations
    print("Testing Blog Operations")
    blog_data = {
        "title": "Hair Care Tips",
        "content": "Here are some tips for maintaining healthy hair...",
        "author": 1  # Assuming the first user has id 1
    }
    blog_response = test_endpoint("POST", "/api/blogs/", blog_data, token)
    blog_id = blog_response.get('id')
    test_endpoint("GET", f"/api/blogs/{blog_id}/", token=token)

    # 8. Coupon Operations
    print("Testing Coupon Operations")
    coupon_data = {
        "code": "SUMMER20",
        "description": "20% off summer discount",
        "discount_type": "percentage",
        "discount_value": 20,
        "start_date": datetime.now().isoformat(),
        "end_date": (datetime.now() + timedelta(days=90)).isoformat(),
        "max_uses": 100
    }
    coupon_response = test_endpoint("POST", "/api/coupons/", coupon_data, token)
    coupon_id = coupon_response.get('id')
    test_endpoint("GET", f"/api/coupons/{coupon_id}/", token=token)

    # 9. Dashboard Operations
    print("Testing Dashboard Operations")
    test_endpoint("GET", "/api/super-admin-dashboard/", token=token)

    # 10. Notification Operations
    print("Testing Notification Operations")
    notification_data = {
        "message": "New feature available!"
    }
    test_endpoint("POST", "/api/notifications/", notification_data, token)

    # 11. Salon Analytics
    print("Testing Salon Analytics")
    test_endpoint("GET", f"/api/salons/{salon_id}/analytics/", token=token)

    print("All tests completed!")

if __name__ == "__main__":
    run_tests()
