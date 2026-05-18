import { ReactNode } from "react";
import { Button } from "@/components/ui/button";

interface AuditFormStepProps {
  title: string;
  description?: string;
  currentStep: number;
  totalSteps: number;
  children: ReactNode;
  onNext?: () => void;
  onPrev?: () => void;
  onSubmit?: () => void;
  isNextDisabled?: boolean;
}

export function AuditFormStep({
  title,
  description,
  currentStep,
  totalSteps,
  children,
  onNext,
  onPrev,
  onSubmit,
  isNextDisabled = false,
}: AuditFormStepProps) {
  return (
    <div className="max-w-2xl mx-auto py-8">
      <div className="mb-8">
        <div className="text-sm text-slate-500 mb-2">
          Step {currentStep} of {totalSteps}
        </div>
        <div className="w-full bg-slate-200 rounded-full h-2 mb-6">
          <div
            className="bg-slate-900 h-2 rounded-full transition-all"
            style={{ width: `${(currentStep / totalSteps) * 100}%` }}
          />
        </div>
        <h2 className="text-2xl font-bold text-slate-900">{title}</h2>
        {description && <p className="mt-2 text-slate-600">{description}</p>}
      </div>

      <div className="space-y-6 bg-white p-6 rounded-lg border border-slate-200 shadow-sm">
        {children}
      </div>

      <div className="mt-8 flex justify-between">
        <Button
          variant="outline"
          onClick={onPrev}
          disabled={currentStep === 1}
          className={currentStep === 1 ? 'invisible' : ''}
        >
          Previous
        </Button>

        {currentStep < totalSteps ? (
          <Button onClick={onNext} disabled={isNextDisabled}>
            Next
          </Button>
        ) : (
          <Button onClick={onSubmit} disabled={isNextDisabled}>
            Submit Audit
          </Button>
        )}
      </div>
    </div>
  );
}
