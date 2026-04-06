# admin/user_dossier.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QTableWidget, QTableWidgetItem,
    QHeaderView, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor

from styles import theme


class UserDossier(QWidget):
    """Full dossier view for a single user. Emits open_case(incident_id) when
    the admin clicks 'View case' inside the activity table."""

    open_case = pyqtSignal(str)   # carries incident id

    def __init__(self, user, db, parent=None):
        super().__init__(parent)
        self.subject   = user   # the user being viewed (not the logged-in admin)
        self.db        = db
        self._build()

    # ── helpers ──────────────────────────────────────────────────────────────

    def _s(self):
        return theme.STYLES

    def _card(self):
        f = QFrame()
        f.setStyleSheet(
            f"QFrame {{ background: {self._s()['bg_card']};"
            f" border: 1px solid {self._s()['border']};"
            f" border-radius: 10px; }}"
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
        k.setFixedWidth(160)
        k.setStyleSheet(f"color: {self._s()['text_muted']}; font-size: 12px;")
        v = QLabel(str(value) if value else "—")
        v.setStyleSheet(
            f"color: {self._s()['text_main']}; font-size: 13px; font-weight: bold;"
        )
        v.setWordWrap(True)
        row.addWidget(k)
        row.addWidget(v, 1)
        return row

    def _status_badge(self, status):
        colors = {
            "available": ("#d1fae5", "#065f46"),
            "active":    ("#d1fae5", "#065f46"),
            "busy":      ("#fef3c7", "#92400e"),
            "suspended": ("#fee2e2", "#991b1b"),
        }
        bg, fg = colors.get((status or "").lower(), ("#e5e7eb", "#374151"))
        lbl = QLabel(status.title() if status else "Unknown")
        lbl.setStyleSheet(
            f"background: {bg}; color: {fg}; font-size: 11px; font-weight: bold;"
            f" padding: 3px 10px; border-radius: 10px;"
        )
        lbl.setFixedHeight(22)
        return lbl

    def _priority_badge(self, priority):
        colors = {
            "P1": ("#fee2e2", "#991b1b"),
            "P2": ("#ffedd5", "#9a3412"),
            "P3": ("#fef9c3", "#854d0e"),
            "P4": ("#dcfce7", "#166534"),
            "P5": ("#f3f4f6", "#374151"),
        }
        bg, fg = colors.get((priority or "").upper(), ("#f3f4f6", "#374151"))
        lbl = QLabel(priority or "—")
        lbl.setStyleSheet(
            f"background: {bg}; color: {fg}; font-size: 11px; font-weight: bold;"
            f" padding: 3px 10px; border-radius: 10px;"
        )
        lbl.setFixedHeight(22)
        return lbl

    def _incident_status_badge(self, status):
        colors = {
            "pending":  ("#fef9c3", "#854d0e"),
            "ongoing":  ("#dbeafe", "#1e40af"),
            "solved":   ("#dcfce7", "#166534"),
            "assigned": ("#ede9fe", "#5b21b6"),
        }
        bg, fg = colors.get((status or "").lower(), ("#f3f4f6", "#374151"))
        lbl = QLabel(status.title() if status else "—")
        lbl.setStyleSheet(
            f"background: {bg}; color: {fg}; font-size: 11px; font-weight: bold;"
            f" padding: 3px 10px; border-radius: 10px;"
        )
        lbl.setFixedHeight(22)
        return lbl

    def _stat_card(self, label, value, color="#378ADD"):
        f = QFrame()
        f.setStyleSheet(
            f"QFrame {{ background: {self._s()['bg_input']};"
            f" border: 1px solid {self._s()['border']}; border-radius: 8px; }}"
        )
        f.setMinimumHeight(80)
        lay = QVBoxLayout(f)
        lay.setContentsMargins(14, 10, 14, 10)
        lay.setSpacing(4)
        num = QLabel(str(value))
        num.setFont(QFont("Arial", 22, QFont.Bold))
        num.setStyleSheet(f"color: {color}; border: none;")
        num.setAlignment(Qt.AlignCenter)
        lbl = QLabel(label)
        lbl.setStyleSheet(
            f"color: {self._s()['text_muted']}; font-size: 11px; border: none;"
        )
        lbl.setAlignment(Qt.AlignCenter)
        lay.addWidget(num)
        lay.addWidget(lbl)
        return f

    # ── build ─────────────────────────────────────────────────────────────────

    def _build(self):
        s      = self.subject
        all_i  = self.db.get_all_incidents()

        if s.role == "responder":
            incidents = self.db.get_incidents_by_responder(s.id)
        else:
            incidents = self.db.get_incidents_by_reporter(s.id)

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
        back_btn = QPushButton("← Back to Users")
        back_btn.setStyleSheet(
            f"QPushButton {{ background: transparent; color: {self._s()['text_muted']};"
            f" border: none; font-size: 12px; padding: 0; }}"
            f"QPushButton:hover {{ color: {self._s()['text_main']}; }}"
        )
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.clicked.connect(self.close_dossier)
        back_row.addWidget(back_btn)
        back_row.addStretch()
        lay.addLayout(back_row)

        # ── identity card ────────────────────────────────────────────────────
        id_card = self._card()
        id_lay  = QHBoxLayout(id_card)
        id_lay.setContentsMargins(20, 20, 20, 20)
        id_lay.setSpacing(24)

        # avatar circle
        initials = "".join(w[0].upper() for w in (s.name or "?").split()[:2])
        av = QLabel(initials)
        av.setFixedSize(72, 72)
        av.setAlignment(Qt.AlignCenter)
        av.setFont(QFont("Arial", 22, QFont.Bold))
        av.setStyleSheet(
            "background: #dbeafe; color: #1e40af; border-radius: 36px;"
            " border: none;"
        )
        id_lay.addWidget(av)

        # left info block
        info = QVBoxLayout()
        info.setSpacing(6)

        name_row = QHBoxLayout()
        name_row.setSpacing(10)
        name_lbl = QLabel(s.name or "—")
        name_lbl.setFont(QFont("Arial", 18, QFont.Bold))
        name_lbl.setStyleSheet(
            f"color: {self._s()['text_main']}; border: none;"
        )
        name_row.addWidget(name_lbl)
        name_row.addWidget(self._status_badge(s.status))
        role_colors = {
            "admin":     ("#fee2e2", "#991b1b"),
            "responder": ("#dbeafe", "#1e40af"),
            "reporter":  ("#dcfce7", "#166534"),
        }
        rbg, rfg = role_colors.get(s.role, ("#f3f4f6", "#374151"))
        role_badge = QLabel(s.role.title())
        role_badge.setStyleSheet(
            f"background: {rbg}; color: {rfg}; font-size: 11px; font-weight: bold;"
            f" padding: 3px 10px; border-radius: 10px; border: none;"
        )
        name_row.addWidget(role_badge)
        name_row.addStretch()
        info.addLayout(name_row)

        grid = QVBoxLayout()
        grid.setSpacing(4)
        grid.addLayout(self._meta_row("User ID", s.id))
        grid.addLayout(self._meta_row("Username", s.username))
        grid.addLayout(self._meta_row("Email", s.email))
        grid.addLayout(self._meta_row("Phone", s.phone))
        grid.addLayout(self._meta_row("Active incidents", s.active_incidents))
        if s.responder_category:
            grid.addLayout(self._meta_row("Specialization", s.responder_category))
        grid.addLayout(self._meta_row(
            "Member since",
            s.created_at.strftime("%b %d, %Y") if s.created_at else "—"
        ))
        info.addLayout(grid)
        id_lay.addLayout(info, 1)

        # photo placeholder on the right
        photo = QFrame()
        photo.setFixedSize(90, 90)
        photo.setStyleSheet(
            f"QFrame {{ background: {self._s()['bg_input']};"
            f" border: 1px solid {self._s()['border']}; border-radius: 8px; }}"
        )
        photo_lay = QVBoxLayout(photo)
        ph_lbl = QLabel("No photo")
        ph_lbl.setAlignment(Qt.AlignCenter)
        ph_lbl.setStyleSheet(
            f"color: {self._s()['text_muted']}; font-size: 10px; border: none;"
        )
        photo_lay.addWidget(ph_lbl)
        id_lay.addWidget(photo)

        lay.addWidget(id_card)

        # ── stats ────────────────────────────────────────────────────────────
        stats_card = self._card()
        stats_outer = QVBoxLayout(stats_card)
        stats_outer.setContentsMargins(16, 14, 16, 14)
        stats_outer.addWidget(self._section_label("Performance summary"))
        stats_row = QHBoxLayout()
        stats_row.setSpacing(10)

        total    = len(incidents)
        active   = len([i for i in incidents if i.status in ("ongoing", "assigned")])
        solved   = len([i for i in incidents if i.status == "solved"])
        pending  = len([i for i in incidents if i.status == "pending"])
        rate     = f"{int(solved/total*100)}%" if total > 0 else "—"

        if s.role == "responder":
            stats_row.addWidget(self._stat_card("Total cases", total, "#378ADD"))
            stats_row.addWidget(self._stat_card("Active", active, "#BA7517"))
            stats_row.addWidget(self._stat_card("Completed", solved, "#1D9E75"))
            stats_row.addWidget(self._stat_card("Success rate", rate, "#1D9E75"))
            stats_row.addWidget(
                self._stat_card("Active incidents", s.active_incidents, "#534AB7")
            )
        else:
            valid   = len([i for i in incidents if i.status == "solved"])
            false_r = len([i for i in incidents if i.status == "pending" and
                           (i.updated_at - i.created_at).total_seconds() > 86400])
            acc = f"{int(valid/total*100)}%" if total > 0 else "—"
            stats_row.addWidget(self._stat_card("Total reports", total, "#378ADD"))
            stats_row.addWidget(self._stat_card("Valid reports", valid, "#1D9E75"))
            stats_row.addWidget(self._stat_card("Pending", pending, "#BA7517"))
            stats_row.addWidget(self._stat_card("Accuracy", acc, "#1D9E75"))

        stats_outer.addLayout(stats_row)
        lay.addWidget(stats_card)

        # ── activity history table ───────────────────────────────────────────
        hist_card = self._card()
        hist_lay  = QVBoxLayout(hist_card)
        hist_lay.setContentsMargins(16, 14, 16, 14)
        hist_lay.setSpacing(10)

        hist_header = QHBoxLayout()
        hist_header.addWidget(self._section_label("Activity history"))
        count_lbl = QLabel(f"{total} total entries")
        count_lbl.setStyleSheet(
            f"color: {self._s()['text_muted']}; font-size: 11px;"
        )
        hist_header.addStretch()
        hist_header.addWidget(count_lbl)
        hist_lay.addLayout(hist_header)

        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(
            ["Case ID", "Incident type", "Role", "Date & time", "Priority", "Status"]
        )
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.horizontalHeader().setStyleSheet(
            f"QHeaderView::section {{ background: {self._s()['bg_input']};"
            f" color: {self._s()['text_muted']}; font-size: 11px; font-weight: bold;"
            f" padding: 6px; border: none;"
            f" border-bottom: 1px solid {self._s()['border']}; }}"
        )
        table.setStyleSheet(
            f"QTableWidget {{ background: {self._s()['bg_card']};"
            f" color: {self._s()['text_main']}; border: none; gridline-color: {self._s()['border']}; }}"
            f"QTableWidget::item {{ padding: 6px; }}"
            f"QTableWidget::item:selected {{ background: {self._s()['bg_input']}; }}"
        )
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setAlternatingRowColors(False)
        table.verticalHeader().setVisible(False)
        table.setShowGrid(True)
        table.setRowCount(len(incidents))

        for row, inc in enumerate(incidents):
            # Case ID — clickable style
            id_item = QTableWidgetItem(inc.id)
            id_item.setForeground(QColor("#185FA5"))
            id_item.setFont(QFont("Arial", 11, QFont.Bold))
            table.setItem(row, 0, id_item)

            table.setItem(row, 1, QTableWidgetItem(
                (inc.incident_category or inc.type or "—").title()
            ))

            role_item = QTableWidgetItem(s.role.title())
            table.setItem(row, 2, role_item)

            dt = inc.created_at.strftime("%b %d %Y  %H:%M") if inc.created_at else "—"
            dt_item = QTableWidgetItem(dt)
            dt_item.setForeground(QColor(self._s()['text_muted']))
            table.setItem(row, 3, dt_item)

            p_item = QTableWidgetItem(inc.priority or "—")
            pcolor = {
                "P1": QColor(220, 38, 38), "P2": QColor(234, 88, 12),
                "P3": QColor(202, 138, 4),  "P4": QColor(22, 163, 74),
            }.get((inc.priority or "").upper(), QColor(107, 114, 128))
            p_item.setForeground(pcolor)
            p_item.setFont(QFont("Arial", 11, QFont.Bold))
            table.setItem(row, 4, p_item)

            st_item = QTableWidgetItem((inc.status or "—").title())
            scolor = {
                "pending":  QColor(202, 138, 4),
                "ongoing":  QColor(37, 99, 235),
                "solved":   QColor(22, 163, 74),
                "assigned": QColor(124, 58, 237),
            }.get((inc.status or "").lower(), QColor(107, 114, 128))
            st_item.setForeground(scolor)
            st_item.setFont(QFont("Arial", 11, QFont.Bold))
            table.setItem(row, 5, st_item)

            table.setRowHeight(row, 38)

        # double-click a row to open the case file
        table.cellDoubleClicked.connect(
            lambda r, _: self._on_view_case(incidents[r].id) if r < len(incidents) else None
        )

        hist_lay.addWidget(table)

        # View case button below table
        view_btn_row = QHBoxLayout()
        view_btn_row.addStretch()
        view_case_btn = QPushButton("Open selected case →")
        view_case_btn.setStyleSheet(
            f"QPushButton {{ background: #3498db; color: white; border: none;"
            f" padding: 7px 18px; border-radius: 6px; font-size: 12px; font-weight: bold; }}"
            f"QPushButton:hover {{ background: #2980b9; }}"
        )
        view_case_btn.setCursor(Qt.PointingHandCursor)
        view_case_btn.clicked.connect(
            lambda: self._on_view_selected(table, incidents)
        )
        view_btn_row.addWidget(view_case_btn)
        hist_lay.addLayout(view_btn_row)

        lay.addWidget(hist_card)

        # ── bottom two columns: timeline + notes ─────────────────────────────
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(12)

        # Timeline
        tl_card = self._card()
        tl_lay  = QVBoxLayout(tl_card)
        tl_lay.setContentsMargins(16, 14, 16, 14)
        tl_lay.setSpacing(8)
        tl_lay.addWidget(self._section_label("Activity timeline"))

        tl_events = []
        if s.created_at:
            tl_events.append((
                s.created_at.strftime("%b %d, %Y"),
                "Account created",
                "System", True
            ))
        for inc in sorted(incidents, key=lambda x: x.created_at):
            tl_events.append((
                inc.created_at.strftime("%b %d, %Y  %H:%M"),
                f"{inc.id} — {(inc.incident_category or inc.type or '').title()} reported",
                inc.reporter_name or "Reporter", True
            ))
            if inc.responder_name:
                tl_events.append((
                    inc.updated_at.strftime("%b %d, %Y  %H:%M") if inc.updated_at else "—",
                    f"{inc.id} — assigned to {inc.responder_name}",
                    "Admin", True
                ))
            if inc.status == "solved":
                tl_events.append((
                    inc.updated_at.strftime("%b %d, %Y  %H:%M") if inc.updated_at else "—",
                    f"{inc.id} — completed",
                    inc.responder_name or "Responder", True
                ))

        for idx, (ts, action, by, done) in enumerate(tl_events[-8:]):
            item_w  = QWidget()
            item_h  = QHBoxLayout(item_w)
            item_h.setContentsMargins(0, 0, 0, 0)
            item_h.setSpacing(10)

            dot = QLabel()
            dot.setFixedSize(10, 10)
            color_dot = "#1D9E75" if done else "#378ADD"
            dot.setStyleSheet(
                f"background: {color_dot}; border-radius: 5px; border: none;"
            )
            item_h.addWidget(dot)
            item_h.setAlignment(dot, Qt.AlignTop)
            item_h.setContentsMargins(0, 4, 0, 0)

            text_col = QVBoxLayout()
            text_col.setSpacing(2)
            act_lbl = QLabel(action)
            act_lbl.setFont(QFont("Arial", 11, QFont.Bold))
            act_lbl.setStyleSheet(
                f"color: {self._s()['text_main']}; border: none;"
            )
            act_lbl.setWordWrap(True)
            sub_lbl = QLabel(f"{ts}  ·  {by}")
            sub_lbl.setStyleSheet(
                f"color: {self._s()['text_muted']}; font-size: 10px; border: none;"
            )
            text_col.addWidget(act_lbl)
            text_col.addWidget(sub_lbl)
            item_h.addLayout(text_col, 1)

            tl_lay.addWidget(item_w)

        tl_lay.addStretch()
        bottom_row.addWidget(tl_card, 1)

        # Notes & flags
        notes_card = self._card()
        notes_lay  = QVBoxLayout(notes_card)
        notes_lay.setContentsMargins(16, 14, 16, 14)
        notes_lay.setSpacing(8)
        notes_lay.addWidget(self._section_label("Notes & flags"))

        # warning flag if any active incidents over-running
        overdue = [
            i for i in incidents
            if i.status == "ongoing" and
            (i.updated_at - i.created_at).total_seconds() > 7200
        ]
        if overdue:
            for inc in overdue[:3]:
                flag = QFrame()
                flag.setStyleSheet(
                    "QFrame { background: #fee2e2; border-left: 3px solid #dc2626;"
                    " border-radius: 0 6px 6px 0; }"
                )
                flag_lay = QVBoxLayout(flag)
                flag_lay.setContentsMargins(10, 7, 10, 7)
                flag_lay.setSpacing(2)
                ft = QLabel(f"Case overdue — {inc.id}")
                ft.setFont(QFont("Arial", 11, QFont.Bold))
                ft.setStyleSheet("color: #991b1b; border: none;")
                fs = QLabel(
                    f"Ongoing for "
                    f"{int((inc.updated_at - inc.created_at).total_seconds()//3600)}h"
                    f"  ·  {inc.location or '—'}"
                )
                fs.setStyleSheet("color: #6b7280; font-size: 10px; border: none;")
                flag_lay.addWidget(ft)
                flag_lay.addWidget(fs)
                notes_lay.addWidget(flag)

        # static admin note
        note = QFrame()
        note.setStyleSheet(
            f"QFrame {{ background: {self._s()['bg_input']};"
            f" border-left: 3px solid {self._s()['border']};"
            f" border-radius: 0 6px 6px 0; }}"
        )
        note_lay = QVBoxLayout(note)
        note_lay.setContentsMargins(10, 7, 10, 7)
        note_lay.setSpacing(2)
        nt = QLabel("Admin note")
        nt.setFont(QFont("Arial", 11, QFont.Bold))
        nt.setStyleSheet(f"color: {self._s()['text_main']}; border: none;")
        ns = QLabel(
            f"Account in good standing. Active since "
            f"{s.created_at.strftime('%b %Y') if s.created_at else '—'}."
        )
        ns.setStyleSheet(
            f"color: {self._s()['text_muted']}; font-size: 11px; border: none;"
        )
        ns.setWordWrap(True)
        note_lay.addWidget(nt)
        note_lay.addWidget(ns)
        notes_lay.addWidget(note)

        notes_lay.addStretch()
        bottom_row.addWidget(notes_card, 1)
        lay.addLayout(bottom_row)

        scroll.setWidget(container)
        main.addWidget(scroll)

    # ── actions ───────────────────────────────────────────────────────────────

    def _on_view_case(self, incident_id):
        self.open_case.emit(incident_id)

    def _on_view_selected(self, table, incidents):
        row = table.currentRow()
        if 0 <= row < len(incidents):
            self.open_case.emit(incidents[row].id)

    def close_dossier(self):
        """Tell the parent (AdminUsers) to go back to the user list."""
        self.hide()
        parent = self.parent()
        if parent and hasattr(parent, "show_user_list"):
            parent.show_user_list()
