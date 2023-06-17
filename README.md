# Poetry環境のセットアップ
```
pip install poetry
```
```
poetry install
```

※
```
rm -rf .venv
```


# requirement.txtの追加
```
poetry export -f requirements.txt --output requirements.txt
```

# 開発環境の起動
```
docker compose up
```