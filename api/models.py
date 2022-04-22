from django.db import models
from django.http import Http404
from mptt.models import MPTTModel, TreeForeignKey


class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    content = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['created']

    @classmethod
    def get_post_or_404(cls, post_id):
        try:
            return cls.objects.get(pk=post_id)
        except cls.DoesNotExist:
            raise Http404


class Comment(MPTTModel):

    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField("Комментарий", blank=False)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    parent = TreeForeignKey('self', verbose_name="Родитель", on_delete=models.DO_NOTHING,
                            blank=True, null=True)

    class MPTTMeta:
        order_insertion_by = ['created']
        parent_attr = 'parent'

    def __str__(self):
        return f"Comment {self.content}"

    @classmethod
    def get_comment_or_404(cls, comment_id, post_id):
        try:
            return cls.objects.get(pk=comment_id, post__id=post_id)
        except cls.DoesNotExist:
            raise Http404
