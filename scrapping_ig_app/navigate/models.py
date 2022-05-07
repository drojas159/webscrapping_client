from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    profile_url = models.CharField(max_length=250)

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
    caption = models.CharField(max_length=1000)
    shortcode = models.CharField(max_length=60)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    text = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)

