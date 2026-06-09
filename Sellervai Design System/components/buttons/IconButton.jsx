import React from "react";

/** Square icon-only button for table rows, card headers, toolbars. */
export function IconButton({ icon, label, className = "", ...rest }) {
  return (
    <button
      type="button"
      className={`sv-icon-btn ${className}`.trim()}
      aria-label={label}
      title={label}
      {...rest}
    >
      <i className={`ti ti-${icon}`} aria-hidden="true" />
    </button>
  );
}
