// frontend/lib/constants.ts

// API Endpoints
export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/api/auth/sign-in',
    REGISTER: '/api/auth/sign-up',
    LOGOUT: '/api/auth/logout',
    ME: '/api/auth/me',
  },
  TASKS: {
    BASE: (userId: string) => `/api/${userId}/tasks` as const,
    CREATE: (userId: string) => `/api/${userId}/tasks` as const,
    GET_ALL: (userId: string) => `/api/${userId}/tasks` as const,
    GET_BY_ID: (userId: string, taskId: string) => `/api/${userId}/tasks/${taskId}` as const,
    UPDATE: (userId: string, taskId: string) => `/api/${userId}/tasks/${taskId}` as const,
    DELETE: (userId: string, taskId: string) => `/api/${userId}/tasks/${taskId}` as const,
    TOGGLE_COMPLETION: (userId: string, taskId: string) => `/api/${userId}/tasks/${taskId}/complete` as const,
  },
} as const;

// Storage keys for localStorage/sessionStorage
export const STORAGE_KEYS = {
  AUTH_TOKEN: 'better-auth-session-token',
  USER_PREFERENCES: 'user-preferences',
  THEME: 'theme',
  LANGUAGE: 'language',
} as const;

// Configuration constants
export const CONFIG = {
  API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
  AUTH_COOKIE_NAME: 'better-auth-session',
  DEFAULT_PAGE_SIZE: 10,
  MAX_PAGE_SIZE: 100,
  DEBOUNCE_DELAY: 300, // milliseconds
  REFRESH_INTERVAL: 30000, // 30 seconds in milliseconds
} as const;

// Validation constants
export const VALIDATION = {
  EMAIL_MIN_LENGTH: 3,
  EMAIL_MAX_LENGTH: 254,
  PASSWORD_MIN_LENGTH: 8,
  PASSWORD_MAX_LENGTH: 128,
  TASK_TITLE_MIN_LENGTH: 1,
  TASK_TITLE_MAX_LENGTH: 255,
  TASK_DESCRIPTION_MAX_LENGTH: 1000,
} as const;

// UI Constants
export const UI = {
  TOAST_DURATION: 5000, // 5 seconds
  MODAL_ANIMATION_DURATION: 300, // milliseconds
  LOADING_DELAY: 500, // milliseconds before showing loading spinner
  SIDEBAR_WIDTH: '240px',
  HEADER_HEIGHT: '64px',
} as const;

// Error messages
export const ERROR_MESSAGES = {
  UNAUTHORIZED: 'Unauthorized. Please sign in to continue.',
  NETWORK_ERROR: 'Network error. Please check your connection and try again.',
  SERVER_ERROR: 'Server error. Please try again later.',
  VALIDATION_ERROR: 'Please check your input and try again.',
  TASK_NOT_FOUND: 'Task not found.',
  GENERIC_ERROR: 'An unexpected error occurred.',
} as const;

// Success messages
export const SUCCESS_MESSAGES = {
  TASK_CREATED: 'Task created successfully!',
  TASK_UPDATED: 'Task updated successfully!',
  TASK_DELETED: 'Task deleted successfully!',
  LOGIN_SUCCESS: 'Login successful!',
  REGISTRATION_SUCCESS: 'Registration successful!',
} as const;

// Route constants
export const ROUTES = {
  HOME: '/',
  DASHBOARD: '/dashboard',
  LOGIN: '/login',
  REGISTER: '/register',
  PROFILE: '/profile',
  TASKS: '/tasks',
  SETTINGS: '/settings',
} as const;

// Theme constants
export const THEMES = {
  LIGHT: 'light',
  DARK: 'dark',
  SYSTEM: 'system',
} as const;