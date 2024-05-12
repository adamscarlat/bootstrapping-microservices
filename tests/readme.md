Running the integration tests
-----------------------------
* Run all commands at the `tests/integreation` folder

* First run compose:

```bash
docker-compose -f ../../docker-compose-dev.yml up --build -d
```

* Run the tests with pytest:

```bash
pytest -s
```

Notes
-----
* Since the tests are running async functions, we need to install `pytest-asyncio` (see requirements.txt)
  - Then decorate any test that uses async with `@pytest.mark.asyncio`

Running the e2e tests
---------------------
* Run all commands at the project root

* Start the stack:
```bash
docker-compose -f docker-compose-dev.yml up --build -d
```

* (first time only) run: 
  - `npm install`
  - `npx playwright install`

* Run tests:

```bash
npx playwright test --reporter=list
```