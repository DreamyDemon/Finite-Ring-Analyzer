# ui/znz_tab.py
import re
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QSpinBox, QLineEdit,
    QCheckBox, QPlainTextEdit, QScrollArea, QFrame,
    QHBoxLayout, QSplitter, QSizePolicy,QFormLayout
)
from PyQt5.QtCore import Qt

class ZnzTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.fast_cb = QCheckBox("Fast Input Mode")
        self.batch_cb = QCheckBox("Batch Mode")

        self.batch_label = QLabel("Amount of batches:")
        self.batch_count = QSpinBox(minimum=1, value=1)
        self.batch_label.setVisible(False)
        self.batch_count.setVisible(False)

        self.n_label = QLabel("Enter modulus n (>=2):")
        self.n_spin = QSpinBox(minimum=2, value=3)
        self.elements_label = QLabel("Elements:")
        self.elements_le = QLineEdit()
        self.elements_le.setPlaceholderText("Example: 0,1,2")

        self.fast_text = QPlainTextEdit()
        self.fast_text.setPlaceholderText(
            "Batch blocks: first line n, second line elements, blank line separator\nExample:\n3\n0,1,2\n\n4\n0,2,3"
        )
        self.fast_text.setVisible(False)

        self.batches_area = QScrollArea()
        self.batches_area.setVisible(False)

        # --- Upper section ---
        upper = QWidget()
        upper_layout = QVBoxLayout(upper)
        upper_layout.setContentsMargins(10, 10, 10, 10)
        upper_layout.setSpacing(5)

        upper_layout.addWidget(self.fast_cb)
        upper_layout.addWidget(self.batch_cb)
        upper_layout.addWidget(self.batch_label)
        upper_layout.addWidget(self.batch_count)

        # FORM layout for labels + inputs
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.addRow(self.n_label, self.n_spin)
        form.addRow(self.elements_label, self.elements_le)
        upper_layout.addLayout(form)

        upper_layout.addWidget(self.fast_text)

        # Resize behavior
        upper.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.batches_area.setMinimumHeight(100)
        self.batches_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Splitter
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(upper)
        splitter.addWidget(self.batches_area)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([0, 1_000_000])

        self.layout.addWidget(splitter)

        # Signals
        self.fast_cb.stateChanged.connect(self.toggle_fast)
        self.batch_cb.stateChanged.connect(self.toggle_batch)
        self.batch_count.valueChanged.connect(self.build_batches)

    def toggle_fast(self, state):
        fast = (state == Qt.Checked)
        # disable batch when fast on
        self.batch_cb.setChecked(False)
        self.batch_cb.setEnabled(not fast)
        # hide batch controls
        self.batch_label.setVisible(False)
        self.batch_count.setVisible(False)
        # show fast vs regular
        self.fast_text.setVisible(fast)
        self.n_label.setVisible(not fast)
        self.n_spin.setVisible(not fast)
        self.elements_label.setVisible(not fast)
        self.elements_le.setVisible(not fast)

    def toggle_batch(self, state):
        batch = (state == Qt.Checked)
        # disable fast when batch on
        self.fast_cb.setChecked(False)
        self.fast_cb.setEnabled(not batch)
        # show/hide batch controls
        self.batch_label.setVisible(batch)
        self.batch_count.setVisible(batch)
        self.batches_area.setVisible(batch)
        # show batch vs regular
        self.n_label.setVisible(not batch)
        self.n_spin.setVisible(not batch)
        self.elements_label.setVisible(not batch)
        self.elements_le.setVisible(not batch)
        if batch:
            self.build_batches()

    def build_batches(self):
        count = self.batch_count.value()
        container = QFrame()
        v = QVBoxLayout(container)
        self.ns = []
        self.elements = []
        for i in range(count):
            h = QHBoxLayout()
            spin = QSpinBox(minimum=2, value=3)
            line = QLineEdit()
            line.setPlaceholderText(f"(e.g. 0,1,2)")
            h.addWidget(QLabel(f"Batch {i+1}"))
            h.addWidget(QLabel(f"modulus n:"))
            h.addWidget(spin)
            h.addWidget(QLabel("Elements:"))
            h.addWidget(line)
            v.addLayout(h)
            self.ns.append(spin)
            self.elements.append(line)
        self.batches_area.setWidget(container)