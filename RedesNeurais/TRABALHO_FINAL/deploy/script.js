
'use strict'


var forms = document.querySelectorAll('.needs-validation')
Array.prototype.slice.call(forms)
    .forEach(function (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault()
            event.stopPropagation()
            if (form.checkValidity()) {
                // Form is valid, make the API request
                const formData = new FormData(form);
                const data_list = []
                const data = Object.fromEntries(formData.entries());
                data_list.push(data);
                console.log(JSON.stringify(data_list))

                fetch('http://localhost:5000/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data_list),
                })
                .then(response => response.json())
                .then(result => {
                    console.log('Success:', result);
                    // Handle the response here
                    const resultMessage = document.getElementById('resultMessage');
                    const alertDiv = resultMessage.querySelector('.alert');
                    
                    alertDiv.textContent = `${result.content.mensagem} (${result.content.porcentagem})`;
                    alertDiv.className = 'alert ' + (result.content.contratar ? 'alert-success' : 'alert-danger');
                    
                    resultMessage.style.display = 'block';
                })
                .catch((error) => {
                    console.error('Error:', error);
                    // Handle errors here
                    const resultMessage = document.getElementById('resultMessage');
                    const alertDiv = resultMessage.querySelector('.alert');
                    
                    alertDiv.textContent = 'Ocorreu um erro ao processar a solicitação.';
                    alertDiv.className = 'alert alert-danger';
                    
                    resultMessage.style.display = 'block';
                });
            }
            form.classList.add('was-validated')
        }, false)
    })

// document.getElementById('myForm').addEventListener('submit', async function(event) {
//     event.preventDefault(); // Prevent the default form submission

//     const formData = new FormData(this);
//     const data_list = []
//     const data = Object.fromEntries(formData.entries());
//     data_list.push(data);

//     try {
//         const response = await fetch('http://127.0.0.1:5000/predict', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify(data_list)
//         });

//         if (!response.ok) {
//             throw new Error('Network response was not ok');
//         }

//         const result = await response.json();

//         modal.style.display = "block";


//         alert(JSON.stringify(result));
//         console.log('Success:', result);
//     } catch (error) {
//         console.error('Error:', error);
//     }
// });