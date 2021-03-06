import datetime

from django.db import models

from vip.models import Vip




class User(models.Model):
    SEX = (
        ('male', '男性'),
        ('female', '女性'),
    )

    LOCATION = (
        ('bj', '北京'),
        ('sh', '上海'),
        ('gz', '广州'),
        ('sz', '深圳'),
        ('cd', '成都'),
        ('xa', '西安'),
        ('wh', '武汉'),
    )
    phonenum = models.CharField(max_length=16, unique=True, verbose_name='手机号')
    nickname = models.CharField(max_length=32, unique=True, verbose_name='昵称')
    sex = models.CharField(max_length=8, choices=SEX, verbose_name='性别')
    birth_year = models.IntegerField(default=2000, verbose_name='出生年')
    birth_month = models.IntegerField(default=1, verbose_name='出生月')
    birth_day = models.IntegerField(default=1, verbose_name='出生日')
    avatar = models.CharField(max_length=256, verbose_name='个人头像的 URL 地址')
    location = models.CharField(max_length=16, choices=LOCATION, verbose_name='常居地')
    vip_id = models.IntegerField(default=1, verbose_name='会员等级')

    @property
    def age(self):
        """用户年龄"""
        today = datetime.date.today()
        birthday = datetime.date(self.birth_year, self.birth_month, self.birth_day)
        return (today - birthday).days // 365

    @property
    def profile(self):
        """用户资料"""
        if not hasattr(self, '_profile'):
            # get_or_create()  返回的是tuple,：(对象, 是否是创建的)
            self._profile, _ = Profile.get_or_create(id=self.id)
        return self._profile

    @property
    def vip(self):
        """用户对应的vip对象"""
        if not hasattr(self, '_vip'):
            self._vip = Vip.get(pk=self.vip_id)
        return self._vip

    class Meta:
        db_table = 'user'


class Profile(models.Model):
    """个人资料"""
    SEX = (
        ('male', '男性'),
        ('female', '女性'),
    )

    LOCATION = (
        ('bj', '北京'),
        ('sh', '上海'),
        ('gz', '广州'),
        ('sz', '深圳'),
        ('cd', '成都'),
        ('xa', '西安'),
        ('wh', '武汉'),
    )

    dating_sex = models.CharField(max_length=8, choices=SEX, verbose_name='匹配的性别')
    location = models.CharField(max_length=16, choices=LOCATION, verbose_name='目标城市')

    min_distance = models.IntegerField(default=1, verbose_name='最小查找范围')
    max_distance = models.IntegerField(default=10, verbose_name='最大查找范围')

    min_dating_age = models.IntegerField(default=18, verbose_name='最小交友年龄')
    max_dating_age = models.IntegerField(default=50, verbose_name='最大交友年龄')

    vibration = models.BooleanField(default=True, verbose_name='开启震动')
    only_matche = models.BooleanField(default=True, verbose_name='不让为匹配的人看我的相册')
    auto_play = models.BooleanField(default=True, verbose_name='自动播放视频')

    class Meta:
        db_table = 'profile'
