- [x] T1. Fetch like count — GET /posts/<id>/likes (added by like-route card) is called on page load for logged-in users; server-rendered count is the fallback
- [x] T2. Display count — span#likesN rendered with ngettext, plus Like/Unlike button using guarded window.toggleLike (POST /posts/<id>/like, reads JSON like_count)
- [x] T3. Styling — Bootstrap utilities only (small text-muted, btn-link btn-sm)
- [x] T4. Zero/unavailable — "0 likes" shown; fetch failure or missing like_count shows "Likes unavailable"

Notes: tests pass (`unittest tests`, plus spec/post_likes.test.py rendering /index and /explore → 200). Mutation (hardcode 0) made the 2-likes test fail; restored. Count in template uses post.query.session.scalars(post.likes.select()) since templates have no db. JS updates use English "like(s)" strings (no ngettext client-side). No CSRF on the fetch, matching translate().
