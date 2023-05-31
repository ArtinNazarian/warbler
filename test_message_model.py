import os
from unittest import TestCase
from sqlalchemy import exc  

from models import db, User, Message, Follows, Likes

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

from app import app

db.create_all()

class UserModelTestCase(TestCase):

    def setUp(self):
        db.drop_all()
        db.create_all()

        self.uid = 94566
        u = User.signup('testing', 'testing@test.com', 'password', None)
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    
    def test_message_model(self):

        m = Message(text='Hi everyone', user_id=self.uid)
        db.session.add(m)
        db.session.commit()

        self.assertEqual(len(self.u.messages), 1)
        self.assertEqual(self.u.messages[0].text, 'Hi everyone')

    def test_message_like(self):
        m1 = Message(text='I ran a marathon today', user_id=self.uid)
        m2 = Message(text='Playing tennis with friends', user_id=self.uid)

        u = User.signup('seconduser', 'seconduser@test.com', 'password', None)
        uid = 888
        u.id = uid
        db.session.add_all([m1,m2,u])
        db.session.commit()

        u.likes.append(m1)
        db.session.commit()

        l = Likes.query.filter(Likes.user_id == uid).all()
        self.assertEqual(len(l),1)
        self.assertEqual(l[0].message_id, m1.id)