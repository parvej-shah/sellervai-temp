import React from "react";

/**
 * Sellervai button. One indigo-solid `primary` action per view; everything
 * else is `secondary` / `ghost`. The gradient + glow `hero` variant is
 * reserved for marketing brand moments only.
 */
export function Button({
  variant = "primary",
  size = "md",
  icon,
  iconRight,
  busy = false,
  disabled = false,
  as = "button",
  children,
  className = "",
  ...rest
}) {
  const Tag = as;
  const cls = [
    "sv-btn",
    `sv-btn-${variant}`,
    size === "sm" ? "sv-btn-sm" : size === "lg" ? "sv-btn-lg" : "",
    className,
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <Tag
      className={cls}
      disabled={Tag === "button" ? disabled || busy : undefined}
      aria-disabled={Tag !== "button" && (disabled || busy) ? "true" : undefined}
      aria-busy={busy ? "true" : undefined}
      {...rest}
    >
      {icon && !busy ? <i className={`ti ti-${icon}`} aria-hidden="true" /> : null}
      {children}
      {iconRight && !busy ? <i className={`ti ti-${iconRight}`} aria-hidden="true" /> : null}
    </Tag>
  );
}
