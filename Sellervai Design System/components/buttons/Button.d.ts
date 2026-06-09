import React from "react";

/**
 * @startingPoint section="Buttons" subtitle="Primary, secondary, ghost, danger + hero CTA" viewport="700x220"
 */
export interface ButtonProps {
  /** Visual hierarchy. `hero` (gradient + glow) is for brand moments only. */
  variant?: "primary" | "secondary" | "ghost" | "danger" | "hero";
  size?: "sm" | "md" | "lg";
  /** Tabler icon name without the `ti-` prefix, e.g. "rocket". */
  icon?: string;
  /** Trailing Tabler icon name. */
  iconRight?: string;
  /** Shows Pico's aria-busy spinner and disables the button. */
  busy?: boolean;
  disabled?: boolean;
  /** Render as a different element, e.g. "a" for links. */
  as?: "button" | "a";
  className?: string;
  children?: React.ReactNode;
}

export function Button(props: ButtonProps): JSX.Element;
