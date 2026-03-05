# slidev-theme-czechitas

Czechitas brand theme for [Slidev](https://sli.dev/), matching the official lecturer PPTX template.

## Usage

In the frontmatter of your `slides.md`, set the theme to the local path:

```yaml
---
theme: ./theme
---
```

The theme enforces a light color scheme and defaults to **Open Sans** / **Source Code Pro** fonts.

## Layouts

### `cover`

Title slide with gradient background and Czechitas character illustration.

```yaml
---
layout: cover
subtitle: Optional subtitle
author: Author name
date: Date string
---

# Slide title
```

### `section`

Section divider with gradient background — for introducing new parts of a talk.

```yaml
---
layout: section
subtitle: Optional subtitle
---

# Section title
```

### `default`

Standard content slide with white background and Czechitas logo in the footer.

### `center`

Centered content slide — same as `default` but with centered text.

### `image-right`

Two-column layout: content on the left, image on the right.

```yaml
---
layout: image-right
image: /path/to/image.png
---

# Heading

Content goes here.
```

### `bio`

Speaker introduction card with photo, optional QR code, and bio text.

```yaml
---
layout: bio
image: /path/to/photo.jpg
name: Speaker Name
subtitle: Role or affiliation
---

Bio text goes here.

::qr::
<QRCode url="https://example.com" :size="120">Label</QRCode>
```

## Components

### `<CzechitasLogo>`

Renders the Czechitas logo. Props: `size` (`"small"` | `"medium"`), `invert` (boolean for white variant).

### `<QRCode>`

Generates a QR code image. Props:

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `url` | String | (required) | URL to encode |
| `size` | Number | `160` | Size in pixels |
| `dark` | String | `#2D2E83` | Foreground color |
| `light` | String | `#ffffff` | Background color |

Slot content is displayed as a label below the QR code.
