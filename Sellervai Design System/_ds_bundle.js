/* @ds-bundle: {"format":3,"namespace":"SellervaiDesignSystem_76e02e","components":[{"name":"PlatformChip","sourcePath":"components/badges/PlatformChip.jsx"},{"name":"StatusPill","sourcePath":"components/badges/StatusPill.jsx"},{"name":"Button","sourcePath":"components/buttons/Button.jsx"},{"name":"IconButton","sourcePath":"components/buttons/IconButton.jsx"},{"name":"Alert","sourcePath":"components/feedback/Alert.jsx"},{"name":"EmptyState","sourcePath":"components/feedback/EmptyState.jsx"},{"name":"Field","sourcePath":"components/forms/Field.jsx"},{"name":"Card","sourcePath":"components/surfaces/Card.jsx"},{"name":"StatTile","sourcePath":"components/surfaces/StatTile.jsx"}],"sourceHashes":{"components/badges/PlatformChip.jsx":"972c17312680","components/badges/StatusPill.jsx":"4072974ef7da","components/buttons/Button.jsx":"5c776cd24670","components/buttons/IconButton.jsx":"39fa735834e9","components/feedback/Alert.jsx":"a4c4bc1d5dd7","components/feedback/EmptyState.jsx":"7c1bfa269ca1","components/forms/Field.jsx":"da8e86c36cad","components/surfaces/Card.jsx":"a3518580e7d4","components/surfaces/StatTile.jsx":"01da470f7d2a","ui_kits/dashboard/screens.jsx":"9e7ae2a4dacd","ui_kits/marketing/screens.jsx":"18db1d50a776","ui_kits/store_detail/screens.jsx":"9750ee21dc41"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.SellervaiDesignSystem_76e02e = window.SellervaiDesignSystem_76e02e || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/badges/PlatformChip.jsx
try { (() => {
const META = {
  whatsapp: {
    icon: "brand-whatsapp",
    label: "WhatsApp"
  },
  messenger: {
    icon: "brand-messenger",
    label: "Messenger"
  },
  instagram: {
    icon: "brand-instagram",
    label: "Instagram"
  },
  telegram: {
    icon: "brand-telegram",
    label: "Telegram"
  }
};

/**
 * Compact platform connection chip, tinted with the platform brand color.
 * For the full connect/disconnect surface use the `.sv-platform` card.
 */
function PlatformChip({
  platform,
  label,
  className = ""
}) {
  const meta = META[platform] || META.whatsapp;
  return /*#__PURE__*/React.createElement("span", {
    className: `sv-chip sv-chip-${platform} ${className}`.trim()
  }, /*#__PURE__*/React.createElement("i", {
    className: `sv-chip-icon ti ti-${meta.icon}`,
    "aria-hidden": "true"
  }), label ?? meta.label);
}
Object.assign(__ds_scope, { PlatformChip });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/badges/PlatformChip.jsx", error: String((e && e.message) || e) }); }

