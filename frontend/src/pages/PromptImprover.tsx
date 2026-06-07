import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { AlertCircle, Copy, CheckCircle2, ChevronRight, XCircle } from 'lucide-react';
import { promptImproverApi, PromptIntelligenceResponse } from '@/api/promptImprover';

export default function PromptImprover() {
  const [prompt, setPrompt] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<PromptIntelligenceResponse | null>(null);
  const [copied, setCopied] = useState(false);

  const characterCount = prompt.length;
  const maxCharacters = 10000;

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
    } catch (err: any) {
      if (err.response && err.response.data && err.response.data.validation) {
        setResult({
           ...err.response.data,
           // fill missing parts to satisfy type if only validation is returned
           operational_context: { detected_context: 'Unknown', purpose: '', operational_environment: '' },
           diagnosis: { strength: 'N/A', missing_elements: [], execution_risks: [] },
           intelligence_scores: { original_score: 0, improved_score: 0 },
           improved_prompt: '',
           improvement_rationale: { context_reasoning: '', changes_made: [], failure_modes_addressed: [], expected_improvements: '' }
        });
      } else {
        // Fallback for API errors without a validation block to avoid UI crash
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

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-h1 font-bold">Prompt Improver</h1>
        <p className="text-body text-text-secondary mt-2">
          Transform operational instructions into high-reliability prompts.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Input Prompt</CardTitle>
          <CardDescription>Paste your operational instructions or existing prompt below.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="relative">
              <Textarea
                placeholder="E.g., Create a customer support chatbot."
                className="min-h-[150px] resize-y"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                disabled={isLoading}
              />
              <div className="absolute bottom-3 right-3 text-sm text-text-secondary">
                {characterCount} / {maxCharacters}
              </div>
            </div>

            {error && (
              <div className="flex items-center gap-2 text-accent-red text-sm">
                <AlertCircle className="w-4 h-4" />
                {error}
              </div>
            )}

            <Button onClick={handleAnalyze} disabled={isLoading || characterCount === 0}>
              {isLoading ? 'Analyzing...' : 'Analyze Prompt'}
            </Button>
          </div>
        </CardContent>
      </Card>

      {result && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
          {/* Left Column: Diagnostics */}
          <div className="lg:col-span-1 space-y-6">

            {/* Validation Status */}
            <Card className={result.validation.passed ? "border-green-500/20 bg-green-50/50 dark:bg-green-950/10" : "border-red-500/20 bg-red-50/50 dark:bg-red-950/10"}>
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
                        <div className="text-3xl font-bold text-text-secondary">{result.intelligence_scores.original_score}</div>
                        <div className="text-xs text-text-secondary uppercase mt-1">Original</div>
                    </div>
                    <ChevronRight className="w-6 h-6 text-border-strong" />
                    <div className="text-center">
                        <div className="text-3xl font-bold text-primary">{result.intelligence_scores.improved_score}</div>
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
                            <div className="font-medium">{result.operational_context.detected_context}</div>
                        </div>
                        <div>
                            <div className="text-sm text-text-secondary mb-1">Operational Environment</div>
                            <div className="font-medium">{result.operational_context.operational_environment}</div>
                        </div>
                        <div>
                            <div className="text-sm text-text-secondary mb-1">Current Intelligence Score</div>
                            <div className="font-medium text-primary">{result.intelligence_scores.improved_score}</div>
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
                            <Badge variant={result.diagnosis.strength === 'Broken' ? 'destructive' : result.diagnosis.strength === 'Weak' ? 'secondary' : 'default'}>
                                {result.diagnosis.strength}
                            </Badge>
                        </div>
                        {result.diagnosis.missing_elements.length > 0 && (
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
                    {result.diagnosis.execution_risks.length > 0 ? (
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
                    <Button variant="outline" size="sm" onClick={handleCopy} className="gap-2">
                        {copied ? <CheckCircle2 className="w-4 h-4 text-green-500" /> : <Copy className="w-4 h-4" />}
                        {copied ? 'Copied' : 'Copy'}
                    </Button>
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
                                {result.improvement_rationale.context_reasoning}
                            </div>
                        </div>

                        <div>
                            <div className="text-sm font-medium mb-3">Changes Made</div>
                            <ul className="space-y-2">
                                {result.improvement_rationale.changes_made.map((change, i) => (
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
                                {result.improvement_rationale.failure_modes_addressed.map((mode, i) => (
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
                                {result.improvement_rationale.expected_improvements}
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
  );
}
