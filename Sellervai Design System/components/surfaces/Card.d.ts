/**
 * @startingPoint section="Surfaces" subtitle="Dashboard panel with header, body, footer" viewport="700x260"
 */
export interface CardProps {
  /** Header title. Omit (with no action) to render a borderless body-only card. */
  title?: React.ReactNode;
  /** Right-aligned header content, e.g. a Button or IconButton. */
  action?: React.ReactNode;
  /** Footer content (rendered on the tinted footer bar). */
  footer?: React.ReactNode;
  className?: string;
  children?: React.ReactNode;
}

export function Card(props: CardProps): JSX.Element;
