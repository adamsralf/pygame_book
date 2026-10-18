from pygame.color import THECOLORS

with open("thecolors.tex", "w", encoding="utf-8") as file:
    for name, rgba in sorted(THECOLORS.items()):
        r, g, b = rgba[:3]
        file.write(
            f"\\colorentry{{{name}}}"
            f"{{{r}}}{{{g}}}{{{b}}}\n"
        )