from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Event, Organizers, Visited, Planed, Comments, Category, User

# Inline для организаторов
class OrganizersInline(admin.TabularInline):
    model = Organizers
    extra = 1  # Количество дополнительных пустых строк
    verbose_name = "Организатор"
    verbose_name_plural = "Организаторы"

# Inline для посетителей
class VisitedInline(admin.TabularInline):
    model = Visited
    extra = 1
    verbose_name = "Посетитель"
    verbose_name_plural = "Посетители"

# Inline для планировщиков
class PlanedInline(admin.TabularInline):
    model = Planed
    extra = 1
    verbose_name = "Планировщик"
    verbose_name_plural = "Планировщики"

# Inline для комментариев
class CommentsInline(admin.TabularInline):
    model = Comments
    extra = 1
    verbose_name = "Комментарий"
    verbose_name_plural = "Комментарии"


# Настройка админки для события
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    # Добавляем inline
    inlines = [
        OrganizersInline,
        VisitedInline,
        PlanedInline,
        CommentsInline,
    ]
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('username',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )

    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Отображаем в списке id и name
    search_fields = ('name',)  # Добавляем возможность поиска по полю name
    list_filter = ('name',)  # Добавляем фильтрацию по полю name


admin.site.register(Category, CategoryAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Event, EventAdmin)
