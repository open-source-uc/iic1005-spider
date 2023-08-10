import random


class Card:
    def __init__(self, num, suit, visible):
        self.num = num
        self.suit = suit
        self.visible = visible

    def __str__(self):
        if self.visible:
            self.txt = "XXX"
        else:
            # Mostramos 2 dígitos
            if self.num <= 9:
                n = "0" + str(self.num)
            else:
                n = str(self.num)

            # Ícono bonito
            if self.suit == 0:
                s = "\u2663"
            elif self.suit == 1:
                s = "\u2662"
            elif self.suit == 2:
                s = "\u2660"
            elif self.suit == 3:
                s = "\u2661"
            self.txt = n + s


class Board:
    def __init__(self):
        self.deck = []
        # Lista de columnas
        self.cols = []
        for i in range(0, 10):
            self.cols.append([])
        self.stock = []
        self.moves = []

    def new_game(self, level):
        self.deck = self.create_deck(level)
        self.place_cards(self.deck)

    def create_deck(self, level):
        deck = []
        for i in range(0, 2):  # 2 pack
            for j in range(0, 4):  # 4 suits
                for k in range(1, 14):  # 13 cartas
                    # nivel easy
                    if level == 1:
                        card = Card(k, 0, False)
                    # nivel spider
                    elif level == 2:
                        card = Card(k, j % 2, False)
                    # nivel spider hard
                    elif level == 3 or level == 4:
                        card = Card(k, j, False)
                    deck.append(card)

        random.shuffle(deck)
        return deck

    def place_cards(self, odeck):
        # Creamos una copia del mazo original
        deck = odeck.copy()

        # Se añaden cartas
        # son 6 en las primeras 4
        for columna in range(0, 4):
            for fila in range(0, 6):
                card = deck.pop(0)
                card.visible = False
                self.cols[fila].append(card)

        # y 5 en las últimas 6 Z
        for columna in range(4, 10):
            for fila in range(0, 5):
                card = deck.pop(0)
                card.visible = False
                self.cols[fila].append(card)

        for c in deck:
            self.stock.append(c)

        return

        for col in self.cols:
            col[-1].visible = True

    def load_game(self, path):
        self.stock.clear()
        for c in self.cols:
            c.clear()
        self.deck.clear()
        self.moves.clear()

        r = open(path, "r")
        lines = r.readlines()

        nstock = int(lines[0])

        # Leemos stock
        l = 1  # l de linea
        for i in range(l, l + nstock):
            fs = lines[i].strip().split(";")
            c = Card(int(fs[0]), int(fs[1]), fs[2] == "True")
            self.stock.append(c)
        l = l + nstock

        # Leemos columnas
        for col in range(0, 10):
            ncol = int(lines[l])
            l += 1
            for i in range(l, l + ncol):
                fs = lines[i].strip().split(";")
                c = Card(int(fs[0]), int(fs[1]), fs[2] == "True")
                self.cols[col].append(c)
            l = l + ncol

        # Leemos el deck
        ndeck = int(lines[l])
        l += 1
        for i in range(l, l + ndeck):
            fs = lines[i].strip().split(";")
            c = Card(int(fs[0]), int(fs[1]), fs[2] == "True")
            self.deck.append(c)
        l = l + ndeck

        # Leer movimientos
        nmoves = int(lines[l])
        l += 1
        for i in range(l, l + nmoves):
            fs = lines[i].strip().split(";")
            m = [fs[0], fs[1], fs[2]]
            self.moves.append(m)
        l = l + nmoves

        r.close()

    def save_game(self, path):
        w = open(path, "w")

        # Guardamos el stock
        print(len(self.stock), file=w)
        for c in self.stock:
            print(c.num, c.suit, c.visible, sep=";", file=w)

        # Escribir columnas
        for col in self.cols:
            print(len(col), file=w)
            for c in col:
                print(c.num, c.suit, c.visible, sep=";", file=w)

        # Escribir deck
        print(len(self.deck), file=w)
        for c in self.deck:
            print(c.num, c.suit, c.visible, sep=";", file=w)

        # Escribir movimientos
        print(len(self.moves), file=w)
        for m in self.moves:
            print(m[0], m[1], m[2], sep=";", file=w)

        w.close()

    def max_depth(self):
        max_val = 0
        for c in self.cols:
            if len(c) > max_val:
                max_val = len(c)
        return max_val

    def __str__(self):
        txt = "Stock (" + str(len(self.stock)) + ")\n"
        header = [
            "---",
            "-0-",
            "-1-",
            "-2-",
            "-3-",
            "-4-",
            "-5-",
            "-6-",
            "-7-",
            "-8-",
            "-9-",
        ]
        txt += "\t".join(header) + "\n"
        for i in range(0, self.max_depth()):
            if i <= 9:
                n = "0" + str(i)
            else:
                n = str(i)
            row = [n + "-"]

            for col in self.cols:
                if len(col) <= i:  # Esta columna ya no tiene cartas en nivel i
                    row.append("   ")
                else:
                    row.append(str(col[i]))
            txt += "\t".join(row) + "\n"
        return txt

    def is_finished(self):
        cards = len(self.stock)
        for c in self.cols:
            cards += len(c)
        return cards == 0

    def can_move(self, sc, sr, tc):
        # Todas visibles
        cond_visible = self.is_visible_to_end(sc, sr)

        # Secuencia cons secuencia de pinta
        cond_suit_sequence = self.is_suit_sequence_to_end(sc, sr)

        # Consecutivas
        if len(self.cols[tc]) == 0:
            cond_consecutive = True
        else:
            snum = self.cols[sc][sr].num
            tnum = self.cols[tc][-1].num
            cond_consecutive = tnum == snum + 1

        valid = cond_visible and cond_suit_sequence and cond_consecutive
        return valid

    def is_visible_to_end(self, c, r):
        visible = True
        for card in self.cols[c][r:]:
            visible = visible and card.visible
        return visible

    def is_suit_sequence_to_end(self, c, r):
        num = self.cols[c][r].num
        suit = self.cols[c][r].suit
        valid = True
        i = 1
        for card in self.cols[c][r + 1 :]:
            if (card.suit != suit) or (card.num + i != num):
                valid = False
            i += 1
        return valid

    def move(self, sc, sr, tc):
        self.cols[tc] += self.cols[sc][sr:]
        self.cols[sc] = self.cols[sc][:sr]

        # Dejamos la última visible
        if len(self.cols[sc]) > 0:
            self.cols[sc][-1].visible = True

        # Resuelve y expone si es posible
        if (
            (len(self.cols[tc]) >= 13)
            and self.is_visible_to_end(tc, -13)
            and self.is_suit_sequence_to_end(tc, -13)
        ):
            self.cols[tc] = self.cols[tc][:-13]
            if len(self.cols[tc]) > 0:
                self.cols[tc][-1].visible = True

        # Guardamos el movimiento
        self.moves.append([sc, sr, tc])

    def round(self):
        for tc in range(0, 10):
            card = self.stock.pop(0)
            card.visible = True
            self.cols[tc].append(card)

            # Resuelve y expone si es posible
            if (
                (len(self.cols[tc]) >= 13)
                and self.is_visible_to_end(tc, -13)
                and self.is_suit_sequence_to_end(tc, -13)
            ):
                self.cols[tc] = self.cols[tc][:-13]
                if len(self.cols[tc]) > 0:
                    self.cols[tc][-1].visible = True

        # Guardamos el movimiento
        self.moves.append([-1, -1, -1])

    def restore_by_moves(self, deck, moves):
        # Limpiamos todo por si acaso
        self.stock.clear()
        for c in self.cols:
            c.clear()
        self.deck.clear()
        self.moves.clear()

        # Guardamos el estado
        self.deck = deck
        self.moves = moves

        # Ponemos las cartas en las columnas
        self.place_cards(deck)

        # Guardamos los movimientos
        for m in self.moves:
            if m[0] == -1:
                self.round()
            else:
                self.move(m[0], m[1], m[2])

    def undo(self):
        ndeck = self.deck.copy()
        nmoves = self.moves.copy()
        nmoves.pop(-1)
        self.restore_by_moves(ndeck, nmoves)

    def possible_moves(self):
        possibles = []
        # Posibles movimientos
        for sc in range(0, 10):
            for sr in range(0, len(self.cols[sc])):
                for tc in range(0, 10):
                    if sc != tc:
                        if self.can_move(sc, sr, tc):
                            possibles.append([sc, sr, tc])

        return possibles


if __name__ == "__main__":
    print("Para correr spider, ve las instrucciones del README.md!")
