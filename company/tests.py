import json
from django.test import TestCase, Client

from .models     import (
    Country, 
    Region, 
    Company, 
    Photo, 
    News
)

from job.models  import Job


class RegionView(TestCase):
    def setUp(self):
        Country.objects.create(
            id = 1,
            name = 'korea'
        )

        Region.objects.create(
            country_id = 1,
            id = 1,
            name = 'seoul'
        )
    
    def tearDown(self):
        Country.objects.all().delete()
        Region.objects.all().delete()
    
    def test_region_get_success(self):
        client = Client() 
        response = client.get('/company/region')
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(response.json(), 
        {'data' : [{
            'id' : 1,
            'name' : 'seoul'}]
        })
    
    def test_region_get_fail(self):
        client = Client() 
        response = client.get('/company/region?country_id=100')
        self.assertEqual(response.status_code, 400) 
        self.assertEqual(response.json(), {'message' : "INVALID_COUNTRY"})


class CompanyListTest(TestCase):
    def setUp(self):
        Company.objects.create(
            id = 1,
            name = 'Sentbe'
        )

    def tearDown(self): 
        Company.objects.all().delete()
    
    def test_companylist_get_success(self):
        client = Client() 
        response = client.get('/company/list')
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(response.json(), 
        {'data' : [{
            'id' : 1,
            'name' : 'Sentbe', 
            'logo_url' : None, 
            'thumbnail_url' : None,
            'number_positions' : 0}]
        })
    
    def test_companydetail_get_not_found(self):
        client = Client()
        response = client.get('/company/list/3')
        self.assertEqual(response.status_code, 404)


class CompanyDetailTest(TestCase):
    def setUp(self):
        Company.objects.create(
            id = 2,
            name = 'Kakao'
        )

        Photo.objects.create(
            company_id = 2
        )

        News.objects.create(
            company_id =2
        )

        Job.objects.create(
            company_id = 2,
            name = 'job'
        )
    
    def tearDown(self): 
        Company.objects.all().delete()
        Photo.objects.all().delete()
        News.objects.all().delete()
        Job.objects.all().delete()

    def test_companydetail_get_success(self):
        client = Client() 
        response = client.get('/company/2')
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(response.json(),

        {'data' : [{
            'id' : 2,
            'name' : 'Kakao',
            'logo_url' : None,
            'article' : None,
            'salary_new' : None,
            'salary_all' : None,
            'employees' : None,
            'images' : [{
                'name' : None,
                'url' : None
            }],
            'news' : [{
                'name' : None,
                'source' : None,
                'url' : None,
            }],
            'jobs' : [{
                'name' : 'job',
                'reward_amount' : None,
                'deadline' : None,
                'likes' : 0,
            }]
        }]})

    def test_companydetail_get_fail(self):
        client = Client()
        response = client.get('/company/300')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {'message' : "INVALID_COMPANY"}
        )
    
    def test_companydetail_get_not_found(self):
        client = Client()
        response = client.get('/company?company=300')
        self.assertEqual(response.status_code, 404)


