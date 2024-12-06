import cv2
import os

class SimpleFaceRecognition:
    def __init__(self, storage_dir='user_images'):
        self.storage_dir = storage_dir
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)

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
            
            # Desenha retângulos nos rostos detectados
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            # Adiciona instruções na tela
            cv2.putText(frame, 
                        "Pressione 'C' para capturar, 'Q' para sair", 
                        (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        0.7, 
                        (0, 255, 0), 
                        2)
            
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

    def save_user_image(self, image, name, cpf, telefone):
        """Salva imagem do usuário"""
        if image is None:
            print("Imagem inválida.")
            return

        filename = f"{name}_{cpf}.jpg"
        filepath = os.path.join(self.storage_dir, filename)
        
        cv2.imwrite(filepath, image)
        
        # Salvar metadados
        metadata_filepath = os.path.join(self.storage_dir, f"{name}_{cpf}_info.txt")
        with open(metadata_filepath, 'w') as f:
            f.write(f"Nome: {name}\n")
            f.write(f"CPF: {cpf}\n")
            f.write(f"Telefone: {telefone}\n")

    def detect_face(self, image):
        """Detecta rosto na imagem"""
        if image is None:
            return False
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        return len(faces) > 0

    def run(self):
        """Executa o fluxo principal da aplicação"""
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
                    print("Usuário cadastrado!")
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
