import React from "react";

const META = {
  whatsapp:  { icon: "brand-whatsapp",  label: "WhatsApp" },
  messenger: { icon: "brand-messenger", label: "Messenger" },
  instagram: { icon: "brand-instagram", label: "Instagram" },
  telegram:  { icon: "brand-telegram",  label: "Telegram" },
};

/**
 * Compact platform connection chip, tinted with the platform brand color.
 * For the full connect/disconnect surface use the `.sv-platform` card.
 */
export function PlatformChip({ platform, label, className = "" }) {
  const meta = META[platform] || META.whatsapp;
  return (
    <span className={`sv-chip sv-chip-${platform} ${className}`.trim()}>
      <i className={`sv-chip-icon ti ti-${meta.icon}`} aria-hidden="true" />
      {label ?? meta.label}
    </span>
  );
}
