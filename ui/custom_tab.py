# ui/custom_tab.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QSpinBox, QTableWidget,
    QCheckBox, QPlainTextEdit, QScrollArea, QFrame, 
    QHeaderView, QSizePolicy, QSplitter
)
from PyQt5.QtCore import Qt

class CustomTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.fast_cb = QCheckBox("Fast Input Mode")
        self.batch_cb = QCheckBox("Batch Mode")
        self.batch_label = QLabel("Amount of batches:")
        self.batch_count = QSpinBox(minimum=1, value=1)
        self.batch_label.setVisible(False)
        self.batch_count.setVisible(False)

        self.size_label = QLabel("Table size n (>=2):")
        self.size_spin = QSpinBox(minimum=2, value=3)
        # self.table_widget = QTableWidget(3, 3)
        # self.table_widget.horizontalHeader().setDefaultSectionSize(30)
        # self.table_widget.verticalHeader().setDefaultSectionSize(30)
        
        # Addition and Multiplication tables
        self.add_label = QLabel("Addition Table:")
        self.add_table = QTableWidget(3, 3)
        self.add_table.horizontalHeader().setDefaultSectionSize(30)
        self.add_table.verticalHeader().setDefaultSectionSize(30)

        self.mul_label = QLabel("Multiplication Table:")
        self.mul_table = QTableWidget(3, 3)
        self.mul_table.horizontalHeader().setDefaultSectionSize(30)
        self.mul_table.verticalHeader().setDefaultSectionSize(30)
        
        self.fast_text = QPlainTextEdit()
        self.fast_text.setPlaceholderText(
            "Batch format: \nfirst line n\nnext n lines rows (addition table)\nnext n line rows (multiplication table)\nblank separator\n\nExample:\n3\n0 1 2\n1 2 0\n0 1 2\n0,0,0\n0,1,2\n0,2,1"
        )
        self.fast_text.setVisible(False)

        self.batches_area = QScrollArea()
        self.batches_area.setWidgetResizable(True)
        self.batches_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.batches_area.setVisible(False)

       # --- Upper section (controls) ---
        upper = QWidget()
        upper_layout = QVBoxLayout(upper)
        upper_layout.addWidget(self.fast_cb)
        upper_layout.addWidget(self.batch_cb)
        upper_layout.addWidget(self.batch_label)
        upper_layout.addWidget(self.batch_count)
        upper_layout.addWidget(self.size_label)
        upper_layout.addWidget(self.size_spin)
        upper_layout.addWidget(self.add_label)
        upper_layout.addWidget(self.add_table)
        upper_layout.addWidget(self.mul_label)
        upper_layout.addWidget(self.mul_table)
        upper_layout.addWidget(self.fast_text)

        # --- Splitter to separate upper and batch ---
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(upper)
        splitter.addWidget(self.batches_area)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([0, 1_000_000])  # [Upper controls, Batch area]

        self.layout.addWidget(splitter)

        # signals
        self.fast_cb.stateChanged.connect(self.toggle_fast)
        self.batch_cb.stateChanged.connect(self.toggle_batch)
        self.batch_count.valueChanged.connect(self.build_batches)
        self.size_spin.valueChanged.connect(self.resize_table)

    def toggle_fast(self, state):
        fast = (state == Qt.Checked)
        self.fast_text.setVisible(fast)
        self.batch_cb.setChecked(False)
        self.batch_cb.setEnabled(not fast)
        
        self.size_label.setVisible(not fast)
        self.size_spin.setVisible(not fast)
        
        self.add_label.setVisible(not fast)
        self.add_table.setVisible(not fast)
        self.mul_label.setVisible(not fast)
        self.mul_table.setVisible(not fast)

    def toggle_batch(self, state):
        batch = (state == Qt.Checked)
        self.fast_cb.setChecked(False)
        self.fast_cb.setEnabled(not batch)
        self.batch_label.setVisible(batch)
        self.batch_count.setVisible(batch)
        self.batches_area.setVisible(batch)
        
        self.size_label.setVisible(not batch)
        self.size_spin.setVisible(not batch)
        
        self.add_label.setVisible(not batch)
        self.add_table.setVisible(not batch)
        self.mul_label.setVisible(not batch)
        self.mul_table.setVisible(not batch)
        if batch:
            self.build_batches()

    def build_batches(self):
        count = self.batch_count.value()
        container = QFrame()
        v = QVBoxLayout(container)
        
        self.sizes = []
        self.add_tables = []
        self.mul_tables = []
        
        for i in range(count):
            size_spin = QSpinBox(minimum=2, value=3)
            add_table = QTableWidget(3, 3)
            mul_table = QTableWidget(3, 3)
            add_table.horizontalHeader().setDefaultSectionSize(30)
            add_table.verticalHeader().setDefaultSectionSize(30)
            mul_table.horizontalHeader().setDefaultSectionSize(30)
            mul_table.verticalHeader().setDefaultSectionSize(30)

            v.addWidget(QLabel(f"Batch {i+1} size:"))
            v.addWidget(size_spin)
            v.addWidget(QLabel("Addition Table:"))
            v.addWidget(add_table)
            v.addWidget(QLabel("Multiplication Table:"))
            v.addWidget(mul_table)

            size_spin.valueChanged.connect(
                lambda val, a=add_table, m=mul_table: (
                    a.setRowCount(val), a.setColumnCount(val),
                    m.setRowCount(val), m.setColumnCount(val)
                )
            )
            
            self.sizes.append(size_spin)
            self.add_tables.append(add_table)
            self.mul_tables.append(mul_table)
        self.batches_area.setWidget(container)

    def resize_table(self, val):
        self.table_widget.setRowCount(val)
        self.table_widget.setColumnCount(val)