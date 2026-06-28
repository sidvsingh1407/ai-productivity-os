import React, { useState, useEffect } from 'react';
import { Modal } from '@/components/ui/modal';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { AlertCircle, CheckCircle2 } from 'lucide-react';
import { projectsApi, Project } from '@/api/projects';

// Simplified select since Shadcn select might not be fully installed or customized
interface SaveToProjectModalProps {
  isOpen: boolean;
  onClose: () => void;
  originalPrompt: string;
  improvedPrompt: string;
}

export function SaveToProjectModal({
  isOpen,
  onClose,
  originalPrompt,
  improvedPrompt,
}: SaveToProjectModalProps) {
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProjectId, setSelectedProjectId] = useState<string>('');
  const [isCreatingNew, setIsCreatingNew] = useState(false);
  const [newProjectName, setNewProjectName] = useState('');
  const [newProjectDescription, setNewProjectDescription] = useState('');
  const [promptTitle, setPromptTitle] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [limitReached, setLimitReached] = useState(false);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    if (isOpen) {
      loadProjects();
      setSuccess(false);
      setPromptTitle('');
      setNewProjectName('');
      setNewProjectDescription('');
      setIsCreatingNew(false);
      setError(null);
      setLimitReached(false);
    }
  }, [isOpen]);

  const loadProjects = async () => {
    try {
      const data = await projectsApi.listProjects();
      setProjects(data);
      if (data.length > 0) {
        setSelectedProjectId(data[0].id);
      } else {
        setIsCreatingNew(true);
      }
    } catch (err) {
      setError('Failed to load projects.');
    }
  };

  const handleSave = async () => {
    setIsLoading(true);
    setError(null);
    setLimitReached(false);

    try {
      let projectIdToUse = selectedProjectId;

      if (isCreatingNew) {
        if (!newProjectName.trim()) {
          setError('Project name is required.');
          setIsLoading(false);
          return;
        }
        try {
          const newProject = await projectsApi.createProject(newProjectName, newProjectDescription);
          projectIdToUse = newProject.id;
          setProjects([newProject, ...projects]);
        } catch (err: any) {
          if (err.response?.data?.detail === 'project_limit_reached') {
            setLimitReached(true);
            setIsLoading(false);
            return;
          }
          throw err;
        }
      }

      if (!projectIdToUse) {
         setError('Please select or create a project.');
         setIsLoading(false);
         return;
      }

      await projectsApi.savePromptToProject(
        projectIdToUse,
        originalPrompt,
        improvedPrompt,
        promptTitle.trim() || undefined
      );

      setSuccess(true);
      setTimeout(() => {
        onClose();
      }, 1500);
    } catch (err: any) {
      setError('Failed to save prompt.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Save to Project">
        {success ? (
          <div className="flex flex-col items-center justify-center py-6 text-center space-y-3 dark:text-white">
            <div className="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center mb-2">
              <CheckCircle2 className="w-6 h-6 text-green-600" />
            </div>
            <h3 className="text-lg font-medium">Saved Successfully</h3>
            <p className="text-sm text-slate-500">Your prompt has been saved to the project.</p>
          </div>
        ) : (
          <div className="space-y-4 py-2 dark:text-white">
            <p className="text-sm text-slate-500 dark:text-slate-400 mb-4">
              Save this prompt and its improved version to a project.
            </p>
            {error && (
               <div className="p-3 bg-red-50 text-red-600 text-sm rounded-md flex items-start gap-2">
                 <AlertCircle className="w-4 h-4 mt-0.5" />
                 <span>{error}</span>
               </div>
            )}

            {limitReached && (
              <div className="p-3 bg-amber-50 text-amber-700 text-sm rounded-md border border-amber-200">
                You've reached the free limit of 3 projects. Upgrade to create more.
              </div>
            )}

            <div className="space-y-2">
              <Label>Save to</Label>
              {projects.length > 0 && (
                <div className="flex items-center space-x-2 mb-2">
                  <input
                    type="radio"
                    id="existing-project"
                    checked={!isCreatingNew}
                    onChange={() => setIsCreatingNew(false)}
                    className="w-4 h-4 text-blue-600"
                  />
                  <Label htmlFor="existing-project" className="font-normal cursor-pointer">
                    Existing project
                  </Label>
                  <input
                    type="radio"
                    id="new-project"
                    checked={isCreatingNew}
                    onChange={() => setIsCreatingNew(true)}
                    className="w-4 h-4 text-blue-600 ml-4"
                  />
                  <Label htmlFor="new-project" className="font-normal cursor-pointer">
                    New project
                  </Label>
                </div>
              )}

              {!isCreatingNew && projects.length > 0 && (
                <select
                    value={selectedProjectId}
                    onChange={(e) => setSelectedProjectId(e.target.value)}
                    className="flex h-10 w-full rounded-md border border-slate-300 bg-transparent px-3 py-2 text-sm placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 dark:border-slate-700 dark:text-slate-50 dark:focus:ring-slate-400 dark:focus:ring-offset-slate-900"
                >
                    <option value="" disabled className="dark:bg-slate-900">Select a project</option>
                    {projects.map((p) => (
                      <option key={p.id} value={p.id} className="dark:bg-slate-900">
                        {p.name}
                      </option>
                    ))}
                </select>
              )}

              {isCreatingNew && (
                <div className="space-y-3 mt-2 p-3 bg-slate-50 dark:bg-slate-800 rounded-md border border-slate-200 dark:border-slate-700">
                  <div className="space-y-1">
                    <Label htmlFor="project-name" className="text-xs text-slate-500 dark:text-slate-400">Project Name</Label>
                    <Input
                      id="project-name"
                      placeholder="e.g., Q3 Marketing Campaigns"
                      value={newProjectName}
                      onChange={(e) => setNewProjectName(e.target.value)}
                    />
                  </div>
                  <div className="space-y-1">
                    <Label htmlFor="project-desc" className="text-xs text-slate-500 dark:text-slate-400">Description (optional)</Label>
                    <Input
                      id="project-desc"
                      placeholder="What is this project for?"
                      value={newProjectDescription}
                      onChange={(e) => setNewProjectDescription(e.target.value)}
                    />
                  </div>
                </div>
              )}
            </div>

            <div className="space-y-2 mt-4">
              <Label htmlFor="prompt-title">Prompt Title (optional)</Label>
              <Input
                id="prompt-title"
                placeholder="e.g., Blog post generator"
                value={promptTitle}
                onChange={(e) => setPromptTitle(e.target.value)}
              />
            </div>
          </div>
        )}

        {!success && (
          <div className="flex justify-end space-x-2 pt-4 border-t mt-4 border-slate-200 dark:border-slate-700">
            <Button variant="outline" onClick={onClose} disabled={isLoading}>
              Cancel
            </Button>
            <Button
              onClick={handleSave}
              disabled={isLoading || limitReached || (isCreatingNew && !newProjectName.trim())}
            >
              {isLoading ? 'Saving...' : 'Save'}
            </Button>
          </div>
        )}
    </Modal>
  );
}
