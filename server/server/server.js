const express = require('express')
const multer = require('multer');
const bodyParser = require('body-parser')
const { spawn } = require('child_process');
const path = require('path');
const app = express()
const port = 3001

const storage = multer.diskStorage({
    destination: (req, file, cb) => {
      cb(null, 'uploads/'); 
    },
    filename: (req, file, cb) => {
      cb(null, Date.now() + path.extname(file.originalname));
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

    let filename = req.file.path

    console.log(filename.replace('\\', '/'))

    const args = [  './python/compile.py', 
                    req.body.polynomial,
                    filename
                ];

    // Spawn the Python script with arguments
    const pythonProcess = spawn('python', args);
    // Capture the output from the Python script
    ended = false;
    pythonProcess.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`);
        if (data.toString().startsWith('ok')) {
            res.json({ name: req.file.filename.split('.')[0], success: true });
            ended = true
            res.end();
        } else {
            res.json({ success: false });
            ended = true
            res.end();
        }
    });

    pythonProcess.stderr.on('data', (data) => {
        console.log(`stderr: ${data}`)
        if (!ended){
            ended = true
            res.json({ success: false });
            res.end();
        }
        //console.error(`stderr: ${data}`);
    });
});
  

app.post('/api/decode', upload.single('file'), (req, res) => {
    if (!req.file) {
      return res.status(400).send('No file uploaded');
    }

    let filename = req.file.path

    const args = [  './python/compile.py', 
                    './uploads/' + filename, 
                    req.body.polynomial
                ];

    // Spawn the Python script with arguments
    const pythonProcess = spawn('python', args);  // Use 'python3' on some systems

    // Capture the output from the Python script
    pythonProcess.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`);
        res.json({ message: 'File uploaded successfully' });
    });

    console.log(req.file.path)
    console.log(req.body.polynomial)
});

app.listen(port, () => {
  console.log(`App listening on port ${port}`)
})