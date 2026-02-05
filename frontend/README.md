# Frontend - Todo App

Next.js 16+ frontend for the Todo Full-Stack Web Application.

## Features

- Modern React with TypeScript
- Tailwind CSS for styling
- Better Auth for authentication
- Responsive design
- JWT token management
- User-friendly interface

## Requirements

- Node.js 18+
- npm or yarn package manager

## Installation

1. Install dependencies:
   ```bash
   npm install
   ```

2. Set up environment variables:
   ```bash
   cp .env.local.example .env.local
   # Edit .env.local with your configuration
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

## Environment Variables

Create a `.env.local` file with the following variables:

```env
NEXT_PUBLIC_API_URL="http://localhost:8000"
NEXT_PUBLIC_ENVIRONMENT="development"
BETTER_AUTH_SECRET="your-super-secret-jwt-key-change-this-in-production"
NEXT_PUBLIC_ENABLE_DEBUG="true"
```

## Available Scripts

In the project directory, you can run:

### `npm run dev`
Runs the app in development mode. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.

### `npm run build`
Builds the app for production to the `build` folder.

### `npm run start`
Runs the built app in production mode.

### `npm run lint`
Runs ESLint to check for code quality issues.

## Project Structure

```
frontend/
├── src/
│   ├── app/             # Next.js App Router pages
│   ├── components/      # React components
│   ├── lib/            # Utility functions and types
│   ├── services/        # API and authentication services
│   └── styles/         # Global styles and CSS
├── public/             # Static assets
├── tests/              # Test suite
├── package.json        # Project configuration
└── .env.local.example  # Environment variables template
```

## Development

### API Integration

The frontend communicates with the FastAPI backend at the URL specified in `NEXT_PUBLIC_API_URL`.

### Authentication

Authentication is handled by Better Auth with JWT tokens. The frontend automatically includes tokens in API requests.

## Testing

```bash
npm run test
```

## Deployment

This application can be deployed to Vercel, Netlify, or any other static hosting service that supports Next.js.

## License

This project is part of the Hackathon II Phase II Todo Full-Stack Web Application.
