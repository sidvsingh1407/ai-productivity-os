import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { AlertCircle, Copy, CheckCircle2, ChevronRight, XCircle, Plus, Trash2, Folder, Clock, ChevronDown, ChevronUp, History } from 'lucide-react';
import { promptImproverApi, PromptIntelligenceResponse } from '@/api/promptImprover';
import { projectsApi, Project, PromptHistoryRecord } from '@/api/projects';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";

// Layout components for responsive sidebar/drawer
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";

export default function PromptImprover() {
  const [prompt, setPrompt] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<PromptIntelligenceResponse | null>(null);
  const [copied, setCopied] = useState(false);

  // Projects state
  const [projects, setProjects] = useState<Project[]>([]);
  const [history, setHistory] = useState<PromptHistoryRecord[]>([]);
  const [expandedProjects, setExpandedProjects] = useState<string[]>([]);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  // New project state
  const [isCreatingProject, setIsCreatingProject] = useState(false);
  const [newProjectName, setNewProjectName] = useState('');
  const [projectError, setProjectError] = useState<string | null>(null);

  // Save dialog state
  const [isSaveDialogOpen, setIsSaveDialogOpen] = useState(false);
  const [selectedProjectId, setSelectedProjectId] = useState<string>('new');
  const [saveTitle, setSaveTitle] = useState('');
  const [isSaving, setIsSaving] = useState(false);

  const characterCount = prompt.length;
  const maxCharacters = 10000;

  useEffect(() => {
    loadProjects();
    loadHistory();
  }, []);

  const loadProjects = async () => {
    try {
      const data = await projectsApi.listProjects();
      setProjects(data);
    } catch (err) {
      console.error("Failed to load projects", err);
    }
  };

  const loadHistory = async () => {
    try {
      const data = await projectsApi.getPromptHistory();
      setHistory(data);
    } catch (err) {
      console.error("Failed to load history", err);
    }
  };

  const handleAnalyze = async () => {
    if (!prompt.trim()) {
      setError('Prompt cannot be empty.');
      return;
    }
    if (characterCount > maxCharacters) {
      setError('Prompt is too long.');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const data = await promptImproverApi.analyzePrompt(prompt);
      setResult(data);
      // Reload history after successful analysis
      if (data.improved_prompt) {
          loadHistory();
      }
    } catch (err: any) {
      if (err.response && err.response.data && err.response.data.validation) {
        setResult({
           ...err.response.data,
           operational_context: { detected_context: 'Unknown', purpose: '', operational_environment: '' },
           diagnosis: { strength: 'N/A', missing_elements: [], execution_risks: [] },
           intelligence_scores: { original_score: 0, improved_score: 0 },
           improved_prompt: '',
           improvement_rationale: { context_reasoning: '', changes_made: [], failure_modes_addressed: [], expected_improvements: '' }
        });
      } else {
        setResult({
           validation: { passed: false, validation_errors: [err.response?.data?.detail || 'An error occurred during analysis.'] },
           operational_context: { detected_context: 'Unknown', purpose: '', operational_environment: '' },
           diagnosis: { strength: 'N/A', missing_elements: [], execution_risks: [] },
           intelligence_scores: { original_score: 0, improved_score: 0 },
           improved_prompt: '',
           improvement_rationale: { context_reasoning: '', changes_made: [], failure_modes_addressed: [], expected_improvements: '' }
        });
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopy = () => {
    if (result?.improved_prompt) {
      navigator.clipboard.writeText(result.improved_prompt);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const toggleProjectExpand = async (projectId: string) => {
    if (expandedProjects.includes(projectId)) {
      setExpandedProjects(expandedProjects.filter(id => id !== projectId));
    } else {
      setExpandedProjects([...expandedProjects, projectId]);
      // Load project details if not loaded
      const project = projects.find(p => p.id === projectId);
      if (project && !project.saved_prompts) {
        try {
          const detail = await projectsApi.getProject(projectId);
          setProjects(projects.map(p => p.id === projectId ? detail : p));
        } catch (err) {
          console.error("Failed to load project details", err);
        }
      }
    }
  };

  const handleCreateProject = async () => {
    if (!newProjectName.trim()) return;
    setProjectError(null);
    try {
      const newProj = await projectsApi.createProject(newProjectName);
      setProjects([newProj, ...projects]);
      setNewProjectName('');
      setIsCreatingProject(false);
    } catch (err: any) {
      if (err.response?.status === 402) {
        setProjectError("You've reached the free limit of 3 projects. Upgrade to organise unlimited AI initiatives.");
      } else {
        setProjectError("Failed to create project.");
      }
    }
  };

  const handleDeleteProject = async (projectId: string) => {
    if (!confirm("Are you sure you want to delete this project and all its saved prompts?")) return;
    try {
      await projectsApi.deleteProject(projectId);
      setProjects(projects.filter(p => p.id !== projectId));
      setExpandedProjects(expandedProjects.filter(id => id !== projectId));
    } catch (err) {
      console.error("Failed to delete project", err);
    }
  };

  const handleDeletePrompt = async (projectId: string, promptId: string) => {
    try {
      await projectsApi.deleteProjectPrompt(projectId, promptId);
      // Update local state
      setProjects(projects.map(p => {
        if (p.id === projectId) {
          return {
            ...p,
            saved_prompts_count: p.saved_prompts_count ? p.saved_prompts_count - 1 : 0,
            saved_prompts: p.saved_prompts?.filter(sp => sp.id !== promptId)
          };
        }
        return p;
      }));
    } catch (err) {
      console.error("Failed to delete prompt", err);
    }
  };

  const handleSaveToProject = async () => {
    if (!result?.improved_prompt) return;

    setIsSaving(true);
    try {
      let targetProjectId = selectedProjectId;

      // If "new", create project first
      if (targetProjectId === 'new') {
        if (!newProjectName.trim()) {
           setProjectError("Please enter a project name.");
           setIsSaving(false);
           return;
        }
        try {
           const newProj = await projectsApi.createProject(newProjectName);
           targetProjectId = newProj.id;
           setProjects([newProj, ...projects]);
        } catch (err: any) {
           if (err.response?.status === 402) {
             setProjectError("You've reached the free limit of 3 projects. Upgrade to organise unlimited AI initiatives.");
           } else {
             setProjectError("Failed to create project.");
           }
           setIsSaving(false);
           return;
        }
      }

      // Save prompt to project
      await projectsApi.savePromptToProject(
          targetProjectId,
          prompt, // original prompt
          result.improved_prompt,
          saveTitle.trim() || undefined
      );

      // Refresh projects
      await loadProjects();

      // Close dialog and show success
      setIsSaveDialogOpen(false);
      setNewProjectName('');
      setSaveTitle('');
      setProjectError(null);
      // Could add a toast notification here

    } catch (err) {
      console.error("Failed to save to project", err);
    } finally {
      setIsSaving(false);
    }
  };

  // Truncate helper
  const truncate = (str: string, length: number = 100) => {
    return str.length > length ? str.substring(0, length) + '...' : str;
  };

  const renderSidebarContent = () => (
    <div className="flex flex-col h-full overflow-hidden">
      <Tabs defaultValue="projects" className="flex-1 flex flex-col overflow-hidden">
        <TabsList className="w-full grid grid-cols-2 p-1 bg-muted rounded-md mb-4 shrink-0">
          <TabsTrigger value="projects" className="flex items-center gap-2">
            <Folder className="w-4 h-4" /> Projects
          </TabsTrigger>
          <TabsTrigger value="history" className="flex items-center gap-2">
            <History className="w-4 h-4" /> History
          </TabsTrigger>
        </TabsList>

        {/* Projects Tab */}
        <TabsContent value="projects" className="flex-1 overflow-y-auto pr-2 space-y-4 m-0">
          <div className="flex justify-between items-center mb-2">
            <h3 className="font-semibold">Your Projects</h3>
            <Button variant="ghost" size="sm" onClick={() => { setIsCreatingProject(true); setProjectError(null); }}>
              <Plus className="w-4 h-4 mr-1" /> New
            </Button>
          </div>

          {isCreatingProject && (
            <div className="bg-muted p-3 rounded-md mb-4 space-y-2 border">
              <Input
                placeholder="Project Name"
                value={newProjectName}
                onChange={e => setNewProjectName(e.target.value)}
                autoFocus
              />
              {projectError && <div className="text-xs text-red-500">{projectError}</div>}
              <div className="flex justify-end gap-2">
                <Button variant="ghost" size="sm" onClick={() => setIsCreatingProject(false)}>Cancel</Button>
                <Button size="sm" onClick={handleCreateProject} disabled={!newProjectName.trim() || projectError?.includes('limit')}>Create</Button>
              </div>
            </div>
          )}

          {projects.length === 0 && !isCreatingProject ? (
            <div className="text-center text-muted-foreground py-8 text-sm">
              <Folder className="w-8 h-8 mx-auto mb-2 opacity-20" />
              <p>No projects yet.</p>
              <p>Create one to save your improved prompts.</p>
            </div>
          ) : (
            <div className="space-y-2">
              {projects.map(project => (
                <div key={project.id} className="border rounded-md overflow-hidden bg-card">
                  <div className="flex items-center justify-between p-3 hover:bg-muted/50 transition-colors">
                    <button
                      className="flex items-center flex-1 text-left font-medium text-sm gap-2"
                      onClick={() => toggleProjectExpand(project.id)}
                    >
                      {expandedProjects.includes(project.id) ? <ChevronDown className="w-4 h-4 text-muted-foreground" /> : <ChevronRight className="w-4 h-4 text-muted-foreground" />}
                      <span className="truncate">{project.name}</span>
                      <Badge variant="secondary" className="ml-auto text-[10px]">{project.saved_prompts_count || 0}</Badge>
                    </button>
                    <Button variant="ghost" size="icon" className="h-6 w-6 ml-1 text-muted-foreground hover:text-destructive" onClick={() => handleDeleteProject(project.id)}>
                      <Trash2 className="w-3.5 h-3.5" />
                    </Button>
                  </div>

                  {expandedProjects.includes(project.id) && (
                    <div className="bg-muted/30 p-2 border-t text-sm">
                      {!project.saved_prompts ? (
                        <div className="text-center py-2 text-xs text-muted-foreground">Loading...</div>
                      ) : project.saved_prompts.length === 0 ? (
                        <div className="text-center py-2 text-xs text-muted-foreground">No prompts saved yet.</div>
                      ) : (
                        <ul className="space-y-2">
                          {project.saved_prompts.map(prompt => (
                            <li key={prompt.id} className="bg-background border rounded p-2 text-xs group relative">
                              <div className="font-medium mb-1 truncate pr-6">{prompt.title || 'Untitled Prompt'}</div>
                              <div className="text-muted-foreground line-clamp-2 mb-2">{prompt.original_prompt}</div>
                              <div className="flex items-center justify-between">
                                <span className="text-[10px] text-muted-foreground">{new Date(prompt.created_at).toLocaleDateString()}</span>
                                <Button
                                  variant="ghost"
                                  size="sm"
                                  className="h-5 px-2 text-[10px]"
                                  onClick={() => {
                                      setPrompt(prompt.original_prompt);
                                      if (prompt.improved_prompt) {
                                          // Simulate a quick result if they want to view it, but typically they would just see it in the UI or re-run
                                          // Since PromptImprover uses state `result`, we can just populate the input.
                                          // For better UX, we'd load the full result, but we only have improved_prompt here.
                                          // Let's just set the input for now.
                                      }
                                  }}
                                >
                                  Load
                                </Button>
                              </div>
                              <button
                                className="absolute top-1 right-1 opacity-0 group-hover:opacity-100 p-1 text-muted-foreground hover:text-destructive transition-opacity"
                                onClick={() => handleDeletePrompt(project.id, prompt.id)}
                              >
                                <XCircle className="w-3.5 h-3.5" />
                              </button>
                            </li>
                          ))}
                        </ul>
                      )}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </TabsContent>

        {/* History Tab */}
        <TabsContent value="history" className="flex-1 overflow-y-auto pr-2 m-0 flex flex-col">
          {history.length === 0 ? (
            <div className="text-center text-muted-foreground py-8 text-sm flex-1">
              <Clock className="w-8 h-8 mx-auto mb-2 opacity-20" />
              <p>Your improved prompts will appear here.</p>
            </div>
          ) : (
            <div className="space-y-3 flex-1">
              {history.map(item => (
                <div key={item.id} className="border rounded-md p-3 bg-card text-sm">
                  <div className="text-muted-foreground line-clamp-2 mb-2 italic">"{item.original_prompt}"</div>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-muted-foreground flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {new Date(item.created_at).toLocaleDateString()}
                    </span>
                    <Button
                      variant="ghost"
                      size="sm"
                      className="h-6 px-2 text-xs"
                      onClick={() => setPrompt(item.original_prompt)}
                    >
                      Reuse
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          )}
          <div className="text-[10px] text-center text-muted-foreground mt-4 pt-4 border-t shrink-0">
            Showing your last 30 prompts.
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );

  return (
    <div className="container mx-auto max-w-7xl px-4 py-8 flex flex-col md:flex-row gap-6 h-[calc(100vh-4rem)]">

      {/* Mobile Drawer Trigger */}
      <div className="md:hidden flex items-center justify-between mb-4 shrink-0">
        <h1 className="text-2xl font-bold">Prompt Improver</h1>
        <Sheet open={isSidebarOpen} onOpenChange={setIsSidebarOpen}>
          <SheetTrigger asChild>
            <Button variant="outline" size="sm" className="gap-2">
              <Folder className="w-4 h-4" /> Projects & History
            </Button>
          </SheetTrigger>
          <SheetContent side="left" className="w-[300px] sm:w-[350px]">
            <SheetHeader className="mb-4">
              <SheetTitle>Workspace</SheetTitle>
              <SheetDescription className="sr-only">Manage your projects and prompt history.</SheetDescription>
            </SheetHeader>
            {renderSidebarContent()}
          </SheetContent>
        </Sheet>
      </div>

      {/* Desktop Sidebar */}
      <div className="hidden md:block w-72 shrink-0 border-r pr-6 h-full">
        <div className="mb-6">
          <h1 className="text-2xl font-bold">Workspace</h1>
        </div>
        {renderSidebarContent()}
      </div>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col h-full overflow-hidden">
        <div className="hidden md:block mb-6 shrink-0">
          <h1 className="text-2xl font-bold">Prompt Improver</h1>
          <p className="text-muted-foreground">Enhance your prompts with intelligence context and validation.</p>
        </div>

        <div className="flex-1 overflow-y-auto pb-8 pr-2">
          {/* Main area from original PromptImprover.tsx */}
          <Card className="mb-8 border-none shadow-none bg-transparent shrink-0">
            <CardContent className="p-0">
              <div className="relative">
                <Textarea
                  placeholder="Paste your raw prompt here..."
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  className="min-h-[200px] resize-y bg-bg-secondary border-border-light text-base p-4"
                />
                <div className="absolute bottom-3 right-3 text-xs text-text-secondary">
                  {characterCount} / {maxCharacters}
                </div>
              </div>

              {error && (
                <div className="mt-4 p-3 bg-red-50 dark:bg-red-950/20 text-red-600 dark:text-red-400 text-sm rounded-md flex items-start gap-2">
                  <AlertCircle className="w-4 h-4 mt-0.5 shrink-0" />
                  <span>{error}</span>
                </div>
              )}

              <div className="mt-4 flex justify-end">
                <Button
                  onClick={handleAnalyze}
                  disabled={isLoading}
                  className="w-full sm:w-auto"
                >
                  {isLoading ? 'Improving Prompt...' : 'Improve Prompt'}
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Results Area */}
          {result && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 shrink-0">
              {/* Left Column: Metrics & Diagnostics */}
              <div className="space-y-6">

                {/* Validation Status Card */}
                <Card className={result.validation.passed ? 'border-green-500/30 bg-green-50/30 dark:bg-green-950/20' : 'border-red-500/30 bg-red-50/30 dark:bg-red-950/20'}>
                    <CardContent className="pt-6">
                       <div className="flex items-center gap-3">
                           {result.validation.passed ? (
                             <CheckCircle2 className="w-6 h-6 text-green-500" />
                           ) : (
                             <XCircle className="w-6 h-6 text-red-500" />
                           )}
                           <div>
                               <h3 className="font-semibold text-lg">{result.validation.passed ? 'Validation Passed' : 'Validation Failed'}</h3>
                           </div>
                       </div>
                       {!result.validation.passed && result.validation.validation_errors && result.validation.validation_errors.length > 0 && (
                           <ul className="mt-4 space-y-2">
                               {result.validation.validation_errors.map((err, i) => (
                                   <li key={i} className="text-sm text-red-600 flex items-start gap-2">
                                      <AlertCircle className="w-4 h-4 mt-0.5 shrink-0" />
                                      <span>{err}</span>
                                   </li>
                               ))}
                           </ul>
                       )}
                    </CardContent>
                </Card>

                {/* Only show rest if we have a full result (passed or graceful degrade) */}
                {result.improved_prompt && (
                  <>
                    <Card>
                    <CardHeader className="pb-3">
                        <CardTitle className="text-base">Intelligence Score</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="flex items-center justify-between">
                        <div className="text-center">
                            <div className="text-3xl font-bold text-text-secondary">{result.intelligence_scores?.original_score || 0}</div>
                            <div className="text-xs text-text-secondary uppercase mt-1">Original</div>
                        </div>
                        <ChevronRight className="w-6 h-6 text-border-strong" />
                        <div className="text-center">
                            <div className="text-3xl font-bold text-primary">{result.intelligence_scores?.improved_score || 0}</div>
                            <div className="text-xs text-text-secondary uppercase mt-1">Improved</div>
                        </div>
                        </div>
                    </CardContent>
                    </Card>

                    <Card>
                    <CardHeader className="pb-3">
                        <CardTitle className="text-base">Operational Context</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                            <div>
                                <div className="text-sm text-text-secondary mb-1">Detected Context</div>
                                <div className="font-medium">{result.operational_context?.detected_context || 'Unknown'}</div>
                            </div>
                            <div>
                                <div className="text-sm text-text-secondary mb-1">Operational Environment</div>
                                <div className="font-medium">{result.operational_context?.operational_environment || 'Unknown'}</div>
                            </div>
                        </div>
                    </CardContent>
                    </Card>

                    <Card>
                    <CardHeader className="pb-3">
                        <CardTitle className="text-base">Diagnosis</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                            <div>
                                <div className="text-sm text-text-secondary mb-1">Strength Rating</div>
                                <Badge variant={result.diagnosis?.strength === 'Broken' ? 'destructive' : result.diagnosis?.strength === 'Weak' ? 'secondary' : 'default'}>
                                    {result.diagnosis?.strength || 'N/A'}
                                </Badge>
                            </div>
                            {result.diagnosis?.missing_elements && result.diagnosis.missing_elements.length > 0 && (
                                <div>
                                    <div className="text-sm text-text-secondary mb-2">Missing Elements</div>
                                    <div className="flex flex-wrap gap-2">
                                        {result.diagnosis.missing_elements.map((item, i) => (
                                            <Badge key={i} variant="outline" className="text-xs">{item}</Badge>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    </CardContent>
                    </Card>

                    <Card className="border-red-500/30 bg-red-50/30 dark:bg-red-950/20">
                    <CardHeader className="pb-3">
                        <CardTitle className="text-base flex items-center gap-2 text-red-700 dark:text-red-400">
                            <AlertCircle className="w-5 h-5" />
                            Top Risks
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        {result.diagnosis?.execution_risks && result.diagnosis.execution_risks.length > 0 ? (
                            <ul className="space-y-2">
                                {result.diagnosis.execution_risks.map((risk, i) => (
                                    <li key={i} className="text-sm flex items-start gap-2 text-red-900/80 dark:text-red-200/80 font-medium">
                                        <div className="w-1.5 h-1.5 rounded-full bg-red-500 mt-1.5 shrink-0" />
                                        {risk}
                                    </li>
                                ))}
                            </ul>
                        ) : (
                            <div className="text-sm text-text-secondary">No significant risks detected.</div>
                        )}
                    </CardContent>
                    </Card>
                  </>
                )}

              </div>

              {/* Right Column: Output */}
              {result.improved_prompt && (
                <div className="lg:col-span-2 space-y-6">
                    <Card className="h-full flex flex-col">
                    <CardHeader className="flex flex-row items-center justify-between pb-3">
                        <div>
                            <CardTitle>Improved Prompt</CardTitle>
                            <CardDescription>Deployable instructions for your AI agent.</CardDescription>
                        </div>
                        <div className="flex items-center gap-2">
                            {/* Save to Project Dialog Trigger */}
                            <Dialog open={isSaveDialogOpen} onOpenChange={setIsSaveDialogOpen}>
                              <DialogTrigger asChild>
                                <Button variant="outline" size="sm" className="gap-2">
                                  <Folder className="w-4 h-4" /> Save to Project
                                </Button>
                              </DialogTrigger>
                              <DialogContent className="sm:max-w-[425px]">
                                <DialogHeader>
                                  <DialogTitle>Save to Project</DialogTitle>
                                  <DialogDescription>
                                    Save this improved prompt to organise your workspace.
                                  </DialogDescription>
                                </DialogHeader>
                                <div className="grid gap-4 py-4">
                                  <div className="grid gap-2">
                                    <Label htmlFor="title">Prompt Title (Optional)</Label>
                                    <Input
                                      id="title"
                                      placeholder="e.g. Marketing copy generator"
                                      value={saveTitle}
                                      onChange={(e) => setSaveTitle(e.target.value)}
                                    />
                                  </div>
                                  <div className="grid gap-2">
                                    <Label>Select Project</Label>
                                    <RadioGroup value={selectedProjectId} onValueChange={setSelectedProjectId} className="space-y-2 mt-2">
                                      {projects.map((project) => (
                                        <div className="flex items-center space-x-2" key={project.id}>
                                          <RadioGroupItem value={project.id} id={project.id} />
                                          <Label htmlFor={project.id} className="cursor-pointer">{project.name}</Label>
                                        </div>
                                      ))}
                                      <div className="flex items-center space-x-2 pt-2 border-t mt-2">
                                        <RadioGroupItem value="new" id="new" />
                                        <Label htmlFor="new" className="cursor-pointer">Create new project</Label>
                                      </div>
                                    </RadioGroup>
                                  </div>

                                  {selectedProjectId === 'new' && (
                                    <div className="grid gap-2 ml-6">
                                      <Input
                                        placeholder="Project Name"
                                        value={newProjectName}
                                        onChange={(e) => setNewProjectName(e.target.value)}
                                      />
                                    </div>
                                  )}
                                  {projectError && <div className="text-sm text-red-500">{projectError}</div>}
                                </div>
                                <DialogFooter>
                                  <Button variant="ghost" onClick={() => setIsSaveDialogOpen(false)}>Cancel</Button>
                                  <Button onClick={handleSaveToProject} disabled={isSaving || (selectedProjectId === 'new' && !newProjectName.trim())}>
                                    {isSaving ? 'Saving...' : 'Save Prompt'}
                                  </Button>
                                </DialogFooter>
                              </DialogContent>
                            </Dialog>

                            <Button variant="outline" size="sm" onClick={handleCopy} className="gap-2">
                                {copied ? <CheckCircle2 className="w-4 h-4 text-green-500" /> : <Copy className="w-4 h-4" />}
                                {copied ? 'Copied' : 'Copy'}
                            </Button>
                        </div>
                    </CardHeader>
                    <CardContent className="flex-1">
                        <div className="bg-bg-secondary border border-border-light rounded-md p-6 h-full font-mono text-sm whitespace-pre-wrap leading-relaxed overflow-y-auto min-h-[300px]">
                            {result.improved_prompt}
                        </div>
                    </CardContent>
                    </Card>

                    <Card>
                    <CardHeader className="pb-3">
                        <CardTitle className="text-base">Improvement Rationale</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div className="md:col-span-2">
                                <div className="text-sm font-medium mb-1">Why This Context Was Selected</div>
                                <div className="text-sm text-text-secondary leading-relaxed">
                                    {result.improvement_rationale?.context_reasoning || 'N/A'}
                                </div>
                            </div>

                            <div>
                                <div className="text-sm font-medium mb-3">Changes Made</div>
                                <ul className="space-y-2">
                                    {result.improvement_rationale?.changes_made?.map((change, i) => (
                                        <li key={i} className="text-sm text-text-secondary flex gap-2">
                                            <CheckCircle2 className="w-4 h-4 text-green-500 shrink-0 mt-0.5" />
                                            <span>{change}</span>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                            <div>
                                <div className="text-sm font-medium mb-3">Failure Modes Addressed</div>
                                <ul className="space-y-2">
                                    {result.improvement_rationale?.failure_modes_addressed?.map((mode, i) => (
                                        <li key={i} className="text-sm text-text-secondary flex gap-2">
                                            <CheckCircle2 className="w-4 h-4 text-accent-blue shrink-0 mt-0.5" />
                                            <span>{mode}</span>
                                        </li>
                                    ))}
                                </ul>
                            </div>

                            <div className="md:col-span-2 mt-2 pt-4 border-t border-border-light">
                                <div className="text-sm font-medium mb-1">Expected Improvement</div>
                                <div className="text-sm text-text-secondary leading-relaxed">
                                    {result.improvement_rationale?.expected_improvements || 'N/A'}
                                </div>
                            </div>
                        </div>
                    </CardContent>
                    </Card>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
