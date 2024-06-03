# Rozpoznawanie tablic rejestracyjnych

1. Detekcja tablic rejestracyjnych
    * Znalezienie pozycji x niebieskiego pionowego prostokąta stosując maskę w przestrzeni barw HSV
    * Wyodrębnienie białych elementów przy pomocy maski w przestrzeni barw HSV
    * Posortowanie białych elementów w zależności od ich powierzchni i wybranie dziesięciu największych
    * Zaakceptowanie pierwszego białego elementu, który spełnia warunki powierzchni, pozycji x oraz ilości narożników
    * Dokonanie transformacji perspektywicznej na wybranym elemencie

2. Rozpoznanie znaków
    * Wykorzystanie adaptacyjnego progowania
    * Posortowanie znalezionych konturów w zależności od ich powierzchni i wybranie dziesięciu największych
    * Posortowanie konturów w zależności od ich pozycji x
    * Wycięcie poszczególnych znaków z obrazu
    * Porównanie wyciętych znaków ze wzorcem i wybranie tego, którego korelacja jest największa
    * Dodanie wykrytch znaków do listy
