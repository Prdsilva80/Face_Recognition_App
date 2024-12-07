import cv2
import psycopg2
import os
import bcrypt
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

class SimpleFaceRecognition:
    def __init__(self):
        # Buscar a URL do banco de dados a partir do arquivo .env
        self.db_url = os.getenv("DATABASE_URL")
        if not self.db_url:
            raise ValueError("A variável DATABASE_URL não foi definida no arquivo .env.")

        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.conn = psycopg2.connect(self.db_url)
        self.create_table()

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
                print("Falha ao capturar imagem.")
                return None

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            cv2.putText(frame, "Pressione 'C' para capturar, 'Q' para sair", 
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

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
        # Converte o CPF para bytes e gera um salt
        cpf_bytes = cpf.encode('utf-8')
        # Usa bcrypt para gerar um hash
        return bcrypt.hashpw(cpf_bytes, bcrypt.gensalt()).decode('utf-8')

    def verify_cpf(self, cpf, stored_hash):
        """Verifica se o CPF corresponde ao hash armazenado."""
        return bcrypt.checkpw(cpf.encode('utf-8'), stored_hash.encode('utf-8'))

    def save_user_image(self, image, name, cpf, telefone):
        """Salva imagem do usuário no banco de dados."""
        if image is None:
            print("Imagem inválida.")
            return

        # Codificar a imagem como bytes
        _, buffer = cv2.imencode('.jpg', image)
        image_bytes = buffer.tobytes()

        # Gerar hash do CPF
        cpf_hash = self.hash_cpf(cpf)

        # Inserir no banco de dados
        with self.conn.cursor() as cursor:
            try:
                cursor.execute("""
                INSERT INTO usuarios (nome, cpf_hash, telefone, imagem)
                VALUES (%s, %s, %s, %s)
                """, (name, cpf_hash, telefone, image_bytes))
                self.conn.commit()
                print("Usuário cadastrado com sucesso!")
            except psycopg2.Error as e:
                print(f"Erro ao salvar no banco de dados: {e}")

    def detect_face(self, image):
        """Detecta rosto na imagem."""
        if image is None:
            return False

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        return len(faces) > 0

    def run(self):
        """Executa o fluxo principal da aplicação."""
        while True:
            print("\nOpções:")
            print("1 - Cadastrar usuário")
            print("2 - Verificar entrada")
            print("3 - Sair")

            choice = input("Escolha: ")

            if choice == '1':
                print("Posicione seu rosto e pressione 'C' para capturar")
                image = self.capture_image()
                if image is not None and self.detect_face(image):
                    name = input("Nome: ")
                    cpf = input("CPF: ")
                    telefone = input("Telefone: ")
                    self.save_user_image(image, name, cpf, telefone)
                else:
                    print("Nenhum rosto detectado ou captura cancelada.")

            elif choice == '2':
                print("Posicione seu rosto e pressione 'C' para verificar")
                image = self.capture_image()
                if image is not None and self.detect_face(image):
                    print("Acesso liberado!")
                else:
                    print("Acesso negado. Rosto não detectado.")

            elif choice == '3':
                break

if __name__ == "__main__":
    app = SimpleFaceRecognition()
    app.run()