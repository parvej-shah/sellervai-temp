/**
 * @startingPoint section="Badges" subtitle="Semantic status pills — online, paid, pending, failed" viewport="700x140"
 */
export interface StatusPillProps {
  /** Semantic tone. NEVER use brand indigo/purple for status. */
  tone?: "success" | "warning" | "danger" | "info" | "neutral";
  /** Show a leading colored dot instead of an icon. */
  dot?: boolean;
  /** Animate the dot (use for the live "AI online" indicator). */
  live?: boolean;
  /** Override the auto-selected Tabler icon (without `ti-`). */
  icon?: string;
  className?: string;
  children?: React.ReactNode;
}

export function StatusPill(props: StatusPillProps): JSX.Element;