// components/badges/StatusPill.jsx
try { (() => {
const ICONS = {
  success: "circle-check",
  warning: "alert-triangle",
  danger: "alert-circle",
  info: "info-circle",
  neutral: ""
};

/**
 * Semantic status pill — online / paid / pending / failed. Uses semantic
 * color tokens ONLY (never brand indigo/purple). Set `live` for the
 * pulsing "AI online" dot.
 */
function StatusPill({
  tone = "neutral",
  dot = false,
  live = false,
  icon,
  children,
  className = ""
}) {
  const glyph = icon ?? (!dot ? ICONS[tone] : "");
  return /*#__PURE__*/React.createElement("span", {
    className: `sv-pill sv-pill-${tone} ${className}`.trim()
  }, dot ? /*#__PURE__*/React.createElement("span", {
    className: `sv-dot${live ? " is-live" : ""}`
  }) : null, glyph ? /*#__PURE__*/React.createElement("i", {
    className: `ti ti-${glyph}`,
    "aria-hidden": "true"
  }) : null, children);
}
Object.assign(__ds_scope, { StatusPill });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/badges/StatusPill.jsx", error: String((e && e.message) || e) }); }

// components/buttons/Button.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Sellervai button. One indigo-solid `primary` action per view; everything
 * else is `secondary` / `ghost`. The gradient + glow `hero` variant is
 * reserved for marketing brand moments only.
 */
function Button({
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
  const cls = ["sv-btn", `sv-btn-${variant}`, size === "sm" ? "sv-btn-sm" : size === "lg" ? "sv-btn-lg" : "", className].filter(Boolean).join(" ");
  return /*#__PURE__*/React.createElement(Tag, _extends({
    className: cls,
    disabled: Tag === "button" ? disabled || busy : undefined,
    "aria-disabled": Tag !== "button" && (disabled || busy) ? "true" : undefined,
    "aria-busy": busy ? "true" : undefined
  }, rest), icon && !busy ? /*#__PURE__*/React.createElement("i", {
    className: `ti ti-${icon}`,
    "aria-hidden": "true"
  }) : null, children, iconRight && !busy ? /*#__PURE__*/React.createElement("i", {
    className: `ti ti-${iconRight}`,
    "aria-hidden": "true"
  }) : null);
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/buttons/Button.jsx", error: String((e && e.message) || e) }); }

// components/buttons/IconButton.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/** Square icon-only button for table rows, card headers, toolbars. */
function IconButton({
  icon,
  label,
  className = "",
  ...rest
}) {
  return /*#__PURE__*/React.createElement("button", _extends({
    type: "button",
    className: `sv-icon-btn ${className}`.trim(),
    "aria-label": label,
    title: label
  }, rest), /*#__PURE__*/React.createElement("i", {
    className: `ti ti-${icon}`,
    "aria-hidden": "true"
  }));
}
Object.assign(__ds_scope, { IconButton });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/buttons/IconButton.jsx", error: String((e && e.message) || e) }); }

// components/feedback/Alert.jsx
try { (() => {
const ICONS = {
  success: "circle-check",
  warning: "alert-triangle",
  danger: "alert-circle",
  info: "info-circle"
};

/** Inline alert / toast in one of the four semantic tones. */
function Alert({
  tone = "info",
  title,
  icon,
  children,
  className = ""
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: `sv-alert sv-alert-${tone} ${className}`.trim(),
    role: "alert"
  }, /*#__PURE__*/React.createElement("i", {
    className: `ti ti-${icon ?? ICONS[tone]}`,
    "aria-hidden": "true"
  }), /*#__PURE__*/React.createElement("div", null, title ? /*#__PURE__*/React.createElement("p", {
    className: "sv-alert-title"
  }, title) : null, children ? /*#__PURE__*/React.createElement("p", null, children) : null));
}
Object.assign(__ds_scope, { Alert });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/Alert.jsx", error: String((e && e.message) || e) }); }

// components/feedback/EmptyState.jsx
try { (() => {
/** Centered empty state for zero-data tables, inboxes, product lists. */
function EmptyState({
  icon = "inbox",
  title,
  children,
  action,
  className = ""
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: `sv-empty ${className}`.trim()
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-empty-icon"
  }, /*#__PURE__*/React.createElement("i", {
    className: `ti ti-${icon}`,
    "aria-hidden": "true"
  })), title ? /*#__PURE__*/React.createElement("h3", null, title) : null, children ? /*#__PURE__*/React.createElement("p", null, children) : null, action ? /*#__PURE__*/React.createElement("div", null, action) : null);
}
Object.assign(__ds_scope, { EmptyState });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/EmptyState.jsx", error: String((e && e.message) || e) }); }

// components/forms/Field.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Labeled form control built on Pico inputs. Renders an input, select, or
 * textarea with optional "(optional)" marker and inline error state.
 */
function Field({
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
  return /*#__PURE__*/React.createElement("label", {
    className: `sv-field ${className}`.trim()
  }, label ? /*#__PURE__*/React.createElement("span", {
    className: "sv-field-label"
  }, label, optional ? /*#__PURE__*/React.createElement("span", {
    className: "sv-optional"
  }, " (optional)") : null) : null, as === "select" ? /*#__PURE__*/React.createElement("select", _extends({
    className: controlCls,
    "aria-invalid": invalid || undefined
  }, rest), options.map(o => /*#__PURE__*/React.createElement("option", {
    key: o.value ?? o,
    value: o.value ?? o
  }, o.label ?? o))) : as === "textarea" ? /*#__PURE__*/React.createElement("textarea", _extends({
    className: controlCls,
    "aria-invalid": invalid || undefined
  }, rest)) : /*#__PURE__*/React.createElement("input", _extends({
    type: type,
    className: controlCls,
    "aria-invalid": invalid || undefined
  }, rest)), error ? /*#__PURE__*/React.createElement("p", {
    className: "sv-field-error"
  }, error) : null);
}
Object.assign(__ds_scope, { Field });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Field.jsx", error: String((e && e.message) || e) }); }

// components/surfaces/Card.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/** Dashboard panel with optional header (title + action) and footer. */
function Card({
  title,
  action,
  footer,
  children,
  className = "",
  ...rest
}) {
  return /*#__PURE__*/React.createElement("section", _extends({
    className: `sv-card ${className}`.trim()
  }, rest), (title || action) && /*#__PURE__*/React.createElement("header", {
    className: "sv-card-header"
  }, title ? /*#__PURE__*/React.createElement("h3", {
    className: "sv-card-title"
  }, title) : /*#__PURE__*/React.createElement("span", null), action ? /*#__PURE__*/React.createElement("div", {
    className: "sv-card-action"
  }, action) : null), /*#__PURE__*/React.createElement("div", {
    className: "sv-card-body"
  }, children), footer ? /*#__PURE__*/React.createElement("footer", {
    className: "sv-card-footer"
  }, footer) : null);
}
Object.assign(__ds_scope, { Card });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/surfaces/Card.jsx", error: String((e && e.message) || e) }); }

// components/surfaces/StatTile.jsx
try { (() => {
/** Single dashboard metric — label, big value, optional icon + trend delta. */
function StatTile({
  label,
  value,
  icon,
  delta,
  trend,
  className = ""
}) {
  return /*#__PURE__*/React.createElement("article", {
    className: `sv-stat ${className}`.trim()
  }, /*#__PURE__*/React.createElement("div", {
    className: "sv-stat-head"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-stat-label"
  }, label), icon ? /*#__PURE__*/React.createElement("span", {
    className: "sv-stat-icon"
  }, /*#__PURE__*/React.createElement("i", {
    className: `ti ti-${icon}`,
    "aria-hidden": "true"
  })) : null), /*#__PURE__*/React.createElement("div", {
    className: "sv-stat-value sv-tnum"
  }, value), delta ? /*#__PURE__*/React.createElement("span", {
    className: `sv-stat-delta ${trend === "down" ? "is-down" : "is-up"}`
  }, /*#__PURE__*/React.createElement("i", {
    className: `ti ti-${trend === "down" ? "trending-down" : "trending-up"}`,
    "aria-hidden": "true"
  }), delta) : null);
}
Object.assign(__ds_scope, { StatTile });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/surfaces/StatTile.jsx", error: String((e && e.message) || e) }); }

// ui_kits/dashboard/screens.jsx
try { (() => {
/* Sellervai — Dashboard UI kit (proposed per the design brief — the live
   app does not yet ship a dashboard template). Shell + overview screen,
   built from the system's .sv-* component classes. */

function Sidebar({
  active,
  go
}) {
  const Item = ({
    id,
    icon,
    label,
    badge
  }) => /*#__PURE__*/React.createElement("a", {
    className: `sv-side-link${active === id ? " is-active" : ""}`,
    onClick: e => {
      e.preventDefault();
      go(id);
    }
  }, /*#__PURE__*/React.createElement("i", {
    className: `ti ti-${icon}`
  }), label, badge != null && /*#__PURE__*/React.createElement("span", {
    className: `sv-pill sv-pill-${badge.tone} sv-side-badge`
  }, badge.text));
  return /*#__PURE__*/React.createElement("aside", {
    className: "sv-sidebar"
  }, /*#__PURE__*/React.createElement("a", {
    className: "sv-brand"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-brand-mark"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-robot"
  })), "Sellervai"), /*#__PURE__*/React.createElement(Item, {
    id: "overview",
    icon: "layout-dashboard",
    label: "Overview"
  }), /*#__PURE__*/React.createElement(Item, {
    id: "inbox",
    icon: "messages",
    label: "Conversations",
    badge: {
      tone: "info",
      text: "6"
    }
  }), /*#__PURE__*/React.createElement(Item, {
    id: "orders",
    icon: "shopping-bag",
    label: "Orders"
  }), /*#__PURE__*/React.createElement(Item, {
    id: "products",
    icon: "package",
    label: "Products"
  }), /*#__PURE__*/React.createElement(Item, {
    id: "coupons",
    icon: "ticket",
    label: "Coupons"
  }), /*#__PURE__*/React.createElement("div", {
    className: "sv-side-section"
  }, "Setup"), /*#__PURE__*/React.createElement(Item, {
    id: "channels",
    icon: "plug-connected",
    label: "Channels"
  }), /*#__PURE__*/React.createElement(Item, {
    id: "kb",
    icon: "database",
    label: "Knowledge base"
  }), /*#__PURE__*/React.createElement(Item, {
    id: "settings",
    icon: "settings",
    label: "Settings"
  }), /*#__PURE__*/React.createElement("div", {
    className: "sv-side-foot"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-avatar"
  }, "AS"), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      minWidth: 0
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "sv-convo-name"
  }, "Acme Store"), /*#__PURE__*/React.createElement("div", {
    className: "sv-convo-time"
  }, "owner@acmestore.com"))));
}
function DashTheme() {
  const [theme, setTheme] = React.useState(() => document.documentElement.dataset.theme || "light");
  React.useEffect(() => {
    document.documentElement.dataset.theme = theme;
    try {
      localStorage.setItem("sv-theme", theme);
    } catch (e) {}
  }, [theme]);
  return /*#__PURE__*/React.createElement("button", {
    className: "sv-theme-toggle",
    "aria-label": "Toggle theme",
    onClick: () => setTheme(t => t === "dark" ? "light" : "dark")
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-sun"
  }), /*#__PURE__*/React.createElement("i", {
    className: "ti ti-moon"
  }));
}
const PLAT = {
  whatsapp: {
    v: "var(--sv-whatsapp)",
    icon: "brand-whatsapp"
  },
  messenger: {
    v: "var(--sv-messenger)",
    icon: "brand-messenger"
  },
  instagram: {
    v: "var(--sv-instagram)",
    icon: "brand-instagram"
  },
  telegram: {
    v: "var(--sv-telegram)",
    icon: "brand-telegram"
  }
};
function PlatDot({
  p
}) {
  const m = PLAT[p];
  return /*#__PURE__*/React.createElement("span", {
    className: "sv-plat-dot",
    style: {
      background: m.v
    }
  }, /*#__PURE__*/React.createElement("i", {
    className: `ti ti-${m.icon}`
  }));
}
const CONVOS = [{
  p: "whatsapp",
  name: "Rahima K.",
  msg: "Do you have the blue kurti in medium?",
  time: "2m"
}, {
  p: "messenger",
  name: "Tanvir A.",
  msg: "Order #10482 — when will it ship?",
  time: "11m"
}, {
  p: "instagram",
  name: "@sadia.styles",
  msg: "Is the discount code still valid?",
  time: "23m"
}, {
  p: "telegram",
  name: "Imran H.",
  msg: "Thanks! The AI answered everything 👍",
  time: "1h"
}];
const ORDERS = [{
  id: "#ORD-10482",
  cust: "Tanvir Ahmed",
  items: 2,
  total: "৳ 2,400",
  status: ["success", "Paid"]
}, {
  id: "#ORD-10481",
  cust: "Rahima Khatun",
  items: 1,
  total: "৳ 890",
  status: ["warning", "Pending"]
}, {
  id: "#ORD-10480",
  cust: "Sadia R.",
  items: 4,
  total: "৳ 5,120",
  status: ["success", "Paid"]
}, {
  id: "#ORD-10479",
  cust: "Imran Hossain",
  items: 1,
  total: "৳ 1,250",
  status: ["danger", "Failed"]
}];
function Overview() {
  return /*#__PURE__*/React.createElement("div", {
    className: "sv-content"
  }, /*#__PURE__*/React.createElement("div", {
    className: "sv-stat-grid"
  }, /*#__PURE__*/React.createElement("article", {
    className: "sv-stat"
  }, /*#__PURE__*/React.createElement("div", {
    className: "sv-stat-head"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-stat-label"
  }, "Conversations today"), /*#__PURE__*/React.createElement("span", {
    className: "sv-stat-icon"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-messages"
  }))), /*#__PURE__*/React.createElement("div", {
    className: "sv-stat-value sv-tnum"
  }, "248"), /*#__PURE__*/React.createElement("span", {
    className: "sv-stat-delta is-up"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-trending-up"
  }), "+12% vs yesterday")), /*#__PURE__*/React.createElement("article", {
    className: "sv-stat"
  }, /*#__PURE__*/React.createElement("div", {
    className: "sv-stat-head"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-stat-label"
  }, "Orders today"), /*#__PURE__*/React.createElement("span", {
    className: "sv-stat-icon"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-shopping-bag"
  }))), /*#__PURE__*/React.createElement("div", {
    className: "sv-stat-value sv-tnum"
  }, "37"), /*#__PURE__*/React.createElement("span", {
    className: "sv-stat-delta is-down"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-trending-down"
  }), "-4% vs yesterday")), /*#__PURE__*/React.createElement("article", {
    className: "sv-stat"
  }, /*#__PURE__*/React.createElement("div", {
    className: "sv-stat-head"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-stat-label"
  }, "Revenue today"), /*#__PURE__*/React.createElement("span", {
    className: "sv-stat-icon"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-coin"
  }))), /*#__PURE__*/React.createElement("div", {
    className: "sv-stat-value sv-tnum"
  }, "\u09F3 84,200"), /*#__PURE__*/React.createElement("span", {
    className: "sv-stat-delta is-up"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-trending-up"
  }), "+8%")), /*#__PURE__*/React.createElement("article", {
    className: "sv-stat"
  }, /*#__PURE__*/React.createElement("div", {
    className: "sv-stat-head"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-stat-label"
  }, "AI agent"), /*#__PURE__*/React.createElement("span", {
    className: "sv-stat-icon"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-robot"
  }))), /*#__PURE__*/React.createElement("div", {
    className: "sv-stat-value",
    style: {
      fontSize: "var(--sv-fs-lg)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-pill sv-pill-success"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-dot is-live"
  }), "Online")), /*#__PURE__*/React.createElement("span", {
    className: "sv-convo-time"
  }, "RAG synced \xB7 1,204 docs indexed"))), /*#__PURE__*/React.createElement("div", {
    className: "sv-alert sv-alert-warning"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-alert-triangle"
  }), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("p", {
    className: "sv-alert-title"
  }, "WhatsApp token expires in 3 days"), /*#__PURE__*/React.createElement("p", null, "Reconnect the channel to keep automated replies running."))), /*#__PURE__*/React.createElement("div", {
    className: "sv-grid-2"
  }, /*#__PURE__*/React.createElement("section", {
    className: "sv-card"
  }, /*#__PURE__*/React.createElement("header", {
    className: "sv-card-header"
  }, /*#__PURE__*/React.createElement("h3", {
    className: "sv-card-title"
  }, "Recent conversations"), /*#__PURE__*/React.createElement("button", {
    className: "sv-btn sv-btn-ghost sv-btn-sm"
  }, "Open inbox", /*#__PURE__*/React.createElement("i", {
    className: "ti ti-chevron-right"
  }))), /*#__PURE__*/React.createElement("div", {
    className: "sv-card-body",
    style: {
      paddingTop: 0,
      paddingBottom: 0
    }
  }, CONVOS.map(c => /*#__PURE__*/React.createElement("div", {
    className: "sv-convo",
    key: c.name
  }, /*#__PURE__*/React.createElement(PlatDot, {
    p: c.p
  }), /*#__PURE__*/React.createElement("div", {
    className: "sv-convo-body"
  }, /*#__PURE__*/React.createElement("div", {
    className: "sv-convo-name"
  }, c.name), /*#__PURE__*/React.createElement("div", {
    className: "sv-convo-msg"
  }, c.msg)), /*#__PURE__*/React.createElement("span", {
    className: "sv-convo-time"
  }, c.time))))), /*#__PURE__*/React.createElement("section", {
    className: "sv-card"
  }, /*#__PURE__*/React.createElement("header", {
    className: "sv-card-header"
  }, /*#__PURE__*/React.createElement("h3", {
    className: "sv-card-title"
  }, "Channels"), /*#__PURE__*/React.createElement("button", {
    className: "sv-btn sv-btn-ghost sv-btn-sm"
  }, "Manage", /*#__PURE__*/React.createElement("i", {
    className: "ti ti-chevron-right"
  }))), /*#__PURE__*/React.createElement("div", {
    className: "sv-card-body",
    style: {
      display: "grid",
      gap: "var(--sv-space-3)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "sv-platform sv-platform-whatsapp",
    style: {
      boxShadow: "none",
      padding: "var(--sv-space-3) var(--sv-space-4)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-platform-logo"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-brand-whatsapp"
  })), /*#__PURE__*/React.createElement("div", {
    className: "sv-platform-meta"
  }, /*#__PURE__*/React.createElement("p", {
    className: "sv-platform-name"
  }, "WhatsApp"), /*#__PURE__*/React.createElement("p", {
    className: "sv-platform-sub"
  }, "+880 1712-xxxxxx")), /*#__PURE__*/React.createElement("span", {
    className: "sv-pill sv-pill-success"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-dot"
  }), "Connected")), /*#__PURE__*/React.createElement("div", {
    className: "sv-platform sv-platform-messenger",
    style: {
      boxShadow: "none",
      padding: "var(--sv-space-3) var(--sv-space-4)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-platform-logo"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-brand-messenger"
  })), /*#__PURE__*/React.createElement("div", {
    className: "sv-platform-meta"
  }, /*#__PURE__*/React.createElement("p", {
    className: "sv-platform-name"
  }, "Messenger"), /*#__PURE__*/React.createElement("p", {
    className: "sv-platform-sub"
  }, "Acme Store Page")), /*#__PURE__*/React.createElement("span", {
    className: "sv-pill sv-pill-success"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-dot"
  }), "Connected")), /*#__PURE__*/React.createElement("div", {
    className: "sv-platform sv-platform-instagram",
    style: {
      boxShadow: "none",
      padding: "var(--sv-space-3) var(--sv-space-4)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-platform-logo"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-brand-instagram"
  })), /*#__PURE__*/React.createElement("div", {
    className: "sv-platform-meta"
  }, /*#__PURE__*/React.createElement("p", {
    className: "sv-platform-name"
  }, "Instagram"), /*#__PURE__*/React.createElement("p", {
    className: "sv-platform-sub"
  }, "Webhook returned 403")), /*#__PURE__*/React.createElement("span", {
    className: "sv-pill sv-pill-danger"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-dot"
  }), "Error")), /*#__PURE__*/React.createElement("div", {
    className: "sv-platform sv-platform-telegram",
    style: {
      boxShadow: "none",
      padding: "var(--sv-space-3) var(--sv-space-4)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-platform-logo"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-brand-telegram"
  })), /*#__PURE__*/React.createElement("div", {
    className: "sv-platform-meta"
  }, /*#__PURE__*/React.createElement("p", {
    className: "sv-platform-name"
  }, "Telegram"), /*#__PURE__*/React.createElement("p", {
    className: "sv-platform-sub"
  }, "Not connected")), /*#__PURE__*/React.createElement("button", {
    className: "sv-btn sv-btn-primary sv-btn-sm"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-plug-connected"
  }), "Connect"))))), /*#__PURE__*/React.createElement("section", {
    className: "sv-card"
  }, /*#__PURE__*/React.createElement("header", {
    className: "sv-card-header"
  }, /*#__PURE__*/React.createElement("h3", {
    className: "sv-card-title"
  }, "Recent orders"), /*#__PURE__*/React.createElement("button", {
    className: "sv-btn sv-btn-secondary sv-btn-sm"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-download"
  }), "Export CSV")), /*#__PURE__*/React.createElement("div", {
    className: "sv-table-wrap",
    style: {
      border: "none",
      borderRadius: 0
    }
  }, /*#__PURE__*/React.createElement("table", {
    className: "sv-table"
  }, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", null, /*#__PURE__*/React.createElement("th", null, "Order"), /*#__PURE__*/React.createElement("th", null, "Customer"), /*#__PURE__*/React.createElement("th", null, "Items"), /*#__PURE__*/React.createElement("th", {
    className: "sv-tnum"
  }, "Total"), /*#__PURE__*/React.createElement("th", null, "Status"), /*#__PURE__*/React.createElement("th", null))), /*#__PURE__*/React.createElement("tbody", null, ORDERS.map(o => /*#__PURE__*/React.createElement("tr", {
    key: o.id
  }, /*#__PURE__*/React.createElement("td", {
    style: {
      fontFamily: "var(--sv-font-mono)",
      fontSize: "var(--sv-fs-xs)"
    }
  }, o.id), /*#__PURE__*/React.createElement("td", null, o.cust), /*#__PURE__*/React.createElement("td", {
    className: "sv-tnum"
  }, o.items), /*#__PURE__*/React.createElement("td", {
    className: "sv-tnum"
  }, o.total), /*#__PURE__*/React.createElement("td", null, /*#__PURE__*/React.createElement("span", {
    className: `sv-pill sv-pill-${o.status[0]}`
  }, o.status[1])), /*#__PURE__*/React.createElement("td", {
    style: {
      textAlign: "right"
    }
  }, /*#__PURE__*/React.createElement("button", {
    className: "sv-icon-btn",
    "aria-label": "Actions"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-dots-vertical"
  }))))))))));
}
const PLACEHOLDER = {
  inbox: "Conversations",
  orders: "Orders",
  products: "Products",
  coupons: "Coupons",
  channels: "Channels",
  kb: "Knowledge base",
  settings: "Settings"
};
function DashboardApp() {
  const [active, setActive] = React.useState("overview");
  const title = active === "overview" ? "Overview" : PLACEHOLDER[active];
  return /*#__PURE__*/React.createElement("div", {
    className: "sv-shell"
  }, /*#__PURE__*/React.createElement(Sidebar, {
    active: active,
    go: setActive
  }), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("header", {
    className: "sv-topbar"
  }, /*#__PURE__*/React.createElement("h1", null, title), /*#__PURE__*/React.createElement("div", {
    className: "sv-topbar-actions"
  }, /*#__PURE__*/React.createElement("button", {
    className: "sv-icon-btn",
    "aria-label": "Search"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-search"
  })), /*#__PURE__*/React.createElement("button", {
    className: "sv-icon-btn",
    "aria-label": "Notifications"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-bell"
  })), /*#__PURE__*/React.createElement(DashTheme, null), /*#__PURE__*/React.createElement("button", {
    className: "sv-btn sv-btn-primary sv-btn-sm"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-plus"
  }), "New product"))), active === "overview" ? /*#__PURE__*/React.createElement(Overview, null) : /*#__PURE__*/React.createElement("div", {
    className: "sv-content"
  }, /*#__PURE__*/React.createElement("div", {
    className: "sv-card"
  }, /*#__PURE__*/React.createElement("div", {
    className: "sv-empty"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-empty-icon"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-layout-grid"
  })), /*#__PURE__*/React.createElement("h3", null, title), /*#__PURE__*/React.createElement("p", null, "This screen is part of the dashboard shell. The Overview screen demonstrates the full component set."), /*#__PURE__*/React.createElement("button", {
    className: "sv-btn sv-btn-secondary",
    onClick: () => setActive("overview")
  }, "Back to Overview"))))));
}
Object.assign(window, {
  DashboardApp
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/dashboard/screens.jsx", error: String((e && e.message) || e) }); }

// ui_kits/marketing/screens.jsx
try { (() => {
/* Sellervai — Marketing + Auth UI kit screens (self-contained demo).
   Mirrors the live Mako templates (index/login/register) restyled under
   the new tokens. Components emit the same .sv-* classes the system ships. */

function ThemeToggle() {
  const [theme, setTheme] = React.useState(() => document.documentElement.dataset.theme || "light");
  React.useEffect(() => {
    document.documentElement.dataset.theme = theme;
    try {
      localStorage.setItem("sv-theme", theme);
    } catch (e) {}
  }, [theme]);
  return /*#__PURE__*/React.createElement("button", {
    className: "sv-theme-toggle",
    "aria-label": "Toggle theme",
    onClick: () => setTheme(t => t === "dark" ? "light" : "dark")
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-sun"
  }), /*#__PURE__*/React.createElement("i", {
    className: "ti ti-moon"
  }));
}
function NavBar({
  go,
  current
}) {
  return /*#__PURE__*/React.createElement("nav", {
    className: "container-fluid sv-nav",
    style: {
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between"
    }
  }, /*#__PURE__*/React.createElement("a", {
    className: "sv-brand",
    href: "#",
    onClick: e => {
      e.preventDefault();
      go("home");
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-brand-mark"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-robot"
  })), "Sellervai"), /*#__PURE__*/React.createElement("div", {
    className: "sv-nav-actions"
  }, /*#__PURE__*/React.createElement(ThemeToggle, null), current !== "login" && /*#__PURE__*/React.createElement("button", {
    className: "sv-btn sv-btn-ghost",
    onClick: () => go("login")
  }, "Sign in"), current !== "register" && /*#__PURE__*/React.createElement("button", {
    className: "sv-btn sv-btn-hero",
    onClick: () => go("register")
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-rocket"
  }), " Get started")));
}
const FEATURES = [{
  icon: "messages",
  title: "Multi-platform messaging",
  body: "Handle WhatsApp, Messenger, Instagram DMs, and Telegram from one unified inbox."
}, {
  icon: "brain",
  title: "AI chat assistant",
  body: "DeepSeek-powered AI answers questions, suggests products, and closes sales 24/7."
}, {
  icon: "database",
  title: "Smart knowledge base",
  body: "Upload PDFs, product lists, and docs — the AI learns your catalogue automatically."
}, {
  icon: "chart-bar",
  title: "Live dashboard",
  body: "Monitor conversations, orders, and performance metrics in real time with HTMX updates."
}, {
  icon: "plug-connected",
  title: "One-click integrations",
  body: "Connect Facebook, Instagram, and WhatsApp via OAuth in seconds — no API keys needed."
}, {
  icon: "lock",
  title: "Secure & private",
  body: "All tokens are encrypted at rest. Your data never leaves your own database."
}];
function HomeScreen({
  go
}) {
  return /*#__PURE__*/React.createElement("main", {
    className: "container sv-main"
  }, /*#__PURE__*/React.createElement("section", {
    className: "sv-hero"
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("span", {
    className: "sv-badge"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-sparkles"
  }), " AI-Powered"), /*#__PURE__*/React.createElement("h1", null, "Automate your store with\xA0", /*#__PURE__*/React.createElement("em", null, "intelligent"), "\xA0AI"), /*#__PURE__*/React.createElement("p", null, "Sellervai connects your store to WhatsApp, Facebook, Instagram, and Telegram \u2014 letting your AI assistant handle messages, orders, and customer support around the clock."), /*#__PURE__*/React.createElement("div", {
    className: "sv-hero-actions"
  }, /*#__PURE__*/React.createElement("button", {
    className: "sv-btn sv-btn-hero",
    onClick: () => go("register")
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-rocket"
  }), " Start for free"), /*#__PURE__*/React.createElement("button", {
    className: "sv-btn sv-btn-secondary sv-btn-lg",
    onClick: () => go("login")
  }, "Sign in"))), /*#__PURE__*/React.createElement("div", {
    className: "sv-hero-visual",
    "aria-hidden": "true"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-robot sv-hero-icon"
  }))), /*#__PURE__*/React.createElement("section", null, /*#__PURE__*/React.createElement("h2", {
    className: "sv-section-title"
  }, "Everything you need to sell smarter"), /*#__PURE__*/React.createElement("div", {
    className: "sv-feature-grid"
  }, FEATURES.map(f => /*#__PURE__*/React.createElement("article", {
    className: "sv-feature-card",
    key: f.title
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-feature-icon"
  }, /*#__PURE__*/React.createElement("i", {
    className: `ti ti-${f.icon}`
  })), /*#__PURE__*/React.createElement("h3", null, f.title), /*#__PURE__*/React.createElement("p", null, f.body))))), /*#__PURE__*/React.createElement("section", null, /*#__PURE__*/React.createElement("h2", {
    className: "sv-section-title"
  }, "Platform status"), /*#__PURE__*/React.createElement("div", {
    className: "sv-status-box"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-pill sv-pill-success"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-dot is-live"
  }), " All systems operational"), /*#__PURE__*/React.createElement("span", null, "Webhooks, AI agent, and database responding normally."))));
}
function AuthShell({
  children
}) {
  return /*#__PURE__*/React.createElement("main", {
    className: "container"
  }, /*#__PURE__*/React.createElement("div", {
    className: "sv-auth-wrap"
  }, children));
}
function LoginScreen({
  go
}) {
  const [err, setErr] = React.useState(false);
  return /*#__PURE__*/React.createElement(AuthShell, null, /*#__PURE__*/React.createElement("div", {
    className: "sv-auth-card"
  }, /*#__PURE__*/React.createElement("div", {
    className: "sv-auth-header"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-auth-logo"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-robot"
  })), /*#__PURE__*/React.createElement("h1", null, "Welcome back"), /*#__PURE__*/React.createElement("p", null, "Sign in to your Sellervai account")), /*#__PURE__*/React.createElement("div", {
    className: "sv-google-btn-wrap"
  }, /*#__PURE__*/React.createElement("button", {
    className: "sv-google-btn"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-brand-google"
  }), " Sign in with Google")), /*#__PURE__*/React.createElement("div", {
    className: "sv-divider"
  }, /*#__PURE__*/React.createElement("span", null, "or continue with email")), /*#__PURE__*/React.createElement("form", {
    className: "sv-form",
    onSubmit: e => {
      e.preventDefault();
      setErr(true);
    }
  }, /*#__PURE__*/React.createElement("label", {
    className: "sv-field"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-field-label"
  }, "Email"), /*#__PURE__*/React.createElement("input", {
    className: "sv-input",
    type: "email",
    placeholder: "you@example.com",
    defaultValue: "owner@acmestore.com"
  })), /*#__PURE__*/React.createElement("label", {
    className: "sv-field"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-field-label"
  }, "Password"), /*#__PURE__*/React.createElement("input", {
    className: `sv-input${err ? " is-invalid" : ""}`,
    type: "password",
    placeholder: "\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022"
  })), err && /*#__PURE__*/React.createElement("p", {
    className: "sv-field-error"
  }, "Incorrect email or password. Please try again."), /*#__PURE__*/React.createElement("button", {
    className: "sv-btn sv-btn-primary",
    type: "submit",
    style: {
      width: "100%",
      marginTop: 4
    }
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-login"
  }), " Sign in")), /*#__PURE__*/React.createElement("p", {
    className: "sv-auth-footer"
  }, "No account? ", /*#__PURE__*/React.createElement("a", {
    href: "#",
    onClick: e => {
      e.preventDefault();
      go("register");
    }
  }, "Create one"))));
}
function RegisterScreen({
  go
}) {
  return /*#__PURE__*/React.createElement(AuthShell, null, /*#__PURE__*/React.createElement("div", {
    className: "sv-auth-card"
  }, /*#__PURE__*/React.createElement("div", {
    className: "sv-auth-header"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-auth-logo"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-rocket"
  })), /*#__PURE__*/React.createElement("h1", null, "Get started"), /*#__PURE__*/React.createElement("p", null, "Create your free Sellervai account")), /*#__PURE__*/React.createElement("div", {
    className: "sv-google-btn-wrap"
  }, /*#__PURE__*/React.createElement("button", {
    className: "sv-google-btn"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-brand-google"
  }), " Sign up with Google")), /*#__PURE__*/React.createElement("div", {
    className: "sv-divider"
  }, /*#__PURE__*/React.createElement("span", null, "or register with email")), /*#__PURE__*/React.createElement("form", {
    className: "sv-form",
    onSubmit: e => {
      e.preventDefault();
      go("home");
    }
  }, /*#__PURE__*/React.createElement("label", {
    className: "sv-field"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-field-label"
  }, "Name"), /*#__PURE__*/React.createElement("input", {
    className: "sv-input",
    placeholder: "Your name"
  })), /*#__PURE__*/React.createElement("label", {
    className: "sv-field"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-field-label"
  }, "Email"), /*#__PURE__*/React.createElement("input", {
    className: "sv-input",
    type: "email",
    placeholder: "you@example.com"
  })), /*#__PURE__*/React.createElement("label", {
    className: "sv-field"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-field-label"
  }, "Phone", /*#__PURE__*/React.createElement("span", {
    className: "sv-optional"
  }, " (optional)")), /*#__PURE__*/React.createElement("input", {
    className: "sv-input",
    type: "tel",
    placeholder: "+880\u2026"
  })), /*#__PURE__*/React.createElement("label", {
    className: "sv-field"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-field-label"
  }, "Password"), /*#__PURE__*/React.createElement("input", {
    className: "sv-input",
    type: "password",
    placeholder: "Min 8 characters"
  })), /*#__PURE__*/React.createElement("button", {
    className: "sv-btn sv-btn-primary",
    type: "submit",
    style: {
      width: "100%",
      marginTop: 4
    }
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-user-plus"
  }), " Create account")), /*#__PURE__*/React.createElement("p", {
    className: "sv-auth-footer"
  }, "Already have an account? ", /*#__PURE__*/React.createElement("a", {
    href: "#",
    onClick: e => {
      e.preventDefault();
      go("login");
    }
  }, "Sign in"))));
}
function MarketingApp() {
  const [screen, setScreen] = React.useState("home");
  const go = s => setScreen(s);
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(NavBar, {
    go: go,
    current: screen
  }), screen === "home" && /*#__PURE__*/React.createElement(HomeScreen, {
    go: go
  }), screen === "login" && /*#__PURE__*/React.createElement(LoginScreen, {
    go: go
  }), screen === "register" && /*#__PURE__*/React.createElement(RegisterScreen, {
    go: go
  }), /*#__PURE__*/React.createElement("footer", {
    className: "container sv-footer"
  }, /*#__PURE__*/React.createElement("small", null, "\xA9 2025 Sellervai \u2014 AI-powered store automation")));
}
Object.assign(window, {
  MarketingApp
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/marketing/screens.jsx", error: String((e && e.message) || e) }); }

// ui_kits/store_detail/screens.jsx
try { (() => {
/* Sellervai — Store detail UI kit (/stores/{id}). Store config, products,
   coupons, orders, and platform connect/disconnect — composed from .sv-* classes. */

function StoreTheme() {
  const [theme, setTheme] = React.useState(() => document.documentElement.dataset.theme || "light");
  React.useEffect(() => {
    document.documentElement.dataset.theme = theme;
    try {
      localStorage.setItem("sv-theme", theme);
    } catch (e) {}
  }, [theme]);
  return /*#__PURE__*/React.createElement("button", {
    className: "sv-theme-toggle",
    "aria-label": "Toggle theme",
    onClick: () => setTheme(t => t === "dark" ? "light" : "dark")
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-sun"
  }), /*#__PURE__*/React.createElement("i", {
    className: "ti ti-moon"
  }));
}
const PRODUCTS = [{
  name: "Hand-block Cotton Kurti",
  sku: "KRT-014",
  price: "৳ 1,250",
  stock: 24,
  status: ["success", "Active"]
}, {
  name: "Silk Scarf — Indigo",
  sku: "SCF-007",
  price: "৳ 690",
  stock: 8,
  status: ["warning", "Low stock"]
}, {
  name: "Leather Sandals",
  sku: "SND-031",
  price: "৳ 2,100",
  stock: 0,
  status: ["danger", "Out of stock"]
}, {
  name: "Embroidered Tote Bag",
  sku: "BAG-019",
  price: "৳ 950",
  stock: 41,
  status: ["success", "Active"]
}];
const COUPONS = [{
  code: "EID25",
  off: "25% off",
  uses: "142 / 500",
  status: ["success", "Active"]
}, {
  code: "WELCOME10",
  off: "৳ 100 off",
  uses: "1,024 / ∞",
  status: ["success", "Active"]
}, {
  code: "MONSOON",
  off: "15% off",
  uses: "300 / 300",
  status: ["neutral", "Ended"]
}];
const CHANNELS = [{
  p: "whatsapp",
  name: "WhatsApp Business",
  sub: "+880 1712-xxxxxx",
  state: "connected"
}, {
  p: "messenger",
  name: "Facebook Messenger",
  sub: "Acme Store Page",
  state: "connected"
}, {
  p: "instagram",
  name: "Instagram Direct",
  sub: "Webhook returned 403",
  state: "error"
}, {
  p: "telegram",
  name: "Telegram Bot",
  sub: "Not connected",
  state: "disconnected"
}];
const PMETA = {
  whatsapp: "brand-whatsapp",
  messenger: "brand-messenger",
  instagram: "brand-instagram",
  telegram: "brand-telegram"
};
function ChannelCard({
  c
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: `sv-platform sv-platform-${c.p}`
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-platform-logo"
  }, /*#__PURE__*/React.createElement("i", {
    className: `ti ti-${PMETA[c.p]}`
  })), /*#__PURE__*/React.createElement("div", {
    className: "sv-platform-meta"
  }, /*#__PURE__*/React.createElement("p", {
    className: "sv-platform-name"
  }, c.name), /*#__PURE__*/React.createElement("p", {
    className: "sv-platform-sub"
  }, c.sub)), c.state === "connected" && /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("span", {
    className: "sv-pill sv-pill-success"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-dot"
  }), "Connected"), /*#__PURE__*/React.createElement("button", {
    className: "sv-btn sv-btn-ghost sv-btn-sm"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-plug-off"
  }), "Disconnect")), c.state === "error" && /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("span", {
    className: "sv-pill sv-pill-danger"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-dot"
  }), "Error"), /*#__PURE__*/React.createElement("button", {
    className: "sv-btn sv-btn-secondary sv-btn-sm"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-refresh"
  }), "Reconnect")), c.state === "disconnected" && /*#__PURE__*/React.createElement("button", {
    className: "sv-btn sv-btn-primary sv-btn-sm"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-plug-connected"
  }), "Connect"));
}
function Products() {
  return /*#__PURE__*/React.createElement("section", {
    className: "sv-card"
  }, /*#__PURE__*/React.createElement("header", {
    className: "sv-card-header"
  }, /*#__PURE__*/React.createElement("h3", {
    className: "sv-card-title"
  }, "Products ", /*#__PURE__*/React.createElement("span", {
    className: "sv-pill sv-pill-neutral"
  }, "4")), /*#__PURE__*/React.createElement("button", {
    className: "sv-btn sv-btn-primary sv-btn-sm"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-plus"
  }), "Add product")), /*#__PURE__*/React.createElement("div", {
    className: "sv-table-wrap",
    style: {
      border: "none",
      borderRadius: 0
    }
  }, /*#__PURE__*/React.createElement("table", {
    className: "sv-table"
  }, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", null, /*#__PURE__*/React.createElement("th", null, "Product"), /*#__PURE__*/React.createElement("th", null, "SKU"), /*#__PURE__*/React.createElement("th", {
    className: "sv-tnum"
  }, "Price"), /*#__PURE__*/React.createElement("th", {
    className: "sv-tnum"
  }, "Stock"), /*#__PURE__*/React.createElement("th", null, "Status"), /*#__PURE__*/React.createElement("th", null))), /*#__PURE__*/React.createElement("tbody", null, PRODUCTS.map(p => /*#__PURE__*/React.createElement("tr", {
    key: p.sku
  }, /*#__PURE__*/React.createElement("td", {
    style: {
      fontWeight: 600
    }
  }, p.name), /*#__PURE__*/React.createElement("td", {
    style: {
      fontFamily: "var(--sv-font-mono)",
      fontSize: "var(--sv-fs-xs)",
      color: "var(--sv-text-muted)"
    }
  }, p.sku), /*#__PURE__*/React.createElement("td", {
    className: "sv-tnum"
  }, p.price), /*#__PURE__*/React.createElement("td", {
    className: "sv-tnum"
  }, p.stock), /*#__PURE__*/React.createElement("td", null, /*#__PURE__*/React.createElement("span", {
    className: `sv-pill sv-pill-${p.status[0]}`
  }, p.status[1])), /*#__PURE__*/React.createElement("td", {
    style: {
      textAlign: "right"
    }
  }, /*#__PURE__*/React.createElement("button", {
    className: "sv-icon-btn",
    "aria-label": "Edit"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-pencil"
  })))))))));
}
function Coupons() {
  return /*#__PURE__*/React.createElement("section", {
    className: "sv-card"
  }, /*#__PURE__*/React.createElement("header", {
    className: "sv-card-header"
  }, /*#__PURE__*/React.createElement("h3", {
    className: "sv-card-title"
  }, "Coupons"), /*#__PURE__*/React.createElement("button", {
    className: "sv-btn sv-btn-primary sv-btn-sm"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-plus"
  }), "New coupon")), /*#__PURE__*/React.createElement("div", {
    className: "sv-table-wrap",
    style: {
      border: "none",
      borderRadius: 0
    }
  }, /*#__PURE__*/React.createElement("table", {
    className: "sv-table"
  }, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", null, /*#__PURE__*/React.createElement("th", null, "Code"), /*#__PURE__*/React.createElement("th", null, "Discount"), /*#__PURE__*/React.createElement("th", null, "Redeemed"), /*#__PURE__*/React.createElement("th", null, "Status"))), /*#__PURE__*/React.createElement("tbody", null, COUPONS.map(c => /*#__PURE__*/React.createElement("tr", {
    key: c.code
  }, /*#__PURE__*/React.createElement("td", {
    style: {
      fontFamily: "var(--sv-font-mono)",
      fontWeight: 600
    }
  }, c.code), /*#__PURE__*/React.createElement("td", null, c.off), /*#__PURE__*/React.createElement("td", {
    className: "sv-tnum"
  }, c.uses), /*#__PURE__*/React.createElement("td", null, /*#__PURE__*/React.createElement("span", {
    className: `sv-pill sv-pill-${c.status[0]}`
  }, c.status[1]))))))));
}
function Channels() {
  return /*#__PURE__*/React.createElement("section", {
    className: "sv-card"
  }, /*#__PURE__*/React.createElement("header", {
    className: "sv-card-header"
  }, /*#__PURE__*/React.createElement("h3", {
    className: "sv-card-title"
  }, "Connected channels")), /*#__PURE__*/React.createElement("div", {
    className: "sv-card-body",
    style: {
      display: "grid",
      gap: "var(--sv-space-3)"
    }
  }, CHANNELS.map(c => /*#__PURE__*/React.createElement(ChannelCard, {
    c: c,
    key: c.p
  }))));
}
function Settings() {
  return /*#__PURE__*/React.createElement("section", {
    className: "sv-card"
  }, /*#__PURE__*/React.createElement("header", {
    className: "sv-card-header"
  }, /*#__PURE__*/React.createElement("h3", {
    className: "sv-card-title"
  }, "Store details")), /*#__PURE__*/React.createElement("div", {
    className: "sv-card-body"
  }, /*#__PURE__*/React.createElement("form", {
    className: "sv-form",
    style: {
      maxWidth: 520
    },
    onSubmit: e => e.preventDefault()
  }, /*#__PURE__*/React.createElement("label", {
    className: "sv-field"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-field-label"
  }, "Store name"), /*#__PURE__*/React.createElement("input", {
    className: "sv-input",
    defaultValue: "Acme Store"
  })), /*#__PURE__*/React.createElement("label", {
    className: "sv-field"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-field-label"
  }, "Description", /*#__PURE__*/React.createElement("span", {
    className: "sv-optional"
  }, " (used by the AI knowledge base)")), /*#__PURE__*/React.createElement("textarea", {
    className: "sv-input",
    rows: "3",
    defaultValue: "Handcrafted clothing & accessories from Dhaka. Fast delivery across Bangladesh."
  })), /*#__PURE__*/React.createElement("label", {
    className: "sv-field"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-field-label"
  }, "Default currency"), /*#__PURE__*/React.createElement("select", {
    className: "sv-input"
  }, /*#__PURE__*/React.createElement("option", null, "BDT (\u09F3)"), /*#__PURE__*/React.createElement("option", null, "USD ($)"), /*#__PURE__*/React.createElement("option", null, "INR (\u20B9)"))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: "var(--sv-space-3)"
    }
  }, /*#__PURE__*/React.createElement("button", {
    className: "sv-btn sv-btn-primary",
    type: "submit"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-check"
  }), "Save changes"), /*#__PURE__*/React.createElement("button", {
    className: "sv-btn sv-btn-ghost",
    type: "button"
  }, "Cancel")))));
}
const TABS = [{
  id: "products",
  label: "Products",
  icon: "package"
}, {
  id: "coupons",
  label: "Coupons",
  icon: "ticket"
}, {
  id: "channels",
  label: "Channels",
  icon: "plug-connected"
}, {
  id: "settings",
  label: "Settings",
  icon: "settings"
}];
function StoreApp() {
  const [tab, setTab] = React.useState("products");
  return /*#__PURE__*/React.createElement("main", {
    className: "container",
    style: {
      maxWidth: 960,
      paddingTop: "var(--sv-space-6)",
      paddingBottom: "var(--sv-space-8)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      marginBottom: "var(--sv-space-5)"
    }
  }, /*#__PURE__*/React.createElement("a", {
    className: "sv-brand"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-brand-mark"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-robot"
  })), "Sellervai"), /*#__PURE__*/React.createElement(StoreTheme, null)), /*#__PURE__*/React.createElement("header", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: "var(--sv-space-4)",
      marginBottom: "var(--sv-space-5)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-platform-logo",
    style: {
      background: "var(--sv-gradient)",
      width: "3.25rem",
      height: "3.25rem",
      borderRadius: "var(--sv-radius)"
    }
  }, /*#__PURE__*/React.createElement("i", {
    className: "ti ti-building-store"
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1
    }
  }, /*#__PURE__*/React.createElement("h1", {
    style: {
      margin: 0
    }
  }, "Acme Store"), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: 0,
      color: "var(--sv-text-muted)",
      fontSize: "var(--sv-fs-sm)"
    }
  }, "store #a1f9 \xB7 4 products \xB7 3 channels live")), /*#__PURE__*/React.createElement("span", {
    className: "sv-pill sv-pill-success"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sv-dot is-live"
  }), "AI online")), /*#__PURE__*/React.createElement("nav", {
    style: {
      display: "flex",
      gap: "var(--sv-space-2)",
      borderBottom: "1px solid var(--sv-border)",
      marginBottom: "var(--sv-space-5)"
    }
  }, TABS.map(t => /*#__PURE__*/React.createElement("button", {
    key: t.id,
    onClick: () => setTab(t.id),
    className: `sv-btn ${tab === t.id ? "sv-btn-ghost" : "sv-btn-ghost"}`,
    style: {
      borderRadius: 0,
      borderBottom: tab === t.id ? "2px solid var(--sv-accent)" : "2px solid transparent",
      color: tab === t.id ? "var(--sv-accent)" : "var(--sv-text-muted)",
      paddingBottom: "0.75rem"
    }
  }, /*#__PURE__*/React.createElement("i", {
    className: `ti ti-${t.icon}`
  }), t.label))), tab === "products" && /*#__PURE__*/React.createElement(Products, null), tab === "coupons" && /*#__PURE__*/React.createElement(Coupons, null), tab === "channels" && /*#__PURE__*/React.createElement(Channels, null), tab === "settings" && /*#__PURE__*/React.createElement(Settings, null));
}
Object.assign(window, {
  StoreApp
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/store_detail/screens.jsx", error: String((e && e.message) || e) }); }

__ds_ns.PlatformChip = __ds_scope.PlatformChip;

__ds_ns.StatusPill = __ds_scope.StatusPill;

__ds_ns.Button = __ds_scope.Button;

__ds_ns.IconButton = __ds_scope.IconButton;

__ds_ns.Alert = __ds_scope.Alert;

__ds_ns.EmptyState = __ds_scope.EmptyState;

__ds_ns.Field = __ds_scope.Field;

__ds_ns.Card = __ds_scope.Card;

__ds_ns.StatTile = __ds_scope.StatTile;

})();
