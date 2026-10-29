import sys
import unittest
sys.path.insert(0, '.')
from app import create_app, db
from app.models import User, Post, Like
from tests import TestConfig


class PostLikeCountCase(unittest.TestCase):
    def setUp(self):
        TestConfig.WTF_CSRF_ENABLED = False
        self.app = create_app(TestConfig)
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def login(self, users):
        self.client.post('/auth/login', data={
            'username': users[0].username, 'password': 'pw'})

    def seed(self):
        users = [User(username=n, email=n + '@x.com') for n in 'abc']
        for u in users:
            u.set_password('pw')
        db.session.add_all(users)
        post = Post(body='hello', author=users[0])
        db.session.add(post)
        db.session.commit()
        return users, post

    def test_pages_render_counts(self):
        users, post = self.seed()
        for u in users[:2]:
            Like.create_like(u, post)
        db.session.commit()
        self.login(users)
        for url in ('/index', '/explore'):
            r = self.client.get(url)
            self.assertEqual(r.status_code, 200)
            self.assertIn('2 likes', r.get_data(as_text=True))

    def test_zero_likes_shown(self):
        users, _ = self.seed()
        self.login(users)
        self.assertIn('0 likes', self.client.get('/explore').get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
