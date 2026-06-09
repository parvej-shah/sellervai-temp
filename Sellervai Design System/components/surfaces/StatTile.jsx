import React from "react";

/** Single dashboard metric — label, big value, optional icon + trend delta. */
export function StatTile({ label, value, icon, delta, trend, className = "" }) {
  return (
    <article className={`sv-stat ${className}`.trim()}>
      <div className="sv-stat-head">
        <span className="sv-stat-label">{label}</span>
        {icon ? <span className="sv-stat-icon"><i className={`ti ti-${icon}`} aria-hidden="true" /></span> : null}
      </div>
      <div className="sv-stat-value sv-tnum">{value}</div>
      {delta ? (
        <span className={`sv-stat-delta ${trend === "down" ? "is-down" : "is-up"}`}>
          <i className={`ti ti-${trend === "down" ? "trending-down" : "trending-up"}`} aria-hidden="true" />
          {delta}
        </span>
      ) : null}
    </article>
  );
}
