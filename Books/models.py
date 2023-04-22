from django.db import models
# Wrap the update code in a transaction

class Book(models.Model):
        title = models.CharField(max_length=50)
        category = models.CharField(max_length=30,null=True,blank=True)
        auther = models.CharField(max_length=30 ,null=True,blank=True)
        book_path=models.CharField(max_length=400,null=True,blank=True)
        new_position = models.IntegerField(default=0)
        
        is_favorite = models.BooleanField(default=False)  
        
        
        def __str__(self):
            return self.title 

        
     