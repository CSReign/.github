# README navigation

The public organization profile, member profile, HQ, Lab, and Atelier landing READMEs share a compact horizontal contents bar and a **Top** button beside each H2/H3 heading. Individual linked SVG pills wrap naturally instead of putting the page inside a wide table. GitHub controls the page layout; the artwork supplies Goddess Veiled colors, rounded corners, a soft sheen and shadow, and outlined Outfit lettering.

## Maintain the headings and links

- Keep the explicit `readme-top` anchor at the beginning of each README.
- Each section has an explicit anchor matching its original GitHub heading fragment, including `project-tracker` and `-glitter-brain`. Keep those IDs stable when changing display copy so existing links continue to work.
- The contents block lives between `GODDESSVERSE:CONTENTS:START` and `GODDESSVERSE:CONTENTS:END`. It lists all H2/H3 sections in reading order; longer headings can use a compact artwork label while retaining the complete heading in the link title and image alt text.
- Add a linked `assets/nav/back-to-top.svg` image beside each new H2/H3 heading and a matching entry in the contents bar. Native heading text stays readable and selectable.
- Keep all contents links and header controls outside the generated `PROJECT-PREVIEW` and `GLITTER-BRAIN` blocks. The private preview updater owns those blocks; navigation does not change their contents or refresh behavior.
- Publish new public assets before publishing private README references to them. Artwork contains generic section labels only, never task data.

## Rebuild the artwork

`scripts/build_navigation.py` owns the label list, sizes, and styling. It requires Python, `fonttools`, Brotli support for WOFF2, and the Outfit variable font. With those dependencies available, run from this repository:

```sh
python3 scripts/build_navigation.py \
  --font ../headquarters/dashboard/node_modules/@fontsource-variable/outfit/files/outfit-latin-wght-normal.woff2
```

The script deterministically regenerates `assets/nav/*.svg`. Font files are not redistributed; letterforms are outlined. [Brand identity and font credits](BRAND.md).

Before publishing, check that every contents fragment has one matching explicit anchor, every Top button targets `readme-top`, all SVG references exist, the preview blocks are unchanged, and the rendered navigation fits narrow screens.
