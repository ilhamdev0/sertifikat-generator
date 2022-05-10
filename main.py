import logging
import re
import csv
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw

# logging config
logging.basicConfig(format='[%(levelname)s] %(message)s', level = logging.INFO, filename = 'app.log', filemode = 'w')

template = Image.open(r'assets/template.png')
template_lebar = template.width
template_tinggi = template.height

FONT_SIZE = 80
FONT_COLOR = "#EEEEEE"
FONT_FILE = ImageFont.truetype(r'assets/font.ttf', FONT_SIZE)

def clear_output_folder():
    [f.unlink() for f in Path("./out/").glob("*") if f.is_file()]

def slugify(s):
    s = s.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_-]+', '-', s)
    s = re.sub(r'^-+|-+$', '', s)
    return s

def posisi_nama(nama_lebar,nama_tinggi):
    x_pos = 2
    y_pos = 2
    offset_x = 0
    offset_y = -25

    if template_lebar - nama_lebar < 0:
        logging.warning("nama dibawah ini terlalu panjang!")
    
    if x_pos < 1 or y_pos < 1:
        logging.warning("Value terlalu rendah")

    return ((template_lebar - nama_lebar) / x_pos + offset_x, (template_tinggi - nama_tinggi) / y_pos + offset_y)

def buat_sertifikat(nama):
    with Image.open(r'assets/template.png') as sertifikat:
        draw = ImageDraw.Draw(sertifikat)

        # Hitung lebar dan tinggi nama 
        nama_lebar, nama_tinggi = draw.textsize(nama, font=FONT_FILE)

        # Tulis nama ke dalam template
        draw.text(posisi_nama(nama_lebar,nama_tinggi), nama, fill=FONT_COLOR, font=FONT_FILE)

        # Simpan sertifikat
        sertifikat.save("./out/" + slugify(nama) +".png")

        logging.info(f"Sertifikat telah dibuat atas nama: {nama}")
        print(f"Sertifikat telah dibuat atas nama: {nama}")

def input_csv():
    with open('nama.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        jumlah_data = 0

        for row in csv_reader:
            baris = f"{row[0]}"
            buat_sertifikat(baris)
            jumlah_data += 1
        
        print(f"\n{jumlah_data} sertifikat selesai diproses")

def start():
    clear_output_folder()
    input_csv()

if __name__ == "__main__":
    start()
