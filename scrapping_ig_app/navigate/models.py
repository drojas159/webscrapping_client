from django.db import models

class Catalog (models.Model):
    name = models.CharField(max_length=60)
    parent = models.ForeignKey("Catalog", on_delete=models.CASCADE, null=True)
    variable = models.CharField(unique = True,max_length=60)
    description = models.TextField(max_length=200,null=True)

class User(models.Model):
    username = models.CharField(max_length=50)
    profile_url = models.CharField(max_length=250)
    user_following = models.ManyToManyField('self')
    is_reviewed = models.BooleanField (default=False)
    number_posts = models.IntegerField(null=True)
    number_followers = models.IntegerField(null=True)
    number_following = models.IntegerField(null=True)
    user_public_name = models.CharField(max_length=250, null=True)
    user_description = models.CharField(max_length=800, null=True)
    user_other_url = models.CharField(max_length=600, null=True) 
    
    def save_user(self):
        if (User.objects.filter(username=self.username).count()==0):
            self.save()

class ScraperUser(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    state = models.BooleanField(default=True)

    def save_user(self):
    
        if (ScraperUser.objects.filter(username=self.username).count()==0):
            self.save()
        else:
            scraper_user = ScraperUser.objects.get(username=self.username)
            scraper_user.password = self.password
            scraper_user.state=True
            scraper_user.save()
            active_users = ScraperUser.objects.filter(state=1).exclude( username = self.username);
            active_users.update(state=0)

class Publication(models.Model):
    publication_url = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_reviewed = models.BooleanField (default=False)
    number_likes = models.IntegerField(null=True)
    publication_date = models.DateField(null=True)

    def save_publication(self):
        if (Publication.objects.filter(publication_url=self.publication_url).count()==0):
            self.save()

class Image (models.Model):
    image_link = models.CharField(max_length=600, null=True)
    content = models.CharField(max_length=600, null=True)
    image_type = models.ForeignKey(Catalog, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    publication = models.ForeignKey(Publication,on_delete=models.CASCADE, null=True)

    def save_image(self):
        if (Image.objects.filter(image_link=self.image_link).count()==0):
            self.save()
            
class Comment(models.Model):
    text = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_url = models.CharField(max_length=300,blank=True)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    is_reviewed = models.BooleanField (default=False)
    comment_date = models.DateField(null=True)

    def save_comment(self):
        if (Comment.objects.filter(comment_url=self.comment_url).count()==0):
            self.save()

