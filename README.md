# 🎯 Crowdfunding Platform Backend

This is the **backend API** for a crowdfunding web application, built with Django and Django REST Framework (DRF). It supports user registration, authentication, project listings, pledging, and admin functionality.

---

## 🚀 Features

- 🧑 User registration & token-based authentication
- 📦 CRUD operations for projects and pledges
- 📂 Category tagging for projects
- 🔒 Permissions and ownership enforcement
- 🧪 Comprehensive test coverage
- ⚙️ CI/CD via GitHub Actions.

---

## 🧰 Tech Stack

- Python 3.12
- Django 4.x
- Django REST Framework
- Pytest
- GitHub Actions

---

### Concept/Name

Sprout is a community-focused crowdfunding platform dedicated to supporting conservation and outdoor recreation projects. Whether developing new parks, restoring rivers and wildlife habitats, or creating outdoor spaces that inspire future generations, Sprout empowers communities and public land managers to bring their visions to life. By connecting passionate individuals with meaningful environmental projects, we help ensure a greener, more accessible outdoors for everyone.

---

### Intended Audience/User Stories

Sprout is intended for people who share a vested interest in preserving natural spaces and enhancing outdoor recreation for current and future generations. Sprout can be used as a platform to raise donation towards charities of interest or launch crowdfunding campaigns for local conservation and outdoor projects.

---

### API Spec

| URL                    | HTTP Method | Purpose                                                              | Request Body                                                                                                                                                                                                                                                              | Successful Response Code | Authentication/Authorisation                                           |
| ---------------------- | ----------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------ | ---------------------------------------------------------------------- |
| /projects/             | GET         | Get a list of all projects to view                                   | N/A                                                                                                                                                                                                                                                                       | 200                      | None -view only                                                        |
| /projects/pk/          | GET         | Get the details of one project with associated pledges and  category | N/A                                                                                                                                                                                                                                                                       | 200                      | None                                                                   |
| /projects/             | POST        | Create a project                                                     | {<br>"title": "Test project4",<br>"description": "testing",<br>"goal": 1,<br>"image": "<br><br>[https://tse4.mm.bing.net/th?id=OIP.dm4JwdZmorEWeATp2nlSCgAAAA&pid=Api](https://tse4.mm.bing.net/th?id=OIP.dm4JwdZmorEWeATp2nlSCgAAAA&pid=Api)",<br>"is_open": "True"<br>} | 201                      | a user - needs to have login details and is logged in                  |
| /projects/pk/          | PUT         | Update project details (owner field cannot be updated)               | {<br>"title": "CHANGE THIS",<br>"is_open": "False"<br>}                                                                                                                                                                                                                   | 200                      | A logged-in user who is the project creator                            |
| /projects/pk/          | DELETE      | Delete a project                                                     | N/A                                                                                                                                                                                                                                                                       | 204                      | A logged-in user who is the project creator                            |
| /category/pk/          | GET         | A list of project belonging to a Category                            | N/A                                                                                                                                                                                                                                                                       | 200                      | None                                                                   |
| /category/pk/          | PUT         | Update the category                                                  | N/A                                                                                                                                                                                                                                                                       | 201                      | ADMIN                                                                  |
| /category/pk/          | DELETE      | Delete a Category                                                    | N/A                                                                                                                                                                                                                                                                       | 204                      | ADMIN                                                                  |
| /pledges/              | GET         | Get a list of all the pledges                                        | N/A                                                                                                                                                                                                                                                                       | 200                      | Admin (Superuser)                                                      |
| /pledges/pk/           | GET         | Get the details of one pledge                                        | N/A                                                                                                                                                                                                                                                                       | 200                      | Admin/owner of the pledge                                              |
| /projects/pk/          | GET         | Get all the pledges associated with one project                      | N/A                                                                                                                                                                                                                                                                       | 200                      | None                                                                   |
| /pledges/              | POST        | Make a pledge                                                        | {<br>"amount": 50,<br>"comment": "Love this project!",<br>"anonymous": false,<br>"project": 1<br>}                                                                                                                                                                        | 201                      | A logged-in user                                                       |
| /pledges/pk/           | PUT         | Update a pledge                                                      | {<br>"amount": 500,<br>"comment": "Updating",<br>"anonymous": false,<br>}                                                                                                                                                                                                 | 201                      | A logged-in user who created the pledge (Admin Should not have access) |
| /pledge/pk/            | DEL         | Delete a pledge                                                      | N/A                                                                                                                                                                                                                                                                       | 200                      | Admin                                                                  |
| /users/                | GET         | Get a list of all existing users                                     | N/A                                                                                                                                                                                                                                                                       | 200                      | Admin                                                                  |
| /users/api-auth-token/ | POST        | User log in                                                          | {<br>”username”:”user”,<br>”password”:”password”,<br>}                                                                                                                                                                                                                    | 200                      | A user who has log in details                                          |
| /users/                | POST        | Create a user                                                        | {<br>”username”:”user”,<br>”email”:”email@mail.com”,<br>”password”:”password”,<br>}                                                                                                                                                                                       | 201                      | None                                                                   |
| /users/pk/             | PUT         | Update user detail                                                   | {<br>”email”:”email1@mail.com”,<br>}                                                                                                                                                                                                                                      | 200                      | Admin/account owner                                                    |
| /users/pk/             | DELETE      | Delete a user                                                        |                                                                                                                                                                                                                                                                           | 204                      | Admin                                                                  |

---

### DB Schema

![Entity Relation Diagram for Sprout](./images/ERD.png)

---

### GET a list of all available projects

![A screenshot of Insomnia, demonstrating a successful GET method for project endpoint](./images/GET_ALL_PROJECTS.png)

### POST method for making a pledge

A screenshot of Insomnia, demonstrating a successful POST method for a pledge endpoint ![](./images/post_pledge.png)

Confirming new pledge show up by looking at the ProjectDetail endpoint ![](./images/project_and_pledge.png)

### Token

A screenshot of Insomnia, demonstrating a token being returned.![](./images/token.png)

---

### Step-by-step instruction to register a new user and create a new project

1. Create a new user by entering the username, email and password fields in json format via POST method to /users/ endpoint ![](./images/creating_new_user.png)
2. Log in as a user via POST request to /api-token-auth/ endpoint to retrieve a token ![](./images/login.png)
3. Copy the token from step 2 into the Auth tab in Insomnia ![](./images/addtoken.png)
4. Make a POST request to /projects/ endpoint with the required fields i.e. "title","goal","image","is_open" and "category" filled out ![](./images/new_project_creation.png)

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/ambo-n/crowdfunding_back_end.git
```
