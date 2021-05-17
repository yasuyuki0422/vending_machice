import sqlite3
import sys
import os


dbname = 'edit.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()

class Vending_machine():
    def __init__(self):
        self.drinks = None
        self.number = None
        self.quantity_1 = None
        self.quantity_2 = None
        self.money1 = None
        self.some_price = None
        self.some_count = None
        self.money2 = None
        self.total_price = None
        self.choice = None


    def drink_names(self):
        cur.execute('SELECT * FROM vending_info')
        a = cur.fetchall()
        drink_name = []
        for b in a:
            print("飲み物:{} 金額:{} 個数:{}".format(b[0],b[1],b[2]))
    # c = cur.fetchone()

    def choose(self):
        while True:
            try:
                self.drinks = str(input("飲み物を選択してください。"))
                cur.execute("select * from vending_info where name = ? ", (self.drinks,))
                drink = cur.fetchone()
                self.quantity_1 = int(drink[2])
                if self.quantity_1 != 0:
                    print("{}の在庫数は{}本です。".format(self.drinks, self.quantity_1))
                    self.quantity_2 = int(drink[1])
                    break

                elif self.quantity_1 == 0:
                    print("在庫が足りないため、他の飲み物を選択してください。")
                    continue

            except TypeError:
                print("文字で入力してください")

    def buy(self):
        while True:
            try:
                self.number = int(input("何本購入しますか?:"))
                if self.quantity_1 >= self.number:
                    self.some_price = self.quantity_2 * self.number
                    print("合計金額は{}円になります".format(self.some_price))
                    self.some_count = self.quantity_1 - self.number
                    break

                elif self.quantity_1 <= self.number:
                    print("在庫よりも多い数値が入力されているため、もう一度入力してください。")
                    continue

            except ValueError:
                print("数値で入力してください")

    def carculate(self):
        while True:
            try:
                self.money1 = int(input('投入金額を入力してください：'))
                if self.money1 < self.some_price:
                    print('投入金額が足りません。')
                    self.total_price = int(self.some_price - self.money1)
                    self.money2 = int(input(str(self.total_price) + "円が不足しているためお金を入れてください:"))
                    while True:
                        try:
                            if self.money2 == self.total_price:
                                print(self.drinks + 'の購入ができました!')
                                cur.execute("update vending_info set quantity = ? where name = ?",(self.some_count, self.drinks,))
                                conn.commit()
                                break

                            elif self.money2 > self.total_price:
                                print("購入出来ました")
                                print("お釣りは" + str(self.money2 - self.total_price) + "円です")
                                cur.execute("update vending_info set quantity = ? where name = ?", (self.some_count, self.drinks,))
                                conn.commit()
                                break

                        except ValueError:
                            print("数値を入力してください")
                    break

                elif self.money1 > self.some_price:
                    print(self.drinks + 'を購入しました!')
                    print('お釣りは' + str(self.money1 - self.total_price) + '円です!')
                    cur.execute("update vending_info set quantity = ? where name = ?", (self.some_count, self.drinks,))
                    conn.commit()
                    break

                else:
                    print(self.drinks + 'を購入しました!')
                    cur.execute("update vending_info set quantity = ? where name = ?", (self.some_count, self.drinks,))
                    conn.commit()
                    break

            except ValueError:
                print("数値で入力してください")



    def roop(self):
        while True:
            self.choice = input('購入を続けますか？YESorNO：')
            if self.choice == 'YES':
                os.system('clear')
                break
            elif self.choice == 'NO':
                print('ご利用ありがとうございました。')
                import menu
                sys.exit()
            else:
                print('YESorNOを入力しください')




vending = Vending_machine()

while True:
    vending.drink_names()
    vending.choose()
    vending.buy()
    vending.carculate()
    vending.roop()


conn.commit()

cur.close()
conn.close()

