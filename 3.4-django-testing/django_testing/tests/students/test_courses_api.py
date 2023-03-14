''' Тесты на правильность выполнения кода '''

import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from students.models import Course, Student


'''создание фикстуры клиент/студент'''
@pytest.fixture
def client():
    return APIClient()


'''создание фабрики фикстуры курсов'''
@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory



'''создание фабрики фикстуры студентов'''
@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory



''' тест на отображение курса из БД'''
@pytest.mark.django_db
def test_get_cource(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=1)

    # Act
    response = client.get('/api/v1/courses/')

    # Assert
    data = response.json()

    assert response.status_code == 200
    assert courses[0].name == data[0]['name']



'''тест на отображение всех/какого-то количества курсов из БД'''
@pytest.mark.django_db
def test_get_course_list(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)

    # Act
    response = client.get('/api/v1/courses/')

    # Assert
    data = response.json()

    for i, course in enumerate(data):
        assert courses[i].name == course['name']
    assert response.status_code == 200



'''тест на фильтрацию курсов из БД по id'''
@pytest.mark.django_db
def test_get_filter_course(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)
    i = 5

    # Act
    response = client.get(f'/api/v1/courses/, {'id': courses[i].id}/')

    # Assert
    # data = response.json()
    assert response.status_code == 200
    assert courses[i].name == response['id']



'''тест на фильтрацию курса по наименованию из БД'''
@pytest.mark.django_db
def test_get_filter_course_name(client, course_factory):

    # Arrange
    courses = course_factory(_quantity=20)
    i = 1

    # Act
    response = client.get(f'/api/v1/courses/?name={courses[i].name}')

    # pprint(f'данные: {data}')

    # Assert
    data = response.json()
    assert response.status_code == 200
    assert courses[i].name == data[0]['name']



'''тест на создание курса в БД'''
@pytest.mark.django_db
def test_create_course(client):

    # Act
    response = client.post('/api/v1/courses/', data={'name': 'one_course'})

    # Assert
    assert response.status_code == 201



'''тест на переименование курса в БД'''
@pytest.mark.django_db
def test_update_course(client, course_factory):

    # Arrange
    courses = course_factory(_quantity=2)

    # Act
    response = client.patch(f'/api/v1/courses/{courses[0].id}/', data={'name': 'two_course'})

    # Assert
    assert response.status_code == 200



'''тест на удаление курса из БД'''
@pytest.mark.django_db
def test_delete_course(client, course_factory):

    # Arrange
    courses = course_factory(_quantity=2)

    # Act
    response = client.delete(f'/api/v1/courses/{courses[0].id}/')

    # Assert
    assert response.status_code == 204


