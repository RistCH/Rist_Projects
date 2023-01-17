import pprint
from pymongo import MongoClient
from datetime import datetime
import sys, os

#Date & Time
now = datetime.now()
date_time = now.strftime("Date & Time: %m/%d/%Y, %H:%M:%S")
date_time_now = now.strftime("%m/%d/%Y %H:%M:%S")

#Client and Link for MongoDB Atlas (Cloud Database)
connection_str = f"mongodb+srv://RistCH:<password>@clusterrist.f3fn9o4.mongodb.net/?retryWrites=true&w=majority&authSource=admin"
client = MongoClient(connection_str)

#Hotel Booking Database
hotel_booking = client.Hotel_Booking
customer_details_collections = hotel_booking.Customer_Details

#Available Room Database
available_room = client.Available_Rooms
queen_vip_rooms = available_room.Queen_VIP_Room
single_rooms = available_room.Single_Room
double_rooms = available_room.Double_Room
triple_rooms = available_room.Triple_Room
quad_rooms = available_room.Quad_Room

#Taken Room Database
taken_room = client.Taken_Rooms
queen_vip_rooms_t = taken_room.Queen_VIP_Room
single_rooms_t = taken_room.Single_Room
double_rooms_t = taken_room.Double_Room
triple_rooms_t = taken_room.Triple_Room
quad_rooms_t = taken_room.Quad_Room

#Print the documents
print_details = pprint.PrettyPrinter()

