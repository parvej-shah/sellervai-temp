import React from "react";

const ICONS = { success: "circle-check", warning: "alert-triangle", danger: "alert-circle", info: "info-circle", neutral: "" };

/**
 * Semantic status pill — online / paid / pending / failed. Uses semantic
 * color tokens ONLY (never brand indigo/purple). Set `live` for the
 * pulsing "AI online" dot.
 */
export function StatusPill({ tone = "neutral", dot = false, live = false, icon, children, className = "" }) {
  const glyph = icon ?? (!dot ? ICONS[tone] : "");
  return (
    <span className={`sv-pill sv-pill-${tone} ${className}`.trim()}>
      {dot ? <span className={`sv-dot${live ? " is-live" : ""}`} /> : null}
      {glyph ? <i className={`ti ti-${glyph}`} aria-hidden="true" /> : null}
      {children}
    </span>
  );
}
