import React from "react";

/** Centered empty state for zero-data tables, inboxes, product lists. */
export function EmptyState({ icon = "inbox", title, children, action, className = "" }) {
  return (
    <div className={`sv-empty ${className}`.trim()}>
      <span className="sv-empty-icon"><i className={`ti ti-${icon}`} aria-hidden="true" /></span>
      {title ? <h3>{title}</h3> : null}
      {children ? <p>{children}</p> : null}
      {action ? <div>{action}</div> : null}
    </div>
  );
}
