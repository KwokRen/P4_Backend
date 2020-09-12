from django.conf.urls import url
from rest_framework import routers
from apps.api.views import TaskViewSet
router = routers.DefaultRouter()
router.register(r'tasks/', TaskViewSet, basename='tasks')
# custom_urlpatterns = [
#    url(r'categories/(?P<category_pk>\d+)/recipes$', CategoryRecipes.as_view(), name='category_recipes'),
#    url(r'categories/(?P<category_pk>\d+)/recipes/(?P<pk>\d+)$', SingleCategoryRecipe.as_view(),
#        name='single_category_recipe'),
# ]
urlpatterns = router.urls
# urlpatterns += custom_urlpatterns