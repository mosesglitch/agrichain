from flask import Flask, request, jsonify, send_file
import qrcode
from PIL import Image
import io

app = Flask(__name__)

def generate_qr_code(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    return img

@app.route('/api/generate_qr_code', methods=['POST'])
def create_qr_code():
    data = request.get_json()
    product_url = data.get('product_url', '')
    print("ppppppp",product_url)
    if not product_url:
        return jsonify({"error": "Product URL is required."}), 400

    img = generate_qr_code(product_url)
    img_io = io.BytesIO()
    # print(img_io, "iiiiiiiiiiiiiiii")

    img.save(img_io, 'PNG')
    img.save("qr-code.png")

    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)