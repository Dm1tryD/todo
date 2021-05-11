import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from todo_api.models import Task, Color, SubTask
from todo_api.serializers import TaskSerializer, SubTaskSerializer, ColorSerializer
from users.models import CustomUser


class TaskApiTestCase(APITestCase):

    def setUp(self):
        self.tasks_url = reverse('task-list')
        self.user_1 = CustomUser.objects.create_user('bob@gmail.com', 'foh34oF34')
        self.user_2 = CustomUser.objects.create_user('susann@gmail.com', 'FHE9huewf')
        self.color = Color.objects.create(name='Black', hex_color='000000')

        self.task_1 = Task.objects.create(author=self.user_1, text='Go to a shop', color=self.color, completed=False)
        self.task_2 = Task.objects.create(author=self.user_1, text='Finish work', color=self.color, completed=True)
        self.task_3 = Task.objects.create(author=self.user_2, text='Go to birthday', color=self.color, completed=False)

    def test_task_get(self):

        self.client.force_login(self.user_1)
        response = self.client.get(self.tasks_url)
        serializer_data = TaskSerializer([self.task_1, self.task_2], many=True).data
        serializer_data_user_3_task = TaskSerializer([self.task_1, self.task_2, self.task_3], many=True).data

        self.assertEqual(serializer_data, response.data, 'User does not see his tasks')
        self.assertNotEqual(serializer_data_user_3_task, response.data, 'Users can see other tasks')

        self.client.logout()
        resp = self.client.get(self.tasks_url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED, 'Unregistered users can see tasks')

    def test_task_post(self):
        task = {'text': 'Do housework', 'color': self.color.pk, 'completed': 'False'}
        json_data = json.dumps(task)
        self.client.force_login(self.user_1)
        response = self.client.post(self.tasks_url, data=json_data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Task was not created')
        self.assertTrue(Task.objects.filter(text=task['text'], color=task['color']), 'Task was not add to database')

        self.client.logout()
        resp = self.client.post(self.tasks_url, json_data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED, 'Unregistered users can create tasks')

    def test_task_put(self):
        put_url = reverse('task-detail', args=(self.task_1.pk,))
        data = {
            'text': 'Read a book',
            'color': self.task_1.color.pk,
            'completed': False
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_1)
        response = self.client.put(put_url, data=json_data, content_type='application/json')
        self.task_1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.task_1.text, data['text'], 'Task has not been changed')

        self.client.logout()
        resp = self.client.put(put_url, data=json_data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_task_delete(self):
        delete_url = reverse('task-detail', args=(self.task_1.pk,))
        self.client.force_login(self.user_1)
        response = self.client.delete(delete_url)
        task_exist = Task.objects.filter(pk=self.task_1.pk).exists()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, 'Task was not deleted')
        self.assertFalse(task_exist, 'Task was not deleted')

        self.client.logout()
        resp = self.client.delete(delete_url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED, 'Unregistered users can delete tasks')