class Hotel:
    def InsertHotelBooking(self):
        while True:
            print("Please input the customer details below: ")
            
            name = str(input("\nCustomer Name: "))
            contact_no = str(input("Contact No.: "))
            
            while True:
                print("\nChoose YOUR ROOM:")
                print("\n1. SINGLE ROOM \n2. DOUBLE ROOM \n3. TRIPLE ROOM \n4. QUAD ROOM \n5. QUEEN/VIP ROOM")
                Room_Category = int(input("\nRoom TYPES: "))
                if Room_Category == 1:
                    room_Type = "SINGLE ROOM"
                    price = 950.00
                elif Room_Category == 2:
                    room_Type = "DOUBLE ROOM"
                    price = 1200.00
                elif Room_Category == 3:
                    room_Type = "TRIPLE ROOM"
                    price = 1800
                elif Room_Category == 4:
                    room_Type = "QUAD ROOM"
                    price = 2400.00
                elif Room_Category == 5:
                    room_Type = "QUEEN/VIP ROOM"
                    price = 3600.00
                else:
                    print("Invalid Input.")
                    continue
                break
                
            Room_no = str(input("Room No.: "))
            check_in = input("Check-IN (YYYY-MM-DD): ")
            check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
            check_out = input("Check-OUT (YYYY-MM-DD): ")
            check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
            
            _id = Room_no
            self.Room_no = Room_no
            self.room_Type = room_Type
            
            customer_details = {
                "Name": name,
                "Contact_No": contact_no,
                "Room_Type": room_Type,
                "Price": price,
                "Room_No": Room_no,
                "Check-IN": check_in_date,
                "Check-OUT": check_out_date
            }
            
            customer_details_validator = {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["Name", "Contact_No", "Room_Type", "Price", "Room_No", 'Check-IN', 'Check-OUT'],
                        "properties": {
                            "Name": {
                                "bsonType": "string"
                            },
                            "Contact_No": {
                                "bsonType": "string",
                                "maxLength": 11
                            },
                            "Room_Type": {
                                "bsonType": "string"
                            },
                            "Price": {
                                "bsonType": "double"
                            },
                            "Room_No": {
                                "bsonType": "string"
                            },
                            "Check-IN": {
                                "bsonType": "date"
                            },
                            "Check-OUT": {
                                "bsonType": "date"
                            }
                        }
                    }
                }
            
            hotel_booking.command("collMod", "Customer_Details", validator=customer_details_validator)
            
            if self.room_Type == "QUEEN/VIP ROOM":
                queen_vip_rooms.delete_one({'_id': _id})
                queen_vip_rooms_t.insert_one({"_id": _id, "Room": self.Room_no})
            elif self.room_Type == "SINGLE ROOM":
                single_rooms.delete_one({'_id': _id})
                single_rooms_t.insert_one({"_id": _id, "Room": self.Room_no})
            elif self.room_Type == "DOUBLE ROOM":
                double_rooms.delete_one({'_id': _id})
                double_rooms_t.insert_one({"_id": _id, "Room": self.Room_no})
            elif self.room_Type == "TRIPLE ROOM":
                triple_rooms.delete_one({'_id': _id})
                triple_rooms_t.insert_one({"_id": _id, "Room": self.Room_no})
            elif self.room_Type == "QUAD ROOM":
                quad_rooms.delete_one({'_id': _id})
                quad_rooms_t.insert_one({"_id": _id, "Room": self.Room_no})
            
            customer_details_collections.insert_one(customer_details)
            break
                
    def type_again(self):
        while True:
            choice = input("\nDo you want to input again? Type Y/N: ")
            if choice.upper() == 'Y':
                H.cls()
                H.InsertHotelBooking()
            elif choice.upper() == 'N':
                break
            else:
                print("\nInvalid Input. Please Try Again!")
                continue
            
    def update_details(self):
        while True:
            if customer_details_collections.count_documents({}) > 0:
                pass
            else:
                print("THE CUSTOMER LIST IS EMPTY!")
                break
                
            field = input("What field do you want to update: ")
            value = input("\nWhat details do you want to update: ")
            
            new_value = input("\nWhat will be the new detail for the " + field + ": ")
            
            field_value = {field: value}
            
            update_details = {"$set":{field: new_value}}
            
            customer_details_collections.update_one(field_value, update_details)
            break
            
    def Available_Rooms(self):
        if queen_vip_rooms.count_documents({}) > 0:
            print("QUEEN/VIP ROOM")
            qv_room = queen_vip_rooms.find()
            for qvRoom in qv_room:
                print_details.pprint(qvRoom)
        else:
            print("There is NO AVAILABLE QUEEN/VIP ROOMS!")
        
        if single_rooms.count_documents({}) > 0:
            print("\nSINGLE ROOM")
            s_room = single_rooms.find()
            for sRoom in s_room:
                print_details.pprint(sRoom)
        else:
            print("There is NO AVAILABLE SINGLE ROOMS!")
            
        if double_rooms.count_documents({}) > 0:
            print("\nDOUBLE ROOM")
            d_room = double_rooms.find()
            for dRoom in d_room:
                print_details.pprint(dRoom)
        else:
            print("\nThere is NO AVAILABLE DOUBLE ROOMS!")
            
        if triple_rooms.count_documents({}) > 0:
            print("\nTRIPLE ROOM")
            t_room = triple_rooms.find()
            for tRoom in t_room:
                print_details.pprint(tRoom)
        else:
            print("\nThere is NO AVAILABLE TRIPLE ROOMS!")
           
        if quad_rooms.count_documents({}) > 0:
            print("\nQUAD ROOM")
            q_room = quad_rooms.find()
            for qRoom in q_room:
                print_details.pprint(qRoom)
        else:
            print("\nThere is NO AVAILABLE QUAD ROOMS!") 
        
    def Reserved_Rooms(self):
        if queen_vip_rooms_t.count_documents({}) > 0:
            print("QUEEN/VIP ROOM")
            qv_room = queen_vip_rooms_t.find()
            for qvRoom in qv_room:
                print_details.pprint(qvRoom)
        elif queen_vip_rooms_t.count_documents({}) == 4:
            print("The QUEEN/VIP ROOMS are all RESERVED")
        else:
            print("There is NO RESERVED QUEEN/VIP ROOMS!")
        
        if single_rooms_t.count_documents({}) > 0:
            print("\nSINGLE ROOM")
            s_room = single_rooms_t.find()
            for sRoom in s_room:
                print_details.pprint(sRoom)
        elif single_rooms_t.count_documents({}) == 4:
            print("\nThe SINGLE ROOMS are all RESERVED")
        else:
            print("\nThere is NO RESERVED SINGLE ROOMS!")
            
        if double_rooms_t.count_documents({}) > 0:
            print("\nDOUBLE ROOM")
            d_room = double_rooms_t.find()
            for dRoom in d_room:
                print_details.pprint(dRoom)
        elif double_rooms_t.count_documents({}) == 4:
            print("\nThe DOUBLE ROOMS are all RESERVED")
        else:
            print("\nThere is NO RESERVED DOUBLE ROOMS!")
            
        if triple_rooms_t.count_documents({}) > 0:
            print("\nTRIPLE ROOM")
            t_room = triple_rooms_t.find()
            for tRoom in t_room:
                print_details.pprint(tRoom)
        elif triple_rooms_t.count_documents({}) == 4:
            print("\nThe TRIPLE ROOMS are all RESERVED")
        else:
            print("\nThere is NO RESERVED TRIPLE ROOMS!")
           
        if quad_rooms_t.count_documents({}) > 0:
            print("\nQUAD ROOM")
            q_room = quad_rooms_t.find()
            for qRoom in q_room:
                print_details.pprint(qRoom)
        elif quad_rooms_t.count_documents({}) == 4:
            print("\nThe QUAD ROOMS are all RESERVED")
        else:
            print("\nThere is NO RESERVED QUAD ROOMS!")

    def display(self):
        if customer_details_collections.count_documents({}) > 0:
            print("CUSTOMER DETAILS as of " + date_time_now + ": \n")
            pass
        else:
            print("THE CUSTOMER LIST IS EMPTY!")
        
        customer = customer_details_collections.find()
        for customers_list in customer:
            print_details.pprint(customers_list)
            print('\n')
            
    def delete_All(self):
        while True:
            if customer_details_collections.count_documents({}) > 0:
                pass
            else:
                print("\nTHE CUSTOMER LIST IS EMPTY!")
                break
                
            choice = input("Are you sure that you want to clear the whole customer list? Type Y/N: ")
            if choice.upper() == 'Y':
                customer_list_delete = client.Hotel_Booking.Customer_Details
                customer_list_delete.delete_many({})
                
                single_rooms_t.delete_many({})
                single_rooms.delete_many({})
                single_rooms.insert_many([{'_id': "101", 'Room': "101"}, {'_id': "102", 'Room': "102"}, {'_id': "103", 'Room': "103"}, {'_id': "104", 'Room': "104"}])
                
                double_rooms_t.delete_many({})
                double_rooms.delete_many({})
                double_rooms.insert_many([{'_id': "201", 'Room': "201"}, {'_id': "202", 'Room': "202"}, {'_id': "203", 'Room': "203"}, {'_id': "204", 'Room': "204"}])
                
                triple_rooms_t.delete_many({})
                triple_rooms.delete_many({})
                triple_rooms.insert_many([{'_id': "301", 'Room': "301"}, {'_id': "302", 'Room': "302"}, {'_id': "303", 'Room': "303"}, {'_id': "304", 'Room': "304"}])
                
                quad_rooms_t.delete_many({})
                quad_rooms.delete_many({})
                quad_rooms.insert_many([{'_id': "401", 'Room': "401"}, {'_id': "402", 'Room': "402"}, {'_id': "403", 'Room': "403"}, {'_id': "404", 'Room': "404"}])
                
                queen_vip_rooms_t.delete_many({})
                queen_vip_rooms.delete_many({})
                queen_vip_rooms.insert_many([{'_id': "001", 'Room': "001"}, {'_id': "002", 'Room': "002"}, {'_id': "003", 'Room': "003"}, {'_id': "004", 'Room': "004"}])
                
            elif choice.upper() == 'N':
                break
            else:
                print("Invalid Input. Please Try Again!")
                continue
    
    def delete_One(self):
        while True: 
            if customer_details_collections.count_documents({}) > 0:
                pass
            else:
                print("\nTHE CUSTOMER LIST IS EMPTY!")
                break
            
            choice = input("Are you sure that you want to delete a customer list? Type Y/N: ")
            if choice.upper() == 'Y':
                H.cls()
                from bson.objectid import ObjectId
                customer_id = input("\nPlease Enter the Object ID of document that you want to delete: ")
                customer_details_collections.delete_one({'_id': ObjectId(customer_id)})
                print("\nPlease enter the type of room: ") 
                print("\n1. SINGLE ROOM \n2. DOUBLE ROOM \n3. TRIPLE ROOM \n4. QUAD ROOM \n5. QUEEN/VIP ROOM")
                Room_type = int(input("\n\nInput 1-6: "))
                Room_num = input("\nPlease enter the room number: ") 
            
                if Room_type == 1:
                    single_rooms_t.delete_one({'_id': Room_num, 'Room': Room_num})
                    single_rooms.insert_one({'_id': Room_num, 'Room': Room_num})
                    break
                elif Room_type == 2:
                    double_rooms_t.delete_one({'_id': Room_num, 'Room': Room_num})
                    double_rooms.insert_one({'_id': Room_num, 'Room': Room_num})
                    break
                elif Room_type == 3:
                    triple_rooms_t.delete_one({'_id': Room_num, 'Room': Room_num})
                    triple_rooms.insert_one({'_id': Room_num, 'Room': Room_num})
                    break
                elif Room_type == 4:
                    quad_rooms_t.delete_one({'_id': Room_num, 'Room': Room_num})
                    quad_rooms.insert_one({'_id': Room_num, 'Room': Room_num})
                    break
                elif Room_type == 5:
                    queen_vip_rooms_t.delete_one({'_id': Room_num, 'Room': Room_num})
                    queen_vip_rooms.insert_one({'_id': Room_num, 'Room': Room_num})
                    break
                else:
                    print("Invalid Input. Please Try Again!")
                    continue

            elif choice.upper() == 'N':
                break
            else:
                print("Invalid Input. Please Try Again!")
                continue
           
    def cls(self):
        os.system('cls||clear')
            
    def exit(self):
        while True:
            exit = input("Do you want to exit the program? Type Y/N: ")
            if exit.upper() == 'Y':
                sys.exit()
            elif exit.upper() == 'N':
                pass
            else:
                print("Invalid Input. Please Try Again!")
                continue
            
    def main_menu(self):
        while True:
            choice = input("\nGo back to main menu? Type Y/N: ")
            if choice.upper() == 'Y':
                break
            elif choice.upper() == 'N':
                continue
            else:
                print("Invalid Input. Please Try Again!")
                pass
            
