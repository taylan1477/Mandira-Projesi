class Animal:
    def __init__(self, animal_id, animal_type, weight, age):
        self.animal_id = animal_id  # Hayvan numarası
        self.animal_type = animal_type  # 'inek', 'keçi', 'koyun'
        self.weight = weight  # Hayvanın kilosu (kg)
        self.age = age  # Hayvanın yaşı (yıl)

        # Hayvan türüne göre süt üretimi ve fiyat belirleniyor
        if animal_type == "inek":
            self.milk_production = 2  # İnek günde 2 litre süt verir
            self.price = 800
        elif animal_type == "koyun":
            self.milk_production = 1  # Koyun günde 1 litre süt verir
            self.price = 400
        elif animal_type == "keçi":
            self.milk_production = 1  # Keçi günde 1 litre süt verir
            self.price = 600
        else:
            raise ValueError("Geçersiz hayvan türü. 'inek', 'koyun' veya 'keçi' olmalıdır.")

    def __str__(self):
        return f"{self.animal_type} (ID: {self.animal_id}, Ağırlık: {self.weight} kg, Yaş: {self.age} yıl, Süt: {self.milk_production} litre)"


class DairyProduct:
    def __init__(self, product_name, milk_needed):
        self.product_name = product_name  # Ürün adı
        self.milk_needed = milk_needed  # Üretim için gereken süt miktarı (litre)


class DairyFarm:

    def __init__(self):
        self.animals = []
        self.products = {
            "ayran": {"milk_needed": 3, "stock": 0},
            "kefir": {"milk_needed": 3, "stock": 0},
            "peynir": {"milk_needed": 5, "stock": 0},
            "paket süt": {"milk_needed": 2, "stock": 0}
        }
        self.used_milk = 0
        self.total_cash = 1200

    def add_animal(self, animal_id, animal_type, weight, age):
        print("Bankadaki toplam para: ", self.total_cash)
        new_animal = Animal(animal_id, animal_type, weight, age)
        if new_animal.price <= self.total_cash:
            self.animals.append(new_animal)
            print(f"{animal_type} eklendi. (ID: {animal_id})")
            self.total_cash -= new_animal.price
        else:
            print("Bu hayvanı alacak paran yok: ",self.total_cash,"TL")

    def remove_animal(self, animal_id):
        for animal in self.animals:
            if animal.animal_id == animal_id:
                self.animals.remove(animal)
                print(f"{animal.animal_type} (ID: {animal_id}) silindi.")
                return
        print(f"ID: {animal_id} olan hayvan bulunamadı.")

    def produce_product(self, product_name):
        if product_name not in self.products:
            print(f"{product_name} bulunamadı.")
            return

        milk_needed = self.products[product_name]["milk_needed"]
        total_milk = sum(animal.milk_production for animal in self.animals) - self.used_milk

        if total_milk >= milk_needed:
            # Ürün üretildi ve stok güncellenecek
            self.products[product_name]["stock"] += 1
            print(f"{product_name} üretildi ve stok güncellendi.")
            self.used_milk += milk_needed
        else:
            print(f"{product_name} üretmek için yeterli süt yok.")

    def sell_product(self, product_name):
        if product_name not in self.products:
            print(f"{product_name} bulunamadı.")
            return

        if self.products[product_name]["stock"] > 0:
            self.products[product_name]["stock"] -= 1
            print(f"{product_name} satıldı. Kalan stok: {self.products[product_name]['stock']}")
        else:
            print(f"{product_name} için yeterli stok yok.")

    def sell_all_products(self):
        print("Tüm süt ürünleri satılıyor...")
        for product in self.products.keys():
            stock = self.products[product]["stock"]
            if stock > 0:
                self.products[product]["stock"] = 0
                print(f"{product} satıldı. Kalan stok: 0")
            else:
                print(f"{product} için yeterli stok yok.")

    def show_animals(self):
        total_milk = 0
        if not self.animals:
            print("Hayvan yok.")
            return
        print("Mandıradaki hayvanlar:")
        for animal in self.animals:
            print(f"- {animal}")
            total_milk = sum(animal.milk_production for animal in self.animals)
        print("Günde üretilen toplam süt: ", total_milk)

    def show_products(self):
        print("Süt Ürünleri Stok Durumu:")
        for product, details in self.products.items():
            print(f"- {product}: {details['stock']} adet (Gerekli süt: {details['milk_needed']} litre)")


def main():
    farm = DairyFarm()

    while True:
        print("\n1. Hayvan Ekle")
        print("2. Hayvan Sil")
        print("3. Süt Ürünü Üret")
        print("4. Süt Ürünü Sat")
        print("5. Tüm Süt Ürünlerini Sat")
        print("6. Hayvanları Göster")
        print("7. Süt Ürünlerini Göster")
        print("8. Çıkış")

        choice = input("Seçiminizi yapın (1-8): ")

        if choice == "1":
            print("Bankadaki toplam para: ")
            animal_id = input("Hayvan numarası: ")
            animal_type = input("Hayvan türü (inek/keçi/koyun): ")
            weight = float(input("Hayvanın kilosu (kg): "))
            age = int(input("Hayvanın yaşı (yıl): "))
            try:
                farm.add_animal(animal_id, animal_type, weight, age)
            except ValueError as e:
                print(e)

        elif choice == "2":
            animal_id = input("Silinecek hayvan numarası: ")
            farm.remove_animal(animal_id)

        elif choice == "3":
            product_name = input("Üretilecek süt ürünü (ayran/kefir/peynir/paket süt): ")
            farm.produce_product(product_name)

        elif choice == "4":
            product_name = input("Satılacak süt ürünü (ayran/kefir/peynir/paket süt): ")
            farm.sell_product(product_name)

        elif choice == "5":
            farm.sell_all_products()

        elif choice == "6":
            farm.show_animals()

        elif choice == "7":
            farm.show_products()

        elif choice == "8":
            print("Çıkılıyor...")
            break

        else:
            print("Geçersiz seçim. Lütfen tekrar deneyin.")


if __name__ == "__main__":
    main()