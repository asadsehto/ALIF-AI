import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton

from scripts.chat import generate_response

class HadithChatbotUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hadith AI Chatbot")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.chatbox = QTextEdit(self)
        self.chatbox.setReadOnly(True)
        layout.addWidget(self.chatbox)

        self.inputbox = QTextEdit(self)
        layout.addWidget(self.inputbox)

        self.send_button = QPushButton("Ask", self)
        self.send_button.clicked.connect(self.handle_query)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

    def handle_query(self):
        user_query = self.inputbox.toPlainText()
        if user_query.strip():
            self.chatbox.append(f"👤 You: {user_query}")
            response = generate_response(user_query)
            self.chatbox.append(f"🤖 AI: {response}")
            self.inputbox.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HadithChatbotUI()
    window.show()
    sys.exit(app.exec())
