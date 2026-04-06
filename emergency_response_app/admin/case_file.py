# admin/case_file.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor

from styles import theme
from incident_data import get_incident_display_name


class CaseFile(QWidget):
    """Full case-file view for a single incident."""

    closed = pyqtSignal()   # emitted when user clicks Back

    def __init__(self, incident, db, parent=None):
        super().__init__(parent)
        self.incident = incident
        self.db       = db
        self._build()

    # ── helpers ──────────────────────────────────────────────────────────────

    def _s(self):
        return theme.STYLES

    def _card(self):
        f = QFrame()
        f.setStyleSheet(
            f"QFrame {{ background: {self._s()['bg_card']};"
            f" border: 1px solid {self._s()['border']}; border-radius: 10px; }}"
        )
        return f

    def _section_label(self, text):
        lbl = QLabel(text.upper())
        lbl.setFont(QFont("Arial", 10, QFont.Bold))
        lbl.setStyleSheet(
            f"color: {self._s()['text_muted']}; letter-spacing: 1px;"
            f" padding-bottom: 6px; border-bottom: 1px solid {self._s()['border']};"
        )
        return lbl

    def _meta_row(self, key, value):
        row = QHBoxLayout()
        row.setSpacing(0)
        k = QLabel(key)
        k.setFixedWidth(150)
        k.setStyleSheet(f"color: {self._s()['text_muted']}; font-size: 12px;")
        v = QLabel(str(value) if value else "—")
        v.setStyleSheet(
            f"color: {self._s()['text_main']}; font-size: 13px; font-weight: bold;"
        )
        v.setWordWrap(True)
        row.addWidget(k)
        row.addWidget(v, 1)
        return row

    def _priority_badge(self, p):
        colors = {
            "P1": ("#fee2e2", "#991b1b"),
            "P2": ("#ffedd5", "#9a3412"),
            "P3": ("#fef9c3", "#854d0e"),
            "P4": ("#dcfce7", "#166534"),
            "P5": ("#f3f4f6", "#374151"),
        }
        bg, fg = colors.get((p or "").upper(), ("#f3f4f6", "#374151"))
        lbl = QLabel(p or "—")
        lbl.setStyleSheet(
            f"background: {bg}; color: {fg}; font-size: 12px; font-weight: bold;"
            f" padding: 4px 12px; border-radius: 10px; border: none;"
        )
        return lbl

    def _status_badge(self, status):
        colors = {
            "pending":  ("#fef9c3", "#854d0e"),
            "ongoing":  ("#dbeafe", "#1e40af"),
            "assigned": ("#ede9fe", "#5b21b6"),
            "solved":   ("#dcfce7", "#166534"),
        }
        bg, fg = colors.get((status or "").lower(), ("#f3f4f6", "#374151"))
        label  = {
            "pending": "Pending", "ongoing": "In progress",
            "assigned": "Assigned", "solved": "Completed",
        }.get((status or "").lower(), status or "—")
        lbl = QLabel(label)
        lbl.setStyleSheet(
            f"background: {bg}; color: {fg}; font-size: 12px; font-weight: bold;"
            f" padding: 4px 12px; border-radius: 10px; border: none;"
        )
        return lbl

    def _person_card(self, name, uid, role, phone, email, extra=None):
        f = QFrame()
        f.setStyleSheet(
            f"QFrame {{ background: {self._s()['bg_input']};"
            f" border: 1px solid {self._s()['border']}; border-radius: 8px; }}"
        )
        lay = QHBoxLayout(f)
        lay.setContentsMargins(12, 10, 12, 10)
        lay.setSpacing(12)

        initials = "".join(w[0].upper() for w in (name or "?").split()[:2])
        av = QLabel(initials)
        av.setFixedSize(40, 40)
        av.setAlignment(Qt.AlignCenter)
        av.setFont(QFont("Arial", 14, QFont.Bold))
        av.setStyleSheet(
            "background: #dbeafe; color: #1e40af;"
            " border-radius: 20px; border: none;"
        )
        lay.addWidget(av)

        info = QVBoxLayout()
        info.setSpacing(2)
        n = QLabel(name or "—")
        n.setFont(QFont("Arial", 12, QFont.Bold))
        n.setStyleSheet(f"color: {self._s()['text_main']}; border: none;")
        sub = QLabel(f"{uid or '—'}  ·  {role or '—'}")
        sub.setStyleSheet(
            f"color: {self._s()['text_muted']}; font-size: 11px; border: none;"
        )
        info.addWidget(n)
        info.addWidget(sub)
        if phone:
            ph = QLabel(f"Phone: {phone}")
            ph.setStyleSheet(
                f"color: {self._s()['text_muted']}; font-size: 11px; border: none;"
            )
            info.addWidget(ph)
        if email:
            em = QLabel(f"Email: {email}")
            em.setStyleSheet(
                f"color: {self._s()['text_muted']}; font-size: 11px; border: none;"
            )
            info.addWidget(em)
        if extra:
            ex = QLabel(extra)
            ex.setStyleSheet(
                f"color: {self._s()['text_muted']}; font-size: 10px; border: none;"
            )
            info.addWidget(ex)

        lay.addLayout(info, 1)
        return f

    def _tl_item(self, ts, action, by, done=True, is_last=False):
        w = QWidget()
        h = QHBoxLayout(w)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(12)

        dot_col = QVBoxLayout()
        dot_col.setSpacing(0)
        dot_col.setAlignment(Qt.AlignTop)
        dot = QLabel()
        dot.setFixedSize(12, 12)
        dot.setStyleSheet(
            f"background: {'#1D9E75' if done else '#D1D5DB'};"
            f" border-radius: 6px; border: none;"
        )
        dot_col.addWidget(dot)
        if not is_last:
            line = QLabel()
            line.setFixedWidth(2)
            line.setMinimumHeight(24)
            line.setStyleSheet(
                f"background: {self._s()['border']}; border: none;"
            )
            line.setAlignment(Qt.AlignHCenter)
            dot_col.addWidget(line)
        h.addLayout(dot_col)

        text_col = QVBoxLayout()
        text_col.setSpacing(2)
        act = QLabel(action)
        act.setFont(QFont("Arial", 12, QFont.Bold))
        act.setStyleSheet(f"color: {self._s()['text_main']}; border: none;")
        act.setWordWrap(True)
        meta = QLabel(f"{ts}  ·  {by}")
        meta.setStyleSheet(
            f"color: {self._s()['text_muted']}; font-size: 11px; border: none;"
        )
        text_col.addWidget(act)
        text_col.addWidget(meta)
        h.addLayout(text_col, 1)
        return w

    # ── build ─────────────────────────────────────────────────────────────────

    def _build(self):
        inc = self.incident
        s   = self._s()

        # fetch reporter & responder user objects
        reporter  = self.db.get_user_by_id(inc.reporter_id)  if inc.reporter_id  else None
        responder = self.db.get_user_by_id(inc.responder_id) if inc.responder_id else None

        main = QVBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        container = QWidget()
        container.setMinimumWidth(600)
        lay = QVBoxLayout(container)
        lay.setContentsMargins(24, 20, 24, 24)
        lay.setSpacing(16)

        # ── back button ──────────────────────────────────────────────────────
        back_row = QHBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.setStyleSheet(
            f"QPushButton {{ background: transparent; color: {s['text_muted']};"
            f" border: none; font-size: 12px; padding: 0; }}"
            f"QPushButton:hover {{ color: {s['text_main']}; }}"
        )
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.clicked.connect(self.closed.emit)
        back_row.addWidget(back_btn)
        back_row.addStretch()
        lay.addLayout(back_row)

        # ── case header ──────────────────────────────────────────────────────
        hdr_card = self._card()
        hdr_lay  = QVBoxLayout(hdr_card)
        hdr_lay.setContentsMargins(20, 16, 20, 16)
        hdr_lay.setSpacing(10)

        top_row = QHBoxLayout()
        id_lbl = QLabel(f"CASE FILE  /  {inc.id}")
        id_lbl.setStyleSheet(
            f"color: {s['text_muted']}; font-size: 11px;"
            f" font-family: monospace; border: none;"
        )
        top_row.addWidget(id_lbl)
        top_row.addStretch()
        created_lbl = QLabel(
            f"Created: {inc.created_at.strftime('%b %d, %Y  %H:%M')}"
            if inc.created_at else ""
        )
        created_lbl.setStyleSheet(
            f"color: {s['text_muted']}; font-size: 12px; border: none;"
        )
        top_row.addWidget(created_lbl)
        hdr_lay.addLayout(top_row)

        type_lbl = QLabel(
            get_incident_display_name(inc.type) if inc.type else inc.type or "—"
        )
        type_lbl.setFont(QFont("Arial", 20, QFont.Bold))
        type_lbl.setStyleSheet(f"color: {s['text_main']}; border: none;")
        hdr_lay.addWidget(type_lbl)

        badge_row = QHBoxLayout()
        badge_row.setSpacing(8)
        badge_row.addWidget(self._priority_badge(inc.priority))
        badge_row.addWidget(self._status_badge(inc.status))
        badge_row.addStretch()
        hdr_lay.addLayout(badge_row)

        # incident details below badges
        hdr_lay.addWidget(self._build_divider())
        details_grid = QVBoxLayout()
        details_grid.setSpacing(5)
        details_grid.addLayout(self._meta_row("Location", inc.location))
        details_grid.addLayout(self._meta_row("Category", inc.incident_category or "—"))
        details_grid.addLayout(self._meta_row("Description", inc.description))
        if inc.emergency_feedback:
            details_grid.addLayout(self._meta_row("Emergency feedback", inc.emergency_feedback))
        hdr_lay.addLayout(details_grid)

        lay.addWidget(hdr_card)

        # ── people ───────────────────────────────────────────────────────────
        people_row = QHBoxLayout()
        people_row.setSpacing(12)

        rep_card = self._card()
        rep_lay  = QVBoxLayout(rep_card)
        rep_lay.setContentsMargins(16, 14, 16, 14)
        rep_lay.setSpacing(8)
        rep_lay.addWidget(self._section_label("Reporter"))
        rep_lay.addWidget(self._person_card(
            inc.reporter_name,
            inc.reporter_id,
            "Reporter",
            reporter.phone  if reporter else "—",
            reporter.email  if reporter else "—",
        ))
        rep_lay.addStretch()
        people_row.addWidget(rep_card, 1)

        resp_card = self._card()
        resp_lay  = QVBoxLayout(resp_card)
        resp_lay.setContentsMargins(16, 14, 16, 14)
        resp_lay.setSpacing(8)
        resp_lay.addWidget(self._section_label("Assigned responder"))
        if responder:
            resp_lay.addWidget(self._person_card(
                inc.responder_name,
                inc.responder_id,
                "Responder",
                responder.phone or "—",
                responder.email or "—",
                f"Category: {responder.responder_category or '—'}",
            ))
        else:
            no_resp = QLabel("No responder assigned yet.")
            no_resp.setStyleSheet(
                f"color: {s['text_muted']}; font-size: 12px; border: none;"
            )
            resp_lay.addWidget(no_resp)
        resp_lay.addStretch()
        people_row.addWidget(resp_card, 1)

        lay.addLayout(people_row)

        # ── timeline ─────────────────────────────────────────────────────────
        tl_card = self._card()
        tl_lay  = QVBoxLayout(tl_card)
        tl_lay.setContentsMargins(16, 14, 16, 14)
        tl_lay.setSpacing(4)
        tl_lay.addWidget(self._section_label("Case timeline"))

        tl_events = []
        tl_events.append((
            inc.created_at.strftime("%b %d, %Y  %H:%M") if inc.created_at else "—",
            "Report created",
            inc.reporter_name or "Reporter",
            True
        ))
        if inc.responder_id:
            tl_events.append((
                inc.updated_at.strftime("%b %d, %Y  %H:%M") if inc.updated_at else "—",
                f"Case assigned to {inc.responder_name or 'responder'}",
                "Admin",
                True
            ))
            tl_events.append((
                inc.updated_at.strftime("%b %d, %Y  %H:%M") if inc.updated_at else "—",
                "Responder acknowledged — en route",
                inc.responder_name or "Responder",
                True
            ))
        if inc.status == "solved":
            tl_events.append((
                inc.updated_at.strftime("%b %d, %Y  %H:%M") if inc.updated_at else "—",
                "Case resolved and closed",
                inc.responder_name or "Responder",
                True
            ))
        elif inc.status in ("ongoing", "assigned"):
            tl_events.append((
                "—",
                "Awaiting resolution",
                "System",
                False
            ))

        for idx, (ts, action, by, done) in enumerate(tl_events):
            tl_lay.addWidget(
                self._tl_item(ts, action, by, done, idx == len(tl_events) - 1)
            )

        lay.addWidget(tl_card)

        # ── actions + attachments ─────────────────────────────────────────────
        lower_row = QHBoxLayout()
        lower_row.setSpacing(12)

        act_card = self._card()
        act_lay  = QVBoxLayout(act_card)
        act_lay.setContentsMargins(16, 14, 16, 14)
        act_lay.setSpacing(8)
        act_lay.addWidget(self._section_label("Actions taken"))

        actions_taken = []
        if inc.responder_id:
            actions_taken.append(
                f"Responder {inc.responder_name or ''} dispatched to {inc.location or 'scene'}"
            )
        if inc.status == "solved":
            actions_taken.append("Incident contained — all-clear issued")
            actions_taken.append("Final status report submitted")
        elif inc.status in ("ongoing", "assigned"):
            actions_taken.append("Response operation in progress")
        if not actions_taken:
            actions_taken.append("No actions logged yet.")

        for action in actions_taken:
            row = QHBoxLayout()
            row.setSpacing(8)
            check = QLabel("✓")
            check.setStyleSheet("color: #1D9E75; font-size: 13px; border: none;")
            check.setFixedWidth(16)
            act_lbl = QLabel(action)
            act_lbl.setStyleSheet(
                f"color: {s['text_main']}; font-size: 12px; border: none;"
            )
            act_lbl.setWordWrap(True)
            row.addWidget(check)
            row.addWidget(act_lbl, 1)
            act_lay.addLayout(row)
            sep = self._build_divider()
            act_lay.addWidget(sep)

        act_lay.addStretch()
        lower_row.addWidget(act_card, 1)

        # notes / internal logs
        notes_card = self._card()
        notes_lay  = QVBoxLayout(notes_card)
        notes_lay.setContentsMargins(16, 14, 16, 14)
        notes_lay.setSpacing(8)
        notes_lay.addWidget(self._section_label("Internal notes"))

        notes = []
        if inc.specific_questions:
            for k, v in inc.specific_questions.items():
                if v:
                    notes.append(f"{k.replace('_', ' ').title()}: {v}")
        if not notes:
            notes.append("No additional notes.")

        for note in notes:
            nf = QFrame()
            nf.setStyleSheet(
                f"QFrame {{ background: {s['bg_input']};"
                f" border-left: 3px solid {s['border']};"
                f" border-radius: 0 6px 6px 0; }}"
            )
            nf_lay = QVBoxLayout(nf)
            nf_lay.setContentsMargins(10, 7, 10, 7)
            nl = QLabel(note)
            nl.setStyleSheet(
                f"color: {s['text_main']}; font-size: 12px; border: none;"
            )
            nl.setWordWrap(True)
            nf_lay.addWidget(nl)
            notes_lay.addWidget(nf)

        notes_lay.addStretch()
        lower_row.addWidget(notes_card, 1)
        lay.addLayout(lower_row)

        # ── final report (only for solved incidents) ──────────────────────────
        if inc.status == "solved":
            fr_card = self._card()
            fr_lay  = QVBoxLayout(fr_card)
            fr_lay.setContentsMargins(16, 14, 16, 14)
            fr_lay.setSpacing(10)
            fr_lay.addWidget(self._section_label("Final report"))

            outcome_row = QHBoxLayout()
            outcome_row.setSpacing(10)

            for label, value, color in [
                ("Outcome",     "Success",  "#1D9E75"),
                ("Casualties",  "None",     "#1D9E75"),
                ("Duration",
                 self._duration(inc.created_at, inc.updated_at), "#378ADD"),
            ]:
                fc = QFrame()
                fc.setStyleSheet(
                    f"QFrame {{ background: {s['bg_input']};"
                    f" border: 1px solid {s['border']}; border-radius: 8px; }}"
                )
                fc_lay = QVBoxLayout(fc)
                fc_lay.setContentsMargins(14, 10, 14, 10)
                fv = QLabel(value)
                fv.setFont(QFont("Arial", 18, QFont.Bold))
                fv.setStyleSheet(f"color: {color}; border: none;")
                fv.setAlignment(Qt.AlignCenter)
                fl = QLabel(label)
                fl.setStyleSheet(
                    f"color: {s['text_muted']}; font-size: 11px; border: none;"
                )
                fl.setAlignment(Qt.AlignCenter)
                fc_lay.addWidget(fv)
                fc_lay.addWidget(fl)
                outcome_row.addWidget(fc)

            fr_lay.addLayout(outcome_row)
            lay.addWidget(fr_card)

        scroll.setWidget(container)
        main.addWidget(scroll)

    # ── utils ─────────────────────────────────────────────────────────────────

    def _build_divider(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"color: {self._s()['border']}; border: none;")
        return line

    @staticmethod
    def _duration(start, end):
        if not start or not end:
            return "—"
        delta = int((end - start).total_seconds())
        h, m  = divmod(delta // 60, 60)
        return f"{h}h {m}m" if h else f"{m}m"
