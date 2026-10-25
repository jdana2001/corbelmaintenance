# corbelmaintenance.com

Static website for Corbel Maintenance Services, the parent of 123 Pothole Repair, 123 Concrete Repair and 123 Dock Doors. Hosted on Netlify and built the same way as the 123 sites.

- `build.py` holds the business details (CONFIG and COMPANIES at the top) and all page copy.
- `src/styles.css` is the stylesheet. Corbel's accent is steel blue; orange is reserved for the 123 companies.
- `src/images/` holds the photos.
- `python3 build.py` regenerates the finished site into `site/`, which Netlify publishes as-is.

## Placeholders still to fill

In CONFIG: phone, email and quote response time. In COMPANIES: each company's phone line. They show highlighted in yellow until replaced.

## Forms

Two Netlify Forms: `contact` (home page) and `walkthrough` (For Property Managers). Turn on form detection in Netlify, redeploy, then add an email notification for each form.
