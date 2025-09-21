# AstroGuessr

An old project from 2023. A simple Tkinter + Matplotlib desktop app that renders a randomized star field with optional overlays for constellations, Messier objects, the celestial equator, and the ecliptic. 

## Quick start

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the app:

```bash
python src/astroguessr.py
```

## Data files

CSV data files are in `Source/data/` and are loaded at runtime:

- `stars.csv`
- `constellations.csv`
- `messier.csv`
- `equator.csv`
- `ecliptic.csv`

## Controls

- Enter numeric `FOV`, `RA`, and `DEC`. Leave blank to randomize on reset.
- Checkboxes toggle overlays and hints. Note that nothing may happen if that toggle doesn't control anything within the FOV
- Use the `Reset` button to re-render with current settings.

## Notes

- Don't put anything thats not a number into the input boxes. 
- I wrote this before knowing how to code. 


