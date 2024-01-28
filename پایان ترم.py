from abc import ABC, abstractmethod
from datetime import datetime
import json

class Person(ABC):
    def __init__(self, unique_id, name, contact_info):
        self.unique_id = unique_id
        self.name = name
        self.contact_info = contact_info
    
    @abstractmethod
    def __str__(self):
        pass

class Guest(Person):
    def __init__(self, unique_id, name, contact_info):
        super().__init__(unique_id, name, contact_info)
        self.booking_date = None
        self.check_in_date = None
        self.check_out_date = None
    
    def check_in(self, date):
        self.check_in_date = date
    
    def check_out(self):
        self.check_out_date = datetime.today()
    
    def __str__(self):
        return f"<Guest: {self.name} - ID: {self.unique_id} - Contact: {self.contact_info}>"

class Room:
    def __init__(self, room_number, room_type):
        self.room_number = room_number
        self.room_type = room_type
        self.availability = True
        self.booking_details = {}
    
    def check_availability(self, date):
        if date in self.booking_details:
            if self.booking_details[date]['status'] == 'booked':
                return False
            else:
                return True
        else:
            return True
    
    def book(self, date, guest_id):
        if self.check_availability(date):
            self.booking_details[date] = {'guest_id': guest_id,'status': 'booked'}
            return f"Room Now Booked"
        else:
            return f"<Room: {self.room_number} Can't be booked! >"

    
    def __str__(self):
        return f"<Room: {self.room_number} - Type: {self.room_type} - Availability: {self.availability}>"

class Staff(Person):
    def __init__(self, unique_id, name, contact_info, position):
        super().__init__(unique_id, name, contact_info)
        self.position = position
    
    def __str__(self):
        return f"<Staff: {self.name} - ID: {self.unique_id} - Contact: {self.contact_info} - Position: {self.position}>"

class Hotel:
    def __init__(self, name):
        self.name = name
        self.guests = {}
        self.rooms = {}
        try:
            self.load_data()
        except:
            ...
    
    def add_guest(self, guest_id, name, contact_info):
        guest = Guest(guest_id, name, contact_info)
        self.guests[guest_id] = {'name':name, 'contact_info':contact_info}
    
    def remove_guest(self, guest_id):
        if guest_id in self.guests:
            del self.guests[guest_id]
            print("Removed!")
    
    def get_guest_details(self, guest_id):
        if guest_id in self.guests:
            return str(self.guests[guest_id])
        else:
            return "Guest not found"
    
    def add_room(self, room_number, room_type):
        room = Room(room_number, room_type)
        self.rooms[room_number] = {'room_type':room_type}
    
    def remove_room(self, room_number):
        if room_number in self.rooms:
            del self.rooms[room_number]
            print("Room Remove !")
    
    def get_room_details(self, room_number):
        if room_number in self.rooms:
            return str(self.rooms[room_number])
        else:
            return "Room not found"
    
    
    def save_data(self):
        with open('guests.json', 'w') as f: # w = write
            json.dump(self.guests, f, indent=4)
        
        with open('rooms.json', 'w') as f:
            json.dump(self.rooms, f, indent=4)
        
    
    def load_data(self):
        with open('guests.json', 'r') as f: # r = read
            self.guests = json.load(f)

        with open('rooms.json', 'r') as f:
            self.rooms = json.load(f)
        

    def __str__(self):
        return f"<Hotel: {self.name} - Number of guests: {len(self.guests)} - Number of rooms: {len(self.rooms)}>"
    
hotel = Hotel("Hotel Glory")

while True:
    print("1. Add guest")
    print("2. Remove guest")
    print("3. Add room")
    print("4. Remove room")
    print("5. Get guest details")
    print("6. Get room details")
    print("7. Get hotel details")
    print("8. Booking")
    print("0. Exit")
    
    cmd = input("Enter your cmd: ")
    
    if cmd == "1":
        guest_id = input("Enter guest ID: ")
        name = input("Enter guest name: ")
        contact_info = input("Enter guest contact info: ")
        hotel.add_guest(guest_id, name, contact_info)
        print("Guest added successfully!")
    
    elif cmd == "2":
        guest_id = input("Enter guest ID: ")
        hotel.remove_guest(guest_id)
        print("Guest removed successfully!")
    
    elif cmd == "3":
        room_number = input("Enter room number: ")
        room_type = input("Enter room type: ")
        hotel.add_room(room_number, room_type)
        print("Room added successfully!")
    
    elif cmd == "4":
        room_number = input("Enter room number: ")
        hotel.remove_room(room_number)
        print("Room removed successfully!")
    
    elif cmd == "5":
        guest_id = input("Enter guest ID: ")
        guest_details = hotel.get_guest_details(guest_id)
        print(guest_details)
    
    elif cmd == "6":
        room_number = input("Enter room number: ")
        room_details = hotel.get_room_details(room_number)
        print(room_details)
    
    elif cmd == "7":
        print(hotel.__str__())
    
    elif cmd == "8":
        all_rooms = hotel.rooms
        print(hotel.rooms)
        booking_id = input("Enter Room ID: ")
        if all_rooms[booking_id] :
            guest_id = input("Enter  Gust ID : ")
            if hotel.guests[guest_id]:
                room = hotel.rooms[booking_id]
                print(room.book(date=datetime.today().strftime('%Y-%m-%d'), guest_id=guest_id))
            else:
                print("Not Guest Found !")
        else:
            print("Not Rooms Found !")
    
    elif cmd == "0":
        hotel.save_data()
        print("Exiting...")
        break
    
    else:
        print("Invalid cmd. Please try again.")
