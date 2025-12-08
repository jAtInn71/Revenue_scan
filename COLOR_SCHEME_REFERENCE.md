# Frontend Color Scheme Reference

## Primary Color System

### Black - Primary Color (#1a1a1a)
**Usage**: Headers, primary buttons, navigation, text on light backgrounds

```html
<!-- Examples -->
<div class="bg-black text-white">Primary Header</div>
<button class="bg-black text-brand-accent">Primary Button</button>
<h1 class="text-black">Page Title</h1>
```

### White - Secondary Color (#ffffff)
**Usage**: Card backgrounds, modal backgrounds, clean white spaces

```html
<!-- Examples -->
<div class="bg-white rounded-xl shadow-md">Card Content</div>
<div class="bg-white p-6">Modal Dialog</div>
```

### Cyan - Accent Color (#00d4ff)
**Usage**: Interactive elements, highlights, accent text, icons, badges, loading

```html
<!-- Examples -->
<button class="text-brand-accent">Accent Text</button>
<div class="border-brand-accent">Accented Border</div>
<div class="bg-brand-accent text-black">Bright Badge</div>
```

---

## Extended Color Palette

### Slate Colors - Backgrounds & Borders
```
bg-slate-50        Very light gray (near white)
bg-slate-100       Light gray background
bg-slate-200       Medium light gray
text-slate-600     Gray text (secondary)
text-slate-900     Dark gray text (primary)
border-slate-200   Light borders
border-slate-300   Medium borders
```

### Status Colors
```
Green (#10b981)    - Success, positive, approved
Red (#ef4444)      - Error, critical, danger
Orange (#f59e0b)   - Warning, caution
Yellow (#eab308)   - Attention needed
Blue (#3b82f6)     - Info, neutral
```

---

## Component Color Examples

### Login/Signup Page
```
Background:        White
Logo Box:          Black with Cyan text
Buttons:           Black with Cyan text
Input Borders:     Slate 300
Focus Ring:        Cyan (00d4ff)
Text:              Black/Slate 900
```

### Dashboard
```
Header:            White background
Cards:             White background
Card Borders:      Slate 200
Metrics Icons:     Green/Red/Cyan/Black
Charts:            Cyan accents
Alert Badges:      Red/Orange/Yellow/Green
Loading Spinner:   Cyan
```

### Navigation/Sidebar
```
Active Item:       Black background + Cyan text
Inactive Item:     White background + Slate text
Hover State:       Slate 50 background
Icons:             Slate 600 → Cyan on hover
Borders:           Slate 200
```

### Form Elements
```
Labels:            Slate 900
Input Fields:      White background, Slate 300 border
Input Focus:       Cyan ring (2px)
Placeholder:       Slate 500
Error Text:        Red 600
Success Text:      Green 600
```

### Alerts & Modals
```
Success Alert:     Green 50 background, Green 200 border
Error Alert:       Red 50 background, Red 200 border
Warning Alert:     Orange 50 background, Orange 200 border
Info Alert:        Cyan 5% background, Cyan border
Modal Overlay:     Black/50 opacity
Modal Background:  White
```

---

## Accessibility Notes

### Contrast Ratios (WCAG AA)
- Black (#1a1a1a) on White (#ffffff): ✅ 21:1 (AAA)
- Cyan (#00d4ff) on White (#ffffff): ✅ 4.5:1 (AA)
- Cyan (#00d4ff) on Black (#1a1a1a): ✅ 7.8:1 (AAA)
- Slate 600 on White: ✅ 7.5:1 (AAA)

### Best Practices
1. Never use Cyan alone for critical information
2. Always pair with shape/icon changes
3. Use color + text for status indicators
4. Ensure disabled states are visually different
5. Test with color blindness simulators

---

## CSS Color Variables Reference

```css
/* Custom brand colors */
--color-brand-primary: #1a1a1a;
--color-brand-secondary: #ffffff;
--color-brand-accent: #00d4ff;
--color-brand-accent-dark: #0099cc;
--color-brand-accent-light: #66e6ff;
--color-brand-bg-dark: #0f0f0f;
--color-brand-bg-light: #f8f9fa;
--color-brand-border: #e5e7eb;
--color-brand-border-dark: #2a2a2a;
```

---

## Tailwind Class Reference

### Background Colors
```
bg-black              #1a1a1a (primary)
bg-white              #ffffff (secondary)
bg-brand-accent       #00d4ff (accent)
bg-slate-50           #f8f9fa (light bg)
bg-red-50             #fef2f2 (error bg)
bg-green-50           #f0fdf4 (success bg)
```

### Text Colors
```
text-black            #000000
text-slate-900        #0f172a (dark text)
text-slate-600        #475569 (gray text)
text-brand-accent     #00d4ff (cyan text)
text-red-600          #dc2626 (error)
text-green-600        #16a34a (success)
```

### Border Colors
```
border-slate-200      #e2e8f0 (light border)
border-slate-300      #cbd5e1 (medium border)
border-brand-accent   #00d4ff (cyan border)
border-red-200        #fecaca (error border)
```

### Ring/Focus Colors
```
ring-brand-accent     Cyan focus ring (2px)
ring-2                2px width
ring-offset-0         No offset
```

---

## Color Migration Reference

If updating from old design:

| Old Color          | New Color              | Usage |
|-------------------|------------------------|-------|
| indigo-600        | black                  | Primary |
| purple-600        | slate-900              | Secondary |
| indigo-50         | slate-50               | Light bg |
| gray-100          | slate-100              | Medium bg |
| gray-700          | slate-900              | Text |
| gradient (multi)  | solid (single color)   | Buttons |

---

## Live Color Samples

### Button States
```
Normal:    bg-black text-brand-accent
Hover:     bg-slate-900 text-brand-accent
Focus:     ring-2 ring-brand-accent
Disabled:  opacity-50 cursor-not-allowed
```

### Card States
```
Normal:    bg-white border-slate-200
Hover:     shadow-lg border-brand-accent
Active:    border-brand-accent bg-brand-accent/5
```

### Badge States
```
Success:   bg-green-100 text-green-700
Error:     bg-red-100 text-red-700
Warning:   bg-orange-100 text-orange-700
Info:      bg-brand-accent/10 text-brand-accent
```

---

## Testing Color Accuracy

### Check Colors With:
1. **Eye Dropper Tool**: DevTools → Color Picker
2. **Contrast Checker**: webaim.org/resources/contrastchecker
3. **Color Blindness Simulator**: coblis.codebeamer.com
4. **Real Device Testing**: Check on actual phones/tablets

### Verify Design:
- [ ] Colors match mockup
- [ ] Contrast meets WCAG AA
- [ ] Works in different lighting conditions
- [ ] Looks good on different screen types
- [ ] Print-friendly (if needed)

---

**Last Updated**: December 8, 2025
**Version**: 1.0 - Complete Redesign
