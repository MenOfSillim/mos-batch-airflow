# mos-batch-airflow

```shell
docker cp /mnt/storage1/airflow/webtoon.csv kafka-mongo:/data/

mongoimport --db crawling --collection webtoon --type csv --headerline --drop --file webtoon-headline.csv
```
