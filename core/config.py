from pydantic import BaseSettings, AnyHttpUrl

app_desc = """
    🎉 用户登录 🎉
    ✨ 账号: admin ✨
    ✨ 密码: 123456 ✨
"""


class Settings(BaseSettings):
    """ 应用配置 """
    APP_TITLE: str = '烽火酒店管理系统'
    APP_API_PREFIX: str = ''
    APP_DEBUG: bool = True
    APP_CORS: bool = True
    APP_DESC: str = app_desc
    APP_VERSION: str = '0.0.1'
    APP_STATIC_DIR: str = 'static'
    APP_GLOBAL_ENCODING: str = 'utf-8'
    APP_CORS_ORIGINS: list[AnyHttpUrl] = ['http://127.0.0.1:3000', 'http://127.0.0.1:5179']
    APP_IS_RELOAD: bool = True

    """ 数据源配置 """
    REDIS_URI: str = 'redis://:123456@127.0.0.1:6379/1'
    DATABASE_URI: str = 'mysql+pymysql://root:123456@127.0.0.1:3306/beacon_hotel-system?charset=utf8'
    DATABASE_ECHO: bool = False
    REDIS_EXPIRE: int = 30 * 60 * 1000

    """ JWT配置 """
    JWT_SAVE_KEY = 'auth'
    JWT_ALGORITHM: str = 'HS256'
    # JWT_SECRET_KEY: str = secrets.token_urlsafe(32)  # 密钥(每次重启服务密钥都会改变, token解密失败导致过期, 可设置为常量)
    JWT_SECRET_KEY: str = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
    JWT_EXPIRE: int = 30 * 60 * 1000
    JWT_IS_BEARER: bool = True

    class Config:
        env_fil: str = '.env'
        case_sensitive: bool = True


settings = Settings()
