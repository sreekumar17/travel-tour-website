document.getElementById('tourBookingForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const tour = document.getElementById('tour').value;
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;

    // Create the booking object
    const booking = { tour, name, email };


    console.log("booking", booking)
    // Send the booking to the backend
    fetch('http://127.0.0.1:5000/book', {  // Ensure this URL matches your Flask API
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(booking),
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);  // Log the response data

            // Clear form fields
            document.getElementById('tourBookingForm').reset();
            document.getElementById('responseMessage').innerText = "Booking submitted successfully!";

            // Fetch updated bookings
            fetchBookings(); // Call function to fetch and display bookings
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});

// Function to display all bookings
function fetchBookings() {
    fetch('http://127.0.0.1:5000/bookings')  // Ensure this URL matches your Flask API
        .then(response => response.json())
        .then(data => {
            const bookingCardsContainer = document.getElementById('bookingCards');
            bookingCardsContainer.innerHTML = '';  // Clear existing bookings

            data.forEach(booking => {
                const bookingCard = document.createElement('div');
                bookingCard.className = 'booking-card';
                bookingCard.innerHTML = `
                    <h3>${booking.tour}</h3>
                    <p>Name: ${booking.name}</p>
                    <p>Email: ${booking.email}</p>
                `;
                bookingCardsContainer.appendChild(bookingCard);
            });
        })
        .catch((error) => {
            console.error('Error fetching bookings:', error);
        });
}

// Initial fetch to display bookings when the page loads
fetchBookings();
