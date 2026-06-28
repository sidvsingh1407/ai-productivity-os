import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Trash2, Folder, ChevronDown, ChevronRight, AlertCircle, RefreshCw, FileText } from 'lucide-react';
import { projectsApi, Project, SavedPrompt } from '@/api/projects';
import { Badge } from '@/components/ui/badge';
import { format } from 'date-fns';

export function ProjectsTab() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedProjects, setExpandedProjects] = useState<Record<string, boolean>>({});

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    setLoading(true);
    try {
      const data = await projectsApi.listProjects();
      setProjects(data);
    } catch (err) {
      setError('Failed to load projects.');
    } finally {
      setLoading(false);
    }
  };

  const toggleProject = (projectId: string) => {
    setExpandedProjects((prev) => ({
      ...prev,
      [projectId]: !prev[projectId],
    }));
  };

  const handleDeleteProject = async (projectId: string, e: React.MouseEvent) => {
    e.stopPropagation(); // Prevent expanding the project
    if (window.confirm('Are you sure you want to delete this project and all its saved prompts?')) {
      try {
        await projectsApi.deleteProject(projectId);
        setProjects(projects.filter((p) => p.id !== projectId));
      } catch (err) {
        alert('Failed to delete project.');
      }
    }
  };

  const handleDeletePrompt = async (projectId: string, promptId: string) => {
    if (window.confirm('Are you sure you want to delete this saved prompt?')) {
      try {
        await projectsApi.deleteProjectPrompt(projectId, promptId);
        // Optimistically update the UI
        setProjects(projects.map(p => {
          if (p.id === projectId && p.saved_prompts) {
            return {
              ...p,
              saved_prompts: p.saved_prompts.filter(sp => sp.id !== promptId)
            };
          }
          return p;
        }));
      } catch (err) {
        alert('Failed to delete prompt.');
      }
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-12">
        <RefreshCw className="w-8 h-8 text-blue-500 animate-spin" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-red-50 text-red-600 rounded-md flex items-center gap-2">
        <AlertCircle className="w-5 h-5" />
        {error}
      </div>
    );
  }

  if (projects.length === 0) {
    return (
      <div className="text-center p-12 border border-dashed rounded-lg border-slate-300 dark:border-slate-700">
        <Folder className="w-12 h-12 text-slate-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-slate-900 dark:text-slate-100">No projects yet</h3>
        <p className="text-slate-500 dark:text-slate-400 mt-2">
          Save an improved prompt to create your first project.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {projects.map((project) => {
        const isExpanded = expandedProjects[project.id] || false;
        const promptCount = project.saved_prompts ? project.saved_prompts.length : 0;

        return (
          <Card key={project.id} className="overflow-hidden">
            <div
              className="p-4 flex items-center justify-between cursor-pointer hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors"
              onClick={() => toggleProject(project.id)}
            >
              <div className="flex items-center gap-3">
                {isExpanded ? (
                  <ChevronDown className="w-5 h-5 text-slate-400" />
                ) : (
                  <ChevronRight className="w-5 h-5 text-slate-400" />
                )}
                <div>
                  <h3 className="font-medium flex items-center gap-2 text-slate-900 dark:text-slate-100">
                    <Folder className="w-4 h-4 text-blue-500" />
                    {project.name}
                  </h3>
                  {project.description && (
                    <p className="text-sm text-slate-500 mt-1">{project.description}</p>
                  )}
                </div>
              </div>
              <div className="flex items-center gap-4">
                <Badge variant="secondary" className="font-normal">
                  {promptCount} {promptCount === 1 ? 'prompt' : 'prompts'}
                </Badge>
                <Button
                  variant="ghost"
                  size="sm"
                  className="text-red-500 hover:text-red-700 hover:bg-red-50 p-2 h-auto"
                  onClick={(e) => handleDeleteProject(project.id, e)}
                  title="Delete Project"
                >
                  <Trash2 className="w-4 h-4" />
                </Button>
              </div>
            </div>

            {isExpanded && (
              <div className="border-t border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900/20 p-4">
                {(!project.saved_prompts || project.saved_prompts.length === 0) ? (
                  <div className="text-center py-6 text-sm text-slate-500">
                    No prompts saved in this project yet.
                  </div>
                ) : (
                  <div className="space-y-3">
                    {project.saved_prompts.map((prompt: SavedPrompt) => (
                      <div key={prompt.id} className="bg-white dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-md p-4">
                        <div className="flex items-start justify-between mb-2">
                          <div className="font-medium text-slate-900 dark:text-slate-100 flex items-center gap-2">
                            <FileText className="w-4 h-4 text-slate-400" />
                            {prompt.title || 'Untitled Prompt'}
                          </div>
                          <div className="flex items-center gap-3">
                            <span className="text-xs text-slate-500">
                              {format(new Date(prompt.created_at), 'MMM d, yyyy h:mm a')}
                            </span>
                            <button
                              onClick={() => handleDeletePrompt(project.id, prompt.id)}
                              className="text-slate-400 hover:text-red-500 transition-colors"
                              title="Delete Prompt"
                            >
                              <Trash2 className="w-4 h-4" />
                            </button>
                          </div>
                        </div>
                        <div className="text-sm text-slate-600 dark:text-slate-400 line-clamp-2 italic">
                          "{prompt.original_prompt}"
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </Card>
        );
      })}
    </div>
  );
}
