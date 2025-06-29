# Raycasting Labyrinth Game

Egy pseudo 3D raycasting labirintus játék Python és Pygame használatával.

## Funkcionalitás

- **Pseudo 3D raycasting motor**: Valós idejű 3D nézet 2D labirintusban
- **Procedurálisan generált labirintus**: Minden játék alkalmával új 32x32-es labirintus
- **Intuitive irányítás**: 
  - WASD: mozgás (W/S előre/hátra, A/D oldalra)
  - Egér: kamera forgatás
  - ESC: szüneteltetés
- **Teljes menürendszer**: Főmenü és szünet menü
- **Minimap**: Kis térkép az aktuális pozícióval és céllal
- **Nyerési feltétel**: Érjük el a labirintus másik végét

## Telepítés és futtatás

1. Győződj meg róla, hogy Python telepítve van (3.7+)
2. Telepítsd a függőségeket:
   ```
   pip install -r requirements.txt
   ```
3. Futtasd a játékot:
   ```
   python main.py
   ```

## Fájlok áttekintése

- `main.py` - Főprogram belépési pont
- `constants.py` - Játék konstansok és beállítások
- `maze.py` - Labirintus generálás és kezelés
- `player.py` - Játékos logika és mozgás
- `raycaster.py` - Raycasting engine a 3D rendereléshez
- `ui.py` - Felhasználói interfész elemek (gombok, menük)
- `game_states.py` - Játék állapot kezelés (menü, játék, szünet)

## Irányítás

- **W**: Előre mozgás
- **S**: Hátra mozgás  
- **A**: Balra mozgás (strafe)
- **D**: Jobbra mozgás (strafe)
- **Egér**: Kamera forgatás
- **ESC**: Szüneteltetés/Menü

## Játék célja

Indulj a labirintus egyik sarkából és találd meg az utat a másik sarokba. A minimap segít a tájékozódásban - a piros pont vagy pozíciód, a zöld pont a cél.

Jó szórakozást!
