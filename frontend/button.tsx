import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";

import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-xl text-sm font-semibold ring-offset-background transition-all duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90 shadow-glow-sm hover:shadow-glow",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90 shadow-[0_0_15px_hsl(var(--destructive)/0.3)] hover:shadow-[0_0_25px_hsl(var(--destructive)/0.4)]",
        outline: "border border-border/50 bg-transparent hover:bg-primary/10 hover:border-primary/50 hover:text-primary",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80 border border-border/30",
        ghost: "hover:bg-secondary/50 hover:text-foreground",
        link: "text-primary underline-offset-4 hover:underline",
        // Custom variants for infrastructure app
        generate: "bg-gradient-to-r from-primary to-accent text-primary-foreground font-bold hover:opacity-90 shadow-glow hover:shadow-glow-lg border border-primary/30",
        apply: "bg-success text-success-foreground font-semibold hover:bg-success/90 shadow-[0_0_15px_hsl(var(--success)/0.3)] hover:shadow-[0_0_25px_hsl(var(--success)/0.4)]",
        panel: "bg-secondary/30 text-foreground border border-border/50 hover:bg-secondary/50 hover:border-primary/30 hover:shadow-glow-sm",
        icon: "bg-transparent hover:bg-secondary/50 text-muted-foreground hover:text-primary",
      },
      size: {
        default: "h-11 px-5 py-2.5",
        sm: "h-9 rounded-lg px-4 text-xs",
        lg: "h-12 rounded-xl px-8 text-base",
        icon: "h-10 w-10",
        "icon-sm": "h-8 w-8",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button";
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    );
  }
);
Button.displayName = "Button";

export { Button, buttonVariants };
