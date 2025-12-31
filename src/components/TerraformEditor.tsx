import { useEffect, useState } from 'react';
import Editor from '@monaco-editor/react';
import { Loader2 } from 'lucide-react';

interface TerraformEditorProps {
  code: string;
  onChange: (value: string) => void;
  readOnly?: boolean;
}

export function TerraformEditor({ code, onChange, readOnly = false }: TerraformEditorProps) {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Monaco editor loaded
    setIsLoading(false);
  }, []);

  return (
    <div className="h-full w-full relative">
      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center bg-code-bg z-10">
          <Loader2 className="w-8 h-8 animate-spin text-primary" />
        </div>
      )}
      <Editor
        height="100%"
        defaultLanguage="hcl"
        language="hcl"
        theme="vs-dark"
        value={code}
        onChange={(value) => onChange(value || '')}
        onMount={() => setIsLoading(false)}
        options={{
          readOnly,
          minimap: { enabled: false },
          fontSize: 13,
          fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
          lineNumbers: 'on',
          scrollBeyondLastLine: false,
          automaticLayout: true,
          padding: { top: 16, bottom: 16 },
          wordWrap: 'on',
          tabSize: 2,
          renderLineHighlight: 'line',
          cursorBlinking: 'smooth',
          smoothScrolling: true,
          bracketPairColorization: { enabled: true },
          guides: {
            bracketPairs: true,
            indentation: true,
          },
        }}
      />
    </div>
  );
}
