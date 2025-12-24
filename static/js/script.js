function login() {
    // Get form data
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Construct request body
    const requestBody = {
        username: username,
        password: password
    };

    // Send POST request to /getProfile endpoint
    fetch('http://localhost:8080/getProfile', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Profile data:', data);
        // Optionally, redirect to the user's profile page or display the profile data
    })
    .catch(error => {
        console.error('Error fetching profile data:', error);
        // Handle errors, show an error message to the user, etc.
    });
}
