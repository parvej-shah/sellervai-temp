export interface PlatformChipProps {
  /** Which messaging platform. Tints the icon with its brand color. */
  platform: "whatsapp" | "messenger" | "instagram" | "telegram";
  /** Override the default label (e.g. the connected page/account name). */
  label?: string;
  className?: string;
}

export function PlatformChip(props: PlatformChipProps): JSX.Element;
