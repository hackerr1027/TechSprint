# Integration Guide: Visual Diagram Frontend

## Overview

This document explains how to run the **iaac-helper-main** React frontend with visual Mermaid diagram rendering, integrated with your existing backend.

## What Changed

The iaac-helper-main frontend has been configured to work with your existing backend **without any changes to the backend**. Here's what was updated:

### ✅ Frontend Changes Made

1. **API Service Updated** (`src/services/api.ts`)
   - Maps backend response format to frontend expectations
   - `mermaid_diagram` → `diagram`
   - `terraform_code` → `terraform`
   - `security_warnings` → `warnings`

2. **Environment Configured** (`.env`)
   - Set `VITE_API_URL=http://localhost:8000`

3. **TypeScript Types Fixed** (`src/vite-env.d.ts`)
   - Added environment variable type definitions

### ✅ Backend - No Changes Required

Your backend at `c:\Users\Ridham Shah\OneDrive\Desktop\DAIICT-25dec\backend` remains **completely unchanged** and will continue to work with both:
- The simple HTML frontend at `frontend/index.html`
- The new React frontend at `frontend/iaac-helper-main`

## Prerequisites

You need to install Node.js and npm to run the React frontend.

### Install Node.js

1. **Download Node.js**: Visit [https://nodejs.org/](https://nodejs.org/)
2. **Choose Version**: Download the LTS (Long Term Support) version
3. **Install**: Run the installer and follow the prompts
4. **Verify Installation**:
   ```bash
   node --version
   npm --version
   ```

## Setup Instructions

Once Node.js is installed, follow these steps:

### 1. Install Dependencies

```bash
cd "c:\Users\Ridham Shah\OneDrive\Desktop\DAIICT-25dec\frontend\iaac-helper-main"
npm install
```

This will install all required packages including:
- React and React DOM
- Mermaid (for visual diagrams)
- Monaco Editor (for Terraform code editing)
- shadcn/ui components
- Tailwind CSS

### 2. Start the Backend Server

In one terminal:

```bash
cd "c:\Users\Ridham Shah\OneDrive\Desktop\DAIICT-25dec"
python -m uvicorn backend.main:app --reload
```

The backend will start at `http://localhost:8000`

### 3. Start the Frontend Development Server

In another terminal:

```bash
cd "c:\Users\Ridham Shah\OneDrive\Desktop\DAIICT-25dec\frontend\iaac-helper-main"
npm run dev
```

The frontend will start (usually at `http://localhost:5173`)

### 4. Open in Browser

Open your browser to the URL shown in the terminal (typically `http://localhost:5173`)

## Features

### Visual Diagram Rendering

Unlike the simple frontend that shows Mermaid code as text, this frontend **renders diagrams visually**:

- **Interactive diagrams** with proper visualization
- **Real-time rendering** using Mermaid.js
- **Professional appearance** with dark theme matching the UI

### Modern UI Components

- **Monaco Editor**: Same editor as VS Code for Terraform editing
- **Health Indicators**: Shows backend connection status
- **Sync Status**: Visual feedback when changes are being applied
- **Toast Notifications**: User-friendly success/error messages
- **Responsive Layout**: Three-panel design (Input | Diagram | Code)

### Enhanced Features

- **Loading States**: Visual feedback during generation
- **Security Panel**: Collapsible warnings section
- **Export Functionality**: Download Terraform as `.tf` file
- **Keyboard Shortcuts**: Ctrl/Cmd + Enter to generate

## Usage

1. **Describe Infrastructure**: Enter your requirements in the left panel
2. **Generate**: Click "Generate Infrastructure" button
3. **View Results**: 
   - Center: Visual Mermaid diagram (not text!)
   - Right: Terraform code with syntax highlighting
   - Bottom: Security warnings and recommendations
4. **Edit**: Use the controls to add resources or edit Terraform code
5. **Export**: Download Terraform code when ready

## Comparison with Simple Frontend

| Feature | Simple Frontend (`frontend/index.html`) | React Frontend (`iaac-helper-main`) |
|---------|----------------------------------------|-------------------------------------|
| Diagram Display | Text-based Mermaid code | **Visual rendered diagram** |
| Code Editor | Plain textarea | Monaco Editor (VS Code) |
| UI Framework | Vanilla HTML/CSS/JS | React + TypeScript |
| Status Indicators | None | Health & Sync indicators |
| Notifications | Browser alerts | Toast notifications |
| Responsiveness | Basic | Advanced responsive design |

## Troubleshooting

### Backend Connection Issues

**Symptom**: "Demo Mode" shown in notifications

**Solution**: 
- Ensure backend is running at `http://localhost:8000`
- Check `http://localhost:8000/health` in your browser
- Verify CORS is enabled in backend (it is by default)

### Diagram Not Rendering

**Symptom**: Empty diagram area or text instead of visual diagram

**Solution**:
- Check browser console for errors
- Ensure Mermaid.js loaded properly (requires internet for CDN)
- Verify backend is returning `mermaid_diagram` field

### Port Already in Use

**Symptom**: "Port 5173 already in use"

**Solution**:
```bash
# Vite will automatically try the next available port
# Or specify a different port:
npm run dev -- --port 3000
```

## Building for Production

To create a production build:

```bash
cd "c:\Users\Ridham Shah\OneDrive\Desktop\DAIICT-25dec\frontend\iaac-helper-main"
npm run build
```

The built files will be in the `dist` folder. You can serve them with any static file server.

## Next Steps

After getting the frontend running:

1. **Test all features**: Generate, edit, export
2. **Verify visual diagrams**: Ensure diagrams render visually, not as text
3. **Check security warnings**: Verify they appear in the bottom panel
4. **Test edit operations**: Add resources and see live updates
5. **Compare with simple frontend**: See the improvement!

## Support

If you encounter issues:
1. Check the browser console for errors (F12)
2. Verify backend is running and healthy
3. Ensure Node.js and npm are properly installed
4. Check that all dependencies installed successfully

---

**Remember**: The backend was NOT modified. Both frontends (simple and React) work with the same backend API!
