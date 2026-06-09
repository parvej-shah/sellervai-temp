import React from "react";

const ICONS = { success: "circle-check", warning: "alert-triangle", danger: "alert-circle", info: "info-circle" };

/** Inline alert / toast in one of the four semantic tones. */
export function Alert({ tone = "info", title, icon, children, className = "" }) {
  return (
    <div className={`sv-alert sv-alert-${tone} ${className}`.trim()} role="alert">
      <i className={`ti ti-${icon ?? ICONS[tone]}`} aria-hidden="true" />
      <div>
        {title ? <p className="sv-alert-title">{title}</p> : null}
        {children ? <p>{children}</p> : null}
      </div>
    </div>
  );
}
