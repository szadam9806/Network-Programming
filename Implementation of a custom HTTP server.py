import http.server
import socketserver
import os

PORT = 8000
WAREHOUSE_DIR = "warehouses"

class InventoryHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.serve_inventory()

    def serve_inventory(self):
        # Rozdziela ścieżkę na konkretne magazyny
        warehouses = self.path.strip("/").split("_")
        inventory = {}
        invalid_warehouses = []

        #Lecimy po magazynach i dodajemy produkty
        for warehouse in warehouses:
            if not warehouse.isdigit():
                invalid_warehouses.append(warehouse)
                continue

            file_path = os.path.join(WAREHOUSE_DIR, f"{warehouse}.txt")
            if os.path.exists(file_path):
                products = self.parse_html_table(file_path)
                for product, quantity in products.items():
                    inventory[product] = inventory.get(product, 0) + quantity

        total_sum = sum(inventory.values())

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        html = "<html><body><h1>Stan magazynu</h1><table border='1'>"

        if invalid_warehouses:
            html += "<p style='color:red'><strong>Nieprawidlowa nazwa magazynu:</strong> "
            html += ", ".join(invalid_warehouses)
            html += "</p>"
            html += "<p style='color:blue'><strong>Zsumowano tylko poprawne magazyny</strong> "


        html += "<tr><th>Produkt</th><th>Ilosc</th></tr>"
        for product, quantity in inventory.items():
            html += f"<tr><td>{product}</td><td>{quantity}</td></tr>"
        html += "</table>"
        html += f"<p><strong>Suma wszystkich produktow: {total_sum}</strong></p></body></html>"
        self.wfile.write(html.encode())

    def parse_html_table(self, file_path):
        products = {}
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for i in range(len(lines)):
            line = lines[i].strip()
            if line.startswith("<tr>") and i + 2 < len(lines):
                try:
                    name_line = lines[i + 1].strip()
                    qty_line = lines[i + 2].strip()

                    name = name_line.replace("<td>", "").replace("</td>", "").strip()
                    qty = qty_line.replace("<td>", "").replace("</td>", "").strip()

                    quantity = int(qty)
                    products[name] = products.get(name, 0) + quantity
                except Exception as e:
                    print(f"Błąd parsowania w {file_path}: {e}")
        return products

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), InventoryHandler) as httpd:
        print(f"Serwer dziala na porcie {PORT}")
        httpd.serve_forever()