class SubApiTestCase(APITestCase):

    def setUp(self):
        self.sub_tasks_url = reverse('subtask-list')
        self.user_1 = CustomUser.objects.create_user('bob@gmail.com', 'foh34oF34')
        self.user_2 = CustomUser.objects.create_user('susann@gmail.com', 'FHE9huewf')
        self.color = Color.objects.create(name='Black', hex_color='000000')

        self.task_1 = Task.objects.create(author=self.user_1, text='Go to a shop', color=self.color, completed=False)
        self.sub_task_1 = SubTask.objects.create(task=self.task_1, text='Buy tomatoes', completed=True)
        self.sub_task_2 = SubTask.objects.create(task=self.task_1, text='Buy potatoes', completed=False)

        self.task_2 = Task.objects.create(author=self.user_2, text='Go to birthday', color=self.color, completed=False)
        self.sub_task_3 = SubTask.objects.create(task=self.task_2, text='Buy a gift', completed=False)

    def test_subtask_get(self):

        self.client.force_login(self.user_1)
        response = self.client.get(self.sub_tasks_url)
        serializer_data = SubTaskSerializer([self.sub_task_1, self.sub_task_2], many=True).data
        serializer_data_user_2_sub_task = SubTaskSerializer(
            [self.sub_task_1, self.sub_task_2, self.sub_task_3], many=True
        ).data

        self.assertEqual(serializer_data, response.data, 'User does not see his subtasks')
        self.assertNotEqual(serializer_data_user_2_sub_task, response.data, 'Users can see other subtasks')

        self.client.logout()
        resp = self.client.get(self.sub_tasks_url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED, 'Unregistered users can see subtasks')

    def test_subtask_post(self):
        sub_task = {'text': 'Buy lemons', 'task': self.task_1.pk, 'completed': 'False'}
        json_data = json.dumps(sub_task)
        self.client.force_login(self.user_1)
        response = self.client.post(self.sub_tasks_url, data=json_data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Subtask was not created')
        self.assertTrue(SubTask.objects.filter(
            text=sub_task['text'], task=sub_task['task']
        ), 'Subtask was not add to database')

        self.client.logout()
        resp = self.client.post(self.sub_tasks_url, json_data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED, 'Unregistered users can create subtasks')

    def test_subtask_put(self):
        sub_task_put_url = reverse('subtask-detail', args=(self.sub_task_1.pk,))
        data = {
            'text': 'Dont buy tomatoes',
            'task': self.task_1.pk,
            'completed': False
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_1)
        response = self.client.put(sub_task_put_url, data=json_data, content_type='application/json')
        self.sub_task_1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.sub_task_1.text, data['text'], 'Subtask has not been changed')

        self.client.logout()
        resp = self.client.put(sub_task_put_url, data=json_data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subtask_delete(self):
        delete_url = reverse('subtask-detail', args=(self.sub_task_1.pk,))
        self.client.force_login(self.user_1)
        response = self.client.delete(delete_url)
        task_exist = SubTask.objects.filter(pk=self.sub_task_1.pk).exists()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, 'Subtask was not deleted')
        self.assertFalse(task_exist, 'Subtask was not deleted')

        self.client.logout()
        resp = self.client.delete(delete_url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED, 'Unregistered users can delete subtasks')


class ColorApiTestCase(APITestCase):

    def setUp(self):
        self.colors_url = reverse('color-list')
        self.user_1 = CustomUser.objects.create_superuser('bob@gmail.com', 'foh34oF34')
        self.user_2 = CustomUser.objects.create_user('susann@gmail.com', 'FHE9huewf')
        self.color_1 = Color.objects.create(name='Black', hex_color='000000')
        self.color_2 = Color.objects.create(name='White', hex_color='FFFFFF')

    def test_color_get(self):
        self.client.force_login(self.user_1)
        response = self.client.get(self.colors_url)
        serializer_data = ColorSerializer([self.color_1, self.color_2], many=True).data

        self.assertEqual(serializer_data, response.data, 'Administrator does not see colors')
        self.client.logout()

        resp = self.client.get(self.colors_url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED, 'Unregistered users can see colors')

    def test_color_post(self):
        color = {'name': 'Red', 'hex_color': 'FF0000'}
        json_data = json.dumps(color)
        self.client.force_login(self.user_1)
        response = self.client.post(self.colors_url, data=json_data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Color was not created')
        self.assertTrue(Color.objects.filter(
            name=color['name'], hex_color=color['hex_color']
        ), 'Color was not add to database')
        self.client.logout()

        self.client.force_login(self.user_2)
        resp = self.client.post(self.colors_url, json_data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN, 'Users can create color')

    def test_color_put(self):
        color_put_url = reverse('color-detail', args=(self.color_1.pk,))
        data = {
            'name': 'Blue',
            'hex_color': '0000FF',
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_1)
        response = self.client.put(color_put_url, data=json_data, content_type='application/json')
        self.color_1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.color_1.name, data['name'], 'Color has not been changed')
        self.client.logout()

        self.client.force_login(self.user_2)
        resp = self.client.put(color_put_url, data=json_data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_color_delete(self):
        delete_url = reverse('color-detail', args=(self.color_1.pk,))
        self.client.force_login(self.user_1)
        response = self.client.delete(delete_url)
        task_exist = Color.objects.filter(pk=self.color_1.pk).exists()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, 'Color was not deleted')
        self.assertFalse(task_exist, 'Color was not deleted')
        self.client.logout()

        self.client.force_login(self.user_2)
        resp = self.client.delete(delete_url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN, 'Users can delete color')