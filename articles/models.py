from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Author(BaseModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    description = models.TextField()
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Article(BaseModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='articles')
    image = models.ImageField(upload_to='articles/', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class Comment(BaseModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField()

    def __str__(self):
        return f"Comment by {self.name} on {self.article.title}"
