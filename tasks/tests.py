from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Task


class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user1', password='testpasswd')
    
    def test_create_task(self):
        task = Task.objects.create(
            label = 'Test Task',
            description = 'Tast Task description',
            type= 'public',
            priority = 3
        )

        self.assertEqual(task.label ,'Test Task')
        self.assertEqual(task.priority, 3)
        self.assertEqual(task.type , 'public')
    
    def test_task_prio_validation(self):
        task = Task(
            label='Test Task',
            description='Test Task description',
            priority=6
        )

        with self.assertRaises(Exception):
            task.full_clean()
    
    def test_task_affected_to_users(self):
        task = Task.objects.create(
            label='Project Task',
            description='Task for many users',
            type='private',
            priority=1
        )
        task.affected_to.add(self.user)
        self.assertEqual(task.affected_to.count(), 1)
        self.assertIn(self.user, task.affected_to.all())


class APITEST(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password="passwrd1")
        self.user2 = User.objects.create_user(username='user2', password="passwrd2")

        self.task1 = Task.objects.create(
            label='Public Task1',
            description='public task1 description',
            type='public',
            priority=1
        )

        self.task2 = Task.objects.create(
            label='private Task2',
            description='private task description',
            type='private',
            priority=3
        )

        self.task2.affected_to.add(self.user1)
    
    def test_create_task_api(self):
        user1 = User.objects.get(username = 'user1')
        user2 = User.objects.get(username = 'user2')
        self.client.force_login(user1)

        data = {
            'label': 'Task1_test_api',
            'description' : 'description : Task1_test_api',
            'type' : 'public',
            'priority' : 3 ,
            'affected_to_ids' : [self.user1.id]
        }

        response = self.client.post('/api/tasks/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3 )
        self.assertEqual(response.data['label'],'Task1_test_api')

    def test_update_task_api(self):
        user1 = User.objects.get(username = 'user2')
        self.client.force_login(user1)

        data = {
            'label': 'updated task1 label api',
            'description' : 'updated description : Task1_test_api',
            'type' : 'private',
            'priority' : 5 ,
            'affected_to_ids' : [self.user2.id]
        }
        response = self.client.put(f'/api/tasks/{self.task1.id}/', data, format= 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.label,'updated task1 label api')
        self.assertEqual(self.task1.priority,5)
    
    def test_delete_task_api(self):
        user1 = User.objects.get(username = 'user2')
        self.client.force_login(user1)

        response = self.client.delete(f'/api/tasks/{self.task1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 1)
    
    def test_get_public_tasks_api(self):
        user1 = User.objects.get(username = 'user2')
        self.client.force_login(user1)

        response  = self.client.get('/api/tasks/public_tasks/')
        self.assertEqual( response.status_code, status.HTTP_200_OK)
        self.assertEqual( len(response.data['results']), 1 )
        self.assertEqual( response.data['results'][0]['type'], 'public' )
    
    def test_get_user_tasks_api(self):
        user1 = User.objects.get(username = 'user2')
        self.client.force_login(user1)

        response = self.client.get(f'/api/tasks/user_tasks/?user_id={self.user1.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], self.task2.id)
    

    def user_tasks_ordered_by_prio(self):
        user1 = User.objects.get(username = 'user2')
        self.client.force_login(user1)

        task3 = Task.objects.create(
            label='task priority 1',
            description='Prio 1 task description',
            type='private',
            priority=1 )
        
        task3.affected_to.add(self.user1)

        response = self.client.get(f'/api/tasks/user_tasks/?user_id={self.user1.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['priority'], 1)
        self.assertEqual(results[1]['priority'], 2)

    def test_user_tasks_pagination(self):
        user1 = User.objects.get(username = 'user2')
        self.client.force_login(user1)

        for i in range(16):
            task = Task.objects.create(
                label=f'task {i}',
                description=f'description of task {i}',
                type='private',
                priority= (i % 5) + 1
                )
            task.affected_to.add(self.user1)
        response = self.client.get(f'/api/tasks/user_tasks/?user_id={self.user1.id}&page=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3) # should be the same as the page_size in views.py TaskPagination
        self.assertIsNotNone(response.data['next'])

        response = self.client.get(f'/api/tasks/user_tasks/?user_id={self.user1.id}&page=6')
        self.assertEqual(len(response.data['results']), 2) # last page has 2 tasks
