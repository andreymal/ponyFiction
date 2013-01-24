from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from ponyFiction.stories.models import Author, User, Character, CharacterGroup, Category, Classifier, Size, Rating, Series, Story, Chapter, Comment, BetaReading

"""
class StoryAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    fields = ('title','summary','notes',('rating','size'),('finished','freezed','original'),'authors')  
    search_fields = ['title', 'summary', 'totes']
    filter_horizontal = ('authors',)
    radio_fields = {'size': admin.HORIZONTAL, 'rating' : admin.HORIZONTAL} 
admin.site.register(Story, StoryAdmin)
"""

models = [Character, CharacterGroup, Category, Classifier, Size, Rating, Series, Story, Chapter, Comment, BetaReading]



class AuthorChangeForm(UserChangeForm):

    class Meta:
        model = Author

class AuthorAdmin(UserAdmin):
    form = AuthorChangeForm
   
    list_display = ('username', 'email', 'last_name', 'first_name', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': (
                'first_name', 'last_name', 'email', 'bio', 'jabber', 'skype', 'tabun', 'forum', 'vk'
            )}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (('Groups'), {'fields': ('groups',)}),
    )

admin.site.unregister(User)
admin.site.register(models)
admin.site.register(Author, AuthorAdmin)