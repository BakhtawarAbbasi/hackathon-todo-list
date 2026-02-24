// Get API base URL from environment variable
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

// Define types for API responses
export interface ApiError {
  message: string;
  status: number;
  details?: any;
}

// Base API client with JWT token handling
class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  // Helper method to get headers with JWT token
  private getAuthHeaders(): Record<string, string> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    // Get the JWT token from localStorage (where we store the backend token)
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('better-auth-session-token');
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
    }

    return headers;
  }

  // Generic GET request
  async get<T>(endpoint: string): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const headers = this.getAuthHeaders();

    const response = await fetch(url, {
      method: 'GET',
      headers,
      credentials: 'include', // Include cookies for session-based auth
    });

    return this.handleResponse<T>(response);
  }

  // Generic POST request
  async post<T>(endpoint: string, data?: any): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const headers = this.getAuthHeaders();

    const response = await fetch(url, {
      method: 'POST',
      headers,
      body: JSON.stringify(data),
      credentials: 'include', // Include cookies for session-based auth
    });

    return this.handleResponse<T>(response);
  }

  // Generic PUT request
  async put<T>(endpoint: string, data?: any): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const headers = this.getAuthHeaders();

    const response = await fetch(url, {
      method: 'PUT',
      headers,
      body: JSON.stringify(data),
      credentials: 'include', // Include cookies for session-based auth
    });

    return this.handleResponse<T>(response);
  }

  // Generic DELETE request
  async delete<T>(endpoint: string): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const headers = this.getAuthHeaders();

    const response = await fetch(url, {
      method: 'DELETE',
      headers,
      credentials: 'include', // Include cookies for session-based auth
    });

    return this.handleResponse<T>(response);
  }

  // Generic PATCH request
  async patch<T>(endpoint: string, data?: any): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const headers = this.getAuthHeaders();

    const response = await fetch(url, {
      method: 'PATCH',
      headers,
      body: JSON.stringify(data),
      credentials: 'include', // Include cookies for session-based auth
    });

    return this.handleResponse<T>(response);
  }

  // Handle response and throw errors if needed
  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      const apiError: ApiError = {
        message: errorData.message || response.statusText,
        status: response.status,
        details: errorData,
      };

      throw apiError;
    }

    // Handle empty responses
    if (response.status === 204) {
      return {} as T;
    }

    return response.json();
  }
}

// Create a singleton instance of the API client
export const apiClient = new ApiClient();

// Export individual methods for convenience
export const { get, post, put, patch, delete: apiDelete } = apiClient;