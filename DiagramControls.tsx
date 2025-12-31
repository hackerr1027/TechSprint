import { useState } from 'react';
import { Plus, Minus, Move, Server, Database, Globe, Shield, Box, Settings2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from '@/components/ui/tooltip';
import { Input } from '@/components/ui/input';
import type { DiagramEditEvent } from '@/services/api';

interface DiagramControlsProps {
  onEdit: (event: DiagramEditEvent) => void;
  disabled?: boolean;
}

const resourceTypes = [
  { value: 'ec2', label: 'EC2 Instance', icon: Server, description: 'Virtual server in the cloud', color: 'text-info' },
  { value: 'rds', label: 'RDS Database', icon: Database, description: 'Managed relational database', color: 'text-accent' },
  { value: 'elb', label: 'Load Balancer', icon: Globe, description: 'Distributes incoming traffic', color: 'text-success' },
  { value: 's3', label: 'S3 Bucket', icon: Box, description: 'Object storage service', color: 'text-warning' },
  { value: 'security_group', label: 'Security Group', icon: Shield, description: 'Virtual firewall for resources', color: 'text-destructive' },
];

const subnetOptions = [
  { value: 'public', label: 'Public Subnet', color: 'bg-success/20 text-success' },
  { value: 'private', label: 'Private Subnet', color: 'bg-warning/20 text-warning' },
  { value: 'database', label: 'Database Subnet', color: 'bg-accent/20 text-accent' },
];

export function DiagramControls({ onEdit, disabled = false }: DiagramControlsProps) {
  const [selectedResource, setSelectedResource] = useState('ec2');
  const [resourceId, setResourceId] = useState('');
  const [targetSubnet, setTargetSubnet] = useState('public');
  const [activeAction, setActiveAction] = useState<'add' | 'remove' | 'move' | null>(null);

  // Helper function to get default properties for each resource type
  const getDefaultProperties = (resourceType: string): Record<string, any> => {
    switch (resourceType) {
      case 'ec2':
        return {
          subnet_id: 'subnet-public-1',
          instance_type: 't2.micro'
        };
      case 'rds':
        return {
          subnet_ids: ['subnet-private-1', 'subnet-private-2'],
          engine: 'postgres',
          instance_class: 'db.t3.micro'
        };
      case 'elb':
      case 'load_balancer':
        return {
          subnet_ids: ['subnet-public-1'],
          target_instance_ids: []
        };
      case 's3':
        return {};
      case 'security_group':
        return {
          vpc_id: 'vpc-main'
        };
      default:
        return {};
    }
  };

  const handleAction = (action: 'add' | 'remove' | 'move') => {
    if (activeAction === action) {
      const event: DiagramEditEvent = {
        action,
        resourceType: selectedResource,
        resourceId: resourceId || undefined,
        targetSubnet: action === 'move' ? targetSubnet : undefined,
        properties: action === 'add' ? getDefaultProperties(selectedResource) : undefined,
      };
      onEdit(event);
      setResourceId('');
      setActiveAction(null);
    } else {
      setActiveAction(action);
    }
  };

  const selectedResourceInfo = resourceTypes.find(r => r.value === selectedResource);

  return (
    <div className="flex flex-col gap-4 p-4 bg-secondary/20 rounded-xl border border-border/50 hover:border-primary/30 transition-all duration-300">
      <div className="flex items-center gap-2">
        <div className="flex items-center justify-center w-6 h-6 rounded-md bg-primary/10 border border-primary/20">
          <Settings2 className="w-3.5 h-3.5 text-primary" />
        </div>
        <span className="text-sm font-semibold text-foreground">Diagram Controls</span>
        <Tooltip>
          <TooltipTrigger>
            <span className="px-1.5 py-0.5 text-[10px] font-bold rounded bg-muted text-muted-foreground cursor-help">?</span>
          </TooltipTrigger>
          <TooltipContent className="glass-strong border-primary/20 max-w-[250px]">
            <p className="text-sm">Modify your infrastructure visually. Changes sync with Terraform automatically.</p>
          </TooltipContent>
        </Tooltip>
      </div>

      {/* Resource Type Selector */}
      <div className="space-y-2">
        <label className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Resource Type</label>
        <Select value={selectedResource} onValueChange={setSelectedResource} disabled={disabled}>
          <SelectTrigger className="w-full bg-background/50 border-border/50 hover:border-primary/30 transition-all duration-300">
            <SelectValue />
          </SelectTrigger>
          <SelectContent className="glass-strong border-primary/20">
            {resourceTypes.map(resource => {
              const Icon = resource.icon;
              return (
                <SelectItem key={resource.value} value={resource.value} className="focus:bg-primary/10">
                  <div className="flex items-center gap-3">
                    <Icon className={`w-4 h-4 ${resource.color}`} />
                    <span className="font-medium">{resource.label}</span>
                  </div>
                </SelectItem>
              );
            })}
          </SelectContent>
        </Select>
        {selectedResourceInfo && (
          <p className="text-xs text-muted-foreground flex items-center gap-2">
            <selectedResourceInfo.icon className={`w-3 h-3 ${selectedResourceInfo.color}`} />
            {selectedResourceInfo.description}
          </p>
        )}
      </div>

      {/* Resource ID for remove/move */}
      {(activeAction === 'remove' || activeAction === 'move') && (
        <div className="space-y-2 animate-fade-in">
          <label className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Resource ID</label>
          <Input
            placeholder="e.g., web-server-1"
            value={resourceId}
            onChange={(e) => setResourceId(e.target.value)}
            disabled={disabled}
            className="bg-background/50 border-border/50 focus:border-primary/50 transition-all duration-300"
          />
        </div>
      )}

      {/* Target Subnet for move */}
      {activeAction === 'move' && (
        <div className="space-y-2 animate-fade-in">
          <label className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Target Subnet</label>
          <Select value={targetSubnet} onValueChange={setTargetSubnet} disabled={disabled}>
            <SelectTrigger className="w-full bg-background/50 border-border/50 hover:border-primary/30 transition-all duration-300">
              <SelectValue />
            </SelectTrigger>
            <SelectContent className="glass-strong border-primary/20">
              {subnetOptions.map(subnet => (
                <SelectItem key={subnet.value} value={subnet.value} className="focus:bg-primary/10">
                  <span className={`px-2 py-0.5 rounded-md text-xs font-medium ${subnet.color}`}>
                    {subnet.label}
                  </span>
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex gap-2 mt-1">
        <Tooltip>
          <TooltipTrigger asChild>
            <Button
              variant={activeAction === 'add' ? 'generate' : 'panel'}
              size="sm"
              onClick={() => handleAction('add')}
              disabled={disabled}
              className="flex-1 group"
            >
              <Plus className={`w-4 h-4 transition-transform duration-300 ${activeAction === 'add' ? 'rotate-45' : 'group-hover:scale-110'}`} />
              {activeAction === 'add' ? 'Confirm' : 'Add'}
            </Button>
          </TooltipTrigger>
          <TooltipContent className="glass-strong border-primary/20">Add a new resource</TooltipContent>
        </Tooltip>

        <Tooltip>
          <TooltipTrigger asChild>
            <Button
              variant={activeAction === 'remove' ? 'destructive' : 'panel'}
              size="sm"
              onClick={() => handleAction('remove')}
              disabled={disabled}
              className="flex-1 group"
            >
              <Minus className={`w-4 h-4 transition-transform duration-300 ${activeAction === 'remove' ? 'scale-125' : 'group-hover:scale-110'}`} />
              {activeAction === 'remove' ? 'Confirm' : 'Remove'}
            </Button>
          </TooltipTrigger>
          <TooltipContent className="glass-strong border-primary/20">Remove a resource</TooltipContent>
        </Tooltip>

        <Tooltip>
          <TooltipTrigger asChild>
            <Button
              variant={activeAction === 'move' ? 'apply' : 'panel'}
              size="sm"
              onClick={() => handleAction('move')}
              disabled={disabled}
              className="flex-1 group"
            >
              <Move className={`w-4 h-4 transition-transform duration-300 ${activeAction === 'move' ? 'translate-x-1' : 'group-hover:scale-110'}`} />
              {activeAction === 'move' ? 'Confirm' : 'Move'}
            </Button>
          </TooltipTrigger>
          <TooltipContent className="glass-strong border-primary/20">Move to another subnet</TooltipContent>
        </Tooltip>
      </div>

      {activeAction && (
        <Button
          variant="ghost"
          size="sm"
          onClick={() => setActiveAction(null)}
          className="text-muted-foreground hover:text-foreground hover:bg-destructive/10 transition-all duration-300"
        >
          Cancel
        </Button>
      )}
    </div>
  );
}
