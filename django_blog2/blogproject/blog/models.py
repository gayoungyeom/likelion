from django.db import models

# 게시글과 댓글은 1:N 구조


class Post(models.Model):  # 게시글
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    pub_date = models.DateTimeField('date published')
    body = models.TextField()

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:20]


class Comment(models.Model):  # 댓글
    # 게시글이 삭제되면 댓글이 삭제되도록 설정
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.content
