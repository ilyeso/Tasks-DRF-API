# Tasks-DRF-API
Simple task management API with Django RestFramework
# Task Management API

A basic Django REST Framework API for managing tasks with user assignments, priorities, and file attachments.

## Features

-  Create, read, update, and delete tasks
-  Assign tasks to multiple users
-  Task priorities (1-5, where 1 is highest)
-  Public and private task types
-  PDF file attachments
-  Pagination support
-  Filter tasks by user
-  Get public tasks
-  Comprehensive test suite


The API will be available at `http://localhost:8000/api/tasks/`

## API Documentation

After running the server , visit : `http://localhost:8000/api/schema/swagger-ui/`  for detailed API documentation .


## Running Tests

```bash
python manage.py test tasks
```



## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks/` | List all tasks |
| POST | `/api/tasks/` | Create new task |
| GET | `/api/tasks/{id}/` | Get task details |
| PUT | `/api/tasks/{id}/` | Update task |
| PATCH | `/api/tasks/{id}/` | Partial update |
| DELETE | `/api/tasks/{id}/` | Delete task |
| GET | `/api/tasks/public_tasks/` | Get public tasks |
| GET | `/api/tasks/user_tasks/?user_id={id}` | Get user tasks |

