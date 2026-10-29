import unittest
import sqlalchemy as sa
from app import create_app, db
from app.models import User, Post, Comment
from tests import TestConfig


class CommentModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_comment_relationships(self):
        u = User(username='susan', email='susan@example.com')
        p = Post(body='hello', author=u)
        c = Comment(content='nice', post=p, author=u)
        db.session.add_all([u, p, c])
        db.session.commit()
        self.assertEqual(db.session.scalars(p.comments.select()).all(), [c])
        self.assertEqual(db.session.scalars(u.comments.select()).all(), [c])
        self.assertEqual(c.to_dict()['author'], 'susan')
        self.assertTrue(c.to_dict()['created_at'].endswith('Z'))

    def test_comment_table_has_both_foreign_keys(self):
        fks = sa.inspect(db.engine).get_foreign_keys('comment')
        self.assertEqual({f['referred_table'] for f in fks}, {'post', 'user'})


if __name__ == '__main__':
    unittest.main()
