from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFileDialog, QTextBrowser)
from PyQt6.QtCore import pyqtSignal, QUrl
from PyQt6.QtGui import QDesktopServices


class PdfPreviewWidget(QWidget):
    """Simple PDF preview page that shows the generated file path and offers Save As / Open / Close."""
    save_requested = pyqtSignal(str)
    closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._pdf_path = None
        self._html = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        title = QLabel("PDF Preview")
        title.setStyleSheet("font-size:18px; font-weight:700; color:#000;")
        layout.addWidget(title)

        self.info = QTextBrowser()
        self.info.setOpenExternalLinks(True)
        self.info.setStyleSheet(
            "border:1px solid #DDD; padding:12px; border-radius:6px;")
        layout.addWidget(self.info)

        btns = QHBoxLayout()
        self.open_btn = QPushButton("Open PDF")
        self.open_btn.clicked.connect(self._open_pdf)
        btns.addWidget(self.open_btn)

        self.save_btn = QPushButton("Save As...")
        self.save_btn.clicked.connect(self._on_save_as)
        btns.addWidget(self.save_btn)

        btns.addStretch()
        self.close_btn = QPushButton("Close and Return to Input")
        self.close_btn.clicked.connect(self._on_close)
        btns.addWidget(self.close_btn)

        layout.addLayout(btns)

    def load_preview(self, pdf_path: str = None, html: str = None):
        """Load generated PDF (path) and HTML snapshot.

        The preview displays a short message with a link to the file. Opening
        will attempt to launch the system default application for PDFs.
        """
        self._pdf_path = pdf_path
        self._html = html or ''
        if pdf_path:
            # show a clickable link
            self.info.setHtml(
                f"<p>PDF generated: <a href=\"file://{pdf_path}\">{pdf_path}</a></p>")
            self.open_btn.setEnabled(True)
            self.save_btn.setEnabled(True)
        else:
            # No PDF; show HTML content and allow saving as HTML
            snippet = (
                self._html[:200] + '...') if self._html else 'No preview available.'
            self.info.setHtml(f"<p>{snippet}</p>")
            self.open_btn.setEnabled(False)
            self.save_btn.setEnabled(True)

    def _open_pdf(self):
        if not self._pdf_path:
            return
        QDesktopServices.openUrl(QUrl.fromLocalFile(self._pdf_path))

    def _on_save_as(self):
        if self._pdf_path:
            dest, _ = QFileDialog.getSaveFileName(
                self, 'Save PDF As', '', 'PDF Files (*.pdf)')
            if not dest:
                return
            try:
                # copy file
                from shutil import copyfile
                copyfile(self._pdf_path, dest)
            except Exception as e:
                # fallback: save HTML
                if self._html:
                    try:
                        with open(dest + '.html', 'w', encoding='utf-8') as f:
                            f.write(self._html)
                    except Exception:
                        pass
        else:
            dest, _ = QFileDialog.getSaveFileName(
                self, 'Save HTML', '', 'HTML Files (*.html)')
            if not dest:
                return
            try:
                with open(dest, 'w', encoding='utf-8') as f:
                    f.write(self._html or '')
            except Exception:
                pass

    def _on_close(self):
        self.closed.emit()
