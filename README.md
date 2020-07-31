> # Репозиторий не обновляется, используйте <a href="https://github.com/pullenti/PullentiServer">PullentiServer</a> + <a href="https://github.com/pullenti/pullenti-client">pullenti-client</a>

# PullentiPython

Зеркало кода для SDK для Python 3 с [pullenti.ru/DownloadPage.aspx](http://www.pullenti.ru/DownloadPage.aspx). Плюс setup.py для выкладки пакета на pypi.org.

## Разработка

Скачать, распаковать архив с [pullenti.ru/DownloadPage.aspx](http://www.pullenti.ru/DownloadPage.aspx)

```bash
make fetch
```

Посмотреть, что изменилось

```bash
git status
git diff
```

Собрать пакет, обратить внимание на версию, например `dist/pullenti-3.14-py3-none-any.whl`

```bash
make clean wheel
```

Загрузить пакет

```bash
make upload
```

Закомитить код

```bash
git add .
git commit -m 'Mirror 3.23'
git push
```
