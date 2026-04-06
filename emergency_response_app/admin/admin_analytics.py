# admin/admin_analytics.py
from collections import defaultdict
from datetime import datetime, timedelta

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QTableWidget, QTableWidgetItem,
    QHeaderView, QComboBox, QSizePolicy, QStackedWidget,
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor, QPainter, QPen, QBrush, QPainterPath
from PyQt5.QtChart import (
    QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis,
    QValueAxis, QPieSeries, QLineSeries, QDateTimeAxis,
)
from PyQt5.QtCore import QDateTime

from styles import theme


# ─────────────────────────────────────────────────────────────────────────────
# Tiny reusable widgets
# ─────────────────────────────────────────────────────────────────────────────

class _Card(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._apply_style()

    def _apply_style(self):
        s = theme.STYLES
        self.setStyleSheet(
            f"QFrame {{ background: {s['bg_card']};"
            f" border: 1px solid {s['border']}; border-radius: 10px; }}"
        )


class _SectionTitle(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text.upper(), parent)
        self.setFont(QFont("Arial", 10, QFont.Bold))
        s = theme.STYLES
        self.setStyleSheet(
            f"color: {s['text_muted']}; letter-spacing: 1px;"
            f" padding-bottom: 6px; border-bottom: 1px solid {s['border']};"
            f" border-radius: 0;"
        )


class _StatCard(QFrame):
    def __init__(self, label, value, color="#378ADD", parent=None):
        super().__init__(parent)
        self.setMinimumHeight(84)
        s = theme.STYLES
        self.setStyleSheet(
            f"QFrame {{ background: {s['bg_input']};"
            f" border: 1px solid {s['border']}; border-radius: 8px; }}"
        )
        lay = QVBoxLayout(self)
        lay.setContentsMargins(14, 10, 14, 10)
        lay.setSpacing(4)
        self._num = QLabel(str(value))
        self._num.setFont(QFont("Arial", 24, QFont.Bold))
        self._num.setStyleSheet(f"color: {color}; border: none;")
        self._num.setAlignment(Qt.AlignCenter)
        lbl = QLabel(label)
        lbl.setStyleSheet(
            f"color: {s['text_muted']}; font-size: 11px; border: none;"
        )
        lbl.setAlignment(Qt.AlignCenter)
        lay.addWidget(self._num)
        lay.addWidget(lbl)

    def set_value(self, v):
        self._num.setText(str(v))


class _TabBar(QWidget):
    """Simple flat tab bar — calls on_select(index) on click."""

    def __init__(self, labels, on_select, parent=None):
        super().__init__(parent)
        self._btns = []
        self._cb   = on_select
        h = QHBoxLayout(self)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(4)
        for i, lbl in enumerate(labels):
            btn = QPushButton(lbl)
            btn.setCheckable(True)
            btn.setChecked(i == 0)
            btn.clicked.connect(lambda _, idx=i: self._select(idx))
            btn.setFixedHeight(30)
            btn.setStyleSheet(self._style(i == 0))
            self._btns.append(btn)
            h.addWidget(btn)
        h.addStretch()

    def _style(self, active):
        s = theme.STYLES
        if active:
            return (
                "QPushButton { background: #3498db; color: white; border: none;"
                " padding: 0 14px; border-radius: 6px; font-size: 12px; font-weight: bold; }"
            )
        return (
            f"QPushButton {{ background: transparent; color: {s['text_muted']};"
            f" border: 1px solid {s['border']}; padding: 0 14px;"
            f" border-radius: 6px; font-size: 12px; }}"
            f"QPushButton:hover {{ background: {s['bg_input']}; }}"
        )

    def _select(self, idx):
        for i, btn in enumerate(self._btns):
            btn.setChecked(i == idx)
            btn.setStyleSheet(self._style(i == idx))
        self._cb(idx)


def _combo(items):
    s = theme.STYLES
    c = QComboBox()
    c.addItems(items)
    c.setFixedHeight(30)
    c.setStyleSheet(
        f"QComboBox {{ background: {s['bg_card']}; color: {s['text_main']};"
        f" border: 1px solid {s['border']}; border-radius: 6px;"
        f" padding: 0 10px; font-size: 12px; }}"
        f"QComboBox::drop-down {{ border: none; }}"
        f"QComboBox QAbstractItemView {{ background: {s['bg_card']};"
        f" color: {s['text_main']}; selection-background-color: #3498db;"
        f" selection-color: white; }}"
    )
    return c


def _styled_table(columns):
    s = theme.STYLES
    t = QTableWidget()
    t.setColumnCount(len(columns))
    t.setHorizontalHeaderLabels(columns)
    t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    t.horizontalHeader().setStyleSheet(
        f"QHeaderView::section {{ background: {s['bg_input']};"
        f" color: {s['text_muted']}; font-size: 11px; font-weight: bold;"
        f" padding: 7px; border: none;"
        f" border-bottom: 1px solid {s['border']}; }}"
    )
    t.setStyleSheet(
        f"QTableWidget {{ background: {s['bg_card']}; color: {s['text_main']};"
        f" border: none; gridline-color: {s['border']}; }}"
        f"QTableWidget::item {{ padding: 6px; }}"
        f"QTableWidget::item:selected {{ background: {s['bg_input']}; }}"
    )
    t.setEditTriggers(QTableWidget.NoEditTriggers)
    t.setSelectionBehavior(QTableWidget.SelectRows)
    t.verticalHeader().setVisible(False)
    t.setShowGrid(True)
    t.setAlternatingRowColors(False)
    return t


PRIORITY_COLORS = {
    "P1": "#dc2626", "P2": "#ea580c",
    "P3": "#ca8a04", "P4": "#16a34a", "P5": "#6b7280",
}
STATUS_COLORS = {
    "pending":  "#ca8a04",
    "ongoing":  "#2563eb",
    "assigned": "#7c3aed",
    "solved":   "#16a34a",
}
CATEGORY_COLORS = [
    "#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6",
    "#1abc9c", "#e67e22", "#34495e", "#e91e63", "#00bcd4",
    "#8bc34a", "#ff5722", "#607d8b", "#795548", "#ff9800",
]


# ─────────────────────────────────────────────────────────────────────────────
# Chart helpers
# ─────────────────────────────────────────────────────────────────────────────

def _make_chart_view(chart):
    s     = theme.STYLES
    is_dk = s.get("is_dark", False)
    chart.setBackgroundBrush(QBrush(QColor(s["bg_card"])))
    chart.setPlotAreaBackgroundVisible(False)
    chart.legend().setLabelColor(QColor(s["text_main"]))
    chart.legend().setVisible(True)
    chart.setAnimationOptions(QChart.SeriesAnimations)
    v = QChartView(chart)
    v.setRenderHint(QPainter.Antialiasing)
    v.setStyleSheet(f"background: {s['bg_card']}; border: none;")
    return v


def _axis_style(axis):
    s = theme.STYLES
    axis.setLabelsColor(QColor(s["text_muted"]))
    axis.setGridLineColor(QColor(s["border"]))
    axis.setLinePenColor(QColor(s["border"]))


def _build_bar_chart(labels, values, colors, title=""):
    chart = QChart()
    chart.setTitle(title)
    chart.setTitleFont(QFont("Arial", 11, QFont.Bold))

    series = QBarSeries()
    for lbl, val, col in zip(labels, values, colors):
        bs = QBarSet(lbl)
        bs.append(val)
        bs.setColor(QColor(col))
        bs.setLabelColor(QColor(col))
        series.append(bs)

    chart.addSeries(series)

    axis_x = QBarCategoryAxis()
    axis_x.append([""])
    _axis_style(axis_x)
    chart.addAxis(axis_x, Qt.AlignBottom)
    series.attachAxis(axis_x)

    axis_y = QValueAxis()
    axis_y.setMin(0)
    axis_y.setMax(max(values) * 1.2 + 1 if values else 10)
    axis_y.setTickCount(5)
    axis_y.setLabelFormat("%d")
    _axis_style(axis_y)
    chart.addAxis(axis_y, Qt.AlignLeft)
    series.attachAxis(axis_y)

    chart.legend().setAlignment(Qt.AlignBottom)
    return _make_chart_view(chart)


def _build_pie_chart(labels, values, colors):
    chart  = QChart()
    series = QPieSeries()
    total  = sum(values) or 1
    for lbl, val, col in zip(labels, values, colors):
        sl = series.append(f"{lbl}  {val}", val)
        sl.setColor(QColor(col))
        sl.setLabelColor(QColor(theme.STYLES["text_main"]))
        if val == max(values):
            sl.setExploded(True)
            sl.setExplodeDistanceFactor(0.08)
    series.setLabelsVisible(False)
    chart.addSeries(series)
    chart.legend().setAlignment(Qt.AlignRight)
    return _make_chart_view(chart)


def _build_line_chart(points, label="Incidents", color="#3498db"):
    """points = list of (datetime, int)"""
    chart  = QChart()
    series = QLineSeries()
    series.setName(label)
    pen = QPen(QColor(color))
    pen.setWidth(2)
    series.setPen(pen)

    for dt, val in points:
        ms = int(dt.timestamp() * 1000)
        series.append(ms, val)

    chart.addSeries(series)

    axis_x = QDateTimeAxis()
    axis_x.setFormat("MMM dd")
    axis_x.setTitleText("Date")
    _axis_style(axis_x)
    chart.addAxis(axis_x, Qt.AlignBottom)
    series.attachAxis(axis_x)

    axis_y = QValueAxis()
    axis_y.setMin(0)
    vals = [v for _, v in points]
    axis_y.setMax(max(vals) * 1.2 + 1 if vals else 10)
    axis_y.setLabelFormat("%d")
    axis_y.setTickCount(5)
    _axis_style(axis_y)
    chart.addAxis(axis_y, Qt.AlignLeft)
    series.attachAxis(axis_y)

    chart.legend().setAlignment(Qt.AlignBottom)
    return _make_chart_view(chart)


# ─────────────────────────────────────────────────────────────────────────────
# Data aggregation helpers
# ─────────────────────────────────────────────────────────────────────────────

def _agg_by_category(incidents):
    counts = defaultdict(int)
    for i in incidents:
        counts[(i.incident_category or "unknown").lower()] += 1
    return dict(counts)


def _agg_by_priority(incidents):
    counts = defaultdict(int)
    for i in incidents:
        counts[(i.priority or "—").upper()] += 1
    return dict(counts)


def _agg_time_series(incidents, period="daily"):
    """Return list of (datetime, count) sorted ascending."""
    buckets = defaultdict(int)
    now     = datetime.now()

    for inc in incidents:
        dt = inc.created_at if inc.created_at else now
        if period == "daily":
            key = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == "weekly":
            key = (dt - timedelta(days=dt.weekday())).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
        elif period == "monthly":
            key = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        else:  # yearly
            key = dt.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        buckets[key] += 1

    return sorted(buckets.items())


# ─────────────────────────────────────────────────────────────────────────────
# Main Analytics Page
# ─────────────────────────────────────────────────────────────────────────────

class AdminAnalytics(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self._incidents = []
        self._users     = []
        self._init_ui()
        self.refresh()

        self._timer = QTimer(self)
        self._timer.timeout.connect(self.refresh)
        self._timer.start(15_000)

    # ── scaffold ──────────────────────────────────────────────────────────────

    def _init_ui(self):
        s = theme.STYLES

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── top bar ──────────────────────────────────────────────────────────
        topbar = QFrame()
        topbar.setStyleSheet(
            f"QFrame {{ background: {s['bg_card']};"
            f" border-bottom: 1px solid {s['border']}; border-radius: 0; }}"
        )
        topbar.setFixedHeight(52)
        tb_lay = QHBoxLayout(topbar)
        tb_lay.setContentsMargins(20, 0, 20, 0)

        tb_title = QLabel("Analysis Dashboard")
        tb_title.setFont(QFont("Arial", 15, QFont.Bold))
        tb_title.setStyleSheet(f"color: {s['text_main']}; border: none;")
        tb_lay.addWidget(tb_title)
        tb_lay.addStretch()

        refresh_btn = QPushButton("Refresh data")
        refresh_btn.setFixedHeight(30)
        refresh_btn.setStyleSheet(
            "QPushButton { background: #3498db; color: white; border: none;"
            " padding: 0 16px; border-radius: 6px; font-size: 12px; font-weight: bold; }"
            "QPushButton:hover { background: #2980b9; }"
        )
        refresh_btn.clicked.connect(self.refresh)
        tb_lay.addWidget(refresh_btn)

        root.addWidget(topbar)

        # ── scrollable body ───────────────────────────────────────────────────
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        body = QWidget()
        body.setMinimumWidth(700)
        self._body_lay = QVBoxLayout(body)
        self._body_lay.setContentsMargins(20, 16, 20, 24)
        self._body_lay.setSpacing(20)

        # ── section tabs ─────────────────────────────────────────────────────
        self._stack = QStackedWidget()

        tabs = _TabBar(
            ["Incident analysis", "Responder analysis", "Reporter analysis"],
            self._stack.setCurrentIndex
        )
        self._body_lay.addWidget(tabs)
        self._body_lay.addWidget(self._stack)

        # build the three section pages
        self._inc_page  = self._build_incident_page()
        self._resp_page = self._build_responder_page()
        self._rep_page  = self._build_reporter_page()

        self._stack.addWidget(self._inc_page)
        self._stack.addWidget(self._resp_page)
        self._stack.addWidget(self._rep_page)

        scroll.setWidget(body)
        root.addWidget(scroll)

    # ── incident section ──────────────────────────────────────────────────────

    def _build_incident_page(self):
        s   = theme.STYLES
        pg  = QWidget()
        lay = QVBoxLayout(pg)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(16)

        # stat cards row
        stat_row = QHBoxLayout()
        stat_row.setSpacing(10)
        self._inc_total    = _StatCard("Total incidents",  0, "#3498db")
        self._inc_pending  = _StatCard("Pending",          0, "#ca8a04")
        self._inc_ongoing  = _StatCard("Ongoing",          0, "#2563eb")
        self._inc_solved   = _StatCard("Resolved",         0, "#16a34a")
        for c in (self._inc_total, self._inc_pending,
                  self._inc_ongoing, self._inc_solved):
            stat_row.addWidget(c)
        lay.addLayout(stat_row)

        # ── chart row 1: category + priority ─────────────────────────────────
        chart_row1 = QHBoxLayout()
        chart_row1.setSpacing(12)

        cat_card = _Card()
        cat_lay  = QVBoxLayout(cat_card)
        cat_lay.setContentsMargins(16, 14, 16, 14)
        cat_lay.setSpacing(8)
        hdr1 = QHBoxLayout()
        hdr1.addWidget(_SectionTitle("Incident category distribution"))
        self._cat_view_toggle = _TabBar(
            ["Bar", "Pie"], lambda i: self._toggle_cat_chart(i)
        )
        hdr1.addStretch()
        hdr1.addWidget(self._cat_view_toggle)
        cat_lay.addLayout(hdr1)

        self._cat_chart_stack = QStackedWidget()
        self._cat_bar_placeholder = QLabel("Loading…")
        self._cat_bar_placeholder.setAlignment(Qt.AlignCenter)
        self._cat_pie_placeholder = QLabel("Loading…")
        self._cat_pie_placeholder.setAlignment(Qt.AlignCenter)
        self._cat_chart_stack.addWidget(self._cat_bar_placeholder)
        self._cat_chart_stack.addWidget(self._cat_pie_placeholder)
        self._cat_chart_stack.setMinimumHeight(280)
        cat_lay.addWidget(self._cat_chart_stack)
        chart_row1.addWidget(cat_card, 3)

        pri_card = _Card()
        pri_lay  = QVBoxLayout(pri_card)
        pri_lay.setContentsMargins(16, 14, 16, 14)
        pri_lay.setSpacing(8)
        pri_lay.addWidget(_SectionTitle("Priority distribution"))
        self._pri_chart_placeholder = QLabel("Loading…")
        self._pri_chart_placeholder.setAlignment(Qt.AlignCenter)
        self._pri_chart_placeholder.setMinimumHeight(280)
        pri_lay.addWidget(self._pri_chart_placeholder)
        chart_row1.addWidget(pri_card, 2)

        lay.addLayout(chart_row1)

        # ── chart row 2: time trends ──────────────────────────────────────────
        trend_card = _Card()
        trend_lay  = QVBoxLayout(trend_card)
        trend_lay.setContentsMargins(16, 14, 16, 14)
        trend_lay.setSpacing(8)

        trend_hdr = QHBoxLayout()
        trend_hdr.addWidget(_SectionTitle("Incident trends over time"))
        trend_hdr.addStretch()
        self._trend_period = _TabBar(
            ["Daily", "Weekly", "Monthly", "Yearly"],
            lambda i: self._redraw_trend(["daily","weekly","monthly","yearly"][i])
        )
        trend_hdr.addWidget(self._trend_period)
        trend_lay.addLayout(trend_hdr)

        self._trend_placeholder = QLabel("Loading…")
        self._trend_placeholder.setAlignment(Qt.AlignCenter)
        self._trend_placeholder.setMinimumHeight(260)
        trend_lay.addWidget(self._trend_placeholder)
        lay.addWidget(trend_card)

        # ── insight banner ────────────────────────────────────────────────────
        self._insight_banner = QFrame()
        self._insight_banner.setStyleSheet(
            "QFrame { background: #1e3a5f; border-radius: 8px; border: none; }"
        )
        ib_lay = QHBoxLayout(self._insight_banner)
        ib_lay.setContentsMargins(16, 10, 16, 10)
        self._insight_lbl = QLabel("—")
        self._insight_lbl.setStyleSheet(
            "color: #93c5fd; font-size: 12px; font-weight: bold; border: none;"
        )
        self._insight_lbl.setWordWrap(True)
        ib_lay.addWidget(QLabel("Insight: "))
        ib_lay.itemAt(0).widget().setStyleSheet(
            "color: white; font-size: 12px; font-weight: bold; border: none;"
        )
        ib_lay.addWidget(self._insight_lbl, 1)
        lay.addWidget(self._insight_banner)

        lay.addStretch()
        return pg

    def _toggle_cat_chart(self, idx):
        self._cat_chart_stack.setCurrentIndex(idx)

    def _redraw_trend(self, period):
        chart_view = _build_line_chart(
            _agg_time_series(self._incidents, period),
            label="Incidents", color="#3498db"
        )
        chart_view.setMinimumHeight(260)
        # swap placeholder
        lay = self._trend_placeholder.parent().layout()
        old = lay.itemAt(lay.count() - 1).widget()
        lay.removeWidget(old)
        old.deleteLater()
        self._trend_placeholder = chart_view
        lay.addWidget(chart_view)

    # ── responder section ─────────────────────────────────────────────────────

    def _build_responder_page(self):
        pg  = QWidget()
        lay = QVBoxLayout(pg)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(12)

        card = _Card()
        c_lay = QVBoxLayout(card)
        c_lay.setContentsMargins(16, 14, 16, 14)
        c_lay.setSpacing(10)

        # filters row
        f_row = QHBoxLayout()
        f_row.setSpacing(8)
        self._resp_cat_filter  = _combo(["All categories"])
        self._resp_type_filter = _combo(["All incident types"])
        self._resp_pri_filter  = _combo(["All priorities", "P1", "P2", "P3", "P4", "P5"])
        for w in (self._resp_cat_filter, self._resp_type_filter, self._resp_pri_filter):
            f_row.addWidget(w)
        f_row.addStretch()
        c_lay.addLayout(f_row)

        cols = [
            "Responder", "ID", "Category", "Total", "Ongoing",
            "Completed", "Incident types", "Priorities handled"
        ]
        self._resp_table = _styled_table(cols)
        self._resp_table.setMinimumHeight(400)
        c_lay.addWidget(self._resp_table)

        for w in (self._resp_cat_filter, self._resp_type_filter, self._resp_pri_filter):
            w.currentIndexChanged.connect(self._filter_responder_table)

        lay.addWidget(card)
        lay.addStretch()
        return pg

    # ── reporter section ──────────────────────────────────────────────────────

    def _build_reporter_page(self):
        pg  = QWidget()
        lay = QVBoxLayout(pg)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(12)

        card = _Card()
        c_lay = QVBoxLayout(card)
        c_lay.setContentsMargins(16, 14, 16, 14)
        c_lay.setSpacing(10)

        f_row = QHBoxLayout()
        f_row.setSpacing(8)
        self._rep_type_filter = _combo(["All incident types"])
        self._rep_cat_filter  = _combo(["All categories"])
        self._rep_pri_filter  = _combo(["All priorities", "P1", "P2", "P3", "P4", "P5"])
        self._rep_act_filter  = _combo(["All activity levels", "High (5+)", "Medium (2–4)", "Low (1)"])
        for w in (self._rep_type_filter, self._rep_cat_filter,
                  self._rep_pri_filter, self._rep_act_filter):
            f_row.addWidget(w)
        f_row.addStretch()
        c_lay.addLayout(f_row)

        cols = [
            "Reporter", "ID", "Total reports", "Incident types",
            "Categories", "Priorities", "Activity level"
        ]
        self._rep_table = _styled_table(cols)
        self._rep_table.setMinimumHeight(400)
        c_lay.addWidget(self._rep_table)

        for w in (self._rep_type_filter, self._rep_cat_filter,
                  self._rep_pri_filter, self._rep_act_filter):
            w.currentIndexChanged.connect(self._filter_reporter_table)

        lay.addWidget(card)
        lay.addStretch()
        return pg

    # ── data refresh ──────────────────────────────────────────────────────────

    def refresh(self):
        self._incidents = self.db.get_all_incidents()
        self._users     = self.db.get_all_users()
        self._redraw_incidents()
        self._rebuild_responder_table()
        self._rebuild_reporter_table()

    # ── incident redraws ──────────────────────────────────────────────────────

    def _redraw_incidents(self):
        incs = self._incidents

        total   = len(incs)
        pending = len([i for i in incs if i.status == "pending"])
        ongoing = len([i for i in incs if i.status in ("ongoing", "assigned")])
        solved  = len([i for i in incs if i.status == "solved"])

        self._inc_total.set_value(total)
        self._inc_pending.set_value(pending)
        self._inc_ongoing.set_value(ongoing)
        self._inc_solved.set_value(solved)

        # category chart
        cat_counts = _agg_by_category(incs)
        cats   = list(cat_counts.keys())
        cvals  = [cat_counts[c] for c in cats]
        clbls  = [c.replace("_", " ").title() for c in cats]
        ccols  = CATEGORY_COLORS[:len(cats)]

        bar_view = _build_bar_chart(clbls, cvals, ccols)
        bar_view.setMinimumHeight(280)
        pie_view = _build_pie_chart(clbls, cvals, ccols)
        pie_view.setMinimumHeight(280)

        self._swap_widget(self._cat_chart_stack, 0, bar_view)
        self._swap_widget(self._cat_chart_stack, 1, pie_view)
        self._cat_bar_placeholder = bar_view
        self._cat_pie_placeholder = pie_view

        # priority chart
        pri_counts = _agg_by_priority(incs)
        pris  = ["P1", "P2", "P3", "P4", "P5"]
        pvals = [pri_counts.get(p, 0) for p in pris]
        pcols = [PRIORITY_COLORS.get(p, "#6b7280") for p in pris]
        pri_view = _build_bar_chart(pris, pvals, pcols)
        pri_view.setMinimumHeight(280)
        pri_card_lay = self._pri_chart_placeholder.parent().layout()
        old = pri_card_lay.itemAt(pri_card_lay.count() - 1).widget()
        pri_card_lay.removeWidget(old)
        old.deleteLater()
        self._pri_chart_placeholder = pri_view
        pri_card_lay.addWidget(pri_view)

        # trend (default daily)
        trend_view = _build_line_chart(
            _agg_time_series(incs, "daily"), color="#3498db"
        )
        trend_view.setMinimumHeight(260)
        trend_lay = self._trend_placeholder.parent().layout()
        old2 = trend_lay.itemAt(trend_lay.count() - 1).widget()
        trend_lay.removeWidget(old2)
        old2.deleteLater()
        self._trend_placeholder = trend_view
        trend_lay.addWidget(trend_view)

        # insight banner
        if cats:
            top_cat = clbls[cvals.index(max(cvals))]
            top_val = max(cvals)
            p1_cnt  = pri_counts.get("P1", 0)
            self._insight_lbl.setText(
                f"Top category: {top_cat} ({top_val} incidents). "
                f"Critical (P1) incidents: {p1_cnt}. "
                f"Resolution rate: {int(solved/total*100) if total else 0}%."
            )

    def _swap_widget(self, stack, idx, new_widget):
        old = stack.widget(idx)
        stack.removeWidget(old)
        old.deleteLater()
        stack.insertWidget(idx, new_widget)

    # ── responder table ────────────────────────────────────────────────────────

    def _rebuild_responder_table(self):
        responders = [u for u in self._users if u.role == "responder"]
        incs       = self._incidents

        # update filter combos
        cats  = sorted({(u.responder_category or "").lower() for u in responders if u.responder_category})
        types = sorted({(i.type or "").lower() for i in incs})
        self._resp_cat_filter.blockSignals(True)
        self._resp_type_filter.blockSignals(True)
        cur_cat  = self._resp_cat_filter.currentText()
        cur_type = self._resp_type_filter.currentText()
        self._resp_cat_filter.clear()
        self._resp_cat_filter.addItem("All categories")
        self._resp_cat_filter.addItems([c.title() for c in cats])
        self._resp_type_filter.clear()
        self._resp_type_filter.addItem("All incident types")
        self._resp_type_filter.addItems([t.replace("_", " ").title() for t in types])
        self._resp_cat_filter.blockSignals(False)
        self._resp_type_filter.blockSignals(False)

        self._resp_data = []
        for u in responders:
            u_incs = [i for i in incs if i.responder_id == u.id]
            types_handled = ", ".join(sorted({
                (i.incident_category or i.type or "—").replace("_", " ").title()
                for i in u_incs
            })) or "—"
            pris_handled = ", ".join(sorted({(i.priority or "—").upper() for i in u_incs})) or "—"
            self._resp_data.append({
                "name":     u.name,
                "id":       u.id,
                "category": (u.responder_category or "—").title(),
                "total":    len(u_incs),
                "ongoing":  len([i for i in u_incs if i.status in ("ongoing", "assigned")]),
                "completed":len([i for i in u_incs if i.status == "solved"]),
                "types":    types_handled,
                "pris":     pris_handled,
            })
        self._resp_data.sort(key=lambda x: x["total"], reverse=True)
        self._populate_resp_table(self._resp_data)

    def _filter_responder_table(self):
        cat  = self._resp_cat_filter.currentText()
        typ  = self._resp_type_filter.currentText()
        pri  = self._resp_pri_filter.currentText()
        rows = self._resp_data
        if cat != "All categories":
            rows = [r for r in rows if r["category"].lower() == cat.lower()]
        if typ != "All incident types":
            rows = [r for r in rows if typ.lower() in r["types"].lower()]
        if pri != "All priorities":
            rows = [r for r in rows if pri.upper() in r["pris"]]
        self._populate_resp_table(rows)

    def _populate_resp_table(self, rows):
        s = theme.STYLES
        t = self._resp_table
        t.setRowCount(len(rows))
        for r, d in enumerate(rows):
            items = [
                d["name"], d["id"], d["category"],
                str(d["total"]), str(d["ongoing"]), str(d["completed"]),
                d["types"], d["pris"]
            ]
            for c, txt in enumerate(items):
                item = QTableWidgetItem(txt)
                if c == 3:   # total — highlight top
                    item.setForeground(QColor("#3498db"))
                    item.setFont(QFont("Arial", 11, QFont.Bold))
                if c == 5:   # completed — green
                    item.setForeground(QColor("#16a34a"))
                if c == 4 and d["ongoing"] > 0:
                    item.setForeground(QColor("#ca8a04"))
                t.setItem(r, c, item)
            t.setRowHeight(r, 36)

    # ── reporter table ─────────────────────────────────────────────────────────

    def _rebuild_reporter_table(self):
        reporters = [u for u in self._users if u.role == "reporter"]
        incs      = self._incidents

        cats  = sorted({(i.incident_category or "").lower() for i in incs if i.incident_category})
        types = sorted({(i.type or "").lower() for i in incs})
        self._rep_cat_filter.blockSignals(True)
        self._rep_type_filter.blockSignals(True)
        self._rep_cat_filter.clear()
        self._rep_cat_filter.addItem("All categories")
        self._rep_cat_filter.addItems([c.replace("_"," ").title() for c in cats])
        self._rep_type_filter.clear()
        self._rep_type_filter.addItem("All incident types")
        self._rep_type_filter.addItems([t.replace("_"," ").title() for t in types])
        self._rep_cat_filter.blockSignals(False)
        self._rep_type_filter.blockSignals(False)

        self._rep_data = []
        for u in reporters:
            u_incs = [i for i in incs if i.reporter_id == u.id]
            types_str = ", ".join(sorted({
                (i.type or "—").replace("_", " ").title() for i in u_incs
            })) or "—"
            cats_str  = ", ".join(sorted({
                (i.incident_category or "—").replace("_", " ").title() for i in u_incs
            })) or "—"
            pris_str  = ", ".join(sorted({(i.priority or "—").upper() for i in u_incs})) or "—"
            cnt       = len(u_incs)
            activity  = "High" if cnt >= 5 else "Medium" if cnt >= 2 else "Low"
            self._rep_data.append({
                "name":     u.name,
                "id":       u.id,
                "total":    cnt,
                "types":    types_str,
                "cats":     cats_str,
                "pris":     pris_str,
                "activity": activity,
            })
        self._rep_data.sort(key=lambda x: x["total"], reverse=True)
        self._populate_rep_table(self._rep_data)

    def _filter_reporter_table(self):
        typ = self._rep_type_filter.currentText()
        cat = self._rep_cat_filter.currentText()
        pri = self._rep_pri_filter.currentText()
        act = self._rep_act_filter.currentText()
        rows = self._rep_data
        if typ != "All incident types":
            rows = [r for r in rows if typ.lower() in r["types"].lower()]
        if cat != "All categories":
            rows = [r for r in rows if cat.lower() in r["cats"].lower()]
        if pri != "All priorities":
            rows = [r for r in rows if pri.upper() in r["pris"]]
        if act != "All activity levels":
            level = act.split(" ")[0]
            rows  = [r for r in rows if r["activity"] == level]
        self._populate_rep_table(rows)

    def _populate_rep_table(self, rows):
        s = theme.STYLES
        t = self._rep_table
        t.setRowCount(len(rows))
        act_colors = {
            "High":   "#dc2626",
            "Medium": "#ca8a04",
            "Low":    "#16a34a",
        }
        for r, d in enumerate(rows):
            items = [
                d["name"], d["id"], str(d["total"]),
                d["types"], d["cats"], d["pris"], d["activity"]
            ]
            for c, txt in enumerate(items):
                item = QTableWidgetItem(txt)
                if c == 2:
                    item.setForeground(QColor("#3498db"))
                    item.setFont(QFont("Arial", 11, QFont.Bold))
                if c == 6:
                    item.setForeground(QColor(act_colors.get(txt, "#6b7280")))
                    item.setFont(QFont("Arial", 11, QFont.Bold))
                t.setItem(r, c, item)
            t.setRowHeight(r, 36)
