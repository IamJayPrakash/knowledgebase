# Cumulative Layout Shift (CLS): Root Causes, Layout Stability, and Fixes

---

## 🐣 1. Layman's Analogy (Hinglish + Real-World ELI5)
Aap mobile par ek article padh rahe ho. Aap "Cancel" button dabane wale the, lekin achanak upar ek image ya ad load hua aur pura content 2 inch neeche chhalang maar gaya! Aapka ungli "Confirm Purchase" button par lag gayi! Is unexpected visual jump ko **Layout Shift** kehte hain.
CLS score target: **< 0.1**.

---

## 📌 2. Point-Wise Core Mechanics & Edge Cases

1. **Common Causes of CLS**:
   - Images, videos, or iframes without explicit `width` and `height` (or CSS `aspect-ratio`).
   - Dynamic ad banners and widgets injected without reserved placeholder containers.
   - Web Fonts causing FOIT (Flash of Invisible Text) or FOUT (Flash of Unstyled Text).
   - Injected banners (cookie consents) at the top of the viewport pushing content down.
2. **CSS `aspect-ratio`**: Allows browsers to calculate layout space before images download.
3. **`font-display: optional` or `font-display: swap` with size-adjust**: Eliminates font swap layout jumps.

---

## 💻 3. Line-by-Line Commented Code Snippets

```html
<!-- Line 1: Anti-pattern causing severe CLS: Image without dimensions -->
<!-- <img src="banner.jpg" alt="Sale" /> -->

<!-- Line 4: Correct: Explicit dimensions allow browser to reserve exact layout box -->
<img 
  src="banner.jpg" 
  width="1200" 
  height="400" 
  alt="Summer Sale Banner" 
  style="width: 100%; height: auto; aspect-ratio: 1200 / 400;" 
/>

<!-- Reserved Ad Container to prevent ad injection shifts -->
<div 
  id="ad-banner-slot" 
  style="min-height: 250px; background-color: #f3f4f6; display: flex; align-items: center; justify-content: center;"
>
  <span style="color: #9ca3af;">Advertisement</span>
</div>
```
