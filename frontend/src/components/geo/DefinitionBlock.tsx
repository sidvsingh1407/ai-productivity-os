

interface DefinitionBlockProps {
  question: string;
  answer: string;
}

export function DefinitionBlock({ question, answer }: DefinitionBlockProps) {
  return (
    <div className="bg-[#F8FAFC] border border-[#E2E8F0] rounded-[12px] p-6 mb-8 mt-4 shadow-sm animate-fade-up">
      <p className="text-[10px] font-mono tracking-wider text-text-secondary uppercase mb-3 font-semibold">
        Definition
      </p>
      <h3 className="text-h3 text-text-primary mb-3">
        {question}
      </h3>
      <p className="text-body text-text-primary leading-relaxed">
        {answer}
      </p>
    </div>
  );
}
