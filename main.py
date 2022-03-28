"""
This example showcases postgres features
"""
from tortoise import Tortoise, fields, run_async
from tortoise.models import Model


class Report(Model):
    id = fields.IntField(pk=True)
    content = fields.JSONField()

    links: fields.ReverseRelation["Link"]

    def __str__(self):
        return str(self.content)

class Link(Model):
    report : fields.ForeignKeyRelation[Report] = fields.ForeignKeyField(
        "models.Report", related_name="links", on_delete='CASCADE'
    )

    def __str__(self):
        return "Links to " + str(self.report)


async def run():
    await Tortoise.init(
        {
            "connections": {
                "default": {
                    "engine": "tortoise.backends.asyncpg",
                    "credentials": {
                        "host": "db",
                        "port": "5432",
                        "user": "tortoise",
                        "password": "pass",
                        "database": "tortoise",
                    },
                }
            },
            "apps": {"models": {"models": ["__main__"], "default_connection": "default"}},
        },
    )
    await Tortoise.generate_schemas()

    report_data = {"foo": "bar"}
    print(await Report.all().delete())
    r = await Report.create(content=report_data)
    print(r)
    print(await Report.filter(content=report_data).all())
    print(await Link.create(report=r))
    print(await Link.create(report=r))
    print(await Link.all())
    print(await Report.all().delete())
    print(await Link.all())


if __name__ == "__main__":
    run_async(run())
