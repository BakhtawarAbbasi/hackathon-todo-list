'use client';

import { useState } from 'react';
import { formatDate } from '@/lib/utils';
import { Task } from '@/types/tasks';
import { tasksService } from '@/services/tasks';
import { cn } from '@/lib/utils';

interface TaskItemProps {
  task: Task;
  onUpdate: (taskId: string, updatedData: { title?: string; description?: string; completed?: boolean }) => void;
  onDelete: (id: string) => void;
  onToggle: (id: string) => void;
}

export function TaskItem({ task, onUpdate, onDelete, onToggle }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || '');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleEdit = async () => {
    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    setLoading(true);
    setError('');

    try {
      onUpdate(task.id, {
        title: title.trim(),
        description: description.trim() || undefined
      });
      setIsEditing(false);
    } catch (err: any) {
      console.error('Error updating task:', err);
      setError(err.message || 'Failed to update task');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        onDelete(task.id);
      } catch (err: any) {
        console.error('Error deleting task:', err);
        alert(err.message || 'Failed to delete task');
      }
    }
  };

  const handleToggle = async () => {
    try {
      onToggle(task.id);
    } catch (err: any) {
      console.error('Error toggling task:', err);
      alert(err.message || 'Failed to update task status');
    }
  };

  return (
    <li className="py-4">
      <div className="flex items-start">
        <div className="flex items-start h-5">
          <input
            id={`task-${task.id}`}
            type="checkbox"
            checked={task.completed}
            onChange={handleToggle}
            className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
          />
        </div>
        <div className="ml-3 flex-1">
          {isEditing ? (
            <div className="space-y-3">
              {error && (
                <div className="text-red-600 text-sm">{error}</div>
              )}
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                placeholder="Task title"
              />
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                placeholder="Task description (optional)"
                rows={2}
              />
              <div className="flex space-x-2">
                <button
                  onClick={handleEdit}
                  disabled={loading}
                  className="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                >
                  {loading ? 'Saving...' : 'Save'}
                </button>
                <button
                  onClick={() => {
                    setIsEditing(false);
                    setTitle(task.title);
                    setDescription(task.description || '');
                    setError('');
                  }}
                  className="inline-flex items-center px-3 py-1 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <div>
              <label htmlFor={`task-${task.id}`} className="block text-sm font-medium text-gray-700">
                <span className={cn(task.completed && 'line-through text-gray-500')}>
                  {task.title}
                </span>
              </label>
              {task.description && (
                <p className={cn('mt-1 text-sm text-gray-500', task.completed && 'text-gray-400')}>
                  {task.description}
                </p>
              )}
              <p className="mt-1 text-xs text-gray-400">
                Created: {formatDate(task.createdAt)}
                {task.updatedAt !== task.createdAt && (
                  <span>, Updated: {formatDate(task.updatedAt)}</span>
                )}
              </p>
            </div>
          )}
        </div>
        <div className="ml-4 flex-shrink-0 flex space-x-2">
          {!isEditing && (
            <>
              <button
                onClick={() => setIsEditing(true)}
                className="inline-flex items-center px-2.5 py-0.5 border border-transparent text-xs font-medium rounded text-blue-700 bg-blue-100 hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Edit
              </button>
              <button
                onClick={handleDelete}
                className="inline-flex items-center px-2.5 py-0.5 border border-transparent text-xs font-medium rounded text-red-700 bg-red-100 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
              >
                Delete
              </button>
            </>
          )}
        </div>
      </div>
    </li>
  );
}