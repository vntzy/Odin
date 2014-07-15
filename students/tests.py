from django.utils import unittest
from django.test.client import Client
from .models import CheckIn, User, HrLoginLog
from django.conf import settings

client = Client()

class CheckInCase(unittest.TestCase):
    def setUp(self):
        self.checkin_settings = '123'
        settings.CHECKIN_TOKEN = self.checkin_settings 
        
        self.student_user = User.objects.create_user('ivo_student@gmail.com', '123')
        self.student_user.status = User.STUDENT
        self.student_user.mac = '4c:80:93:1f:a4:50'
        self.student_user.save()

        self.hr_user = User.objects.create_user('ivan_hr@gmail.com', '1234')
        self.hr_user.status = User.HR
        self.hr_user.mac = '4c:80:93:1f:a4:51'
        self.hr_user.save()

    def tearDown(self):
        self.student_user.delete()
        self.hr_user.delete()

    def test_new_check_in_status(self):
        response = client.post('/set-check-in/', {
            'mac': self.student_user.mac, 
            'token': self.checkin_settings,
        })

        self.assertEqual(response.status_code, 200)

    def test_new_check_in_result(self):
        response = client.post('/set-check-in/', {
            'mac': self.student_user.mac, 
            'token': self.checkin_settings,
        })

        checkin = CheckIn.objects.get(student=self.student_user)

        assert checkin is not None

    def test_new_check_in_case_insensitive(self):
        response = client.post('/set-check-in/', {
            'mac': self.student_user.mac, 
            'token': self.checkin_settings,
        })

        checkin = CheckIn.objects.get(student=self.student_user)

        assert checkin is not None

    def test_double_checkin_same_day(self):
        response_first = client.post('/set-check-in/', {'mac': self.student_user.mac, 
            'token': self.checkin_settings,
        })

        response_second = client.post('/set-check-in/', {'mac': self.student_user.mac, 
            'token': self.checkin_settings,
        })

        self.assertEqual(response_first.status_code, 200)
        self.assertEqual(response_second.status_code, 418)

    def test_hr_login_log(self):
        before_log = HrLoginLog.objects.count()
        client.login(username='ivan_hr@gmail.com', password='1234')
        after_log = HrLoginLog.objects.count()

        self.assertEqual(before_log + 1, after_log)
