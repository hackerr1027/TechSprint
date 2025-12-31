import { AlertTriangle, AlertCircle, Info, ShieldCheck, ExternalLink } from 'lucide-react';
import type { Warning } from '@/services/api';
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from '@/components/ui/tooltip';

interface WarningsPanelProps {
  warnings: Warning[];
}

const severityConfig = {
  error: {
    icon: AlertCircle,
    bgClass: 'bg-destructive/5 border-destructive/30 hover:border-destructive/50',
    iconClass: 'text-destructive',
    labelClass: 'bg-destructive/20 text-destructive',
    label: 'Critical',
  },
  warning: {
    icon: AlertTriangle,
    bgClass: 'bg-warning/5 border-warning/30 hover:border-warning/50',
    iconClass: 'text-warning',
    labelClass: 'bg-warning/20 text-warning',
    label: 'Warning',
  },
  info: {
    icon: Info,
    bgClass: 'bg-info/5 border-info/30 hover:border-info/50',
    iconClass: 'text-info',
    labelClass: 'bg-info/20 text-info',
    label: 'Info',
  },
};

export function WarningsPanel({ warnings }: WarningsPanelProps) {
  if (warnings.length === 0) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="flex flex-col items-center gap-4 p-8">
          <div className="relative">
            <div className="absolute inset-0 bg-success/20 rounded-full blur-xl" />
            <div className="relative w-16 h-16 rounded-xl bg-success/10 border border-success/30 flex items-center justify-center">
              <ShieldCheck className="w-8 h-8 text-success" />
            </div>
          </div>
          <div className="text-center">
            <p className="font-semibold text-foreground">All Clear</p>
            <p className="text-sm text-muted-foreground">No security or compliance issues detected</p>
          </div>
        </div>
      </div>
    );
  }

  const grouped = warnings.reduce((acc, warning) => {
    if (!acc[warning.severity]) acc[warning.severity] = [];
    acc[warning.severity].push(warning);
    return acc;
  }, {} as Record<string, Warning[]>);

  const sortedSeverities = ['error', 'warning', 'info'].filter(s => grouped[s]);

  return (
    <div className="flex flex-wrap gap-3 p-4 overflow-auto">
      {sortedSeverities.map(severity => (
        grouped[severity].map((warning, index) => {
          const config = severityConfig[severity as keyof typeof severityConfig];
          const Icon = config.icon;

          return (
            <Tooltip key={`${severity}-${index}`}>
              <TooltipTrigger asChild>
                <div
                  className={`
                    flex items-start gap-3 p-4 rounded-xl border cursor-help
                    transition-all duration-300 hover:scale-[1.02] hover-lift
                    animate-fade-in min-w-[280px] max-w-[400px]
                    ${config.bgClass}
                  `}
                  style={{ animationDelay: `${index * 80}ms` }}
                >
                  <div className={`
                    flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center
                    ${config.labelClass.replace('text-', 'bg-').replace('/20', '/10')}
                  `}>
                    <Icon className={`w-5 h-5 ${config.iconClass}`} />
                  </div>
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center gap-2 mb-1.5">
                      <span className={`px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider rounded-md ${config.labelClass}`}>
                        {config.label}
                      </span>
                      {warning.resource && (
                        <span className="text-xs text-muted-foreground font-mono truncate">
                          {warning.resource}
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-foreground leading-relaxed">{warning.message}</p>
                  </div>
                </div>
              </TooltipTrigger>
              <TooltipContent side="top" className="glass-strong border-primary/20 max-w-sm p-4">
                <div className="flex items-start gap-2 mb-2">
                  <ExternalLink className="w-4 h-4 text-primary mt-0.5" />
                  <p className="font-semibold text-foreground">Recommendation</p>
                </div>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  {warning.recommendation || getDefaultRecommendation(warning)}
                </p>
              </TooltipContent>
            </Tooltip>
          );
        })
      ))}
    </div>
  );
}

function getDefaultRecommendation(warning: Warning): string {
  const recommendations: Record<string, string> = {
    'security': 'This could expose your infrastructure to unauthorized access. Review and restrict permissions.',
    'compliance': 'This may violate regulatory requirements. Ensure your infrastructure meets compliance standards.',
    'cost': 'This configuration may lead to unexpected costs. Consider optimizing resource allocation.',
    'performance': 'This may impact application performance. Consider reviewing resource sizing.',
  };

  const key = Object.keys(recommendations).find(k => 
    warning.message.toLowerCase().includes(k)
  );

  return key 
    ? recommendations[key] 
    : 'Review this finding and take appropriate action to maintain infrastructure best practices.';
}
