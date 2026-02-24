# Todo App Frontend

A modern Next.js frontend application for the Todo App with authentication and task management features.

## Features

- User authentication with Better Auth (signup/signin)
- Task management (create, read, update, delete, toggle completion)
- Responsive design with Tailwind CSS
- JWT token handling for secure API communication
- Clean, component-based architecture

## Tech Stack

- Next.js 16+ with App Router
- React 19
- TypeScript
- Tailwind CSS
- Better Auth for authentication
- clsx and tailwind-merge for utility classes

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. Clone the repository
2. Navigate to the frontend directory: `cd frontend`
3. Install dependencies: `npm install`

### Environment Variables

Create a `.env.local` file in the frontend directory with the following:

```env
# API Configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

# Better Auth Configuration
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-key-here
```

### Running the Application

```bash
# Development mode
npm run dev

# Build for production
npm run build

# Run in production
npm start
```

The application will be available at http://localhost:3000 (or the next available port).

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── (auth)/            # Authentication pages
│   │   ├── signup/        # Signup page
│   │   └── signin/        # Signin page
│   ├── dashboard/         # Dashboard page
│   └── page.tsx           # Home page
├── components/            # Reusable React components
│   ├── auth/              # Authentication components
│   ├── layout/            # Layout components
│   └── tasks/             # Task management components
├── hooks/                 # Custom React hooks
├── lib/                   # Utility functions and constants
├── services/              # API and authentication services
│   ├── api.ts             # API client with JWT handling
│   ├── auth.ts            # Authentication service
│   └── tasks.ts           # Task management service
├── types/                 # TypeScript type definitions
│   ├── auth.ts            # Authentication types
│   └── tasks.ts           # Task types
├── public/                # Static assets
└── package.json           # Dependencies and scripts
```

## Services

### API Service
Handles all communication with the backend API, including JWT token management.

### Auth Service
Manages user authentication with Better Auth, including signup, signin, and session management.

### Tasks Service
Handles all task-related operations with the backend API.

## Components

### Authentication Components
- LoginForm: Handles user login
- SignupForm: Handles user registration

### Task Components
- TaskList: Displays a list of tasks
- TaskItem: Displays an individual task with actions
- TaskForm: Form for creating new tasks

### Layout Components
- Header: Navigation and user info
- Sidebar: Main navigation menu

## Hooks

- useAuth: Provides authentication state and methods throughout the app

## Types

TypeScript definitions for:
- User authentication data
- Task data structures
- API response formats

## Environment Variables

- `NEXT_PUBLIC_API_BASE_URL`: Base URL for the backend API
- `NEXT_PUBLIC_BETTER_AUTH_URL`: URL for Better Auth service
- `BETTER_AUTH_SECRET`: Secret key for Better Auth (should be kept secure)

## API Integration

The application communicates with the backend API using the service layer which properly handles:
- JWT token inclusion in requests
- Error handling
- Loading states
- Authentication state management

## Responsive Design

The application is fully responsive and works on mobile, tablet, and desktop devices using Tailwind CSS utility classes.
