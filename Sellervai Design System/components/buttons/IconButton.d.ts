export interface IconButtonProps {
  /** Tabler icon name without the `ti-` prefix, e.g. "dots-vertical". */
  icon: string;
  /** Accessible label (also used as tooltip). */
  label: string;
  className?: string;
}

export function IconButton(props: IconButtonProps): JSX.Element;
