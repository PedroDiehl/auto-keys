import cv2
from pyzbar import pyzbar


users = {
   "19101160": {
      "nome": "Aluno1",
      "email": "aluno1.email@email.com",
      "funcao": "Aluno"
   },
   "19100949": {
      "nome": "Aluno2",
      "email": "aluno2.email@email.com",
      "funcao": "Aluno"
   },
   "6419898": {
      "nome": "Servidor1",
      "email": "servidor1.email@email.com",
      "funcao": "Servidor"
   }
}


class BarcodeReader:
   def __init__(self):
      pass

   def find_barcode(self, frame):
      barcodes = pyzbar.decode(frame) 
      self.log_barcodes(barcodes)

      for barcode in barcodes:
         self.draw_barcode_box(barcode, frame)
         barcode_data = self.extract_barcode_data(barcode)
         user = self.interpret_barcode_data(barcode_data)

         print(user)

      return bool(barcodes)

   def draw_barcode_box(self, barcode, frame):
      self.barcode_image = frame.copy()

      (x, y, w, h) = barcode.rect
      cv2.rectangle(self.barcode_image, (x - 10, y - 10), (x + w + 10, y + h + 10), (255, 0, 0), 2)
      cv2.imshow('Barcode box', self.barcode_image)
      cv2.waitKey(0)

      return

   def extract_barcode_data(self, barcode):
      barcode_data = barcode.data.decode("utf-8")
      barcode_type = barcode.type

      print(f"Found barcode type: {barcode_type} barcode: {barcode_data}")

      return barcode_data

   def interpret_barcode_data(self, barcode_data):
      # Write a regex to interpret the barcode data
      # the last two digits are always 01

      # The first digit can be ignored (check)
      # The second digit can be 1 or 3 (user role) (check)

      # Example: 011910116001 -> user 19101160

      # Check if in this example there is noise
      # or if the first digit information is important
      # Example: x30641989801 -> user 6419898

      # Split the last two digits
      user_number = barcode_data[:-2]

      # Check if the second digit is 1 or 3
      if user_number[1] == "1":
         user_number = user_number[2:]
      elif user_number[1] == "3":
         user_number = user_number[3:]

      # Check if the user number is in the users dictionary
      if user_number not in users:
         print("User not found")
         return

      print(f"User {user_number} found")

      return users[user_number]

   def barcode_capture(self):
      # open the camera
      cap = cv2.VideoCapture(0)

      while True:
         # Capture frame-by-frame
         ret, frame = cap.read()

         # Our operations on the frame come here
         cv2.imshow('Webcam', frame)

         if self.find_barcode(frame) or (cv2.waitKey(1) & 0xFF == ord('q')):
            break

      return

   def log_barcodes(self, barcodes):
      print(f"Found {len(barcodes)} barcode(s)")
      print(barcodes)
      return

if __name__ == '__main__': 
   barcode_reader = BarcodeReader()
   barcode_reader.barcode_capture()
