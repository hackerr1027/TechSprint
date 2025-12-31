import { Activity, CheckCircle2, AlertCircle, Loader2, Wifi, WifiOff } from 'lucide-react';
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from '@/components/ui/tooltip';

interface StatusIndicatorProps {
  type: 'health' | 'sync';
  status: 'healthy' | 'unhealthy' | 'synced' | 'syncing' | 'error';
  label?: string;
}

const statusConfig = {
  healthy: {
    icon: Wifi,
    className: 'text-success',
    dotClass: 'status-dot status-healthy',
    label: 'Backend Connected',
    bgClass: 'bg-success/10 border-success/30',
  },
  unhealthy: {
    icon: WifiOff,
    className: 'text-destructive',
    dotClass: 'status-dot status-error',
    label: 'Backend Disconnected',
    bgClass: 'bg-destructive/10 border-destructive/30',
  },
  synced: {
    icon: CheckCircle2,
    className: 'text-success',
    dotClass: 'status-dot status-healthy',
    label: 'In Sync',
    bgClass: 'bg-success/10 border-success/30',
  },
  syncing: {
    icon: Loader2,
    className: 'text-warning animate-spin',
    dotClass: 'status-dot status-syncing',
    label: 'Syncing...',
    bgClass: 'bg-warning/10 border-warning/30',
  },
  error: {
    icon: AlertCircle,
    className: 'text-destructive',
    dotClass: 'status-dot status-error',
    label: 'Sync Error',
    bgClass: 'bg-destructive/10 border-destructive/30',
  },
};

export function StatusIndicator({ type, status, label }: StatusIndicatorProps) {
  const config = statusConfig[status];
  const Icon = config.icon;

  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <div className={`
          flex items-center gap-2.5 px-3 py-2 rounded-xl border cursor-help
          transition-all duration-300 hover:scale-105
          ${config.bgClass}
        `}>
          {type === 'health' && <Activity className="w-3.5 h-3.5 text-muted-foreground" />}
          <div className={`${config.dotClass} ring-2 ring-offset-1 ring-offset-background`} 
               style={{ 
                 '--tw-ring-color': status === 'healthy' || status === 'synced' 
                   ? 'hsl(var(--success) / 0.3)' 
                   : status === 'syncing' 
                     ? 'hsl(var(--warning) / 0.3)' 
                     : 'hsl(var(--destructive) / 0.3)' 
               } as React.CSSProperties} 
          />
          <span className="text-xs font-semibold text-foreground tracking-wide">
            {label || config.label}
          </span>
        </div>
      </TooltipTrigger>
      <TooltipContent className="glass-strong border-primary/20">
        <div className="flex items-center gap-2">
          <Icon className={`w-4 h-4 ${config.className}`} />
          <span className="font-medium">{config.label}</span>
        </div>
        {type === 'health' && status === 'unhealthy' && (
          <p className="text-xs text-muted-foreground mt-1.5 max-w-[200px]">
            Running in demo mode. Connect backend for full functionality.
          </p>
        )}
      </TooltipContent>
    </Tooltip>
  );
}
