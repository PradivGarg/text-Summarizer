import sys
import re
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog, QVBoxLayout, QTextEdit
from PyQt5.QtCore import Qt
from collections import Counter

class textSummary(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Text Summary Generator")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #19404B;")

        layout = QVBoxLayout()

        self.label = QLabel("Uplaod file to generate summary")
        self.label.setAlignment(Qt.AlignLeft)
        self.label.setFixedSize(550, 50)
        self.label.setStyleSheet("font-size: 14px; color: #f0f0f0;")
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(self.label)

        self.textEdit = QTextEdit(self)
        self.textEdit.setPlaceholderText("Uploaded Text will be displayed here...")
        self.textEdit.setReadOnly(True)
        self.textEdit.setFixedSize(550, 100)
        self.textEdit.setStyleSheet("background-color: #19404B; font-size: 14px; color: #f0f0f0; border: none;")
        self.textEdit.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(self.textEdit)

        self.textLabel = QLabel("Summary")
        self.textLabel.setAlignment(Qt.AlignLeft)
        self.textLabel.setFixedSize(550, 50)
        self.textLabel.setStyleSheet("font-size: 14px; color: #f0f0f0;")
        self.textLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(self.textLabel)

        self.summaryText = QTextEdit(self)
        self.summaryText.setPlaceholderText("Summary will be displayed here...")
        self.summaryText.setReadOnly(True)
        self.summaryText.setFixedSize(550, 100)
        self.summaryText.setStyleSheet("background-color: #19404B; font-size: 14px; color: #f0f0f0; border:none;")
        self.summaryText.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(self.summaryText)

        self.uploadButton = QPushButton("Upload Text File", self)
        self.uploadButton.clicked.connect(self.uploadTextFile)
        self.uploadButton.setFixedSize(200, 50)
        self.uploadButton.setStyleSheet("background-color: #40A4BF; color: white; font-size: 16px;")
        layout.addWidget(self.uploadButton)

        self.setLayout(layout)

    def uploadTextFile(self):
        option = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Upload Text File", "", "Text Files (*.txt);", options=option)
        if filename:
            self.generateSummary(filename)
        
    def generateSummary(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
                self.textEdit.setPlainText(content)
                self.label.setText("File Contains:")
                summary = self.summarizeContent(content)
                self.summaryText.setPlainText(summary)
        except Exception as e:
            self.summaryText.setPlainText(f"Error: {e}")
            self.textEdit.setPlainText(f"Error: {e}")
            self.label.setText("Error reading file.")
        
    def summarizeContent(self, content):
        text = content.strip()
        if not text:
            return "File is Empty."
        
        charCount = len(text)
        charCountNoSpaces  = len(text.replace(" ", "").replace("\n", ""))

        lines = text.splitlines()
        numLines = len(lines)
        
        words = re.findall(r'\b\w+\b', text.lower())
        numWords = len(words)

        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        numSentences = len(sentences)

        avgWordLen = (sum(len(word) for word in words) / numWords) if numWords > 0 else 0

        avgSentenceLen = (numWords / numSentences) if numSentences > 0 else 0
        stopWords =set([
            'the', 'and', 'a', 'to', 'of', 'in', 'that', 'is', 'was', 'he', 'for',
            'it', 'with', 'as', 'his', 'on', 'be', 'at', 'by', 'i', 'this', 'had',
            'not', 'are', 'but', 'from', 'or', 'have', 'an', 'they', 'which', 'you',
            'one', 'were', 'all', 'we', 'can', 'her', 'has', 'there', 'been', 'if',
            'more', 'no', 'out', 'up', 'do', 'will', 'about', 'so', 'what', 'when',
            'who', 'my', 'your', 'their', 'its', 'than', 'some', 'just', 'like', 'me',
            'them', 'these', 'those', 'other', 'then', 'now', 'into', 'over', 'after',
            'before', 'such', 'most', 'any', 'also', 'back', 'down', 'see', 'way',
            'get', 'make', 'time', 'know', 'take', 'go', 'come', 'think', 'say',
            'want', 'look', 'use', 'find', 'give', 'tell', 'work', 'call', 'try',
            'indeed', 'because', 'than', 'while', 'where', 'how', 'whoever', 'whenever',
        ])

        filteredWords = [w for w in words if w not in stopWords]
        wordFreq = Counter(filteredWords)
        commonWords = wordFreq.most_common(5)

        summaryLines = [
            f"Number of characters (including spaces): {charCount}",
            f"Number of characters (Excluding spaces): {charCountNoSpaces}",
            f"Number of Lines: {numLines}",
            f"Number of words: {numWords}",
            f"Number of sentences: {numSentences}",
            f"Average word length: {avgWordLen:.2f} characters",
            f"Average sentence length: {avgSentenceLen:.2f} words",
            "",
            "Top 5 most common words (excluding stop words):",
        ]

        if commonWords:
            for word, count in commonWords:
                summaryLines.append(f" {word}: {count}")
        else:
            summaryLines.append("no Frequent words found.")
        return "\n".join(summaryLines)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = textSummary()
    ex.show()
    sys.exit(app.exec_())