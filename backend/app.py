from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import tkinter as tk
from tkinter import messagebox
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# In-memory storage for bookings (for demonstration purposes)
bookings = []

@app.route('/book', methods=['POST'])
def book_tour():
    data = request.get_json()
    bookings.append(data)  # Save booking in the list
    return jsonify(data), 201  # Return the booking data as response

@app.route('/bookings', methods=['GET'])
def get_bookings():
    return jsonify(bookings)

# Tkinter GUI Function
def run_tkinter_app():
    def book():
        tour = tour_entry.get().strip()
        name = name_entry.get().strip()
        email = email_entry.get().strip()

        # Basic validation
        if not tour or not name or not email:
            messagebox.showerror("Input Error", "All fields are required.")
            return

        # Make a POST request to the Flask backend
        response = requests.post('http://127.0.0.1:5000/book', json={
            'tour': tour,
            'name': name,
            'email': email
        })

        if response.status_code == 201:
            messagebox.showinfo("Success", "Booking Successful!")
            tour_entry.delete(0, tk.END)
            name_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Booking Failed!")

    def view_bookings():
        # Fetch and display bookings
        response = requests.get('http://127.0.0.1:5000/bookings')
        if response.status_code == 200:
            bookings_list = response.json()
            if bookings_list:
                booking_info = "\n".join(
                    [f"Tour: {b['tour']}, Name: {b['name']}, Email: {b['email']}" for b in bookings_list]
                )
                messagebox.showinfo("Bookings", booking_info)
            else:
                messagebox.showinfo("Bookings", "No bookings found.")
        else:
            messagebox.showerror("Error", "Failed to retrieve bookings.")

    # Create the main window
    root = tk.Tk()
    root.title("Tour Booking")

    # Create and place the labels and entries
    tk.Label(root, text="Tour Name:").pack()
    tour_entry = tk.Entry(root)
    tour_entry.pack()

    tk.Label(root, text="Your Name:").pack()
    name_entry = tk.Entry(root)
    name_entry.pack()

    tk.Label(root, text="Your Email:").pack()
    email_entry = tk.Entry(root)
    email_entry.pack()

    # Create and place the booking button
    book_button = tk.Button(root, text="Book Tour", command=book)
    book_button.pack()

    # Create and place the view bookings button
    view_button = tk.Button(root, text="View Bookings", command=view_bookings)
    view_button.pack()

    # Run the Tkinter event loop
    root.mainloop()

if __name__ == '__main__':
    # Start the Flask app in the main thread
    threading.Thread(target=app.run, kwargs={'debug': True, 'use_reloader': False}).start()
    
    # Run the Tkinter application
    run_tkinter_app()