H = Hotel()
while True:
    H.cls()
    print("HOTEL RESERVATION SYSTEM - with PyMongo\n")
    print("1. Display Queue \n2. Add Reservation \n3. Update Customer Details \n4. Check Available & Reserved Rooms. \n5. Delete or Cancel Booking \n6. Exit Program")
    input_num = int(input("\nInput 1-6: "))
    
    if input_num == 1:
        H.cls()
        H.display()
        H.main_menu()
        
    elif input_num == 2:
        H.cls()
        H.InsertHotelBooking()
        H.type_again()
        H.main_menu()
    
    elif input_num == 3:
        H.cls()
        H.update_details()
        H.main_menu()

    elif input_num == 4:
        while True:
            H.cls()
            print("1. AVAILABLE Rooms \n2. RESERVED Rooms \n3. Go back to MAIN MENU")
            choice = int(input("\nInput 1-3: "))
            if choice == 1:
                H.cls()
                H.Available_Rooms()
                H.main_menu()
                break
            
            elif choice == 2:
                H.cls()
                H.Reserved_Rooms()
                H.main_menu()
                
            elif choice == 3:
                break
                
            else:
                print("Invalid Input. Please Try Again Later!")
        
    elif input_num == 5:
        while True:
            H.cls()
            print("1. Delete a booking \n2. Delete ALL Bookings \n3. Go back to MAIN MENU")
            choice = int(input("\nInput 1-3: "))
            
            if choice == 1:
                H.cls()
                H.delete_One()
                H.main_menu()
                break
            
            elif choice == 2:
                H.cls()
                H.delete_All()
                H.main_menu()
                break
            
            elif choice == 3:
                break
                
            else:
                print("Invalid Input. Please Try Again Later!")
            
        
    elif input_num == 6:
        H.cls()
        H.exit()
    
    else:
        print("Invalid Input. Please Try Again!")
        continue

    


