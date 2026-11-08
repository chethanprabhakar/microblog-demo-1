- [x] T1. Add comment rendering logic to post template — author, content, moment timestamp, "No comments yet" empty state, server-rendered
- [x] T2. Style comments section in post template — Bootstrap utilities only (bg-light, border-start, small, text-muted, p-2, mb-1)
- [x] T3. Implement dynamic comment loading in post view — partial: loadComments(postId) (fetch, render, "Could not load comments" on failure) and addComment (appends + updates count after POST) are defined, but no GET /posts/<id>/comments endpoint exists (only POST), so there is no "Show comments" link; comments are server-rendered by default
- [x] T4. Add comment count to post preview — ngettext "1 comment"/"N comments"; count updates after addComment

Notes: Post.comments is write-only, so the count uses post.query.session.scalars(post.comments.select()), like likes. No test file added (card may only change _post.html); existing `unittest tests` passes (4 OK). Scratch check: /index returned 200 with and without comments. Mutation (fixed 'comments' string) showed "1 comments"; restored. _post.html is over 100 lines and cannot be split within the single-file limit.
