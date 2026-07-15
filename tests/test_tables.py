from services.table_service import TableService

service = TableService()

print(f"Таблиц: {len(service.tables)}")

print()

table = service.get_tables()[0]

print(table.name)

print(table.dice)

print()

for _ in range(5):

    print(

        service.random_result(

            table.name

        )

    )