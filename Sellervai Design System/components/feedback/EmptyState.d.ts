export interface EmptyStateProps {
  /** Tabler icon name (without `ti-`). Default "inbox". */
  icon?: string;
  /** Headline, e.g. "No conversations yet". */
  title?: string;
  /** Right place for a primary Button. */
  action?: React.ReactNode;
  className?: string;
  children?: React.ReactNode;
}

export function EmptyState(props: EmptyStateProps): JSX.Element;
