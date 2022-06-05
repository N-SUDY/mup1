import datetime
import motor.motor_asyncio
from pyrogram import Client
from sample_config import Config
from pyrogram.types import Message


class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.USERS

    def new_user(self, id):
        return dict(id=id, thumbnail=None)

    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)

    async def is_user_exist(self, id):
        user = await self.col.find_one({"id": int(id)})
        return True if user else False

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        await self.col.delete_many({"id": int(user_id)})

    async def set_thumbnail(self, id, thumbnail):
        await self.col.update_one({"id": id}, {"$set": {"thumbnail": thumbnail}})

    async def get_thumbnail(self, id):
        user = await self.col.find_one({"id": int(id)})
        return user.get("thumbnail", None)


async def AddUser(bot: Client, update: Message):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)


db = Database(Config.DATABASE_URL, Config.DATABASE_NAME)