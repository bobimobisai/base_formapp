from DB.database import async_session_factory, async_engine
from sqlalchemy import select, update, insert, delete
from DB.models import Base, UserOrm, UserAuthOrm, TaskOrm


class AsyncOrm:

    @staticmethod
    async def option_insert(data: dict, table: Base):
        """
        table: Base = UserOrm, UserAuthOrm, TaskOrm
        data = {
            "column_name": arg(int, str, datetime, custom_tupe)
        }
        """
        async with async_session_factory() as session:
            query = insert(table).values(data)
            await session.execute(query)
            await session.commit()

    @staticmethod
    async def option_select(data: dict, table: Base, args: dict):
        """
        table: Base = UserOrm, UserAuthOrm, TaskOrm
        args = {
        "filter_by": str,
        "arg": int,
        }
        """
        async with async_session_factory() as session:
            query = select(table).where(args)
            await session.execute(query)
            await session.commit()

    @staticmethod
    async def option_update(data: dict, table: Base, args: dict):
        """
        table: Base = UserOrm, UserAuthOrm, TaskOrm
        data = {
            "column_name": arg(int, str, datetime, custom_tupe)
        }
        args = {
        "filter_by": str,
        "arg": int,
        }
        """
        async with async_session_factory() as session:
            query = update(table).values(data).where(args)
            await session.execute(query)
            await session.commit()

    @staticmethod
    async def option_delete(table: Base, args: dict):
        """
        table: Base = UserOrm, UserAuthOrm, TaskOrm
        args = {
        "arg": int,
        }
        """
        async with async_session_factory() as session:
            query = delete(table).where(args)
            await session.execute(query)
            await session.commit()

    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def insert_user(data: dict, table: Base = UserOrm):
        """
        data = {
        "user_name": str,
        "email": str
        }
        """
        async with async_session_factory() as session:
            user = table(user_name=data["user_name"], email=data["email"])
            session.add(user)
            await session.commit()

    @staticmethod
    async def insert_auth(data: dict, table: Base = UserAuthOrm):
        """
        data = {
        "user_id": int,
        "email": str,
        "password": str
        }
        """
        async with async_session_factory() as session:
            auth = table(
                user_id=data["user_id"], email=data["email"], password=data["password"]
            )
            session.add(auth)
            await session.commit()

    @staticmethod
    async def insert_user_auth(
        data: dict, table_user: Base = UserOrm, table_auth: Base = UserAuthOrm
    ):
        """
        data = {
        "user_name": str,
        "email": str,
        "password": str
        }
        """
        async with async_session_factory() as session:
            user = table_user(user_name=data["user_name"], email=data["email"])
            session.add(user)
            await session.flush()
            await session.refresh(user)  # вернет айдишник после инсерта, До комита
            auth = table_auth(
                user_id=user.id, email=data["email"], password=data["password"]
            )
            session.add(auth)
            await session.flush()
            await session.commit()

    @staticmethod
    async def select_user_by_id(data: dict, table: Base = UserOrm):
        """
        data = {
        "user_id": int,
        }
        """
        async with async_session_factory() as session:
            query = select(table).where(table.id == data["user_id"])
            result = await session.execute(query)
            users = result.scalars().fetchall()
            return users[0]

    @staticmethod
    async def select_user_by_email(data: dict, table: Base = UserOrm):
        """
        data = {
        "email": str,
        }
        """
        async with async_session_factory() as session:
            query = select(table).where(table.email == data["email"])
            result = await session.execute(query)
            users = result.scalars().fetchall()
            return users[0]

    @staticmethod
    async def update_user_name_by_id(data: dict, table: Base = UserOrm):
        """
        data = {
        "user_id": int,
        "user_name": str,
        }
        """
        async with async_session_factory() as session:
            user = await session.get(entity=table, ident=data["user_id"])
            user.user_name = data["user_name"]
            # await session.refresh(user) если данные изменились то откат
            await session.commit()

    @staticmethod
    async def update_user_name_by_email(data: dict, table: Base = UserOrm):
        """
        data = {
        "email": str,
        "user_name": str,
        }
        """
        async with async_session_factory() as session:
            query = (
                update(table)
                .values(user_name=data["user_name"])
                .where(table.email == data["email"])
            )
            await session.execute(query)
            await session.commit()

    @staticmethod
    async def update_user_email_by_id(
        data: dict, t_usr: Base = UserOrm, t_aut: Base = UserAuthOrm
    ):
        """
        data = {
        "email": str,
        "user_id": int,
        }
        """
        async with async_session_factory() as session:
            async with session.begin():
                user = await session.get(t_usr, data["user_id"], with_for_update=True)
                auth = await session.get(t_aut, data["user_id"], with_for_update=True)

                user.email = data["email"]
                auth.email = data["email"]

                session.add(user)
                session.add(auth)

            await session.commit()

    @staticmethod
    async def update_task_stastus(data: dict, table: Base = TaskOrm):
        """
        data = {
            "status": StatusTask.PENDING,
            "performer_id": int(user_id)}
        """
        async with async_session_factory() as session:
            query = (
                update(table)
                .values(status=data["status"])
                .where(table.performer_id == data["performer_id"])
            )
            await session.execute(query)
            await session.commit()

    @staticmethod
    async def insert_task(data: dict, table: Base = TaskOrm):
        """
        data = {
        "title": str,
        "description": str256,
        "deadline": datetime.datetime(2024, 2, 29),
        "performer_id" : int
        """
        async with async_session_factory() as session:
            # query = insert(table).values(data)
            task = table(
                title=data["title"],
                description=data["description"],
                deadline=data["deadline"],
                performer_id=data["performer_id"],
            )
            session.add(task)
            # await session.execute(query)
            await session.commit()
