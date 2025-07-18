from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ...

    def __str__(self):
        return f"{self.username}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    image = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    winner = models.CharField(max_length=50, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

    def highest_bid(self):
        highest = self.bids.order_by('-bid').first()
        return highest.bid if highest else None


class Bid(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    bid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"${self.bid} on {self.item.title} by {self.user}"


class Comment(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user} on {self.item}: {self.comment}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'item')

    def __str__(self):
        return f"{self.user.username} is watching {self.item.title}"
