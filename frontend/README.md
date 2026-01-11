# Tiling System Frontend

Professional tiling project management and calculation tools - Frontend Application

## Overview

The frontend is a responsive, vanilla JavaScript application that provides an intuitive interface for managing tiling projects and performing calculations.

## Features

- **Dashboard**: Overview of project statistics and quick actions
- **Calculator**: Three-step calculation workflow
  - Area calculation (length × width)
  - Material calculation (tiles, grout, adhesive)
  - Cost estimation with detailed breakdown
- **Projects Management**: Create, view, and delete tiling projects
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## Pages

### Dashboard (`index.html`)
- Project statistics overview (total, active, completed)
- Quick access to calculator and projects
- Real-time data from backend API

### Calculator (`pages/calculator.html`)
- **Step 1**: Calculate area from dimensions
- **Step 2**: Calculate materials needed (auto-fills from step 1)
- **Step 3**: Calculate total project cost (auto-fills from step 2)
- Smart field auto-population for seamless workflow

### Projects (`pages/projects.html`)
- List all projects in a responsive grid
- Create new projects with client information
- Delete projects with confirmation
- Color-coded status badges

## Technology Stack

- **HTML5**: Semantic markup
- **CSS3**: Modern styling with flexbox and grid
- **Vanilla JavaScript**: No frameworks, pure ES6+
- **Fetch API**: RESTful API communication

## Getting Started

### Prerequisites

- Modern web browser (Chrome, Firefox, Safari, Edge)
- Backend API running on `http://localhost:8000`

### Running the Frontend

#### Option 1: Simple HTTP Server (Python)
```bash
cd frontend
python -m http.server 8080
```

Then open http://localhost:8080 in your browser.

#### Option 2: Any Static File Server
```bash
# Using Node.js http-server
npx http-server frontend -p 8080

# Using PHP
cd frontend && php -S localhost:8080
```

## Project Structure

```
frontend/
├── index.html              # Dashboard page
├── pages/
│   ├── calculator.html     # Calculator page
│   └── projects.html       # Projects page
├── css/
│   └── style.css          # Main stylesheet
└── js/
    ├── api.js             # API client
    ├── main.js            # Dashboard logic
    ├── calculator.js      # Calculator logic
    └── projects.js        # Projects logic
```

## API Configuration

The frontend expects the backend API to be running at `http://localhost:8000/api/v1`.

To change this, edit the `API_BASE_URL` constant in `js/api.js`:

```javascript
const API_BASE_URL = 'http://your-backend-url/api/v1';
```

## Features in Detail

### Responsive Design
- Mobile-first approach
- Breakpoint at 768px for tablet/mobile
- Touch-friendly buttons and forms
- Collapsible navigation on mobile

### Form Validation
- HTML5 validation attributes
- Required field checking
- Number input constraints
- Real-time error messages

### User Experience
- Auto-population of calculated values
- Confirmation dialogs for destructive actions
- Loading states and error handling
- Smooth transitions and hover effects

### Color Scheme
- Primary: Purple gradient (`#667eea` to `#764ba2`)
- Navigation: Dark blue (`#2c3e50`)
- Backgrounds: Light gray (`#f5f5f5`)
- Status badges: Semantic colors

### Status Badge Colors
- **Planning**: Blue (`#1976d2`)
- **In Progress**: Orange (`#f57c00`)
- **Completed**: Green (`#388e3c`)
- **Archived**: Gray (`#616161`)

## Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Development

### Adding a New Page

1. Create HTML file in `pages/` or root
2. Include navigation bar markup
3. Link `css/style.css` and relevant JS files
4. Add page-specific JavaScript in `js/`

### Styling Guidelines

- Use existing CSS classes from `style.css`
- Follow BEM naming convention for new classes
- Maintain color scheme consistency
- Test responsive behavior

### JavaScript Guidelines

- Use ES6+ features (arrow functions, async/await)
- Handle errors gracefully with try-catch
- Provide user feedback for all actions
- Keep functions small and focused

## Troubleshooting

### "Failed to load projects" Error
- Ensure backend is running on `http://localhost:8000`
- Check CORS settings in backend
- Verify API_BASE_URL in `js/api.js`

### Styles Not Loading
- Check file paths are correct (relative paths)
- Ensure `style.css` is in `css/` folder
- Clear browser cache

### Calculations Not Working
- Open browser console (F12) for error messages
- Verify all form fields are filled correctly
- Check backend API is responding

## Future Enhancements

- [ ] Authentication and user accounts
- [ ] Project editing functionality
- [ ] Export project data (PDF, CSV)
- [ ] Dark mode support
- [ ] Offline mode with local storage
- [ ] Progressive Web App (PWA)
- [ ] Image upload for projects
- [ ] Advanced pattern calculators

## Contributing

When contributing to the frontend:

1. Test on multiple browsers
2. Ensure responsive design works
3. Follow existing code style
4. Add comments for complex logic
5. Test with and without backend

## License

Part of the Construct-IQ Ecosystem - Tiling System

---

**Version**: 1.0.0  
**Last Updated**: 2026-01-11
