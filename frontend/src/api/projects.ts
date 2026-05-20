// Projects API client
import { getToken } from './auth';

const API_BASE = '/api/projects';

export interface Project {
  id: string;
  name: string;
  gpt_description?: string;
  lyrics?: string;
  music_genre?: string;
  style?: string;
  voice_id?: string;
  task_id?: string;
  suno_title?: string;
  suno_id?: string;
  mv: string;
  duration?: number;
  music_url?: string;
  cover_url?: string;
  vocal_url?: string;
  final_url?: string;
  status: string;
  error_message?: string;
  points_cost: number;
  created_at: string;
}

export interface ProjectCreate {
  name: string;
  gpt_description?: string;
  lyrics?: string;
  music_genre?: string;
  style?: string;
  voice_id?: string;
  mv?: string;
  make_instrumental?: boolean;
}

export interface TaskStatus {
  task_id: string;
  status: 'pending' | 'completed' | 'failed';
  audio_url?: string;
  cover_url?: string;
  duration?: number;
  title?: string;
  lyrics?: string;
  error_msg?: string;
  points_cost: number;
}

// Create a new project
export async function createProject(data: ProjectCreate): Promise<Project> {
  const token = getToken();
  const res = await fetch(API_BASE, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: '创建失败' }));
    throw new Error(err.detail || '创建失败');
  }
  return res.json();
}

// Generate music for a project
export async function generateMusic(projectId: string): Promise<{ task_ids: number[]; message: string }> {
  const token = getToken();
  const res = await fetch(`${API_BASE}/${projectId}/generate`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: '生成失败' }));
    throw new Error(err.detail || '生成失败');
  }
  return res.json();
}

// Check generation status
export async function checkStatus(projectId: string): Promise<TaskStatus> {
  const token = getToken();
  const res = await fetch(`${API_BASE}/${projectId}/status`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: '查询失败' }));
    throw new Error(err.detail || '查询失败');
  }
  return res.json();
}

// Get all projects
export async function listProjects(): Promise<Project[]> {
  const token = getToken();
  const res = await fetch(API_BASE, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  if (!res.ok) {
    throw new Error('获取项目列表失败');
  }
  return res.json();
}

// Get single project
export async function getProject(projectId: string): Promise<Project> {
  const token = getToken();
  const res = await fetch(`${API_BASE}/${projectId}`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  if (!res.ok) {
    throw new Error('获取项目失败');
  }
  return res.json();
}

// Delete project
export async function deleteProject(projectId: string): Promise<void> {
  const token = getToken();
  const res = await fetch(`${API_BASE}/${projectId}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  if (!res.ok) {
    throw new Error('删除失败');
  }
}