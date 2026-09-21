"use strict";

// Draws the confirmed resume sections in the Figma "Template 50" layout; the
// styles are in resume-template.css. Shared by /review (the live preview, which
// shows empty sections so the caseworker sees what is missing) and /jobs (the
// resume an application goes with, which leaves them out).
//
// sections: the /api/resume-sections shape (profile, contacts, education,
// employment, volunteer, skills, certificates). Nothing is added to it: the
// template has no skill levels, because nobody was asked for one.
window.ResumeTemplate = (() => {
  const join = (...parts) => parts.map(p => String(p || "").trim()).filter(Boolean).join(", ");

  function el(tag, attrs, ...children) {
    const node = document.createElement(tag);
    for (const [key, value] of Object.entries(attrs || {})) {
      if (value !== null && value !== undefined && value !== false) node.setAttribute(key, value);
    }
    for (const child of children.flat(Infinity)) {
      if (child === null || child === undefined || child === false) continue;
      node.append(child instanceof Node ? child : document.createTextNode(String(child)));
    }
    return node;
  }

  function render(sections, { name = "", showEmpty = false } = {}) {
    const s = sections;
    const none = () => el("p", { class: "rt-body rt-none" }, "Nothing recorded.");
    const section = (title, filled, body) =>
      filled || showEmpty ? el("section", { class: "rt-section" }, el("h2", {}, title), filled ? body() : none()) : null;
    const entries = (list, title, where) => list.map(e => el("div", { class: "rt-entry" },
      el("span", { class: "rt-dates" }, e.dates || ""),
      el("div", {},
        el("h3", {}, title(e)),
        where(e) ? el("p", { class: "rt-where" }, where(e)) : null,
        e.description ? el("p", {}, e.description) : null)));
    const list = items => el("ul", { class: "rt-list" }, items.map(x => el("li", {}, x)));
    // The headline is the latest role the jobseeker named, never a guess.
    const role = s.employment.length ? s.employment[0].position : "";
    const contact = [s.contacts.phone, s.contacts.email].filter(Boolean).join(", ");
    return el("article", { class: "rt", lang: "en" },
      el("header", { class: "rt-head" },
        el("h1", { class: name ? null : "empty" }, name ? join(name, role) : "Name not entered"),
        el("p", {}, contact || "No phone or email recorded.")),
      section("Profile", Boolean(s.profile), () => el("p", { class: "rt-body" }, s.profile)),
      section("Employment", s.employment.length > 0, () =>
        entries(s.employment, e => [e.position, e.company].filter(Boolean).join(" at ") || "Untitled role", e => e.location)),
      section("Volunteer", s.volunteer.length > 0, () =>
        entries(s.volunteer, e => e.role || "Volunteer", e => e.location)),
      section("Education", s.education.length > 0, () =>
        entries(s.education, e => e.school || "Study", e => join(e.major, e.location))),
      section("Skills", s.skills.length > 0, () => list(s.skills)),
      section("Certificates", s.certificates.length > 0, () => list(s.certificates)));
  }

  return { render };
})();
