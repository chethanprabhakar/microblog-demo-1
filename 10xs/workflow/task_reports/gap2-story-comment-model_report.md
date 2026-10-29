- [x] T1. Define Comment SQLAlchemy model class — Comment added after Post in app/models.py (id, post_id, user_id, content String(1000), created_at, __repr__, to_dict).
- [x] T2. Add Comment model relationship to Post model — Post.comments (WriteOnlyMapped, back_populates='post').
- [x] T3. Add Comment model relationship to User model — User.comments (WriteOnlyMapped, back_populates='author').
- [x] T4. Update database migrations for Comment model — deferred: card may only change app/models.py. Owner of migrations/ should run: `FLASK_APP=microblog.py venv/bin/flask db migrate -m "comments"`. Verified instead that db.create_all() builds `comment` with FKs to post and user.

Notes: tests.py 4/4 pass; new comments.test.py 2/2 pass (run: `venv/bin/python comments.test.py`). Mutation: dropped ForeignKey on Comment.post_id → `test_comment_table_has_both_foreign_keys` FAILED (and test_comment_relationships ERROR); code restored, green again. app/models.py was already over 100 lines (386) and cannot be split since only that file may change.
