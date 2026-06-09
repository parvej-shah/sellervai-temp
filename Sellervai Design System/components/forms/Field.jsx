import React from "react";

/**
 * Labeled form control built on Pico inputs. Renders an input, select, or
 * textarea with optional "(optional)" marker and inline error state.
 */
export function Field({
  label,
  type = "text",
  as = "input",
  optional = false,
  error,
  options = [],
  className = "",
  ...rest
}) {
  const invalid = Boolean(error);
  const controlCls = `sv-input${invalid ? " is-invalid" : ""}`;
  return (
    <label className={`sv-field ${className}`.trim()}>
      {label ? (
        <span className="sv-field-label">
          {label}
          {optional ? <span className="sv-optional"> (optional)</span> : null}
        </span>
      ) : null}
      {as === "select" ? (
        <select className={controlCls} aria-invalid={invalid || undefined} {...rest}>
          {options.map((o) => (
            <option key={o.value ?? o} value={o.value ?? o}>{o.label ?? o}</option>
          ))}
        </select>
      ) : as === "textarea" ? (
        <textarea className={controlCls} aria-invalid={invalid || undefined} {...rest} />
      ) : (
        <input type={type} className={controlCls} aria-invalid={invalid || undefined} {...rest} />
      )}
      {error ? <p className="sv-field-error">{error}</p> : null}
    </label>
  );
}
