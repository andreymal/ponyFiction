from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from ponyFiction.models import Author, Character, CharacterGroup, Category, Classifier, Rating, Series, Story, Chapter, Comment, BetaReading


class StoryAdmin(admin.ModelAdmin):
    exclude = ('vote',)

class ChapterAdmin(admin.ModelAdmin):
    raw_id_fields = ('story',)
    
admin.site.register(Story, StoryAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register([Character, CharacterGroup, Category, Classifier, Rating, Series, Comment, BetaReading])



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

admin.site.register(Author, AuthorAdmin)