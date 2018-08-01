from django.db import models
from user.models import User

# Create your models here.

# 文章详情信息表
class Post(models.Model):
    class Meta:
        db_table = "post"

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, null=False)
    pubdate = models.DateTimeField(null=False)
    # 外键，从post要查作者, 查内容，migrate会生成author_id字段
    author = models.ForeignKey(User)

    def __repr__(self):
        # self.content可以访问Content实例,内容访问是self.content.content
        return "<Post {} {} {} {}>".format(
            self.id, self.title, self.author_id, self.content.content
        )

    __str__ = __repr__

# 文章内容表
class Content(models.Model):
    class Meta:
        db_table = "content"

    # 不写主键会自动创建一个自增主键
    post = models.OneToOneField(Post)  # 一对一的关系，一篇文章对应一个作者，会有一个外键引用post.id
    content = models.TextField(null=False)

    def __repr__(self):
        return "<Content {} {}>".format(self.post.id, self.content[:20])

    __str__ = __repr__