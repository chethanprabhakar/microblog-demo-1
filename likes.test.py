import unittest
import sqlalchemy as sa
from app import create_app, db
from app.models import User, Post, Like
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ELASTICSEARCH_URL = None


class LikeModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
        self.u = User(username='u', email='u@x.com')
        self.v = User(username='v', email='v@x.com')
        self.p = Post(body='hi', author=self.v)
        db.session.add_all([self.u, self.v, self.p])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_table_created(self):
        self.assertIn('like', sa.inspect(db.engine).get_table_names())

    def test_create_like_is_idempotent(self):
        a = Like.create_like(self.u, self.p)
        db.session.commit()
        b = Like.create_like(self.u, self.p)
        db.session.commit()
        self.assertEqual(a.id, b.id)
        self.assertEqual(len(db.session.scalars(sa.select(Like)).all()), 1)

    def test_create_like_twice_before_commit(self):
        Like.create_like(self.u, self.p)
        Like.create_like(self.u, self.p)
        db.session.commit()
        self.assertEqual(len(db.session.scalars(sa.select(Like)).all()), 1)

    def test_getters(self):
        Like.create_like(self.u, self.p)
        Like.create_like(self.v, self.p)
        db.session.commit()
        self.assertEqual(len(Like.get_likes_by_post(self.p)), 2)
        self.assertEqual(len(Like.get_likes_by_user(self.u)), 1)

    def test_toggle(self):
        self.assertTrue(Like.toggle_like(self.u, self.p))
        db.session.commit()
        self.assertFalse(Like.toggle_like(self.u, self.p))
        db.session.commit()
        self.assertEqual(Like.get_likes_by_post(self.p), [])


if __name__ == '__main__':
    unittest.main()
