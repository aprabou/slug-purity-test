const fs = require('fs');

// Read the HTML template
let html = fs.readFileSync('index.html', 'utf8');

// Replace placeholders with environment variables
html = html.replace('YOUR_SUPABASE_URL_HERE', process.env.SUPABASE_URL || '');
html = html.replace('YOUR_SUPABASE_ANON_KEY_HERE', process.env.SUPABASE_ANON_KEY || '');

// Create dist directory if it doesn't exist
if (!fs.existsSync('dist')) {
    fs.mkdirSync('dist');
}

// Write the processed HTML to dist folder
fs.writeFileSync('dist/index.html', html);

console.log('Build complete! Environment variables injected.');