const express = require('express')
const multer = require('multer');
const bodyParser = require('body-parser')
const { spawn } = require('child_process');
const path = require('path');
const app = express()
const port = 3001

const storage = multer.diskStorage({
    destination: (req, file, cb) => {
      cb(null, 'uploads/'); // File will be uploaded to the 'uploads' folder
    },
    filename: (req, file, cb) => {
      cb(null, Date.now() + path.extname(file.originalname)); // Create unique filename
    }
  });
  
const upload = multer({ storage: storage });

app.use(express.static('public'));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.post('/api/encode', upload.single('file'), (req, res) => {
    if (!req.file) {
      return res.status(400).send('No file uploaded');
    }

    const args = ['arg1', 'arg2', 'arg3'];

    // Spawn the Python script with arguments
    const pythonProcess = spawn('python', ['./python/test.py', ...args]);  // Use 'python3' on some systems

    // Capture the output from the Python script
    pythonProcess.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`);
        console.log(2738)
    });

    // Capture any errors from the Python script
pythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
    
  });
  
  // Handle the completion of the process
  pythonProcess.on('close', (code) => {
    console.log(`Python process exited with code ${code}`);
  });

    console.log(req.file.path)
    console.log(req.body.polynomial)
    res.json({ message: 'File uploaded successfully', file: req.file });
});
  

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})