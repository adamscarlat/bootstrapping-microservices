Packaging and publishing the pypi package
-----------------------------------------
```bash
# Make sure that the previous dist folder is removed
rm -r dist/

# Requires pip installing build
python -m build

# Use --repository-url if not using the default pypi.org one
twine upload dist/*
```