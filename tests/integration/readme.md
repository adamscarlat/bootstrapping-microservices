Running the integration tests
-----------------------------
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