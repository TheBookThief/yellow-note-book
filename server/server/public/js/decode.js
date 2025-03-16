document.getElementById('upload-form-decode').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission

    let formData = new FormData();
    formData.append('file', document.getElementById('fileInput-decode').files[0]);

    // Create AJAX request to send the file to the server
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/decode', true);

    // Set up the callback to handle the server response
    xhr.onload = function() {
      if (xhr.status === 200) {
        let response = JSON.parse(xhr.responseText);
        if (response.success) {
            let input = document.getElementById('decode-submit')
            let output = document.getElementById('decode-output')
            let result = document.getElementById('result-decoded')
            let img = document.getElementById('de-spectorgram')
            result.innerHTML = response.result  
            img.setAttribute('src', '/spect/' + response.name + ".png")
            input.style.display = 'none'
            output.style.display = 'block'
        } else {
            alert('Failed to decode polynomial.')
        }
      } else {
        alert("Unknown error.")
      }
    };

    // Send the form data (which contains the file)
    xhr.send(formData);
  });