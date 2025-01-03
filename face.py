import cv2
import psycopg2
import os
import bcrypt
from dotenv import load_dotenv
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

load_dotenv()


class SimpleFaceRecognitionApp:
    def __init__(self):
        # Configurações iniciais
        self.db_url = os.getenv("DATABASE_URL")
        if not self.db_url:
            raise ValueError("A variável DATABASE_URL não foi definida no arquivo .env.")

        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.conn = psycopg2.connect(self.db_url)
        self.create_table()

        # Configuração da interface
        self.root = tk.Tk()
        self.root.title("Reconhecimento Facial Simples")

        tk.Label(self.root, text="Reconhecimento Facial", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Cadastrar Usuário", command=self.register_user).pack(pady=5)
        tk.Button(self.root, text="Verificar Entrada", command=self.verify_user).pack(pady=5)
        tk.Button(self.root, text="Sair", command=self.root.quit).pack(pady=10)

        self.root.mainloop()

    def create_table(self):
        """Cria a tabela no banco de dados, se não existir."""
        with self.conn.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                cpf_hash VARCHAR(60) UNIQUE NOT NULL,
                telefone VARCHAR(15),
                imagem BYTEA
            );
            """)
            self.conn.commit()

    def capture_image(self):
        """Captura imagem da webcam"""
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                messagebox.showerror("Erro", "Falha ao capturar imagem.")
                return None

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            cv2.imshow('Capturar Imagem', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('c'):
                cap.release()
                cv2.destroyAllWindows()
                return frame
            elif key == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return None

    def hash_cpf(self, cpf):
        """Gera um hash seguro para o CPF."""
        cpf_bytes = cpf.encode('utf-8')
        return bcrypt.hashpw(cpf_bytes, bcrypt.gensalt()).decode('utf-8')

    def save_user_image(self, image, name, cpf, telefone):
        """Salva imagem do usuário no banco de dados."""
        if image is None:
            messagebox.showerror("Erro", "Imagem inválida.")
            return

        _, buffer = cv2.imencode('.jpg', image)
        image_bytes = buffer.tobytes()

        cpf_hash = self.hash_cpf(cpf)

        with self.conn.cursor() as cursor:
            try:
                cursor.execute("""
                INSERT INTO usuarios (nome, cpf_hash, telefone, imagem)
                VALUES (%s, %s, %s, %s)
                """, (name, cpf_hash, telefone, image_bytes))
                self.conn.commit()
                messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            except psycopg2.Error as e:
                messagebox.showerror("Erro", f"Erro ao salvar no banco de dados: {e}")

    def detect_face(self, image):
        """Detecta rosto na imagem."""
        if image is None:
            return False

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        return len(faces) > 0

    def register_user(self):
        """Fluxo para registrar usuário."""
        image = self.capture_image()
        if image is not None and self.detect_face(image):
            name = simpledialog.askstring("Cadastro", "Digite o nome:")
            cpf = simpledialog.askstring("Cadastro", "Digite o CPF:")
            telefone = simpledialog.askstring("Cadastro", "Digite o telefone:")
            self.save_user_image(image, name, cpf, telefone)
        else:
            messagebox.showerror("Erro", "Nenhum rosto detectado ou captura cancelada.")

    def verify_user(self):
        """Fluxo para verificar usuário."""
        image = self.capture_image()
        if image is not None and self.detect_face(image):
            messagebox.showinfo("Sucesso", "Acesso liberado!")
        else:
            messagebox.showerror("Erro", "Rosto não detectado ou acesso negado.")


if __name__ == "__main__":
    SimpleFaceRecognitionApp()