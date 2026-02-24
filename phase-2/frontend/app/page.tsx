'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import { ROUTES } from '@/lib/constants';
import { tasksService, Task } from '@/services/tasks';

export default function Home() {
  const router = useRouter();
  const { loading, isAuthenticated, user, refetchUser } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTask, setNewTask] = useState('');
  const [loadingTasks, setLoadingTasks] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load tasks when user is authenticated
  useEffect(() => {
    if (isAuthenticated && user?.id) {
      loadTasks();
    } else {
      setTasks([]);
    }
  }, [isAuthenticated, user?.id]);

  const loadTasks = async () => {
    if (!user?.id) return;

    try {
      setLoadingTasks(true);
      const userTasks = await tasksService.getAll(user.id);
      setTasks(userTasks);
    } catch (err) {
      console.error('Error loading tasks:', err);
      setError('Failed to load tasks');
    } finally {
      setLoadingTasks(false);
    }
  };

  // Only redirect if user tries to add a task while not authenticated
  const handleAddTask = async () => {
    if (!isAuthenticated) {
      router.push(ROUTES.LOGIN);
      return;
    }

    if (!newTask.trim()) {
      setError('Task title cannot be empty');
      return;
    }

    if (!user?.id) {
      setError('User not found');
      return;
    }

    try {
      setError(null);
      const createdTask = await tasksService.create(user.id, {
        title: newTask.trim(),
        description: '',
        completed: false
      });

      setTasks(prev => [createdTask, ...prev]);
      setNewTask('');
    } catch (err) {
      console.error('Error creating task:', err);
      setError('Failed to create task');
    }
  };

  const handleToggleTask = async (taskId: string) => {
    if (!user?.id) return;

    try {
      const updatedTask = await tasksService.toggleCompletion(user.id, taskId);
      setTasks(prev => prev.map(task =>
        task.id === taskId ? updatedTask : task
      ));
    } catch (err) {
      console.error('Error toggling task:', err);
      setError('Failed to update task');
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    if (!user?.id) return;

    try {
      await tasksService.delete(user.id, taskId);
      setTasks(prev => prev.filter(task => task.id !== taskId));
    } catch (err) {
      console.error('Error deleting task:', err);
      setError('Failed to delete task');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Todo List</h1>
          <p className="text-gray-600 mt-2">
            {isAuthenticated
              ? 'Manage your tasks'
              : 'Sign in to manage your tasks'}
          </p>
        </header>

        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <div className="flex gap-3">
            <input
              type="text"
              value={newTask}
              onChange={(e) => setNewTask(e.target.value)}
              placeholder="Enter a new task..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={!isAuthenticated}
              onKeyDown={(e) => e.key === 'Enter' && handleAddTask()}
            />
            <button
              onClick={handleAddTask}
              className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={!isAuthenticated}
            >
              Add Task
            </button>
          </div>
          {error && (
            <div className="mt-3 text-red-600 text-sm">
              {error}
            </div>
          )}
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Your Tasks</h2>
          {loadingTasks ? (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
            </div>
          ) : tasks.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              {isAuthenticated
                ? 'No tasks yet. Add a new task to get started!'
                : 'Sign in to see your tasks'}
            </div>
          ) : (
            <ul className="space-y-3">
              {tasks.map((task) => (
                <li key={task.id} className="flex items-center justify-between p-3 border-b border-gray-200">
                  <div className="flex items-center">
                    <input
                      type="checkbox"
                      checked={task.completed}
                      onChange={() => handleToggleTask(task.id)}
                      className="mr-3 h-4 w-4 text-blue-600 rounded focus:ring-blue-500"
                    />
                    <span className={task.completed ? 'line-through text-gray-500' : 'text-gray-800'}>
                      {task.title}
                    </span>
                  </div>
                  <button
                    onClick={() => handleDeleteTask(task.id)}
                    className="text-red-600 hover:text-red-800 text-sm"
                  >
                    Delete
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>

        {!isAuthenticated && (
          <div className="mt-6 text-center">
            <p className="text-gray-600">
              Please <a
                href={ROUTES.LOGIN}
                onClick={(e) => {
                  e.preventDefault();
                  router.push(ROUTES.LOGIN);
                }}
                className="text-blue-600 hover:underline font-medium"
              >
                sign in
              </a> to manage your tasks.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
