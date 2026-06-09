export interface StatTileProps {
  /** Uppercase metric label, e.g. "Conversations today". */
  label: string;
  /** The headline figure (string or number). Rendered with tabular figures. */
  value: React.ReactNode;
  /** Tabler icon name (without `ti-`) shown top-right. */
  icon?: string;
  /** Trend value, e.g. "+12%". */
  delta?: string;
  /** Direction of the delta — colors it success/danger. */
  trend?: "up" | "down";
  className?: string;
}

export function StatTile(props: StatTileProps): JSX.Element;
