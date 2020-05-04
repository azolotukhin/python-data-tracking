# CLI

### Build (python cli.py proto_builder build_proto)
- Компилирует proto 
- Собирает все query в либу

### Run collector (python cli.py collector_cli collector --kafka-topic test --kafka-group-id test --batch_size 40)
- Запускает коллектор

### Print create tables query (python cli.py schema_migration create_tables)
- Печатает запросы для создания таблиц в БД


#Schema (path: /query)




#Query (path: /query)



##Query Params

- ***${date}*** - Заменяется на конкретную дату (например '2018-01-01') используется в связке c date = ${date}

- ***${date_range}*** Заменятся на интервал дат (напримет '2018-01-01' AND '2018-01-03' в этом случае в выборку попадут  '2018-01-01', '2018-01-02', '2018-01-03'), используется с date BETWEEN ${date_range}

- ***${player_segments}*** Заменяется на фильтры по сегментам игроков (например PS_country = 'US' AND PS_env = 'android' AND PS_web_publisher = 'fb'), если сегменты не используются будет заменен на 1


 
