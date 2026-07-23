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

// Sort files to process less-preferred extensions first, so preferred extensions overwrite them.
// Preference: gif > webp > png > jpg > jpeg > avif > svg
const extensionPreference = ['svg', 'avif', 'jpeg', 'jpg', 'png', 'webp', 'gif'];

const sortedFiles = files.sort((a, b) => {
  const extA = path.extname(a).slice(1).toLowerCase();
  const extB = path.extname(b).slice(1).toLowerCase();
  const prefA = extensionPreference.indexOf(extA);
  const prefB = extensionPreference.indexOf(extB);
  return prefA - prefB;
});

sortedFiles.forEach(file => {
  if (file.match(/\.(jpg|jpeg|png|webp|svg|gif|avif)$/i)) {
    // Basic heuristic: take the first part before underscore or dot
    const wordName = path.parse(file).name.toLowerCase().split('_')[0].split('.')[0];
    mapping[wordName] = `/Images/${file}`;
  }
});

fs.writeFileSync(mappingPath, JSON.stringify(mapping, null, 2));
console.log('image_mapping.json initialized with existing images.');
