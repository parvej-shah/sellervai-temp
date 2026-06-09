/**
 * @startingPoint section="Forms" subtitle="Labeled input / select / textarea with error state" viewport="700x300"
 */
export interface FieldOption { value: string; label: string; }

export interface FieldProps {
  /** Field label text. */
  label?: string;
  /** Input type when `as="input"`. */
  type?: string;
  /** Which control to render. */
  as?: "input" | "select" | "textarea";
  /** Appends a muted "(optional)" marker to the label. */
  optional?: boolean;
  /** Error message — shows the invalid state and the message below. */
  error?: string;
  /** Options for `as="select"`. */
  options?: (FieldOption | string)[];
  placeholder?: string;
  className?: string;
}

export function Field(props: FieldProps): JSX.Element;
