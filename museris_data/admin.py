from .models import (
    DataObject, DataObjectImage, DataObjectProperty, DataObjectLatLong,
    Institution, Person, PersonProperty, DataObjectPerson
)
from django.contrib import admin
from django.db.models import Count
from . import VerboseForeignKeyRawIdWidget


class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', )

admin.site.register(Institution, InstitutionAdmin)


class DataObjectImageInline(admin.TabularInline):
    model = DataObjectImage
    extra = 0


class DataObjectPropertyInline(admin.TabularInline):
    model = DataObjectProperty
    extra = 0


class DataObjectLatLongInline(admin.TabularInline):
    model = DataObjectLatLong
    extra = 0


class DataObjectPersonInline(admin.TabularInline):
    model = DataObjectPerson
    extra = 0
    raw_id_fields = ('person', )

    # makes the person fk clickable
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in self.raw_id_fields:
            kwargs.pop("request", None)
            type = db_field.rel.__class__.__name__
            if type in ("ManyToOneRel", "OneToOneRel"):
                kwargs['widget'] = VerboseForeignKeyRawIdWidget(
                    db_field.rel, self.admin_site)
            return db_field.formfield(**kwargs)
        return super(DataObjectPersonInline, self).formfield_for_dbfield(db_field, **kwargs)


def object_filter(property_):
    class ObjectsWithPropertyFilter(admin.SimpleListFilter):
        title = 'has %s' % property_

        # Parameter for the filter that will be used in the URL query.
        parameter_name = 'has_%s' % property_

        def lookups(self, request, model_admin):
            return (
                ('yes', 'Yes'),
                ('no', 'No'),
            )

        def queryset(self, request, queryset):
            if self.value() == 'yes':
                return queryset.annotate(prop_count=Count(property_)).filter(prop_count__gt=0)
            if self.value() == 'no':
                return queryset.annotate(prop_count=Count(property_)).filter(prop_count=0)
    return ObjectsWithPropertyFilter


class DataObjectAdmin(admin.ModelAdmin):
    list_display = ('object_id', '__unicode__', 'institution', )
    list_filter = ('institution', object_filter('images'), object_filter('coords'), object_filter('people'))
    search_fields = ('properties__value', 'properties__key', )
    inlines = [DataObjectImageInline, DataObjectPropertyInline, DataObjectLatLongInline, DataObjectPersonInline]

admin.site.register(DataObject, DataObjectAdmin)


class PersonPropertyInline(admin.TabularInline):
    model = PersonProperty
    extra = 0


class PersonAdmin(admin.ModelAdmin):
    list_display = ('object_id', 'name')
    search_fields = ('properties__key', 'properties__value', 'name', )
    inlines = [PersonPropertyInline, ]

admin.site.register(Person, PersonAdmin)
