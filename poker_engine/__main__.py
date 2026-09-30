from .deck import Deck


def main():
    deck = Deck()

    print(f"Deck initial : {deck.remaining} cartes")

    deck.shuffle()

    print("\nDeck mélangé.")

    cards = deck.draw_many(2)

    print("\nDeux cartes tirées :")

    for card in cards:
        print(f"- {card}")

    print(f"\nCartes restantes : {deck.remaining}")


if __name__ == "__main__":
    main()
