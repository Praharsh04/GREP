const express = require('express');
const multer = require('multer');
const path = require('path');
const cors = require('cors');
const fs = require('fs');

const app = express();
const port = 3000;

app.use(cors());
app.use(express.json());

// Ensure Images directory exists
const imagesDir = path.join(__dirname, 'Images');
if (!fs.existsSync(imagesDir)) {
  fs.mkdirSync(imagesDir);
}

// Serve the image mapping file specifically
app.get('/image-mapping', (req, res) => {
  const mappingPath = path.join(__dirname, 'image_mapping.json');
  if (fs.existsSync(mappingPath)) {
    res.sendFile(mappingPath);
  } else {
    res.json({});
  }
});

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'Images/');
  },
  filename: function (req, file, cb) {
    const wordName = req.body.wordName.toLowerCase().replace(/\s+/g, '_');
    const ext = path.extname(file.originalname) || '.png';
    cb(null, `${wordName}${ext}`);
  }
});

const upload = multer({ storage: storage });

app.post('/upload-image', upload.single('image'), (req, res) => {
  if (!req.file) return res.status(400).send('No file uploaded.');
  
  const wordName = req.body.wordName.toLowerCase();
  const filename = req.file.filename;
  
  const mappingPath = path.join(__dirname, 'image_mapping.json');
  let mapping = {};
  if (fs.existsSync(mappingPath)) {
    mapping = JSON.parse(fs.readFileSync(mappingPath, 'utf8'));
  }
  
  mapping[wordName] = `/Images/${filename}`;
  fs.writeFileSync(mappingPath, JSON.stringify(mapping, null, 2));
  
  res.json({ url: mapping[wordName] });
});

// Serve static files
app.use('/Images', express.static(path.join(__dirname, 'Images')));
app.use(express.static(__dirname));

app.listen(port, () => {
  console.log(`Local editor server running at http://localhost:${port}`);
});
