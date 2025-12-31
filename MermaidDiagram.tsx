import { useEffect, useRef, useState } from 'react';
import mermaid from 'mermaid';
import { Loader2, Network, Sparkles } from 'lucide-react';

// Initialize mermaid with custom dark theme
mermaid.initialize({
  startOnLoad: false,
  theme: 'dark',
  themeVariables: {
    primaryColor: '#00d4ff',
    primaryTextColor: '#f0f9ff',
    primaryBorderColor: '#00d4ff',
    lineColor: '#64748b',
    secondaryColor: '#3b1d5e',
    tertiaryColor: '#0a0f1a',
    background: '#080c14',
    mainBkg: '#1a1033',
    secondBkg: '#0f0a1a',
    fontFamily: 'Space Grotesk, sans-serif',
    fontSize: '14px',
    nodeBorder: '#00d4ff',
    clusterBkg: 'rgba(59, 29, 94, 0.3)',
    clusterBorder: 'rgba(0, 212, 255, 0.3)',
    edgeLabelBackground: '#080c14',
  },
  flowchart: {
    htmlLabels: true,
    curve: 'basis',
    padding: 20,
    nodeSpacing: 50,
    rankSpacing: 70,
  },
});

interface MermaidDiagramProps {
  code: string;
  className?: string;
}

export function MermaidDiagram({ code, className = '' }: MermaidDiagramProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [svgContent, setSvgContent] = useState<string>('');
  const [isRendering, setIsRendering] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const renderDiagram = async () => {
      console.log('=== MermaidDiagram Render Start ===');
      console.log('Code length:', code?.length);
      console.log('Container ref exists:', !!containerRef.current);

      if (!code.trim()) {
        console.log('No code to render');
        setSvgContent('');
        setIsRendering(false);
        return;
      }

      setIsRendering(true);
      setError(null);
      setSvgContent(''); // Clear old content

      try {
        const id = `mermaid-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
        console.log('Rendering with ID:', id);

        const { svg } = await mermaid.render(id, code);

        console.log('✅ Mermaid render SUCCESS!');
        console.log('SVG length:', svg.length);
        console.log('SVG preview:', svg.substring(0, 200));

        // Store SVG in state to trigger re-render
        setSvgContent(svg);
        console.log('✅ SVG content set in state');

      } catch (err) {
        console.error('❌ Mermaid render FAILED:', err);
        console.error('Failed code:', code);
        setError(err instanceof Error ? err.message : 'Failed to render diagram');
        setSvgContent('');
      } finally {
        setIsRendering(false);
      }
    };

    renderDiagram();
  }, [code]);

  // Update container with SVG after state changes
  useEffect(() => {
    if (svgContent && containerRef.current) {
      console.log('📦 Inserting SVG into container...');
      console.log('Container exists:', !!containerRef.current);
      containerRef.current.innerHTML = svgContent;
      console.log('✅ SVG INSERTED into DOM!');

      // Force browser to recognize the SVG
      const svgElement = containerRef.current.querySelector('svg');
      if (svgElement) {
        console.log('✅ SVG element found in DOM');
        console.log('SVG dimensions:', svgElement.getBoundingClientRect());
        // Ensure SVG is visible
        svgElement.style.maxWidth = '100%';
        svgElement.style.height = 'auto';
        svgElement.style.display = 'block';
      } else {
        console.error('❌ SVG element NOT found after insertion!');
      }
    }
  }, [svgContent]);

  if (!code.trim()) {
    return (
      <div className={`flex flex-col items-center justify-center h-full text-muted-foreground gap-6 p-8 ${className}`}>
        <div className="relative">
          <div className="absolute inset-0 bg-primary/20 rounded-full blur-2xl animate-pulse-subtle" />
          <div className="relative w-24 h-24 rounded-2xl bg-gradient-to-br from-primary/10 to-accent/10 border border-primary/20 flex items-center justify-center">
            <Network className="w-12 h-12 text-primary/50" />
          </div>
        </div>
        <div className="text-center space-y-2 max-w-xs">
          <p className="text-lg font-semibold text-foreground/80">No Infrastructure Yet</p>
          <p className="text-sm text-muted-foreground">
            Enter a description and click <span className="text-primary font-medium">Generate</span>
          </p>
        </div>
        <div className="flex items-center gap-2 px-4 py-2 rounded-full bg-primary/5 border border-primary/10">
          <Sparkles className="w-4 h-4 text-primary" />
          <span className="text-xs text-muted-foreground">Powered by AI</span>
        </div>
      </div>
    );
  }

  if (isRendering) {
    return (
      <div className={`flex flex-col items-center justify-center h-full gap-4 ${className}`}>
        <div className="relative">
          <div className="absolute inset-0 bg-primary/30 rounded-full blur-xl animate-pulse" />
          <div className="relative w-16 h-16 rounded-xl bg-primary/10 border border-primary/30 flex items-center justify-center">
            <Loader2 className="w-8 h-8 animate-spin text-primary" />
          </div>
        </div>
        <p className="text-sm text-muted-foreground animate-pulse">Rendering diagram...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`flex items-center justify-center h-full ${className}`}>
        <div className="text-center p-6 rounded-xl bg-destructive/5 border border-destructive/20 max-w-md">
          <p className="font-semibold text-destructive mb-2">Diagram Error</p>
          <p className="text-sm text-muted-foreground">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`w-full h-full p-6 overflow-auto ${className}`}>
      <div
        ref={containerRef}
        className="w-full min-h-full flex items-center justify-center"
        style={{
          minHeight: '600px',
        }}
      />
    </div>
  );
}
