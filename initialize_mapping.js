const fs = require('fs');
const path = require('path');

const imagesDir = path.join(__dirname, 'Images');
const mappingPath = path.join(__dirname, 'image_mapping.json');

if (!fs.existsSync(imagesDir)) {
  console.log('Images directory does not exist.');
  process.exit(0);
}

const files = fs.readdirSync(imagesDir);
const mapping = {};

files.forEach(file => {
  if (file.match(/\.(jpg|jpeg|png|webp|svg|gif)$/i)) {
    // Basic heuristic: take the first part before underscore or dot
    const wordName = path.parse(file).name.toLowerCase().split('_')[0].split('.')[0];
    mapping[wordName] = `/Images/${file}`;
  }
});

fs.writeFileSync(mappingPath, JSON.stringify(mapping, null, 2));
console.log('image_mapping.json initialized with existing images.');
