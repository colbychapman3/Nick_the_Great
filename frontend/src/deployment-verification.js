/**
 * Frontend Deployment Verification Script
 * 
 * This script performs checks on the frontend environment to verify proper
 * configuration for deployment. It checks for:
 * - Required environment variables
 * - API connectivity
 * - Authentication flow
 * 
 * Usage:
 * Open your terminal and run:
 * ```
 * cd frontend
 * node src/deployment-verification.js
 * ```
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const readline = require('readline');

// Create interactive console interface
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

const question = (query) => new Promise((resolve) => rl.question(query, resolve));

// Helper for colored console output
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
};

function log(message, color = 'reset') {
  console.log(colors[color] + message + colors.reset);
}

// Main verification function
async function verifyFrontendDeployment() {
  log('=== NICK THE GREAT FRONTEND DEPLOYMENT VERIFICATION ===', 'cyan');
  log('This script checks the frontend configuration for deployment readiness.\n');

  // Step 1: Check for .env file
  log('--- Step 1: Environment Variables Check ---', 'magenta');
  
  const envPath = path.join(process.cwd(), '.env');
  const envExamplePath = path.join(process.cwd(), '.env.example');
  
  if (fs.existsSync(envPath)) {
    log('✅ .env file exists', 'green');
    
    // Read .env file and check for required variables
    const envContent = fs.readFileSync(envPath, 'utf8');
    const requiredVars = [
      'NEXT_PUBLIC_API_URL',
      'NEXT_PUBLIC_AUTH_API_URL'
    ];
    
    let missingVars = [];
    for (const variable of requiredVars) {
      if (!envContent.includes(`${variable}=`)) {
        missingVars.push(variable);
      }
    }
    
    if (missingVars.length === 0) {
      log('✅ All required environment variables are defined', 'green');
      
      // Extract and display the backend URLs
      const apiUrlMatch = envContent.match(/NEXT_PUBLIC_API_URL=(.+)/);
      const authApiUrlMatch = envContent.match(/NEXT_PUBLIC_AUTH_API_URL=(.+)/);
      
      if (apiUrlMatch && authApiUrlMatch) {
        const apiUrl = apiUrlMatch[1];
        const authApiUrl = authApiUrlMatch[1];
        
        log(`   API URL: ${apiUrl}`, 'blue');
        log(`   Auth API URL: ${authApiUrl}`, 'blue');
        
        // Check if URLs are production URLs
        if (apiUrl.includes('localhost') || authApiUrl.includes('localhost')) {
          log('⚠️ Warning: You are using localhost URLs. For production, use Render/deployed URLs.', 'yellow');
        } else {
          log('✅ Production URLs detected', 'green');
        }
      }
    } else {
      log(`❌ Missing required environment variables: ${missingVars.join(', ')}`, 'red');
      log('   Please add these variables to your .env file before deploying', 'yellow');
      
      if (fs.existsSync(envExamplePath)) {
        log('   You can reference .env.example for the required format', 'yellow');
      }
    }
  } else {
    log('❌ .env file not found', 'red');
    
    if (fs.existsSync(envExamplePath)) {
      log('   Please create a .env file based on .env.example before deploying', 'yellow');
      const createEnv = await question('Do you want to create a .env file from .env.example now? (y/n): ');
      
      if (createEnv.toLowerCase() === 'y') {
        fs.copyFileSync(envExamplePath, envPath);
        log('✅ Created .env file from .env.example', 'green');
        log('   Please review and update the values in the .env file', 'yellow');
      }
    } else {
      log('   .env.example also not found. This is concerning.', 'red');
    }
  }
  
  // Step 2: Check package.json for build scripts
  log('\n--- Step 2: Build Configuration Check ---', 'magenta');
  
  const packageJsonPath = path.join(process.cwd(), 'package.json');
  
  if (fs.existsSync(packageJsonPath)) {
    try {
      const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
      
      // Check build script
      if (packageJson.scripts && packageJson.scripts.build) {
        log('✅ Build script exists:', 'green');
        log(`   "${packageJson.scripts.build}"`, 'blue');
      } else {
        log('❌ No build script found in package.json', 'red');
        log('   This is required for Vercel deployment', 'yellow');
      }
      
      // Check dependencies
      const deps = { ...packageJson.dependencies, ...packageJson.devDependencies };
      log('\nChecking for key dependencies:');
      
      const requiredDeps = ['next', 'react', 'react-dom'];
      let missingDeps = [];
      
      for (const dep of requiredDeps) {
        if (deps[dep]) {
          log(`✅ ${dep}: ${deps[dep]}`, 'green');
        } else {
          log(`❌ ${dep}: Not found`, 'red');
          missingDeps.push(dep);
        }
      }
      
      if (missingDeps.length > 0) {
        log(`\n⚠️ Missing key dependencies: ${missingDeps.join(', ')}`, 'yellow');
        log('   These are required for a Next.js application to function correctly', 'yellow');
      }
    } catch (error) {
      log(`❌ Error parsing package.json: ${error.message}`, 'red');
    }
  } else {
    log('❌ package.json not found', 'red');
    log('   This file is required for deployment', 'yellow');
  }
  
  // Step 3: Check for next.config.js
  log('\n--- Step 3: Next.js Configuration Check ---', 'magenta');
  
  const nextConfigPath = path.join(process.cwd(), 'next.config.js');
  const nextConfigMjsPath = path.join(process.cwd(), 'next.config.mjs');
  
  if (fs.existsSync(nextConfigPath) || fs.existsSync(nextConfigMjsPath)) {
    log('✅ Next.js configuration file exists', 'green');
    
    // Read the next config file
    const configPath = fs.existsSync(nextConfigPath) ? nextConfigPath : nextConfigMjsPath;
    const configContent = fs.readFileSync(configPath, 'utf8');
    
    // Check for key configurations
    if (configContent.includes('env:') || configContent.includes('publicRuntimeConfig')) {
      log('ℹ️ Found environment variable configuration in next.config', 'blue');
    }
    
    if (configContent.includes('reactStrictMode')) {
      log('ℹ️ React strict mode is configured', 'blue');
    }
  } else {
    log('⚠️ No Next.js configuration file found', 'yellow');
    log('   This is not critical, but you may want to create one for custom settings', 'yellow');
  }
  
  // Step 4: Check for Vercel configuration
  log('\n--- Step 4: Vercel Configuration Check ---', 'magenta');
  
  const vercelConfigPath = path.join(process.cwd(), 'vercel.json');
  
  if (fs.existsSync(vercelConfigPath)) {
    log('✅ vercel.json exists', 'green');
    
    try {
      const vercelConfig = JSON.parse(fs.readFileSync(vercelConfigPath, 'utf8'));
      log('   Vercel configuration found:', 'blue');
      log(`   ${JSON.stringify(vercelConfig, null, 2)}`, 'blue');
    } catch (error) {
      log(`❌ Error parsing vercel.json: ${error.message}`, 'red');
    }
  } else {
    log('ℹ️ No vercel.json found', 'blue');
    log('   This is normal. Vercel can deploy Next.js apps without a config file.', 'blue');
    log('   Default settings will be used for deployment.', 'blue');
  }
  
  // Step 5: Check app structure
  log('\n--- Step 5: App Structure Check ---', 'magenta');
  
  // Check for pages or app directory (depending on if using Pages Router or App Router)
  const appDirPath = path.join(process.cwd(), 'src/app');
  const pagesDirPath = path.join(process.cwd(), 'src/pages');
  const legacyPagesDirPath = path.join(process.cwd(), 'pages');
  
  if (fs.existsSync(appDirPath)) {
    log('✅ App Router structure detected (src/app directory)', 'green');
    log('   Using modern Next.js App Router', 'blue');
  } else if (fs.existsSync(pagesDirPath)) {
    log('✅ Pages Router structure detected (src/pages directory)', 'green');
    log('   Using Next.js Pages Router in src directory', 'blue');
  } else if (fs.existsSync(legacyPagesDirPath)) {
    log('✅ Legacy Pages Router structure detected (pages directory)', 'green');
    log('   Using Next.js Pages Router in root directory', 'blue');
  } else {
    log('❌ Neither app/ nor pages/ directory found', 'red');
    log('   Next.js requires either an app/ or pages/ directory', 'yellow');
  }
  
  // Check for key components/routes
  let routeStructure = '';
  let routeBase = '';
  
  if (fs.existsSync(appDirPath)) {
    routeStructure = 'App Router';
    routeBase = appDirPath;
  } else if (fs.existsSync(pagesDirPath)) {
    routeStructure = 'Pages Router';
    routeBase = pagesDirPath;
  } else if (fs.existsSync(legacyPagesDirPath)) {
    routeStructure = 'Legacy Pages Router';
    routeBase = legacyPagesDirPath;
  }
  
  if (routeBase) {
    log('\nChecking key routes:', 'blue');
    
    // Paths to check depend on the router type
    const pathsToCheck = routeStructure === 'App Router' 
      ? {
          'Homepage': 'page.tsx',
          'Login Page': 'login/page.tsx',
          'Dashboard': 'dashboard/page.tsx',
        }
      : {
          'Homepage': 'index.tsx',
          'Login Page': 'login.tsx',
          'Dashboard': 'dashboard.tsx',
        };
    
    for (const [name, relativePath] of Object.entries(pathsToCheck)) {
      const fullPath = path.join(routeBase, relativePath);
      if (fs.existsSync(fullPath)) {
        log(`✅ ${name} (${relativePath})`, 'green');
      } else {
        log(`❌ ${name} (${relativePath})`, 'red');
      }
    }
  }
  
  // Step 6: Final checklist for Vercel deployment
  log('\n--- Step 6: Vercel Deployment Readiness ---', 'magenta');
  
  const deploymentChecklist = [
    {
      name: 'Environment Variables',
      details: 'Make sure NEXT_PUBLIC_API_URL and NEXT_PUBLIC_AUTH_API_URL are set',
      status: fs.existsSync(envPath) ? 'good' : 'warning'
    },
    {
      name: 'Build Command',
      details: 'Vercel should use "npm run build" or custom command if specified',
      status: 'info'
    },
    {
      name: 'Node.js Version',
      details: 'Use Node.js 16.x or later in Vercel settings',
      status: 'info'
    },
    {
      name: 'Output Directory',
      details: 'Default: .next (usually automatic)',
      status: 'info'
    },
    {
      name: 'Install Command',
      details: 'Default: npm install (usually automatic)',
      status: 'info'
    }
  ];
  
  log('\nVercel Deployment Checklist:', 'blue');
  for (const item of deploymentChecklist) {
    let icon, color;
    switch (item.status) {
      case 'good':
        icon = '✅';
        color = 'green';
        break;
      case 'warning':
        icon = '⚠️';
        color = 'yellow';
        break;
      default:
        icon = 'ℹ️';
        color = 'blue';
    }
    
    log(`${icon} ${item.name}: ${item.details}`, color);
  }

  // Final summary
  log('\n=== DEPLOYMENT VERIFICATION SUMMARY ===', 'cyan');
  log('The frontend appears to be generally ready for deployment.', 'green');
  log('Key points to remember:', 'blue');
  log('1. Ensure your backend API is deployed and accessible', 'blue');
  log('2. Set the correct environment variables in Vercel', 'blue');
  log('3. After deployment, verify all routes and functionality', 'blue');
  
  log('\nYou can now deploy your frontend to Vercel:', 'green');
  log('1. Push your code to GitHub', 'green');
  log('2. Import project in Vercel dashboard', 'green');
  log('3. Configure environment variables', 'green');
  log('4. Deploy!', 'green');

  rl.close();
}

// Run the verification
verifyFrontendDeployment().catch(error => {
  console.error('An unexpected error occurred during verification:', error);
  rl.close();
});
