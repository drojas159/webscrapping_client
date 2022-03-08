from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    profile_url = models.CharField(max_length=250)

class ScraperUser(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    state = models.BooleanField(default=True)

    def save_user(self):
        
        if (ScraperUser.objects.filter(username=self.username).count()==0):
            print(self.username, self.password)
            self.save()
        else:
            scraper_user = ScraperUser.objects.get(username=self.username)
            scraper_user.password = self.password
            scraper_user.save()
        
    
    



