const fs = require('fs');

// Create the config file with environment variables
const configContent = `// Supabase configuration
window.SUPABASE_CONFIG = {
    url: '${process.env.SUPABASE_URL || ''}',
    anonKey: '${process.env.SUPABASE_ANON_KEY || ''}'
};`;

// Write the config file
fs.writeFileSync('config.js', configContent);

console.log('Build complete! Environment variables injected.');
console.log('Config file generated with environment variables');