import { Task } from '@/types/tasks';
import { TaskItem } from './TaskItem';

interface TaskListProps {
  tasks: Task[];
  onTaskUpdate: (taskId: string, updatedData: { title?: string; description?: string; completed?: boolean }) => void;
  onTaskDelete: (id: string) => void;
  onTaskToggle: (id: string) => void;
}

export function TaskList({ tasks, onTaskUpdate, onTaskDelete, onTaskToggle }: TaskListProps) {
  if (tasks.length === 0) {
    return (
      <div className="text-center py-10">
        <svg
          className="mx-auto h-12 w-12 text-gray-400"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
          />
        </svg>
        <h3 className="mt-2 text-sm font-medium text-gray-900">No tasks</h3>
        <p className="mt-1 text-sm text-gray-500">Get started by creating a new task.</p>
      </div>
    );
  }

  return (
    <ul className="divide-y divide-gray-200">
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onUpdate={onTaskUpdate}
          onDelete={onTaskDelete}
          onToggle={onTaskToggle}
        />
      ))}
    </ul>
  );
}