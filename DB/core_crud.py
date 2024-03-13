from sqlalchemy import cast, insert, select, text, update, delete
from DB.database import async_engine, sync_engine
from DB.models import Base, UserOrm, StatusTask, TaskOrm


class SyncCore:
    @staticmethod
    def create_table(drop_table: bool = False):
        if drop_table is False:
            Base.metadata.drop_all(sync_engine)
            Base.metadata.create_all(sync_engine)
        else:
            raise Exception("давай ка ты поставишь drop_table = False")


class AsyncCore:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def insert_user(data: dict):
        """
        data = {
        "user_name": str,
        "email": str
        }
        """
        async with async_engine.connect() as conn:
            stmt = text(
                'INSERT INTO "user" (user_name, email) VALUES(:user_name, :email)'
            )
            stmt = stmt.bindparams(user_name=data["user_name"], email=data["email"])
            await conn.execute(stmt)
            await conn.commit()

    @staticmethod
    async def insert_auth(data: dict):
        """
        data = {
        "user_id": int,
        "email": str,
        "password": str
        }
        """
        async with async_engine.connect() as conn:
            stmt = text(
                'INSERT INTO "auth" (user_id, email, password) VALUES(:user_id, :email, :password)'
            )
            stmt = stmt.bindparams(
                user_id=data["user_id"], email=data["email"], password=data["password"]
            )
            await conn.execute(stmt)
            await conn.commit()

    @staticmethod
    async def insert_task(data: dict):
        """
        data = {
        "title": str,
        "description": str256,
        "deadline": datetime.datetime(2024, 2, 29),
        "performer_id" : int,
        "status": StatusTask | None
        }
        """
        async with async_engine.connect() as conn:
            query = insert(TaskOrm).values(
                title=data["title"],
                description=data["description"],
                deadline=data["deadline"],
                performer_id=data["performer_id"],
            )
            await conn.execute(query)
            await conn.commit()

    @staticmethod
    async def select_task_by_user_id(data: dict):
        """
        data = {
        "performer_id" : int,
        }
        """
        async with async_engine.connect() as conn:
            stmt = text('SELECT * FROM "task" WHERE performer_id=:performer_id')
            stmt = stmt.bindparams(
                performer_id=data["performer_id"],
            )
            data_task = await conn.execute(stmt)
            res = data_task.fetchall()
            return res

    @staticmethod
    async def select_user_by_id(data: dict):
        """
        data = {
        "user_id": int,
        }
        """
        async with async_engine.connect() as conn:
            stmt = text('SELECT * FROM "user" WHERE id=:user_id')
            stmt = stmt.bindparams(user_id=data["user_id"])
            data = await conn.execute(stmt)
            res = data.fetchall()
            return res

    @staticmethod
    async def select_auth_by_login(data: dict):
        """
        data = {
        "email": str,
        }
        """
        async with async_engine.connect() as conn:
            stmt = text('SELECT * FROM "auth" WHERE email=:email')
            stmt = stmt.bindparams(email=data["email"])
            data = await conn.execute(stmt)
            res = data.fetchall()
            return res

    @staticmethod
    async def select_auth_by_user_id(data: dict):
        """
        data = {
        "user_id": int,
        }
        """
        async with async_engine.connect() as conn:
            stmt = text('SELECT * FROM "auth" WHERE user_id=:user_id')
            stmt = stmt.bindparams(user_id=data["user_id"])
            data = await conn.execute(stmt)
            res = data.fetchall()
            return res

    @staticmethod
    async def select_user_by_email(data: dict):
        """
        data = {
        "email": str,
        }
        """
        async with async_engine.connect() as conn:
            stmt = text('SELECT * FROM "user" WHERE email=:email')
            stmt = stmt.bindparams(login=data["email"])
            data = await conn.execute(stmt)
            res = data.fetchall()
            return res

    @staticmethod
    async def update_task_stastus(data: dict):
        """
        data = {
        "status": TaskOrm,
        "performer_id": int
        }
        """
        async with async_engine.connect() as conn:
            query = (
                update(TaskOrm)
                .values(status=data["status"])
                .where(TaskOrm.performer_id == data["performer_id"])
            )
            await conn.execute(query)
            await conn.commit()

    @staticmethod
    async def update_user_name_by_id(data: dict):
        """
        data = {
        "new_data": str,
        "user_id": int,
        }
        """
        async with async_engine.connect() as conn:
            stmt = text('UPDATE "user" SET user_name=:new_data WHERE id=:user_id')
            stmt = stmt.bindparams(new_data=data["new_data"], user_id=data["user_id"])
            await conn.execute(stmt)
            await conn.commit()

    @staticmethod
    async def update_auth_pass_by_email(data: dict):
        """
        data = {
        "new_data": str,
        "email": str,
        }
        """
        async with async_engine.connect() as conn:
            stmt = text('UPDATE "auth" SET password=:new_data WHERE email=:email')
            stmt = stmt.bindparams(new_data=data["new_data"], email=data["email"])
            await conn.execute(stmt)
            await conn.commit()

    @staticmethod
    async def update_auth_pass_by_id(data: dict):
        """
        data = {
        "new_data": str,
        "user_id": int,
        }
        """
        async with async_engine.connect() as conn:
            stmt = text('UPDATE "auth" SET password=:new_data WHERE user_id=:user_id')
            stmt = stmt.bindparams(new_data=data["new_data"], email=data["user_id"])
            await conn.execute(stmt)
            await conn.commit()

    @staticmethod
    async def delete_user_by_id(data: dict):
        """
        data = {
        "user_id": int,
        }
        """
        async with async_engine.connect() as conn:
            stmt = text('DELETE FROM "user" WHERE id=:user_id')
            stmt = stmt.bindparams(user_id=data["user_id"])
            await conn.execute(stmt)
            await conn.commit()
