document.getElementById('myForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent the default form submission

    const formData = new FormData(this);
    const data_list = []
    const data = Object.fromEntries(formData.entries());
    data_list.push(data);

    try {
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data_list)
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();

        alert(JSON.stringify(result));
        console.log('Success:', result);
    } catch (error) {
        console.error('Error:', error);
    }
});