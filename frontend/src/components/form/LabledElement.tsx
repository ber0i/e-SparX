export interface LabeledElementProps {
  label: string;
  error?: string;
  children: React.ReactElement<HTMLFormElement>;
}

export default function LabeledElement({
  label,
  error,
  children,
}: LabeledElementProps) {
  return (
    <div className="flex flex-col">
      <div className="flex flex-row gap-2 items-center">
        <label className="h-fit">{label}</label>
        {children}
      </div>
      {error ? <span className="self-end text-brand-red">{error}</span> : ""}
    </div>
  );
}
