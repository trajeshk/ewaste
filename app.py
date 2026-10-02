# ==============================================================================
# PROJECT TITLE: E-WASTE MANAGEMENT SYSTEM
# CLASS: XII CS (CBSE PRACTICAL ASSESSMENT 2026-2027)
# MODULE: MAIN APPLICATION SOURCE CODE
# ==============================================================================
import mysql.connector
from datetime import date
def get_db_connection():
    """
    Establishes and returns a connection to the MySQL database.
    Handles potential connection errors gracefully.
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="user",
            password="password",  # Substitute with your MySQL password
            database="ewaste_db"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"\n[ERROR]: Database Connection Failed! Details: {err}")
        return None
def register_user():
    """
    Registers a new user in the system and stores details in MySQL database.
    """
    conn = get_db_connection()
    if not conn:
        return
    cursor = conn.cursor()
    print("\n==========================================")
    print("        NEW USER REGISTRATION MODULE      ")
    print("==========================================")
    name = input("Enter Full Name: ").strip()
    phone = input("Enter Phone Number: ").strip()
    if not name or not phone:
        print("[WARNING]: Name and Phone number cannot be empty!")
        return
    try:
        query = "INSERT INTO users (name, phone, eco_points) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, phone, 0))
        conn.commit()
        print(f"\n[SUCCESS]: User registered successfully!")
        print(f"--> Assigned User ID: {cursor.lastrowid}")
    except mysql.connector.Error as err:
        print(f"[ERROR]: Failed to register user. Details: {err}")
    finally:
        cursor.close()
        conn.close()
def log_ewaste_request():
    """
    Logs an e-waste pickup request for an existing user and awards Eco-Points.
    """
    conn = get_db_connection()
    if not conn:
        return
    cursor = conn.cursor()
    print("\n==========================================")
    print("      LOG E-WASTE PICKUP REQUEST          ")
    print("==========================================")
    try:
        user_id = int(input("Enter your User ID: "))
        # Check if user exists
        cursor.execute("SELECT name, eco_points FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        if not user:
            print(f"[ERROR]: User ID {user_id} not found! Please register first.")
            return
        print(f"\nWelcome back, {user[0]}! (Current Eco-Points: {user[1]})")
        print("\nSelect Category:")
        print("1. Mobiles / Tablets / Smartwatches")
        print("2. Laptops / Desktops / Peripherals")
        print("3. Batteries / Power Banks / Chargers")
        print("4. Large Home Appliances (Refrigerators, ACs)")
        cat_choice = input("Enter Choice (1-4): ").strip()
        categories = {
            "1": "Mobiles/Tablets",
            "2": "Laptops/Desktops",
            "3": "Batteries/Power Supplies",
            "4": "Home Appliances"
        }
        category = categories.get(cat_choice, "Other Electronics")

        weight = float(input("Enter estimated weight in kg: "))
        if weight <= 0:
            print("[ERROR]: Weight must be greater than zero.")
            return
        today = date.today()
        # Insert Request
        query = """INSERT INTO pickup_requests (user_id, item_category, weight_kg, status, request_date) 
                   VALUES (%s, %s, %s, 'Pending', %s)"""
        cursor.execute(query, (user_id, category, weight, today))
        # Calculate Eco-Points (10 points per kg)
        points_earned = int(weight * 10)
        cursor.execute("UPDATE users SET eco_points = eco_points + %s WHERE user_id = %s", (points_earned, user_id))
        conn.commit()
        print(f"\n[SUCCESS]: Pickup request logged successfully!")
        print(f"--> Earned Eco-Points: +{points_earned}")
    except ValueError:
        print("[ERROR]: Invalid numerical input provided.")
    except mysql.connector.Error as err:
        print(f"[ERROR]: Database operation failed: {err}")
    finally:
        cursor.close()
        conn.close()
def view_all_requests():
    """
    Administrative function to view all logged pickup requests across all users.
    Uses SQL JOIN to display combined table records.
    """
    conn = get_db_connection()
    if not conn:
        return
    cursor = conn.cursor()    
    print("\n================================================================================")
    print("                    ADMIN DASHBOARD - ALL PICKUP REQUESTS                        ")    
    print("================================================================================")
    query = """
    SELECT r.request_id, u.name, u.phone, r.item_category, r.weight_kg, r.status, r.request_date
    FROM pickup_requests r
    JOIN users u ON r.user_id = u.user_id
    ORDER BY r.request_id DESC
    """
    try:
        cursor.execute(query)
        records = cursor.fetchall()

        if not records:
            print("\n[INFO]: No pickup requests found in system.")
        else:
            print(f"{'Req ID':<8} | {'User Name':<15} | {'Phone':<12} | {'Category':<20} | {'Weight (kg)':<10} | {'Status':<10}")
            print("-" * 88)
            for row in records:
                print(f"{row[0]:<8} | {row[1]:<15} | {row[2]:<12} | {row[3]:<20} | {row[4]:<10} | {row[5]:<10}")
    except mysql.connector.Error as err:
        print(f"[ERROR]: Database query failed: {err}")
    finally:
        cursor.close()
        conn.close()
def update_request_status():
    """
    Administrative function to update the processing status of a pickup request.
    """
    conn = get_db_connection()
    if not conn:
        return
    cursor = conn.cursor()
    print("\n==========================================")
    print("     ADMIN - UPDATE REQUEST STATUS        ")
    print("==========================================")
    try:
        req_id = int(input("Enter Request ID to update: "))
        print("\nStatuses: 1. Pending | 2. Collected | 3. Processed")
        choice = input("Select New Status (1-3): ").strip()
        status_map = {"1": "Pending", "2": "Collected", "3": "Processed"}
        new_status = status_map.get(choice)
        if not new_status:
            print("[ERROR]: Invalid status selection.")
            return
        query = "UPDATE pickup_requests SET status = %s WHERE request_id = %s"
        cursor.execute(query, (new_status, req_id))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"\n[SUCCESS]: Request #{req_id} updated to status '{new_status}'.")
        else:
            print(f"\n[ERROR]: Request ID #{req_id} not found.")
    except ValueError:
        print("[ERROR]: Invalid Request ID format.")
    except mysql.connector.Error as err:
        print(f"[ERROR]: Database update failed: {err}")
    finally:
        cursor.close()
        conn.close()
def main_menu():
    """
    Main driver execution loop providing interactive CLI menu interface.
    """
    while True:        
        print("\n==================================================")
        print("    E-WASTE MANAGEMENT SYSTEM - CLASS XII CS      ")        
        print("==================================================")
        print("1. Register New Citizen User")
        print("2. Submit E-Waste Pickup Request")
        print("3. Admin: View All Pickup Requests")
        print("4. Admin: Update Request Fulfillment Status")
        print("5. Exit System")        
        print("==================================================")
        choice = input("Enter Choice Option (1-5): ").strip()
        if choice == '1':
            register_user()
        elif choice == '2':
            log_ewaste_request()
        elif choice == '3':
            view_all_requests()
        elif choice == '4':
            update_request_status()
        elif choice == '5':
            print("\nThank you for using E-Waste Management System. Protect the Planet!")
            break
        else:
            print("\n[INVALID]: Option not recognized. Please choose from 1 to 5.")
if __name__ == "__main__":
    main_menu()

