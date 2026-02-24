'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/hooks/useAuth';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { TaskList } from '@/components/tasks/TaskList';
import { TaskForm } from '@/components/tasks/TaskForm';
import { tasksService } from '@/services/tasks';
import { Task } from '@/types/tasks';
import { cn } from '@/lib/utils';

export default function DashboardPage() {
  const { user } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Load tasks for the authenticated user
  useEffect(() => {
    const fetchTasks = async () => {
      if (!user?.id) return; // Wait for user to be loaded

      try {
        setLoading(true);
        setError(null);
        const tasksData = await tasksService.getAll(user.id);
        setTasks(tasksData);
      } catch (err: any) {
        console.error('Error fetching tasks:', err);
        setError(err.message || 'Failed to load tasks');
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, [user]);

  const handleTaskCreate = async (title: string, description?: string) => {
    if (!user?.id) return;

    try {
      const newTask = await tasksService.create(user.id, { title, description });
      setTasks(prev => [...prev, newTask]);
    } catch (err: any) {
      console.error('Error creating task:', err);
      setError(err.message || 'Failed to create task');
    }
  };

  const handleTaskUpdate = async (taskId: string, updatedData: { title?: string; description?: string; completed?: boolean }) => {
    if (!user?.id) return;

    try {
      const updatedTask = await tasksService.update(user.id, taskId, updatedData);
      setTasks(prev => prev.map(task => task.id === taskId ? updatedTask : task));
    } catch (err: any) {
      console.error('Error updating task:', err);
      setError(err.message || 'Failed to update task');
    }
  };

  const handleTaskDelete = async (taskId: string) => {
    if (!user?.id) return;

    try {
      await tasksService.delete(user.id, taskId);
      setTasks(prev => prev.filter(task => task.id !== taskId));
    } catch (err: any) {
      console.error('Error deleting task:', err);
      setError(err.message || 'Failed to delete task');
    }
  };

  const handleTaskToggle = async (taskId: string) => {
    if (!user?.id) return;

    try {
      const updatedTask = await tasksService.toggleCompletion(user.id, taskId);
      setTasks(prev => prev.map(task =>
        task.id === taskId ? updatedTask : task
      ));
    } catch (err: any) {
      console.error('Error toggling task completion:', err);
      setError(err.message || 'Failed to update task status');
    }
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-10">
            <h1 className="text-3xl font-bold text-gray-900 sm:text-4xl">
              Welcome, {user?.name || user?.email}!
            </h1>
            <p className="mt-3 text-lg text-gray-500">
              Manage your tasks efficiently
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2">
              <div className="bg-white shadow rounded-lg">
                <div className="px-4 py-5 sm:p-6">
                  <h2 className="text-xl font-semibold text-gray-800 mb-4">Your Tasks</h2>

                  {error && (
                    <div className="bg-red-50 text-red-700 p-3 rounded-md text-sm mb-4">
                      {error}
                    </div>
                  )}

                  {loading ? (
                    <div className="flex justify-center items-center py-10">
                      <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600"></div>
                    </div>
                  ) : (
                    <TaskList
                      tasks={tasks}
                      onTaskUpdate={handleTaskUpdate}
                      onTaskDelete={handleTaskDelete}
                      onTaskToggle={handleTaskToggle}
                    />
                  )}
                </div>
              </div>
            </div>

            <div>
              <div className="bg-white shadow rounded-lg">
                <div className="px-4 py-5 sm:p-6">
                  <h2 className="text-xl font-semibold text-gray-800 mb-4">Add New Task</h2>
                  <TaskForm onSubmit={handleTaskCreate} />
                </div>
              </div>

              <div className="mt-6 bg-white shadow rounded-lg">
                <div className="px-4 py-5 sm:p-6">
                  <h3 className="text-lg font-medium text-gray-800">Statistics</h3>
                  <div className="mt-4 space-y-3">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Total Tasks:</span>
                      <span className="font-medium">{tasks.length}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Completed:</span>
                      <span className="font-medium">
                        {tasks.filter(t => t.completed).length}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Pending:</span>
                      <span className="font-medium">
                        {tasks.filter(t => !t.completed).length}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}