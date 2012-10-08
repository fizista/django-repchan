# -*- encoding: utf-8
from django.contrib import admin
from repchan.tests.repchantest.models import AuthorAlias, Author, Section, \
                                             Chapter, Page, Book

class AuthorAliasAdmin(admin.ModelAdmin):
    pass

class AuthorAdmin(admin.ModelAdmin):
    pass

class SectionAdmin(admin.ModelAdmin):
    pass

class ChapterAdmin(admin.ModelAdmin):
    pass

class PageAdmin(admin.ModelAdmin):
    pass

class BookAdmin(admin.ModelAdmin):
    # The admin panel should edit only the title and author  of the book
    #exclude = ('log',)
    pass



admin.site.register(AuthorAlias, AuthorAliasAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Book, BookAdmin)
