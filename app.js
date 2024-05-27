document.addEventListener('DOMContentLoaded', function() {
    const apiUrl = 'http://192.168.0.155:8080'; // Update this URL if your Flask server runs on a different port

    // Register
    document.getElementById('register-form').addEventListener('submit', function(event) {
        event.preventDefault();

        const data = {
            name: document.getElementById('register-name').value,
            surname: document.getElementById('register-surname').value,
            nickname: document.getElementById('register-nickname').value,
            email: document.getElementById('register-email').value,
            password: document.getElementById('register-password').value,
        };

        fetch(`${apiUrl}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('response').innerText = JSON.stringify(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    // Login
    document.getElementById('login-form').addEventListener('submit', function(event) {
        event.preventDefault();

        const data = {
            email: document.getElementById('login-email').value,
            password: document.getElementById('login-password').value,
        };

        fetch(`${apiUrl}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('response').innerText = JSON.stringify(data);
            localStorage.setItem('token', data.access_token);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    // Upload
    document.getElementById('upload-form').addEventListener('submit', function(event) {
        event.preventDefault();

        const fileInput = document.getElementById('upload-file');
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        const token = localStorage.getItem('token');

        fetch(`${apiUrl}/upload`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
            },
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('response').innerText = JSON.stringify(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    // Protected Route
    document.getElementById('protected-btn').addEventListener('click', function() {
        const token = localStorage.getItem('token');

        fetch(`${apiUrl}/protected`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('response').innerText = JSON.stringify(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    // Download
    document.getElementById('download-form').addEventListener('submit', function(event) {
        event.preventDefault();

        const songId = document.getElementById('song-id').value;
        const token = localStorage.getItem('token');

        fetch(`${apiUrl}/download/${songId}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.blob();
        })
        .then(blob => {
            const url = window.URL.createObjectURL(new Blob([blob]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `song_${songId}.mp3`); // Set the file name
            document.body.appendChild(link);
            link.click();
            link.parentNode.removeChild(link);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
