# Image prompts — littlestjames.net

Generate these, then hand them back and I'll drop them into `site/assets/`.
Filenames and dimensions matter — the CSS already points at these exact paths.

---

## 1. `hero.jpg` — REQUIRED · 2400 × 1400 px · JPG

This sits **behind the hero text at 34% opacity**, cover-cropped and anchored at
`center 60%`. So: the middle band gets covered by big type, the bottom third is
what people actually see, and it must be dark enough that cream-white text stays
readable on top. Do not let it get busy or bright in the center.

**Prompt to paste:**

> A wide cinematic matte painting of a small tropical island at late golden hour,
> viewed from low down and slightly across a calm dark ocean. A thin strip of pale
> sand, a handful of palms leaning over the water, gentle surf. The sun is low and
> warm but mostly out of frame, throwing a soft amber glow across the horizon line.
> Colour palette strictly limited to: warm gold #E8B44C, deep teal #1B4D4B, and
> near-black #0B0F0F. Deep shadow across the upper third of the image fading to a
> darker sky; the water and island detail sit in the lower third. Soft, hazy,
> low-contrast — almost silhouetted. Painterly and atmospheric, not photorealistic,
> not illustrative-cartoon. Very subtle hint of blocky geometric structure in the
> terrain, suggested rather than literal. Horizontal composition with a calm,
> uncluttered centre. No text, no logos, no watermarks, no people, no user
> interface, no game HUD. 2400x1400.

**Negative prompt (if your tool takes one):**
`text, letters, watermark, logo, people, characters, HUD, UI, neon, purple, magenta, high contrast, busy detail in centre, lens flare, minecraft blocks, voxel cubes, pixelated`

> **If it comes back too bright or too busy**, tell the generator "darker, hazier,
> less detail, more negative space in the upper two-thirds" and regenerate. The
> page looks better with a plain gradient than with a fighting-for-attention photo
> — the CSS gradient underneath is a complete design on its own, so this image is
> genuinely optional.

---

## 2. `divider.png` — OPTIONAL · 2400 × 160 px · PNG with transparency

The section dividers are currently done in pure CSS (a stepped gold pixel strip),
which costs nothing and scales perfectly. You don't need this file. But if you
want something richer between sections, generate this and I'll wire it in.

**Prompt to paste:**

> A seamless horizontal border strip: a stylised shoreline where dark water meets
> pale sand, rendered as a chunky stepped pixel edge, like a low-resolution sprite
> blown up large. Warm gold #E8B44C highlights along the waterline, deep teal
> #1B4D4B water below, fully transparent above the sand line. Flat, graphic, two
> or three colours only, no gradients, no shading. Tiles seamlessly left to right.
> Extremely wide and short banner format. No text, no logos. 2400x160, transparent
> background PNG.

**Negative prompt:** `text, logo, watermark, gradient, 3d, realistic, shadow, noise`

---

## 3. `icon.png` — you already have this · export at 512 × 512 px · PNG

Your gold-monogram-on-dark icon. Just export it square at 512×512 and hand it
over — it's used as the favicon, the hero badge, and the footer mark. There's a
plain placeholder in `assets/icon.png` right now that yours will replace.

**Bonus, unrelated to the website:** if you want that same icon showing up next to
the server in players' Minecraft multiplayer lists, export a **second** copy at
exactly **64 × 64 px**, name it `server-icon.png`, and drop it in your server's
root folder next to `server.properties`. Minecraft is strict about that size.

---

## 4. `og-image.png` — DONE, nothing needed

Already built and in place at 1200×630. I composited this one directly rather
than prompting for it, because image generators reliably garble rendered text and
this graphic is mostly text. If you'd rather have artwork behind the wordmark,
generate the `hero.jpg` above and say the word — I'll rebuild the og image with
that as its background.
