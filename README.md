## Customer API

---

### Steps to use:

1. Clone the repository to your system.
2. Build docker images by issuing `docker-compose build`
3. Start the container `docker-compose up -d`
4. Browse the api by visiting `http://localhost/swagger/`

### Steps to use the API via Swagger:

1. A new user should be created by calling `/user/create`
2. Once user is created, use `/user/obtain_token` api to get the token.
3. Once token is generated. Click `Authorize` button in swagger and type `Bearer {token from Step 2}`
4. Now all others apis will be authenticated.
