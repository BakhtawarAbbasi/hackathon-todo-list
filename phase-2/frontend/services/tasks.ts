// frontend/services/tasks.ts
import { apiClient } from './api';
import type {
  Task as TaskType,
  CreateTaskRequest,
  UpdateTaskRequest,
  TaskResponse as RawTaskResponse,
  TasksResponse as RawTasksResponse
} from '@/types/tasks';

// Define raw response types that match the backend API
interface RawTask {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

interface RawTaskResponse {
  task: RawTask;
}

interface RawTasksResponse {
  tasks: RawTask[];
}

// Helper function to convert from backend format to frontend type
const mapRawTaskToFrontend = (rawTask: RawTask): TaskType => {
  return {
    id: rawTask.id,
    title: rawTask.title,
    description: rawTask.description,
    completed: rawTask.completed,
    user_id: rawTask.user_id,
    created_at: rawTask.created_at,
    updated_at: rawTask.updated_at,
  };
};

class TasksService {
  // Get all tasks for the authenticated user
  async getAll(userId: string): Promise<TaskType[]> {
    try {
      const response = await apiClient.get<RawTasksResponse>(`/api/${userId}/tasks`);
      return response.tasks.map(mapRawTaskToFrontend);
    } catch (error) {
      console.error('Error fetching tasks:', error);
      throw error;
    }
  }

  // Get a specific task by ID
  async getById(userId: string, id: string): Promise<TaskType> {
    try {
      const response = await apiClient.get<RawTaskResponse>(`/api/${userId}/tasks/${id}`);
      return mapRawTaskToFrontend(response.task);
    } catch (error) {
      console.error(`Error fetching task with ID ${id}:`, error);
      throw error;
    }
  }

  // Create a new task
  async create(userId: string, taskData: CreateTaskRequest): Promise<TaskType> {
    try {
      const response = await apiClient.post<RawTaskResponse>(`/api/${userId}/tasks`, taskData);
      return mapRawTaskToFrontend(response.task);
    } catch (error) {
      console.error('Error creating task:', error);
      throw error;
    }
  }

  // Update an existing task
  async update(userId: string, id: string, taskData: UpdateTaskRequest): Promise<TaskType> {
    try {
      const response = await apiClient.put<RawTaskResponse>(`/api/${userId}/tasks/${id}`, taskData);
      return mapRawTaskToFrontend(response.task);
    } catch (error) {
      console.error(`Error updating task with ID ${id}:`, error);
      throw error;
    }
  }

  // Delete a task
  async delete(userId: string, id: string): Promise<void> {
    try {
      await apiClient.delete(`/api/${userId}/tasks/${id}`);
    } catch (error) {
      console.error(`Error deleting task with ID ${id}:`, error);
      throw error;
    }
  }

  // Toggle task completion status
  async toggleCompletion(userId: string, id: string): Promise<TaskType> {
    try {
      const response = await apiClient.patch<RawTaskResponse>(`/api/${userId}/tasks/${id}/complete`, {});
      return mapRawTaskToFrontend(response.task);
    } catch (error) {
      console.error(`Error toggling completion for task with ID ${id}:`, error);
      throw error;
    }
  }
}

// Export a singleton instance of the TasksService
export const tasksService = new TasksService();

// Export individual methods for convenience
export const { getAll, getById, create, update, delete: deleteTask, toggleCompletion } = tasksService;