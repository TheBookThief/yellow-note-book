document.getElementById('upload-form-encode').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission

    let formData = new FormData();
    formData.append('file', document.getElementById('fileInput').files[0]);
    formData.append('polynomial', document.getElementById('polynomialInput').value);

    // Create AJAX request to send the file to the server
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/encode', true);

    // Set up the callback to handle the server response
    xhr.onload = function() {
      if (xhr.status === 200) {
        let response = JSON.parse(xhr.responseText);
        
      } else {
        
      }
    };

    // Send the form data (which contains the file)
    xhr.send(formData);
  });