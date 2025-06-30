# ui/main_window.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit,
    QTabWidget, QTableWidget, QTableWidgetItem, QMessageBox,
    QHBoxLayout, QCheckBox,
    QFileDialog
)
from PyQt5.QtGui import QColor
from logic.ring_checker import analyze_ring
from logic.ring_table import parse_fast_blocks, validate_addition_table, validate_multiplication_table
from ui.znz_tab import ZnzTab
from ui.custom_tab import CustomTab
import re
import csv
import traceback

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Finite Ring Analyzer")
        self.resize(600, 700)
        self.move(400, 50)
        self.layout = QVBoxLayout(self)
        
        self.batch_results = []
        self.batch_tables = []

        self.tabs = QTabWidget()
        self.znz_tab = ZnzTab()
        self.custom_tab = CustomTab()
        self.tabs.addTab(self.znz_tab, "Z/nZ")
        self.tabs.addTab(self.custom_tab, "Custom")
        
        # hide output checkbox
        self.hide_output_cb = QCheckBox("Hide Output")
        self.hide_output_cb.setChecked(True)
        self.hide_output_cb.stateChanged.connect(self.toggle_output_visibility)

        self.analyze_btn = QPushButton("Analyze")
        self.analyze_btn.clicked.connect(self.analyze)
        
        # --- Results Container (hidden initially) ---
        self.results_container = QWidget()
        rc_layout = QVBoxLayout(self.results_container)
        self.results_label = QLabel("Results:")
        self.results_box = QTextEdit(readOnly=True)

        self.add_label = QLabel("Addition Table:")
        self.add_table = QTableWidget()
        
        self.mul_label = QLabel("Multiplication Table:")
        self.mul_table = QTableWidget()

        # Smaller cells
        for table in [self.mul_table, self.add_table]:
            table.horizontalHeader().setDefaultSectionSize(30)
            table.verticalHeader().setDefaultSectionSize(30)

        rc_layout.addWidget(self.results_label)
        rc_layout.addWidget(self.results_box)
        rc_layout.addWidget(self.add_label)
        rc_layout.addWidget(self.add_table)
        rc_layout.addWidget(self.mul_label)
        rc_layout.addWidget(self.mul_table)

        self.results_container.setVisible(False)
        
        self.layout.addWidget(self.tabs, stretch=1)
        self.layout.addWidget(self.analyze_btn)
        self.layout.addWidget(self.results_container, stretch=1)
        
        # previous and next batch buttons
        self.nav_label = QLabel("Batch: 1")
        self.prev_btn = QPushButton("◀ Prev")
        self.next_btn = QPushButton("Next ▶")
        
        self.prev_btn.clicked.connect(self.prev_batch)
        self.next_btn.clicked.connect(self.next_batch)
        nav_layout = QHBoxLayout()
        
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.nav_label)
        nav_layout.addWidget(self.next_btn)
        rc_layout.addLayout(nav_layout)
        
        # Export button
        self.export_btn = QPushButton("Export Results")
        self.export_btn.clicked.connect(self.export_results)
        rc_layout.addWidget(self.export_btn)
        self.layout.addWidget(self.hide_output_cb)

        # Ensure UI matches default state
        self.toggle_output_visibility()
        
        self.layout.addStretch()

    def analyze(self):
        try:
            idx = self.tabs.currentIndex()
            if idx == 0:
                tables = self.collect_znz()
                if not tables:
                    raise ValueError("No valid batches were parsed. Check your input format.")

                # Z/nZ only has mul_table (and auto-generated add)
                self.batch_tables = [(None, t) for t in tables]
            else:
                # Custom gives (add, mul) tuples directly
                tables = self.collect_custom()
                self.batch_tables = tables
                
            # print(f"[analyze] Parsed {len(tables)} table(s): {tables}")

            self.batch_results = [analyze_ring(mul) for (_, mul) in self.batch_tables]
            self.current_batch = 0
            self.update_batch_display()

            add, mul = self.batch_tables[0]
            self.display_results(self.batch_results[0])
            self.visualize(add, mul, self.batch_results[0])

            self.hide_output_cb.setChecked(False)
            
        except Exception as e:
            # traceback.print_exc()
            QMessageBox.critical(self, "Error", str(e))
            
        # print(f"Parsed {len(self.batch_results)} batches")

    def collect_znz(self):
        tab = self.znz_tab
        if tab.fast_cb.isChecked():
            return parse_fast_blocks(tab.fast_text.toPlainText(), custom=False)
        elif tab.batch_cb.isChecked():
            results = []
            for n_spin, el_le in zip(tab.ns, tab.elements):
                n = n_spin.value()
                elems = [int(x) for x in re.split(r"[,\s]+", el_le.text())]
                # after you parse elems = [...]
                if any(e < 0 or e >= n for e in elems):
                    raise ValueError(f"All elements must be between 0 and {n-1}.")
                table = [[(a*b)%n for b in elems] for a in elems]
                results.append(table)
            return results
        else:
            n = tab.n_spin.value()
            elems = [int(x) for x in re.split(r"[,\s]+", tab.elements_le.text()) if x]
            if any(e<0 or e>=n for e in elems):
                raise ValueError(f"All elements must be between 0 and {n-1}.")
            table = [[(a*b)%n for b in elems] for a in elems]
            return [table]


    def collect_custom(self):
        tab = self.custom_tab

        if tab.fast_cb.isChecked():
            parsed = parse_fast_blocks(tab.fast_text.toPlainText(), custom=True)
            validated = []
            for add, mul in parsed:
                validate_addition_table(add)
                validate_multiplication_table(mul)
                validated.append((add, mul))

            return validated

        elif tab.batch_cb.isChecked():
            results = []
            for size_spin, add_w, mul_w in zip(tab.sizes, tab.add_tables, tab.mul_tables):
                n = size_spin.value()
                # read add table
                add_table = [
                    [int(add_w.item(i, j).text() or "0") for j in range(n)]
                    for i in range(n)
                ]
                # read mul table
                mul_table = [
                    [int(mul_w.item(i, j).text() or "0") for j in range(n)]
                    for i in range(n)
                ]
                
                # print(f"[manual batch mode] n={n}, parsed add_table: {len(add_table)}x{len(add_table[0])}, mul_table: {len(mul_table)}x{len(mul_table[0])}")

                # separate validations
                validate_addition_table(add_table)        # raises on error
                validate_multiplication_table(mul_table)  # raises on error

                results.append((add_table, mul_table))

            return results

        else:
            n = tab.size_spin.value()
            add = [
                [int(tab.add_table.item(i, j).text() or "0") for j in range(n)]
                for i in range(n)
            ]
            mul = [
                [int(tab.mul_table.item(i, j).text() or "0") for j in range(n)]
                for i in range(n)
            ]

            validate_addition_table(add)
            validate_multiplication_table(mul)

            return [(add, mul)]

    def display_results(self, res):
        lines = []
        for prop, data in res.items():
            ok = data["value"]
            lines.append(f"{'✅' if ok else '❌'} {prop.title()}")

            if not ok:
                # Provide explanation or reason for failure
                if "counterexample" in data and data["counterexample"] is not None:
                    lines.append(f"    Counterexample: {data['counterexample']}")
                elif "zero divisors" in data:
                    if data["zero divisors"] is not None:
                        lines.append(f"    Zero divisors: {data['zero divisors']}")
                    else:
                        lines.append("    Skipped: no identity element")
                elif "missing inverse" in data:
                    if data["missing inverse"] is not None:
                        lines.append(f"    Missing inverse for: {data['missing inverse']}")
                    else:
                        lines.append("    Skipped: no identity element")
                elif "identity" in data and data["identity"] is None:
                    lines.append("    No multiplicative identity found")

        self.results_box.setPlainText("\n".join(lines))

    def visualize(self, add_table, mul_table, res):
        n = len(mul_table)

        # Clear tables and set size
        for tbl in [self.mul_table, self.add_table]:
            tbl.clear()
            tbl.setRowCount(n)
            tbl.setColumnCount(n)

        # If no custom add table, generate default (ZnZ mode)
        if add_table is None:
            add_table = [[(i + j) % n for j in range(n)] for i in range(n)]

        identity = res['has identity']['identity']
        zero_div = res['integral domain']['zero divisors']

        for i in range(n):
            for j in range(n):
                m_item = QTableWidgetItem(str(mul_table[i][j]))
                if identity is not None and (i == identity or j == identity):
                    m_item.setBackground(QColor(200, 255, 200))
                if zero_div and (i, j) == tuple(zero_div):
                    m_item.setBackground(QColor(255, 200, 200))
                self.mul_table.setItem(i, j, m_item)

                a_item = QTableWidgetItem(str(add_table[i][j]))
                self.add_table.setItem(i, j, a_item)
                
    def update_batch_display(self):
        self.nav_label.setText(f"Batch: {self.current_batch + 1}")
        self.display_results(self.batch_results[self.current_batch])
        add, mul = self.batch_tables[self.current_batch]
        self.visualize(add, mul, self.batch_results[self.current_batch])

    def prev_batch(self):
        if self.current_batch > 0:
            self.current_batch -= 1
            self.update_batch_display()

    def next_batch(self):
        if self.current_batch < len(self.batch_results) - 1:
            self.current_batch += 1
            self.update_batch_display()
            
    def toggle_output_visibility(self):
        visible = not self.hide_output_cb.isChecked()
        self.results_container.setVisible(visible)
        self.prev_btn.setVisible(visible)
        self.next_btn.setVisible(visible)
        self.nav_label.setVisible(visible)
        
    def export_results(self):
        if not self.batch_results or not self.batch_tables:
            QMessageBox.warning(self, "Nothing to export", "Run analysis first.")
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Export Results", "", "CSV Files (*.csv);;Text Files (*.txt)"
        )
        if not path:
            return

        try:
            with open(path, "w", newline="") as f:
                writer = csv.writer(f) if path.endswith(".csv") else None
                for i, (res, _) in enumerate(zip(self.batch_results, self.batch_tables)):
                    header = f"Batch {i+1}"
                    if writer:
                        writer.writerow([header])
                        for k, d in res.items():
                            value_str = "Yes" if d["value"] else "No"
                            explanation = ""

                            if not d["value"]:
                                if "counterexample" in d and d["counterexample"] is not None:
                                    explanation = f"Counterexample: {d['counterexample']}"
                                elif "zero divisors" in d:
                                    explanation = (
                                        f"Zero divisors: {d['zero divisors']}" if d["zero divisors"] is not None
                                        else "Skipped: no identity element"
                                    )
                                elif "missing inverse" in d:
                                    explanation = (
                                        f"Missing inverse for: {d['missing inverse']}" if d["missing inverse"] is not None
                                        else "Skipped: no identity element"
                                    )
                                elif "identity" in d and d["identity"] is None:
                                    explanation = "No multiplicative identity found"

                            writer.writerow([k, value_str, explanation])
                        writer.writerow([])  # spacer between batches
                    else:
                        f.write(f"{header}\n")
                        for k, d in res.items():
                            value_str = "Yes" if d["value"] else "No"
                            f.write(f"{k}: {value_str}\n")

                            if not d["value"]:
                                if "counterexample" in d and d["counterexample"] is not None:
                                    f.write(f"    Counterexample: {d['counterexample']}\n")
                                elif "zero divisors" in d:
                                    if d["zero divisors"] is not None:
                                        f.write(f"    Zero divisors: {d['zero divisors']}\n")
                                    else:
                                        f.write(f"    Skipped: no identity element\n")
                                elif "missing inverse" in d:
                                    if d["missing inverse"] is not None:
                                        f.write(f"    Missing inverse for: {d['missing inverse']}\n")
                                    else:
                                        f.write(f"    Skipped: no identity element\n")
                                elif "identity" in d and d["identity"] is None:
                                    f.write("    No multiplicative identity found\n")
                        f.write("\n")
            QMessageBox.information(self, "Export Successful", f"Results saved to:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", str(e))