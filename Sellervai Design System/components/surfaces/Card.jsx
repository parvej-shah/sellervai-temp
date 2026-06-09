import React from "react";

/** Dashboard panel with optional header (title + action) and footer. */
export function Card({ title, action, footer, children, className = "", ...rest }) {
  return (
    <section className={`sv-card ${className}`.trim()} {...rest}>
      {(title || action) && (
        <header className="sv-card-header">
          {title ? <h3 className="sv-card-title">{title}</h3> : <span />}
          {action ? <div className="sv-card-action">{action}</div> : null}
        </header>
      )}
      <div className="sv-card-body">{children}</div>
      {footer ? <footer className="sv-card-footer">{footer}</footer> : null}
    </section>
  );
}
