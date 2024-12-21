class Animal:
    def __init__(self, animal_id, animal_type, weight, age):
        self.animal_id = animal_id  # Hayvan numarası
        self.animal_type = animal_type  # 'inek', 'keçi', 'koyun'
        self.weight = weight  # Hayvanın kilosu (kg)
        self.age = age  # Hayvanın yaşı (yıl)

        # Hayvan türüne göre süt üretimi ve fiyat belirleniyor
        if animal_type == "inek":
            self.milk_production = 4  # İnek günde 4 litre süt verir
            self.price = 800
        elif animal_type == "koyun":
            self.milk_production = 2  # Koyun günde 2 litre süt verir
            self.price = 400
        elif animal_type == "keçi":
            self.milk_production = 3  # Keçi günde 3 litre süt verir
            self.price = 600
        else:
            raise ValueError("Geçersiz hayvan türü. 'inek', 'koyun' veya 'keçi' olmalıdır.")

    def feed(self):
        raise NotImplementedError("Bu metod alt sınıflar tarafından uygulanmalıdır.")

    def __str__(self):
        return f"{self.animal_type} (ID: {self.animal_id}, Ağırlık: {self.weight} kg, Yaş: {self.age} yıl, Süt: {self.milk_production} litre) "


class Cow(Animal):
    def feed(self):
        return f"{self.animal_id} numaralı ineğe saman verildi"


class Goat(Animal):
    def feed(self):
        return f"{self.animal_id} numaralı keçiye arpa verildi"


class Sheep(Animal):
    def feed(self):
        return f"{self.animal_id} numaralı koyuna ot verildi"


class DairyProduct:
    def __init__(self, product_name, milk_needed, product_price):
        self.product_name = product_name  # Ürün adı
        self.milk_needed = milk_needed  # Üretim için gereken süt miktarı (litre)
        self.product_price = product_price


class DairyFarm:

    def __init__(self):
        self.animals = []
        self.products = {
            "ayran": {"milk_needed": 3, "stock": 0, "price": 150},
            "kefir": {"milk_needed": 4, "stock": 0, "price": 200},
            "peynir": {"milk_needed": 5, "stock": 0, "price": 250},
            "paket süt": {"milk_needed": 2, "stock": 0, "price": 100}
        }
        self.total_cash = 1200
        self.total_milk = DairyFarm.calculate_total_milk(self.animals)
        self.used_milk = 0

    def add_animal(self, animal_id, animal_type, weight, age):

        # Benzersizlik kontrolü
        if any(animal.animal_id == animal_id for animal in self.animals):
            print(f"ID: {animal_id} ile zaten bir hayvan mevcut.")
            return

        if animal_type == "inek":
            new_animal = Cow(animal_id, animal_type, weight, age)
        elif animal_type == "koyun":
            new_animal = Sheep(animal_id, animal_type, weight, age)
        elif animal_type == "keçi":
            new_animal = Goat(animal_id, animal_type, weight, age)
        else:
            print("Geçersiz hayvan türü.")
            return

        if new_animal.price <= self.total_cash:
            self.animals.append(new_animal)
            print(f"{animal_type} eklendi. (ID: {animal_id})")
            self.total_cash -= new_animal.price
        else:
            print("Bu hayvanı alacak paran yok: ", new_animal.price, "TL")

    def remove_animal(self, animal_id):
        for animal in self.animals:
            if animal.animal_id == animal_id:
                self.animals.remove(animal)
                self.total_cash += animal.price
                print(f"{animal.animal_type} (ID: {animal_id}) satıldı.")
                return
        print(f"ID: {animal_id} olan hayvan bulunamadı.")

    def produce_product(self, product_name):
        if product_name not in self.products:
            print(f"{product_name} bulunamadı.")
            return

        milk_needed = self.products[product_name]["milk_needed"]
        self.total_milk = sum(animal.milk_production for animal in self.animals) - self.used_milk

        if self.total_milk >= milk_needed:
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
            self.total_cash += self.products[product_name]["price"]
            print(f"{product_name} satıldı. Kalan stok: {self.products[product_name]['stock']}")
        else:
            print(f"{product_name} için yeterli stok yok.")

    def sell_all_products(self):
        print("Tüm süt ürünleri satılıyor...")
        for product in self.products.keys():
            stock = self.products[product]["stock"]
            if stock > 0:
                self.total_cash += self.products[product]["price"] * stock
                self.products[product]["stock"] = 0
                print(f"{product} satıldı. Kalan stok: 0")
            else:
                print(f"{product} için yeterli stok yok.")

    @staticmethod
    def calculate_total_milk(animals):
        return sum(animal.milk_production for animal in animals)

    def show_animals(self):
        if not self.animals:
            print("Hayvan yok.")
            return
        print("Mandıradaki hayvanlar:")
        for animal in self.animals:
            print(f"- {animal}")
        total_milk = DairyFarm.calculate_total_milk(self.animals)
        print("Toplam süt üretimi:", total_milk)

    def show_products(self):
        print("Süt Ürünleri Stok Durumu:")
        for product, details in self.products.items():
            print(f"- {product}: {details['stock']} adet (Gerekli süt: {details['milk_needed']} litre)")

    def feed_animals(self):
        if not self.animals:
            print("Hayvan yok.")
            return
        for animal in self.animals:
            print(animal.feed())

    # GÜN METODU EKLENCEK !!!!!!!!!!!!!!!!!

    def skip_day(self):
        print("\nBir gün geçti...")

        # Süt miktarlarını sıfırlayıp yeniden hesaplıyoruz
        self.used_milk = 0
        print("Hayvanlar yeniden süt üretti.")

        # Günlük hayvan süt üretimlerini raporluyoruz
        for animal in self.animals:
            print(f"{animal.animal_id} numaralı {animal.animal_type} günlük {animal.milk_production} litre süt üretti.")

        # Toplam süt miktarını gün sonunda raporluyoruz
        self.total_milk += sum(animal.milk_production for animal in self.animals)
        print(f"Gün sonunda toplam süt miktarı: {self.total_milk} litre")


def main():
    farm = DairyFarm()

    while True:
        print("\nBankadaki toplam para: ", farm.total_cash)
        print("Depomuzdaki toplam süt: ", farm.total_milk)
        print("\n1. Hayvan Satın Al")
        print("2. Hayvan Sat")
        print("3. Süt Ürünü Üret")
        print("4. Süt Ürünü Sat")
        print("5. Tüm Süt Ürünlerini Sat")
        print("6. Hayvanları Göster")
        print("7. Süt Ürünlerini Göster")
        print("8. Hayvanları Besle")
        print("9. Günü Bitir")
        print("10. Çıkış")

        choice = input("Seçiminizi yapın (1-10): ")

        if choice == "1":
            animal_id = input("Hayvan numarası: ")
            animal_type = input("Hayvan türü (inek/keçi/koyun): ")
            weight = float(input("Hayvanın kilosu (kg): "))
            age = int(input("Hayvanın yaşı (yıl): "))
            farm.add_animal(animal_id, animal_type, weight, age)

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
            farm.feed_animals()

        elif choice == "9":
            farm.skip_day()

        elif choice == "10":
            print("Çıkılıyor...")
            break

        else:
            print("Geçersiz seçim. Lütfen tekrar deneyin.")


if __name__ == "__main__":
    main()
