import { apiClient } from './client';

export interface SavedPrompt {
    id: string;
    project_id: string;
    user_id: string;
    title: string | null;
    original_prompt: string;
    improved_prompt: string | null;
    created_at: string;
}

export interface Project {
    id: string;
    user_id: string;
    name: string;
    description: string | null;
    created_at: string;
    updated_at: string;
    saved_prompts?: SavedPrompt[];
    saved_prompts_count?: number;
}

export interface PromptHistoryRecord {
    id: string;
    user_id: string;
    original_prompt: string;
    improved_prompt: string | null;
    created_at: string;
}

export const projectsApi = {
    createProject: async (name: string, description?: string): Promise<Project> => {
        const { data } = await apiClient.post('/api/projects', { name, description });
        return data;
    },
    listProjects: async (): Promise<Project[]> => {
        const { data } = await apiClient.get('/api/projects');
        return data;
    },
    getProject: async (projectId: string): Promise<Project> => {
        const { data } = await apiClient.get(`/api/projects/${projectId}`);
        return data;
    },
    updateProject: async (projectId: string, name?: string, description?: string): Promise<Project> => {
        const { data } = await apiClient.put(`/api/projects/${projectId}`, { name, description });
        return data;
    },
    deleteProject: async (projectId: string): Promise<void> => {
        await apiClient.delete(`/api/projects/${projectId}`);
    },
    savePromptToProject: async (projectId: string, original_prompt: string, improved_prompt: string, title?: string): Promise<SavedPrompt> => {
        const { data } = await apiClient.post(`/api/projects/${projectId}/prompts`, { original_prompt, improved_prompt, title });
        return data;
    },
    listProjectPrompts: async (projectId: string): Promise<SavedPrompt[]> => {
        const { data } = await apiClient.get(`/api/projects/${projectId}/prompts`);
        return data;
    },
    deleteProjectPrompt: async (projectId: string, promptId: string): Promise<void> => {
        await apiClient.delete(`/api/projects/${projectId}/prompts/${promptId}`);
    },
    getPromptHistory: async (): Promise<PromptHistoryRecord[]> => {
        const { data } = await apiClient.get('/api/prompt-improver/history');
        return data;
    }
};
