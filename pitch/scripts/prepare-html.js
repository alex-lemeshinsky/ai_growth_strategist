#!/usr/bin/env node
/**
 * Script to prepare HTML files with environment variables
 * Replaces ${API_BASE_URL} placeholders with actual values
 */

const fs = require('fs');
const path = require('path');
require('dotenv').config({ path: '.env.local' });

// Get API base URL from environment
const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

console.log('🔧 Preparing HTML files with environment variables...');
console.log(`📡 API Base URL: ${apiBaseUrl}`);

// Files to process
const filesToProcess = [
  'public/chat-mvp-demo.html'
];

filesToProcess.forEach(filePath => {
  const fullPath = path.join(__dirname, '..', filePath);
  
  if (!fs.existsSync(fullPath)) {
    console.log(`⚠️  File not found: ${filePath}`);
    return;
  }
  
  try {
    // Read file content
    let content = fs.readFileSync(fullPath, 'utf8');
    
    // Replace placeholders
    content = content.replace(/\$\{API_BASE_URL\}/g, apiBaseUrl);
    content = content.replace(/NEXT_PUBLIC_API_BASE_URL: '\$\{API_BASE_URL\}'/g, `NEXT_PUBLIC_API_BASE_URL: '${apiBaseUrl}'`);
    
    // Write back to file
    fs.writeFileSync(fullPath, content, 'utf8');
    
    console.log(`✅ Updated: ${filePath}`);
  } catch (error) {
    console.error(`❌ Error processing ${filePath}:`, error.message);
  }
});

console.log('🎉 HTML preparation completed!');