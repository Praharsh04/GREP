const { execSync } = require('child_process');

function sync() {
  try {
    console.log('--- Starting Sync to GitHub ---');

    // 1. Stage changes (Images and the mapping file)
    console.log('Staging changes...');
    execSync('git add Images/ image_mapping.json index.html');

    // 2. Check if there are actually changes to commit
    const status = execSync('git status --porcelain').toString();
    if (!status) {
      console.log('No new images or changes detected. Nothing to sync.');
      return;
    }

    // 3. Commit
    const timestamp = new Date().toLocaleString();
    console.log('Committing changes...');
    execSync(`git commit -m "Sync: Added/Updated images on ${timestamp}"`);

    // 4. Push
    console.log('Pushing to GitHub (Live Site)...');
    execSync('git push origin main');

    console.log('--- SUCCESS! Your images are now safe on GitHub and going live ---');
  } catch (error) {
    console.error('--- ERROR DURING SYNC ---');
    console.error(error.message);
    console.log('Make sure you have Git installed and are logged in.');
  }
}

sync();
