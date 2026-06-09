/**
 * @startingPoint section="Feedback" subtitle="Inline alerts in four semantic tones" viewport="700x260"
 */
export interface AlertProps {
  /** Semantic tone — sets color + default icon. */
  tone?: "success" | "warning" | "danger" | "info";
  /** Bold first line. */
  title?: React.ReactNode;
  /** Override the default Tabler icon (without `ti-`). */
  icon?: string;
  className?: string;
  children?: React.ReactNode;
}

export function Alert(props: AlertProps): JSX.Element;
