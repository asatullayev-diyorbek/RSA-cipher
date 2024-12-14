import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox
)
from PyQt5.QtCore import Qt  # Qt import qilinadi
import math

class RSAGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("RSA Shifrlash")
        self.setGeometry(100, 100, 800, 500)
        self.showMaximized()

        # Kerakli xabarlar
        self.stars = '*'*45
        self.lines = '-'*45

        # Asosiy layout
        main_layout = QHBoxLayout()

        # Chap tomon - Kiritish va tugmalar
        left_layout = QVBoxLayout()

        # Tub sonlar uchun label va inputlar
        self.p_label = QLabel("Birinchi tub son (p):")
        self.p_label.setFont(QFont('Arial', 18))
        self.p_input = QLineEdit()
        self.p_input.setStyleSheet("height: 50px; font-size: 22px")
        left_layout.addWidget(self.p_label)
        left_layout.addWidget(self.p_input)

        self.q_label = QLabel("Ikkinchi tub son (q):")
        self.q_label.setFont(QFont('Arial', 18))
        self.q_input = QLineEdit()
        self.q_input.setStyleSheet("height: 50px; font-size: 22px")
        left_layout.addWidget(self.q_label)
        left_layout.addWidget(self.q_input)

        # Ochiq kalit uchun label va input
        self.e_label = QLabel("Ochiq kalit (e):")
        self.e_label.setFont(QFont('Arial', 18))
        self.e_input = QLineEdit()
        self.e_input.setStyleSheet("height: 50px; font-size: 22px")
        left_layout.addWidget(self.e_label)
        left_layout.addWidget(self.e_input)

        # Xabar uchun label va input
        self.message_label = QLabel("Shifrlash uchun xabar:")
        self.message_label.setFont(QFont('Arial', 18))
        self.message_input = QTextEdit()
        self.message_input.setStyleSheet("height: 100px; font-size: 14px")
        left_layout.addWidget(self.message_label)
        left_layout.addWidget(self.message_input)

        # Tugmalar
        self.generate_button = QPushButton("Kalitlarni yaratish")
        self.generate_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px; padding: 10px 20px; font-size: 18px;")
        self.generate_button.clicked.connect(self.generate_keys)
        left_layout.addWidget(self.generate_button)

        self.encrypt_button = QPushButton("Shifrlash")
        self.encrypt_button.setStyleSheet("background-color: #008CBA; color: white; border-radius: 5px; padding: 10px 20px; font-size: 18px;")
        self.encrypt_button.clicked.connect(self.encrypt_message)
        left_layout.addWidget(self.encrypt_button)

        self.decrypt_button = QPushButton("Deshifrlash")
        self.decrypt_button.setStyleSheet("background-color: #f44336; color: white; border-radius: 5px; padding: 10px 20px; font-size: 18px;")
        self.decrypt_button.clicked.connect(self.decrypt_message)
        left_layout.addWidget(self.decrypt_button)

        self.clear_button = QPushButton("Tozalash")
        self.clear_button.setStyleSheet("background-color: #b1b1b1; color: black; border-radius: 5px; padding: 10px 20px; font-size: 18px;")
        self.clear_button.clicked.connect(self.clear_inputs)
        left_layout.addWidget(self.clear_button)

        self.programmers_info = QPushButton("Dasturchilar:\nAsadbek Sotvoldiyev\nDiyorbek Asatullayev")
        self.programmers_info.setStyleSheet("background-color: #c1c1c1; color: black; border-radius: 5px; padding: 10px 20px; font-size: 18px; height: 150px")
        left_layout.addWidget(self.programmers_info)

        # O'ng tomon - Izohlar va natija
        right_layout = QVBoxLayout()

        # Asosiy izohlar uchun qism
        self.main_explanation_layout = QVBoxLayout()
        self.main_explanation_label = QLabel("ASOSIY IZOH:")
        self.main_explanation_label.setFont(QFont('Arial', 18))
        self.main_explanation_text = QTextEdit()
        self.main_explanation_text.setFont(QFont('Arial', 18))
        self.main_explanation_text.setReadOnly(True)
        self.main_explanation_layout.addWidget(self.main_explanation_label)
        self.main_explanation_layout.addWidget(self.main_explanation_text)
        right_layout.addLayout(self.main_explanation_layout)

        # Oraliq izohlar uchun qism
        self.intermediate_explanation_layout = QVBoxLayout()
        self.intermediate_explanation_label = QLabel("ORALIQ IZOH:")
        self.intermediate_explanation_label.setFont(QFont('Arial', 18))
        self.intermediate_explanation_text = QTextEdit()
        self.intermediate_explanation_text.setFont(QFont('Arial', 18))
        self.intermediate_explanation_text.setReadOnly(True)
        self.intermediate_explanation_layout.addWidget(self.intermediate_explanation_label)
        self.intermediate_explanation_layout.addWidget(self.intermediate_explanation_text)
        right_layout.addLayout(self.intermediate_explanation_layout)

        # Barcha layoutlarni birlashtirish
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        # Asosiy vidjet
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # O'zgaruvchilar
        self.steps = []
        self.n = None
        self.phi = None
        self.e = None
        self.d = None

        # O'zgaruvchilar haqida ma'lumot
        # self.info_label = QLabel("Dasturchilar: Asadbek Sotvoldiyev, Diyorbek Asatullayev")
        # self.info_label.setFont(QFont('Arial', 16))
        # self.info_label.setAlignment(Qt.AlignCenter)
        # main_layout.addWidget(self.info_label)

    def get_font(self):
        # Return a standard font for the application
        return self.font().setPointSize(18)

    def append_step(self, text, is_intermediate=False):
        if is_intermediate:
            self.intermediate_explanation_text.append(text)
        else:
            self.main_explanation_text.append(text)

    def is_prime(self, num):
        self.append_step("~~ Tublikga tekshirish ~~", is_intermediate=True)
        self.append_step(f"{num} tub sonligini tekshirish jarayoni boshlandi.", is_intermediate=True)
        if num <= 1:
            self.append_step(f"{num} 1 dan katta bo'lishi kerak!", is_intermediate=True)
            return False
        for i in range(2, int(math.sqrt(num)) + 1):
            self.append_step(f"{num} ni {i} ga bo'linishi tekshirilmoqda.", is_intermediate=True)
            if num % i == 0:
                self.append_step(f"{num} {i} ga bo'linadi, tub emas.", is_intermediate=True)
                return False
        self.append_step(f"{num} tub son.", is_intermediate=True)
        return True

    def generate_keys(self):
        self.append_step("***** Kalitlarni yaratish *****", is_intermediate=False)
        self.append_step("Kalitlarni yaratish jarayoni boshlanmoqda:", is_intermediate=True)
        try:
            p = int(self.p_input.text())
            q = int(self.q_input.text())

            self.append_step(f"p = {p}, q = {q}", is_intermediate=True)

            self.append_step("~~ Tublikga tekshirish ~~", is_intermediate=False)

            if not self.is_prime(p) or not self.is_prime(q):
                QMessageBox.warning(self, "Xatolik", "p va q tub sonlar bo'lishi kerak!")
                self.append_step("Xatolik! p va q tub sonlar bo'lishi kerak!", is_intermediate=True)
                self.append_step("Xatolik! p va q tub sonlar bo'lishi kerak!")
                return

            if p == q:
                self.append_step("p va q har xil bo'lishi kerak!", is_intermediate=True)
                QMessageBox.warning(self, "Xatolik", "p va q har xil bo'lishi kerak!")
                self.append_step("Xatolik! p va q har xil bo'lishi kerak!")
                return

            self.append_step("~ ~ ~")

            self.n = p * q
            self.phi = (p - 1) * (q - 1)

            self.append_step(f"n = {self.n}, φ(n) = {self.phi}", is_intermediate=True)
            self.append_step(f"Ochiq kalit (n: p*q) = {self.n}")
            self.append_step(f"Yopiq kalit (φ(n): (p-1)*(q-1)) = {self.phi}")
            self.append_step("Kalitlarni yaratish jarayoni tugadi.")
            self.append_step(self.stars)
            self.append_step("Kalitlarni yaratish jarayoni tugadi.", is_intermediate=True)
            self.append_step(self.lines, is_intermediate=True)
        except ValueError:
            self.append_step("Kiritilgan qiymatlar noto'g'ri.", is_intermediate=True)
            self.append_step("Kiritilgan qiymatlar noto'g'ri.")
            QMessageBox.warning(self, "Xatolik", "Iltimos, faqat butun son kiriting!")

    def encrypt_message(self):
        self.append_step("***** Shifrlash *****", is_intermediate=False)
        self.append_step("Shifrlash jarayoni boshlanmoqda:", is_intermediate=True)
        try:
            self.e = int(self.e_input.text())
            self.append_step(f"e = {self.e}", is_intermediate=True)

            if math.gcd(self.e, self.phi) != 1:
                self.append_step("e va φ(n) o'zaro tub emas.", is_intermediate=True)
                QMessageBox.warning(self, "Xatolik", "e va φ(n) o'zaro tub bo'lishi kerak!")
                return

            message = self.message_input.toPlainText()
            self.append_step(f"Shifrlanayotgan xabar: '{message}'", is_intermediate=True)
            cipher = []
            cipher_char = []
            for char in message:
                self.append_step(f"Shifrlanayotgan belgi: {char}", is_intermediate=True)

                ascii_value = ord(char)
                encrypted_char = pow(ascii_value, self.e, self.n)  # (m^e) % n
                cipher.append(encrypted_char)
                cipher_char.append(chr(encrypted_char))

            self.append_step(f"Shifrlangan xabar: {cipher}", is_intermediate=True)
            self.append_step(f"Shifrlangan xabar (ASCII): {cipher}")
            self.append_step(f"Shifrlangan xabar: '{cipher_char}'")
            self.append_step(f"Shifrlash jarayoni tugadi")
            self.append_step(self.lines, is_intermediate=True)
            self.append_step(self.stars)

            self.cipher_text = cipher
        except:
            self.append_step("Kiritilgan e noto'g'ri.", is_intermediate=True)
            QMessageBox.warning(self, "Xatolik", "Iltimos, faqat butun son kiriting!")

    def decrypt_message(self):
        self.append_step("***** Deshifrlash *****", is_intermediate=False)
        self.append_step("Deshifrlash jarayoni boshlanmoqda:", is_intermediate=True)
        try:
            self.append_step(f"Yopiq kalitni hisoblash")
            d = self.calculate_d()

            if not d:
                return

            self.append_step(f"Yopiq kalit (d): {d}", is_intermediate=True)

            decrypt = []
            decrypt_chars = ""
            for char in self.cipher_text:
                self.append_step(f"Deshifrlanayotgan belgi: {chr(char)}", is_intermediate=True)

                self.append_step(f"ASCII qiymati: {char}", is_intermediate=True)

                decrypt_char = pow(char, d, self.n)
                self.append_step(
                    f"Deshifrlangan qiymati: {char}^{self.d} mod({self.n}) = {decrypt_char} - '{chr(decrypt_char)}'",
                    is_intermediate=True)

                decrypt.append(decrypt_char)
                decrypt_chars = f"{decrypt_chars}{chr(decrypt_char)}"

            self.append_step(f"Deshifrlangan xabar: {self.cipher_text}", is_intermediate=True)
            self.append_step(f"Deshifrlangan xabar (ASCII): {decrypt}")
            self.append_step(f"Deshifrlangan xabar: {decrypt_chars}")
            self.append_step(f"Deshifrlash jarayoni tugadi")
            self.append_step(self.lines, is_intermediate=True)
            self.append_step(self.stars)
        except Exception as e:
            self.append_step("Deshifrlashda xatolik.", is_intermediate=True)
            QMessageBox.warning(self, "Xatolik", f"Deshifrlashda xatolik: {e}")

    def calculate_d(self):
        self.append_step("Ochiq kalit (e) va φ(n) o'zaro tub son bo'lishi kerak", is_intermediate=True)

        for d_candidate in range(2, self.phi):
            if (self.e * d_candidate) % self.phi == 1:
                self.append_step(f"Yopiq kalit (d) topildi: d = {d_candidate}", is_intermediate=True)
                self.append_step(f"Yopiq kalit (d) topildi: d = {d_candidate}")
                return d_candidate

        self.append_step("Yopiq kalit (d) topilmadi!", is_intermediate=True)
        self.append_step("Yopiq kalit (d) topilmadi!")
        QMessageBox.warning(self, "Xatolik", "Yopiq kalit (d) topilmadi!")
        return None

    def clear_inputs(self):
        self.p_input.clear()
        self.q_input.clear()
        self.e_input.clear()
        self.message_input.clear()
        self.main_explanation_text.clear()
        self.intermediate_explanation_text.clear()
        self.append_step(self.stars)
        self.append_step("Tozalash jarayoni tugadi.", is_intermediate=True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = RSAGUI()
    gui.show()
    sys.exit(app.exec_())
